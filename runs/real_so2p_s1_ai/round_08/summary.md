# real_so2p seed 1 arm ai -- round 8

assigned peaks 76, floating params 10, last rms (weighted) 0.857
predictions considered 48, with candidates 42, unresolvable windows 0, p_have=0.95 (from 50 sharp predictions)
candidate rows 65: default accept 2 (of which flagged 0), deferred with P>=0.5: 8

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 174 | 18 5 13 19 4 16 | -0.6600 | -3.0 | 0.23 | +0.14 | 5 | keep |
| 163 | 25 3 23 24 4 20 | -0.0751 | -1.6 | 0.93 | +0.65 | 6 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 2100 | PhiKJ | 6 | 15.8 | -3.285e-05 | 4.0 | 0.71 | release |
| 3100 | LKKJ | 8 | 10.6 | -6.568e-07 | 3.3 | 2.6e+02 | hold |
| 2200 | LJK | 8 | 8.2 | -4.119e-08 | 2.9 | 1.7e+02 | hold |
| 43000 | lK | 8 | 6.4 | 1.199e-06 | 2.5 | 4.8e+02 | hold |
| 41100 | phiJK | 6 | 1.6 | 1.041e-06 | 1.3 | 0.23 | hold |
| 41299 | lJK | 8 | 1.5 | 8.311e-10 | 1.2 | 2.2e+02 | hold |
| 4000 | LK | 8 | 1.0 | 4.064e-06 | 1.0 | 42 | hold |
| 1200 | PhiJK | 6 | 1.0 | -1.152e-06 | 1.0 | 0.25 | hold |
| 400 | LJ | 8 | 0.6 | -1.659e-11 | 0.8 | 2.9e+02 | hold |
| 40200 | phiJ | 6 | 0.4 | 3.851e-09 | 0.6 | 0.056 | hold |
| 40300 | lJ | 8 | 0.3 | 2.678e-12 | 0.5 | 47 | hold |
| 1300 | LJJK | 8 | 0.3 | 5.77e-10 | 0.5 | 1.5e+02 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0003 | 16 6 10 17 5 13 | 7.66 | 2068 | +0.16 | +0.40 | 0.942 | 0.04 | 0.00 |  |
| C0004 | 19 7 13 20 6 14 | 17.5 | 2662 | +1.07 | +0.45 | 0.937 | 0.00 | 0.00 |  |
| C0005 | 17 6 12 18 5 13 | 8.78 | 1714 | +0.11 | +0.58 | 0.923 | 0.01 | 0.00 |  |
| C0006 | 15 6 10 16 5 11 | 6.66 | 2308 | +2.10 | +0.25 | 0.919 | 0.00 | 0.00 |  |
| C0007 | 22 7 15 23 6 18 | 8.27 | 1785 | -0.98 | +0.62 | 0.865 | 0.00 | 0.00 |  |
| C0008 | 20 7 13 21 6 16 | 19.7 | 2370 | +0.17 | +0.65 | 0.746 | 0.00 | 0.00 |  |
| C0009 | 30 4 26 30 3 27 | 24.9 | 2387 | -0.65 | +0.46 | 0.646 | 0.12 | 0.00 | multi |
| C0010 | 14 5 9 15 4 12 | 3.36 | 1325 | -0.96 | +0.06 | 0.522 | 0.47 | 0.00 | multi |

Unflagged default accepts: 2, min P 0.993, max |z| 0.83
