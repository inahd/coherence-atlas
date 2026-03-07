import csv, os
from pathlib import Path

BASE=Path('/opt/atlas')
DS=BASE/'datasets'
INBOX=DS/'relations_inbox.csv'

OUT_CANON=DS/'relations_resolved_canon.csv'
OUT_INF=DS/'relations_resolved_inference.csv'
OUT_OVR=DS/'relations_resolved_overlays.csv'

# Standard-ish header (extra columns are fine)
HDR=['from_id','relation','to_id','source_title','source_locator','excerpt','tradition','confidence','notes']

CANON_OK=set(['canonical','attested_primary','attested_secondary'])

def read_rows(p:Path):
  if not p.exists():
    return []
  with p.open(newline='',encoding='utf-8',errors='ignore') as f:
    r=csv.DictReader(f)
    rows=[]
    for row in r:
      rr={k:(row.get(k,'') or '') for k in HDR}
      if rr['from_id'] and rr['relation']:
        rows.append(rr)
    return rows

def write_rows(p:Path, rows):
  p.parent.mkdir(parents=True, exist_ok=True)
  with p.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=HDR)
    w.writeheader()
    for r in rows:
      w.writerow({k:r.get(k,'') for k in HDR})


def main():
  if not INBOX.exists():
    raise SystemExit('Missing: '+str(INBOX)+' (run ingest_relations_auto.py first)')

  rows=read_rows(INBOX)

  canon=[]
  inf=[]
  ovr=[]

  for r in rows:
    conf=(r.get('confidence') or '').strip()
    has_ev = bool((r.get('source_locator') or '').strip()) and bool((r.get('excerpt') or '').strip())

    # strict canon: only if explicitly marked + evidence present
    if conf in CANON_OK and has_ev:
      canon.append(r)
      continue

    # safe-aggressive: inference grows fast, but labeled
    if conf == 'inferred_coherent':
      inf.append(r)
    else:
      ovr.append(r)

  write_rows(OUT_CANON, canon)
  write_rows(OUT_INF, inf)
  write_rows(OUT_OVR, ovr)

  print('canon_rows=', len(canon))
  print('inference_rows=', len(inf))
  print('overlays_rows=', len(ovr))
  print('wrote:', OUT_CANON)
  print('wrote:', OUT_INF)
  print('wrote:', OUT_OVR)

if __name__=='__main__':
  main()
