"""Build a scorable, label-free test case from a CDMS .lin file.

Output directory testcases/<case>_s<seed>/ :
  peaks.csv      what the assignment loop sees: id, freq (MHz), err (MHz), lgint (log10 nm^2 MHz)
  truth.csv      HIDDEN, for scoring only: id, source, labels (';'-separated 6-tuples), true freq
  model.json     perturbed starting constants with priors (and absent higher-order terms)
  start.par      the same, as an SPFIT .par file (for inspection)
  testcase.json  settings and bookkeeping

Physics of the synthetic "observed" list
  * true lines   = measured ground-state frequencies from the expert .lin (labels removed).
                   Blends (successive .lin rows with identical freq/err) become one peak with
                   several labels.  Rows whose label is inconsistent with the official constants
                   by >20 sigma (e.g. CDMS 'difference' pseudo-lines) are not spectral peaks and
                   are excluded.
  * intensities  = SPCAT intensities from the official constants (300 K), summed over blend
                   components, with log-normal noise; distractor isotopologues are scaled by
                   natural abundance, vibrational satellites carry their Boltzmann factor.
  * frequency noise sigma = noise_scale * err is added, and the reported uncertainty is inflated
    to err*sqrt(1+noise_scale^2) so the list stays statistically self-consistent.
"""
import argparse
import csv
import json
import os
import shutil
import tempfile
import zlib

import numpy as np

from . import pickett as pk
from .model import load_case, rel, starting_model, official_params, scale

DEFAULTS = dict(
    seed=1,
    drop_frac=0.15,  # fraction of true lines removed
    noise_scale=1.0,  # added frequency noise in units of the line's measurement error
    int_noise_dex=0.15,  # log-normal intensity noise
    det_quantile=0.05,  # detection limit = this quantile of true-line intensities
    abc_lo=0.005, abc_hi=0.010, abc_prior=0.010,  # A,B,C perturbation and prior (relative)
    q_lo=0.10, q_hi=0.30, q_prior=0.50,  # quartic constants
    absent_factor=10.0,  # model-error prior for absent terms = factor * magnitude estimate
)


def doppler_fwhm(f_mhz, cfg):
    """Doppler FWHM (MHz) = 7.162e-7 * nu * sqrt(T/M)."""
    return 7.162e-7 * f_mhz * np.sqrt(cfg.get("temperature_K", 300.0) / cfg["mass_amu"])


def key_str(k):
    return " ".join(str(x) for x in k)


def read_lin_rows(cfg, v):
    lay = cfg["lin_layout"]
    rows = []
    for line in open(rel(cfg["truth_lin"])):
        if len(line) < 40:
            continue
        try:
            q = [int(line[3 * i:3 * i + 3]) if line[3 * i:3 * i + 3].strip() else 0 for i in range(12)]
            t = line[36:].split()
            f, e = float(t[0]), float(t[1])
        except (ValueError, IndexError):
            continue
        if q[lay["vu"]] != v or q[lay["vl"]] != v:
            continue
        if e < 0:  # wavenumber units
            f, e = f * pk.MHZ_PER_CM, -e * pk.MHZ_PER_CM
        f, e = f * scale(cfg), e * scale(cfg)  # blind cases: hidden overall scale
        rows.append((tuple(q[i] for i in lay["up"]) + tuple(q[i] for i in lay["lo"]), f, e))
    return rows


def group_blends(rows):
    """Successive rows with identical (freq, err) form one peak."""
    peaks = []
    for k, f, e in rows:
        if peaks and peaks[-1]["freq"] == f and peaks[-1]["err"] == e:
            peaks[-1]["labels"].append(k)
        else:
            peaks.append(dict(freq=f, err=e, labels=[k]))
    return peaks


def int_text(cfg, dipoles=None, fmax_ghz=None, tag=None):
    i = cfg["int"]
    dips = dipoles or i["dipoles"]
    s = f"{cfg['name']}\n0 {tag or i['tag']} {i['qrot']} 0 {i['fend']} -30.0 -30.0 {fmax_ghz or 3500.0} 300.0\n"
    return s + "".join(f" {d} {m}\n" for d, m in dips)


def dipoles_from_int(path):
    L = open(rel(path)).read().splitlines()
    return [(int(l.split()[0]), float(l.split()[1])) for l in L[2:] if l.split()]


def official_catalog_v(cfg, dipoles, vib):
    """Catalog for vibrational state `vib` of a multi-state official file."""
    par = pk.read_par(rel(cfg["official_var"]), cfg["official_nopt"])
    d = tempfile.mkdtemp()
    try:
        p = par.copy()
        for q in p.params:
            q.prior = 0.0
            q.value *= scale(cfg)
        p.write(os.path.join(d, "x.var"))
        open(os.path.join(d, "x.int"), "w").write(int_text(cfg, dipoles))
        pk._run(pk.SPCAT, d, ["x.var", "x.int"])
        return pk.read_cat(os.path.join(d, "x.cat"), vib=vib)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def build(case, **kw):
    cfg = load_case(case)
    s = dict(DEFAULTS, **{k: v for k, v in kw.items() if v is not None})
    secret = s.pop("secret_seed", None)  # blind cases: data/perturbation seed not known to the decision-maker
    ss = np.random.SeedSequence([secret if secret is not None else s["seed"], zlib.crc32(cfg["key"].encode())])
    rng_data, rng_const = [np.random.default_rng(x) for x in ss.spawn(2)]
    fmin, fmax = cfg["fmin_mhz"], cfg["fmax_mhz"]
    log = []

    # ---- true ground-state lines
    off = official_catalog_v(cfg, None, 0)
    offmap = {k: (f, li) for k, f, li in zip(off.keys(), off.freq, off.lgint)}
    peaks = [p for p in group_blends(read_lin_rows(cfg, 0)) if fmin <= p["freq"] <= fmax]
    true, excluded = [], []
    for p in peaks:
        fl = [offmap.get(k) for k in p["labels"]]
        if any(x is None for x in fl):
            excluded.append((p, "label not in official catalog"))
            continue
        fcalc = np.mean([x[0] for x in fl])
        if abs(p["freq"] - fcalc) > max(20 * p["err"], 2.0):
            excluded.append((p, f"obs-calc(official) = {p['freq'] - fcalc:.3f} MHz"))
            continue
        p["lgint"] = float(np.log10(np.sum([10 ** x[1] for x in fl])))
        p["source"] = "true"
        true.append(p)
    log.append(f"true peaks in range: {len(true)} (excluded {len(excluded)} rows/blends: "
               + "; ".join(f"{key_str(e[0]['labels'][0])} {e[1]}" for e in excluded[:20]) + ")")
    lg_true = np.array([p["lgint"] for p in true])
    i_det = float(np.quantile(lg_true, s["det_quantile"]))
    errs_true = np.array([p["err"] for p in true])

    # ---- drop lines
    keep = rng_data.random(len(true)) >= s["drop_frac"]
    dropped = [p for p, k in zip(true, keep) if not k]
    true = [p for p, k in zip(true, keep) if k]
    log.append(f"dropped {len(dropped)} true peaks; kept {len(true)}")
    n_true = len(true)

    # ---- distractors
    distract = []
    occupied = np.sort([p["freq"] for p in true])

    def too_close(f, e):
        """A distractor closer than the Doppler width (or 2 err) to an existing peak would not be
        resolved from it, so it is not added as a separate peak."""
        i = np.searchsorted(occupied, f)
        near = occupied[max(i - 1, 0):i + 1]
        return np.any(np.abs(near - f) < max(2 * e, doppler_fwhm(f, cfg)))

    for d in cfg["distractors"]:
        n_want = int(round(d["frac"] * n_true))
        cand = []
        if d["kind"] == "lin_state":
            cat = official_catalog_v(cfg, dipoles_from_int(d["int_file"]), d["v"])
            cm = {k: li for k, li in zip(cat.keys(), cat.lgint)}
            for p in group_blends(read_lin_rows(cfg, d["v"])):
                if fmin <= p["freq"] <= fmax and all(k in cm for k in p["labels"]):
                    p["lgint"] = float(np.log10(sum(10 ** cm[k] for k in p["labels"])) + np.log10(d["abundance"]))
                    cand.append(p)
        elif d["kind"] == "catalog":
            cat = pk.read_cat(rel(d["path"]))
            for k, f, li in zip(cat.keys(), cat.freq * scale(cfg), cat.lgint):
                if fmin <= f <= fmax:
                    cand.append(dict(freq=float(f), err=float(rng_data.choice(errs_true)), labels=[k],
                                     lgint=float(li + np.log10(d["abundance"]))))
        elif d["kind"] == "random":
            lo, hi = min(p["freq"] for p in true), max(p["freq"] for p in true)
            for _ in range(n_want):
                cand.append(dict(freq=float(rng_data.uniform(lo, hi)), err=float(rng_data.choice(errs_true)),
                                 labels=[], lgint=float(rng_data.choice(lg_true) + rng_data.normal(0, 0.3))))
        elig = [c for c in cand if c["lgint"] >= i_det]
        idx = rng_data.permutation(len(elig))
        chosen, n_close = [], 0
        for i in idx:
            if len(chosen) >= n_want:
                break
            c = elig[i]
            if too_close(c["freq"], c["err"]):
                n_close += 1
                continue
            c["source"] = d["label"]
            chosen.append(c)
            occupied = np.sort(np.append(occupied, c["freq"]))
        distract += chosen
        log.append(f"distractor {d['label']}: {len(cand)} candidates, {len(elig)} above detection limit, "
                   f"took {len(chosen)} (wanted {n_want}; skipped {n_close} unresolved from existing peaks)")

    # ---- noise and output
    allp = true + distract
    for p in allp:
        p["true_freq"] = p["freq"]
        p["freq"] = p["freq"] + rng_data.normal(0, s["noise_scale"] * p["err"])
        p["err_obs"] = p["err"] * np.sqrt(1 + s["noise_scale"] ** 2)
        p["lgint_obs"] = p["lgint"] + rng_data.normal(0, s["int_noise_dex"])
    allp.sort(key=lambda p: p["freq"])
    out = os.path.join(pk.ROOT, "testcases", f"{cfg['key']}_s{s['seed']}")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "peaks.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "freq", "err", "lgint"])
        for i, p in enumerate(allp):
            p["id"] = i + 1
            w.writerow([p["id"], f"{p['freq']:.6f}", f"{p['err_obs']:.6f}", f"{p['lgint_obs']:.3f}"])
    with open(os.path.join(out, "truth.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "source", "labels", "true_freq", "true_lgint"])
        for p in allp:
            w.writerow([p["id"], p["source"], ";".join(key_str(k) for k in p["labels"]),
                        f"{p['true_freq']:.6f}", f"{p['lgint']:.3f}"])
        for p in dropped:  # dropped true lines are recorded for completeness (id 0 = not in list)
            w.writerow([0, "dropped", ";".join(key_str(k) for k in p["labels"]), f"{p['freq']:.6f}", f"{p['lgint']:.3f}"])

    model = starting_model(cfg, rng_const, s)
    with open(os.path.join(out, "model.json"), "w") as f:
        json.dump(model.to_json(), f, indent=1)
    model.to_parfile(title=f"{cfg['name']} start s{s['seed']}").write(os.path.join(out, "start.par"))
    offp = official_params(cfg)
    hidden = [dict(idpar=p.idpar, label=p.label, start=p.value, official=offp[p.idpar][0], prior=p.prior)
              for p in model.floating()]
    with open(os.path.join(out, "truth_constants.json"), "w") as f:  # HIDDEN, scoring only
        json.dump(hidden, f, indent=1)
    meta = dict(case=cfg["key"], settings=s, detection_limit_lgint=i_det, n_peaks=len(allp),
                n_true=n_true, n_distractors=len(distract), log=log)
    with open(os.path.join(out, "testcase.json"), "w") as f:
        json.dump(meta, f, indent=1)
    return out, meta


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("case")
    for k, v in DEFAULTS.items():
        ap.add_argument(f"--{k}", type=type(v), default=None)
    a = vars(ap.parse_args())
    out, meta = build(a.pop("case"), **a)
    print(out)
    print("\n".join(meta["log"]))


if __name__ == "__main__":
    main()
