# blind1 seed 1 arm ai -- round 8

assigned peaks 465, floating params 26, last rms (weighted) 0.919
predictions considered 2303, with candidates 20, unresolvable windows 0, p_have=0.17 (from 2664 sharp predictions)
candidate rows 20: default accept 0 (of which flagged 0), deferred with P>=0.5: 1

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 16 | 63 13 51 64 12 52 | +0.0043 | +5.1 | 0.67 | +0.08 | 4 | reject |
| 1 | 60 11 49 59 12 48 | +0.0016 | +3.9 | 0.50 | +0.06 | 4 | keep |
| 712 | 30 16 14 31 15 17 | -0.2833 | -3.1 | 0.16 | +0.07 | 5 | keep |
| 29 | 49 4 46 48 5 43 | -0.0004 | -1.1 | 0.83 | +0.16 | 6 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 2300 | PJJK | 10 | 41.3 | 1.424e-15 | 6.4 | 18 | release |
| 5100 | SKKKJ | 12 | 20.5 | -4.662e-16 | 4.5 | 56 | hold |
| 1300 | LJJK | 8 | 0.8 | -5.894e-14 | 0.9 | 0.036 | hold |
| 41299 | lJK | 8 | 0.8 | -3.374e-14 | 0.8 | 0.02 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 63 9 55 62 10 52 | 1.3 | 324 | -1.80 | -0.84 | 0.821 | 0.00 | 0.00 | intensity |
