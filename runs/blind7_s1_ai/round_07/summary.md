# blind7 seed 1 arm ai -- round 7

assigned peaks 71, floating params 15, last rms (weighted) 1.212
predictions considered 634, with candidates 100, unresolvable windows 0, p_have=0.15 (from 504 sharp predictions)
candidate rows 100: default accept 10 (of which flagged 0), deferred with P>=0.5: 1

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 28 | 20 5 15 20 5 16 | +0.0007 | +4.4 | 0.64 | -0.03 | 5 | reject |
| 39 | 15 4 11 15 4 12 | +0.0004 | +3.2 | 0.82 | -0.04 | 4 | keep |
| 215 | 16 1 15 16 1 16 | +0.0630 | +2.5 | 0.86 | +0.32 | 4 | keep |
| 267 | 13 1 13 12 1 12 | -0.0031 | -0.3 | 0.81 | +0.08 | 4 | keep |
| 193 | 5 2 3 6 0 6 | +0.0886 | +0.2 | 0.90 | -0.17 | 3 | keep |
| 32 | 21 5 16 21 5 17 | -0.0005 | -6.2 | 0.93 | -0.33 | 4 | keep |
| 122 | 20 3 17 21 1 20 | -0.0000 | -0.0 | 1.00 | -0.12 | 6 | keep |
| 61 | 45 4 41 46 2 44 | -0.0000 | -0.0 | 1.00 | +0.11 | 6 | keep |
| 276 | 13 11 2 12 11 1;13 11 3 12 11 2 | +0.0000 | +0.0 | 1.00 | +0.23 | 6 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 1399 | LJJK | 8 | 10.4 | 4.965e-08 | 4.0 | 9.2e+02 | release |
| 50299 | l2 | 8 | 3.5 | -1.807e-11 | 1.8 | 18 | hold |
| 2299 | LJK | 8 | 2.2 | 3.956e-07 | 1.5 | 1.4e+02 | hold |
| 60199 | l3 | 8 | 1.0 | -2.967e-12 | 1.0 | 3 | hold |
| 4099 | LK | 8 | 0.3 | 0.0004869 | 0.5 | 4.2e+02 | hold |
| 3199 | LKKJ | 8 | 0.1 | 1.365e-07 | 0.2 | 2.6 | hold |
| 3099 | HK | 6 | -0.1 | -0.0007698 | 0.0 | 0.05 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0011 | 13 3 10 13 3 11 | 0.0591 | 51 | -3.71 | +0.17 | 0.917 | 0.00 | 0.00 | far |

Unflagged default accepts: 10, min P 0.951, max |z| 2.92
