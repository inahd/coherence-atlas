#!/usr/bin/env bash
set -e

cd /opt/atlas

echo
echo "=============================="
echo "ATLAS COSMOLOGY GROWTH CYCLE"
echo "=============================="
echo

echo "[1/8] expanding structure"
python3 scripts/expand_structure.py || true

echo "[2/8] generating research tasks"
python3 scripts/generate_research_tasks.py || true

echo "[3/8] generating heatmap"
python3 scripts/generate_knowledge_heatmap.py || true

echo "[4/8] exporting coherence metrics"
python3 scripts/export_coherence_metrics.py || true

echo "[5/8] inspecting graph"
python3 scripts/inspect_graph_structure.py || true

echo "[6/8] detecting clusters"
python3 scripts/detect_clusters.py || true

echo "[7/8] rebuilding atlas"
atlas pb || true

echo "[8/8] git commit + push"

git add \
  ontology/ \
  datasets/ \
  research_queue/ \
  memory/reports/ \
  memory/yantra/ \
  scripts/

if git diff --cached --quiet; then
    echo "No new changes to commit."
else
    git commit -m "atlas cycle: structure expansion, research tasks, metrics, clusters"
    git push
fi

echo
echo "=============================="
echo "ATLAS CYCLE COMPLETE"
echo "=============================="
echo
