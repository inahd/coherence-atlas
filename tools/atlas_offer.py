import os
import shutil

BASE = "/opt/atlas/import"
PROCESSING = os.path.join(BASE, "processing")
IMPORTED = os.path.join(BASE, "imported")

def offer_files():
    files = os.listdir(PROCESSING)

    for f in files:
        src = os.path.join(PROCESSING, f)
        dst = os.path.join(IMPORTED, f)

        if os.path.isfile(src):
            print(f"Offering: {f}")
            shutil.move(src, dst)

if __name__ == "__main__":
    offer_files()
