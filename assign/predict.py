"""Line predictions with honest uncertainties.

sigma_pred^2 = J Cov J^T  +  sum_k c_k^2
  * J        : d(freq)/d(param) for the parameters in the fit, by finite differences of SPCAT runs
  * Cov      : (Ja^T W Ja + P0^-1)^-1 -- the linearised posterior of the SPFIT fit (Gaussian priors P0
               on the starting constants, W = 1/err^2 of assigned lines).  This reproduces SPFIT's own
               parameter errors (checked in tests) and is needed because SPCAT caps printed
               uncertainties at ~100 MHz.
  * c_k      : the frequency contribution of every higher-order term NOT yet in the model, evaluated
               at its order-of-magnitude scale (model error / truncation error).
"""
import numpy as np

from . import pickett as pk
from .testcase import int_text


class Prediction:
    def __init__(self, keys, freq, lgint, J, ids, cov, sig_par, sig_model):
        self.keys = keys
        self.index = {k: i for i, k in enumerate(keys)}
        self.freq, self.lgint, self.J, self.ids, self.cov = freq, lgint, J, ids, cov
        self.sig_par, self.sig_model = sig_par, sig_model
        self.sigma = np.sqrt(sig_par ** 2 + sig_model ** 2)


class Predictor:
    def __init__(self, cfg, fmin, fmax, target_shift=300.0):
        self.cfg, self.fmin, self.fmax = cfg, fmin, fmax
        self.int = int_text(cfg, fmax_ghz=fmax * 1.02 / 1000.0)
        self.steps = {}
        self.contrib = {}  # idpar -> {key: contribution at scale}
        self.target = target_shift

    def _cat(self, model, extra=None):
        cat = pk.spcat(model.current_parfile(extra), self.int)
        m = (cat.freq >= self.fmin) & (cat.freq <= self.fmax)
        return {k: (f, li) for k, f, li, mm in zip(cat.keys(), cat.freq, cat.lgint, m) if mm}

    def _shift(self, base, model, idp, h):
        cur = model.get(idp).value if idp in {p.idpar for p in model.floating()} else 0.0
        c = self._cat(model, {idp: cur + h})
        return np.array([c[k][0] - base[k][0] if k in c else np.nan for k in base])

    def absent_contributions(self, model, base):
        """Contribution of each absent parameter at its scale; computed once and cached."""
        keys = list(base)
        for p in model.absent():
            if p.idpar not in self.contrib:
                d = self._shift(base, model, p.idpar, p.scale)
                self.contrib[p.idpar] = dict(zip(keys, np.nan_to_num(d)))
        out = np.zeros(len(keys))
        for p in model.absent():
            c = self.contrib[p.idpar]
            out += np.array([c.get(k, 0.0) for k in keys]) ** 2
        return np.sqrt(out)

    def predict(self, model, assigned=(), var_text=None):
        """assigned: list of (keys_tuple, err) per assigned peak (blends average their rows).
        var_text: SPFIT's posterior .var for the same assignments.  When given, SPCAT's own
        uncertainty propagation (exact derivatives + full correlation matrix) is used for lines with
        0.002 < sigma < 99 MHz; our linear propagation is used outside that range, where SPCAT's
        printed value is capped or below its output resolution (validated by Monte Carlo refits,
        tests/test_sigma_montecarlo.py)."""
        base = self._cat(model)
        keys = list(base)
        freq = np.array([base[k][0] for k in keys])
        lgint = np.array([base[k][1] for k in keys])
        fl = model.floating()
        J = np.zeros((len(keys), len(fl)))
        for j, p in enumerate(fl):
            # step chosen afresh every call (deterministic, independent of history)
            h = abs(p.value) * 1e-4 if p.value else (p.scale or 1e-6)
            for _ in range(3):
                d = self._shift(base, model, p.idpar, h)
                m = np.nanpercentile(np.abs(d), 99) if np.isfinite(d).any() else 0.0
                if m > 0 and 0.3 < m / self.target < 3:
                    break
                h = h * (self.target / m) if m > 1e-3 else h * 1000
            self.steps[p.idpar] = h
            # central difference: cancels the second-order (nonlinear) term, so large steps can be
            # used and the 1e-4 MHz output precision of SPCAT is not limiting
            dm = self._shift(base, model, p.idpar, -h)
            J[:, j] = np.nan_to_num((d - dm) / (2 * h))
        idx = {k: i for i, k in enumerate(keys)}
        rows, w = [], []
        for ks, err in assigned:
            ii = [idx[k] for k in ks if k in idx]
            if ii:
                rows.append(J[ii].mean(axis=0))
                w.append(1.0 / err ** 2)
        info = np.zeros((len(fl), len(fl)))
        if rows:
            Ja = np.array(rows)
            info += Ja.T @ (Ja * np.array(w)[:, None])
        for j, p in enumerate(fl):
            if p.prior < 1e30:
                info[j, j] += 1.0 / p.prior ** 2
        # scale for numerical stability before inverting
        d = np.sqrt(np.maximum(np.diag(info), 1e-300))
        cov = np.linalg.pinv(info / np.outer(d, d), rcond=1e-14) / np.outer(d, d)
        sig_par = np.sqrt(np.maximum(np.einsum("ij,jk,ik->i", J, cov, J), 0))
        if var_text:
            c = pk.spcat_var(var_text, self.int)
            e = dict(zip(c.keys(), c.err))
            se = np.array([e.get(k, -1.0) for k in keys])
            use = (se > 0.002) & (se < 99)
            sig_par = np.where(use, se, sig_par)
        sig_model = self.absent_contributions(model, base)
        return Prediction(keys, freq, lgint, J, [p.idpar for p in fl], cov, sig_par, sig_model)
