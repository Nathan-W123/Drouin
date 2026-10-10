"""Write an AI-arm decision file from a review (decision aid; every row carries a reason).

  python -m assign.decide <case> --accept defaults|defaults_P0.9|defaults_P0.5 --reason "..."
        [--release 3000,2100 --release-reason "..."] [--hold id:reason ...] [--reject key@peak:reason ...]
        [--outlier peak:action:reason ...] [--hyp rank:action:reason ...] [--stop "reason"] [--defer-reason "..."]
"""
import argparse
import csv
import os

from .engine import Run


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case"); ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--accept", default=None); ap.add_argument("--reason", default="")
    ap.add_argument("--release", default=""); ap.add_argument("--release-reason", default="")
    ap.add_argument("--hold", nargs="*", default=[]); ap.add_argument("--reject", nargs="*", default=[])
    ap.add_argument("--outlier", nargs="*", default=[]); ap.add_argument("--stop", default=None)
    ap.add_argument("--defer-reason", default="not in the jointly consistent set")
    ap.add_argument("--confirm", default="remaining rule defaults reviewed")
    a = ap.parse_args()
    run = Run(a.case, a.seed, "ai")
    rnd = run.round + 1
    R = os.path.join(run.dir, f"round_{rnd:02d}")
    out = []
    if a.accept:
        for k in [x for x in open(os.path.join(R, f"review_kept_{a.accept}.txt")).read().split(";") if x]:
            out.append(dict(kind="assign", item=k, action="accept", reason=a.reason))
    for x in a.reject:
        k, why = x.split(":", 1)
        out.append(dict(kind="assign", item=k, action="reject", reason=why))
    for idp in [x for x in a.release.split(",") if x]:
        out.append(dict(kind="param", item=idp, action="release", reason=a.release_reason))
    for x in a.hold:
        idp, why = x.split(":", 1)
        out.append(dict(kind="param", item=idp, action="hold", reason=why))
    for x in a.outlier:
        p, act, why = x.split(":", 2)
        out.append(dict(kind="outlier", item=p, action=act, reason=why))
    if a.stop:
        out.append(dict(kind="stop", item="stop", action="yes", reason=a.stop))
    out.append(dict(kind="all", item="assign", action="defer", reason=a.defer_reason))
    out.append(dict(kind="all", item="defaults", action="confirm", reason=a.confirm))
    os.makedirs(run.dec_dir, exist_ok=True)
    with open(os.path.join(run.dec_dir, f"round_{rnd:02d}.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["kind", "item", "action", "reason"]); w.writeheader(); w.writerows(out)
    print(f"wrote {len(out)} decisions for {a.case} round {rnd}")


if __name__ == "__main__":
    main()
