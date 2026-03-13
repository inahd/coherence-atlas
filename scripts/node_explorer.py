import csv
import sys
from pathlib import Path

DATA = Path("/opt/atlas/data")

nodes_file = DATA / "nodes.csv"
relations_file = DATA / "relations.csv"

if len(sys.argv) < 2:
    print("Usage: python node_explorer.py NODE_ID")
    sys.exit()

node = sys.argv[1]

print("\nNODE:", node)
print("-"*40)

if relations_file.exists():
    with open(relations_file) as f:
        for r in csv.DictReader(f):

            if r["from_id"] == node:
                print(f"{node} --{r['relation']}--> {r['to_id']}")

            if r["to_id"] == node:
                print(f"{r['from_id']} --{r['relation']}--> {node}")
else:
    print("No relations file found")

print()
