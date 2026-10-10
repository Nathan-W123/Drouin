# blind3 seed 1 arm ai -- round 10

assigned peaks 428, floating params 25, last rms (weighted) 0.957
predictions considered 1813, with candidates 9, unresolvable windows 0, p_have=0.19 (from 2174 sharp predictions)
candidate rows 9: default accept 1 (of which flagged 1), deferred with P>=0.5: 0

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 2 | 60 11 49 59 12 48 | +0.0019 | +4.0 | 0.52 | -0.14 | 4 | reject |
| 22 | 63 13 51 64 12 52 | +0.0034 | +3.7 | 0.69 | -0.00 | 4 | keep |
| 670 | 63 21 43 64 20 44 | -0.0721 | -3.6 | 0.35 | -0.06 | 8 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 5100 | SKKKJ | 12 | 30.1 | -2.965e-16 | 5.5 | 30 | release |
| 2300 | PJJK | 10 | 28.0 | 1.594e-15 | 5.3 | 19 | hold |
| 6000 | SK | 12 | 16.8 | -1.927e-15 | 4.1 | 9.6 | hold |
| 1300 | LJJK | 8 | 0.8 | -7.008e-14 | 0.8 | 0.041 | hold |
| 41299 | lJK | 8 | 0.1 | -7.72e-15 | 0.2 | 0.0045 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|
| C0001 | 66 22 44 67 21 47 | 683 | +0.20 | +0.85 | 0.960 | intensity |  |

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
