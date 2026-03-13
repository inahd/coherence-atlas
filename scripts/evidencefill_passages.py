import csv, re
from pathlib import Path

BASE=Path('/opt/atlas')
DS=BASE/'datasets'
PASS=DS/'sources/passages.csv'

REL_FILES=[
  DS/'relations_nakshatra_deity.csv',
  DS/'relations_nakshatra_plants.csv',
  DS/'relations_devi_weapon.csv',
  DS/'relations_ritual_calendar.csv',
  DS/'relations_raga_ritual.csv',
]

def typ(_id:str)->str:
  return (_id.split(':',1)[0] if ':' in (_id or '') else 'unknown').strip().lower()

def label(_id:str)->str:
  if not _id: return ''
  if ':' in _id:
    return _id.split(':',1)[1].replace('_',' ').lower()
  return _id.lower()

def read_csv(p:Path):
  if not p.exists(): return []
  with p.open(newline='', encoding='utf-8', errors='ignore') as f:
    return list(csv.DictReader(f))

def write_csv(p:Path, rows):
  if not rows: return
  hdr=list(rows[0].keys())
  with p.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=hdr)
    w.writeheader()
    for r in rows: w.writerow(r)

def main():
  if not PASS.exists():
    print('Missing passages:', PASS); return
  passages=[]
  with PASS.open(newline='', encoding='utf-8', errors='ignore') as f:
    for r in csv.DictReader(f):
      ex=(r.get('excerpt') or r.get('text') or '').strip()
      if not ex: 
        continue
      passages.append({
        'locator': (r.get('locator') or r.get('passage_id') or '').strip(),
        'excerpt': ex.replace('\n',' ')[:900],
      })

  updated=0
  scanned=0

  for relp in REL_FILES:
    if not relp.exists():
      continue
    rows=read_csv(relp)
    changed=0
    for r in rows:
      scanned += 1
      # only fill if evidence missing
      if (r.get('source_locator') or '').strip() and (r.get('excerpt') or '').strip():
        continue

      fr=(r.get('from_id') or '').strip()
      to=(r.get('to_id') or '').strip()

      # if to_id missing, can't match
      if not fr or not to:
        continue

      a=label(fr)
      b=label(to)
      if not a:
        continue

      # Find a passage that mentions a (and preferably b)
      found=None
      for p in passages:
        txt=p['excerpt'].lower()
        if a in txt and (not b or b in txt):
          found=p; break
      # fallback: just anchor mention
      if not found:
        for p in passages:
          txt=p['excerpt'].lower()
          if a in txt:
            found=p; break

      if found:
        r['source_title'] = (r.get('source_title') or 'passages.csv')
        r['source_locator'] = (r.get('source_locator') or found['locator'] or 'unknown')
        r['excerpt'] = (r.get('excerpt') or found['excerpt'])
        # do NOT auto-canonize; just attach evidence so you can later promote
        if not (r.get('confidence') or '').strip():
          r['confidence'] = 'seed_unverified'
        note=(r.get('notes') or '')
        if 'AUTO_EVID' not in note:
          r['notes'] = (note + ' | AUTO_EVID: matched passages.csv').strip(' |')
        changed += 1
        updated += 1

    if changed:
      write_csv(relp, rows)
    print(relp.name, 'evidence_added=', changed, 'rows=', len(rows))

  print('TOTAL evidence_added=', updated, 'rows_scanned=', scanned)

if __name__=='__main__':
  main()
