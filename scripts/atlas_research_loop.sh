#!/bin/bash

echo "==== ATLAS RESEARCH LOOP START ===="

echo "1. Detecting graph gaps"
python scripts/atlas_gap_detector.py

echo "2. Generating research tasks"
python scripts/generate_research_tasks.py

echo "3. Executing research"
python scripts/atlas_execute_research.py

echo "4. Deep research pass"
python scripts/deep_research_pass.py

echo "5. Rebuilding cosmology graph"
python scripts/rebuild_cosmology_graph.py

echo "6. Checking graph integrity"
python scripts/ensure_graph_integrity.py

echo "7. Computing coherence"
python scripts/atlas_compute_coherence.py

echo "8. Generating visualizations"
python scripts/nakshatra_cosmic_wheel.py
python scripts/build_cosmic_mandala.py

echo "==== ATLAS RESEARCH LOOP COMPLETE ===="
