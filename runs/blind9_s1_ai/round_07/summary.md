# blind9 seed 1 arm ai -- round 7

assigned peaks 163, floating params 16, last rms (weighted) 0.748
predictions considered 384, with candidates 107, unresolvable windows 0, p_have=0.48 (from 330 sharp predictions)
candidate rows 111: default accept 1 (of which flagged 0), deferred with P>=0.5: 9

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 175 | 5 3 3 4 3 2 | -0.1578 | -3.1 | 0.02 | -0.09 | 4 | keep |
| 135 | 20 3 17 21 1 20 | -0.0018 | -0.3 | 0.83 | -0.14 | 4 | keep |
| 231 | 9 7 2 8 7 1;9 7 3 8 7 2 | -0.0034 | -0.5 | 0.98 | -0.21 | 4 | keep |
| 77 | 32 2 30 31 4 27 | +0.0186 | +0.8 | 0.92 | +0.07 | 5 | keep |
| 65 | 31 1 30 30 3 27 | -0.0003 | -0.1 | 0.91 | -0.13 | 6 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 399 | HJ | 6 | 0.5 | 6.092e-09 | 0.7 | 0.0029 | hold |
| 50299 | l2 | 8 | 0.4 | -2.489e-13 | 0.6 | 0.055 | hold |
| 2199 | HKJ | 6 | 0.4 | 1.073e-05 | 0.6 | 0.013 | hold |
| 2299 | LJK | 8 | 0.1 | 1.729e-09 | 0.2 | 0.47 | hold |
| 4099 | LK | 8 | 0.1 | 5.809e-06 | 0.1 | 7.5 | hold |
| 1399 | LJJK | 8 | -0.0 | 9.016e-12 | 0.1 | 0.069 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 10 4 6 9 4 5 | 4.29 | 244 | -0.00 | -0.08 | 1.000 | 0.00 | 0.99 | contested |
| C0003 | 10 4 7 9 4 6 | 4.29 | 244 | +2.37 | -0.08 | 0.993 | 0.00 | 1.00 | contested |
| C0004 | 23 3 20 24 1 23 | 105 | 83 | +0.00 | -0.12 | 0.992 | 0.00 | 0.96 | contested |
| C0005 | 25 1 24 24 3 21 | 128 | 83 | -1.74 | -0.00 | 0.960 | 0.00 | 0.99 | contested |
| C0006 | 47 3 44 46 5 41 | 2.98e+03 | 200 | +0.51 | -0.32 | 0.739 | 0.00 | 0.00 |  |
| C0007 | 9 4 6 8 4 5 | 3.76 | 232 | +0.05 | -0.15 | 0.727 | 0.27 | 0.37 | multi,contested |
| C0008 | 9 4 5 8 4 4 | 3.76 | 233 | +0.01 | +0.26 | 0.629 | 0.37 | 0.27 | multi,contested |
| C0009 | 8 4 4 7 4 3 | 3.3 | 212 | -0.07 | -0.02 | 0.551 | 0.45 | 0.48 | multi,contested |
| C0010 | 8 4 5 7 4 4 | 3.3 | 211 | +0.04 | +0.02 | 0.520 | 0.48 | 0.45 | multi,contested |

Unflagged default accepts: 1, min P 0.998, max |z| 0.00
