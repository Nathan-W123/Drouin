#!/usr/bin/env bash
# Re-run SPFIT on the official CDMS SO2.par/SO2.lin and compare with the official SO2.fit.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RUN="$ROOT/runs/sanity_SO2"; rm -rf "$RUN"; mkdir -p "$RUN"; cd "$RUN"
cp "$ROOT/data/SO2/SO2.par" "$ROOT/data/SO2/SO2.lin" .
"$ROOT/external/pickett_src/Pickett/spfit" SO2 > spfit.log 2>&1
echo "== RMS (ours, then official)"; grep "END OF ITERATION" SO2.fit | tail -1; grep "END OF ITERATION" "$ROOT/data/SO2/SO2.fit" | tail -1
echo "== line listing (obs, calc, obs-calc) differences:"
diff <(grep -E '^\s+[0-9]+:' SO2.fit) <(grep -E '^\s+[0-9]+:' "$ROOT/data/SO2/SO2.fit") || true
echo "== final parameter block (value(unc)) differences, whitespace/sign-of-zero ignored:"
blk() { awk '/NEW PARAMETER/{n=NR} {a[NR]=$0} END{for(i=n+1;i<n+60;i++) print a[i]}' "$1" | awk '{print $1,$2,$3,$4}'; }
diff <(blk SO2.fit) <(blk "$ROOT/data/SO2/SO2.fit") && echo "identical"
