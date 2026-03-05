#!/usr/bin/env bash
set -euo pipefail
python3 /opt/atlas/scripts/layered_relations_build.py
# temporarily point the viewer at layered_graph.json by copying into the expected canonical path
cp /opt/atlas/memory/graphs/layered_graph.json /opt/atlas/memory/graphs/canonical_graph.json
atlas graph canonical
