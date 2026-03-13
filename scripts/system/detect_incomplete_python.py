#!/usr/bin/env python3

import ast
import os
from pathlib import Path

ROOT = Path("/opt/atlas")

broken = []

for path in ROOT.rglob("*.py"):
    try:
        src = path.read_text()
        ast.parse(src)
    except Exception as e:
        broken.append((path, str(e)))

print()
print("=== PYTHON FILE INTEGRITY SCAN ===")
print()

if not broken:
    print("All python files parsed successfully.")
else:
    for p,e in broken:
        print("BROKEN:",p)
        print("ERROR :",e)
        print()

    print("Total broken:",len(broken))

print()
