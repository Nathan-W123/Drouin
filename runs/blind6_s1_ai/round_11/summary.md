# blind6 seed 1 arm ai -- round 11

assigned peaks 409, floating params 26, last rms (weighted) 0.911
predictions considered 1728, with candidates 29, unresolvable windows 0, p_have=0.19 (from 2008 sharp predictions)
candidate rows 29: default accept 3 (of which flagged 0), deferred with P>=0.5: 2

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 656 | 63 21 43 64 20 44 | -0.0714 | -4.0 | 0.54 | +0.13 | 9 | reject |
| 21 | 63 13 51 64 12 52 | +0.0039 | +3.8 | 0.65 | +0.08 | 5 | keep |
| 2 | 60 11 49 59 12 48 | +0.0018 | +3.8 | 0.52 | -0.01 | 8 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 2300 | PJJK | 10 | 42.5 | 2.347e-15 | 6.5 | 13 | release |
| 5100 | SKKKJ | 12 | 17.7 | -2.342e-16 | 4.2 | 38 | hold |
| 6000 | SK | 12 | 8.7 | -1.403e-15 | 3.0 | 6.9 | hold |
| 1300 | LJJK | 8 | 2.0 | -3.002e-13 | 1.4 | 0.081 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 14 8 6 15 7 9 | 0.00472 | 429 | -0.77 | -0.05 | 1.000 | 0.00 | 0.61 | contested |
| C0005 | 54 7 47 54 6 48 | 1.53 | 429 | -3.27 | +0.56 | 0.613 | 0.00 | 1.00 | contested,far |

Unflagged default accepts: 3, min P 0.999, max |z| 0.05
