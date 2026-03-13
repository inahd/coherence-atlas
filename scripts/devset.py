import json, sys
from pathlib import Path

CFG=Path('/opt/atlas/dev/devcycle_config.json')

PRESETS = {
  # safest: just show plan
  'safe': {'mode':'dry','max_steps':8},

  # focus: documentation generation + dashboards
  'docs': {'mode':'apply','max_steps':10},

  # focus: tests and lint
  'tests': {'mode':'apply','max_steps':12},

  # focus: pipeline reliability (run cycle + ready report if present)
  'pipeline': {'mode':'apply','max_steps':12},

  # keep it conservative even when applying
  'conservative_apply': {'mode':'apply','max_steps':6},
}

def main():
  if not CFG.exists():
    raise SystemExit('Missing config: '+str(CFG))
  d=json.loads(CFG.read_text(encoding='utf-8'))
  if len(sys.argv) < 2:
    print('Usage: devset.py <preset>')
    print('Presets:', ', '.join(sorted(PRESETS)))
    raise SystemExit(2)
  key=sys.argv[1].strip()
  if key not in PRESETS:
    raise SystemExit('Unknown preset: '+key+' (choose: '+', '.join(sorted(PRESETS))+')')
  d.update(PRESETS[key])
  CFG.write_text(json.dumps(d, indent=2), encoding='utf-8')
  print('Set preset:', key)
  print(json.dumps(d, indent=2))

if __name__=='__main__':
  main()
