"""Real-spectrum test case: peaks extracted from a public astronomical survey spectrum.

Source: TIMASSS survey of the protostar IRAS 16293-2422 (Caux et al. 2011, A&A 532, A23; CDS
J/A+A/532/A23), IRAM-30m, 80-281.5 GHz, T_A* [K], frequencies in the source rest frame (VLSR 3.8 km/s).

  python -m assign.realspec <case>          e.g. real_so2  (config in cases/real_so2.json)

Steps
  1. Peak finding. The spectrum is split into contiguous windows (gaps > 5 MHz). The noise is a
     sigma-clipped MAD in 200 MHz blocks. Every local maximum (+-3 channels) above `snr_min` x noise
     is fitted with a Gaussian (centre, amplitude, FWHM) on +-5 channels.
  2. Peak uncertainty: err^2 = (FWHM / (2 SNR))^2 + (nu * v_sys / c)^2 + (channel/sqrt(12))^2.
     v_sys covers the two velocity components of the binary and asymmetric line shapes; its value
     (config `v_sys_kms`) was set from the scatter of the reference matches (see below).
  3. Intensity scale. The loop compares log intensities with SPCAT's (log10 nm^2 MHz) at the case
     temperature, so the observed peak is converted with  lgint = log10(T_A* nu) + C  (optically thin,
     Rayleigh-Jeans: integrated intensity ~ SPCAT intensity / nu, and the line widths are similar).
     C and the rotational temperature come from the reference matches (2 numbers, see REPORT).
  4. Reference assignment (HIDDEN, scoring only): a peak carries a label of the target molecule
     if a line of the CDMS reference catalog lies within max(3 err, FWHM/2) of it and its predicted
     intensity is consistent with the peak (-1.0 <= lgint_pred - lgint_obs <= +0.7 dex; the peak
     may be brighter because of blending, not much fainter). All other peaks are 'other' (the
     ~70 other species of the source, which act as real distractors).
"""
import argparse
import csv
import json
import os

import numpy as np

from . import pickett as pk
from .model import load_case, rel, starting_model, official_params
from .testcase import official_catalog_v, key_str

C_KMS = 299792.458


def load_spectrum(cfg):
    from astropy.io import fits
    d = fits.open(rel(cfg["spectrum"]))[1].data
    f, t = np.asarray(d["wave"], float) * 1000.0, np.asarray(d["flux"], float)
    o = np.argsort(f)
    return f[o], t[o]


def windows(f, gap=5.0):
    cut = np.where(np.diff(f) > gap)[0]
    starts, ends = np.r_[0, cut + 1], np.r_[cut, len(f) - 1]
    return [(s, e) for s, e in zip(starts, ends) if e - s > 50]


def noise(f, t, block=200.0):
    sig = np.zeros_like(t)
    for b in np.arange(f.min(), f.max() + block, block):
        m = (f >= b) & (f < b + block)
        if m.sum() < 30:
            continue
        x = t[m]
        for _ in range(6):
            med = np.median(x)
            s = 1.4826 * np.median(np.abs(x - med))
            x = x[np.abs(x - med) < 3 * s]
        sig[m] = s
    return sig


def gauss_fit(x, y):
    from scipy.optimize import curve_fit
    g = lambda x, a, c, w: a * np.exp(-4 * np.log(2) * (x - c) ** 2 / w ** 2)
    i = np.argmax(y)
    p0 = [y[i], x[i], 2.0]
    try:
        p, _ = curve_fit(g, x, y, p0=p0, maxfev=2000)
        if p[0] <= 0 or abs(p[1] - x[i]) > 1.5 or not (0.3 < abs(p[2]) < 20):
            raise RuntimeError
        return p[0], p[1], abs(p[2])
    except Exception:
        # parabola through the top 3 channels
        j = min(max(i, 1), len(x) - 2)
        a, b, c = np.polyfit(x[j - 1:j + 2] - x[j], y[j - 1:j + 2], 2)
        xc = -b / (2 * a) if a < 0 else 0.0
        return y[i], x[j] + xc, float("nan")


def find_peaks(f, t, sig, snr_min, half=3, fit_half=5):
    out = []
    for s, e in windows(f):
        for i in range(s + half, e - half):
            if sig[i] <= 0 or t[i] < snr_min * sig[i]:
                continue
            if t[i] < t[i - half:i + half + 1].max():
                continue
            lo, hi = max(i - fit_half, s), min(i + fit_half + 1, e + 1)
            a, c, w = gauss_fit(f[lo:hi], t[lo:hi])
            out.append(dict(freq=c, amp=a, fwhm=w, snr=a / sig[i], chan=f[i + 1] - f[i]))
    return out


def peak_err(p, cfg):
    w = p["fwhm"] if np.isfinite(p["fwhm"]) else cfg["fwhm_kms"] * p["freq"] / C_KMS
    return float(np.sqrt((w / (2 * p["snr"])) ** 2 + (p["freq"] * cfg["v_sys_kms"] / C_KMS) ** 2 + p["chan"] ** 2 / 12))


def reference(cfg, peaks):
    """Reference (CDMS) assignment of the extracted peaks: labels and residuals (scoring only)."""
    cat = official_catalog_v(cfg, None, 0)
    o = np.argsort(cat.freq)
    cf, cl, ck = cat.freq[o], cat.lgint[o], [cat.keys()[i] for i in o]
    for p in peaks:
        tol = max(3 * p["err"], 0.5 * (p["fwhm"] if np.isfinite(p["fwhm"]) else 2.0))
        a, b = np.searchsorted(cf, p["freq"] - tol), np.searchsorted(cf, p["freq"] + tol)
        labs = [(ck[k], cf[k], cl[k]) for k in range(a, b)]
        p["ref"] = labs
    return cf, cl


def build(case, seed=1):
    cfg = load_case(case)
    f, t = load_spectrum(cfg)
    sig = noise(f, t)
    peaks = find_peaks(f, t, sig, cfg["snr_min"])
    for p in peaks:
        p["err"] = peak_err(p, cfg)
        p["lgint"] = float(np.log10(p["amp"] * p["freq"]) + cfg["int_offset_C"])
    reference(cfg, peaks)
    n_true = 0
    for p in peaks:
        good = []
        for k, fc, lc in p["ref"]:
            if -1.0 <= lc - p["lgint"] <= 0.7:
                good.append((k, fc, lc))
        if good:
            tot = np.log10(sum(10 ** g[2] for g in good))
            p["labels"], p["source"] = [g[0] for g in good], "true"
            p["true_freq"] = float(np.mean([g[1] for g in good]))
            p["true_lgint"] = float(tot)
            n_true += 1
        else:
            p["labels"], p["source"], p["true_freq"], p["true_lgint"] = [], "other", p["freq"], p["lgint"]
    peaks.sort(key=lambda p: p["freq"])
    out = os.path.join(pk.ROOT, "testcases", f"{cfg['key']}_s{seed}")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "peaks.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "freq", "err", "lgint"])
        for i, p in enumerate(peaks):
            p["id"] = i + 1
            w.writerow([p["id"], f"{p['freq']:.6f}", f"{p['err']:.6f}", f"{p['lgint']:.3f}"])
    with open(os.path.join(out, "truth.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "source", "labels", "true_freq", "true_lgint"])
        for p in peaks:
            w.writerow([p["id"], p["source"], ";".join(key_str(k) for k in p["labels"]),
                        f"{p['true_freq']:.6f}", f"{p['true_lgint']:.3f}"])
    rng = np.random.default_rng(np.random.SeedSequence([seed, 77]))
    s = dict(seed=seed, abc_lo=0.005, abc_hi=0.010, abc_prior=0.010, q_lo=0.10, q_hi=0.30, q_prior=0.50,
             absent_factor=10.0)
    s.update(cfg.get("start_perturbation", {}))  # e.g. 0.05-0.1% for the 'good prior' variant
    model = starting_model(cfg, rng, s)
    json.dump(model.to_json(), open(os.path.join(out, "model.json"), "w"), indent=1)
    model.to_parfile(title=f"{cfg['name']} start s{seed}").write(os.path.join(out, "start.par"))
    offp = official_params(cfg)
    json.dump([dict(idpar=p.idpar, label=p.label, start=p.value, official=offp[p.idpar][0], prior=p.prior)
               for p in model.floating()], open(os.path.join(out, "truth_constants.json"), "w"), indent=1)
    i_det = float(np.quantile([p["lgint"] for p in peaks], 0.05))  # from the peak list only, not the reference
    meta = dict(case=cfg["key"], settings=s, spectrum=cfg["spectrum"], detection_limit_lgint=i_det,
                n_peaks=len(peaks), n_true=n_true, n_distractors=len(peaks) - n_true,
                log=[f"{len(peaks)} peaks >= {cfg['snr_min']} sigma; {n_true} carry a reference label"])
    json.dump(meta, open(os.path.join(out, "testcase.json"), "w"), indent=1)
    return out, meta, peaks


def calibrate(case):
    """Diagnostics used to set v_sys_kms, int_offset_C and the temperature (reported, not hidden)."""
    cfg = load_case(case)
    f, t = load_spectrum(cfg)
    sig = noise(f, t)
    peaks = find_peaks(f, t, sig, cfg["snr_min"])
    for p in peaks:
        p["err"] = peak_err(p, cfg)
        p["lg0"] = float(np.log10(p["amp"] * p["freq"]))
    reference(cfg, peaks)
    # unique, isolated reference matches of predicted-strong lines
    rows = [(p, p["ref"][0]) for p in peaks if len(p["ref"]) == 1]
    lc = np.array([r[1][2] for r in rows])
    strong = lc >= np.quantile(lc, 0.5) if len(lc) else []
    sel = [r for r, s in zip(rows, strong) if s]
    dI = np.array([r[1][2] - r[0]["lg0"] for r in sel])
    C = float(np.median(dI)) if len(dI) else float("nan")
    z = np.array([(r[0]["freq"] - r[1][1]) / r[0]["err"] for r in sel])
    dv = np.array([(r[0]["freq"] - r[1][1]) / r[1][1] * C_KMS for r in sel])
    w = np.array([r[0]["fwhm"] / r[0]["freq"] * C_KMS for r in sel if np.isfinite(r[0]["fwhm"])])
    print(f"{len(peaks)} peaks >= {cfg['snr_min']} sigma; {len(rows)} with exactly one reference line in tolerance; "
          f"{len(sel)} of them predicted-strong")
    print(f"intensity offset C = median(lgint_ref - log10(T nu)) = {C:.3f}  (scatter {np.std(dI):.2f} dex)")
    print(f"velocity offset: median {np.median(dv):+.2f} km/s, robust scatter {1.4826 * np.median(np.abs(dv - np.median(dv))):.2f} km/s")
    print(f"z = (obs-ref)/err: median {np.median(z):+.2f}, robust sd {1.4826 * np.median(np.abs(z - np.median(z))):.2f}")
    print(f"FWHM: median {np.median(w):.2f} km/s")
    return C


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("case")
    ap.add_argument("--calibrate", action="store_true")
    a = ap.parse_args()
    if a.calibrate:
        calibrate(a.case)
    else:
        out, meta, _ = build(a.case)
        print(out)
        print("\n".join(meta["log"]))
