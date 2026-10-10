# blind12 seed 1 arm ai -- round 6

assigned peaks 162, floating params 16, last rms (weighted) 0.823
predictions considered 388, with candidates 87, unresolvable windows 0, p_have=0.42 (from 386 sharp predictions)
candidate rows 90: default accept 0 (of which flagged 0), deferred with P>=0.5: 6

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 212 | 9 8 1 8 8 0;9 8 2 8 8 1 | -0.0447 | -1.4 | 0.85 | -0.66 | 3 | keep |
| 60 | 31 1 30 30 3 27 | -0.0002 | -0.1 | 1.00 | +0.22 | 5 | keep |
| 68 | 32 2 30 31 4 27 | +0.0070 | +0.3 | 0.91 | -0.16 | 5 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 3199 | LKKJ | 8 | 2.0 | -1.817e-07 | 1.4 | 2.8 | hold |
| 4099 | LK | 8 | 1.0 | -3.768e-05 | 1.0 | 56 | hold |
| 50299 | l2 | 8 | 0.6 | -3.045e-13 | 0.8 | 0.068 | hold |
| 1399 | LJJK | 8 | 0.2 | 6.253e-11 | 0.5 | 0.51 | hold |
| 2299 | LJK | 8 | 0.0 | 4.671e-10 | 0.0 | 0.14 | hold |
| 399 | HJ | 6 | -0.0 | 2.01e-09 | 0.2 | 0.00096 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 36 5 31 36 5 32 | 3.58 | 85 | -0.00 | +0.03 | 1.000 | 0.00 | 0.46 | contested |
| C0002 | 46 2 44 45 4 41 | 2.6e+03 | 82 | +0.64 | +0.24 | 0.905 | 0.00 | 0.00 |  |
| C0003 | 23 3 20 24 1 23 | 101 | 75 | -0.00 | -0.15 | 0.888 | 0.10 | 0.17 | multi,contested |
| C0004 | 25 1 24 24 3 21 | 123 | 76 | +0.00 | +0.05 | 0.818 | 0.17 | 0.10 | multi,contested |
| C0005 | 45 2 43 44 4 40 | 2.33e+03 | 107 | -1.50 | +0.09 | 0.699 | 0.00 | 0.00 |  |
| C0006 | 30 1 29 29 3 26 | 307 | 86 | +0.00 | +0.13 | 0.526 | 0.46 | 0.00 | multi |
