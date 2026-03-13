import subprocess
import sys

if len(sys.argv)<2:
    print("Usage: run.py <script>")
    exit()

script=sys.argv[1]

subprocess.run(f"python /opt/atlas/scripts/{script}",shell=True)
