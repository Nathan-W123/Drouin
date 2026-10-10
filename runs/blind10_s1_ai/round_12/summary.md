# blind10 seed 1 arm ai -- round 12

assigned peaks 285, floating params 22, last rms (weighted) 0.882
predictions considered 1848, with candidates 167, unresolvable windows 0, p_have=0.20 (from 1893 sharp predictions)
candidate rows 169: default accept 120 (of which flagged 0), deferred with P>=0.5: 7

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 430 | 55 16 40 56 15 41 | +0.3590 | +3.5 | 0.64 | -0.03 | 11 | keep |
| 4 | 48 10 38 49 9 41 | -0.0001 | -1.1 | 0.88 | +0.03 | 11 | keep |
| 35 | 35 6 30 34 7 27 | -0.0001 | -0.6 | 0.88 | -0.14 | 11 | keep |
| 2 | 60 11 49 59 12 48 | -0.0000 | -0.0 | 0.98 | -0.09 | 11 | keep |
| 164 | 42 4 38 43 3 41 | +0.0003 | +0.6 | 0.98 | +0.15 | 11 | keep |
| 21 | 63 13 51 64 12 52 | -0.0001 | -0.2 | 0.98 | +0.07 | 11 | keep |
| 180 | 53 12 42 54 11 43 | -0.0024 | -2.5 | 0.92 | +0.12 | 11 | keep |
| 650 | 63 4 60 64 1 63 | -0.0014 | -1.3 | 1.00 | +0.06 | 11 | keep |
| 448 | 72 8 64 72 7 65 | -0.0004 | -0.5 | 1.00 | +0.08 | 11 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 4100 | PKKKJ | 10 | 17.6 | -1.827e-12 | 4.2 | 39 | release |
| 5100 | SKKKJ | 12 | 16.9 | -3.722e-15 | 4.1 | 2.4e+03 | hold |
| 3200 | PKKJ | 10 | 14.8 | -6.31e-14 | 3.9 | 17 | hold |
| 2300 | PJJK | 10 | 11.3 | -3.325e-15 | 3.4 | 37 | hold |
| 43000 | lK | 8 | 5.2 | -9.157e-09 | 2.4 | 6.4 | hold |
| 6000 | SK | 12 | 1.3 | 2.155e-14 | 1.2 | 7e+02 | hold |
| 1300 | LJJK | 8 | 0.5 | -9.489e-13 | 0.8 | 0.36 | hold |
| 41299 | lJK | 8 | 0.1 | 2.503e-13 | 0.4 | 0.094 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0009 | 52 3 49 53 2 52 | 0.632 | 514 | +0.19 | -0.10 | 0.999 | 0.00 | 0.18 | contested |
| C0058 | 72 4 68 73 3 71 | 5.89 | 652 | -0.25 | -0.19 | 0.997 | 0.00 | 0.22 | contested |
| C0066 | 79 7 73 80 4 76 | 10.5 | 503 | -0.12 | -0.28 | 0.996 | 0.00 | 0.99 | contested |
| C0097 | 75 21 55 76 20 56 | 30.3 | 503 | -0.61 | -0.21 | 0.988 | 0.00 | 1.00 | contested |
| C0125 | 68 22 46 69 21 49 | 18.9 | 654 | +1.85 | -0.05 | 0.948 | 0.00 | 0.00 |  |
| C0126 | 74 9 65 74 8 66 | 10.7 | 513 | +0.38 | -0.18 | 0.805 | 0.18 | 0.00 | multi |
| C0127 | 73 23 51 74 22 52 | 30.6 | 653 | +1.81 | +0.23 | 0.705 | 0.22 | 0.00 | multi |

Unflagged default accepts: 120, min P 0.951, max |z| 1.90
