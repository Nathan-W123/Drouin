# blind2 seed 1 arm ai -- round 8

assigned peaks 157, floating params 16, last rms (weighted) 0.816
predictions considered 357, with candidates 55, unresolvable windows 0, p_have=0.38 (from 405 sharp predictions)
candidate rows 55: default accept 1 (of which flagged 0), deferred with P>=0.5: 5

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 79 | 25 4 21 25 4 22 | +0.1068 | +3.1 | 0.01 | +0.28 | 5 | keep |
| 117 | 20 3 17 21 1 20 | +0.0040 | +0.6 | 0.84 | -0.12 | 4 | keep |
| 80 | 44 6 38 44 6 39 | -0.0025 | -1.3 | 0.95 | +0.11 | 5 | keep |
| 150 | 27 4 23 28 2 26 | +0.0015 | +0.2 | 0.98 | -0.08 | 5 | keep |
| 71 | 32 2 30 31 4 27 | +0.0054 | +0.3 | 0.94 | +0.13 | 5 | keep |
| 62 | 31 1 30 30 3 27 | -0.0068 | -1.3 | 0.91 | -0.09 | 6 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 50299 | l2 | 8 | 0.3 | -1.605e-13 | 0.6 | 0.025 | hold |
| 3199 | LKKJ | 8 | 0.1 | 4.544e-08 | 0.4 | 0.32 | hold |
| 4099 | LK | 8 | 0.1 | -8.836e-06 | 0.2 | 4.5 | hold |
| 1399 | LJJK | 8 | 0.1 | 2.482e-11 | 0.3 | 0.11 | hold |
| 399 | HJ | 6 | 0.1 | -1.882e-09 | 0.2 | 0.0007 | hold |
| 2299 | LJK | 8 | -0.0 | 1.922e-09 | 0.2 | 0.25 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0001 | 23 3 20 24 1 23 | 0.0226 | 77 | +1.00 | -0.08 | 1.000 | 0.00 | 0.97 | contested |
| C0003 | 25 1 24 24 3 21 | 157 | 77 | -1.47 | +0.04 | 0.972 | 0.00 | 1.00 | contested |
| C0004 | 48 3 45 47 5 42 | 4.09e+03 | 186 | +1.15 | +0.08 | 0.692 | 0.00 | 0.00 |  |
| C0005 | 44 3 41 43 5 38 | 2.65e+03 | 145 | +2.04 | +0.29 | 0.646 | 0.00 | 0.00 |  |
| C0006 | 34 2 32 33 4 29 | 729 | 108 | +1.92 | +0.49 | 0.627 | 0.00 | 0.00 |  |

Unflagged default accepts: 1, min P 1.000, max |z| 0.00
