import csv, json, time
from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict

BASE = Path("/opt/atlas")
DS = BASE / "datasets"
OUT_PROTO = DS / "relations_resolved_proto_canon.csv"
OUT_CANON = DS / "relations_resolved_canon.csv"
OUT_OVR   = DS / "relations_resolved_overlays.csv"
REPORT    = BASE / "memory/reports/stability_report.json"

EVID_KEYS = ["source_title","source_locator","excerpt"]
HDR_OUT = ["from_id","relation","to_id","profile","source_title","source_locator","excerpt","confidence","score","notes"]

REL_INPUTS = [
    DS/"relations_nakshatra_deity.csv",
    DS/"relations_devi_weapon.csv",
    DS/"relations_nakshatra_plants.csv",
    DS/"relations_ritual_calendar.csv",
    DS/"relations_raga_ritual.csv",
    DS/"relations_nakshatra_graha.csv",
]

def read_csv(p: Path):
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(p: Path, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HDR_OUT)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in HDR_OUT})

def ev_present(r):
    return all((r.get(k) or "").strip() for k in EVID_KEYS)

def norm_profile(x: str):
    x = (x or "").strip().lower()
    return x if x else "unknown"

def conf_weight(conf: str):
    conf = (conf or "").strip()
    return {
        "canonical": 4.0,
        "attested_secondary": 2.5,
        "auto_proposed": 1.0,
        "seed_unverified": 0.3,
    }.get(conf, 0.0)

def score_row(r):
    s = 0.0
    if ev_present(r):
        s += 3.0
    s += conf_weight(r.get("confidence", ""))
    prof = norm_profile(r.get("tradition", ""))
    if prof != "unknown":
        s += 0.2
    return s, prof

@dataclass
class Cand:
    to_id: str
    profile: str
    score: float
    evidence_ok: bool
    source_title: str
    source_locator: str
    excerpt: str
    confidence: str
    notes: str

def main():
    clusters = defaultdict(list)
    scanned = 0

    for p in REL_INPUTS:
        for r in read_csv(p):
            scanned += 1
            fr = (r.get("from_id") or "").strip()
            rel = (r.get("relation") or "").strip()
            to = (r.get("to_id") or "").strip()
            if not (fr and rel and to):
                continue
            s, prof = score_row(r)
            clusters[(fr, rel)].append(Cand(
                to_id=to,
                profile=prof,
                score=s,
                evidence_ok=ev_present(r),
                source_title=(r.get("source_title") or "").strip(),
                source_locator=(r.get("source_locator") or "").strip(),
                excerpt=(r.get("excerpt") or "").strip(),
                confidence=(r.get("confidence") or "seed_unverified").strip(),
                notes=(r.get("notes") or "").strip(),
            ))

    proto_rows=[]
    canon_rows=[]
    overlay_rows=[]
    conflicts=[]
    unsettled=0

    CANON_MIN_SCORE = 6.0
    CANON_MARGIN = 1.5
    REQUIRE_EVIDENCE = True
    # proto-canon allows missing evidence if coherence/score is strong
    PROTO_ALLOW_MISSING_EVIDENCE = True

    for (fr, rel), cands in clusters.items():
        best={}
        for c in cands:
            k=(c.to_id, c.profile)
            if k not in best or c.score > best[k].score:
                best[k]=c
        cands=list(best.values())
        cands.sort(key=lambda x: x.score, reverse=True)
        top=cands[0]
        runner=cands[1] if len(cands)>1 else None

        canon_ok=True
        if REQUIRE_EVIDENCE and not top.evidence_ok:
            canon_ok=False
        if top.score < CANON_MIN_SCORE:
            canon_ok=False
        if runner and (top.score-runner.score) < CANON_MARGIN:
            canon_ok=False

        if canon_ok:
            # If evidence missing, route to proto-canon instead of strict canon
            if PROTO_ALLOW_MISSING_EVIDENCE and (not top.evidence_ok):
                proto_rows.append({
                    "from_id": fr, "relation": rel, "to_id": top.to_id,
                    "profile": "proto_canon",
                    "source_title": top.source_title,
                    "source_locator": top.source_locator,
                    "excerpt": top.excerpt[:900],
                    "confidence": "attested_secondary" if top.confidence else "seed_unverified",
                    "score": f"{top.score:.2f}",
                    "notes": ("PROTO_CANON (needs evidence) | " + (top.notes or "")).strip(" |")
                })
            else:

                            canon_rows.append({
                "from_id": fr, "relation": rel, "to_id": top.to_id,
                "profile": "canon",
                "source_title": top.source_title,
                "source_locator": top.source_locator,
                "excerpt": top.excerpt[:900],
                "confidence": "canonical" if top.confidence in ("canonical","attested_secondary") else "attested_secondary",
                "score": f"{top.score:.2f}",
                "notes": ("RESOLVED_CANON | " + (top.notes or "")).strip(" |")
            })
        else:
            unsettled += 1
            conflicts.append({
                "from_id": fr, "relation": rel,
                "reason": "insufficient evidence/score or too-close runner-up",
                "top": {"to_id": top.to_id, "score": top.score, "profile": top.profile, "evidence": top.evidence_ok, "confidence": top.confidence},
                "runnerup": None if not runner else {"to_id": runner.to_id, "score": runner.score, "profile": runner.profile, "evidence": runner.evidence_ok, "confidence": runner.confidence},
            })

        for c in cands:
            overlay_rows.append({
                "from_id": fr, "relation": rel, "to_id": c.to_id,
                "profile": c.profile,
                "source_title": c.source_title,
                "source_locator": c.source_locator,
                "excerpt": c.excerpt[:900],
                "confidence": c.confidence,
                "score": f"{c.score:.2f}",
                "notes": ("OVERLAY | " + (c.notes or "")).strip(" |")
            })

    write_csv(OUT_PROTO, proto_rows)
    write_csv(OUT_CANON, canon_rows)
    write_csv(OUT_OVR, overlay_rows)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps({
        "generated": int(time.time()),
        "scanned_rows": scanned,
        "clusters": len(clusters),
        "canon_edges": len(canon_rows),
        "overlay_edges": len(overlay_rows),
        "unsettled_clusters": unsettled,
        "conflicts_sample": conflicts[:50],
        "config": {"canon_min_score": CANON_MIN_SCORE, "canon_margin": CANON_MARGIN, "require_evidence": REQUIRE_EVIDENCE}
    }, indent=2), encoding="utf-8")

    print("canon_edges:", len(canon_rows))
    print("overlay_edges:", len(overlay_rows))
    print("report:", REPORT)

if __name__ == "__main__":
    main()
