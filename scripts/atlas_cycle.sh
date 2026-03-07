#!/usr/bin/env bash
set -e

cd /opt/atlas

echo
echo "=============================="
echo "ATLAS COSMOLOGY GROWTH CYCLE"
echo "=============================="
echo

echo "[1/7] expanding structure"
python3 scripts/expand_structure.py || true

echo "[2/7] generating research tasks"
python3 scripts/generate_research_tasks.py || true

echo "[3/7] generating heatmap"
python3 scripts/generate_knowledge_heatmap.py || true

echo "[4/7] exporting coherence metrics"
python3 scripts/export_coherence_metrics.py || true

echo "[5/7] inspecting graph"
python3 scripts/inspect_graph_structure.py || true

echo "[6/7] detecting clusters"
python3 scripts/detect_clusters.py || true

echo "[7/7] git commit + push"

git add ontology datasets research_queue scripts || true

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

echo ""
echo "[CANON] exporting atlas canonical state"

python3 scripts/export_atlas_canon.py

echo "[CANON] atlas_canon.md and atlas_state.json updated"


echo ""
echo "[GRAPH CHECK] validating graph integrity"
python3 scripts/ensure_graph_integrity.py


echo ""
echo "[PATTERN ENGINE] scanning graph structure"
python3 scripts/atlas_pattern_engine.py

