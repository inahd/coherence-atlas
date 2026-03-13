import os

print("🩺 Atlas Doctor\n")

paths = [
    "architecture",
    "seeds",
    "atlas_graph",
    "cards",
    "visual",
    "tools"
]

for p in paths:
    if os.path.exists(p):
        print(f"✔ {p}/ exists")
    else:
        print(f"⚠ {p}/ missing")

print("\nSeed files:")
if os.path.exists("seeds"):
    seeds = [f for f in os.listdir("seeds") if f.endswith(".md")]
    if seeds:
        for s in seeds:
            print("  🌱", s)
    else:
        print("  ⚠ no seeds found")

print("\nGraph status:")
if os.path.exists("atlas_graph/nodes.json"):
    print("✔ nodes.json exists")
else:
    print("⚠ nodes.json missing")

if os.path.exists("atlas_graph/relations.json"):
    print("✔ relations.json exists")
else:
    print("⚠ relations.json missing")

print("\nDiagnosis complete.")
