# blind10 seed 1 arm ai -- round 13

assigned peaks 387, floating params 25, last rms (weighted) 0.995
predictions considered 1745, with candidates 26, unresolvable windows 0, p_have=0.19 (from 2131 sharp predictions)
candidate rows 26: default accept 19 (of which flagged 0), deferred with P>=0.5: 5

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 473 | 57 17 41 58 16 42 | +0.0584 | +4.3 | 0.40 | -0.02 | 12 | reject |
| 510 | 66 8 58 65 9 57 | -0.0537 | -3.8 | 0.33 | +0.21 | 12 | keep |
| 452 | 64 18 46 65 17 49 | -0.1098 | -3.5 | 0.21 | -0.07 | 12 | keep |
| 491 | 72 9 63 71 10 62 | +0.0390 | +3.1 | 0.48 | -0.10 | 12 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 4100 | PKKKJ | 10 | 48.5 | -5.716e-13 | 7.0 | 12 | release |
| 3200 | PKKJ | 10 | 24.1 | -1.664e-14 | 4.9 | 4.5 | hold |
| 5100 | SKKKJ | 12 | 20.9 | -6.078e-16 | 4.6 | 3.8e+02 | hold |
| 6000 | SK | 12 | 4.7 | 2.786e-15 | 2.2 | 91 | hold |
| 2300 | PJJK | 10 | 3.2 | -3.349e-16 | 1.8 | 3.8 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0020 | 65 21 45 66 20 46 | 2.65 | 634 | +2.92 | -0.02 | 0.928 | 0.00 | 0.00 |  |
| C0021 | 64 21 43 65 20 46 | 2.55 | 649 | +3.31 | +0.05 | 0.830 | 0.00 | 0.00 | far |
| C0022 | 73 23 51 74 22 52 | 6.49 | 653 | +3.04 | +0.23 | 0.694 | 0.00 | 0.00 | far |
| C0023 | 68 22 46 69 21 49 | 4.04 | 654 | +3.41 | -0.05 | 0.577 | 0.00 | 0.00 | far |
| C0024 | 63 21 43 64 20 44 | 2.45 | 656 | +3.68 | -0.07 | 0.508 | 0.00 | 0.00 | far |

Unflagged default accepts: 19, min P 0.952, max |z| 2.64
