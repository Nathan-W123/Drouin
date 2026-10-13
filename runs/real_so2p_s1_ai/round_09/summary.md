# real_so2p seed 1 arm ai -- round 9

assigned peaks 79, floating params 11, last rms (weighted) 0.722
predictions considered 45, with candidates 35, unresolvable windows 0, p_have=0.90 (from 61 sharp predictions)
candidate rows 51: default accept 1 (of which flagged 0), deferred with P>=0.5: 3

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 2200 | 5 4 2 6 3 3 | -2.6068 | -3.2 | 0.03 | +0.39 | 4 | keep |
| 163 | 25 3 23 24 4 20 | -0.0837 | -1.7 | 0.93 | +0.65 | 6 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 1300 | LJJK | 8 | 5.1 | 2.756e-09 | 2.3 | 7.3e+02 | hold |
| 43000 | lK | 8 | 3.1 | -1.62e-06 | 1.7 | 6.4e+02 | hold |
| 2200 | LJK | 8 | 2.6 | 5.237e-08 | 1.6 | 2.1e+02 | hold |
| 1200 | PhiJK | 6 | 2.2 | 2.106e-06 | 1.5 | 0.46 | hold |
| 41100 | phiJK | 6 | 1.9 | 1.11e-06 | 1.4 | 0.24 | hold |
| 41299 | lJK | 8 | 1.6 | 8.418e-10 | 1.2 | 2.2e+02 | hold |
| 400 | LJ | 8 | 1.1 | -2.118e-11 | 1.0 | 3.7e+02 | hold |
| 42199 | lKJ | 8 | 0.9 | -8.294e-08 | 1.0 | 3.3e+02 | hold |
| 300 | PhiJ | 6 | 0.7 | -2.157e-08 | 0.8 | 0.31 | hold |
| 4000 | LK | 8 | 0.4 | 2.289e-06 | 0.6 | 24 | hold |
| 3100 | LKKJ | 8 | 0.2 | 1.971e-07 | 0.5 | 78 | hold |
| 40200 | phiJ | 6 | 0.2 | 2.721e-09 | 0.4 | 0.039 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0002 | 20 7 13 21 6 16 | 5.05 | 2370 | +0.16 | +0.65 | 0.838 | 0.00 | 0.00 |  |
| C0003 | 22 7 15 23 6 18 | 8.14 | 1785 | -1.08 | +0.62 | 0.731 | 0.00 | 0.00 |  |
| C0004 | 30 4 26 30 3 27 | 24.2 | 2387 | -0.65 | +0.46 | 0.581 | 0.10 | 0.00 | multi |

Unflagged default accepts: 1, min P 0.991, max |z| 0.22
