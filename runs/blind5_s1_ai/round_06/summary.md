# blind5 seed 1 arm ai -- round 6

assigned peaks 194, floating params 16, last rms (weighted) 0.839
predictions considered 430, with candidates 95, unresolvable windows 0, p_have=0.45 (from 466 sharp predictions)
candidate rows 95: default accept 3 (of which flagged 2), deferred with P>=0.5: 7

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 285 | 13 11 2 12 11 1;13 11 3 12 11 2 | -0.0013 | -0.2 | 0.80 | -0.00 | 4 | keep |
| 80 | 44 6 38 44 6 39 | +0.0019 | +1.2 | 0.95 | +0.14 | 4 | keep |
| 60 | 31 1 30 30 3 27 | +0.0051 | +1.8 | 0.96 | -0.15 | 5 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 1399 | LJJK | 8 | 10.7 | -1.753e-10 | 3.3 | 2.1 | release |
| 399 | HJ | 6 | 8.4 | 5.95e-09 | 2.9 | 0.0062 | hold |
| 50299 | l2 | 8 | 2.2 | 2.792e-13 | 1.4 | 0.19 | hold |
| 2299 | LJK | 8 | 1.4 | 2.87e-09 | 1.2 | 0.64 | hold |
| 4099 | LK | 8 | 0.3 | 2.644e-06 | 0.6 | 1.5 | hold |
| 3199 | LKKJ | 8 | 0.0 | -5.905e-10 | 0.2 | 0.0074 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|
| C0002 | 13 5 8 12 5 7 | 290 | -0.19 | +0.29 | 1.000 | blend | 13 5 9 12 5 8 |
| C0003 | 13 5 9 12 5 8 | 290 | +0.21 | +0.29 | 1.000 | blend | 13 5 8 12 5 7 |

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0004 | 36 5 31 36 5 32 | 1.19 | 86 | -0.03 | -0.46 | 1.000 | 0.00 | 0.96 | contested |
| C0005 | 30 1 29 29 3 26 | 140 | 86 | -1.47 | -0.28 | 0.964 | 0.00 | 1.00 | contested |
| C0006 | 41 3 38 40 5 35 | 668 | 88 | -0.81 | +0.28 | 0.933 | 0.00 | 0.00 |  |
| C0007 | 54 4 50 53 6 47 | 2.65e+03 | 184 | -1.43 | +0.22 | 0.838 | 0.00 | 0.00 |  |
| C0008 | 36 2 34 35 4 31 | 349 | 133 | +0.15 | +0.68 | 0.837 | 0.00 | 0.00 |  |
| C0009 | 46 3 43 45 5 40 | 1.19e+03 | 174 | -2.33 | -0.14 | 0.558 | 0.00 | 0.00 |  |
| C0010 | 45 3 42 44 5 39 | 1.06e+03 | 165 | -2.11 | +0.37 | 0.523 | 0.00 | 0.00 |  |

Unflagged default accepts: 1, min P 1.000, max |z| 0.00
