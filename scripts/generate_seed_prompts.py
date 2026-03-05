import csv, json, time
from pathlib import Path

BASE = Path("/opt/atlas")
DS = BASE / "datasets"
REPORTS = BASE / "memory" / "reports"
PROMPTS_DIR = BASE / "prompts"
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

GAPS_JSON = REPORTS / "gaps.json"
PROMPTS_MD = PROMPTS_DIR / "seed_prompts.md"

REL_FILES = [
    DS / "relations_nakshatra_deity.csv",
    DS / "relations_devi_weapon.csv",
    DS / "relations_nakshatra_plants.csv",
    DS / "relations_ritual_calendar.csv",
    DS / "relations_raga_ritual.csv",
    DS / "relations_nakshatra_graha.csv",
]

EVID_KEYS = ["source_title","source_locator","excerpt"]

def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def pick_missing(rows, n=10):
    # prioritize missing to_id first, then missing evidence
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

def load_gaps_summary():
    if not GAPS_JSON.exists():
        return ""
    try:
        g = json.loads(GAPS_JSON.read_text(encoding="utf-8"))
        top = g.get("prioritized", [])[:8]
        lines = [f"- {x.get('bucket')}: score={int(x.get('score',0))} miss_to={x.get('missing_to_id')} miss_ev={x.get('missing_evidence')}" for x in top]
        return "\n".join(lines)
    except Exception:
        return ""

def mk_block(title, body, lang="text"):
    return f"### {title}\n\n```{lang}\n{body.rstrip()}\n```\n"

def build_prompt_bundle():
    # Collect a small actionable queue across relations
    missing_to_all = []
    missing_ev_all = []

    for f in REL_FILES:
        rows = read_csv(f)
        miss_to, miss_ev = pick_missing(rows, n=12)
        for r in miss_to:
            missing_to_all.append((f.name, r))
        for r in miss_ev:
            missing_ev_all.append((f.name, r))

    missing_to_all = missing_to_all[:25]
    missing_ev_all = missing_ev_all[:25]

    gaps = load_gaps_summary()
    header = f"# Atlas Seed Prompts\n\nGenerated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n## Current gap priorities\n{gaps or '(run: atlas gaps)'}\n"

    # Prompt 1: “Evidence-first fill” (best for canonical maturation)
    ev_rows_txt = "\n".join(
        [f"- {fname} | {r.get('from_id','')} | {r.get('relation','')} | {r.get('to_id','')}" for fname, r in missing_ev_all]
    ) or "(none)"
    p1 = f"""You are helping me mature an evidence-backed Vedic knowledge graph.

Task:
- For each row below (has to_id, missing evidence), propose:
  - source_title (likely document name),
  - source_locator (page/section/lines),
  - a short excerpt (1–4 sentences),
  - and a confidence suggestion (attested_secondary vs canonical) WITHOUT inventing facts.

Rules:
- If you cannot find evidence from the provided excerpts or sources, say "NO EVIDENCE FOUND" for that row.
- Do not hallucinate citations.

Rows:
{ev_rows_txt}
"""

    # Prompt 2: “to_id completion” (structural completion, low risk)
    to_rows_txt = "\n".join(
        [f"- {fname} | {r.get('from_id','')} | {r.get('relation','')} | to_id: (missing)" for fname, r in missing_to_all]
    ) or "(none)"
    p2 = f"""You are helping me fill missing `to_id` targets in a Vedic knowledge schema.

Task:
- For each row below, suggest a plausible `to_id` in the format type:slug.
- Mark each suggestion as:
  - HIGH (common/standard mapping),
  - MED (plausible but tradition-dependent),
  - LOW (speculative; keep in overlay only).
- Do NOT present LOW items as fact.

Rows:
{to_rows_txt}
"""

    # Prompt 3: “Schema refinement” (keeps system clean, not bogged down)
    p3 = """You are helping refine an ontology-driven Vedic knowledge database.

Task:
- Propose improvements to keep the system maintainable:
  1) Which relations should remain canonical-only (require evidence) vs overlay (model_layered)?
  2) Which entity types should be merged or separated (deity vs devi vs nitya_devi)?
  3) Identify 5–10 constraints that prevent nonsense edges.

Output:
- A concise list of recommended constraints + a JSON/YAML sketch of ontology changes.
"""

    # Prompt 4: “Manifest curation” (wget list growth)
    p4 = """You are helping curate public-domain / permissively-licensed source URLs for corpus growth.

Task:
- Provide 10–30 stable URLs (or source landing pages) for ONE domain:
  - nakshatra OR tithi_nitya OR ritual OR music OR plants
- Prefer: GRETIL / archive.org public domain scans / institutional repositories.
- Avoid copyrighted paywalled sources.
- Return a plain list suitable for a wget manifest (one URL per line).
"""

    content = header + "\n"
    content += mk_block("Prompt A — Evidence fill (missing evidence)", p1, "text")
    content += mk_block("Prompt B — Fill to_id (missing targets)", p2, "text")
    content += mk_block("Prompt C — Ontology constraints (keep it clean)", p3, "text")
    content += mk_block("Prompt D — Wget manifest curation (source growth)", p4, "text")
    return content

def main():
    md = build_prompt_bundle()
    PROMPTS_MD.write_text(md, encoding="utf-8")
    print(str(PROMPTS_MD))

if __name__ == "__main__":
    main()
