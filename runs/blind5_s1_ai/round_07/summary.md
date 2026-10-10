# blind5 seed 1 arm ai -- round 7

assigned peaks 195, floating params 17, last rms (weighted) 0.803
predictions considered 429, with candidates 94, unresolvable windows 0, p_have=0.45 (from 466 sharp predictions)
candidate rows 94: default accept 2 (of which flagged 2), deferred with P>=0.5: 7

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 285 | 13 11 2 12 11 1;13 11 3 12 11 2 | -0.0058 | -0.9 | 0.81 | -0.00 | 4 | keep |
| 69 | 32 2 30 31 4 27 | -0.0048 | -0.1 | 0.81 | +0.11 | 4 | keep |
| 80 | 44 6 38 44 6 39 | -0.0005 | -0.3 | 0.96 | +0.14 | 4 | keep |
| 60 | 31 1 30 30 3 27 | +0.0002 | +0.1 | 0.98 | -0.15 | 5 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 399 | HJ | 6 | 2.0 | 3.39e-09 | 1.4 | 0.0035 | hold |
| 2299 | LJK | 8 | 1.8 | 3.288e-09 | 1.3 | 0.73 | hold |
| 4099 | LK | 8 | 1.7 | 6.191e-06 | 1.3 | 3.4 | hold |
| 3199 | LKKJ | 8 | 0.9 | -3.822e-09 | 1.0 | 0.048 | hold |
| 50299 | l2 | 8 | 0.7 | -2.162e-13 | 0.9 | 0.15 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|
| C0001 | 13 5 8 12 5 7 | 290 | -0.20 | +0.29 | 1.000 | blend | 13 5 9 12 5 8 |
| C0002 | 13 5 9 12 5 8 | 290 | +0.20 | +0.29 | 1.000 | blend | 13 5 8 12 5 7 |

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0003 | 36 5 31 36 5 32 | 1.18 | 86 | -0.02 | -0.46 | 1.000 | 0.00 | 0.96 | contested |
| C0004 | 30 1 29 29 3 26 | 140 | 86 | -1.47 | -0.28 | 0.964 | 0.00 | 1.00 | contested |
| C0005 | 41 3 38 40 5 35 | 668 | 88 | -0.82 | +0.28 | 0.933 | 0.00 | 0.00 |  |
| C0006 | 36 2 34 35 4 31 | 349 | 133 | +0.15 | +0.68 | 0.838 | 0.00 | 0.00 |  |
| C0007 | 54 4 50 53 6 47 | 2.65e+03 | 184 | -1.44 | +0.22 | 0.835 | 0.00 | 0.00 |  |
| C0008 | 46 3 43 45 5 40 | 1.19e+03 | 174 | -2.33 | -0.14 | 0.555 | 0.00 | 0.00 |  |
| C0009 | 45 3 42 44 5 39 | 1.06e+03 | 165 | -2.11 | +0.37 | 0.520 | 0.00 | 0.00 |  |
