#!/usr/bin/env bash
set -euo pipefail
python3 /opt/atlas/scripts/dashboard.py
python3 - <<'PY'
import webbrowser
from pathlib import Path
p = Path("/opt/atlas/memory/reports/dashboard.html")
webbrowser.open("file://" + str(p))
print("Opened:", p)
PY
