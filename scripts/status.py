import csv, json, os, re
from pathlib import Path
from collections import Counter

BASE = Path("/opt/atlas")
DATASETS = BASE / "datasets"
RESEARCH = BASE / "research"
MEMORY = BASE / "memory"
SCRIPTS = BASE / "scripts"

# ---- Targets (edit these later as your “projected map”) ----
TARGETS = {
    "tithis": 30,
    "nakshatras": 27,
    # Nitya devi can vary by tradition; keep this as a target you can adjust.
    "nitya_devis": 15,
    # Starter goal for research corpus diversity/size:
    "research_files": 25,
}
WEIGHTS = {
    "system": 0.20,
    "canonical": 0.45,
    "corpus": 0.20,
    "integration": 0.15,
}

# ---- Helpers ----
def exists(p: Path) -> bool:
    return p.exists()

def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def read_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def pct(a, b):
    if b <= 0:
        return 0.0
    return max(0.0, min(1.0, a / b))

def count_research_files():
    if not RESEARCH.exists():
        return 0, 0
    files = []
    total_bytes = 0
    for p in RESEARCH.rglob("*"):
        if p.is_file() and not p.name.startswith("."):
            files.append(p)
            total_bytes += p.stat().st_size
    return len(files), total_bytes

def human_bytes(n):
    for unit in ["B","KB","MB","GB","TB"]:
        if n < 1024:
            return f"{n:.1f}{unit}" if unit != "B" else f"{int(n)}B"
        n /= 1024
    return f"{n:.1f}PB"

def grep_file(path: Path, pattern: str) -> bool:
    if not path.exists():
        return False
    txt = path.read_text(encoding="utf-8", errors="ignore")
    return re.search(pattern, txt) is not None

# ---- Measure Layer A: System Reliability ----
def score_system():
    checks = {
        "Ollama reachable (:11434)": os.system("curl -s http://localhost:11434 >/dev/null 2>&1") == 0,
        "datasets folder": exists(DATASETS),
        "research folder": exists(RESEARCH),
        "memory folder": exists(MEMORY),
        "capsule CSVs present": all(exists(DATASETS / f) for f in ["tithi_list.csv","nitya_devi_mapping.csv","nakshatra_list.csv"]),
        "capsule graph exists": exists(MEMORY / "vedic_cosmology_graph.json"),
        "concept graph exists": exists(MEMORY / "concepts.json"),
    }
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    return passed, total, checks

# ---- Measure Layer B: Canonical dataset coverage ----
def score_canonical():
    tithi_rows = read_csv(DATASETS / "tithi_list.csv")
    naks_rows = read_csv(DATASETS / "nakshatra_list.csv")
    map_rows = read_csv(DATASETS / "nitya_devi_mapping.csv")

    tithis = len(tithi_rows)
    nakshatras = len(naks_rows)

    # Unique nitya devis from mapping file
    nitya_devis = len({(r.get("nitya_devi") or "").strip() for r in map_rows if (r.get("nitya_devi") or "").strip()})

    # Evidence coverage from capsule graph links (if present)
    capsule_graph = read_json(MEMORY / "vedic_cosmology_graph.json") or {}
    links = capsule_graph.get("links", [])
    total_links = len(links)
    links_with_evidence = sum(1 for e in links if isinstance(e, dict) and e.get("evidence"))

    # Scores
    s_tithi = pct(tithis, TARGETS["tithis"])
    s_naks = pct(nakshatras, TARGETS["nakshatras"])
    s_devis = pct(nitya_devis, TARGETS["nitya_devis"])
    s_evidence = pct(links_with_evidence, total_links) if total_links else 0.0

    # canonical score: average of these 4 components
    canonical_score = (s_tithi + s_naks + s_devis + s_evidence) / 4.0

    details = {
        "tithis": (tithis, TARGETS["tithis"], s_tithi),
        "nakshatras": (nakshatras, TARGETS["nakshatras"], s_naks),
        "nitya_devis": (nitya_devis, TARGETS["nitya_devis"], s_devis),
        "evidence_links": (links_with_evidence, total_links, s_evidence),
        "mapping_rows": len(map_rows),
    }
    return canonical_score, details

# ---- Measure Layer C: Research corpus depth ----
def score_corpus():
    n_files, total_bytes = count_research_files()
    s_files = pct(n_files, TARGETS["research_files"])
    # light heuristic: size indicates substance; cap at 10MB for this score
    s_size = pct(min(total_bytes, 10 * 1024 * 1024), 10 * 1024 * 1024)
    corpus_score = (s_files + s_size) / 2.0
    return corpus_score, {"files": n_files, "target_files": TARGETS["research_files"], "size": total_bytes}

# ---- Measure Layer D: Integration readiness ----
def score_integration():
    # very pragmatic checks (no guessing)
    has_research_search = exists(SCRIPTS / "research_search.py")
    ai_router = SCRIPTS / "ai_router.py"
    uses_research = grep_file(ai_router, r"research_search|chromadb|collection\.query")
    has_query = exists(SCRIPTS / "query.py")
    has_graph_viewer = exists(SCRIPTS / "graph_viewer.py")

    checks = {
        "research retrieval module exists": has_research_search,
        "ai_router appears to use retrieval": uses_research,
        "query tool exists": has_query,
        "graph viewer exists": has_graph_viewer,
    }
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    integration_score = passed / total if total else 0.0
    return integration_score, checks

def main():
    sys_passed, sys_total, sys_checks = score_system()
    canonical_score, canonical_details = score_canonical()
    corpus_score, corpus_details = score_corpus()
    integration_score, integration_checks = score_integration()

    system_score = sys_passed / sys_total if sys_total else 0.0

    overall = (
        system_score * WEIGHTS["system"] +
        canonical_score * WEIGHTS["canonical"] +
        corpus_score * WEIGHTS["corpus"] +
        integration_score * WEIGHTS["integration"]
    )

    def fmtp(x): return f"{int(round(x*100))}%"

    print("\nAtlas Status\n")

    print(f"System reliability:   {sys_passed}/{sys_total}  ({fmtp(system_score)})")
    for k,v in sys_checks.items():
        print(f"  [{'OK' if v else 'FAIL'}] {k}")

    print("\nCanonical (extant) coverage:")
    t = canonical_details["tithis"]; n = canonical_details["nakshatras"]; d = canonical_details["nitya_devis"]; e = canonical_details["evidence_links"]
    print(f"  Tithis:        {t[0]}/{t[1]}  ({fmtp(t[2])})")
    print(f"  Nakshatras:    {n[0]}/{n[1]}  ({fmtp(n[2])})")
    print(f"  Nitya Devis:   {d[0]}/{d[1]}  ({fmtp(d[2])})")
    print(f"  Evidence links:{e[0]}/{e[1]}  ({fmtp(e[2])})")
    print(f"  Mapping rows:  {canonical_details['mapping_rows']}")
    print(f"  Canonical score: {fmtp(canonical_score)}")

    print("\nResearch corpus:")
    print(f"  Files: {corpus_details['files']}/{corpus_details['target_files']}  ({fmtp(pct(corpus_details['files'], corpus_details['target_files']))})")
    print(f"  Size:  {human_bytes(corpus_details['size'])}")
    print(f"  Corpus score: {fmtp(corpus_score)}")

    print("\nIntegration readiness:")
    for k,v in integration_checks.items():
        print(f"  [{'OK' if v else 'FAIL'}] {k}")
    print(f"  Integration score: {fmtp(integration_score)}")

    print("\nOverall completion:")
    print(f"  {fmtp(overall)}  (weights: system {WEIGHTS['system']}, canonical {WEIGHTS['canonical']}, corpus {WEIGHTS['corpus']}, integration {WEIGHTS['integration']})\n")

    print("Next good moves (minimal):")
    if not (MEMORY / "vedic_cosmology_graph.json").exists():
        print("  - Run: atlas capsule_build")
    if canonical_details["tithis"][0] < TARGETS["tithis"]:
        print("  - Add missing tithis to datasets/tithi_list.csv")
    if corpus_details["files"] < TARGETS["research_files"]:
        print("  - Add more varied sources into /opt/atlas/research (astro, ritual, plants, music)")
    print("")

if __name__ == "__main__":
    main()
