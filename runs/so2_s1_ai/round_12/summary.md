# so2 seed 1 arm ai -- round 12

assigned peaks 375, floating params 25, last rms (weighted) 0.924
predictions considered 2079, with candidates 80, unresolvable windows 0, p_have=0.18 (from 2449 sharp predictions)
candidate rows 80: default accept 79 (of which flagged 0), deferred with P>=0.5: 0

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 29 | 35 6 30 34 7 27 | +0.0005 | +3.4 | 0.70 | -0.08 | 5 | keep |
| 89 | 52 9 43 51 10 42 | -0.4373 | -3.1 | 0.00 | +0.04 | 8 | keep |
| 422 | 70 8 62 70 7 63 | +0.0010 | +0.2 | 0.89 | +0.06 | 9 | keep |
| 31 | 61 11 51 60 12 48 | -0.0005 | -2.3 | 0.92 | +0.06 | 5 | keep |
| 621 | 64 21 43 65 20 46 | +0.0029 | +0.7 | 0.92 | +0.10 | 6 | keep |
| 28 | 49 4 46 48 5 43 | +0.0001 | +0.6 | 0.95 | +0.11 | 9 | keep |
| 512 | 90 10 80 90 9 81 | -0.0088 | -0.7 | 0.97 | +0.06 | 9 | keep |
| 495 | 66 8 58 65 9 57 | -0.0035 | -1.4 | 0.97 | +0.02 | 9 | keep |
| 586 | 51 3 49 52 0 52 | +0.0088 | +1.5 | 0.92 | +0.22 | 11 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 2300 | PJJK | 10 | 25.8 | 2.319e-15 | 5.1 | 52 | release |
| 3200 | PKKJ | 10 | 12.3 | 2.542e-14 | 3.5 | 8.4 | hold |
| 5100 | SKKKJ | 12 | 11.1 | -1.721e-16 | 3.3 | 86 | hold |
| 6000 | SK | 12 | 8.1 | -1.34e-15 | 2.8 | 30 | hold |
| 41299 | lJK | 8 | 1.4 | -2.073e-13 | 1.2 | 0.18 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|

Unflagged default accepts: 79, min P 0.987, max |z| 2.42
