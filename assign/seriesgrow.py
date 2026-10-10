"""Decision aid: grow a jointly consistent assignment set from coherent series (optionally discarding the
current assignments, e.g. inconsistent bootstrap anchors).
  python -m assign.seriesgrow <case> <seed> [--fresh-start] [--pmax 1e-6] [--dJ 1] [--r0 X --rtol Y] [--release ids]"""
import argparse
import csv
import os

from .engine import Run, _with_trial
from .series import analyse
from .whatif import add_candidates, grow_consistent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case"); ap.add_argument("seed", type=int)
    ap.add_argument("--fresh-start", action="store_true"); ap.add_argument("--pmax", type=float, default=1e-6)
    ap.add_argument("--dJ", type=int, default=None); ap.add_argument("--r0", type=float, default=None)
    ap.add_argument("--rtol", type=float, default=1e-3); ap.add_argument("--release", default="")
    a = ap.parse_args()
    run = Run(a.case, a.seed, "ai")
    R = os.path.join(run.dir, f"round_{run.round + 1:02d}")
    rows = list(csv.DictReader(open(os.path.join(R, "proposal.csv"))))
    items, order = [], []
    for c in analyse(rows, min_members=4):
        g = c["series"]
        if c["p_chance"] > a.pmax or (a.dJ is not None and g[0] != a.dJ) or c["members"][0]["sr"] > 0.05:
            continue
        if a.r0 is not None and abs(c["r0"] - a.r0) > a.rtol:
            continue
        for m in c["members"]:
            r = m["row"]
            items.append(f"{r['key']}@{r['peak']}")
            order.append((int(r["peak"]), tuple(int(x) for x in r["key"].split())))
    if a.fresh_start:
        run.assign = {}
    for idp in [int(x) for x in a.release.split(",") if x]:
        run.model = _with_trial(run.model, run.model.get(idp))
    base = add_candidates(run.assign, R, None, items, False)
    kept, removed, rms = grow_consistent(run, base, 4.0, order)
    n = sum(len(v) for v in kept.values())
    print(f"{len(items)} series members -> kept {n}, removed {len(removed)}, rms {rms:.3f}")
    for p, ks, z in removed[:12]:
        print(f"   removed {p:>4d} {' '.join(map(str, ks[0])):<22s} z={z:+.1f}")
    open(os.path.join(R, "review_kept_series.txt"), "w").write(";".join(f"{' '.join(map(str, k))}@{p}" for p, ks in kept.items() for k in ks))


if __name__ == "__main__":
    main()
