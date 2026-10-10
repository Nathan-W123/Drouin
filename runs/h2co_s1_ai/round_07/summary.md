# h2co seed 1 arm ai -- round 7

assigned peaks 192, floating params 15, last rms (weighted) 1.009
predictions considered 357, with candidates 52, unresolvable windows 0, p_have=0.48 (from 428 sharp predictions)
candidate rows 53: default accept 2 (of which flagged 2), deferred with P>=0.5: 1

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 278 | 36 3 33 36 3 34 | +0.6679 | +6.5 | 0.48 | +0.09 | 6 | reject |
| 63 | 40 6 34 40 6 35 | +0.0219 | +3.7 | 0.29 | +0.08 | 4 | keep |
| 33 | 22 5 17 22 5 18 | +0.0014 | +3.6 | 0.16 | +0.03 | 4 | keep |
| 67 | 41 6 35 41 6 36 | -0.0159 | -3.1 | 0.47 | +0.03 | 4 | keep |
| 61 | 31 1 30 30 3 27 | +0.0134 | +4.8 | 0.96 | +0.15 | 6 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 60199 | l3 | 8 | 82.2 | -5.183e-13 | 9.1 | 0.46 | release |
| 50299 | l2 | 8 | 38.0 | -8.69e-13 | 6.2 | 0.77 | hold |
| 2299 | LJK | 8 | 36.4 | 1.391e-08 | 6.0 | 3.1 | hold |
| 399 | HJ | 6 | 35.0 | 1.077e-08 | 5.9 | 0.014 | hold |
| 4099 | LK | 8 | 5.4 | 1.018e-05 | 2.4 | 5.1 | hold |
| 3199 | LKKJ | 8 | 0.2 | -1.535e-09 | 0.4 | 0.011 | hold |
| 1399 | LJJK | 8 | 0.1 | 1.792e-11 | 0.3 | 0.25 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|
| C0001 | 13 11 2 12 11 1 | 281 | -0.01 | +0.57 | 0.998 | blend | 13 11 3 12 11 2 |
| C0002 | 13 11 3 12 11 2 | 281 | -0.01 | +0.57 | 0.998 | blend | 13 11 2 12 11 1 |

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0003 | 32 2 30 31 4 27 | 160 | 70 | +0.00 | -0.11 | 0.896 | 0.10 | 0.00 | multi |
