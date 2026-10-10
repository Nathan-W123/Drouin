# so2 seed 4 arm ai -- round 12

assigned peaks 432, floating params 26, last rms (weighted) 0.896
predictions considered 2022, with candidates 5, unresolvable windows 0, p_have=0.18 (from 2451 sharp predictions)
candidate rows 5: default accept 1 (of which flagged 0), deferred with P>=0.5: 1

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 471 | 51 8 44 52 5 47 | +0.0329 | +3.4 | 0.53 | -0.13 | 10 | keep |
| 331 | 49 6 44 48 7 41 | -0.4282 | -3.4 | 0.00 | -0.06 | 6 | keep |
| 33 | 61 11 51 60 12 48 | -0.0006 | -2.1 | 0.90 | -0.08 | 5 | keep |
| 30 | 49 4 46 48 5 43 | +0.0004 | +1.5 | 0.92 | +0.14 | 7 | keep |
| 493 | 70 5 65 71 4 68 | -0.0161 | -18.1 | 1.00 | -0.14 | 10 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 2300 | PJJK | 10 | 51.3 | 1.781e-15 | 7.2 | 10 | release |
| 6000 | SK | 12 | 10.9 | -1.429e-15 | 3.3 | 6.2 | hold |
| 5100 | SKKKJ | 12 | 10.8 | -1.634e-16 | 3.3 | 16 | hold |
| 3200 | PKKJ | 10 | 3.8 | 7.384e-15 | 1.9 | 0.64 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 79 7 73 80 4 76 | 0.194 | 488 | +0.07 | -0.02 | 1.000 | 0.00 | 0.18 | contested |

Unflagged default accepts: 1, min P 0.999, max |z| 0.15
