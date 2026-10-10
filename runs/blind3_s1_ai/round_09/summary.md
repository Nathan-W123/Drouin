# blind3 seed 1 arm ai -- round 9

assigned peaks 412, floating params 25, last rms (weighted) 0.961
predictions considered 1829, with candidates 25, unresolvable windows 0, p_have=0.19 (from 2174 sharp predictions)
candidate rows 26: default accept 16 (of which flagged 1), deferred with P>=0.5: 1

## Outliers / high leverage in last fit
| peak | keys | res MHz | t | h | dI | round | default |
|---|---|---|---|---|---|---|---|
| 2 | 60 11 49 59 12 48 | +0.0018 | +4.0 | 0.53 | -0.14 | 4 | keep |
| 22 | 63 13 51 64 12 52 | +0.0033 | +3.8 | 0.73 | -0.00 | 4 | keep |
| 670 | 63 21 43 64 20 44 | -0.0719 | -3.6 | 0.39 | -0.06 | 8 | keep |

## Parameter release trials
| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |
|---|---|---|---|---|---|---|---|
| 5100 | SKKKJ | 12 | 31.6 | -3.351e-16 | 5.6 | 34 | release |
| 2300 | PJJK | 10 | 28.8 | 1.861e-15 | 5.4 | 22 | hold |
| 6000 | SK | 12 | 17.5 | -2.122e-15 | 4.2 | 11 | hold |
| 1300 | LJJK | 8 | 1.9 | -1.273e-13 | 1.4 | 0.074 | hold |
| 41299 | lJK | 8 | 0.4 | -3.426e-14 | 0.6 | 0.02 | hold |

## Default-accepted candidates carrying flags
| cid | key | peak | z | dI | P | flags | blend |
|---|---|---|---|---|---|---|---|
| C0016 | 66 22 44 67 21 47 | 683 | +0.21 | +0.85 | 0.960 | intensity |  |

## Deferred candidates with P >= 0.5
| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |
|---|---|---|---|---|---|---|---|---|---|
| C0017 | 63 10 54 62 11 51 | 1.34 | 241 | +0.19 | +1.08 | 0.647 | 0.00 | 0.00 | intensity |

Unflagged default accepts: 15, min P 0.961, max |z| 0.31
