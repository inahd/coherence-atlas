import csv, json, re, time
from pathlib import Path
from collections import defaultdict

BASE = Path("/opt/atlas")
DS = BASE/"datasets"
OUT_DIR = DS/"relations_strict"
OUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT = BASE/"memory/reports/quality_report.json"
CANON_GRAPH = BASE/"memory/graphs/canonical_graph.json"

EVID = ["source_title","source_locator","excerpt"]
CONF_OK = {"attested_secondary","canonical","regional_tradition"}

REL_INPUTS = [
    DS/"relations_nakshatra_deity.csv",
    DS/"relations_devi_weapon.csv",
    DS/"relations_nakshatra_plants.csv",
    DS/"relations_ritual_calendar.csv",
    DS/"relations_raga_ritual.csv",
    DS/"relations_nakshatra_graha.csv",
    DS/"relations"/"nakshatra__deity.csv",
    DS/"relations"/"tithi__nitya_devi.csv",
]

HDR = ["from_id","relation","to_id","source_title","source_locator","excerpt","tradition","confidence","notes"]
ID_RE = re.compile(r"^[a-z_]+:[a-z0-9_]+$|^[a-z_]+:\d+$")

def read_csv(p: Path):
    if not p.exists(): return []
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(p: Path, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=HDR)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k,"") for k in HDR})

def evidence_ok(r):
    return all((r.get(k) or "").strip() for k in EVID)

def confidence_ok(r):
    return (r.get("confidence") or "").strip() in CONF_OK

def core_ok(r):
    a=(r.get("from_id") or "").strip()
    b=(r.get("to_id") or "").strip()
    rel=(r.get("relation") or "").strip()
    return bool(a and b and rel)

def id_ok(_id):
    return bool(ID_RE.match((_id or "").strip()))

def main():
    kept=[]
    dropped=defaultdict(int)
    by_rel=defaultdict(int)

    for p in REL_INPUTS:
        for r in read_csv(p):
            if not core_ok(r):
                dropped["missing_core"] += 1; continue
            if not id_ok(r["from_id"]) or not id_ok(r["to_id"]):
                dropped["bad_id_format"] += 1; continue
            if not evidence_ok(r):
                dropped["missing_evidence"] += 1; continue
            if not confidence_ok(r):
                dropped["low_confidence"] += 1; continue
            kept.append(r)
            by_rel[r["relation"]] += 1

    # write strict relations split by relation
    per_rel=defaultdict(list)
    for r in kept:
        per_rel[r["relation"]].append(r)

    strict_files=[]
    for rel, rows in per_rel.items():
        out = OUT_DIR / f"{rel.replace(':','_')}.csv"
        write_csv(out, rows)
        strict_files.append(str(out))

    # graph
    nodes={}
    links=[]
    def add_node(i):
        if i not in nodes:
            t = i.split(":",1)[0] if ":" in i else "unknown"
            nodes[i]={"id":i,"type":t,"name":i}

    for r in kept:
        add_node(r["from_id"]); add_node(r["to_id"])
        links.append({
            "source": r["from_id"],
            "target": r["to_id"],
            "relation": r["relation"],
            "confidence": r.get("confidence",""),
            "evidence": {k: r.get(k,"") for k in EVID},
        })

    CANON_GRAPH.parent.mkdir(parents=True, exist_ok=True)
    CANON_GRAPH.write_text(json.dumps({"nodes": list(nodes.values()), "links": links}, indent=2), encoding="utf-8")

    report = {
        "timestamp": int(time.time()),
        "kept_rows": len(kept),
        "dropped": dict(dropped),
        "by_relation": dict(sorted(by_rel.items(), key=lambda x: x[1], reverse=True)),
        "strict_files": strict_files,
        "canonical_graph": str(CANON_GRAPH),
        "graph_nodes": len(nodes),
        "graph_links": len(links),
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("STRICT kept_rows:", len(kept))
    print("Dropped:", dict(dropped))
    print("Graph nodes:", len(nodes), "links:", len(links))
    print("Report:", REPORT)

if __name__ == "__main__":
    main()
