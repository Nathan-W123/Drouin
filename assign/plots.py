"""Diagnostic plots for each round: a normalised Loomis-Wood plot and a residual plot."""
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .match import key_str, parse_key

# validated reference categorical palette (dataviz skill), slots 1-3 + neutrals
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#a3a29c", "#e6e5e0"
plt.rcParams.update({"font.size": 8, "axes.edgecolor": MUTED, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 110})


def series_key(k):
    """Branch label: (dJ, Ka', Ka", Kc'+Ka'-N' parity, Kc"+Ka"-N" parity) -- lines of one branch,
    indexed by N", form a Loomis-Wood series."""
    return (k[0] - k[3], k[1], k[4], (k[1] + k[2] - k[0]), (k[4] + k[5] - k[3]))


def round_plots(run, pred, rdir, crows=None):
    peaks = run.peaks
    assigned = {k: pid for pid, ks in run.assign.items() for k in ks}
    proposed = {}
    for r in crows or []:
        if r["default"] == "accept":
            proposed[parse_key(r["key"])] = r["peak"]
    # ---- choose series: most strong predictions, preferring ones that contain assignments
    groups = {}
    for i, k in enumerate(pred.keys):
        if pred.lgint[i] < run.s["i_det"]:
            continue
        groups.setdefault(series_key(k), []).append(i)
    def rank(g):
        ks = [pred.keys[i] for i in groups[g]]
        return (sum(k in assigned for k in ks) > 0, len(ks))
    chosen = sorted(groups, key=rank, reverse=True)[:6]
    fig, axes = plt.subplots(1, len(chosen) or 1, figsize=(2.3 * max(len(chosen), 1), 4.2), sharey=False, squeeze=False)
    for ax, g in zip(axes[0], chosen):
        idx = sorted(groups[g], key=lambda i: pred.keys[i][3])
        for i in idx:
            k, y = pred.keys[i], pred.keys[i][3]
            s = math.hypot(pred.sigma[i], float(np.median(peaks.err)))
            a, b = peaks.window(pred.freq[i] - 6 * s, pred.freq[i] + 6 * s)
            z = (peaks.freq[a:b] - pred.freq[i]) / s
            ax.scatter(z, np.full(len(z), y), s=6 + 4 * np.clip(peaks.lgint[a:b] - run.s["i_det"], 0, 6),
                       color=MUTED, linewidths=0, zorder=2)
            for ref, col in ((assigned, BLUE), (proposed, AQUA)):
                if k in ref:
                    n = peaks.pos[ref[k]]
                    ax.scatter([(peaks.freq[n] - pred.freq[i]) / s], [y], s=34, color=col, edgecolors="white",
                               linewidths=1.2, zorder=3)
        ax.axvline(0, color=INK2, lw=0.8, zorder=1)
        ax.set_xlim(-6, 6)
        ax.set_title(f"dJ={g[0]} Ka'={g[1]} Ka\"={g[2]}\nKc parity {g[3]},{g[4]}", fontsize=7, color=INK)
        ax.set_xlabel("(obs - pred) / sigma")
    axes[0][0].set_ylabel("N\" (lower state)")
    fig.suptitle(f"{run.case} {run.arm} round {run.round}: Loomis-Wood (grey = peaks, blue = assigned, "
                 f"aqua = proposed accept)", fontsize=8, color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(rdir, "loomis_wood.png"))
    plt.close(fig)

    if not run.resid:
        return
    pids = [p for p in run.resid if p in run.assign]
    if not pids:
        return
    z = np.array([run.resid[p]["z"] for p in pids])
    N = np.array([run.assign[p][0][3] for p in pids])
    Ka = np.array([run.assign[p][0][4] for p in pids])
    f = np.array([run.resid[p]["obs"] for p in pids]) / 1000.0
    fig, axes = plt.subplots(1, 3, figsize=(9, 2.8), sharey=True)
    for ax, x, lab in zip(axes, (f, N, Ka), ("frequency (GHz)", "N\"", "Ka\"")):
        ax.scatter(x, z, s=10, color=BLUE, linewidths=0)
        for lv in (-3, 3):
            ax.axhline(lv, color=MUTED, lw=0.8, ls="--")
        ax.set_xlabel(lab)
    axes[0].set_ylabel("(obs - calc) / err")
    fig.suptitle(f"{run.case} {run.arm} after round {run.round}: weighted residuals of {len(pids)} assigned peaks",
                 fontsize=8, color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(rdir, "residuals.png"))
    plt.close(fig)
