# blind8 seed 1 arm ai -- round 6

assigned peaks 427, floating params 25, last rms (weighted) 0.992
predictions considered 2330, with candidates 33, unresolvable windows 0, p_have=0.16 (from 2741 sharp predictions)
candidate rows 33: default accept 27 (of which flagged 0), deferred with P>=0.5: 1

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 151 | 38 6 32 37 7 31 | -0.0117 | -4.3 | 0.12 | -0.17 | 4 | reject |
| 459 | 62 18 44 63 17 47 | +0.1065 | +4.2 | 0.21 | -0.01 | 5 | keep |
| 431 | 64 18 46 65 17 49 | -0.1018 | -4.0 | 0.22 | +0.06 | 5 | keep |
| 30 | 61 11 51 60 12 48 | -0.0021 | -3.8 | 0.59 | +0.01 | 4 | keep |
| 472 | 51 8 44 52 5 47 | +0.0359 | +3.7 | 0.55 | +0.14 | 5 | keep |
| 540 | 20 11 9 21 10 12 | +0.2266 | +3.2 | 0.02 | -0.08 | 4 | keep |
| 28 | 49 4 46 48 5 43 | -0.0003 | -0.8 | 0.84 | +0.19 | 5 | keep |
| 516 | 78 22 56 79 21 59 | -0.0211 | -0.6 | 0.94 | +0.07 | 5 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 4100 | PKKKJ | 10 | 46.2 | -4.988e-13 | 6.8 | 9.4 | release |
| 3200 | PKKJ | 10 | 27.2 | -1.606e-14 | 5.2 | 5.3 | hold |
| 5100 | SKKKJ | 12 | 24.3 | -3.897e-16 | 4.9 | 2e+02 | hold |
| 2300 | PJJK | 10 | 4.7 | -4.15e-16 | 2.2 | 9.2 | hold |
| 6000 | SK | 12 | 0.1 | -1.857e-16 | 0.2 | 4 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0028 | 68 22 46 69 21 49 | 4.29 | 619 | +2.29 | +0.02 | 0.949 | 0.00 | 0.00 |  |

Unflagged default accepts: 27, min P 0.966, max |z| 2.31
