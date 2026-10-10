"""Audit of the AI arm's departures from the rule-based defaults against the hidden truth."""
import csv
import glob
import json
import os
import sys
from collections import Counter

from . import score
from .match import parse_key
from .model import load_case


def audit(run):
    case, seed = run.split("_s")[0], int(run.split("_s")[1].split("_")[0])
    cfg = load_case(case)
    truth = score.load_truth(f"testcases/{case}_s{seed}")
    ok = lambda p, k: truth[p][0] == "true" and (k in truth[p][1] or score.degenerate_partner(k, truth[p][1], cfg))
    res = Counter()
    for f in sorted(glob.glob(f"runs/{run}/round_*/decisions_applied.csv")):
        rd = os.path.dirname(f)
        prop = {r["cid"]: r for r in csv.DictReader(open(os.path.join(rd, "proposal.csv")))} if os.path.exists(os.path.join(rd, "proposal.csv")) else {}
        outl = {r["peak"]: r for r in csv.DictReader(open(os.path.join(rd, "outliers.csv")))} if os.path.exists(os.path.join(rd, "outliers.csv")) else {}
        for r in csv.DictReader(open(f)):
            if r["source"] != "ai-override":
                continue
            if r["kind"] == "assign" and r["item"] in prop:
                p, k = int(prop[r["item"]]["peak"]), parse_key(prop[r["item"]]["key"])
                res[(f"assign {r['action']}", "candidate was correct" if ok(p, k) else "candidate was wrong")] += 1
            elif r["kind"] == "outlier" and r["item"] in outl:
                p = int(r["item"])
                keys = [parse_key(x) for x in outl[r["item"]]["keys"].split(";")]
                good = all(ok(p, k) for k in keys)
                res[(f"outlier {r['action']}", "line was correct" if good else "line was wrong")] += 1
            elif r["kind"] == "param":
                res[(f"param {r['action']}", "-")] += 1
    return res


if __name__ == "__main__":
    for run in sys.argv[1:]:
        print(run)
        for (a, b), n in sorted(audit(run).items()):
            print(f"   {a:18s} {b:24s} {n}")
