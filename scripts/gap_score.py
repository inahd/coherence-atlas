import csv, json, time
from pathlib import Path

BASE = Path("/opt/atlas")
SCHEMA = BASE / "schemas" / "atlas_projection.json"
DATASETS = BASE / "datasets"
REPORTS = BASE / "memory" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

REL_FILES = {
    "nakshatra_deity": DATASETS / "relations_nakshatra_deity.csv",
    "devi_weapon": DATASETS / "relations_devi_weapon.csv",
    "nakshatra_plants": DATASETS / "relations_nakshatra_plants.csv",
    "ritual_calendar": DATASETS / "relations_ritual_calendar.csv",
    "raga_ritual": DATASETS / "relations_raga_ritual.csv",
    "nakshatra_graha": DATASETS / "relations_nakshatra_graha.csv",
}

EVID_KEYS = ["source_title","source_locator","excerpt"]

def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def evidence_ok(r):
    return all((r.get(k) or "").strip() for k in EVID_KEYS)

def safe_load_projection():
    if not SCHEMA.exists():
        # Minimal fallback if schema absent
        return {
            "targets": {
                "jyotish": {"relations": {"nakshatra_associated_deity": 27, "nakshatra_ruling_graha": 27}},
                "deity_iconography": {"relations": {"devi_wields_weapon": 80}},
                "plants_materia": {"relations": {"plant_used_in_ritual": 200, "plant_sacred_to_deity": 200}},
                "ritual_calendar": {"relations": {"ritual_prescribed_on": 120}},
                "music": {"relations": {"ritual_uses_raga": 50}}
            }
        }
    return json.loads(SCHEMA.read_text(encoding="utf-8"))

def compute_counts():
    out = {}
    for k, p in REL_FILES.items():
        rows = read_csv(p)
        total = len(rows)
        missing_to = sum(1 for r in rows if not (r.get("to_id") or "").strip())
        with_ev = sum(1 for r in rows if evidence_ok(r))
        out[k] = {
            "file": str(p),
            "total_rows": total,
            "missing_to_id": missing_to,
            "with_evidence": with_ev,
            "missing_evidence": total - with_ev
        }
    return out

def score_gaps(counts, projection):
    # Heuristic: prioritize domains with many missing_to_id + missing_evidence.
    # Also prioritize domains that exist in projection targets.
    weights = {
        "nakshatra_deity": 3.0,
        "nakshatra_graha": 2.5,
        "devi_weapon": 2.0,
        "nakshatra_plants": 2.0,
        "ritual_calendar": 1.5,
        "raga_ritual": 1.5,
    }

    scored = []
    for k, c in counts.items():
        w = weights.get(k, 1.0)
        score = w * (c["missing_to_id"] * 2 + c["missing_evidence"] * 1)
        scored.append({
            "bucket": k,
            "score": score,
            **c
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored

def main():
    counts = compute_counts()
    projection = safe_load_projection()
    scored = score_gaps(counts, projection)

    report = {
        "timestamp": int(time.time()),
        "counts": counts,
        "prioritized": scored
    }

    out = REPORTS / "gaps.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Wrote:", out)

    # also write a short text summary
    lines = []
    for s in scored[:10]:
        lines.append(f"{s['bucket']}: score={int(s['score'])} total={s['total_rows']} miss_to={s['missing_to_id']} miss_ev={s['missing_evidence']}")
    (REPORTS / "gaps_top.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote:", REPORTS / "gaps_top.txt")

if __name__ == "__main__":
    main()
