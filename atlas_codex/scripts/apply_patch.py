import csv
import sys

PATCH_FILE = sys.argv[1]

print("Applying patch:", PATCH_FILE)

with open(PATCH_FILE) as f:
    reader = csv.reader(f)
    for row in reader:
        print("Patch row:", row)

print("Patch preview complete. Review before applying to canon.")
