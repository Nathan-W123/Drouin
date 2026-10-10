# blind5 seed 1 arm ai -- round 5

assigned peaks 193, floating params 16, last rms (weighted) 0.831
predictions considered 431, with candidates 96, unresolvable windows 0, p_have=0.45 (from 466 sharp predictions)
candidate rows 97: default accept 2 (of which flagged 2), deferred with P>=0.5: 9

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 283 | 36 3 33 36 3 34 | +0.0656 | +1.1 | 0.84 | -0.38 | 4 | keep |
| 285 | 13 11 2 12 11 1;13 11 3 12 11 2 | -0.0023 | -0.4 | 0.80 | -0.00 | 4 | keep |
| 80 | 44 6 38 44 6 39 | +0.0015 | +0.9 | 0.95 | +0.14 | 4 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 1399 | LJJK | 8 | 7.4 | -1.723e-10 | 2.7 | 2.1 | hold |
| 399 | HJ | 6 | 5.3 | 6.94e-09 | 2.3 | 0.0072 | hold |
| 2299 | LJK | 8 | 1.4 | 2.856e-09 | 1.2 | 0.63 | hold |
| 4099 | LK | 8 | 0.8 | 4.219e-06 | 0.9 | 2.3 | hold |
| 50299 | l2 | 8 | 0.3 | 1.037e-13 | 0.4 | 0.07 | hold |
| 3199 | LKKJ | 8 | 0.2 | -1.807e-09 | 0.5 | 0.023 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|
| C0002 | 13 5 8 12 5 7 | 290 | -0.19 | +0.29 | 1.000 | blend | 13 5 9 12 5 8 |
| C0003 | 13 5 9 12 5 8 | 290 | +0.21 | +0.29 | 1.000 | blend | 13 5 8 12 5 7 |

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 39 6 33 39 6 34 | 0.49 | 59 | +0.00 | +0.00 | 1.000 | 0.00 | 0.05 | contested |
| C0004 | 36 5 31 36 5 32 | 1.19 | 86 | -0.02 | -0.46 | 1.000 | 0.00 | 0.96 | contested |
| C0005 | 30 1 29 29 3 26 | 140 | 86 | -1.47 | -0.28 | 0.964 | 0.00 | 1.00 | contested |
| C0006 | 41 3 38 40 5 35 | 668 | 88 | -0.81 | +0.28 | 0.933 | 0.00 | 0.00 |  |
| C0007 | 31 1 30 30 3 27 | 165 | 60 | +0.00 | -0.15 | 0.925 | 0.05 | 0.00 | multi |
| C0008 | 54 4 50 53 6 47 | 2.65e+03 | 184 | -1.43 | +0.22 | 0.838 | 0.00 | 0.00 |  |
| C0009 | 36 2 34 35 4 31 | 349 | 133 | +0.15 | +0.68 | 0.838 | 0.00 | 0.00 |  |
| C0010 | 46 3 43 45 5 40 | 1.19e+03 | 174 | -2.33 | -0.14 | 0.558 | 0.00 | 0.00 |  |
| C0011 | 45 3 42 44 5 39 | 1.06e+03 | 165 | -2.11 | +0.37 | 0.523 | 0.00 | 0.00 |  |
