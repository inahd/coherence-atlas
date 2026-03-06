import csv
from pathlib import Path
from collections import defaultdict

BASE=Path('/opt/atlas')
DS=BASE/'datasets'
WIKI=BASE/'docs/wiki'
WIKI.mkdir(parents=True, exist_ok=True)

FILES = [
  DS/'relations_resolved_canon.csv',
  DS/'relations_resolved_inference.csv',
  DS/'relations_resolved_overlays.csv',
]

def read(p: Path):
  if not p.exists(): return []
  with p.open(newline='', encoding='utf-8') as f:
    return list(csv.DictReader(f))

def typ(_id: str) -> str:
  return (_id.split(':',1)[0] if ':' in (_id or '') else 'unknown').strip().lower()

def title(_id: str) -> str:
  if not _id: return 'Unknown'
  if ':' in _id:
    t,v=_id.split(':',1)
    return f'{t.title()}: {v.replace('_',' ').title()}'
  return _id

def md_escape(s: str) -> str:
  return (s or '').replace('\n',' ').strip()

def main():
  rows=[]
  for f in FILES:
    rows += read(f)

  by_entity = defaultdict(list)
  for r in rows:
    fr=(r.get('from_id') or '').strip()
    to=(r.get('to_id') or '').strip()
    if fr: by_entity[fr].append(r)
    if to:
      # backlink placeholder (so pages exist even if only targets)
      by_entity.setdefault(to, [])

  # build indexes by type
  by_type=defaultdict(list)
  for eid in by_entity.keys():
    by_type[typ(eid)].append(eid)
  for k in by_type: by_type[k].sort()

  # write home
  home = []
  home.append('# Coherence Atlas Wiki')
  home.append('')
  home.append('Generated pages from resolved layers:')
  home.append('- canon (evidence-backed where available)')
  home.append('- inference (coherence-derived, explicitly marked)')
  home.append('- overlays (alternatives / variants)')
  home.append('')
  home.append('## Index')
  for t, ids in sorted(by_type.items(), key=lambda x: x[0]):
    home.append(f'- [{t}](./index_{t}.md) ({len(ids)})')
  (WIKI/'Home.md').write_text('\n'.join(home)+'\n', encoding='utf-8')

  # write type indexes
  for t, ids in by_type.items():
    lines=[f'# Index: {t}', '']
    for eid in ids:
      slug=eid.replace(':','__')
      lines.append(f'- [{title(eid)}](./{slug}.md)')
    (WIKI/f'index_{t}.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')

  # write entity pages
  for eid, rels in by_entity.items():
    slug=eid.replace(':','__')
    lines=[f'# {title(eid)}', '', f'**id:** ', '']
    # group by relation
    grp=defaultdict(list)
    for r in rels:
      grp[(r.get('relation') or 'related_to').strip()].append(r)

    for rel, items in sorted(grp.items(), key=lambda x: x[0]):
      lines.append(f'## {rel}')
      lines.append('')
      for r in sorted(items, key=lambda x: (x.get('profile',''), x.get('score','')), reverse=True):
        to=r.get('to_id','')
        layer=r.get('profile','')
        conf=r.get('confidence','')
        score=r.get('score','')
        trad=r.get('tradition','')
        loc=r.get('source_locator','')
        src=r.get('source_title','')
        ex=md_escape((r.get('excerpt','') or '')[:300])
        to_link = f'./{to.replace(':','__')}.md' if to else ''
        if to and (WIKI/(to.replace(':','__')+'.md')).exists():
          tgt=f'[{to}]({to_link})'
        else:
          tgt=f'' if to else ''
        lines.append(f'- **{layer}**  score={score} trad={trad} → {tgt}')
        if src or loc:
          lines.append(f'  - src:  loc: ')
        if ex:
          lines.append(f'  - ex: {ex}')
      lines.append('')

    (WIKI/f'{slug}.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')

  print('Wrote wiki:', WIKI)

if __name__=='__main__':
  main()
