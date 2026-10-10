# blind12 seed 1 arm ai -- round 4

assigned peaks 111, floating params 15, last rms (weighted) 0.768
predictions considered 439, with candidates 149, unresolvable windows 2, p_have=0.46 (from 366 sharp predictions)
candidate rows 152: default accept 49 (of which flagged 0), deferred with P>=0.5: 8

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 212 | 9 8 1 8 8 0;9 8 2 8 8 1 | -0.0534 | -1.7 | 0.86 | -0.66 | 3 | keep |
| 149 | 27 4 23 28 2 26 | -0.0052 | -0.3 | 0.90 | +0.13 | 3 | keep |
| 172 | 26 4 22 27 2 25 | +0.0048 | +0.3 | 0.90 | -0.07 | 3 | keep |
| 122 | 20 3 17 21 1 20 | -0.0013 | -0.5 | 0.98 | +0.13 | 3 | keep |
| 90 | 26 1 25 25 3 22 | -0.0029 | -0.5 | 0.97 | +0.08 | 3 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 3199 | LKKJ | 8 | 3.3 | -2.57e-07 | 1.8 | 3.9 | hold |
| 50299 | l2 | 8 | 0.5 | -1.486e-12 | 0.8 | 0.33 | hold |
| 2299 | LJK | 8 | 0.1 | -8.635e-09 | 0.3 | 2.6 | hold |
| 60199 | l3 | 8 | 0.1 | -2.097e-13 | 0.3 | 0.047 | hold |
| 1399 | LJJK | 8 | 0.1 | 1.268e-10 | 0.3 | 1 | hold |
| 399 | HJ | 6 | 0.1 | -3.194e-09 | 0.3 | 0.0015 | hold |
| 4099 | LK | 8 | -0.1 | 3.38e-06 | 0.1 | 5 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0042 | 36 5 31 36 5 32 | 9.54 | 85 | -0.04 | +0.03 | 0.999 | 0.00 | 0.46 | contested |
| C0051 | 32 2 30 31 4 27 | 424 | 68 | +0.00 | -0.16 | 0.931 | 0.00 | 0.00 |  |
| C0052 | 46 2 44 45 4 41 | 2.6e+03 | 82 | +0.64 | +0.24 | 0.916 | 0.00 | 0.00 |  |
| C0053 | 31 1 30 30 3 27 | 361 | 60 | +0.00 | +0.22 | 0.916 | 0.00 | 0.00 |  |
| C0054 | 23 3 20 24 1 23 | 101 | 75 | +0.00 | -0.15 | 0.884 | 0.10 | 0.17 | multi,contested |
| C0055 | 25 1 24 24 3 21 | 123 | 76 | +0.00 | +0.05 | 0.814 | 0.17 | 0.10 | multi,contested |
| C0056 | 45 2 43 44 4 40 | 2.33e+03 | 107 | -1.49 | +0.09 | 0.728 | 0.00 | 0.00 |  |
| C0057 | 30 1 29 29 3 26 | 307 | 86 | +0.00 | +0.13 | 0.527 | 0.46 | 0.00 | multi |

Unflagged default accepts: 49, min P 0.997, max |z| 2.07
