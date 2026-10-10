# blind2 seed 1 arm ai -- round 5

assigned peaks 97, floating params 14, last rms (weighted) 0.780
predictions considered 418, with candidates 136, unresolvable windows 0, p_have=0.43 (from 364 sharp predictions)
candidate rows 137: default accept 58 (of which flagged 2), deferred with P>=0.5: 9

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 75 | 24 4 20 24 4 21 | +0.0038 | +1.1 | 0.86 | +0.05 | 4 | keep |
| 117 | 20 3 17 21 1 20 | +0.0001 | +0.2 | 1.00 | -0.12 | 4 | keep |
| 209 | 14 3 11 15 1 14 | +0.0139 | +0.2 | 0.94 | -0.03 | 4 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 3099 | HK | 6 | 3.2 | 0.007682 | 1.8 | 0.32 | hold |
| 50299 | l2 | 8 | 1.6 | 5.149e-12 | 1.3 | 0.81 | hold |
| 60199 | l3 | 8 | 1.3 | 1.016e-12 | 1.1 | 0.16 | hold |
| 2299 | LJK | 8 | 0.9 | -8.025e-08 | 1.0 | 10 | hold |
| 399 | HJ | 6 | 0.9 | -8.129e-08 | 0.9 | 0.03 | hold |
| 1399 | LJJK | 8 | 0.3 | -1.931e-09 | 0.6 | 8.7 | hold |
| 4099 | LK | 8 | 0.0 | 4.484e-05 | 0.3 | 23 | hold |
| 3199 | LKKJ | 8 | -0.0 | -2.885e-08 | 0.2 | 0.2 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|
| C0022 | 8 6 2 7 6 1 | 197 | +0.11 | -0.13 | 1.000 | blend | 8 6 3 7 6 2 |
| C0023 | 8 6 3 7 6 2 | 197 | +0.11 | -0.13 | 1.000 | blend | 8 6 2 7 6 1 |

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0021 | 23 3 20 24 1 23 | 0.277 | 77 | -0.02 | -0.08 | 1.000 | 0.00 | 0.95 | contested |
| C0050 | 36 5 31 36 5 32 | 11.7 | 88 | -0.00 | +0.06 | 0.998 | 0.00 | 0.43 | contested |
| C0061 | 25 1 24 24 3 21 | 158 | 77 | -1.46 | +0.04 | 0.955 | 0.00 | 1.00 | contested |
| C0062 | 32 2 30 31 4 27 | 549 | 71 | -0.01 | +0.13 | 0.920 | 0.00 | 0.00 |  |
| C0063 | 31 1 30 30 3 27 | 460 | 62 | -0.00 | -0.09 | 0.887 | 0.00 | 0.00 |  |
| C0064 | 48 3 45 47 5 42 | 4.11e+03 | 186 | +1.13 | +0.08 | 0.732 | 0.00 | 0.00 |  |
| C0065 | 44 3 41 43 5 38 | 2.68e+03 | 145 | +2.01 | +0.29 | 0.700 | 0.00 | 0.00 |  |
| C0066 | 34 2 32 33 4 29 | 737 | 108 | +1.89 | +0.49 | 0.679 | 0.00 | 0.00 |  |
| C0067 | 30 1 29 29 3 26 | 390 | 89 | -0.00 | +0.09 | 0.546 | 0.43 | 0.00 | multi |

Unflagged default accepts: 56, min P 0.984, max |z| 1.86
