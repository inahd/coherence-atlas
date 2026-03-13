#!/usr/bin/env bash
set -euo pipefail
python3 /opt/atlas/scripts/generate_seed_prompts.py >/dev/null
cat /opt/atlas/prompts/seed_prompts.md
