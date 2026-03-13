import re, zipfile
from pathlib import Path

INP = Path('/opt/atlas/research/_incoming')
OUT = Path('/opt/atlas/research/_text')
OUT.mkdir(parents=True, exist_ok=True)

def safe(s: str) -> str:
  s=re.sub(r'[^A-Za-z0-9._-]+','_', s)
  return s[:180]

def write(out: Path, txt: str):
  out.write_text(txt, encoding='utf-8', errors='ignore')

def html_to_text(html: str) -> str:
  html=re.sub(r'(?is)<script.*?>.*?</script>', ' ', html)
  html=re.sub(r'(?is)<style.*?>.*?</style>', ' ', html)
  txt=re.sub(r'(?is)<[^>]+>', ' ', html)
  txt=re.sub(r'\s+', ' ', txt).strip()
  return txt

def handle_epub(src: Path) -> str:
  parts=[]
  with zipfile.ZipFile(src, 'r') as z:
    for name in z.namelist():
      ln=name.lower()
      if ln.endswith(('.xhtml','.html','.htm')):
        data=z.read(name).decode('utf-8', errors='ignore')
        t=html_to_text(data)
        if t: parts.append(t)
  return '\n\n'.join(parts)

def main():
  if not INP.exists():
    print('no incoming:', INP); return
  new=0
  for f in INP.rglob('*'):
    if not f.is_file(): 
      continue
    ln=f.name.lower()
    try:
      if ln.endswith('.txt'):
        out=OUT/(safe(f.name))
        if not out.exists():
          write(out, f.read_text(encoding='utf-8', errors='ignore')); new+=1
      elif ln.endswith(('.html','.htm')):
        out=OUT/(safe(f.name)+'.txt')
        if not out.exists():
          write(out, html_to_text(f.read_text(encoding='utf-8', errors='ignore'))); new+=1
      elif ln.endswith('.epub'):
        out=OUT/(safe(f.name)+'.txt')
        if not out.exists():
          write(out, handle_epub(f)); new+=1
    except Exception:
      pass
  print('extract_nonpdf: new_text_files=', new, 'outdir=', OUT)

if __name__=='__main__':
  main()
