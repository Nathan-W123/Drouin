#!/usr/bin/env bash
# Download SPFIT/SPCAT source, CDMS ground-truth files and docs; build the binaries.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CDMS=https://cdms.astro.uni-koeln.de/classic/predictions/daten
mkdir -p "$ROOT/external" "$ROOT/data/SO2" "$ROOT/data/H2CO" "$ROOT/docs"

cd "$ROOT/external"
[ -f Pickett.zip ] || curl -sSfL -o Pickett.zip https://spin.astro.uni-koeln.de/chapter/Prerequisites/files/Pickett.zip
rm -rf pickett_src && mkdir pickett_src && (cd pickett_src && unzip -q ../Pickett.zip && rm -rf __MACOSX)
(cd pickett_src/Pickett && make spfit spcat >/dev/null 2>&1)

for f in SO2.par SO2.lin SO2.int SO2.fit SO2.red SO2v.int c064502i.cat c064503i.cat; do
  [ -f "$ROOT/data/SO2/$f" ] || curl -sSfL -o "$ROOT/data/SO2/$f" "$CDMS/SO2/SO2/$f"
done
for f in alle.par alle.lin alle.fit H2CO.int H2CO.var c030501.cat; do
  [ -f "$ROOT/data/H2CO/$f" ] || curl -sSfL -o "$ROOT/data/H2CO/$f" "$CDMS/H2CO/H2CO/$f"
done
[ -f "$ROOT/docs/spinv.pdf" ] || curl -sSfL -o "$ROOT/docs/spinv.pdf" https://spec.jpl.nasa.gov/ftp/pub/calpgm/spinv.pdf
[ -f "$ROOT/docs/crib.htm" ] || curl -sSfL -o "$ROOT/docs/crib.htm" http://info.ifpan.edu.pl/~kisiel/asym/pickett/crib.htm

echo "export PYCKETT_SPFIT_PATH=$ROOT/external/pickett_src/Pickett/spfit"
echo "export PYCKETT_SPCAT_PATH=$ROOT/external/pickett_src/Pickett/spcat"
