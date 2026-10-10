# blind6 seed 1 arm ai -- round 12

assigned peaks 412, floating params 26, last rms (weighted) 0.914
predictions considered 1725, with candidates 26, unresolvable windows 0, p_have=0.19 (from 2008 sharp predictions)
candidate rows 26: default accept 0 (of which flagged 0), deferred with P>=0.5: 2

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 21 | 63 13 51 64 12 52 | +0.0043 | +4.1 | 0.64 | +0.08 | 5 | reject |
| 2 | 60 11 49 59 12 48 | +0.0019 | +4.0 | 0.51 | -0.01 | 8 | keep |
| 656 | 63 21 43 64 20 44 | -0.0705 | -4.0 | 0.54 | +0.13 | 9 | keep |
| 4 | 48 10 38 49 9 41 | +0.0006 | +3.1 | 0.72 | -0.09 | 5 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 2300 | PJJK | 10 | 44.6 | 2.37e-15 | 6.7 | 13 | release |
| 5100 | SKKKJ | 12 | 20.9 | -2.452e-16 | 4.6 | 39 | hold |
| 6000 | SK | 12 | 9.8 | -1.483e-15 | 3.1 | 7.3 | hold |
| 1300 | LJJK | 8 | 2.4 | -3.323e-13 | 1.6 | 0.09 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 14 8 6 15 7 9 | 0.00471 | 429 | -0.77 | -0.05 | 1.000 | 0.00 | 0.61 | contested |
| C0002 | 54 7 47 54 6 48 | 1.53 | 429 | -3.27 | +0.56 | 0.613 | 0.00 | 1.00 | contested,far |
