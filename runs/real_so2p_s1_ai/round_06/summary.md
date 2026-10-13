# real_so2p seed 1 arm ai -- round 6

assigned peaks 71, floating params 9, last rms (weighted) 0.884
predictions considered 53, with candidates 43, unresolvable windows 5, p_have=0.95 (from 31 sharp predictions)
candidate rows 130: default accept 1 (of which flagged 0), deferred with P>=0.5: 9

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 957 | 15 5 11 16 4 12 | +0.8629 | +3.5 | 0.20 | +0.32 | 5 | keep |
| 1987 | 11 5 7 12 4 8 | +1.6353 | +3.3 | 0.11 | +0.21 | 5 | keep |
| 2200 | 5 4 2 6 3 3 | -2.4797 | -3.1 | 0.02 | +0.39 | 4 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 3000 | PhiK | 6 | 4.7 | 0.0001815 | 2.2 | 0.1 | hold |
| 43000 | lK | 8 | 4.4 | 1.032e-06 | 2.1 | 4.1e+02 | hold |
| 4000 | LK | 8 | 3.8 | 3.438e-06 | 2.0 | 35 | hold |
| 2200 | LJK | 8 | 3.7 | -2.621e-08 | 1.9 | 1.1e+02 | hold |
| 42199 | lKJ | 8 | 2.5 | -1.427e-07 | 1.6 | 5.7e+02 | hold |
| 2100 | PhiKJ | 6 | 2.3 | -9.999e-06 | 1.5 | 0.22 | hold |
| 300 | PhiJ | 6 | 2.2 | 5.899e-08 | 1.5 | 0.85 | hold |
| 1200 | PhiJK | 6 | 1.4 | -1.765e-06 | 1.2 | 0.38 | hold |
| 400 | LJ | 8 | 0.9 | 3.081e-11 | 1.0 | 5.4e+02 | hold |
| 3100 | LKKJ | 8 | 0.8 | -1.342e-07 | 0.9 | 53 | hold |
| 1300 | LJJK | 8 | 0.7 | 1.187e-09 | 0.8 | 3.2e+02 | hold |
| 41299 | lJK | 8 | 0.4 | 5.086e-10 | 0.7 | 1.4e+02 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0002 | 22 2 20 22 1 21 | 9.72 | 1743 | -0.01 | +0.17 | 0.895 | 0.10 | 0.00 | multi |
| C0003 | 25 3 23 24 4 20 | 14.8 | 163 | -0.03 | +0.65 | 0.824 | 0.14 | 0.00 | multi |
| C0004 | 9 5 5 10 4 6 | 20.7 | 2541 | +0.05 | +0.11 | 0.702 | 0.28 | 0.00 | multi |
| C0005 | 20 6 14 21 5 17 | 57.1 | 1068 | +0.05 | +0.50 | 0.671 | 0.05 | 0.00 | multi |
| C0006 | 4 4 0 5 3 3 | 6.03 | 2454 | +1.28 | +0.53 | 0.659 | 0.27 | 0.00 | multi |
| C0007 | 30 4 26 30 3 27 | 25.8 | 2387 | -0.61 | +0.46 | 0.645 | 0.12 | 0.00 | multi |
| C0008 | 14 5 9 15 4 12 | 20.9 | 1325 | -0.15 | +0.06 | 0.595 | 0.34 | 0.00 | multi |
| C0009 | 12 5 7 13 4 10 | 20.7 | 1623 | -0.09 | +0.23 | 0.524 | 0.45 | 0.00 | multi |
| C0010 | 18 2 16 17 3 15 | 3.55 | 1198 | -0.04 | +0.14 | 0.522 | 0.47 | 0.00 | multi |

Unflagged default accepts: 1, min P 0.974, max |z| 0.33
