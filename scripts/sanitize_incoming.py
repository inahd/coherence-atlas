from pathlib import Path

INP = Path('/opt/atlas/research/_incoming')
BAD = Path('/opt/atlas/research/_bad')
BAD.mkdir(parents=True, exist_ok=True)

def ok_pdf(p: Path) -> bool:
  try:
    if p.stat().st_size < 1024:
      return False
    with p.open('rb') as f:
      h=f.read(8)
    return h.startswith(b'%PDF-')
  except Exception:
    return False

def move_bad(p: Path):
  dst = BAD / p.name
  i=1
  while dst.exists():
    dst = BAD / f'{p.stem}__bad{i}{p.suffix}'
    i+=1
  p.rename(dst)
  print('[MOVED_BAD]', p, '->', dst)

def main():
  if not INP.exists():
    print('no incoming:', INP); return
  moved=0; scanned=0
  for p in INP.rglob('*.pdf'):
    scanned += 1
    if ok_pdf(p): 
      continue
    try:
      move_bad(p); moved += 1
    except Exception as e:
      print('[FAIL_MOVE]', p, e)
  print('sanitize_incoming: scanned=', scanned, 'moved_bad=', moved, 'bad_dir=', BAD)

if __name__=='__main__':
  main()
