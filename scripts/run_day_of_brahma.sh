#!/usr/bin/env bash
set -e
source /opt/atlas/venv/bin/activate
cd /opt/atlas || exit 1
python scripts/atlas_cycle_runner.py
