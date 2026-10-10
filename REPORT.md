# AI-in-the-loop line assignment with SPFIT/SPCAT — a scorable proof of concept

**Nathan Ward**, UC Davis (chemistry + civil engineering) — prepared for Dr. Brian Drouin, JPL Molecular
Spectroscopy, as the first step of a SURF@JPL 2027 proposal. October 2026.
Code, data, decision logs: this repository (`README.md` explains how to rerun everything).

## 1. Summary

The bottleneck in rotational spectroscopy is **assignment**, not measurement. The question this
week's prototype asks: *does a judgement step in the SPFIT/SPCAT loop make automatic assignment work
where automation alone fails?* Test cases are built from real expert line lists (CDMS) for **SO₂**
(main test) and **H₂CO** (warm-up). In each, the labels are hidden, 15% of the lines are dropped, the
list is contaminated with **33–37% distractor peaks** (isotopologues, a vibrational satellite, random
peaks) and noise is added. The run starts from constants that are **0.5–1% off** in A, B, C and
**10–30% off** in the quartic constants, with every higher-order term missing.

| | greedy (no judgement) | rules (P ≥ 0.95) | rules+ (lessons codified) | **AI-in-the-loop** |
|---|---|---|---|---|
| SO₂, true lines correctly assigned | 0.0–0.2% (5 seeds) | 0.4–19% (5 seeds) | 17–91% (5 seeds) | **97.2% / 95.8%** (seeds 1, 4) |
| SO₂, assignments that are correct | 0–1% | 67–100% | 87–100% | **100% / 100%** |
| H₂CO, true lines correctly assigned | 0–1% | 1–16% (1–64%²) | 1.5–96.5% (0.5–95.5%²) | **96.5% / 93.4%** (seeds 1, 2) |
| H₂CO, assignments correct (strict / physics-aware¹) | 0–1% | 50–91% | 33–98% | **97.2–97.5% / 100%** |

² With the corrected finite-difference step (300 MHz); the as-run step was 3000 MHz, see §5.
SO₂ results are identical at both settings.

¹ All 11 "wrong" H₂CO labels are the second component of a high-Ka K-doublet that is degenerate to
<8 kHz (Doppler width 1.3–1.5 MHz) and that the CDMS list labels only once; see §4.3.

![per-round results](figures/fig_rounds.png)

*Figure 1. Seed 1: percentage of the true lines in the list correctly assigned (top) and percentage of
assignments that are correct (bottom), per round. Greedy assigns hundreds of lines, almost none
correctly (on SO₂ 245 of its 629 assignments land on distractor peaks). The rules arm stalls after 2–3
lines. The AI-in-the-loop arm reaches 96–97% at 97–100% precision in 8 (H₂CO) and 13 (SO₂) rounds.*

![over seeds](figures/fig_seeds.png)

*Figure 2. All seeds. Codifying the H₂CO judgement as rules ("rules+") works on some test cases and
collapses on others (H₂CO 1.5–96.5%, SO₂ 17–91%). The AI arm was run on two seeds per molecule,
including the two where rules+ failed worst (H₂CO seed 2: 1.5%; SO₂ seed 4: 25%), and reached
93–97% coverage at 100% physics-aware precision on all four.*

**Final constants.** For SO₂ (seed 1), A, B, C agree with the CDMS values to ~1×10⁻⁹ (≤0.2σ). All 25
fitted constants are within 0.74σ of an *oracle* fit (all true lines in the list with their true labels,
same Hamiltonian). In other words, the loop extracted everything this line list can give.

**What the judgement actually did** (scored afterwards against the hidden truth, §4.2). Across four AI
runs, 361 of 366 extra accepts beyond the rule threshold were correct. All 126 "keep" decisions that
overrode the rule's "reject this outlier" kept correct lines: the rule mistook an incomplete
Hamiltonian for a misassignment. Of 44 rejections and unassignments, 33 removed wrong lines or candidates and
11 removed correct ones.

**Honest caveats** (§5): a finite-difference step bug, found after the runs, handicapped some H₂CO automated runs (SO₂ unaffected; corrected re-runs reported); the line lists are catalog-derived (measured frequencies, not a raw
spectrum) and sparse; both molecules are rigid asymmetric tops without internal rotation; the
decision-maker (Claude, in this session) had seen the official constants while building the test
cases; the tools the judgement relied on were developed during the H₂CO warm-up run; the AI arm was
run on 2 seeds per molecule, not 5.

## 2. What was built

### 2.1 Tools and sanity check
SPFIT/SPCAT were built from the Cologne `Pickett.zip` source. On the official CDMS `SO2.par` +
`SO2.lin` (2428 lines, 59 parameters: ground state, ν2=1 and the ν2 band), SPFIT reproduces the
official `SO2.fit` exactly: the same weighted rms (0.87499), the same MW rms (0.067816 MHz), and all 58
fitted values and uncertainties. 2427/2428 calculated frequencies are identical; one differs by 1e-5 MHz
in the last printed digit (`scripts/sanity_check.sh`).

### 2.2 Test cases (scorable, label-free)
`assign/testcase.py`, configured by `cases/*.json`, seeded:

* **True lines**: measured ground-state frequencies of the CDMS `.lin`, 0–1 THz. Successive rows with
  identical frequency/error become one peak with several labels (blends). Rows that are not spectral
  peaks are excluded: CDMS "difference" pseudo-lines (pairs with one transition written reversed; 15
  groups in SO₂), and for H₂CO 261 rows that violate a-type selection rules (ground-state combination
  differences from IR work).
* **Dropped lines**: 15% at random.
* **Distractors**, only above the detection limit and never closer than the Doppler width to an
  existing peak:
  * SO₂: measured ν2=1 rotational lines (real frequencies), ³⁴SO₂ (CDMS catalogue, ×4.25% abundance)
    and random peaks.
  * H₂CO: H₂¹³CO (×1.07%), H₂C¹⁸O (×0.205%) and random peaks.
  * Seed 1: SO₂ has 745 peaks (467 true, 278 distractors), H₂CO 300 (201 true, 99 distractors).
* **Noise**: frequency noise σ = measurement error, with the reported uncertainty inflated to err·√2.
  Intensities are SPCAT intensities from the official constants at 300 K, with 0.15 dex noise.
* **Starting constants**: A, B, C off by 0.5–1% and quartics off by 10–30% (random sign); higher-order
  terms absent. Gaussian priors: 1% on A, B, C, 50% on quartics.
* The hidden labels are read only by `assign/score.py`.

### 2.3 One round of the loop
1. **Predict** (SPCAT + uncertainty). Prediction uncertainties combine two parts:
   * the posterior covariance of the fitted constants, taken from SPCAT's own propagation of SPFIT's
     `.var` where that is reliable, and from Jacobian propagation where SPCAT caps it at about 100 MHz;
   * a *model-error* term from every Watson term not yet in the model, at an order-of-magnitude scale.

   Validated against SPFIT's parameter errors (≤1.1%) and against Monte Carlo refits (agreement at
   the Monte Carlo noise level), `tests/`.
2. **Propose.** Each prediction gets a Bayesian probability for each peak within 4σ. The probability
   uses frequency agreement, intensity agreement (0.3 dex), the local density of unrelated peaks, and
   the fraction of predicted lines present in the list, which is estimated from the data (≈0.2 for SO₂,
   0.5 for H₂CO, so these lists are sparse). Flags: rival peaks, contested peaks, Doppler-unresolved
   blends, intensity mismatch.

   Round 1 is a bootstrap: a search over triples of well-predicted anchor lines × candidate peaks,
   scored by how many other predictions then land on intensity-consistent peaks beyond chance (cf.
   AUTOFIT).
3. **Decide** on candidates, outliers of the last fit (studentised residuals with leverage) and
   parameter releases (trial SPFIT fits: Δχ² ≥ 9 and |value/σ| ≥ 3).
4. **Refit** with SPFIT. SPFIT's a-priori error acts as a Gaussian prior centred on the value written in
   the `.par` (verified in `calfit.c` and numerically), so constrained parameters are always written with
   their original starting value. A prior is dropped once the data dominate it.

### 2.4 The four arms
* **greedy**: each prediction, sharpest first, takes the nearest free peak within 3σ; refit; repeat.
* **rules**: the full pipeline with every default applied automatically.
* **rules+**: rules plus five lessons codified from the H₂CO seed-1 AI session *after* it was done:
  * automated series coherence;
  * several parameter releases per round by forward selection, capped at 10× the magnitude estimate;
  * no outlier rejection while a release is pending;
  * no new lines while the fit is contaminated;
  * rejection by leave-one-out influence.
* **AI-in-the-loop**: the same pipeline, but every round stops for a decision file (one line and one
  reason per decision). In this prototype the decision-maker was Claude, in this Claude Code session,
  with Nathan reviewing. It used the proposal tables, the Loomis-Wood and residual plots, and three
  deterministic aids that ship with the code:
  * series coherence (`assign/series.py`);
  * what-if refits with leave-one-out, trial releases and pruning of inconsistent additions
    (`assign/whatif.py`);
  * a branch/J split (`assign/split.py`).

  The decision files are in `decisions/`; every applied decision with its reason is in
  `runs/*_ai/round_NN/decisions_applied.csv`.

## 3. Results

Complete tables, including per-round tables and the constants of every run, are in
[`results/tables.md`](results/tables.md), generated from `results/*.json` by `python3 -m assign.tables`.

### 3.1 Final assignment quality

| molecule | seed | arm | rounds | true lines correctly assigned | strict precision | physics-aware precision | assignments | on distractors | wrong label on true line |
|---|---|---|---|---|---|---|---|---|---|
| SO₂ | 1 | **AI-in-the-loop** | 13 | **97.2%** (454/467) | **100%** | **100%** | 454 | 0 | 0 |
| SO₂ | 1 | rules+ | 30 | 90.6% (423/467) | 100% | 100% | 423 | 0 | 0 |
| SO₂ | 1 | rules | 4 | 0.4% (2/467) | 100% | 100% | 2 | 0 | 0 |
| SO₂ | 1 | greedy | 8 | 0.0% (0/467) | 0.0% | 0.0% | 629 | 245 | 384 |
| SO₂ | 4 | **AI-in-the-loop** | 14 | **95.8%** (434/453) | **100%** | **100%** | 434 | 0 | 0 |
| SO₂ | 4 | rules+ | 10 | 24.9% (113/453) | 86.9% | 86.9% | 130 | 4 | 13 |
| SO₂ | 4 | rules | 4 | 0.4% (2/453) | 66.7% | 66.7% | 3 | 1 | 0 |
| SO₂ | 4 | greedy | 12 | 0.2% (1/453) | 0.2% | 0.2% | 609 | 246 | 362 |
| H₂CO | 1 | **AI-in-the-loop** | 8 | **96.5%** (194/201) | 97.2% | **100%** | 215 | 0 | 6 |
| H₂CO | 1 | rules+ | 15 | 96.5% (194/201) | 98.1% | 100% | 212 | 0 | 4 |
| H₂CO | 1 | rules | 2 | 1.0% (2/201) | 66.7% | 66.7% | 3 | 0 | 1 |
| H₂CO | 1 | greedy | 20 | 0.0% (0/201) | 0.0% | 0.0% | 35 | 7 | 28 |
| H₂CO | 2 | **AI-in-the-loop** | 7 | **93.4%** (185/198) | 97.5% | **100%** | 203 | 0 | 5 |
| H₂CO | 2 | rules+ | 7 | 1.5% (3/198) | 33.3% | 33.3% | 9 | 1 | 5 |
| H₂CO | 2 | rules | 7 | 16.2% (32/198) | 91.4% | 91.4% | 35 | 2 | 1 |
| H₂CO | 2 | greedy | 6 | 0.0% (0/198) | 0.0% | 0.0% | 221 | 85 | 136 |

**Over 5 seeds (automated arms):**

| | greedy | rules | rules+ |
|---|---|---|---|
| H₂CO, coverage mean (range) | 0.2% (0–1.0) | 4.3% (1.0–16.2) | 50.0% (1.5–96.5) |
| SO₂, coverage mean (range) | 0.1% (0–0.2) | 7.6% (0.4–19.3) | 62.6% (16.7–90.9) |

The rules threshold is not what makes the rules arm fail: on seed 1, P ≥ 0.5, 0.7, 0.8 and 0.9 all
stall below 2.5% coverage (`results/*_rules_p*.json`).

**Rounds and corrections.** The AI arm used 7–14 rounds. Human corrections: **0**. Nathan delegated the
whole run and did not override any decision. The AI arm departed from the rule-based default 124–286
times per run; those departures are audited in §4.2.

### 3.2 Constants (SO₂, seed 1)
These come from an unconstrained refit of the final 454 assignments with the 25 terms the loop
released: weighted rms 0.957, against 1.039 for the oracle.

| | value (this work) | CDMS | rel. dev. | dev/σ vs CDMS | dev/σ vs oracle |
|---|---|---|---|---|---|
| A / MHz | 60778.54969(45) | 60778.54978(29) | −1.5e-9 | −0.2 | −0.23 |
| B / MHz | 10318.07355(8) | 10318.07353(5) | +1.3e-9 | +0.1 | −0.44 |
| C / MHz | 8799.703406(67) | 8799.703401(45) | +5.8e-10 | +0.1 | −0.47 |
| −Δ_K / MHz | −2.5903177(42) | −2.5903172(33) | 2.1e-7 | −0.1 | +0.44 |
| −Δ_JK / MHz | 0.11695798(81) | 0.11695464(44) | 2.9e-5 | +3.6 | +0.01 |
| −Δ_J / MHz | −6.611737(61)e-3 | −6.611890(35)e-3 | −2.3e-5 | +2.2 | +0.49 |
| −δ_K / MHz | −2.537126(69)e-2 | −2.537096(40)e-2 | 1.2e-5 | −0.4 | +0.07 |
| −δ_J / MHz | −1.7010810(54)e-3 | −1.7010917(29)e-3 | −6.3e-6 | +1.7 | +0.06 |

All 25 constants are within 0.74σ of the oracle (SO₂ seed 4: 0.69σ; H₂CO: ≤1.1σ). Some higher-order
constants differ from CDMS by several σ (e.g. P_K −17σ). That is a model difference, not an assignment
difference: the CDMS fit also uses ν2=1 and infrared data, and includes S_K, S_KKKJ, P_KKJ and P_JJK,
which this ground-state, ≤1 THz list could not justify. The oracle shows the same deviations.

## 4. What the judgement step contributed

### 4.1 Where automation fails, concretely
1. **Sparse, contaminated lists defeat per-line statistics.**
   * Only ~20% (SO₂) and ~50% (H₂CO) of the lines predicted above the detection limit are in these
     lists. A single isolated match is therefore weak evidence, and after the bootstrap almost no
     candidate reaches P ≥ 0.95.
   * Lowering the threshold lets in wrong lines, and the fit diverges.
   * Greedy matching assigns hundreds of lines, about 40% of them to distractor peaks.
2. **Wrong bootstrap anchors.** In 3 of the 4 AI runs the initial 3-line hypothesis contained a wrong
   anchor (SO₂ s1: 3₁₃–2₀₂ on the wrong peak; H₂CO s1: a Ka=5 K-doublet; H₂CO s2: two different
   transitions on one peak). In the fourth (SO₂ s4) a wrong *default accept* entered in round 2. The bootstrap still had the right
   constants overall, since the linear update absorbs one bad anchor among wide priors. Leave-one-out
   refits found the bad line within one round each time; the plain rules arm never does.
3. **Model inadequacy looks like misassignment.** As the line set grows, the residuals of *correct*
   lines grow (kHz-precision K-doublets need sextic and octic terms). The rule "reject the worst
   outlier" then throws out correct lines. In the H₂CO rules+ seed-1 run, 31 lines were removed in one
   round before this was codified.
4. **Resolution.** Two K-doublet components are a blend only if they are closer than the Doppler width.
   This was my own error in round 2 of the H₂CO run: I accepted resolved Ka=4 components as blends. The
   build-up fit exposed it in round 3 and it was undone (§4.3).

### 4.2 Audit of the AI arm's departures from the defaults
These counts are scored against the hidden truth after the runs (`python3 -m assign.override_audit`).

| departure from the rule default | H₂CO s1 | H₂CO s2 | SO₂ s1 | SO₂ s4 |
|---|---|---|---|---|
| extra **accepts** (below threshold): correct / total | 94 / 99 | 42 / 42 | 90 / 90 | 135 / 135 |
| **keep** a line the rule wanted to reject: correct / total | 119 / 119 | 1 / 1 | 3 / 3 | 3 / 3 |
| **reject / unassign** an assigned line: wrong / total | 5 / 6 | 2 / 2 | 1 / 2 | – |
| **reject** a candidate: wrong / total | 2 / 2 | – | 11 / 12 | 12 / 20 |
| **defer** a candidate the rule would accept: correct / total | 53 / 55 | 112 / 114 | 1 / 1 | 1 / 1 |
| parameter releases / holds against the default | 4 / 1 | 6 / 0 | 13 / 3 | 13 / 1 |

How the judgement worked in practice: it formed physical hypotheses and tested them with refits.
1. **Series coherence.** Five Ka=0 R-branch lines of H₂CO shared one fractional offset, −0.011739 ±
   0.000010, the signature of a 1.2% error in B+C. Each line alone had P ≈ 0.07.
2. **K-doubling scaling.** The Q-branch Ka=4 splittings divided by (J+K)!/(J−K)! vary smoothly
   (1.2292→1.2203×10⁻⁷ over J = 8–13); that identified the right line on contested peaks and exposed
   the wrong Ka=5 anchor.
3. **Build-up by Ka.** R-branch Ka≤3 fits at rms 0.85, and adding Ka=4 breaks it; this localised an error.
4. **Joint release tests.** Five sextics together take a 111-line SO₂ set from rms 32.6 to 0.83, so the
   lines were right and the model was incomplete.
5. **Plausibility.** A release was refused when its value was 14–250× its order-of-magnitude estimate,
   which means it was compensating for a misassignment.

### 4.3 Errors (all of them)
* **Strict-precision "errors" in H₂CO (11 pairs).** All are the second component of Ka ≥ 5 K-doublets.
  The official constants put the two components 0–7 kHz apart, with identical intensities, against a
  Doppler width of 1.3–1.5 MHz. The peak physically contains both lines; the CDMS `.lin` lists one.
  Counting the exactly degenerate partner as correct gives 100%.
* **My judgement errors during the runs**, each found and corrected within the run unless stated:
  * the Ka=4 blend misjudgement (H₂CO s1, round 2; 6 peaks, undone in round 3);
  * one correct J=71 SO₂ line unassigned (re-assigned 2 rounds later);
  * on SO₂ s4, 8 correct candidates rejected because the joint test fit had diverged, making their
    |z| meaningless — a candidate should be rejected only on a fit that converged;
  * on SO₂ s1 and H₂CO s2, one true line each was lost, because its peak had been blacklisted with a
    different label.
* **Missed lines.**
  * SO₂: 12 of 13 missed lines are weak (log I ≈ −8 to −9), low-frequency (5–47 GHz) ΔJ = ±1, Ka = 10–15
    lines at J = 48–73.
  * H₂CO: all 7 misses in seed 1 and 8 of 13 in seed 2 are ultra-weak (log I ≈ −15) MHz-frequency
    K-doublets from molecular-beam work, which lie below the intensity cut the loop uses to decide which predictions are worth matching.

### 4.4 Can the judgement simply be written down as rules?
Partly. Rules+ is the H₂CO judgement codified after the fact. It reproduces the AI result on the
seed it was written from (96.5%) and does well on SO₂ seeds 1–3 (90–91%). It fails on H₂CO seeds 2–4
(1.5–40%) and SO₂ seeds 4–5 (17–25%), mostly when the bootstrap or an early round goes wrong and the
fixed rules dig deeper instead of backing out. It also loses correct lines late in a run: SO₂ seed 1
peaked at 97% in round 9 and ended at 91% after its influence rule removed correct lines. The AI arm
reached 93–97% on exactly those failing cases. The parts that transfer as code are worth keeping as
defaults. Recovering from a wrong state, and choosing which hypothesis to test next, is where judgement
paid off.

## 5. Limitations (please read)
* **A bug found after the runs: the finite-difference step.** All runs in §3 used a 3000 MHz
  finite-difference step for the Jacobian, instead of the 300 MHz value validated in `tests/`
  (a parameter sweep left the wrong value in the code). The line uncertainties used inside
  0.002–99 MHz come from SPCAT and were unaffected, and the round-1 uncertainties agree to within 2%
  (95th percentile). But the Jacobian also drives the bootstrap ranking, leverage and the blend test.
  For H₂CO seed 1 the top bootstrap hypothesis changes: the wrong 15₅,₁₀ anchor that the AI arm had to
  find and remove in round 3 is *not* chosen at 300 MHz. I re-ran all automated arms at 300 MHz
  (`--fd-step 300`, now the default); true lines correctly assigned (%) per seed 1–5:

  | molecule | arm | as run (3000 MHz) | corrected (300 MHz) |
  |---|---|---|---|
  | H₂CO | greedy | 0.0 / 0.0 / 0.0 / 1.0 / 0.0 (mean 0.2) | 0.0 / 0.0 / 0.0 / 1.0 / 0.0 (mean 0.2) |
  | H₂CO | rules | 1.0 / 16.2 / 1.0 / 2.0 / 1.1 (mean 4.3) | 52.2 / 1.5 / 63.8 / 1.5 / 1.1 (mean 24.0) |
  | H₂CO | rules+ | 96.5 / 1.5 / 40.2 / 15.3 / 96.3 (mean 50.0) | 95.5 / 0.5 / 93.5 / 27.0 / 50.5 (mean 53.4) |
  | SO₂ | greedy | 0.0 / 0.2 / 0.0 / 0.2 / 0.0 (mean 0.1) | 0.0 / 0.0 / 0.0 / 0.4 / 0.7 (mean 0.2) |
  | SO₂ | rules | 0.4 / 1.1 / 19.3 / 0.4 / 16.9 (mean 7.6) | 0.4 / 1.1 / 18.9 / 0.4 / 21.8 (mean 8.5) |
  | SO₂ | rules+ | 90.6 / 90.9 / 89.7 / 24.9 / 16.7 (mean 62.6) | 90.6 / 90.9 / 89.7 / 24.9 / 16.7 (mean 62.6) |

  SO₂ is unchanged. On H₂CO the plain rules arm does much better on two seeds (52%, 64%) and rules+
  changes seed by seed (mean 50% → 53%). Rules+ still fails where the AI arm succeeded: H₂CO seed 2
  (0.5% at 300 MHz against 93.4% for the AI arm) and SO₂ seed 4 (25% against 95.8%). The AI runs were not
  repeated at 300 MHz, because that would require new decisions. Replay them exactly with `--fd-step 3000`.
* **Not a raw spectrum.**
  * The "observed" peaks are the catalog's measured frequencies plus distractors. The lists are
    *sparse*: only the lines experimenters chose to measure, about 20% of the predicted SO₂ lines above
    the detection limit.
  * There is no baseline, line-shape fitting, peak-finding error, intensity calibration drift, or
    unresolved spectral confusion beyond the Doppler criterion.
  * Intensities are model intensities with noise.
* **Easy molecules.** SO₂ and H₂CO are rigid asymmetric tops with well-behaved Watson Hamiltonians.
  There is no internal rotation (methyl rotors), no hyperfine structure (ignored for H₂CO), and no
  perturbations between vibrational states. The ν2=1 lines were distractors only, not fitted.
* **The decision-maker was not blind.** I (Claude) read the official `.par` files and printed the
  official constants while building the test cases, before the build step was changed to hide them.
  The decision tables show only line-level diagnostics, never comparisons with official constants, and
  every decision is grounded in a logged diagnostic. Still, this is not a blinded study.
  * The tooling (series coherence, what-if refits, branch split) was developed *during* the H₂CO seed-1
    run, so that run is a development run.
  * The later runs (SO₂ s1, H₂CO s2, SO₂ s4) used tools and physics knowledge accumulated earlier,
    e.g. which terms H₂CO needed. A spectroscopist would carry that over too, but it is prior knowledge.
* **Small n for the AI arm**: 2 seeds per molecule, against 5 for the automated arms. The AI runs were
  chosen to include the worst rules+ seeds, which favours showing robustness, but no AI run was done on
  the remaining seeds.
* **Cost.** Each AI round took on the order of a few minutes of model time plus SPFIT/SPCAT refits.
  That was cheap here, but the "decision-maker" was a frontier LLM working interactively with full tool
  access, not a constrained API call. Nathan did not intervene (0 human corrections), so the
  *human*-in-the-loop part is untested.
* **Model building is part of the judgement.** Which centrifugal-distortion terms to release, and when,
  was decided with Δχ², significance and magnitude-plausibility tests. For molecules whose Hamiltonian
  is itself uncertain (internal rotation, Coriolis coupling), that part becomes harder and more
  important.

## 6. Next steps (summer project)
1. Real, partly assigned JPL spectra: peak finding, blends and line shapes, and the actual spectrum
   density in place of a sparse catalog list.
2. A methyl-rotor molecule (e.g. acetaldehyde or methyl formate) with SPFIT's internal-rotation /
   Fourier options, or with ERHAM/XIAM-style codes. That is where human assignment takes a year.
3. A blinded protocol: the test case is built by someone else, the decision-maker never sees the
   reference constants, and there are more seeds.
4. Turn the decision aids into an API-driven agent with a fixed toolset (propose, what-if, series,
   release tests). Measure cost per round and the rate at which a human reviewer disagrees, i.e. make
   the human-in-the-loop part real.
5. Keep the codifiable lessons (Doppler-aware blends, release-before-reject, influence-based cleaning,
   series coherence) as defaults. Spend the judgement on recovery from wrong states and on hypothesis
   choice.

## 7. Reproducing
See `README.md`. In short: `scripts/setup.sh`; `scripts/sanity_check.sh`; `python3 -m assign.testcase
so2 --seed 1`; `python3 -m assign.engine so2 --arm ai --fresh` replays the AI run from the decision files
in `decisions/so2_s1/`; `scripts/run_automated.sh` runs the automated arms; `python3 -m assign.score
runs/<run>`, `python3 -m assign.tables`, `python3 -m assign.figures`.
