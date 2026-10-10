# blind8 seed 1 arm ai -- round 8

assigned peaks 441, floating params 26, last rms (weighted) 0.945
predictions considered 2316, with candidates 15, unresolvable windows 0, p_have=0.16 (from 2754 sharp predictions)
candidate rows 15: default accept 4 (of which flagged 0), deferred with P>=0.5: 10

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 540 | 20 11 9 21 10 12 | +0.2560 | +3.6 | 0.03 | -0.08 | 4 | keep |
| 151 | 38 6 32 37 7 31 | -0.0093 | -3.5 | 0.15 | -0.17 | 4 | keep |
| 585 | 92 11 81 92 10 82 | +0.3039 | +3.5 | 0.43 | +0.21 | 5 | keep |
| 22 | 24 4 20 23 5 19 | +0.0022 | +3.2 | 0.36 | -0.24 | 3 | keep |
| 29 | 8 1 7 7 2 6 | -0.0015 | -3.0 | 0.30 | +0.13 | 2 | keep |
| 28 | 49 4 46 48 5 43 | -0.0002 | -0.7 | 0.85 | +0.19 | 5 | keep |
| 27 | 42 9 33 43 8 36 | +0.0000 | +0.4 | 0.87 | +0.10 | 4 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 2300 | PJJK | 10 | 46.1 | 2.228e-15 | 6.8 | 49 | release |
| 5100 | SKKKJ | 12 | 19.1 | -2.125e-16 | 4.4 | 1.1e+02 | hold |
| 6000 | SK | 12 | 14.4 | -1.715e-15 | 3.8 | 37 | hold |
| 3200 | PKKJ | 10 | 5.0 | 1.511e-14 | 2.2 | 5 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 48 10 38 49 9 41 | 0.00728 | 3 | +0.01 | +0.01 | 1.000 | 0.00 | 0.00 | prev-rejected |
| C0002 | 37 8 30 38 7 31 | 0.000819 | 17 | -0.99 | -0.13 | 1.000 | 0.00 | 0.00 | prev-rejected |
| C0003 | 42 4 38 43 3 41 | 0.0027 | 172 | +0.59 | -0.12 | 1.000 | 0.00 | 0.00 | prev-rejected |
| C0004 | 61 11 51 60 12 48 | 0.0462 | 30 | -0.07 | +0.01 | 1.000 | 0.00 | 0.00 | prev-rejected |
| C0005 | 63 13 51 64 12 52 | 0.084 | 16 | +0.20 | -0.17 | 1.000 | 0.00 | 0.00 | prev-rejected |
| C0007 | 72 20 52 73 19 55 | 1.21 | 458 | -0.03 | -0.12 | 0.999 | 0.00 | 0.00 | prev-rejected |
| C0009 | 30 16 14 31 15 17 | 0.048 | 699 | -1.84 | +0.26 | 0.999 | 0.00 | 0.00 | prev-rejected |
| C0012 | 51 8 44 52 5 47 | 0.0174 | 472 | +2.98 | +0.14 | 0.998 | 0.00 | 0.00 | prev-rejected |
| C0013 | 75 23 53 76 22 54 | 2.86 | 596 | -0.03 | +0.23 | 0.997 | 0.00 | 0.00 | prev-rejected |
| C0014 | 70 22 48 71 21 51 | 1.72 | 600 | +0.17 | +0.20 | 0.997 | 0.00 | 0.00 | prev-rejected |

Unflagged default accepts: 4, min P 0.998, max |z| 0.33
