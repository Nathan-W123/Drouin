"""Markdown tables for REPORT.md, generated from results/*.json (python3 -m assign.tables > results/tables.md)."""
import glob
import json
import os

import numpy as np

from .pickett import ROOT

ARMS = [("ai", "AI-in-the-loop"), ("rules_plus", "rules+"), ("rules", "rules"), ("greedy", "greedy")]


def load(name):
    p = os.path.join(ROOT, "results", f"{name}.json")
    return json.load(open(p)) if os.path.exists(p) else None


def pct(x):
    return "–" if x is None or not np.isfinite(x) else f"{100 * x:.1f}%"


def main_table():
    L = ["| molecule | seed | arm | rounds | true lines correctly assigned | precision (strict) | precision (physics-aware) | assignments | on distractors | wrong label on true line | AI overrides of rule default | human corrections |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for case in ("h2co", "so2"):
        for name in sorted(glob.glob(os.path.join(ROOT, "results", f"{case}_s*_*.json"))):
            s = json.load(open(name))
            arm = s["arm"]
            if arm not in dict(ARMS):
                continue
            f = s["final"]
            L.append(f"| {case.upper()} | {s['seed']} | {dict(ARMS)[arm]} | {s['rounds']} | {pct(f['coverage'])} "
                     f"({f['n_covered']}/{f['n_true']}) | {pct(f['precision']) if f['n_pairs'] else '–'} | "
                     f"{pct(f.get('precision_phys')) if f['n_pairs'] else '–'} | {f['n_pairs']} | {f['wrong_on_distractors']} | "
                     f"{f['wrong_label_on_true']} | {s['ai_overrides'] if arm == 'ai' else '–'} | "
                     f"{s['human_corrections'] if arm == 'ai' else '–'} |")
    return "\n".join(L)


def seed_summary():
    L = ["| molecule | arm | seeds | coverage mean (min–max) | strict precision mean (min–max) |", "|---|---|---|---|---|"]
    for case in ("h2co", "so2"):
        for arm, lab in ARMS:
            fs = [f for f in glob.glob(os.path.join(ROOT, "results", f"{case}_s*_{arm}.json")) if json.load(open(f))["arm"] == arm]
            if not fs:
                continue
            cov = [json.load(open(f))["final"]["coverage"] for f in fs]
            pre = [json.load(open(f))["final"]["precision"] for f in fs if json.load(open(f))["final"]["n_pairs"]]
            seeds = sorted(json.load(open(f))["seed"] for f in fs)
            L.append(f"| {case.upper()} | {lab} | {','.join(map(str, seeds))} | {100 * np.mean(cov):.1f}% ({100 * min(cov):.1f}–{100 * max(cov):.1f}) | "
                     + (f"{100 * np.mean(pre):.1f}% ({100 * min(pre):.1f}–{100 * max(pre):.1f})" if pre else "–") + " |")
    return "\n".join(L)


def blind_table():
    """Blind cases: the decision-maker never saw the molecule's official constants or the scale factor."""
    L = ["| case | arm | rounds | true lines correctly assigned | precision (strict) | precision (physics-aware) | on distractors | wrong label on true line | max \\|this−oracle\\|/σ |",
         "|---|---|---|---|---|---|---|---|---|"]
    for i in range(1, 100):
        if not glob.glob(os.path.join(ROOT, "results", f"blind{i}_s1_*.json")):
            break
        for arm, lab in ARMS:
            s = load(f"blind{i}_s1_{arm}")
            if not s:
                continue
            f = s["final"]
            dev = [abs(c["dev_from_oracle_sigma"]) for c in s.get("constants") or [] if c.get("dev_from_oracle_sigma") is not None]
            L.append(f"| blind{i} | {lab} | {s['rounds']} | {pct(f['coverage'])} ({f['n_covered']}/{f['n_true']}) | "
                     f"{pct(f['precision']) if f['n_pairs'] else '–'} | {pct(f.get('precision_phys')) if f['n_pairs'] else '–'} | "
                     f"{f['wrong_on_distractors']} | {f['wrong_label_on_true']} | "
                     f"{f'{max(dev):.2f}' if dev and s['final_fit_ok'] and f['coverage'] > 0.5 else '–'} |")
    return "\n".join(L)


def constants_table(name):
    s = load(name)
    L = [f"Run `{name}`: unconstrained refit of the final assignments ({s['n_free_params']} free parameters, "
         f"weighted rms {s['final_rms']:.3f}); oracle = all true lines of the list with their true labels "
         f"(weighted rms {s['oracle_rms']:.3f}).", "",
         "| parameter | this work | official (CDMS) | rel. deviation | (this−official)/σ | (this−oracle)/σ |",
         "|---|---|---|---|---|---|"]
    for c in s["constants"]:
        L.append(f"| {c['label']} | {c['value']:.10g} ({c['sigma']:.2g}) | {c['official']:.10g} ({c['official_sigma']:.2g}) | "
                 f"{c['rel_dev']:+.1e} | {c['dev_in_sigma']:+.1f} | {c['dev_from_oracle_sigma']:+.2f} |")
    return "\n".join(L)


def per_round(name):
    s = load(name)
    L = [f"| round | assigned peaks | coverage | precision | weighted rms | free params | AI overrides |", "|---|---|---|---|---|---|---|"]
    for r in s["per_round"]:
        L.append(f"| {r['round']} | {r['n_peaks_assigned']} | {pct(r['coverage'])} | {pct(r['precision']) if r['n_pairs'] else '–'} | "
                 f"{r['rms']:.3f} | {r['n_float']} | {r['overrides']} |")
    return "\n".join(L)


if __name__ == "__main__":
    print("## Final results\n")
    print(main_table())
    print("\n## Over seeds\n")
    print(seed_summary())
    print("\n## Blind cases\n")
    print(blind_table())
    for n in ("so2_s1_ai", "h2co_s1_ai", "so2_s1_rules_plus"):
        if load(n):
            print(f"\n## Constants: {n}\n")
            print(constants_table(n))
    for n in ("so2_s1_ai", "h2co_s1_ai", "h2co_s2_ai"):
        if load(n):
            print(f"\n## Per round: {n}\n")
            print(per_round(n))
