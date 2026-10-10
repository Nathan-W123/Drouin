#!/usr/bin/env bash
# Standard review of an AI-arm round: summary header, outliers, release trials, joint-consistency tests.
# Usage: scripts/round_review.sh <case> <seed> <round> [release-ids]
c=$1; s=$2; n=$(printf %02d $3); rel=${4:-}
R=runs/${c}_s${s}_ai/round_$n
sed -n 3,6p $R/summary.md
grep -A10 "## Outliers" $R/summary.md | head -10
grep -A8 "## Parameter release" $R/summary.md | head -8
echo "joint [defaults] release[$rel]: $(python3 -m assign.whatif $c $s ai --add-round $R --add-defaults --release "$rel" --worst 3 | grep -E 'lines|worst' | tr '\n' ' ' | cut -c1-330)"
python3 -m assign.whatif $c $s ai --add-round $R --add-defaults --add-p 0.5 --release "$rel" --prune 4 > $R/prune_p0.5.txt
echo "pruned [defaults + P>=0.5] release[$rel]: $(head -1 $R/prune_p0.5.txt)"
grep "removed" $R/prune_p0.5.txt | head -12
