# blind6 seed 1 arm ai -- round 9

assigned peaks 388, floating params 25, last rms (weighted) 0.953
predictions considered 1749, with candidates 52, unresolvable windows 0, p_have=0.19 (from 1993 sharp predictions)
candidate rows 53: default accept 21 (of which flagged 0), deferred with P>=0.5: 5

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 522 | 54 17 37 55 16 40 | +0.0658 | +4.3 | 0.24 | -0.06 | 8 | reject |
| 450 | 58 17 41 59 16 44 | -0.0816 | -3.4 | 0.14 | -0.08 | 8 | keep |
| 513 | 66 8 58 65 9 57 | -0.0441 | -3.1 | 0.34 | -0.06 | 8 | keep |
| 467 | 57 17 41 58 16 42 | -0.0461 | -3.0 | 0.23 | +0.06 | 8 | keep |
| 21 | 63 13 51 64 12 52 | +0.0020 | +2.9 | 0.84 | +0.08 | 5 | keep |
| 630 | 75 23 53 76 22 54 | -0.0635 | -3.3 | 0.99 | +0.08 | 8 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 4100 | PKKKJ | 10 | 62.0 | -1.163e-12 | 7.9 | 9.1 | release |
| 5100 | SKKKJ | 12 | 42.6 | -7.017e-16 | 6.5 | 1.1e+02 | hold |
| 2300 | PJJK | 10 | 11.9 | 1.651e-15 | 3.4 | 9.2 | hold |
| 6000 | SK | 12 | 11.5 | -3.795e-15 | 3.4 | 19 | hold |
| 1300 | LJJK | 8 | 1.3 | -2.394e-13 | 1.1 | 0.065 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 14 8 6 15 7 9 | 0.00502 | 429 | -0.77 | -0.05 | 1.000 | 0.00 | 0.61 | contested |
| C0002 | 52 3 49 53 2 52 | 0.714 | 515 | +0.03 | -0.03 | 1.000 | 0.00 | 0.35 | contested |
| C0005 | 79 7 73 80 4 76 | 6.23 | 506 | +0.02 | -0.06 | 0.998 | 0.00 | 0.43 | contested |
| C0025 | 74 9 65 74 8 66 | 13.4 | 514 | -0.00 | +0.22 | 0.644 | 0.35 | 0.00 | multi |
| C0026 | 54 7 47 54 6 48 | 1.53 | 429 | -3.27 | +0.56 | 0.612 | 0.00 | 1.00 | contested,far |

Unflagged default accepts: 21, min P 0.993, max |z| 0.55
