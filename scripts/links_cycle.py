from __future__ import annotations
import argparse, json, os, re, time, hashlib, random, string, shutil, sys
from pathlib import Path
from urllib.parse import urlparse
import subprocess
import fcntl

BASE = Path("/opt/atlas")
RESEARCH = BASE / "research"
WGETROOT = RESEARCH / "_wget"
JOBS = WGETROOT / "jobs"
LOCK = WGETROOT / "lock"
SEEDS = WGETROOT / "seeds.json"
LINKS = WGETROOT / "links.json"
LINKS_TXT = WGETROOT / "links.txt"

KEYWORDS_DEFAULT = [
    "nakshatra","tithi","panchang","panchanga","jyotish","jyotisha","vedanga",
    "ritual","vrata","festival","mantra","sangita","raga","tala","stotra"
]

# Curated starter set (PD/CC0; see notes in report)
DEFAULT_SEED_LINKS = [
  {"url":"https://upload.wikimedia.org/wikipedia/commons/5/58/Translation_of_surya_siddhanta_%28IA_dli.csl.7956%29.pdf",
   "title":"Translation of Surya Siddhanta (1860)", "license":"PDM (Wikimedia Commons)", "base_score": 5.0},
  {"url":"https://upload.wikimedia.org/wikipedia/commons/8/81/Hindu_fasts_and_feasts_%28IA_hindufastsfeasts00mukeiala%29.pdf",
   "title":"Hindu fasts and feasts (1918)", "license":"PD-1923 (Wikimedia Commons)", "base_score": 4.0},
  {"url":"https://www.wilbourhall.org/pdfs/the_brihat_jataka_of_varaha_mihira.pdf",
   "title":"The Brihat Jataka of Varaha Mihira (public domain scan)", "license":"Public domain notice in scan", "base_score": 4.0},
  {"url":"https://archive.org/download/wg1077/WG1077-1865%20-The%20Brihat%20Samhita%20Of%20Varaha-Mihira_text.pdf",
   "title":"The Brihat Samhita of Varaha Mihira (1865) [PDF with text]", "license":"Likely PD (pre-1931); verify on item page", "base_score": 3.5},
  {"url":"https://ia801506.us.archive.org/32/items/in.ernet.dli.2015.170526/2015.170526.Hindu-Feasts-Fasts-And-Ceremonies_text.pdf",
   "title":"Hindu Feasts, Fasts and Ceremonies (1902) [PDF with text]", "license":"PD (Wikisource claims PD); verify", "base_score": 3.5},
  {"url":"https://archive.org/download/hindumusicfromvariousauthorssourindromohuntagore/Hindu%20Music%20From%20Various%20Authors%20Sourindro%20Mohun%20Tagore.pdf",
   "title":"Hindu Music From Various Authors (Tagore)","license":"CC0 (Internet Archive item)", "base_score": 3.0},
  {"url":"https://archive.org/download/SharadaAlmanac504920301895197374VijeshwarPanchang/Sharada%20Almanac_5049_2030_1895_1973-74%20-%20Vijeshwar%20Panchang.pdf",
   "title":"Sharada Almanac (Vijeshwar Panchang)","license":"CC0 (Internet Archive item)", "base_score": 3.0},
  {"url":"https://archive.org/download/NakshatraJyotishRagunandanPrasadGowd/Nakshatra%20Jyotish%20-Ragunandan%20Prasad%20Gowd_text.pdf",
   "title":"Nakshatra Jyotish (Ragunandan Prasad Gowd) [PDF with text]","license":"CC0 (Internet Archive item)", "base_score": 3.0},
  {"url":"https://archive.org/download/VedicMantrasOfNakshatraSwamiMssNo215SanskritAlm7Shelf4PanjabUni.pdf/Vedic%20Mantras%20of%20Nakshatra%20Swami_Mss%20No%20215_Sanskrit_Alm%207_Shelf%204-Panjab%20Uni.pdf.pdf",
   "title":"Vedic Mantras of Nakshatra (manuscript scan)","license":"CC0 (Internet Archive item)", "base_score": 3.0},
  {"url":"https://archive.org/download/in.ernet.dli.2015.109519/2015.109519.A-Historical-View-Of-The-Hindu-Astronomy--Part-1-2_text.pdf",
   "title":"A Historical View of the Hindu Astronomy (1825) [PDF with text]","license":"In Public Domain (item metadata)", "base_score": 3.0},
]

def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def rand_id(n=6) -> str:
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()

def safe_slug(name: str, maxlen: int = 90) -> str:
    name = name.strip()
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return (name[:maxlen] or "download")

def run_cmd(argv: list[str], timeout: int | None = None) -> dict:
    t0 = time.time()
    try:
        cp = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return {
            "cmd": argv,
            "code": cp.returncode,
            "stdout": cp.stdout[-3000:],
            "stderr": cp.stderr[-2000:],
            "seconds": round(time.time() - t0, 3),
        }
    except subprocess.TimeoutExpired as e:
        return {
            "cmd": argv, "code": 124, "timeout": True,
            "stdout": (e.stdout or "")[-2000:], "stderr": (e.stderr or "TIMEOUT")[-2000:],
            "seconds": round(time.time() - t0, 3),
        }

def load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default
    return default

def save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

def score_entry(title: str, url: str, base: float, keywords: list[str]) -> float:
    t = (title or "").lower()
    u = (url or "").lower()
    score = base
    for kw in keywords:
        if kw in t: score += 0.8
        if kw in u: score += 0.3
    if "upload.wikimedia.org" in u: score += 0.5
    if "archive.org" in u or "us.archive.org" in u: score += 0.2
    return round(score, 3)

def init_cmd(force: bool) -> dict:
    WGETROOT.mkdir(parents=True, exist_ok=True)
    JOBS.mkdir(parents=True, exist_ok=True)
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    LOCK.touch(exist_ok=True)

    if force or not SEEDS.exists():
        save_json(SEEDS, {"generated": now_iso(), "links": DEFAULT_SEED_LINKS, "seed_pages": []})

    if force or not LINKS.exists():
        save_json(LINKS, {"generated": now_iso(), "links": {}})

    return {"ok": True, "seeds_path": str(SEEDS), "links_path": str(LINKS)}

def build_cmd(keywords: list[str]) -> dict:
    seeds = load_json(SEEDS, {"links": [], "seed_pages": []})
    reg = load_json(LINKS, {"links": {}})
    links = reg.get("links", {})

    # Add seed links
    for s in seeds.get("links", []):
        url = s["url"].strip()
        if not url:
            continue
        if url not in links:
            links[url] = {
                "url": url,
                "title": s.get("title",""),
                "license": s.get("license","unspecified"),
                "score": 0.0,
                "success": 0,
                "fail": 0,
                "last_status": None,
                "last_seen": now_iso(),
            }
        else:
            links[url]["last_seen"] = now_iso()
            if s.get("title"): links[url]["title"] = s["title"]

        base = float(s.get("base_score", 1.0))
        links[url]["score"] = score_entry(links[url].get("title",""), url, base, keywords)

    # Write registry + plain list txt sorted by score
    reg["generated"] = now_iso()
    reg["links"] = links
    save_json(LINKS, reg)

    ordered = sorted(links.values(), key=lambda x: x.get("score",0), reverse=True)
    LINKS_TXT.write_text("\n".join([x["url"] for x in ordered]) + "\n", encoding="utf-8")

    return {
        "ok": True,
        "links_total": len(links),
        "written": [str(LINKS), str(LINKS_TXT)],
        "top5": [{"url": x["url"], "score": x["score"]} for x in ordered[:5]],
    }

def download_one(url: str, out_dir: Path, wait_s: float, max_mib: int | None) -> dict:
    u = urlparse(url)
    base = Path(u.path).name or "download.pdf"
    if not base.lower().endswith(".pdf"):
        base += ".pdf"

    prefix = sha1(url)[:10]
    fname = f"{prefix}__{safe_slug(base)}"
    out_path = out_dir / fname

    argv = ["wget", "-c", "-nv", f"--wait={wait_s}", "--random-wait", "--tries=3", "--timeout=30"]
    if max_mib is not None:
        argv.append(f"--max-filesize={max_mib}m")
    argv += ["-O", str(out_path), url]

    r = run_cmd(argv, timeout=None)
    ok = (r["code"] == 0 and out_path.exists() and out_path.stat().st_size > 0)

    return {"url": url, "out": str(out_path), "ok": ok, "wget": r, "bytes": out_path.stat().st_size if out_path.exists() else 0}

def write_status(job_dir: Path, obj: dict):
    save_json(job_dir / "status.json", obj)

def run_cycle(job_id: str, top: int, propose: int, graph: bool, dry_run: bool, wait: float, max_mib: int | None) -> dict:
    LOCK.touch(exist_ok=True)
    with LOCK.open("r+") as lf:
        fcntl.flock(lf.fileno(), fcntl.LOCK_EX)

        # Ensure base files exist
        if not SEEDS.exists() or not LINKS.exists():
            init_cmd(force=False)

        build = build_cmd(KEYWORDS_DEFAULT)
        reg = load_json(LINKS, {"links": {}})
        links = list(reg.get("links", {}).values())
        links = sorted(links, key=lambda x: x.get("score",0), reverse=True)[:top]

        job_dir = JOBS / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        status = {
            "job_id": job_id,
            "started": now_iso(),
            "state": "running",
            "dry_run": dry_run,
            "download": {"requested": top, "completed": 0, "ok": 0, "items": []},
            "ingest": None,
            "pipeline": None,
            "ended": None,
        }
        write_status(job_dir, status)

        # Download
        downloaded_files = []
        for entry in links:
            url = entry["url"]
            if dry_run:
                item = {"url": url, "dry_run": True}
            else:
                item = download_one(url, job_dir, wait_s=wait, max_mib=max_mib)
                if item.get("ok"):
                    downloaded_files.append(item["out"])
            status["download"]["items"].append(item)
            status["download"]["completed"] += 1
            status["download"]["ok"] += 1 if item.get("ok") else 0
            write_status(job_dir, status)

        # Ingest + maturity
        if not dry_run:
            ingest_cmd = ["atlas", "ingest", "--paths", str(job_dir), "--propose", str(propose)]
            # ensure JSON stdout
            ingest_cmd += ["--json-pretty"]
            if graph:
                ingest_cmd += ["--graph"]

            ing = run_cmd(ingest_cmd, timeout=None)
            status["ingest"] = ing
            # Try to parse ingest JSON from stdout
            try:
                status["pipeline"] = json.loads(ing.get("stdout","{}"))
            except Exception:
                status["pipeline"] = {"parse_error": True}

        status["state"] = "finished"
        status["ended"] = now_iso()
        write_status(job_dir, status)

        # Score updates (simple)
        reg = load_json(LINKS, {"links": {}})
        reg_links = reg.get("links", {})
        for item in status["download"]["items"]:
            url = item["url"]
            if url not in reg_links:
                continue
            if item.get("ok"):
                reg_links[url]["success"] = int(reg_links[url].get("success",0)) + 1
                reg_links[url]["last_status"] = "ok"
                reg_links[url]["score"] = float(reg_links[url].get("score",0)) + 0.25
            else:
                reg_links[url]["fail"] = int(reg_links[url].get("fail",0)) + 1
                reg_links[url]["last_status"] = "fail"
                reg_links[url]["score"] = float(reg_links[url].get("score",0)) - 0.5
            reg_links[url]["last_seen"] = now_iso()

        reg["generated"] = now_iso()
        reg["links"] = reg_links
        save_json(LINKS, reg)

        return {"ok": True, "job_id": job_id, "job_dir": str(job_dir), "status_file": str(job_dir / "status.json")}

def spawn_async(args_list: list[str]) -> dict:
    job_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + "_" + rand_id(4)
    job_dir = JOBS / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    save_json(job_dir / "status.json", {"job_id": job_id, "state": "queued", "created": now_iso()})

    # Spawn a detached process that runs: links_cycle.py run-job <job_id> ...
    argv = [sys.executable, str(Path(__file__).resolve()), "run-job", job_id] + args_list
    with open(os.devnull, "w") as dn:
        p = subprocess.Popen(argv, stdout=dn, stderr=dn, start_new_session=True)
    return {"ok": True, "job_id": job_id, "pid": p.pid, "status_file": str(job_dir / "status.json")}

def status_cmd(job_id: str) -> dict:
    job_dir = JOBS / job_id
    st = job_dir / "status.json"
    if not st.exists():
        return {"ok": False, "error": "missing job", "job_id": job_id}
    return load_json(st, {})

def main():
    ap = argparse.ArgumentParser(prog="atlas links")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--force", action="store_true")

    p_build = sub.add_parser("build")
    p_build.add_argument("--keywords", nargs="*", default=KEYWORDS_DEFAULT)

    p_cycle = sub.add_parser("cycle")
    p_cycle.add_argument("--top", type=int, default=10)
    p_cycle.add_argument("--propose", type=int, default=25)
    p_cycle.add_argument("--graph", action="store_true")
    p_cycle.add_argument("--dry-run", action="store_true")
    p_cycle.add_argument("--async", dest="async_mode", action="store_true")
    p_cycle.add_argument("--wait", type=float, default=1.0)
    p_cycle.add_argument("--max-mib", type=int, default=None, help="wget --max-filesize (MiB)")

    p_run = sub.add_parser("run-job")
    p_run.add_argument("job_id")
    p_run.add_argument("--top", type=int, default=10)
    p_run.add_argument("--propose", type=int, default=25)
    p_run.add_argument("--graph", action="store_true")
    p_run.add_argument("--dry-run", action="store_true")
    p_run.add_argument("--wait", type=float, default=1.0)
    p_run.add_argument("--max-mib", type=int, default=None)

    p_status = sub.add_parser("status")
    p_status.add_argument("job_id")

    args = ap.parse_args()

    if args.cmd == "init":
        out = init_cmd(force=args.force)
    elif args.cmd == "build":
        out = build_cmd(args.keywords)
    elif args.cmd == "cycle":
        if args.async_mode:
            out = spawn_async(["--top", str(args.top), "--propose", str(args.propose)] +
                              (["--graph"] if args.graph else []) +
                              (["--dry-run"] if args.dry_run else []) +
                              ["--wait", str(args.wait)] +
                              (["--max-mib", str(args.max_mib)] if args.max_mib is not None else []))
        else:
            job_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + "_" + rand_id(4)
            out = run_cycle(job_id, args.top, args.propose, args.graph, args.dry_run, args.wait, args.max_mib)
    elif args.cmd == "run-job":
        out = run_cycle(args.job_id, args.top, args.propose, args.graph, args.dry_run, args.wait, args.max_mib)
    elif args.cmd == "status":
        out = status_cmd(args.job_id)

    print(json.dumps(out, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
