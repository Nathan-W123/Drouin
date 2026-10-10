# blind4 seed 1 arm ai -- round 6

assigned peaks 215, floating params 18, last rms (weighted) 0.799
predictions considered 713, with candidates 50, unresolvable windows 0, p_have=0.31 (from 782 sharp predictions)
candidate rows 50: default accept 4 (of which flagged 1), deferred with P>=0.5: 1

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 185 | 8 4 5 7 4 4;8 4 4 7 4 3 | -0.5218 | -4.6 | 0.00 | -0.14 | 2 | reject |
| 258 | 13 11 2 12 11 1;13 11 3 12 11 2 | -0.0067 | -1.4 | 0.81 | -0.06 | 4 | keep |
| 78 | 30 1 29 29 3 26 | +0.0097 | +1.2 | 0.86 | -0.07 | 5 | keep |
| 255 | 36 3 33 36 3 34 | +0.0023 | +0.1 | 0.86 | -0.24 | 4 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 1399 | LJJK | 8 | 6.9 | -1.365e-10 | 2.6 | 2.7 | hold |
| 2299 | LJK | 8 | 0.5 | -1.199e-09 | 0.7 | 0.37 | hold |
| 4099 | LK | 8 | 0.4 | -3.76e-06 | 0.6 | 2.5 | hold |
| 50299 | l2 | 8 | 0.3 | -1.187e-13 | 0.6 | 0.15 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|
| C0001 | 10 5 5 10 5 6 | 1 | +1.51 | -0.00 | 1.000 | blend | 22 7 15 22 7 16 |

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0005 | 22 7 15 22 7 16 | 1.94e-06 | 1 | +3.42 | +1.18 | 0.974 | 0.00 | 0.00 | blend,intensity,far |

Unflagged default accepts: 3, min P 1.000, max |z| 0.01
