import csv, re
from pathlib import Path
import yaml

BASE=Path('/opt/atlas')
DS=BASE/'datasets'

REL_FILES=[
  DS/'relations_nakshatra_deity.csv',
  DS/'relations_nakshatra_plants.csv',
  DS/'relations_devi_weapon.csv',
]

NAK_YAML=DS/'nakshatra.yaml'
DEITIES_YAML=DS/'deities.yaml'

def slug(s:str)->str:
  s=(s or '').strip().lower()
  s=re.sub(r'[^a-z0-9]+','_',s).strip('_')
  return s

def load_yaml(p:Path):
  if not p.exists(): return None
  return yaml.safe_load(p.read_text(encoding='utf-8', errors='ignore'))

def read_csv(p:Path):
  if not p.exists(): return []
  with p.open(newline='', encoding='utf-8') as f:
    return list(csv.DictReader(f))

def write_csv(p:Path, rows):
  if not rows: return
  hdr=list(rows[0].keys())
  with p.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=hdr)
    w.writeheader()
    for r in rows: w.writerow(r)

def build_nak_maps():
  obj=load_yaml(NAK_YAML)
  # expected structure: {Ashwini:{deity:..., plant:...}, ...} or list
  name_by_num={}
  deity_by_name={}
  plant_by_name={}
  if isinstance(obj, dict):
    names=list(obj.keys())
    # preserve order if possible
    for idx,n in enumerate(names, start=1):
      name_by_num[str(idx)] = n
      v=obj.get(n) or {}
      if isinstance(v, dict):
        if v.get('deity'): deity_by_name[n]=v.get('deity')
        if v.get('plant'): plant_by_name[n]=v.get('plant')
        # sometimes 'tree' or 'sacred_plant'
        if (not plant_by_name.get(n)) and v.get('sacred_plant'):
          plant_by_name[n]=v.get('sacred_plant')
        if (not plant_by_name.get(n)) and v.get('tree'):
          plant_by_name[n]=v.get('tree')
  return name_by_num, deity_by_name, plant_by_name

def build_devi_weapon():
  obj=load_yaml(DEITIES_YAML)
  mapping={}
  items=[]
  if isinstance(obj, list):
    items=obj
  elif isinstance(obj, dict):
    # could be {id:{...}} or graph-shaped; handle dict entries only
    for k,v in obj.items():
      if isinstance(v, dict):
        vv=dict(v); vv.setdefault('id', k); items.append(vv)
  for it in items:
    nm = it.get('name') or it.get('title') or it.get('id')
    if not nm: 
      continue
    from_id=f'devi:{slug(str(nm))}'
    weapons = it.get('weapons') or it.get('weapon') or it.get('wields')
    if isinstance(weapons, str): weapons=[weapons]
    if isinstance(weapons, list) and weapons:
      mapping[from_id]=f'weapon:{slug(str(weapons[0]))}'
  return mapping

def main():
  name_by_num, deity_by_name, plant_by_name = build_nak_maps()
  devi_weapon = build_devi_weapon()

  total_filled=0
  for relp in REL_FILES:
    if not relp.exists():
      continue
    rows=read_csv(relp)
    filled=0
    for r in rows:
      if (r.get('to_id') or '').strip():
        continue
      rel=(r.get('relation') or '').strip()
      fr=(r.get('from_id') or '').strip()

      # nakshatra numeric ids -> names -> deity/plant ids
      if fr.startswith('nakshatra:'):
        num=fr.split(':',1)[1].strip()
        name=name_by_num.get(num)
        if name:
          if rel=='nakshatra_associated_deity':
            d=deity_by_name.get(name)
            if d:
              r['to_id']=f'deity:{slug(str(d))}'
              filled+=1
          if rel=='nakshatra_sacred_plant':
            pl=plant_by_name.get(name)
            if pl:
              r['to_id']=f'plant:{slug(str(pl))}'
              filled+=1

      # devi weapon mapping
      if fr.startswith('devi:') and rel=='devi_wields_weapon':
        if fr in devi_weapon:
          r['to_id']=devi_weapon[fr]
          filled+=1

    if filled:
      write_csv(relp, rows)
    print(relp.name, 'filled_to_id=', filled, 'rows=', len(rows))
    total_filled += filled

  print('TOTAL filled_to_id=', total_filled)

if __name__=='__main__':
  main()
