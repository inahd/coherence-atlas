import os
import shutil

BASE = "/opt/atlas/import"
INCOMING = os.path.join(BASE, "incoming")
PROCESSING = os.path.join(BASE, "processing")

def prepare_files():
    files = os.listdir(INCOMING)

    for f in files:
        src = os.path.join(INCOMING, f)
        dst = os.path.join(PROCESSING, f)

        if os.path.isfile(src):
            print(f"Preparing: {f}")
            shutil.move(src, dst)

if __name__ == "__main__":
    prepare_files()
