import csv, glob, os
from pathlib import Path

BASE=Path('/opt/atlas')
DS=BASE/'datasets'
AUTO=DS/'relations_auto'/'relations_auto.csv'
OUT=DS/'relations_inbox.csv'

HDR=['from_id','relation','to_id','source_title','source_locator','excerpt','tradition','confidence','notes']

# seed relations (exclude resolved and candidates/inbox)
seed_files=[p for p in DS.glob('relations_*.csv') if not p.name.startswith('relations_resolved_') and p.name not in ('relations_candidates.csv','relations_inbox.csv')]

rows=[]

def read(p:Path):
  if not p.exists():
    return 0
  n=0
  with p.open(newline='',encoding='utf-8',errors='ignore') as f:
    r=csv.DictReader(f)
    for row in r:
      rr={k:(row.get(k,'') or '') for k in HDR}
      if rr['from_id'] and rr['relation']:
        rows.append(rr)
        n += 1
  return n

def main():
  total=0
  for f in seed_files:
    total += read(f)

  if AUTO.exists():
    total += read(AUTO)

  # dedupe
  seen=set(); out=[]
  for r in rows:
    key=(r['from_id'], r['relation'], r['to_id'], r['source_locator'])
    if key in seen: continue
    seen.add(key)
    out.append(r)

  OUT.write_text('')
  with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=HDR)
    w.writeheader()
    for r in out:
      w.writerow(r)

  print('seed_files=', len(seed_files))
  print('wrote=', len(out), '->', OUT)

if __name__=='__main__':
  main()
