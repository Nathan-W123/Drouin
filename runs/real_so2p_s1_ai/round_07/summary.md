# real_so2p seed 1 arm ai -- round 7

assigned peaks 76, floating params 9, last rms (weighted) 0.958
predictions considered 48, with candidates 39, unresolvable windows 5, p_have=0.95 (from 32 sharp predictions)
candidate rows 120: default accept 1 (of which flagged 0), deferred with P>=0.5: 4

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 1068 | 20 6 14 21 5 17 | +2.6152 | +3.6 | 0.10 | +0.50 | 6 | keep |
| 2200 | 5 4 2 6 3 3 | -2.4969 | -3.1 | 0.02 | +0.39 | 4 | keep |
| 1987 | 11 5 7 12 4 8 | +1.5420 | +3.1 | 0.09 | +0.21 | 5 | keep |
| 163 | 25 3 23 24 4 20 | -0.0163 | -0.3 | 0.93 | +0.65 | 6 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 4000 | LK | 8 | 14.9 | 3.622e-06 | 3.9 | 37 | release |
| 3000 | PhiK | 6 | 13.9 | 0.0002127 | 3.7 | 0.12 | hold |
| 3100 | LKKJ | 8 | 3.3 | 1.681e-07 | 1.8 | 67 | hold |
| 1300 | LJJK | 8 | 1.2 | 1.201e-09 | 1.1 | 3.2e+02 | hold |
| 41299 | lJK | 8 | 0.8 | 6.059e-10 | 0.9 | 1.6e+02 | hold |
| 41100 | phiJK | 6 | 0.8 | 7.291e-07 | 0.9 | 0.16 | hold |
| 40200 | phiJ | 6 | 0.4 | 3.855e-09 | 0.6 | 0.056 | hold |
| 40300 | lJ | 8 | 0.4 | 2.976e-12 | 0.6 | 52 | hold |
| 42199 | lKJ | 8 | 0.3 | -4.719e-08 | 0.6 | 1.9e+02 | hold |
| 2200 | LJK | 8 | 0.2 | 4.57e-09 | 0.4 | 18 | hold |
| 1200 | PhiJK | 6 | 0.1 | 3.671e-07 | 0.3 | 0.08 | hold |
| 300 | PhiJ | 6 | 0.1 | 7.181e-09 | 0.3 | 0.1 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0002 | 4 4 0 5 3 3 | 6.03 | 2454 | +1.28 | +0.53 | 0.660 | 0.27 | 0.00 | multi |
| C0003 | 30 4 26 30 3 27 | 25.8 | 2387 | -0.61 | +0.46 | 0.645 | 0.12 | 0.00 | multi |
| C0004 | 14 5 9 15 4 12 | 20.9 | 1325 | -0.15 | +0.06 | 0.595 | 0.34 | 0.00 | multi |
| C0005 | 12 5 7 13 4 10 | 20.7 | 1623 | -0.09 | +0.23 | 0.525 | 0.44 | 0.00 | multi |

Unflagged default accepts: 1, min P 0.974, max |z| 0.34
