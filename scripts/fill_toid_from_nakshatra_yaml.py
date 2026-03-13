import csv, re
from pathlib import Path
import yaml

DS = Path("/opt/atlas/datasets")
NAK_LIST = DS/"nakshatra_list.csv"
NAK_YAML = DS/"nakshatra.yaml"

REL_DEITY = DS/"relations_nakshatra_deity.csv"
REL_GRAHA = DS/"relations_nakshatra_graha.csv"

HDR = ["from_id","relation","to_id","source_title","source_locator","excerpt","tradition","confidence","notes"]

def read_csv(p):
    if not p.exists(): return []
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(p, rows):
    with p.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=HDR)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k,"") for k in HDR})

def slug(s):
    s=(s or "").strip().lower()
    s=re.sub(r"[^a-z0-9]+","_",s)
    s=re.sub(r"_+","_",s).strip("_")
    return s or "unknown"

def norm_key(name):
    return re.sub(r"[^A-Za-z0-9]","",name or "")

def main():
    if not (NAK_LIST.exists() and NAK_YAML.exists()):
        print("Missing nakshatra_list.csv or nakshatra.yaml")
        return

    id_to_name={}
    for r in read_csv(NAK_LIST):
        if r.get("id") and r.get("name"):
            id_to_name[str(r["id"]).strip()] = str(r["name"]).strip()

    ny = yaml.safe_load(NAK_YAML.read_text(encoding="utf-8", errors="ignore"))
    if not isinstance(ny, dict):
        print("nakshatra.yaml not dict")
        return

    name_to_deity={}
    name_to_ruler={}
    for k,v in ny.items():
        if isinstance(v, dict):
            if v.get("deity"): name_to_deity[norm_key(k)] = str(v["deity"]).strip()
            if v.get("ruler"): name_to_ruler[norm_key(k)] = str(v["ruler"]).strip()

    # fill deity file
    rows = read_csv(REL_DEITY)
    changed=0
    for r in rows:
        if (r.get("relation") or "").strip() != "nakshatra_associated_deity":
            continue
        if (r.get("to_id") or "").strip():
            continue
        src=(r.get("from_id") or "").strip()
        if not src.startswith("nakshatra:"): continue
        nid=src.split(":",1)[1]
        nm=id_to_name.get(nid)
        if not nm: continue
        deity=name_to_deity.get(norm_key(nm))
        if not deity: continue
        r["to_id"]=f"deity:{slug(deity)}"
        r["confidence"]= (r.get("confidence") or "seed_unverified") or "seed_unverified"
        r["notes"]=(r.get("notes") or "" + " | TOID: nakshatra.yaml deity").strip(" |")
        changed += 1
    write_csv(REL_DEITY, rows)

    # create/populate graha file
    if not REL_GRAHA.exists():
        write_csv(REL_GRAHA, [])

    g = read_csv(REL_GRAHA)
    existing={(r.get("from_id",""), r.get("relation","")) for r in g}
    added=0
    for nid,nm in id_to_name.items():
        src=f"nakshatra:{nid}"
        rel="nakshatra_ruling_graha"
        if (src,rel) in existing:
            continue
        ruler=name_to_ruler.get(norm_key(nm))
        if not ruler:
            continue
        g.append({
            "from_id": src,
            "relation": rel,
            "to_id": f"graha:{slug(ruler)}",
            "source_title": "",
            "source_locator": "",
            "excerpt": "",
            "tradition": "unknown",
            "confidence": "seed_unverified",
            "notes": "TOID: nakshatra.yaml ruler"
        })
        added += 1
    write_csv(REL_GRAHA, g)

    print("filled deity to_id:", changed, "added graha rows:", added)

if __name__ == "__main__":
    main()
