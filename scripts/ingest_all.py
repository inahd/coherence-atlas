from __future__ import annotations
import argparse, json, time, hashlib, shutil, sys, os
from pathlib import Path
import subprocess
import fcntl

BASE = Path("/opt/atlas")
RESEARCH = BASE / "research"
TEXTDIR = RESEARCH / "_text"
INGEST_DIR = RESEARCH / "_ingest"
MANIFEST = INGEST_DIR / "manifest.json"
LOCKFILE = INGEST_DIR / "lock"
DATASETS = BASE / "datasets"
BACKUPS = DATASETS / "_backups"

EXCLUDE_DIRS = {"_text", "_ingest"}  # _wget is allowed (jobs live there)

def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def sha256_file(p: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def file_id(p: Path) -> str:
    return hashlib.sha1(str(p.resolve()).encode("utf-8", errors="ignore")).hexdigest()[:8]

def text_output_for(pdf: Path) -> Path:
    return TEXTDIR / f"{pdf.stem}__{file_id(pdf)}.txt"

def ensure_under_root(p: Path, root: Path) -> Path:
    rp = p.expanduser().resolve()
    rr = root.resolve()
    try:
        rp.relative_to(rr)
    except ValueError:
        raise ValueError(f"path outside allowed root: {rp} (root={rr})")
    return rp

def load_manifest() -> dict:
    if MANIFEST.exists():
        try:
            return json.loads(MANIFEST.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_manifest(m: dict):
    INGEST_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")

def run_cmd(argv: list[str], timeout: int | None = None) -> dict:
    t0 = time.time()
    try:
        cp = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return {
            "cmd": argv,
            "code": cp.returncode,
            "stdout": cp.stdout[-4000:],
            "stderr": cp.stderr[-2000:],
            "seconds": round(time.time() - t0, 3),
        }
    except subprocess.TimeoutExpired as e:
        return {
            "cmd": argv,
            "code": 124,
            "stdout": (e.stdout or "")[-2000:],
            "stderr": (e.stderr or "TIMEOUT")[-2000:],
            "seconds": round(time.time() - t0, 3),
            "timeout": True,
        }

def iter_pdfs(paths: list[Path]) -> list[Path]:
    out = []
    for p in paths:
        if p.is_file() and p.suffix.lower() == ".pdf":
            out.append(p)
        elif p.is_dir():
            for x in p.rglob("*.pdf"):
                if any(part in EXCLUDE_DIRS for part in x.parts):
                    continue
                if x.is_file():
                    out.append(x)
    return sorted(set(out))

def text_stats(pdf: Path, threshold: int) -> dict:
    txt = text_output_for(pdf)
    if not txt.exists():
        return {"text_path": str(txt), "text_chars": 0, "low_text": None}
    s = txt.read_text(encoding="utf-8", errors="ignore").strip()
    n = len(s)
    return {"text_path": str(txt), "text_chars": n, "low_text": (n < threshold)}

def backup_relations(run_id: str) -> str:
    dst = BACKUPS / run_id
    dst.mkdir(parents=True, exist_ok=True)
    copied = 0
    for f in DATASETS.glob("relations_*.csv"):
        shutil.copy2(f, dst / f.name)
        copied += 1
    return str(dst)

def maybe_ocr(pdf: Path, out_pdf: Path) -> dict:
    # Only run if ocrmypdf is installed
    if shutil.which("ocrmypdf") is None:
        return {"ok": False, "error": "ocrmypdf not installed"}
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    # --skip-text avoids re-OCR on pages that already have text
    return run_cmd(["ocrmypdf", "--skip-text", str(pdf), str(out_pdf)], timeout=None)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", nargs="*", default=[str(RESEARCH)], help="PDF file/dir paths under /opt/atlas/research")
    ap.add_argument("--propose", type=int, default=25)
    ap.add_argument("--graph", action="store_true")
    ap.add_argument("--always-pipeline", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--threshold", type=int, default=500, help="low-text detection threshold (chars)")
    ap.add_argument("--backup", action="store_true", default=True, help="backup relations_*.csv before propose")
    ap.add_argument("--no-backup", action="store_true", help="disable backup")
    ap.add_argument("--ocr", action="store_true", help="OCR low-text PDFs using ocrmypdf --skip-text")
    ap.add_argument("--json-pretty", action="store_true")
    args = ap.parse_args()

    if args.no_backup:
        args.backup = False

    # Resolve & restrict paths to /opt/atlas/research
    in_paths = [ensure_under_root(Path(p), RESEARCH) for p in args.paths]

    INGEST_DIR.mkdir(parents=True, exist_ok=True)
    LOCKFILE.touch(exist_ok=True)

    result = {"ok": True, "run_id": time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()), "started": now_iso()}
    t_start = time.time()

    with LOCKFILE.open("r+") as lf:
        fcntl.flock(lf.fileno(), fcntl.LOCK_EX)

        mf = load_manifest()
        mf.setdefault("meta", {})
        mf.setdefault("files", {})

        pdfs = iter_pdfs(in_paths)
        changed = []
        unchanged = 0

        for pdf in pdfs:
            rel = str(pdf.relative_to(RESEARCH))
            h = sha256_file(pdf)
            old = mf["files"].get(rel, {})
            if old.get("sha256") == h:
                unchanged += 1
                continue
            changed.append((pdf, rel, h))

        result["pdfs_found"] = len(pdfs)
        result["unchanged"] = unchanged
        result["changed"] = len(changed)

        harvested = []
        low_text = []

        # Harvest only changed PDFs
        for pdf, rel, h in changed:
            entry = {"pdf": rel, "sha256": h}
            if args.dry_run:
                entry["dry_run"] = True
                harvested.append(entry)
                continue

            # Harvest via existing command
            r = run_cmd(["atlas", "harvestpdf", str(pdf)], timeout=None)
            entry["harvest"] = r

            stats = text_stats(pdf, args.threshold)
            entry.update(stats)

            mf["files"][rel] = {
                "sha256": h,
                "last_ingested": now_iso(),
                "harvest_code": r.get("code"),
                "text_path": stats["text_path"],
                "text_chars": stats["text_chars"],
                "low_text": stats["low_text"],
                "size_bytes": pdf.stat().st_size,
            }

            if stats["low_text"] is True:
                low_text.append(rel)

                # Optional OCR
                if args.ocr:
                    ocr_out = pdf.with_suffix("").with_name(pdf.stem + "__ocr.pdf")
                    ocr_out = ensure_under_root(ocr_out, RESEARCH)
                    ocr_res = maybe_ocr(pdf, ocr_out)
                    entry["ocr"] = ocr_res
                    # If OCR succeeded, harvest OCR output too
                    if ocr_res.get("code") == 0 and ocr_out.exists():
                        r2 = run_cmd(["atlas", "harvestpdf", str(ocr_out)], timeout=None)
                        entry["harvest_ocr"] = r2

            harvested.append(entry)

        if not args.dry_run:
            mf["meta"]["last_run"] = now_iso()
            save_manifest(mf)

        result["harvested"] = harvested
        result["low_text"] = low_text
        result["manifest"] = str(MANIFEST)

        # Maturity pipeline once per run
        pipeline = {"ran": False}
        should_run = args.always_pipeline or (len(changed) > 0)

        if should_run and not args.dry_run:
            pipeline["ran"] = True
            if args.backup:
                pipeline["backup_dir"] = backup_relations(result["run_id"])

            pipeline["propose"] = run_cmd(["atlas", "propose", str(args.propose)], timeout=None)
            pipeline["factcheck"] = run_cmd(["atlas", "factcheck"], timeout=None)
            pipeline["seedgraph"] = run_cmd(["atlas", "seedgraph"], timeout=None)
            if args.graph:
                pipeline["graph"] = run_cmd(["atlas", "graph", "seed"], timeout=None)

        result["pipeline"] = pipeline

    result["ended"] = now_iso()
    result["seconds"] = round(time.time() - t_start, 3)

    s = json.dumps(result, indent=2 if args.json_pretty else None, ensure_ascii=False)
    print(s)

if __name__ == "__main__":
    main()
