import json, sys, time, urllib.parse, urllib.request
from pathlib import Path

MANI = Path('/opt/atlas/manifests')
MANI.mkdir(parents=True, exist_ok=True)

ADV = 'https://archive.org/advancedsearch.php'
META = 'https://archive.org/metadata/'
DL   = 'https://archive.org/download/'

# Domains (broad). Tune queries anytime.
QUERIES = {
  'nakshatra': [
    'title:(nakshatra OR "book of nakshatras") OR (jyotish AND nakshatra)',
    'subject:(nakshatra OR jyotisha OR vedic-astrology) AND (text OR book)'
  ],
  'tithi_nitya': [
    'title:(tithi OR panchanga OR "nitya devi" OR "nitya-devi")',
    'subject:(panchanga OR tithi OR lunar) AND (mantra OR devi)'
  ],
  'ritual': [
    'title:(vrata OR "vrata katha" OR "ritual calendar" OR panchanga)',
    'subject:(ritual OR vrata OR upavasa OR puja) AND (calendar OR lunar OR panchanga)'
  ],
  'music': [
    'title:(raga OR kirtan OR bhajan) OR subject:(raga OR kirtan OR bhajan)',
    'subject:(indian-music OR carnatic OR hindustani) AND (raga OR tala)'
  ],
  'plants': [
    'title:(ayurveda AND plants) OR title:(dravyaguna) OR subject:(medicinal-plants AND ayurveda)',
    'subject:(ayurveda OR dravyaguna) AND (plants OR materia-medica OR herbs)'
  ],
  'bija': [
    'title:(bija OR bīja OR bijakshara OR bījākṣara OR "seed syllable")',
    'title:(tantra AND mantra) AND (bija OR bijakshara OR "seed syllable")'
  ],
  'yoga_asana': [
    'title:(asana OR āsana OR hatha OR "hatha yoga" OR "yoga asana")',
    'subject:(asana OR hatha-yoga) AND (text OR manual OR book)'
  ],
  'guna_dosha': [
    'title:(tridosha OR tridoṣa OR vata OR pitta OR kapha OR guna OR guṇa)',
    'subject:(ayurveda AND dosha) OR subject:(sankhya OR sāmkhya) AND (guna OR guṇa)'
  ],
  'mantra': [
    'title:(mantra AND (chandas OR rishi OR devata OR nyasa))',
    'subject:(mantra) AND (chandas OR rishi OR devata OR nyasa)'
  ],
  'yantra': [
    'title:(yantra OR mandala) AND (tantra OR mantra)',
    'subject:(yantra OR mandala) AND (text OR book)'
  ],
}

FL = ['identifier']

# TEXT-FIRST priority (this is the key change)
PREFERRED_EXT = ['.txt', '.epub', '.html', '.htm', '.pdf', '.djvu', '.zip']
SKIP_EXT = ('.jpg','.jpeg','.png','.gif','.json','.xml','.opf','.mp3','.mp4','.m4a','.ogg','.webm','.srt','.csv','.sqlite','.db')

def http_json(url: str, timeout=30):
  req = urllib.request.Request(url, headers={'User-Agent':'CoherenceAtlas/0.2 (+local)'})
  with urllib.request.urlopen(req, timeout=timeout) as r:
    return json.loads(r.read().decode('utf-8', errors='ignore'))

def search_ids(q: str, rows=50, page=1):
  params={'q':q,'fl[]':FL,'rows':str(rows),'page':str(page),'output':'json'}
  url=ADV+'?'+urllib.parse.urlencode(params, doseq=True)
  data=http_json(url)
  docs=(data.get('response') or {}).get('docs') or []
  out=[]
  for d in docs:
    i=d.get('identifier')
    if i: out.append(i)
  # dedupe
  seen=set(); uniq=[]
  for i in out:
    if i in seen: continue
    seen.add(i); uniq.append(i)
  return uniq

def score_name(name: str):
  ln=name.lower()
  if ln.endswith(SKIP_EXT): return 9999
  for idx, ext in enumerate(PREFERRED_EXT):
    if ln.endswith(ext): return idx
  return 999

def pick_files(meta: dict, max_files: int):
  files = meta.get('files') or []
  names=[]
  for f in files:
    name=f.get('name') or ''
    if not name: 
      continue
    if score_name(name) >= 999: 
      continue
    names.append(name)
  names.sort(key=lambda n: (score_name(n), len(n)))
  # pick top N unique
  out=[]
  for n in names:
    if n not in out:
      out.append(n)
    if len(out) >= max_files:
      break
  return out

def build_domain(domain: str, n_items: int, max_files: int):
  ids=[]
  for q in QUERIES[domain]:
    for page in (1,2):
      ids += search_ids(q, rows=min(50,n_items), page=page)
  seen=set(); uniq=[]
  for i in ids:
    if i in seen: continue
    seen.add(i); uniq.append(i)
  uniq = uniq[:n_items]

  urls=[]
  for ident in uniq:
    try:
      meta=http_json(META+urllib.parse.quote(ident))
      for name in pick_files(meta, max_files):
        urls.append(f'{DL}{ident}/{urllib.parse.quote(name)}')
    except Exception:
      pass
    time.sleep(0.2)

  # dedupe
  seen=set(); out=[]
  for u in urls:
    if u in seen: continue
    seen.add(u); out.append(u)

  p=MANI/f'wget_{domain}.txt'
  header = '# Auto-generated DIRECT URLs (text-first) from Internet Archive\n# One URL per line.\n\n'
  p.write_text(header + '\n'.join(out) + '\n', encoding='utf-8')
  print('Wrote:', p, 'links:', len(out), 'items:', len(uniq))

def main():
  dom=sys.argv[1].strip() if len(sys.argv)>1 else 'all'
  n=int(sys.argv[2]) if len(sys.argv)>2 else 25
  m=int(sys.argv[3]) if len(sys.argv)>3 else 2
  if dom=='all':
    for d in QUERIES.keys():
      build_domain(d, n, m)
  else:
    if dom not in QUERIES:
      raise SystemExit('Unknown domain: '+dom)
    build_domain(dom, n, m)

if __name__=='__main__':
  main()
