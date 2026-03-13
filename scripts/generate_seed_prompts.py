import csv, json, time
from pathlib import Path

BASE = Path("/opt/atlas")
DS = BASE / "datasets"
REPORTS = BASE / "memory" / "reports"
PROMPTS_DIR = BASE / "prompts"
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

PROMPTS_MD = PROMPTS_DIR / "seed_prompts.md"

REL_FILES = [
    DS / "relations_nakshatra_deity.csv",
    DS / "relations_devi_weapon.csv",
    DS / "relations_nakshatra_plants.csv",
    DS / "relations_ritual_calendar.csv",
    DS / "relations_raga_ritual.csv",
    DS / "relations_nakshatra_graha.csv",
]

EVID_KEYS = ["source_title", "source_locator", "excerpt"]

def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def factcheck_snapshot():
    total = 0
    missing_to = 0
    missing_ev = 0
    by_file = []
    for f in REL_FILES:
        rows = read_csv(f)
        if not rows:
            by_file.append((f.name, 0, 0, 0))
            continue
        mt = 0
        me = 0
        for r in rows:
            total += 1
            if not (r.get("to_id") or "").strip():
                mt += 1
            ev_ok = all((r.get(k) or "").strip() for k in EVID_KEYS)
            if not ev_ok:
                me += 1
        missing_to += mt
        missing_ev += me
        by_file.append((f.name, len(rows), mt, me))
    return total, missing_to, missing_ev, by_file

def list_research_public(maxn=40):
    root = BASE / "research_public"
    if not root.exists():
        return []
    items = []
    for p in sorted(root.rglob("*")):
        if p.is_file():
            items.append(str(p))
        if len(items) >= maxn:
            break
    return items

def list_reports(maxn=20):
    if not REPORTS.exists():
        return []
    items = []
    for p in sorted(REPORTS.glob("*")):
        if p.is_file():
            items.append(p.name)
        if len(items) >= maxn:
            break
    return items

def sample_missing(rows, n=15):
    miss_to = []
    miss_ev = []
    for r in rows:
        to_missing = not (r.get("to_id") or "").strip()
        ev_missing = not all((r.get(k) or "").strip() for k in EVID_KEYS)
        if to_missing:
            miss_to.append(r)
        elif ev_missing:
            miss_ev.append(r)
    return miss_to[:n], miss_ev[:n]

def mk(title, body):
    return f"## {title}\n\n{body.rstrip()}\n\n"

def mk_code(lang, body):
    return f"```{lang}\n{body.rstrip()}\n```\n\n"

def build():
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    total, missing_to, missing_ev, by_file = factcheck_snapshot()

    state = []
    state.append(f"Generated: {now}")
    state.append("")
    state.append("Factcheck snapshot:")
    state.append(f"- total rows: {total}")
    state.append(f"- missing to_id: {missing_to}")
    state.append(f"- missing evidence: {missing_ev}")
    state.append("")
    state.append("Per-file:")
    for name, n, mt, me in by_file:
        state.append(f"- {name}: rows={n} missing_to_id={mt} missing_evidence={me}")

    research_pub = list_research_public()
    reports = list_reports()

    # Build a compact queue of missing work
    missing_to_all = []
    missing_ev_all = []
    for f in REL_FILES:
        rows = read_csv(f)
        mt, me = sample_missing(rows, n=10)
        missing_to_all.extend([(f.name, r) for r in mt])
        missing_ev_all.extend([(f.name, r) for r in me])
    missing_to_all = missing_to_all[:30]
    missing_ev_all = missing_ev_all[:30]

    queue_to = "\n".join([f"- {fn}\t{r.get('from_id','')}\t{r.get('relation','')}\t(to_id missing)" for fn, r in missing_to_all]) or "(none)"
    queue_ev = "\n".join([f"- {fn}\t{r.get('from_id','')}\t{r.get('relation','')}\t{r.get('to_id','')}" for fn, r in missing_ev_all]) or "(none)"

    # Prompt pack
    out = "# Atlas Seed Prompts (Batch Processor Pack)\n\n"

    out += mk("Contract (read first)", mk_code("text", """
You are helping maintain Coherence Atlas: a local-first Vedic knowledge graph.

Hard rules:
- Do NOT hallucinate citations. If evidence is not present, output NO EVIDENCE FOUND.
- Keep canon clean: anything uncertain must remain auto_proposed or seed_unverified.
- Every canonical-eligible row MUST include: source_title, source_locator, excerpt, tradition, confidence.
- IDs must follow: type:slug_or_int (lowercase, underscores for spaces).
- Output MUST be files (with suggested filenames) containing clean blocks (CSV/YAML/JSON) only.
"""))

    out += mk("Ontology + allowed relations", mk_code("yaml", """
id_format: "type:slug_or_int"
entity_types:
  - nakshatra
  - tithi
  - graha
  - rashi
  - deity
  - devi
  - nitya_devi
  - plant
  - weapon
  - ritual
  - raga
relations:
  - name: nakshatra_associated_deity
    from: nakshatra
    to: [deity, devi, nitya_devi]
  - name: nakshatra_ruling_graha
    from: nakshatra
    to: [graha]
  - name: nakshatra_sacred_plant
    from: nakshatra
    to: [plant]
  - name: devi_wields_weapon
    from: devi
    to: [weapon]
  - name: ritual_prescribed_on
    from: ritual
    to: [tithi, nakshatra]
  - name: ritual_uses_raga
    from: ritual
    to: [raga]
confidence_allowed: [seed_unverified, auto_proposed, attested_secondary, canonical]
evidence_required: [source_title, source_locator, excerpt]
"""))

    out += mk("Current state", mk_code("text", "\n".join(state)))

    out += mk("Available public research files (repo-safe)", mk_code("text", "\n".join(research_pub) if research_pub else "(none found in /opt/atlas/research_public)"))

    out += mk("Reports present", mk_code("text", "\n".join(reports) if reports else "(no reports found)"))

    out += mk("Task A — Fill missing to_id (safe structural completion)", mk_code("text", f"""
For each row below:
- propose to_id (type:slug) and confidence (HIGH/MED/LOW).
- HIGH only if mapping is widely standard; MED if tradition-dependent; LOW if speculative.
- Output a CSV file patch that updates ONLY to_id + confidence + notes.
Queue:
{queue_to}
"""))

    out += mk("Task B — Attach evidence to evidence-missing rows", mk_code("text", f"""
For each row below (to_id present; evidence missing):
- Find/construct evidence ONLY from provided sources/excerpts (if included in the pasted bundle).
- If you cannot, output NO EVIDENCE FOUND for that row.
- Output a CSV file patch that updates source_title, source_locator, excerpt, tradition, confidence, notes.
Queue:
{queue_ev}
"""))

    out += mk("Task C — Generate new relation rows from a single source (Journey-with-the-Moon etc.)", mk_code("text", """
Given a pasted excerpt bundle from one source, propose new seed rows into:
- relations_ritual_calendar.csv (ritual_prescribed_on)
- relations_raga_ritual.csv (ritual_uses_raga)
Rules:
- include source_title + locator + excerpt in every new row
- confidence must be seed_unverified or auto_proposed unless explicitly attested
Output new CSV files with correct headers.
"""))

    out += mk("Output format (strict)", mk_code("text", """
Return results as multiple files.

For each file:
1) A line: FILENAME: <path/filename>
2) Then the exact file content as a clean block (CSV/YAML/JSON)
3) No extra commentary.

CSV headers must match existing dataset headers exactly.
"""))

    return out

def main():
    PROMPTS_MD.write_text(build(), encoding="utf-8")
    print("Wrote:", PROMPTS_MD)

if __name__ == "__main__":
    main()
