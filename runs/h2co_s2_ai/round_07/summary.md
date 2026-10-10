# h2co seed 2 arm ai -- round 7

assigned peaks 185, floating params 16, last rms (weighted) 0.804
predictions considered 366, with candidates 56, unresolvable windows 0, p_have=0.45 (from 439 sharp predictions)
candidate rows 58: default accept 0 (of which flagged 0), deferred with P>=0.5: 6

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 287 | 20 1 19 20 1 20 | +0.0276 | +1.5 | 0.81 | -0.05 | 5 | keep |
| 273 | 36 3 33 36 3 34 | -0.0203 | -0.4 | 0.86 | -0.25 | 6 | keep |
| 76 | 44 6 38 44 6 39 | -0.0019 | -1.2 | 0.95 | +0.14 | 6 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 2299 | LJK | 8 | 2.8 | 3.761e-09 | 1.7 | 1 | hold |
| 50299 | l2 | 8 | 2.5 | -3.915e-13 | 1.6 | 0.31 | hold |
| 1399 | LJJK | 8 | 1.2 | 7.861e-11 | 1.1 | 1.2 | hold |
| 399 | HJ | 6 | 0.9 | 2.783e-09 | 0.9 | 0.0033 | hold |
| 4099 | LK | 8 | 0.7 | 3.362e-06 | 0.8 | 2.3 | hold |
| 3199 | LKKJ | 8 | 0.1 | -1.176e-09 | 0.3 | 0.012 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 39 6 33 39 6 34 | 0.416 | 49 | -0.02 | -0.01 | 1.000 | 0.00 | 0.06 | contested |
| C0002 | 36 5 31 36 5 32 | 1.01 | 82 | -0.00 | +0.16 | 1.000 | 0.00 | 0.94 | contested |
| C0003 | 30 1 29 29 3 26 | 124 | 82 | -1.59 | +0.41 | 0.936 | 0.00 | 1.00 | contested |
| C0004 | 31 1 30 30 3 27 | 146 | 50 | +0.00 | +0.02 | 0.921 | 0.06 | 0.00 | multi |
| C0005 | 32 2 30 31 4 27 | 171 | 64 | +0.00 | +0.06 | 0.883 | 0.10 | 0.00 | multi |
| C0006 | 45 3 42 44 5 39 | 939 | 169 | -2.28 | -0.07 | 0.813 | 0.00 | 0.00 |  |
