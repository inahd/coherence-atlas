#!/usr/bin/env bash

echo "----- Atlas Cycle -----"

echo "1️⃣ Harvest prompts → seeds"
python3 scripts/prompts_to_seeds.py || true

echo "2️⃣ Seeds → cards"
python3 scripts/seed_to_cards.py || true

echo "3️⃣ Update reports"
python3 scripts/control_panel.py || true

echo "4️⃣ Commit cycle state"

git add .

git commit -m "atlas growth cycle $(date)" || true

echo "5️⃣ Sync with remote"

git pull --rebase origin main || true

git push origin main || true

echo "✨ Atlas cycle complete"
