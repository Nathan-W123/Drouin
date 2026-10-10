"""Joint-consistency of default/high-P candidates split by branch and J range (decision aid)."""
import csv
import sys

import numpy as np

from .engine import Run
from .whatif import add_candidates, whatif


def main(case, seed, rnd, release="", pmin=None):
    R = f"runs/{case}_s{seed}_ai/round_{int(rnd):02d}"
    rows = list(csv.DictReader(open(R + "/proposal.csv")))
    rel = [int(x) for x in release.split(",") if x]
    sel = lambda r: r["default"] == "accept" or (pmin is not None and float(r["P"]) >= pmin and float(r["contest"]) <= 0.05)
    groups = [("R-branch", lambda k: k[0] - k[3] != 0),
              ("Q-branch J<=15", lambda k: k[0] == k[3] and k[0] <= 15),
              ("Q-branch 15<J<=25", lambda k: k[0] == k[3] and 15 < k[0] <= 25),
              ("Q-branch J>25", lambda k: k[0] == k[3] and k[0] > 25)]
    for lab, g in groups:
        items = [f"{r['key']}@{r['peak']}" for r in rows if sel(r) and g(list(map(int, r["key"].split())))]
        if not items:
            continue
        run = Run(case, int(seed), "ai")
        base = add_candidates(run.assign, R, None, items, False)
        r, res, z, a = whatif(run, release=rel, base=base)
        worst = sorted(res.items(), key=lambda kv: -abs(kv[1]["z"]))[:3]
        print(f"{lab:18s} add {len(items):3d}: lines {len(res)} rms {np.sqrt(np.mean(z ** 2)):.2f} worst "
              + ", ".join(f"{p}:{' '.join(map(str, a[p][0]))} z={v['z']:+.1f}" for p, v in worst))


if __name__ == "__main__":
    main(*sys.argv[1:4], *(sys.argv[4:5] or [""]), *([float(sys.argv[5])] if len(sys.argv) > 5 else []))
