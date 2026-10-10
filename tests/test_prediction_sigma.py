"""Validate predicted line uncertainties against SPCAT's own propagation from SPFIT's posterior
.var file (which includes the full correlation matrix)."""
import sys, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from assign import pickett as pk
from assign.model import load_case, official_params, Model, P
from assign.testcase import read_lin_rows, group_blends
from assign.predict import Predictor


def run(case, fmax=1e6, nlines=None, seed=0):
    cfg = load_case(case)
    off = official_params(cfg)
    m = Model(cfg, [P(i, l, v, v, pk.FREE_ERR, "float") for i, (v, s, l) in off.items()])
    pr = Predictor(cfg, 0, fmax)
    pred = pr.predict(m)
    peaks = [p for p in group_blends(read_lin_rows(cfg, 0)) if p["freq"] <= fmax
             and all(k in pred.index for k in p["labels"])
             and abs(p["freq"] - np.mean([pred.freq[pred.index[k]] for k in p["labels"]])) < max(20 * p["err"], 2)]
    if nlines:  # a sparser data set gives larger, more interesting prediction errors
        peaks = [peaks[i] for i in np.random.default_rng(seed).choice(len(peaks), nlines, replace=False)]
    rows = [dict(up=k[:3], lo=k[3:], freq=p["freq"], err=p["err"]) for p in peaks for k in p["labels"]]
    d = tempfile.mkdtemp()
    fit = pk.spfit(m.to_parfile(), rows, workdir=d)
    open(os.path.join(d, "x.int"), "w").write(pr.int)
    pk._run(pk.SPCAT, d, ["x.var", "x.int"])
    cat = pk.read_cat(os.path.join(d, "x.cat"))
    for p in m.params:
        p.value = fit.params.get(p.idpar).value
    pred = pr.predict(m, [(tuple(p["labels"]), p["err"]) for p in peaks])
    ours, theirs = [], []
    for k, e in zip(cat.keys(), cat.err):
        if k in pred.index and 0.002 < e < 99:
            ours.append(pred.sig_par[pred.index[k]]); theirs.append(e)
    r = np.array(ours) / np.array(theirs)
    q = np.percentile(np.abs(np.log(r)), [50, 95, 99])
    print(f"{case} lines in fit={len(peaks)}  compared {len(r)} predictions (0.002<err<99 MHz): "
          f"|ln ratio| median {q[0]:.3f}, 95% {q[1]:.3f}, 99% {q[2]:.3f}")
    return q


if __name__ == "__main__":
    ok = True
    for case, n in (("so2", None), ("so2", 120), ("h2co", None), ("h2co", 80)):
        q = run(case, nlines=n)
        ok &= q[1] < 0.10
    print("OK" if ok else "FAILED")
