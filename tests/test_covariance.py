"""Check that our linearised covariance reproduces SPFIT's parameter uncertainties,
with and without Gaussian priors."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from assign import pickett as pk
from assign.model import load_case, official_params, Model, P
from assign.testcase import read_lin_rows, group_blends
from assign.predict import Predictor


def run(case, prior_rel=None, fmax=1e6):
    cfg = load_case(case)
    off = official_params(cfg)
    ps = []
    for idp, (v, s, lab) in off.items():
        pr = abs(v) * prior_rel if (prior_rel and idp in cfg["start_params"]) else pk.FREE_ERR
        ps.append(P(idp, lab, v, v, pr, "float"))
    m = Model(cfg, ps)
    peaks = [p for p in group_blends(read_lin_rows(cfg, 0)) if p["freq"] <= fmax]
    pr = Predictor(cfg, 0, fmax)
    pred = pr.predict(m)
    peaks = [p for p in peaks if all(k in pred.index for k in p["labels"])
             and abs(p["freq"] - np.mean([pred.freq[pred.index[k]] for k in p["labels"]])) < max(20 * p["err"], 2)]
    rows = [dict(up=k[:3], lo=k[3:], freq=p["freq"], err=p["err"]) for p in peaks for k in p["labels"]]
    fit = pk.spfit(m.to_parfile(), rows)
    pred = pr.predict(m, [(tuple(p["labels"]), p["err"]) for p in peaks])
    ours = np.sqrt(np.diag(pred.cov))
    print(f"{case} prior={prior_rel} lines={len(peaks)} rms={fit.rms:.3f}")
    worst = 0
    for j, idp in enumerate(pred.ids):
        r = ours[j] / fit.errors[idp]
        worst = max(worst, abs(np.log(r)))
        if j < 8:
            print(f"   {idp:>8d} {m.get(idp).label:8s} spfit {fit.errors[idp]:.4e}  ours {ours[j]:.4e}  ratio {r:.3f}")
    print(f"   max |ratio-1| over {len(pred.ids)} params: {np.exp(worst) - 1:.3f}")
    return np.exp(worst) - 1


if __name__ == "__main__":
    assert run("so2") < 0.05
    assert run("so2", prior_rel=1e-6) < 0.05
    # Known limitation: for H2CO the finite-difference Jacobian misestimates the uncertainties of the
    # weakly determined K-dependent terms (Delta_K, H_K, L_K...) by up to ~25%, because their effect on
    # a-type Delta-Ka=0 lines is below SPCAT's 1e-4 MHz output resolution. The loop therefore uses
    # SPCAT's own propagation for line uncertainties (validated by Monte Carlo refits in
    # test_sigma_montecarlo.py); this number is reported, not asserted.
    print(f"h2co parameter-level max deviation (informational): {run('h2co'):.2f}")
    print("OK")
