# h2co seed 1 arm ai -- round 6

assigned peaks 166, floating params 14, last rms (weighted) 1.095
predictions considered 385, with candidates 124, unresolvable windows 0, p_have=0.51 (from 316 sharp predictions)
candidate rows 130: default accept 24 (of which flagged 0), deferred with P>=0.5: 10

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 182 | 30 3 27 30 3 28 | +0.9086 | +9.5 | 0.54 | -0.02 | 4 | reject |
| 67 | 41 6 35 41 6 36 | -0.0182 | -4.2 | 0.62 | +0.03 | 4 | keep |
| 63 | 40 6 34 40 6 35 | +0.0195 | +3.5 | 0.37 | +0.08 | 4 | keep |
| 227 | 24 2 22 24 2 23 | -0.4474 | -3.5 | 0.17 | +0.12 | 4 | keep |
| 35 | 15 4 11 15 4 12 | -0.0008 | -3.1 | 0.24 | +0.05 | 4 | keep |
| 291 | 20 1 19 20 1 20 | -0.0088 | -0.6 | 0.89 | -0.17 | 4 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 2199 | HKJ | 6 | 94.7 | 1.536e-05 | 9.8 | 0.01 | release |
| 60199 | l3 | 8 | 91.0 | -1.018e-12 | 9.5 | 0.9 | hold |
| 50299 | l2 | 8 | 87.8 | -2.285e-12 | 9.4 | 2 | hold |
| 2299 | LJK | 8 | 84.8 | 2.791e-08 | 9.2 | 6.3 | hold |
| 1399 | LJJK | 8 | 64.7 | 9.9e-10 | 8.0 | 14 | hold |
| 3199 | LKKJ | 8 | 24.2 | 2.499e-08 | 4.9 | 0.19 | hold |
| 399 | HJ | 6 | 0.2 | -2.633e-08 | 0.6 | 0.033 | hold |
| 4099 | LK | 8 | -0.1 | -2.245e-06 | 0.3 | 1.1 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0025 | 12 11 1 11 11 0 | 529 | 253 | +0.00 | +0.31 | 0.956 | 0.00 | 0.88 | contested,blend |
| C0026 | 12 11 2 11 11 1 | 529 | 253 | +0.00 | +0.31 | 0.956 | 0.00 | 0.88 | contested,blend |
| C0027 | 13 10 3 12 10 2 | 391 | 282 | +0.00 | +0.13 | 0.918 | 0.05 | 0.53 | contested,blend |
| C0028 | 13 10 4 12 10 3 | 391 | 282 | +0.00 | +0.13 | 0.918 | 0.05 | 0.53 | contested,blend |
| C0029 | 12 10 2 11 10 1 | 361 | 253 | -1.93 | +0.16 | 0.882 | 0.00 | 0.96 | contested,blend |
| C0030 | 12 10 3 11 10 2 | 361 | 253 | -1.93 | +0.16 | 0.882 | 0.00 | 0.96 | contested,blend |
| C0031 | 42 3 39 41 5 36 | 1.32e+03 | 114 | -1.59 | +0.39 | 0.824 | 0.00 | 0.00 |  |
| C0032 | 32 2 30 31 4 27 | 332 | 70 | -0.28 | -0.11 | 0.679 | 0.31 | 0.00 | multi |
| C0033 | 13 11 2 12 11 1 | 573 | 282 | +1.33 | +0.16 | 0.534 | 0.39 | 0.92 | multi,contested,blend |
| C0034 | 13 11 3 12 11 2 | 573 | 282 | +1.33 | +0.16 | 0.534 | 0.39 | 0.92 | multi,contested,blend |

Unflagged default accepts: 24, min P 0.973, max |z| 0.92
