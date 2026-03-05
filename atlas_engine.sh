#!/usr/bin/env bash

BASE="/opt/atlas"

echo
echo "=== COHERENCE ATLAS ENGINE ==="
echo

# ensure directories exist
mkdir -p $BASE/panchanga
mkdir -p $BASE/datasets
mkdir -p $BASE/journals
mkdir -p $BASE/graph

echo "Directories verified."

# compute today's panchanga
if [ -f "$BASE/scripts/panchanga.py" ]; then
    echo "Computing Panchanga..."
    python $BASE/scripts/panchanga.py
fi

# list datasets
echo
echo "Datasets installed:"
ls $BASE/datasets 2>/dev/null

echo
echo "Atlas system ready."
echo
echo "Useful commands:"
echo "atlas today"
echo "atlas journal"
echo "atlas search <term>"

echo
