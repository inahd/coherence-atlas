#!/usr/bin/env bash
set -euo pipefail
python3 /opt/atlas/scripts/generate_seed_prompts.py >/dev/null
cd /opt/atlas
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "Not a git repo"; exit 1; }
git add prompts/seed_prompts.md
git commit -m "Update seed prompts (auto)" || true
git push || true
echo "[DONE] pushed prompts/seed_prompts.md"
