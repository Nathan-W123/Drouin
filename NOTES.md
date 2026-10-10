# Working notes

## Step 1 — tools and sanity check (2026-10-10)

- `scripts/setup.sh` downloads Pickett.zip (SPFIT/SPCAT source), CDMS files and docs, and builds
  `spfit`/`spcat` with gcc (`make spfit spcat`; compiler warnings only). Both binaries show the
  "Enter file name" prompt. `pyckett` 0.2.2 is installed and parses the .lin/.cat files.
- CDMS does not publish `SO2.var`/`SO2.cat` in that directory; the catalog files are `c064502i.cat` etc.
- **Sanity check** (`scripts/sanity_check.sh`): SPFIT on the official `SO2.par` + `SO2.lin`
  (2428 lines, 59 params) reproduces the official `SO2.fit`:
  - weighted RMS 0.87499 (identical), MW RMS 0.067816 MHz (identical)
  - all 58 final parameter values and uncertainties identical
  - 2427/2428 calc frequencies identical; one differs by 1e-5 MHz (last printed digit)
  - only other differences: exponent formatting and the "NORMALIZED DIAGONAL" diagnostic block
    (CDMS's file was made in 2005 with an older SPFIT build).

### What's in SO2.lin
| upper v | lower v | units | rows |
|---|---|---|---|
| 0 | 0 | MHz (pure rotation, ground state) | 680 |
| 1 | 1 | MHz (pure rotation, v2=1) | 356 |
| 1 | 0 | cm-1 (v2 band, IR) | 1392 |

Ground-state rows: 662 ordinary lines (1.0–3198 GHz, J ≤ 92, Ka ≤ 28; 12 rows in true blends) plus
18 rows below 1 GHz that are *difference* pseudo-lines: pairs of rows with identical freq/error where one
transition is written reversed, so SPFIT fits the difference of two transitions. These are not
spectral peaks and will be excluded from the assignment test.

### Ground-state-only reference fit
680 v=0 MW rows + the 30 v=0 parameters (NVIB=1) → weighted RMS 0.720, MW RMS 0.0736 MHz; constants agree
with the full official fit within ~1σ. This is the reference for scoring the SO2 test.

### Format gotchas found (worth remembering)
- With NVIB=1, `v` is dropped from the quantum numbers: 3 per state (N Ka Kc), not 4.
- The frequency field must start at column 37 of the .lin line (QN field is 12×I3 = 36 cols).
- A long .par title line crashes SPFIT ("stack smashing detected") — keep titles short.
- SPFIT overwrites the .par (old copy → .bak), so always run in a scratch copy.
