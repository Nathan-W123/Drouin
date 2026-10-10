# blind1 seed 1 arm ai -- round 7

assigned peaks 449, floating params 26, last rms (weighted) 0.907
predictions considered 2319, with candidates 36, unresolvable windows 0, p_have=0.17 (from 2664 sharp predictions)
candidate rows 37: default accept 15 (of which flagged 0), deferred with P>=0.5: 2

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 16 | 63 13 51 64 12 52 | +0.0033 | +4.7 | 0.76 | +0.08 | 4 | reject |
| 1 | 60 11 49 59 12 48 | +0.0014 | +3.6 | 0.52 | +0.06 | 4 | keep |
| 712 | 30 16 14 31 15 17 | -0.3082 | -3.4 | 0.19 | +0.07 | 5 | keep |
| 673 | 43 18 26 44 17 27 | -0.4438 | -3.4 | 0.16 | +0.05 | 6 | keep |
| 29 | 49 4 46 48 5 43 | -0.0003 | -1.0 | 0.83 | +0.16 | 6 | keep |
| 602 | 65 21 45 66 20 46 | +0.0037 | +1.6 | 0.97 | +0.10 | 6 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 2300 | PJJK | 10 | 40.8 | 1.516e-15 | 6.4 | 19 | release |
| 5100 | SKKKJ | 12 | 36.8 | -9.799e-16 | 6.1 | 1.2e+02 | hold |
| 41299 | lJK | 8 | 1.3 | -4.742e-14 | 1.1 | 0.029 | hold |
| 1300 | LJJK | 8 | 1.2 | -7.599e-14 | 1.1 | 0.046 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0016 | 74 9 65 74 8 66 | 6.09 | 495 | +0.00 | -0.11 | 0.948 | 0.05 | 0.00 |  |
| C0017 | 63 9 55 62 10 52 | 1.3 | 324 | -1.80 | -0.84 | 0.821 | 0.00 | 0.00 | intensity |

Unflagged default accepts: 15, min P 0.994, max |z| 0.12
