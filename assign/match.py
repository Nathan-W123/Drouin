"""Candidate matching between predicted and observed lines.

Probability model for one prediction i (frequency nu_i, uncertainty s_i, log intensity I_i) whose
window (|z| < n_win) contains peaks j:
    H0  : none of the peaks is line i (its line is missing from the list, or hidden)
    H_j : peak j is line i, all other peaks are unrelated
    r_j = p_have/(1-p_have) * [phi(z_j)/s_tot_j * N(dI_j; 0, s_I)] / [rho * h(I_obs_j)]
    P_j = r_j / (1 + sum_k r_k)
  rho   local density of unassigned peaks (per MHz), h = intensity density of all peaks (per dex),
  s_tot = sqrt(s_i^2 + err_j^2), dI = I_obs - I_pred,  s_I = intensity uncertainty (dex).
  p_have = probability that a predicted line above the detection limit is in the list; estimated from
  the data (fraction of well-predicted lines that have a counterpart, corrected for chance).
Two predictions that claim the same peak are a *blend* if their predicted separation is not
resolvable (|nu_i - nu_k| < 3 err_j + 3 sigma_sep, sigma_sep from the covariance); otherwise the
peak is *contested*.
"""
import itertools
import math

import numpy as np

SQ2PI = math.sqrt(2 * math.pi)


class Peaks:
    def __init__(self, ids, freq, err, lgint):
        o = np.argsort(freq)
        self.id, self.freq, self.err, self.lgint = ids[o], freq[o], err[o], lgint[o]
        self.pos = {int(i): n for n, i in enumerate(self.id)}
        hist, edges = np.histogram(self.lgint, bins=np.arange(self.lgint.min() - 1, self.lgint.max() + 1.25, 0.25))
        dens = np.convolve(hist, [0.25, 0.5, 0.25], mode="same") / (len(self.lgint) * 0.25)
        self._h = (edges[:-1] + 0.125, np.maximum(dens, 0.02))

    def h(self, lg):
        return np.interp(lg, *self._h)

    def window(self, lo, hi):
        return np.searchsorted(self.freq, lo), np.searchsorted(self.freq, hi, side="right")

    @classmethod
    def load(cls, path):
        d = np.genfromtxt(path, delimiter=",", names=True)
        return cls(d["id"].astype(int), d["freq"], d["err"], d["lgint"])


def key_str(k):
    return " ".join(str(x) for x in k)


def parse_key(s):
    return tuple(int(x) for x in s.split())


def _density(peaks, free_mask, f, half=5000.0):
    a, b = peaks.window(f - half, f + half)
    return (free_mask[a:b].sum() + 1) / (2 * half)


def usable(pred, settings):
    """Predictions that are in range and above the detection limit (with margin). The matching limit is
    the weakest observed peak when available (i_det_match), so very weak true lines are not excluded."""
    lim = settings.get("i_det_match", settings["i_det"])
    return np.where(pred.lgint >= lim - settings["int_margin"])[0]


def sep_sigma(pred, i, k):
    d = pred.J[i] - pred.J[k]
    return math.sqrt(max(d @ pred.cov @ d, 0) + (pred.sig_model[i] - pred.sig_model[k]) ** 2)


def estimate_p_have(pred, peaks, idx, free_mask, assigned_keys, settings):
    """Fraction of predictions with a counterpart, from predictions sharp enough that chance
    coincidences are rare (expected random matches < 0.1 per window)."""
    n, hit, chance = 0, 0, 0.0
    for i in idx:
        s = math.hypot(pred.sigma[i], np.median(peaks.err))
        rho = _density(peaks, np.ones_like(free_mask), pred.freq[i])
        lam = rho * 6 * s
        if lam > 0.1:
            continue
        n += 1
        chance += 1 - math.exp(-lam)
        if pred.keys[i] in assigned_keys:
            hit += 1
            continue
        a, b = peaks.window(pred.freq[i] - 3 * s, pred.freq[i] + 3 * s)
        if any(free_mask[j] and abs(peaks.lgint[j] - pred.lgint[i]) < 0.75 for j in range(a, b)):
            hit += 1
    if n < settings["p_have_min_n"]:
        return settings["p_have0"], n
    pr = chance / n
    return float(np.clip((hit / n - pr) / (1 - pr), 0.05, 0.95)), n


def candidates(pred, peaks, assigned_peaks, assigned_keys, rejected, settings):
    """Return (rows, info). rows: candidate (prediction, peak) pairs with probabilities, flags and
    the rule-based default action."""
    free = np.array([int(i) not in assigned_peaks for i in peaks.id])
    idx = [i for i in usable(pred, settings) if pred.keys[i] not in assigned_keys]
    p_have, n_cal = estimate_p_have(pred, peaks, usable(pred, settings), free, assigned_keys, settings)
    odds = p_have / (1 - p_have)
    sI, nwin = settings["sigma_I"], settings["n_win"]
    med_err = float(np.median(peaks.err))
    cand = {}  # (i, jpos) -> dict
    by_pred, n_unres = {}, 0
    for i in idx:
        s0 = math.hypot(pred.sigma[i], med_err)
        a, b = peaks.window(pred.freq[i] - nwin * s0 * 1.5, pred.freq[i] + nwin * s0 * 1.5)
        js = [j for j in range(a, b) if free[j]]  # previously rejected pairs are re-proposed (flagged)
        if len(js) > settings["max_in_window"]:
            n_unres += 1
            continue
        rho = _density(peaks, free, pred.freq[i])
        rs = []
        for j in js:
            st = math.hypot(pred.sigma[i], peaks.err[j])
            z = (peaks.freq[j] - pred.freq[i]) / st
            if abs(z) > nwin:
                continue
            dI = peaks.lgint[j] - pred.lgint[i]
            L = math.exp(-0.5 * z * z) / (SQ2PI * st) * math.exp(-0.5 * (dI / sI) ** 2) / (SQ2PI * sI)
            r = odds * L / (rho * peaks.h(peaks.lgint[j]))
            rs.append((j, z, dI, r, st))
        if not rs:
            continue
        tot = 1 + sum(x[3] for x in rs)
        by_pred[i] = []
        for j, z, dI, r, st in rs:
            c = dict(i=i, j=j, z=z, dI=dI, P=r / tot, n_win=len(rs), sig_tot=st)
            cand[(i, j)] = c
            by_pred[i].append(c)
    # claims per peak
    by_peak = {}
    for c in cand.values():
        by_peak.setdefault(c["j"], []).append(c)
    rows = []
    for i, cs in by_pred.items():
        cs.sort(key=lambda c: -c["P"])
        for rank, c in enumerate(cs):
            if c["P"] < settings["p_show"] and rank > 0:
                continue
            j = c["j"]
            others = [o for o in by_peak[j] if o["i"] != i]
            blend_with, contest = [], 0.0
            for o in others:
                k = o["i"]
                if o["P"] < 0.05:
                    continue
                sep = abs(pred.freq[i] - pred.freq[k])
                # a blend only if the two lines are *confidently* unresolved: closer than the Doppler
                # width (or 3 err for sub-Doppler measurements), including the separation uncertainty
                res = max(3 * peaks.err[j], settings["fwhm_factor"] * peaks.freq[j])
                if sep + 2 * sep_sigma(pred, i, k) < res:
                    blend_with.append(k)
                else:
                    contest = max(contest, o["P"])
            rival = max([o["P"] for o in cs if o is not c] or [0.0])
            flags = []
            if rival > 0.05:
                flags.append("multi")
            if contest > 0.05:
                flags.append("contested")
            if blend_with:
                flags.append("blend")
            if abs(c["dI"]) > 0.75:
                flags.append("intensity")
            if abs(c["z"]) > 3:
                flags.append("far")
            prev_rej = (int(peaks.id[j]), pred.keys[i]) in rejected
            if prev_rej:
                flags.append("prev-rejected")
            Pb = c["P"]
            if blend_with:  # re-evaluate intensity with the summed blend intensity
                tot_int = math.log10(sum(10 ** pred.lgint[k] for k in [i] + blend_with))
                c["dI_blend"] = peaks.lgint[j] - tot_int
            ok = (rank == 0 and Pb >= settings["p_accept"] and contest <= 0.05 and abs(c["z"]) <= 3 and not prev_rej)
            if ok and blend_with:
                ok = all(by_pred[k][0]["j"] == j and by_pred[k][0]["P"] >= settings["p_accept"] for k in blend_with) \
                    and abs(c.get("dI_blend", 0)) < 0.75
            default = "accept" if ok else "defer"
            reason = (f"P={Pb:.3f} z={c['z']:+.2f} dI={c['dI']:+.2f}" + (f" (blend dI={c['dI_blend']:+.2f})" if blend_with else "")
                      + f" n_win={c['n_win']}" + (f" rival={rival:.2f}" if rival > 0.05 else "")
                      + (f" contest={contest:.2f}" if contest > 0.05 else ""))
            rows.append(dict(key=key_str(pred.keys[i]), pred_freq=pred.freq[i], pred_sigma=pred.sigma[i],
                             pred_lgint=pred.lgint[i], peak=int(peaks.id[j]), obs_freq=peaks.freq[j],
                             obs_err=peaks.err[j], obs_lgint=peaks.lgint[j], z=c["z"], dI=c["dI"], P=Pb,
                             n_win=c["n_win"], rival=rival, contest=contest,
                             blend_with="|".join(key_str(pred.keys[k]) for k in blend_with),
                             flags=",".join(flags), default=default, reason=reason))
    rows.sort(key=lambda r: (-r["P"], r["pred_sigma"]))
    for n, r in enumerate(rows):
        r["cid"] = f"C{n + 1:04d}"
    info = dict(p_have=p_have, n_calib=n_cal, n_predictions=len(idx), n_unresolvable=n_unres,
                n_with_candidates=len(by_pred))
    return rows, info


# ------------------------------------------------------------------ bootstrap
def bootstrap(pred, peaks, settings, n_anchor=8, max_cand=15, n_top=15):
    """Hypothesis search for the first assignments (cf. AUTOFIT, Seifert et al. 2015).
    For every triple of anchor lines and every combination of their candidate peaks, update the
    constants by Bayesian linear least squares from the prior and count how many other strong
    predictions then land on an intensity-consistent peak. Score = significance above chance."""
    idx = usable(pred, settings)
    free = np.ones(len(peaks.id), bool)
    med_err = float(np.median(peaks.err))
    max_cand = settings.get("boot_max_cand", max_cand)  # dense (real) spectra need more candidates per anchor
    # anchors: the best-predicted lines that are comfortably above the detection limit
    strong = idx[pred.lgint[idx] >= settings["i_det"] + 1.0]
    strong = strong[np.argsort(pred.sigma[strong])]
    anchors = []
    for i in strong:
        s = math.hypot(pred.sigma[i], med_err)
        a, b = peaks.window(pred.freq[i] - 3.5 * s, pred.freq[i] + 3.5 * s)
        js = [j for j in range(a, b) if abs(peaks.lgint[j] - pred.lgint[i]) < 1.0]
        if 1 <= len(js) <= max_cand:
            anchors.append((i, js))
        if len(anchors) >= n_anchor:
            break
    score_idx = np.array([i for i in idx if pred.lgint[i] >= settings["i_det"] + 0.5
                          and i not in {a[0] for a in anchors}])
    # density of intensity-consistent peaks around each scoring line
    rhoI = np.array([(lambda a, b: (np.abs(peaks.lgint[a:b] - pred.lgint[i]) < 0.75).sum() + 1)(
        *peaks.window(pred.freq[i] - 5000, pred.freq[i] + 5000)) / 10000.0 for i in score_idx])
    P0, f0 = pred.cov, pred.freq
    JS = pred.J[score_idx]
    hyps = []
    for trip in itertools.combinations(range(len(anchors)), 3):
        ai = [anchors[t][0] for t in trip]
        Ja = pred.J[ai]
        R = np.diag([med_err ** 2 + pred.sig_model[i] ** 2 for i in ai])
        S = Ja @ P0 @ Ja.T + R
        K = P0 @ Ja.T @ np.linalg.inv(S)
        P1 = P0 - K @ Ja @ P0
        sS = np.sqrt(np.maximum(np.einsum("ij,jk,ik->i", JS, P1, JS), 0) + pred.sig_model[score_idx] ** 2 + med_err ** 2)
        lam = rhoI * 5 * sS
        use = lam < settings.get("boot_lam_max", 0.15)  # dense spectra: scored lines may have a higher chance rate
        if use.sum() < 10:
            continue
        e = 1 - np.exp(-lam[use])
        var_e = np.sum(e * (1 - e)) + 1e-9
        JK = JS[use] @ K
        cl = [anchors[t][1] for t in trip]
        combos = np.array(list(itertools.product(*cl)))
        Y = peaks.freq[combos] - f0[ai][None, :]  # (C, 3)
        F = f0[score_idx[use]][None, :] + Y @ JK.T  # (C, nS)
        pos = np.searchsorted(peaks.freq, F)
        hit = np.zeros(F.shape, bool)
        lgS = pred.lgint[score_idx[use]][None, :]
        for off in (-2, -1, 0, 1):
            p = np.clip(pos + off, 0, len(peaks.freq) - 1)
            hit |= (np.abs(peaks.freq[p] - F) < 2.5 * sS[use][None, :]) & (np.abs(peaks.lgint[p] - lgS) < 0.75)
        nm = hit.sum(axis=1)
        Z = (nm - e.sum()) / math.sqrt(var_e)
        for c in np.argsort(-Z)[:5]:
            dp = K @ Y[c]
            hyps.append(dict(Z=float(Z[c]), n_match=int(nm[c]), n_scored=int(use.sum()), n_expected=float(e.sum()),
                             sd=np.sqrt(np.maximum(np.diag(P1), 0)),
                             anchors=[(pred.keys[i], int(peaks.id[j])) for i, j in zip(ai, combos[c])],
                             dp=dp, matched=[(pred.keys[score_idx[use][s]]) for s in np.where(hit[c])[0]]))
    hyps.sort(key=lambda h: -h["Z"])
    # Hypotheses whose implied constants agree within their own posterior uncertainty (3 sigma, every
    # parameter) are the same solution: e.g. for an a-type spectrum A is barely constrained by three
    # R-branch lines, so hypotheses that differ only in A are not rivals.
    clusters = []
    for h in hyps:
        for c in clusters:
            if np.all(np.abs(h["dp"] - c["dp"]) < 3 * np.hypot(h["sd"], c["sd"]) + 1e-12):
                c["support"] += 1
                c["members"].append(h)
                break
        else:
            clusters.append(dict(h, support=1, members=[h]))
    clusters = clusters[:n_top]
    for c in clusters:  # anchor assignments shared by all members of the cluster
        common = set(map(tuple, c["members"][0]["anchors"]))
        votes = {}
        for m in c["members"]:
            for a in m["anchors"]:
                votes[tuple(a)] = votes.get(tuple(a), 0) + 1
        c["anchor_votes"] = sorted(votes.items(), key=lambda kv: -kv[1])
    return clusters, [(pred.keys[i], [int(peaks.id[j]) for j in js]) for i, js in anchors]


# ------------------------------------------------------------------ greedy baseline
def greedy(pred, peaks, settings, n_sigma=3.0):
    """Nearest-match assignment with no judgement: predictions in order of increasing uncertainty
    each take the nearest still-free peak within n_sigma."""
    idx = usable(pred, settings)
    idx = idx[np.argsort(pred.sigma[idx])]
    taken, out = set(), []
    for i in idx:
        s = math.hypot(pred.sigma[i], float(np.median(peaks.err)))
        a, b = peaks.window(pred.freq[i] - n_sigma * s, pred.freq[i] + n_sigma * s)
        js = [j for j in range(a, b) if j not in taken]
        if not js:
            continue
        j = min(js, key=lambda j: abs(peaks.freq[j] - pred.freq[i]))
        taken.add(j)
        out.append((int(peaks.id[j]), pred.keys[i]))
    return out
