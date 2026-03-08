#!/usr/bin/env bash

echo "=== ATLAS CYCLE ==="

python tools/offering_plate_interpreter.py > memory/reports/plate.txt
python tools/generate_offerings.py > memory/reports/generated.txt
python tools/rebuild_readme_top.py

git add -A
git commit -m "atlas: cycle turn" || true
git push || true

echo "=== CYCLE COMPLETE ==="
