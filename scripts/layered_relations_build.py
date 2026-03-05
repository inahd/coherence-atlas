import csv, re, json, time
from pathlib import Path
import yaml

BASE = Path("/opt/atlas")
DS = BASE/"datasets"
OUT = DS/"overlays"/"relations_layered.csv"
GRAPH = BASE/"memory"/"graphs"/"layered_graph.json"

OUT.parent.mkdir(parents=True, exist_ok=True)
GRAPH.parent.mkdir(parents=True, exist_ok=True)

HDR = ["from_id","relation","to_id","layer","confidence","notes"]

def slug(s: str) -> str:
    s=(s or "").strip().lower()
    s=re.sub(r"[^a-z0-9]+","_",s)
    s=re.sub(r"_+","_",s).strip("_")
    return s or "unknown"

def norm_key(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]","",name or "")

def read_csv(path: Path):
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=HDR)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k,"") for k in HDR})

def load_yaml(p: Path):
    if not p.exists(): return None
    return yaml.safe_load(p.read_text(encoding="utf-8", errors="ignore"))

def build():
    rows=[]

    # --- Core structural dimensions ---
    # Tithi list provides names; we compute paksha + index deterministically.
    tithi_list = DS/"tithi_list.csv"
    if tithi_list.exists():
        trows = read_csv(tithi_list)
        # If file contains 30 tithis, we assume order 1..30
        # if it contains named 15, we still map those to a single paksha unknown.
        for i, r in enumerate(trows, start=1):
            tid = f"tithi:{i}"
            paksha = "shukla" if i <= 15 else "krishna"
            idx = i if i <= 15 else i-15
            rows.append({"from_id": tid, "relation": "tithi_in_paksha", "to_id": f"paksha:{paksha}",
                         "layer": "structure", "confidence": "model_layered",
                         "notes": f"derived paksha from position {i}"})
            rows.append({"from_id": tid, "relation": "tithi_index_in_paksha", "to_id": f"tithi_index:{idx}",
                         "layer": "structure", "confidence": "model_layered",
                         "notes": f"derived index {idx} from position {i}"})

    # Nakshatra list: generate nakshatra:1..27 (or use existing ids), and padas 1..4
    nak_list = DS/"nakshatra_list.csv"
    if nak_list.exists():
        nrows = read_csv(nak_list)
        for i, r in enumerate(nrows, start=1):
            # prefer the csv id if present; otherwise use i
            nid = (r.get("id") or str(i)).strip()
            n_from = f"nakshatra:{nid}"
            for p in range(1,5):
                pada_id = f"pada:{p}"
                np_id = f"nakshatra_pada:{nid}_{p}"  # 27*4=108 derived
                rows.append({"from_id": n_from, "relation": "nakshatra_has_pada", "to_id": pada_id,
                             "layer": "structure", "confidence": "model_layered",
                             "notes": "derived: 4 padas per nakshatra"})
                rows.append({"from_id": n_from, "relation": "nakshatra_pada_entity", "to_id": np_id,
                             "layer": "derived_set", "confidence": "model_layered",
                             "notes": "derived: nakshatra×pada (108) carrier node"})

    # --- Mappings from your existing structured sources (still model_layered here) ---
    # nakshatra.yaml has deity/ruler keyed by name (Ashwini, Rohini, etc.)
    nak_yaml = DS/"nakshatra.yaml"
    if nak_yaml.exists() and nak_list.exists():
        ny = load_yaml(nak_yaml)
        # id -> name
        id_to_name={}
        for r in read_csv(nak_list):
            if (r.get("id") or "").strip() and (r.get("name") or "").strip():
                id_to_name[str(r["id"]).strip()] = str(r["name"]).strip()

        if isinstance(ny, dict):
            # nameKey -> deity/ruler
            name_to_deity={}
            name_to_ruler={}
            for k,v in ny.items():
                if isinstance(v, dict):
                    if v.get("deity"): name_to_deity[norm_key(k)] = str(v["deity"]).strip()
                    if v.get("ruler"): name_to_ruler[norm_key(k)] = str(v["ruler"]).strip()

            for nid, nm in id_to_name.items():
                key = norm_key(nm)
                deity = name_to_deity.get(key)
                ruler = name_to_ruler.get(key)
                if deity:
                    rows.append({"from_id": f"nakshatra:{nid}", "relation": "nakshatra_associated_deity",
                                 "to_id": f"deity:{slug(deity)}", "layer": "jyotisha",
                                 "confidence": "model_layered", "notes": "from nakshatra.yaml deity"})
                if ruler:
                    rows.append({"from_id": f"nakshatra:{nid}", "relation": "nakshatra_ruling_graha",
                                 "to_id": f"graha:{slug(ruler)}", "layer": "jyotisha",
                                 "confidence": "model_layered", "notes": "from nakshatra.yaml ruler"})

    # tithi -> nitya_devi mapping (if your mapping csv exists)
    # expected: nitya_devi_mapping.csv has columns tithi_id, devi_name OR similar
    # We'll attempt several columns.
    mapping = DS/"nitya_devi_mapping.csv"
    if mapping.exists():
        mrows = read_csv(mapping)
        for r in mrows:
            # try common column guesses
            tid = (r.get("tithi_id") or r.get("tithi") or r.get("id") or "").strip()
            dnm = (r.get("nitya_devi") or r.get("devi") or r.get("name") or "").strip()
            if not (tid and dnm):
                continue
            # allow "1" or "tithi:1" style
            if tid.isdigit():
                from_id = f"tithi:{tid}"
            else:
                from_id = tid
            rows.append({"from_id": from_id, "relation": "tithi_associated_nitya_devi",
                         "to_id": f"nitya_devi:{slug(dnm)}", "layer": "tantra_time",
                         "confidence": "model_layered", "notes": "from nitya_devi_mapping.csv"})

    # --- Heuristic “general Vedic” bridges (quarantined; optional) ---
    # Example: connect deity<->graha co-mentions if names overlap by known list (tiny default)
    # Keep VERY conservative and mark "heuristic".
    heur_pairs = [
        ("deity:surya","graha:surya"),
        ("deity:chandra","graha:chandra"),
    ]
    for a,b in heur_pairs:
        rows.append({"from_id": a, "relation": "identity_bridge", "to_id": b,
                     "layer": "heuristic", "confidence": "model_layered",
                     "notes": "very conservative identity bridge"})

    # Deduplicate
    seen=set()
    uniq=[]
    for r in rows:
        key=(r["from_id"], r["relation"], r["to_id"], r["layer"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(r)

    write_csv(OUT, uniq)
    return uniq

def build_graph(rows):
    nodes={}
    links=[]
    def add_node(i):
        if i not in nodes:
            t = i.split(":",1)[0] if ":" in i else "unknown"
            nodes[i]={"id":i,"type":t,"name":i}
    for r in rows:
        add_node(r["from_id"]); add_node(r["to_id"])
        links.append({
            "source": r["from_id"],
            "target": r["to_id"],
            "relation": r["relation"],
            "layer": r["layer"],
            "confidence": r["confidence"]
        })
    GRAPH.write_text(json.dumps({"nodes": list(nodes.values()), "links": links, "timestamp": int(time.time())}, indent=2),
                     encoding="utf-8")

def main():
    rows = build()
    build_graph(rows)
    print("Wrote overlay relations:", OUT, "rows:", len(rows))
    print("Wrote overlay graph:", GRAPH)

if __name__ == "__main__":
    main()
