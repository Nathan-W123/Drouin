# blind12 seed 1 arm ai -- round 1: BOOTSTRAP

Anchor lines (best-predicted, strong) and their number of intensity-consistent candidate peaks:
- 8 4 4 8 4 5: 3 candidates (peaks [7, 11, 13])
- 4 3 1 4 3 2: 3 candidates (peaks [15, 16, 17])
- 14 5 9 14 5 10: 6 candidates (peaks [7, 11, 13, 16, 17, 18])
- 9 4 5 9 4 6: 7 candidates (peaks [7, 11, 13, 15, 16, 17, 21])
- 15 5 10 15 5 11: 7 candidates (peaks [7, 11, 13, 15, 16, 17, 21])
- 5 3 2 5 3 3: 4 candidates (peaks [15, 21, 22, 24])
- 10 4 6 10 4 7: 6 candidates (peaks [15, 16, 17, 21, 23, 24])
- 16 5 11 16 5 12: 7 candidates (peaks [11, 13, 15, 16, 17, 21, 23])

| rank | Z | matched/scored | chance | support | anchors | default |
|---|---|---|---|---|---|---|
| 1 | 19.9 | 26/34 | 1.6 | 233 | 4 3 1 4 3 2->15;9 4 5 9 4 6->15;5 3 2 5 3 3->22 | accept |
| 2 | 19.8 | 25/33 | 1.5 | 17 | 8 4 4 8 4 5->7;14 5 9 14 5 10->7;5 3 2 5 3 3->22 | reject |
| 3 | 19.8 | 25/33 | 1.5 | 28 | 8 4 4 8 4 5->13;14 5 9 14 5 10->11;5 3 2 5 3 3->22 | reject |
| 4 | 8.4 | 12/34 | 1.6 | 1 | 8 4 4 8 4 5->13;4 3 1 4 3 2->15;5 3 2 5 3 3->21 | reject |
| 5 | 8.1 | 11/31 | 1.5 | 1 | 8 4 4 8 4 5->7;4 3 1 4 3 2->15;10 4 6 10 4 7->17 | reject |
