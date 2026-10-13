# real_so2p seed 1 arm ai -- round 10

assigned peaks 81, floating params 11, last rms (weighted) 0.718
predictions considered 43, with candidates 33, unresolvable windows 0, p_have=0.90 (from 61 sharp predictions)
candidate rows 49: default accept 0 (of which flagged 0), deferred with P>=0.5: 2

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 2200 | 5 4 2 6 3 3 | -2.5718 | -3.2 | 0.03 | +0.39 | 4 | keep |
| 163 | 25 3 23 24 4 20 | -0.0864 | -1.7 | 0.93 | +0.65 | 6 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 1300 | LJJK | 8 | 4.7 | 2.629e-09 | 2.2 | 7e+02 | hold |
| 43000 | lK | 8 | 3.4 | -1.664e-06 | 1.8 | 6.6e+02 | hold |
| 2200 | LJK | 8 | 3.0 | 5.023e-08 | 1.7 | 2e+02 | hold |
| 1200 | PhiJK | 6 | 2.2 | 2.093e-06 | 1.5 | 0.46 | hold |
| 41100 | phiJK | 6 | 2.0 | 1.134e-06 | 1.4 | 0.25 | hold |
| 41299 | lJK | 8 | 1.6 | 8.584e-10 | 1.3 | 2.3e+02 | hold |
| 400 | LJ | 8 | 1.2 | -2.249e-11 | 1.1 | 4e+02 | hold |
| 300 | PhiJ | 6 | 0.8 | -2.369e-08 | 0.9 | 0.34 | hold |
| 4000 | LK | 8 | 0.7 | 1.413e-06 | 0.8 | 15 | hold |
| 3100 | LKKJ | 8 | 0.6 | 1.9e-07 | 0.8 | 75 | hold |
| 42199 | lKJ | 8 | 0.6 | -6.221e-08 | 0.8 | 2.5e+02 | hold |
| 40200 | phiJ | 6 | 0.2 | 2.754e-09 | 0.4 | 0.04 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 22 7 15 23 6 18 | 8.1 | 1785 | -1.14 | +0.62 | 0.718 | 0.00 | 0.00 |  |
| C0002 | 30 4 26 30 3 27 | 24.2 | 2387 | -0.66 | +0.46 | 0.581 | 0.10 | 0.00 | multi |
