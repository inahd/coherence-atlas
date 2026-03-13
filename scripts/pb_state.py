import csv, json, os, time
from pathlib import Path

BASE=Path('/opt/atlas')
RPT=BASE/'memory/reports'
STATE=RPT/'pb_state.json'

FILES={
  'auto':'/opt/atlas/datasets/relations_auto/relations_auto.csv',
  'canon':'/opt/atlas/datasets/relations_resolved_canon.csv',
  'inference':'/opt/atlas/datasets/relations_resolved_inference.csv',
  'overlays':'/opt/atlas/datasets/relations_resolved_overlays.csv',
  'passages':'/opt/atlas/datasets/sources/passages.csv',
}

def count_csv(p):
  if not os.path.exists(p): return 0
  with open(p,newline='',encoding='utf-8',errors='ignore') as f:
    return sum(1 for _ in csv.DictReader(f))

def main():
  d={'ts':int(time.time()), 'paths':FILES, 'counts':{k:count_csv(v) for k,v in FILES.items()}}
  # last cycle log tail if present
  cycle_log=os.path.expanduser('~/.local/state/atlas/atlas-cycle.log')
  if os.path.exists(cycle_log):
    with open(cycle_log,encoding='utf-8',errors='ignore') as f:
      d['cycle_log_tail']=''.join(f.readlines()[-40:])
  else:
    d['cycle_log_tail']=''

  RPT.mkdir(parents=True, exist_ok=True)
  STATE.write_text(json.dumps(d, indent=2), encoding='utf-8')
  print('WROTE', STATE)
  print(json.dumps(d['counts'], indent=2))

if __name__=='__main__':
  main()
