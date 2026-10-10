# blind9 seed 1 arm ai -- round 5

assigned peaks 119, floating params 15, last rms (weighted) 0.799
predictions considered 428, with candidates 155, unresolvable windows 2, p_have=0.49 (from 324 sharp predictions)
candidate rows 160: default accept 41 (of which flagged 0), deferred with P>=0.5: 13

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 175 | 5 3 3 4 3 2 | -0.1541 | -3.1 | 0.04 | -0.09 | 4 | keep |
| 231 | 9 7 2 8 7 1;9 7 3 8 7 2 | -0.0053 | -0.8 | 0.98 | -0.21 | 4 | keep |
| 135 | 20 3 17 21 1 20 | +0.0003 | +0.3 | 1.00 | -0.14 | 4 | keep |
| 194 | 26 4 22 27 2 25 | +0.0020 | +0.2 | 0.96 | -0.10 | 4 | keep |
| 169 | 27 4 23 28 2 26 | -0.0017 | -0.2 | 0.96 | -0.00 | 4 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 2199 | HKJ | 6 | 1.3 | 2.216e-05 | 1.1 | 0.028 | hold |
| 399 | HJ | 6 | 1.1 | 3.787e-08 | 1.1 | 0.018 | hold |
| 4099 | LK | 8 | 0.4 | 6.839e-05 | 0.7 | 88 | hold |
| 1399 | LJJK | 8 | 0.2 | 3.106e-10 | 0.5 | 2.4 | hold |
| 50299 | l2 | 8 | 0.1 | -5.649e-13 | 0.4 | 0.12 | hold |
| 2299 | LJK | 8 | 0.1 | 1.255e-08 | 0.4 | 3.4 | hold |
| 60199 | l3 | 8 | -0.1 | 4.493e-14 | 0.1 | 0.0099 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0027 | 10 4 6 9 4 5 | 4.29 | 244 | -0.00 | -0.08 | 1.000 | 0.00 | 0.99 | contested |
| C0041 | 36 5 31 36 5 32 | 19.1 | 93 | -0.01 | -0.34 | 0.997 | 0.00 | 0.30 | contested |
| C0042 | 10 4 7 9 4 6 | 4.29 | 244 | +2.37 | -0.08 | 0.994 | 0.00 | 1.00 | contested |
| C0045 | 23 3 20 24 1 23 | 105 | 83 | +0.00 | -0.12 | 0.985 | 0.00 | 0.93 | contested |
| C0046 | 32 2 30 31 4 27 | 455 | 77 | +0.00 | +0.07 | 0.930 | 0.00 | 0.00 |  |
| C0047 | 25 1 24 24 3 21 | 128 | 83 | -1.75 | -0.00 | 0.925 | 0.00 | 0.98 | contested |
| C0048 | 31 1 30 30 3 27 | 366 | 65 | -0.00 | -0.13 | 0.887 | 0.00 | 0.00 |  |
| C0049 | 47 3 44 46 5 41 | 2.98e+03 | 200 | +0.51 | -0.32 | 0.745 | 0.00 | 0.00 |  |
| C0050 | 9 4 6 8 4 5 | 3.76 | 232 | +0.05 | -0.15 | 0.727 | 0.27 | 0.37 | multi,contested |
| C0051 | 30 1 29 29 3 26 | 311 | 95 | -0.00 | -0.05 | 0.683 | 0.30 | 0.00 | multi |
| C0052 | 9 4 5 8 4 4 | 3.76 | 233 | +0.01 | +0.26 | 0.629 | 0.37 | 0.27 | multi,contested |
| C0053 | 8 4 4 7 4 3 | 3.3 | 212 | -0.07 | -0.02 | 0.551 | 0.45 | 0.48 | multi,contested |
| C0054 | 8 4 5 7 4 4 | 3.3 | 211 | +0.05 | +0.02 | 0.520 | 0.48 | 0.45 | multi,contested |

Unflagged default accepts: 41, min P 0.986, max |z| 1.87
