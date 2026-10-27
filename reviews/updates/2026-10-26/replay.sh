#!/bin/sh
# Rebuild data/map.json for v3 from the last release (a1b264d) by replaying the scripted edits in order.
# update2.py runs update1.py itself. Run from the repository root.
set -e
D=reviews/updates/2026-10-26
git checkout a1b264de50e5426a7b6c589085a7801e7572d4b0 -- data/map.json
for u in update2 update3 update4 update5 update6 update7; do python3 -I "$D/$u.py" data/map.json; done
