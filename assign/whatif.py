"""What-if refits for the decision-maker: refit the current assignment set with some peaks removed
(or only some branches kept) and report rms and constants, without changing the run state.

  python -m assign.whatif <case> <seed> <arm> [--drop 14,27] [--only-dJ 1]
"""
import argparse
import numpy as np
from .engine import Run


def whatif(run, drop=(), only_dJ=None, release=()):
    from .engine import _with_trial
    assign = {p: ks for p, ks in run.assign.items() if p not in drop
              and (only_dJ is None or all(k[0] - k[3] == only_dJ for k in ks))}
    model = run.model
    for idp in release:
        model = _with_trial(model, model.get(idp))
    r, res, chi = run.fit(model=model, assign=assign)
    z = np.array([v["z"] for v in res.values()])
    return r, res, z, assign


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case"); ap.add_argument("seed", type=int); ap.add_argument("arm")
    ap.add_argument("--drop", default="")
    ap.add_argument("--only-dJ", type=int, default=None)
    ap.add_argument("--release", default="", help="comma-separated IDPARs to release (trial)")
    ap.add_argument("--worst", type=int, default=8)
    ap.add_argument("--loo", action="store_true", help="leave-one-out: chi2 drop when each peak is removed")
    a = ap.parse_args()
    run = Run(a.case, a.seed, a.arm)
    drop = {int(x) for x in a.drop.split(",") if x}
    rel = [int(x) for x in a.release.split(",") if x]
    r, res, z, assign = whatif(run, drop, a.only_dJ, rel)
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
            r2, res2, z2, _ = whatif(run, drop | {pid}, a.only_dJ, rel)
            out.append((chi0 - float(np.sum(z2 ** 2)), pid, np.sqrt(np.mean(z2 ** 2)) if len(z2) else 0))
        out.sort(reverse=True)
        print("leave-one-out: chi2 drop when removed (top 12)")
        for d, pid, rms in out[:12]:
            print(f"   peak {pid:4d} {';'.join(' '.join(map(str, k)) for k in assign[pid]):<28s} dchi2 {d:12.1f}  rms without {rms:.2f}")


if __name__ == "__main__":
    main()
