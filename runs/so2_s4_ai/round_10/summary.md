# so2 seed 4 arm ai -- round 10

assigned peaks 348, floating params 25, last rms (weighted) 0.834
predictions considered 2106, with candidates 106, unresolvable windows 0, p_have=0.18 (from 2377 sharp predictions)
candidate rows 107: default accept 81 (of which flagged 0), deferred with P>=0.5: 8

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 331 | 49 6 44 48 7 41 | -0.4045 | -3.2 | 0.00 | -0.06 | 6 | keep |
| 31 | 35 6 30 34 7 27 | +0.0002 | +1.9 | 0.83 | +0.10 | 5 | keep |
| 160 | 42 4 38 43 3 41 | -0.0009 | -0.8 | 0.84 | -0.06 | 6 | keep |
| 33 | 61 11 51 60 12 48 | -0.0004 | -2.7 | 0.97 | -0.08 | 5 | keep |
| 421 | 68 8 60 68 7 61 | -0.0005 | -0.1 | 0.97 | -0.12 | 6 | keep |
| 582 | 67 21 47 68 20 48 | +0.0005 | +0.3 | 1.00 | +0.16 | 6 | keep |
| 30 | 49 4 46 48 5 43 | -0.0001 | -1.4 | 1.00 | +0.14 | 7 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 42199 | lKJ | 8 | 8.9 | 7.799e-11 | 3.0 | 0.35 | hold |
| 2300 | PJJK | 10 | 8.5 | 1.996e-15 | 2.9 | 11 | hold |
| 3200 | PKKJ | 10 | 1.6 | 2.522e-14 | 1.3 | 2.2 | hold |
| 5100 | SKKKJ | 12 | 1.4 | -3.107e-16 | 1.2 | 31 | hold |
| 6000 | SK | 12 | 0.4 | -1.147e-15 | 0.6 | 4.9 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0059 | 79 7 73 80 4 76 | 16.8 | 488 | +0.08 | -0.02 | 0.993 | 0.00 | 0.22 | contested |
| C0083 | 92 9 83 92 8 84 | 42.7 | 602 | +0.19 | +0.24 | 0.928 | 0.00 | 0.00 |  |
| C0084 | 90 11 79 90 10 80 | 77.3 | 600 | -0.04 | -0.04 | 0.913 | 0.00 | 0.00 |  |
| C0085 | 90 11 79 89 12 78 | 62.7 | 591 | +0.04 | +0.35 | 0.909 | 0.00 | 0.83 | contested |
| C0086 | 92 11 81 92 10 82 | 81.9 | 584 | -0.03 | -0.24 | 0.893 | 0.07 | 0.00 | multi |
| C0087 | 47 18 30 48 17 31 | 1.23 | 621 | +1.65 | +0.77 | 0.886 | 0.00 | 0.00 | intensity |
| C0088 | 67 10 58 68 7 61 | 23.4 | 591 | +1.21 | -0.55 | 0.825 | 0.00 | 0.91 | contested |
| C0089 | 77 10 68 77 9 69 | 14.9 | 649 | -2.02 | -0.30 | 0.812 | 0.00 | 0.00 |  |

Unflagged default accepts: 81, min P 0.959, max |z| 1.81
