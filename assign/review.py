"""One-command review of an AI-arm round (decision aid; reads only what the loop sees).

  python -m assign.review <case> <seed>     (reviews the pending round)
Writes runs/<case>_s<seed>_ai/round_NN/review.txt and review_kept_*.txt (key@peak lists).
"""
import os
import sys

import numpy as np

from .engine import Run, _with_trial
from .series import analyse, report
from .whatif import add_candidates, grow_consistent, whatif
import csv


def main(case, seed):
    run = Run(case, int(seed), "ai")
    rnd = run.round + 1
    R = os.path.join(run.dir, f"round_{rnd:02d}")
    out = []
    pr = lambda *a: out.append(" ".join(str(x) for x in a))
    pr(open(os.path.join(R, "summary.md")).read().split("## Outliers")[0].strip())
    rows = list(csv.DictReader(open(os.path.join(R, "proposal.csv"))))
    orow = list(csv.DictReader(open(os.path.join(R, "outliers.csv"))))
    pr("\nOUTLIERS (top 8):")
    for r in orow[:8]:
        pr(f"  peak {r['peak']:>4s} {r['keys']:<28s} t={float(r['t']):+.1f} h={float(r['leverage']):.2f} default={r['default']}")
    # forward selection of releases with plausibility cap (same as rules+), on current assignments
    run.s.update(release_multi=True)
    prow = run.param_table()
    rel = [int(r["idpar"]) for r in prow if r["default"] == "release"]
    pr("\nRELEASE forward selection (<=10x scale):", [(r["label"], round(r["dchi2"], 1), f"{r['ratio']:.2g}x") for r in prow if r["default"] == "release"] or "none")
    pr("  other trials:", [(r["label"], round(r["dchi2"], 1), f"{r['ratio']:.2g}x") for r in prow if r["default"] != "release"][:6])
    m0 = run.model
    for idp in rel:
        run.model = _with_trial(run.model, run.model.get(idp))
    r, res, z, a = whatif(run)
    pr(f"  current {len(res)} lines: rms {np.sqrt(np.mean(z ** 2)):.3f} with releases " + (f"(without: {run.history[-1]['rms']:.3f})" if run.history else ""))
    order = [(int(x["peak"]), tuple(int(v) for v in x["key"].split())) for x in sorted(rows, key=lambda x: -float(x["P"]))]
    for lab, pmin, dflt in (("defaults", None, True), ("defaults+P>=0.9", 0.9, True), ("defaults+P>=0.5", 0.5, True)):
        base = add_candidates(run.assign, R, pmin, (), dflt)
        n_add = sum(len(v) for v in base.values()) - sum(len(v) for v in run.assign.values())
        if n_add == 0:
            pr(f"\nJOINT {lab}: nothing to add")
            continue
        kept, removed, rms = grow_consistent(run, base, 4.0, order=order)  # P-ordered, converged fits only
        nk = sum(len(v) for v in kept.values())
        pr(f"\nJOINT {lab}: {n_add} added -> kept {nk}, removed {len(removed)}, rms {rms:.3f}")
        for p, ks, zz in removed[:10]:
            pr(f"   removed {p:>4d} {' '.join(map(str, ks[0])):<22s} z={zz:+.1f}")
        tag = lab.replace("+", "_").replace(">=", "")
        open(os.path.join(R, f"review_kept_{tag}.txt"), "w").write(";".join(f"{' '.join(map(str, k))}@{p}" for p, ks in kept.items() for k in ks))
    run.model = m0
    # forward selection of releases on the JOINT set (current + defaults [+P>=0.9]), then grow
    from .model import order as _order
    for lab, pmin in (("defaults", None), ("defaults+P>=0.9", 0.9)):
        base = add_candidates(run.assign, R, pmin, (), True)
        model, chosen = m0, []
        r0, res0, chi0 = run.fit(model=model, assign=base)
        for _ in range(8):
            best = None
            maxo = max(_order(q.idpar) for q in model.floating())
            for p in model.absent():
                if _order(p.idpar) > maxo + 2:
                    continue
                rr, res, chi = run.fit(model=_with_trial(model, p), assign=base)
                if rr is None or not rr.ok:
                    continue
                v = rr.params.get(p.idpar).value
                if abs(v) > 10 * p.scale:
                    continue
                if best is None or chi < best[0]:
                    best = (chi, p, v)
            if best is None or chi0 - best[0] < 9:
                break
            chosen.append((best[1].label, best[1].idpar, round(chi0 - best[0], 1), f"{abs(best[2]) / best[1].scale:.2g}x"))
            model = _with_trial(model, best[1])
            chi0 = best[0]
        run.model = model
        kept, removed, rms = grow_consistent(run, base, 4.0, order=order)
        run.model = m0
        nk = sum(len(v) for v in kept.values())
        pr(f"\nJOINT-RELEASE {lab}: releases {[(c[0], c[2], c[3]) for c in chosen]} -> kept {nk}, removed {len(removed)}, rms {rms:.3f}")
        pr("   RELEASE_IDS " + ",".join(str(c[1]) for c in chosen))
        for p, ks, zz in removed[:8]:
            pr(f"   removed {p:>4d} {' '.join(map(str, ks[0])):<22s} z={zz:+.1f}")
        tag = "jr_" + lab.replace("+", "_").replace(">=", "")
        open(os.path.join(R, f"review_kept_{tag}.txt"), "w").write(";".join(f"{' '.join(map(str, k))}@{p}" for p, ks in kept.items() for k in ks))
    pr("\nSERIES (top 6):")
    pr(report(analyse(rows, min_members=4), 6).split("\n    ")[0] if False else "\n".join(l for l in report(analyse(rows, min_members=4), 6).splitlines() if l.startswith("series")))
    txt = "\n".join(out)
    open(os.path.join(R, "review.txt"), "w").write(txt + "\n")
    print(txt)
    print("\nRELEASES_SUGGESTED", ",".join(map(str, rel)))


if __name__ == "__main__":
    main(*sys.argv[1:3])
