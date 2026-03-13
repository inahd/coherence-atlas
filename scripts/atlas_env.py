import sys

def main():
    off = len(sys.argv) > 1 and sys.argv[1] in ("--off","off","deactivate")

    if off:
        print("deactivate 2>/dev/null || true")
        return

    print("cd /opt/atlas && source /opt/atlas/venv/bin/activate")

if __name__ == "__main__":
    main()
