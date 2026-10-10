# blind6 seed 1 arm ai -- round 8

assigned peaks 304, floating params 25, last rms (weighted) 0.824
predictions considered 1833, with candidates 143, unresolvable windows 0, p_have=0.19 (from 1985 sharp predictions)
candidate rows 144: default accept 105 (of which flagged 0), deferred with P>=0.5: 5

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 606 | 51 3 49 52 0 52 | -0.0043 | -0.5 | 0.90 | -0.00 | 6 | keep |
| 4 | 48 10 38 49 9 41 | -0.0001 | -0.4 | 0.87 | -0.09 | 5 | keep |
| 31 | 35 6 30 34 7 27 | -0.0001 | -0.4 | 0.82 | +0.17 | 5 | keep |
| 490 | 51 8 44 52 5 47 | +0.0005 | +0.1 | 0.93 | +0.01 | 5 | keep |
| 629 | 79 6 74 80 3 77 | +0.0102 | +0.9 | 0.98 | +0.07 | 5 | keep |
| 21 | 63 13 51 64 12 52 | +0.0000 | +0.0 | 0.91 | +0.08 | 5 | keep |
| 33 | 61 11 51 60 12 48 | +0.0001 | +0.2 | 0.94 | +0.05 | 6 | keep |
| 462 | 47 15 33 48 14 34 | +0.0075 | +1.6 | 0.93 | +0.21 | 6 | keep |
| 434 | 70 8 62 70 7 63 | +0.0006 | +0.6 | 1.00 | +0.04 | 6 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 4100 | PKKKJ | 10 | 3.2 | -1.96e-12 | 1.8 | 15 | hold |
| 5100 | SKKKJ | 12 | 2.9 | -1.745e-15 | 1.7 | 2.8e+02 | hold |
| 2300 | PJJK | 10 | 2.3 | 3.446e-15 | 1.5 | 19 | hold |
| 6000 | SK | 12 | 0.9 | -1.253e-14 | 1.5 | 62 | hold |
| 1300 | LJJK | 8 | 0.0 | -8.875e-14 | 0.1 | 0.024 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0004 | 14 8 6 15 7 9 | 0.0143 | 429 | -1.06 | -0.05 | 1.000 | 0.00 | 0.60 | contested |
| C0020 | 52 3 49 53 2 52 | 0.714 | 515 | +0.01 | -0.03 | 0.999 | 0.00 | 0.34 | contested |
| C0054 | 79 7 73 80 4 76 | 6.28 | 506 | +0.13 | -0.06 | 0.997 | 0.00 | 0.27 | contested |
| C0109 | 74 9 65 74 8 66 | 13.5 | 514 | +0.04 | +0.22 | 0.651 | 0.34 | 0.00 | multi |
| C0110 | 54 7 47 54 6 48 | 1.53 | 429 | -3.28 | +0.56 | 0.602 | 0.00 | 1.00 | contested,far |

Unflagged default accepts: 105, min P 0.954, max |z| 1.31
