"""Result figures from results/*.json.

  fig_rounds.png  : per-round % of true lines correctly assigned and precision, all arms, seed 1
  fig_seeds.png   : final coverage / precision of the automated arms over seeds (AI arm: seed 1)
  fig_blind.png   : final coverage / precision of every arm on the blind cases
"""
import glob
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .pickett import ROOT

# validated categorical palette (dataviz reference, slots 1-4, light mode); secondary encoding by
# marker shape and direct labels because aqua/yellow are below 3:1 contrast on the light surface
ARMS = [("ai", "AI-in-the-loop", "#2a78d6", "o"), ("rules_plus", "rules+ (codified)", "#eb6834", "s"),
        ("rules", "rules (P>=0.95)", "#1baf7a", "^"), ("greedy", "greedy", "#eda100", "D")]
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#a3a29c", "#e6e5e0"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150,
                     "axes.titlecolor": INK, "axes.titlesize": 10})


def load(case, seed, arm):
    p = os.path.join(ROOT, "results", f"{case}_s{seed}_{arm}.json")
    return json.load(open(p)) if os.path.exists(p) else None


def fig_rounds(out):
    cases = [("h2co", "H$_2$CO (warm-up)"), ("so2", "SO$_2$ (main test)")]
    fig, axes = plt.subplots(2, 2, figsize=(9.5, 6.2), sharex="col")
    for col, (case, title) in enumerate(cases):
        for row, (metric, ylab) in enumerate([("coverage", "true lines correctly assigned (%)"),
                                              ("precision", "assignments that are correct (%)")]):
            ax = axes[row][col]
            ends = []
            for arm, lab, colr, mk in ARMS:
                s = load(case, 1, arm)
                if not s:
                    continue
                pr = s["per_round"]
                x = [0] + [r["round"] for r in pr]
                if metric == "coverage":
                    y = [0] + [100 * r["coverage"] for r in pr]
                else:
                    x = [r["round"] for r in pr if r["n_pairs"]]
                    y = [100 * r["precision"] for r in pr if r["n_pairs"]]
                ax.plot(x, y, color=colr, lw=2, marker=mk, ms=5, mec="white", mew=1.0, label=lab, zorder=3)
                if metric == "coverage":
                    ends.append([y[-1], x[-1], f"{lab} {y[-1]:.0f}%"])
            ends.sort()
            for i in range(1, len(ends)):  # nudge direct labels apart (min 7 points of the 0-100 scale)
                ends[i][0] = max(ends[i][0], ends[i - 1][0] + 7)
            xmax = max([e[1] for e in ends] or [1])
            for yv, xv, txt in ends:
                ax.annotate(txt, (xmax, yv), xytext=(8, 0), textcoords="offset points", fontsize=7.5,
                            color=INK2, va="center", annotation_clip=False)
            ax.set_ylim(-3, 103)
            if row == 0:
                ax.set_title(title)
            if col == 0:
                ax.set_ylabel(ylab)
            if row == 1:
                ax.set_xlabel("round")
    h, l = axes[0][0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=4, fontsize=8.5, frameon=False, bbox_to_anchor=(0.5, 0.95))
    fig.suptitle("Line assignment from 1%-perturbed constants: AI-in-the-loop vs automated baselines (seed 1)",
                 color=INK, fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 0.87, 0.92))
    fig.savefig(out)
    plt.close(fig)


def fig_seeds(out):
    cases = [("h2co", "H$_2$CO"), ("so2", "SO$_2$")]
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.4), sharey=True)
    for ax, (case, title) in zip(axes, cases):
        for i, (arm, lab, colr, mk) in enumerate(ARMS):
            files = sorted(glob.glob(os.path.join(ROOT, "results", f"{case}_s*_{arm}.json")))
            files = [f for f in files if os.path.basename(f).split("_s")[1].split("_", 1)[1] == arm + ".json"]
            cov = [100 * json.load(open(f))["final"]["coverage"] for f in files]
            prec = [100 * json.load(open(f))["final"]["precision"] if json.load(open(f))["final"]["n_pairs"] else 0
                    for f in files]
            xs = np.full(len(cov), i) + np.linspace(-0.12, 0.12, max(len(cov), 1))[:len(cov)]
            ax.scatter(xs, cov, color=colr, marker=mk, s=42, edgecolors="white", linewidths=1, zorder=3,
                       label="coverage" if i == 0 else None)
            ax.scatter(xs + 0.3, prec, facecolors="white", edgecolors=colr, marker=mk, s=36, linewidths=1.5,
                       zorder=3, label="precision" if i == 0 else None)
            ax.text(i + 0.15, -14, f"n={len(cov)}", ha="center", fontsize=7, color=INK2)
        ax.set_xticks(range(len(ARMS)))
        ax.set_xticklabels([a[1] for a in ARMS], fontsize=8)
        ax.set_ylim(-18, 105)
        ax.set_title(title)
    axes[0].set_ylabel("final value (%)")
    axes[0].legend(loc="center right", fontsize=8, frameon=False)
    fig.suptitle("Robustness over test-case seeds (filled = coverage, open = strict precision; AI arm: 2 seeds per molecule)",
                 color=INK, fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(out)
    plt.close(fig)


def fig_blind(out):
    cases = sorted({os.path.basename(f).split("_s")[0] for f in glob.glob(os.path.join(ROOT, "results", "blind*_s1_*.json"))},
                   key=lambda c: int(c[5:]))
    if not cases:
        return
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.4), sharey=True)
    for ax, (metric, title) in zip(axes, [("coverage", "true lines correctly assigned (%)"),
                                          ("precision", "assignments that are correct, strict (%)")]):
        for i, (arm, lab, colr, mk) in enumerate(ARMS):
            xs, ys = [], []
            for j, c in enumerate(cases):
                s = load(c, 1, arm)
                if s and (metric == "coverage" or s["final"]["n_pairs"]):
                    xs.append(j + (i - 1.5) * 0.15)
                    ys.append(100 * s["final"][metric])
            ax.scatter(xs, ys, color=colr, marker=mk, s=40, edgecolors="white", linewidths=1, zorder=3, label=lab)
        ax.set_xticks(range(len(cases)))
        ax.set_xticklabels(cases, fontsize=8)
        ax.set_ylim(-5, 105)
        ax.set_title(title)
    axes[0].set_ylabel("final value (%)")
    axes[1].legend(loc="lower right", fontsize=7.5, frameon=False)
    fig.suptitle("Blind test: six cases built without the decision-maker seeing the molecule's constants (scale factor hidden)",
                 color=INK, fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(out)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    fig_rounds(os.path.join(ROOT, "figures", "fig_rounds.png"))
    fig_seeds(os.path.join(ROOT, "figures", "fig_seeds.png"))
    fig_blind(os.path.join(ROOT, "figures", "fig_blind.png"))
    print("figures written")
