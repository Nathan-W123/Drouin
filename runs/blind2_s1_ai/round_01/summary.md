# blind2 seed 1 arm ai -- round 1: BOOTSTRAP

Anchor lines (best-predicted, strong) and their number of intensity-consistent candidate peaks:
- 4 3 1 4 3 2: 4 candidates (peaks [10, 13, 14, 15])
- 9 4 5 9 4 6: 6 candidates (peaks [8, 10, 12, 13, 14, 15])
- 15 5 10 15 5 11: 6 candidates (peaks [8, 10, 12, 14, 15, 16])
- 16 5 11 16 5 12: 6 candidates (peaks [8, 10, 12, 13, 14, 15])
- 10 4 6 10 4 7: 7 candidates (peaks [10, 12, 13, 14, 15, 19, 21])
- 5 3 2 5 3 3: 4 candidates (peaks [13, 19, 20, 21])
- 17 5 12 17 5 13: 7 candidates (peaks [10, 12, 13, 14, 15, 19, 21])
- 11 4 7 11 4 8: 7 candidates (peaks [13, 14, 15, 19, 21, 22, 23])

| rank | Z | matched/scored | chance | support | anchors | default |
|---|---|---|---|---|---|---|
| 1 | 18.7 | 22/29 | 1.3 | 5 | 4 3 1 4 3 2->14;9 4 5 9 4 6->12;5 3 2 5 3 3->19 | accept |
| 2 | 17.3 | 21/29 | 1.4 | 268 | 9 4 5 9 4 6->15;5 3 2 5 3 3->20;11 4 7 11 4 8->21 | reject |
| 3 | 14.6 | 18/26 | 1.4 | 3 | 9 4 5 9 4 6->10;10 4 6 10 4 7->21;11 4 7 11 4 8->22 | reject |
| 4 | 14.2 | 17/29 | 1.3 | 2 | 4 3 1 4 3 2->15;5 3 2 5 3 3->19;11 4 7 11 4 8->13 | reject |
| 5 | 14.2 | 17/29 | 1.3 | 1 | 4 3 1 4 3 2->15;10 4 6 10 4 7->10;5 3 2 5 3 3->19 | reject |
| 6 | 12.0 | 15/29 | 1.4 | 1 | 9 4 5 9 4 6->14;10 4 6 10 4 7->21;5 3 2 5 3 3->13 | reject |
