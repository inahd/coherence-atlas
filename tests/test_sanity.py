import json, csv
from pathlib import Path

BASE = Path("/opt/atlas")

def must_exist(p: Path):
    if not p.exists():
        raise SystemExit(f"Missing required path: {p}")

def test_files():
    must_exist(BASE/"datasets")
    must_exist(BASE/"memory")
    must_exist(BASE/"scripts")
    # relation csv headers sanity
    rel = BASE/"datasets"/"relations_nakshatra_deity.csv"
    must_exist(rel)
    with rel.open(newline="", encoding="utf-8") as f:
        rdr = csv.reader(f)
        hdr = next(rdr)
        required = {"from_id","relation","to_id","source_title","source_locator","excerpt","tradition","confidence","notes"}
        if not required.issubset(set(hdr)):
            raise SystemExit(f"Bad header in {rel}: {hdr}")

def test_seed_graph_if_present():
    p = BASE/"memory"/"graphs"/"seed_graph.json"
    if not p.exists():
        return
    d = json.loads(p.read_text(encoding="utf-8"))
    assert "nodes" in d and "links" in d
    assert isinstance(d["nodes"], list) and isinstance(d["links"], list)

def main():
    test_files()
    test_seed_graph_if_present()
    print("OK: sanity")

if __name__ == "__main__":
    main()
