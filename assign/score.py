"""Score a run against the hidden truth (the only module that reads truth.csv).

Per round:
  coverage    = true peaks carrying at least one correct label / true peaks in the list
  precision   = correct (peak, label) pairs / all assigned pairs
  wrong       = assigned pairs that are not correct, split into: on distractor peaks (by source) and
                wrong label on a true peak
Final:
  constants of an unconstrained refit of the final assignments (priors removed, Kisiel's rule for
  final fits) compared with (a) the official CDMS constants and (b) an "oracle" fit of all true peaks
  in the list with their true labels and the same Hamiltonian terms.
"""
import csv
import glob
import json
import math
import os

import numpy as np

from . import pickett as pk
from .match import parse_key
from .model import Model, load_case, official_params


def load_truth(tc):
    truth = {}
    for r in csv.DictReader(open(os.path.join(tc, "truth.csv"))):
        if r["id"] == "0":
            continue
        truth[int(r["id"])] = (r["source"], {parse_key(s) for s in r["labels"].split(";") if s})
    return truth


_OFFCAT = {}


def official_freqs(cfg):
    """Official-constant frequencies of all ground-state transitions (cached)."""
    if cfg["key"] not in _OFFCAT:
        from .testcase import official_catalog_v
        cat = official_catalog_v(cfg, None, 0)
        _OFFCAT[cfg["key"]] = dict(zip(cat.keys(), cat.freq))
    return _OFFCAT[cfg["key"]]


def degenerate_partner(k, labels, cfg):
    """True if transition k is predicted (official constants) within 0.1 Doppler FWHM of a true label of
    the peak: an unresolved, physically present component that the expert .lin labels only once."""
    from .testcase import doppler_fwhm
    off = official_freqs(cfg)
    if k not in off:
        return False
    return any(l in off and abs(off[k] - off[l]) < 0.1 * doppler_fwhm(off[l], cfg) for l in labels)


def score_assignments(assign, truth, cfg=None):
    n_true = sum(1 for s, _ in truth.values() if s == "true")
    pairs = [(p, k) for p, ks in assign.items() for k in ks]
    correct = [(p, k) for p, k in pairs if truth[p][0] == "true" and k in truth[p][1]]
    wrong_dis = {}
    wrong_label = 0
    for p, k in pairs:
        if (p, k) in correct:
            continue
        if truth[p][0] == "true":
            wrong_label += 1
        else:
            wrong_dis[truth[p][0]] = wrong_dis.get(truth[p][0], 0) + 1
    covered = {p for p, k in correct}
    n_degen = 0
    if cfg is not None:
        n_degen = sum(1 for p, k in pairs if (p, k) not in correct and truth[p][0] == "true"
                      and degenerate_partner(k, truth[p][1], cfg))
    return dict(n_true=n_true, n_pairs=len(pairs), n_correct=len(correct), n_covered=len(covered), n_degenerate_partner=n_degen,
                precision_phys=(len(correct) + n_degen) / len(pairs) if pairs else float("nan"),
                coverage=len(covered) / n_true, precision=len(correct) / len(pairs) if pairs else float("nan"),
                wrong_on_distractors=sum(wrong_dis.values()), wrong_by_source=wrong_dis,
                wrong_label_on_true=wrong_label, n_peaks_assigned=len(assign))


def read_round_assign(rdir):
    path = os.path.join(rdir, "assignments.csv")
    if not os.path.exists(path):
        return None
    out = {}
    for r in csv.DictReader(open(path)):
        out[int(r["peak"])] = [parse_key(s) for s in r["keys"].split(";")]
    return out


def final_fit(run_dir, cfg, peaks, assign, from_start=False):
    """Unconstrained refit (priors removed) of an assignment set with the run's final Hamiltonian
    terms.  from_start: start from the official constants instead of the run's own solution, so the
    oracle fit converges independently (the least-squares optimum does not depend on the start)."""
    st = json.load(open(os.path.join(run_dir, "state.json")))
    model = Model.from_json(cfg, st["model"])
    if from_start:
        off = official_params(cfg)
        for p in model.floating():
            p.value = off[p.idpar][0] if p.idpar in off else 0.0
    for p in model.floating():
        p.prior = pk.FREE_ERR
    model_nitr = 50
    rows = []
    for pid, ks in sorted(assign.items(), key=lambda kv: peaks[kv[0]][0]):
        f, e = peaks[pid]
        for k in ks:
            rows.append(dict(up=k[:3], lo=k[3:], freq=f, err=e, wt=1.0 if len(ks) > 1 else None))
    r = pk.spfit(model.to_parfile(nitr=model_nitr), rows)
    return model, r


def compare_constants(cfg, fit, oracle):
    off = official_params(cfg)
    out = []
    for p in fit.params.params:
        if p.idpar not in off:
            continue
        ov, os_, lab = off[p.idpar]
        e = fit.errors.get(p.idpar, float("nan"))
        orc = oracle.params.get(p.idpar).value if oracle and oracle.params.get(p.idpar) else float("nan")
        orc_e = oracle.errors.get(p.idpar, float("nan")) if oracle else float("nan")
        out.append(dict(idpar=p.idpar, label=lab, value=p.value, sigma=e, official=ov, official_sigma=os_,
                        rel_dev=(p.value - ov) / ov if ov else float("nan"),
                        dev_in_sigma=(p.value - ov) / math.hypot(e, os_) if np.isfinite(e) else float("nan"),
                        oracle=orc, oracle_sigma=orc_e,
                        dev_from_oracle_sigma=(p.value - orc) / math.hypot(e, orc_e) if np.isfinite(e) and np.isfinite(orc_e) else float("nan")))
    return out


def score_run(run_dir):
    name = os.path.basename(run_dir.rstrip("/"))
    case, seed = name.split("_s")[0], int(name.split("_s")[1].split("_")[0])
    cfg = load_case(case)
    tc = os.path.join(pk.ROOT, "testcases", f"{case}_s{seed}")
    truth = load_truth(tc)
    peaks = {int(r["id"]): (float(r["freq"]), float(r["err"])) for r in csv.DictReader(open(os.path.join(tc, "peaks.csv")))}
    st = json.load(open(os.path.join(run_dir, "state.json")))
    per_round = []
    for rdir in sorted(glob.glob(os.path.join(run_dir, "round_*"))):
        a = read_round_assign(rdir)
        if a is None:
            continue
        m = score_assignments(a, truth, cfg)
        m["round"] = int(rdir[-2:])
        h = next((x for x in st["history"] if x["round"] == m["round"]), {})
        m.update(rms=h.get("rms"), n_float=h.get("n_float"), overrides=h.get("overrides", 0))
        per_round.append(m)
    final_assign = {int(k): [tuple(x) for x in v] for k, v in st["assign"].items()}
    fin = score_assignments(final_assign, truth, cfg)
    model, fit = final_fit(run_dir, cfg, peaks, final_assign) if final_assign else (None, None)
    # oracle: every true peak in the list with its true labels, same Hamiltonian terms
    oracle_assign = {p: sorted(l) for p, (s, l) in truth.items() if s == "true"}
    _, ofit = final_fit(run_dir, cfg, peaks, oracle_assign, from_start=True)
    consts = compare_constants(cfg, fit, ofit) if fit is not None and fit.ok else []
    # decision provenance (AI arm)
    n_ai_override = sum(m.get("overrides") or 0 for m in per_round)
    n_human = 0
    for f in glob.glob(os.path.join(run_dir, "round_*", "decisions_applied.csv")):
        n_human += sum(1 for r in csv.DictReader(open(f)) if r.get("source") == "human")
    out = dict(run=name, case=case, seed=seed, arm=name.split("_", 2)[2], rounds=len(per_round), per_round=per_round,
               final=fin, final_fit_ok=bool(fit and fit.ok), final_rms=fit.rms if fit else None,
               oracle_rms=ofit.rms if ofit else None, n_free_params=len(model.floating()) if model else 0,
               constants=consts, ai_overrides=n_ai_override, human_corrections=n_human)
    os.makedirs(os.path.join(pk.ROOT, "results"), exist_ok=True)
    with open(os.path.join(pk.ROOT, "results", f"{name}.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    return out


def summary_line(s):
    f = s["final"]
    return (f"{s['run']:<26s} rounds {s['rounds']:2d}  coverage {100 * f['coverage']:5.1f}%  precision "
            f"{100 * f['precision'] if f['n_pairs'] else float('nan'):5.1f}% (phys {100 * f['precision_phys'] if f['n_pairs'] else float('nan'):5.1f}%)  pairs {f['n_pairs']:4d} "
            f"wrong: distractors {f['wrong_on_distractors']:3d} {f['wrong_by_source']} wrong-label {f['wrong_label_on_true']:3d}  "
            f"final rms {s['final_rms'] if s['final_rms'] is not None else float('nan'):.3f}  overrides {s['ai_overrides']}")


if __name__ == "__main__":
    import sys
    for d in sys.argv[1:]:
        s = score_run(d)
        print(summary_line(s))
        for c in s["constants"][:8]:
            print(f"    {c['label']:8s} {c['value']: .9e} +- {c['sigma']:.2e}  official {c['official']: .9e}  "
                  f"rel {c['rel_dev']:+.2e}  dev/sigma {c['dev_in_sigma']:+.1f}  vs oracle {c['dev_from_oracle_sigma']:+.1f}")
