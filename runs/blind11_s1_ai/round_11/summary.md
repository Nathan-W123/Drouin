# blind11 seed 1 arm ai -- round 11

assigned peaks 393, floating params 24, last rms (weighted) 0.954
predictions considered 1868, with candidates 45, unresolvable windows 0, p_have=0.19 (from 2244 sharp predictions)
candidate rows 45: default accept 26 (of which flagged 0), deferred with P>=0.5: 8

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 34 | 35 6 30 34 7 27 | +0.0012 | +5.8 | 0.62 | +0.19 | 9 | reject |
| 20 | 63 13 51 64 12 52 | +0.0056 | +4.9 | 0.54 | -0.07 | 9 | keep |
| 184 | 53 12 42 54 11 43 | -0.0103 | -3.4 | 0.19 | -0.10 | 9 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 5000 | PK | 10 | 62.9 | 5.134e-12 | 7.9 | 6.2 | release |
| 2300 | PJJK | 10 | 55.5 | 1.148e-15 | 7.5 | 14 | hold |
| 3200 | PKKJ | 10 | 51.3 | 1.647e-14 | 7.2 | 4.9 | hold |
| 4100 | PKKKJ | 10 | 49.6 | 2.703e-13 | 7.0 | 7.5 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0010 | 72 4 68 73 3 71 | 0.0454 | 680 | -0.61 | -0.18 | 1.000 | 0.00 | 0.66 | contested |
| C0012 | 79 7 73 80 4 76 | 0.0837 | 520 | +1.78 | -0.16 | 1.000 | 0.00 | 0.95 | contested |
| C0029 | 75 21 55 76 20 56 | 6.52 | 520 | -2.50 | -0.14 | 0.949 | 0.00 | 1.00 | contested |
| C0030 | 78 22 56 79 21 59 | 9.92 | 557 | +2.87 | +0.08 | 0.946 | 0.00 | 0.00 |  |
| C0031 | 69 20 50 70 19 51 | 4.04 | 542 | +2.39 | -0.04 | 0.945 | 0.00 | 0.00 |  |
| C0032 | 70 20 50 71 19 53 | 4.09 | 522 | +2.29 | +0.32 | 0.912 | 0.00 | 0.00 |  |
| C0033 | 74 21 53 75 20 56 | 6.44 | 541 | +2.59 | +0.09 | 0.908 | 0.00 | 0.00 |  |
| C0034 | 73 23 51 74 22 52 | 13.8 | 680 | -2.12 | +0.58 | 0.660 | 0.00 | 1.00 | contested |

Unflagged default accepts: 26, min P 0.953, max |z| 2.72
