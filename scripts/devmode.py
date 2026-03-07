import json, sys
from pathlib import Path
CFG=Path('/opt/atlas/dev/devcycle_config.json')
def main():
  if len(sys.argv)<2:
    print('Usage: devmode.py dry|apply')
    raise SystemExit(2)
  mode=sys.argv[1].strip()
  if mode not in ('dry','apply'):
    raise SystemExit('mode must be dry or apply')
  d=json.loads(CFG.read_text(encoding='utf-8'))
  d['mode']=mode
  CFG.write_text(json.dumps(d, indent=2), encoding='utf-8')
  print('mode set to', mode)
if __name__=='__main__': main()
