"""Ground truth for prediction uncertainties: Monte Carlo refits.
Perturb the observed frequencies by their errors, refit with SPFIT, predict with SPCAT, and
compare the scatter of predicted frequencies with (a) our linear propagation and (b) SPCAT's."""
import sys, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from assign import pickett as pk
from assign.model import load_case, official_params, Model, P
from assign.testcase import read_lin_rows, group_blends
from assign.predict import Predictor

case, nl, nmc = (sys.argv[1] if len(sys.argv) > 1 else "so2"), 120, 40
cfg = load_case(case)
off = official_params(cfg)
m = Model(cfg, [P(i, l, v, v, pk.FREE_ERR, "float") for i, (v, s, l) in off.items()])
pr = Predictor(cfg, 0, 1e6)
pred0 = pr.predict(m)
peaks = [p for p in group_blends(read_lin_rows(cfg, 0)) if p["freq"] <= 1e6
         and all(k in pred0.index for k in p["labels"])
         and abs(p["freq"] - np.mean([pred0.freq[pred0.index[k]] for k in p["labels"]])) < max(20 * p["err"], 2)]
rng = np.random.default_rng(0)
peaks = [peaks[i] for i in rng.choice(len(peaks), nl, replace=False)]
# synthetic exact data from the official model so that the MC is unbiased
for p in peaks:
    p["f0"] = np.mean([pred0.freq[pred0.index[k]] for k in p["labels"]])
d = tempfile.mkdtemp()
open(os.path.join(d, "x.int"), "w").write(pr.int)
sims = []
for it in range(nmc):
    rows = [dict(up=k[:3], lo=k[3:], freq=p["f0"] + rng.normal(0, p["err"]), err=p["err"]) for p in peaks for k in p["labels"]]
    fit = pk.spfit(m.to_parfile(), rows, workdir=d)
    c = pk.read_cat(os.path.join(d, "x.cat")) if False else None
    pk._run(pk.SPCAT, d, ["x.var", "x.int"])
    cat = pk.read_cat(os.path.join(d, "x.cat"))
    sims.append(dict(zip(cat.keys(), cat.freq)))
    if it == 0:
        spcat_err = dict(zip(cat.keys(), cat.err))
pred = pr.predict(m, [(tuple(p["labels"]), p["err"]) for p in peaks])
keys = [k for k in pred.keys if all(k in s for s in sims) and 0.005 < spcat_err.get(k, 0) < 99]
mc = np.array([np.std([s[k] for s in sims], ddof=1) for k in keys])
ours = np.array([pred.sig_par[pred.index[k]] for k in keys])
theirs = np.array([spcat_err[k] for k in keys])
# with nmc=40, the MC sigma itself has ~11% relative scatter
for name, v in (("ours", ours), ("spcat", theirs)):
    q = np.percentile(np.abs(np.log(v / mc)), [50, 90, 95])
    print(f"{case}: {name:5s} vs Monte Carlo over {len(keys)} lines: |ln ratio| median {q[0]:.3f}  90% {q[1]:.3f}  95% {q[2]:.3f}")
for lo, hi in ((0, 1), (1, 10), (10, 100)):
    s = (mc >= lo) & (mc < hi)
    if s.sum():
        print(f"  MC sigma {lo:>3}-{hi:<3} MHz ({s.sum():4d} lines): median |ln(ours/mc)| {np.median(np.abs(np.log(ours[s]/mc[s]))):.3f}"
              f"   median |ln(spcat/mc)| {np.median(np.abs(np.log(theirs[s]/mc[s]))):.3f}")
predh = pr.predict(m, [(tuple(p["labels"]), p["err"]) for p in peaks], var_text=fit.var_text)
hyb = np.array([predh.sig_par[predh.index[k]] for k in keys])
q = np.percentile(np.abs(np.log(hyb / mc)), [50, 90, 95])
print(f"{case}: hybrid (used by the loop) vs Monte Carlo: |ln ratio| median {q[0]:.3f}  90% {q[1]:.3f}  95% {q[2]:.3f}")
