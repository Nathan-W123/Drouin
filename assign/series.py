"""Series-coherence diagnostic (a Loomis-Wood analysis in numbers).

A wrong set of constants shifts the lines of one branch *systematically*: for an R-branch the error is
nearly proportional to frequency, so true lines of one series share a common fractional offset
r = (obs - pred)/pred, while chance coincidences scatter uniformly over the window.  For each series
(dJ, Ka', Ka", Kc-parities) this tool finds the largest set of candidates (one per J) whose r agree
within a tolerance, and computes how many such agreements would be expected by chance.

  python -m assign.series runs/<run>/round_NN [--min 3]
"""
import argparse
import csv
import math
import os

import numpy as np

from .plots import series_key


def analyse(rows, assigned_r=None, min_members=3, tol_frac=0.03):
    """rows: candidate dicts from proposal.csv. Returns list of coherent chains, most significant first."""
    groups = {}
    for r in rows:
        if float(r["P"]) < 0.01:
            continue
        k = tuple(int(x) for x in r["key"].split())
        groups.setdefault(series_key(k), []).append(r)
    out = []
    for g, rs in groups.items():
        items = []
        for r in rs:
            pf, of, s = float(r["pred_freq"]), float(r["obs_freq"]), float(r["pred_sigma"])
            if pf <= 0:
                continue
            items.append(dict(row=r, J=int(r["key"].split()[3]), r=(of - pf) / pf, sr=s / pf,
                              er=float(r["obs_err"]) / pf))
        if len({it["J"] for it in items}) < min_members:
            continue
        best = None
        for seed in items:
            tol = max(tol_frac * seed["sr"], 3 * seed["er"], 2e-6)
            members = {}
            for it in items:
                if abs(it["r"] - seed["r"]) < tol:
                    if it["J"] not in members or abs(it["r"] - seed["r"]) < abs(members[it["J"]]["r"] - seed["r"]):
                        members[it["J"]] = it
            if len(members) < min_members:
                continue
            # chance expectation: per J, candidates in window * (2 tol / window width)
            expected = 0.0
            for J in {it["J"] for it in items}:
                nJ = sum(1 for it in items if it["J"] == J)
                width = 2 * 4 * np.median([it["sr"] for it in items if it["J"] == J])
                expected += min(1.0, nJ * 2 * tol / max(width, 1e-12))
            n = len(members)
            # Poisson tail probability of >= n coincidences
            p = 1 - sum(math.exp(-expected) * expected ** k / math.factorial(k) for k in range(n))
            cand = dict(series=g, r0=seed["r"], tol=tol, members=sorted(members.values(), key=lambda m: m["J"]),
                        n=n, expected=expected, p_chance=max(p, 1e-300))
            if best is None or (cand["n"], -cand["p_chance"]) > (best["n"], -best["p_chance"]):
                best = cand
        if best:
            out.append(best)
    out.sort(key=lambda c: c["p_chance"])
    return out


def report(chains, top=25):
    L = []
    for c in chains[:top]:
        g = c["series"]
        L.append(f"series dJ={g[0]} Ka'={g[1]} Ka\"={g[2]} parity={g[3]},{g[4]}: {c['n']} coherent members, "
                 f"r0={c['r0']:+.6f} tol={c['tol']:.1e}, expected by chance {c['expected']:.2f}, "
                 f"P(chance)={c['p_chance']:.1e}")
        for m in c["members"]:
            r = m["row"]
            L.append(f"    {r['cid']} {r['key']:<14s} peak {r['peak']:>4s}  r={m['r']:+.6f}  z={float(r['z']):+.2f}  "
                     f"P={float(r['P']):.2f}  default={r['default']}")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rdir")
    ap.add_argument("--min", type=int, default=3)
    ap.add_argument("--top", type=int, default=25)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(os.path.join(a.rdir, "proposal.csv"))))
    txt = report(analyse(rows, min_members=a.min), a.top)
    open(os.path.join(a.rdir, "series.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
