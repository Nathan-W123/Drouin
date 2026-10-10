"""What-if refits for the decision-maker: refit the current assignment set with some peaks removed
(or only some branches kept) and report rms and constants, without changing the run state.

  python -m assign.whatif <case> <seed> <arm> [--drop 14,27] [--only-dJ 1]
"""
import argparse
import csv
import os

import numpy as np
from .engine import Run


def add_candidates(assign, rdir, pmin=None, items=(), default_accept=False, nocontest=True):
    """Add proposal candidates to an assignment dict (trial only)."""
    import csv, os
    from .match import parse_key
    a = {p: list(k) for p, k in assign.items()}
    for r in csv.DictReader(open(os.path.join(rdir, "proposal.csv"))):
        tag = f"{r['key']}@{r['peak']}"
        ok = tag in items or (default_accept and r["default"] == "accept") or \
            (pmin is not None and float(r["P"]) >= pmin and (not nocontest or float(r["contest"]) <= 0.05))
        if not ok:
            continue
        k = parse_key(r["key"])
        if any(k in v for v in a.values()):
            continue
        a.setdefault(int(r["peak"]), []).append(k)
    return a


def whatif(run, drop=(), only_dJ=None, release=(), base=None):
    from .engine import _with_trial
    assign = {p: ks for p, ks in (base or run.assign).items() if p not in drop
              and (only_dJ is None or all(k[0] - k[3] == only_dJ for k in ks))}
    model = run.model
    for idp in release:
        model = _with_trial(model, model.get(idp))
    r, res, chi = run.fit(model=model, assign=assign)
    z = np.array([v["z"] for v in res.values()])
    return r, res, z, assign


def _bad_fit(r, res):
    """A trial fit whose z values cannot be trusted: not converged, or non-physical residuals."""
    return r is None or not r.ok or not res or max(abs(v["z"]) for v in res.values()) > 1e4


def grow_consistent(run, base, zmax=4.0, order=None):
    """Robust alternative used when the joint trial fit diverges: start from the current assignments and
    add the trial lines one at a time (in the given order), keeping a line only if the fit converges and
    every line stays within |z| <= zmax. A line is reported as removed only with the z of a *converged*
    fit (z=nan if its own addition made the fit diverge)."""
    cur = {p: list(ks) for p, ks in run.assign.items()}
    added = [(p, k) for p, ks in base.items() for k in ks if k not in run.assign.get(p, [])]
    if order:
        rank = {pk: i for i, pk in enumerate(order)}
        added.sort(key=lambda pk: rank.get(pk, 1e9))
    removed = []
    for p, k in added:
        trial = {q: list(v) for q, v in cur.items()}
        trial.setdefault(p, []).append(k)
        r, res, chi = run.fit(assign=trial)
        if _bad_fit(r, res):
            removed.append((p, [k], float("nan")))
            continue
        worst = max(abs(v["z"]) for v in res.values())
        if worst > zmax:
            removed.append((p, [k], res.get(p, {}).get("z", float("nan"))))
            continue
        cur = trial
    r, res, chi = run.fit(assign=cur)
    z = np.array([v["z"] for v in res.values()])
    kept = {p: [k for k in ks if k not in run.assign.get(p, [])] for p, ks in cur.items()}
    return {p: ks for p, ks in kept.items() if ks}, removed, float(np.sqrt(np.mean(z ** 2)))


def prune_inconsistent(run, base, zmax=4.0, max_steps=300, order=None):
    """Remove *added* lines one at a time (largest |z| first) while any added line has |z| > zmax.
    Only z values of converged fits are used: if a trial fit diverges, switch to grow_consistent."""
    cur = {p: list(ks) for p, ks in base.items()}
    removed = []
    for _ in range(max_steps):
        r, res, chi = run.fit(assign=cur)
        if _bad_fit(r, res):
            kept, rem, rms = grow_consistent(run, base, zmax, order)
            return kept, removed + rem, rms
        added = [p for p in cur if any(k not in run.assign.get(p, []) for k in cur[p])]
        bad = [p for p in added if p in res and abs(res[p]["z"]) > zmax]
        if not bad:
            break
        worst = max(bad, key=lambda p: abs(res[p]["z"]))
        removed.append((worst, [k for k in cur[worst] if k not in run.assign.get(worst, [])], res[worst]["z"]))
        keep = [k for k in cur[worst] if k in run.assign.get(worst, [])]
        if keep:
            cur[worst] = keep
        else:
            del cur[worst]
    z = np.array([v["z"] for v in res.values()])
    kept = {p: [k for k in ks if k not in run.assign.get(p, [])] for p, ks in cur.items()}
    return {p: ks for p, ks in kept.items() if ks}, removed, float(np.sqrt(np.mean(z ** 2)))


def consistent_subset(run, base, target=1.2, max_steps=200):
    """Starting from base (current assignments + trial additions), repeatedly remove the *added* line
    with the largest |z| until the weighted rms <= target. Returns (kept_added, removed)."""
    added = {p: [k for k in ks if k not in run.assign.get(p, [])] for p, ks in base.items()}
    added = {p: ks for p, ks in added.items() if ks}
    cur = {p: list(ks) for p, ks in base.items()}
    removed = []
    for _ in range(max_steps):
        r, res, chi = run.fit(assign=cur)
        z = {p: v["z"] for p, v in res.items()}
        rms = float(np.sqrt(np.mean([x * x for x in z.values()])))
        if rms <= target:
            break
        cand = [p for p in added if p in cur and any(k not in run.assign.get(p, []) for k in cur[p])]
        if not cand:
            break
        worst = max(cand, key=lambda p: abs(z.get(p, 0)))
        removed.append((worst, [k for k in cur[worst] if k not in run.assign.get(worst, [])], z.get(worst)))
        keep = [k for k in cur[worst] if k in run.assign.get(worst, [])]
        if keep:
            cur[worst] = keep
        else:
            del cur[worst]
    kept = {p: [k for k in ks if k not in run.assign.get(p, [])] for p, ks in cur.items()}
    return {p: ks for p, ks in kept.items() if ks}, removed, rms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case"); ap.add_argument("seed", type=int); ap.add_argument("arm")
    ap.add_argument("--drop", default="")
    ap.add_argument("--only-dJ", type=int, default=None)
    ap.add_argument("--release", default="", help="comma-separated IDPARs to release (trial)")
    ap.add_argument("--add-round", default=None, help="round dir whose proposal candidates are added")
    ap.add_argument("--add-p", type=float, default=None, help="add candidates with P >= this (uncontested)")
    ap.add_argument("--add-defaults", action="store_true", help="add the default-accepted candidates")
    ap.add_argument("--add", default="", help="';'-separated key@peak items to add")
    ap.add_argument("--subset", type=float, default=None, help="find the consistent subset of the additions (target rms)")
    ap.add_argument("--prune", type=float, default=None, help="remove added lines while any has |z| > this")
    ap.add_argument("--worst", type=int, default=8)
    ap.add_argument("--loo", action="store_true", help="leave-one-out: chi2 drop when each peak is removed")
    a = ap.parse_args()
    run = Run(a.case, a.seed, a.arm)
    drop = {int(x) for x in a.drop.split(",") if x}
    rel = [int(x) for x in a.release.split(",") if x]
    base = None
    if a.add_round:
        base = add_candidates(run.assign, a.add_round, a.add_p, [x for x in a.add.split(";") if x], a.add_defaults)
    order = None
    if a.add_round:
        rows = sorted(csv.DictReader(open(os.path.join(a.add_round, "proposal.csv"))), key=lambda r: -float(r["P"]))
        order = [(int(r["peak"]), tuple(int(x) for x in r["key"].split())) for r in rows]
    if (a.subset is not None or a.prune is not None) and base is not None:
        from .engine import _with_trial
        for idp in rel:  # pruning must use the same trial model as the plain what-if fit
            run.model = _with_trial(run.model, run.model.get(idp))
        kept, removed, rms = (consistent_subset(run, base, a.subset) if a.subset is not None
                              else prune_inconsistent(run, base, a.prune, order=order))
        print(f"consistent subset: kept {sum(len(v) for v in kept.values())} added lines, removed {len(removed)}, rms {rms:.3f}")
        for p, ks, z in removed:
            print(f"   removed peak {p:4d} {';'.join(' '.join(map(str, k)) for k in ks):<28s} z {z:+.1f}")
        print("KEPT " + ";".join(f"{' '.join(map(str, k))}@{p}" for p, ks in kept.items() for k in ks))
        return
    r, res, z, assign = whatif(run, drop, a.only_dJ, rel, base)
    print(f"lines {len(res)}  fit ok {r.ok}  weighted rms {np.sqrt(np.mean(z**2)):.3f}  median |z| {np.median(np.abs(z)):.2f}")
    for p in r.params.params:
        print(f"   {p.idpar:>8d} {p.label:8s} {p.value: .8e} +- {r.errors.get(p.idpar, float('nan')):.2e}")
    worst = sorted(res.items(), key=lambda kv: -abs(kv[1]["z"]))[:a.worst]
    for pid, v in worst:
        print(f"   worst peak {pid:4d} {';'.join(' '.join(map(str, k)) for k in assign[pid]):<28s} res {v['res']:+.4f} MHz z {v['z']:+.1f}")
    if a.loo:
        chi0 = float(np.sum(z ** 2))
        out = []
        for pid in assign:
            r2, res2, z2, _ = whatif(run, drop | {pid}, a.only_dJ, rel, base)
            out.append((chi0 - float(np.sum(z2 ** 2)), pid, np.sqrt(np.mean(z2 ** 2)) if len(z2) else 0))
        out.sort(reverse=True)
        print("leave-one-out: chi2 drop when removed (top 12)")
        for d, pid, rms in out[:12]:
            print(f"   peak {pid:4d} {';'.join(' '.join(map(str, k)) for k in assign[pid]):<28s} dchi2 {d:12.1f}  rms without {rms:.2f}")


if __name__ == "__main__":
    main()
