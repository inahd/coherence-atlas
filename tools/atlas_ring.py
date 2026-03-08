import subprocess

steps = [
    ("🌱 Parsing seeds", ["python","tools/build_graph.py"]),
    ("🃏 Generating cards", ["python","tools/generate_cards.py"]),
    ("🌌 Rendering constellation", ["python","tools/render_constellation.py"]),
]

print("🔔 Atlas bell rung\n")

for name,cmd in steps:
    print(name)
    try:
        subprocess.run(cmd)
    except:
        print("⚠ step failed")

print("\n✨ Atlas cycle complete.")
