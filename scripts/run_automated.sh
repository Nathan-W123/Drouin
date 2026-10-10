#!/usr/bin/env bash
# Run the automated arms (greedy, rules, rules+) for the given cases and seeds, 4 in parallel,
# then score them.  Usage: scripts/run_automated.sh "h2co so2" "1 2 3 4 5"
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
CASES=${1:-"h2co so2"}; SEEDS=${2:-"1 2 3 4 5"}
mkdir -p logs
jobs=()
for c in $CASES; do for s in $SEEDS; do
  [ -f "testcases/${c}_s$s/peaks.csv" ] || python3 -m assign.testcase "$c" --seed "$s" > /dev/null
  jobs+=("$c $s greedy" "$c $s rules" "$c $s rules_plus")
done; done
printf '%s\n' "${jobs[@]}" | xargs -P 4 -L 1 bash -c '
  c=$0; s=$1; arm=$2
  if [ "$arm" = rules_plus ]; then extra="--arm rules --tag _plus --plus"; else extra="--arm $arm"; fi
  python3 -m assign.engine "$c" --seed "$s" $extra --fresh > "logs/${c}_s${s}_${arm}.log" 2>&1
  echo "$c s$s $arm: $(tail -1 logs/${c}_s${s}_${arm}.log)"'
for c in $CASES; do for s in $SEEDS; do for d in runs/${c}_s${s}_greedy runs/${c}_s${s}_rules runs/${c}_s${s}_rules_plus; do
  python3 -m assign.score "$d" | head -1; done; done; done
