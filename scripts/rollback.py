import argparse, json, shutil
from pathlib import Path

BASE = Path("/opt/atlas")
DATASETS = BASE / "datasets"
BACKUPS = DATASETS / "_backups"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("backup_id", help="folder name under datasets/_backups/")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json-pretty", action="store_true")
    args = ap.parse_args()

    src = BACKUPS / args.backup_id
    if not src.exists() or not src.is_dir():
        print(json.dumps({"ok": False, "error": "backup not found", "path": str(src)}))
        return

    restored = []
    for f in src.glob("relations_*.csv"):
        target = DATASETS / f.name
        if args.dry_run:
            restored.append({"file": f.name, "to": str(target), "dry_run": True})
        else:
            shutil.copy2(f, target)
            restored.append({"file": f.name, "to": str(target), "restored": True})

    out = {"ok": True, "backup": args.backup_id, "restored": restored}
    print(json.dumps(out, indent=2 if args.json_pretty else None))

if __name__ == "__main__":
    main()
