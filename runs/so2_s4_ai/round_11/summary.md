# so2 seed 4 arm ai -- round 11

assigned peaks 431, floating params 25, last rms (weighted) 0.983
predictions considered 2023, with candidates 21, unresolvable windows 0, p_have=0.18 (from 2378 sharp predictions)
candidate rows 22: default accept 0 (of which flagged 0), deferred with P>=0.5: 6

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 471 | 51 8 44 52 5 47 | +0.0402 | +4.1 | 0.53 | -0.13 | 10 | reject |
| 613 | 63 4 60 64 1 63 | +0.0941 | +3.8 | 0.22 | -0.24 | 7 | keep |
| 512 | 71 6 66 72 3 69 | -0.0510 | -3.5 | 0.53 | +0.05 | 10 | keep |
| 31 | 35 6 30 34 7 27 | +0.0005 | +3.5 | 0.78 | +0.10 | 5 | keep |
| 26 | 40 7 33 39 8 32 | -0.0026 | -3.4 | 0.17 | +0.04 | 5 | keep |
| 495 | 43 3 41 44 0 44 | -0.0625 | -3.3 | 0.19 | -0.17 | 7 | keep |
| 331 | 49 6 44 48 7 41 | -0.4077 | -3.2 | 0.00 | -0.06 | 6 | keep |
| 422 | 69 8 62 68 9 59 | +0.0822 | +3.2 | 0.17 | +0.15 | 10 | keep |
| 479 | 70 7 63 70 6 64 | +0.0351 | +3.2 | 0.39 | -0.16 | 10 | keep |
| 33 | 61 11 51 60 12 48 | -0.0006 | -2.3 | 0.90 | -0.08 | 5 | keep |
| 30 | 49 4 46 48 5 43 | -0.0001 | -0.4 | 0.92 | +0.14 | 7 | keep |
| 493 | 70 5 65 71 4 68 | -0.0399 | -44.6 | 1.00 | -0.14 | 10 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 42199 | lKJ | 8 | 72.8 | 7.678e-11 | 8.6 | 0.35 | release |
| 2300 | PJJK | 10 | 38.0 | 1.552e-15 | 6.2 | 8.9 | hold |
| 5100 | SKKKJ | 12 | 13.0 | -1.782e-16 | 3.6 | 18 | hold |
| 6000 | SK | 12 | 12.0 | -1.491e-15 | 3.5 | 6.4 | hold |
| 3200 | PKKJ | 10 | 7.2 | 1.019e-14 | 2.7 | 0.89 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 79 7 73 80 4 76 | 16.8 | 488 | -0.01 | -0.02 | 0.996 | 0.00 | 0.45 | contested |
| C0002 | 90 11 79 89 12 78 | 62.7 | 591 | -0.00 | +0.35 | 0.941 | 0.00 | 0.88 | contested |
| C0003 | 47 18 30 48 17 31 | 1.22 | 621 | +1.48 | +0.77 | 0.911 | 0.00 | 0.00 | intensity |
| C0004 | 92 11 81 92 10 82 | 81.8 | 584 | +0.00 | -0.24 | 0.897 | 0.06 | 0.00 | multi |
| C0005 | 67 10 58 68 7 61 | 23.4 | 591 | +1.22 | -0.55 | 0.881 | 0.00 | 0.94 | contested |
| C0006 | 77 10 68 77 9 69 | 14.9 | 649 | -2.03 | -0.30 | 0.807 | 0.00 | 0.00 |  |
