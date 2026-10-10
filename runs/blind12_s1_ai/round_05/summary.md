# blind12 seed 1 arm ai -- round 5

assigned peaks 160, floating params 16, last rms (weighted) 0.827
predictions considered 390, with candidates 89, unresolvable windows 0, p_have=0.42 (from 386 sharp predictions)
candidate rows 92: default accept 2 (of which flagged 0), deferred with P>=0.5: 6

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 212 | 9 8 1 8 8 0;9 8 2 8 8 1 | -0.0458 | -1.4 | 0.85 | -0.66 | 3 | keep |
| 90 | 26 1 25 25 3 22 | +0.0020 | +0.2 | 0.92 | +0.08 | 3 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 3199 | LKKJ | 8 | 2.1 | -1.917e-07 | 1.5 | 2.9 | hold |
| 4099 | LK | 8 | 1.1 | -4.611e-05 | 1.0 | 68 | hold |
| 50299 | l2 | 8 | 0.8 | -4.711e-13 | 0.9 | 0.1 | hold |
| 1399 | LJJK | 8 | 0.4 | 1.212e-10 | 0.7 | 0.98 | hold |
| 399 | HJ | 6 | 0.1 | 3.304e-09 | 0.4 | 0.0016 | hold |
| 2299 | LJK | 8 | -0.0 | 2.242e-09 | 0.2 | 0.66 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 36 5 31 36 5 32 | 3.58 | 85 | -0.00 | +0.03 | 1.000 | 0.00 | 0.46 | contested |
| C0004 | 46 2 44 45 4 41 | 2.6e+03 | 82 | +0.64 | +0.24 | 0.905 | 0.00 | 0.00 |  |
| C0005 | 23 3 20 24 1 23 | 101 | 75 | -0.00 | -0.15 | 0.888 | 0.10 | 0.17 | multi,contested |
| C0006 | 25 1 24 24 3 21 | 123 | 76 | +0.00 | +0.05 | 0.818 | 0.17 | 0.10 | multi,contested |
| C0007 | 45 2 43 44 4 40 | 2.33e+03 | 107 | -1.50 | +0.09 | 0.699 | 0.00 | 0.00 |  |
| C0008 | 30 1 29 29 3 26 | 307 | 86 | +0.00 | +0.13 | 0.526 | 0.46 | 0.00 | multi |

Unflagged default accepts: 2, min P 0.959, max |z| 0.00
