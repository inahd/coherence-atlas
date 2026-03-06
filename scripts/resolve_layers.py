import csv, json, time
from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict

BASE = Path('/opt/atlas')
DS = BASE/'datasets'
REP = BASE/'memory'/'reports'

OUT_CANON = DS/'relations_resolved_canon.csv'
OUT_INF   = DS/'relations_resolved_inference.csv'
OUT_OVR   = DS/'relations_resolved_overlays.csv'
OUT_REP   = REP/'stability_report.json'

EVID = ['source_title','source_locator','excerpt']
HDR = ['from_id','relation','to_id','profile','tradition','confidence','score','source_title','source_locator','excerpt','notes']

# strict canon
CANON_MIN_SCORE = 6.0
CANON_MARGIN = 1.5
CANON_REQUIRE_EVIDENCE = True

# inference (benefit-of-doubt) layer
INF_MIN_SCORE = 3.0
INF_MARGIN = 1.0
INF_CONF = 'inferred_coherent'

def read_csv(p: Path):
    if not p.exists(): return []
    with p.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write_csv(p: Path, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=HDR)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k,'') for k in HDR})

def ev_ok(r: dict) -> bool:
    return all((r.get(k) or '').strip() for k in EVID)

def conf_w(conf: str) -> float:
    conf = (conf or '').strip()
    return {
        'canonical': 4.0,
        'attested_secondary': 2.5,
        'auto_proposed': 1.0,
        'seed_unverified': 0.3,
        'inferred_coherent': 0.0,
    }.get(conf, 0.0)

def score(r: dict) -> float:
    s = 0.0
    if ev_ok(r): s += 3.0
    s += conf_w(r.get('confidence',''))
    trad = (r.get('tradition') or '').strip().lower()
    if trad and trad != 'unknown': s += 0.2
    return s

@dataclass
class Cand:
    to_id: str
    s: float
    ev: bool
    tradition: str
    confidence: str
    source_title: str
    source_locator: str
    excerpt: str
    notes: str

def iter_relation_files():
    # pull all datasets/relations_*.csv (exclude resolved outputs)
    for p in DS.glob('relations_*.csv'):
        if p.name.startswith('relations_resolved_'):
            continue
        yield p

def main():
    clusters = defaultdict(list)
    scanned = 0
    used = []

    for p in iter_relation_files():
        rows = read_csv(p)
        if not rows: 
            continue
        used.append(p.name)
        for r in rows:
            scanned += 1
            fr = (r.get('from_id') or '').strip()
            rel = (r.get('relation') or '').strip()
            to  = (r.get('to_id') or '').strip()
            if not (fr and rel and to):
                continue
            clusters[(fr, rel)].append(Cand(
                to_id=to,
                s=score(r),
                ev=ev_ok(r),
                tradition=((r.get('tradition') or 'unknown').strip() or 'unknown'),
                confidence=((r.get('confidence') or 'seed_unverified').strip() or 'seed_unverified'),
                source_title=(r.get('source_title') or '').strip(),
                source_locator=(r.get('source_locator') or '').strip(),
                excerpt=(r.get('excerpt') or '').strip(),
                notes=(r.get('notes') or '').strip(),
            ))

    canon=[]
    inf=[]
    ovr=[]
    conflicts=[]

    for (fr, rel), cands in clusters.items():
        # dedupe by to_id keeping best score
        best={}
        for c in cands:
            if (c.to_id not in best) or (c.s > best[c.to_id].s):
                best[c.to_id]=c
        ranked=sorted(best.values(), key=lambda x: x.s, reverse=True)
        top=ranked[0]
        runner=ranked[1] if len(ranked)>1 else None

        canon_ok=True
        if CANON_REQUIRE_EVIDENCE and not top.ev: canon_ok=False
        if top.s < CANON_MIN_SCORE: canon_ok=False
        if runner and (top.s-runner.s) < CANON_MARGIN: canon_ok=False

        inf_ok=False
        if not canon_ok:
            inf_ok=True
            if top.s < INF_MIN_SCORE: inf_ok=False
            if runner and (top.s-runner.s) < INF_MARGIN: inf_ok=False

        if canon_ok:
            canon.append({
                'from_id': fr,'relation': rel,'to_id': top.to_id,
                'profile': 'canon','tradition': 'canon',
                'confidence': 'canonical' if top.confidence in ('canonical','attested_secondary') else 'attested_secondary',
                'score': f'{top.s:.2f}',
                'source_title': top.source_title,'source_locator': top.source_locator,'excerpt': top.excerpt[:900],
                'notes': ('CANON | ' + (top.notes or '')).strip(' |')
            })
        elif inf_ok:
            inf.append({
                'from_id': fr,'relation': rel,'to_id': top.to_id,
                'profile': 'inference','tradition': top.tradition or 'unknown',
                'confidence': INF_CONF,'score': f'{top.s:.2f}',
                'source_title': top.source_title,'source_locator': top.source_locator,'excerpt': top.excerpt[:900],
                'notes': ('INFERRED (coherent; needs evidence to canonize) | ' + (top.notes or '')).strip(' |')
            })
        else:
            conflicts.append({
                'from_id': fr,'relation': rel,
                'top': {'to_id': top.to_id,'score': top.s,'evidence': top.ev,'confidence': top.confidence},
                'runnerup': None if not runner else {'to_id': runner.to_id,'score': runner.s,'evidence': runner.ev,'confidence': runner.confidence}
            })

        for c in ranked:
            ovr.append({
                'from_id': fr,'relation': rel,'to_id': c.to_id,
                'profile': 'overlay','tradition': c.tradition or 'unknown',
                'confidence': c.confidence,'score': f'{c.s:.2f}',
                'source_title': c.source_title,'source_locator': c.source_locator,'excerpt': c.excerpt[:900],
                'notes': ('OVERLAY | ' + (c.notes or '')).strip(' |')
            })

    write_csv(OUT_CANON, canon)
    write_csv(OUT_INF, inf)
    write_csv(OUT_OVR, ovr)

    OUT_REP.write_text(json.dumps({
        'generated': int(time.time()),
        'scanned_rows': scanned,
        'clusters': len(clusters),
        'canon_edges': len(canon),
        'inference_edges': len(inf),
        'overlay_edges': len(ovr),
        'unsettled_clusters': len(conflicts),
        'used_relation_files': used,
        'conflicts_sample': conflicts[:60],
        'config': {
            'canon_min_score': CANON_MIN_SCORE,
            'canon_margin': CANON_MARGIN,
            'canon_require_evidence': CANON_REQUIRE_EVIDENCE,
            'inf_min_score': INF_MIN_SCORE,
            'inf_margin': INF_MARGIN,
            'inf_confidence': INF_CONF
        }
    }, indent=2), encoding='utf-8')

    print('canon_edges:', len(canon))
    print('inference_edges:', len(inf))
    print('overlay_edges:', len(ovr))
    print('report:', OUT_REP)

if __name__=='__main__':
    main()
