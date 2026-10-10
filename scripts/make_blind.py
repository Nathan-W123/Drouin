"""Build blind test cases. Molecule order, overall scale factor and the data/perturbation seed are drawn
from OS randomness and written only to hidden files (testcases/<case>_s1/truth_blind.json); nothing
secret is printed.  Usage: python3 scripts/make_blind.py 3 3 [first_index]   (n_so2 n_h2co; default first index 1)"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from assign.testcase import build  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = random.SystemRandom()
mols = ["so2"] * int(sys.argv[1]) + ["h2co"] * int(sys.argv[2])
rng.shuffle(mols)
first = int(sys.argv[3]) if len(sys.argv) > 3 else 1
for i, mol in enumerate(mols, first):
    name = f"blind{i}"
    cfg = json.load(open(os.path.join(ROOT, "cases", f"{mol}.json")))
    hidden = f"testcases/{name}_s1/truth_blind.json"
    cfg.update(name=name, description="blind test case", blind_truth=hidden)
    os.makedirs(os.path.join(ROOT, os.path.dirname(hidden)), exist_ok=True)
    secret = dict(molecule=mol, scale=round(rng.uniform(0.80, 1.25), 6), secret_seed=rng.randrange(10**9))
    json.dump(secret, open(os.path.join(ROOT, hidden), "w"))
    json.dump(cfg, open(os.path.join(ROOT, "cases", f"{name}.json"), "w"), indent=2)
    out, meta = build(name, seed=1, secret_seed=secret["secret_seed"])
    print(f"{name}: {meta['n_peaks']} peaks")
