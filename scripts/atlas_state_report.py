import os
import subprocess
from pathlib import Path
from collections import Counter

ROOT = Path("/opt/atlas")
OUT = ROOT / "analysis" / "atlas_state_report.txt"

OUT.parent.mkdir(exist_ok=True)

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True)
    except:
        return "error running command\n"

def file_extensions():
    counter = Counter()
    for root, dirs, files in os.walk(ROOT):
        for f in files:
            ext = f.split(".")[-1] if "." in f else "noext"
            counter[ext] += 1
    return counter

def largest_files():
    results = []
    for root, dirs, files in os.walk(ROOT):
        for f in files:
            p = Path(root) / f
            try:
                size = p.stat().st_size
                if size > 20_000_000:
                    results.append((size, str(p)))
            except:
                pass
    return sorted(results, reverse=True)[:20]

with open(OUT, "w") as report:

    report.write("=== ATLAS STATE REPORT ===\n\n")

    report.write("ROOT:\n")
    report.write(str(ROOT) + "\n\n")

    report.write("=== DIRECTORY SIZES ===\n")
    report.write(run("du -h --max-depth=1 /opt/atlas | sort -h"))
    report.write("\n")

    report.write("=== RECENT FILES ===\n")
    report.write(run("find /opt/atlas -type f -printf '%TY-%Tm-%Td %TT %p\\n' | sort -r | head -40"))
    report.write("\n")

    report.write("=== GIT STATUS ===\n")
    report.write(run("git -C /opt/atlas status"))
    report.write("\n")

    report.write("=== GIT RECENT COMMITS ===\n")
    report.write(run("git -C /opt/atlas log --oneline -20"))
    report.write("\n")

    report.write("=== FILE EXTENSION COUNTS ===\n")
    for ext, count in file_extensions().most_common():
        report.write(f"{ext}: {count}\n")
    report.write("\n")

    report.write("=== LARGE FILES (>20MB) ===\n")
    for size, path in largest_files():
        report.write(f"{size/1024/1024:.1f} MB  {path}\n")

print("Atlas report written to:", OUT)

