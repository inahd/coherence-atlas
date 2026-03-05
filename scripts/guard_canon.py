import csv, json, re, sys
from pathlib import Path
from collections import defaultdict

BASE = Path("/opt/atlas")
ONTO = json.loads((BASE/"schemas/ontology.json").read_text(encoding="utf-8"))
TRAD = json.loads((BASE/"schemas/traditions.json").read_text(encoding="utf-8"))

CANON_DIR = BASE/"datasets/relations"
REPORT = BASE/"memory/reports/canon_guard.json"

EVID = ONTO["evidence_required"]
CONF_OK = set(ONTO["confidence_allowed"])
PROFILES = {p["name"] for p in TRAD["profiles"]}

REL_RULES = {r["name"]: r for r in ONTO["relations"]}
TYPESET = set(ONTO["types"])

ID_RE = re.compile(r"^[a-z_]+:[a-z0-9_]+$|^[a-z_]+:\d+$")

def type_of(_id: str) -> str:
    return _id.split(":",1)[0] if ":" in _id else "unknown"

def read_csv(p: Path):
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    problems = []
    totals = {"files":0,"rows":0}
    rel_counts = defaultdict(int)

    for f in sorted(CANON_DIR.glob("*.csv")):
        rows = read_csv(f)
        if not rows:
            continue
        totals["files"] += 1

        for r in rows:
            totals["rows"] += 1
            from_id = (r.get("from_id") or "").strip()
            to_id   = (r.get("to_id") or "").strip()
            rel     = (r.get("relation") or "").strip()
            trad    = (r.get("tradition") or "").strip() or "unknown"
            conf    = (r.get("confidence") or "").strip() or "unknown"

            # ID format
            if not (from_id and to_id and rel):
                problems.append({"file":f.name,"issue":"missing core fields","row":r})
                continue
            if not ID_RE.match(from_id):
                problems.append({"file":f.name,"issue":"bad from_id format","from_id":from_id})
            if not ID_RE.match(to_id):
                problems.append({"file":f.name,"issue":"bad to_id format","to_id":to_id})

            # relation allowed
            if rel not in REL_RULES:
                problems.append({"file":f.name,"issue":"unknown relation","relation":rel})
            else:
                rule = REL_RULES[rel]
                ft = type_of(from_id); tt = type_of(to_id)
                if ft != rule["from"]:
                    problems.append({"file":f.name,"issue":"wrong from type","relation":rel,"from_type":ft,"expected":rule["from"]})
                if tt not in rule["to"]:
                    problems.append({"file":f.name,"issue":"wrong to type","relation":rel,"to_type":tt,"allowed":rule["to"]})

            # evidence required for canonical-ish rows
            ev_ok = all((r.get(k) or "").strip() for k in EVID)
            if not ev_ok:
                problems.append({"file":f.name,"issue":"missing evidence","relation":rel,"from_id":from_id,"to_id":to_id})

            # tradition profile
            if trad not in PROFILES:
                problems.append({"file":f.name,"issue":"unknown tradition profile","tradition":trad,"from_id":from_id})

            # confidence
            if conf not in CONF_OK:
                problems.append({"file":f.name,"issue":"unknown confidence","confidence":conf,"from_id":from_id})

            rel_counts[rel] += 1

    report = {"totals":totals,"relation_counts":dict(rel_counts),"problems":problems[:500]}
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Wrote:", REPORT)
    print("Rows scanned:", totals["rows"], "Problems:", len(problems))

    # Exit non-zero if problems found (promotion gate)
    if problems:
        sys.exit(2)

if __name__ == "__main__":
    main()
