import json, os, re, subprocess, sys, time
from pathlib import Path

BASE=Path('/opt/atlas')
LOGDIR=BASE/'logs'
LOGDIR.mkdir(parents=True, exist_ok=True)

ALLOWED_PATTERNS=[
  r'^python3\s+/opt/atlas/scripts/[a-zA-Z0-9_\-\.]+\.py(\s+.*)?$',
  r'^bash\s+/opt/atlas/scripts/[a-zA-Z0-9_\-\.]+\.sh(\s+.*)?$',
  r'^atlas\s+[a-zA-Z0-9_\-]+(\s+.*)?$',
  r'^(ls|head|tail|wc|du|find|grep|sed|awk).* /opt/atlas.*$',
]

BLOCKLIST=[r'rm', r'sudo', r'chown', r'chmod', r'mkfs', r'shutdown', r'reboot', r':>']

def allowed(cmd:str)->bool:
  s=cmd.strip()
  for b in BLOCKLIST:
    if re.search(b,s):
      return False
  return any(re.match(p,s) for p in ALLOWED_PATTERNS)

def run(cmd:str, log:Path)->int:
  with log.open('a', encoding='utf-8') as f:
    f.write(f"
$ {cmd}
")
  p=subprocess.run(cmd, shell=True, text=True, capture_output=True)
  with log.open('a', encoding='utf-8') as f:
    if p.stdout: f.write(p.stdout+'
')
    if p.stderr: f.write(p.stderr+'
')
    f.write(f"[rc={p.returncode}]
")
  return p.returncode

def main():
  plan=json.load(sys.stdin)
  ts=time.strftime('%Y%m%d_%H%M%S')
  log=LOGDIR/f'llm_cycle_{ts}.log'

  steps=plan.get('steps',[])
  ok=0; bad=[]
  for st in steps:
    cmd=(st.get('cmd') or '').strip()
    if not cmd:
      continue
    if not allowed(cmd):
      bad.append(cmd)
      continue
    rc=run(cmd, log)
    if rc==0:
      ok += 1

  report=BASE/'memory/reports/llm_cycle_last.json'
  report.write_text(json.dumps({
    'log': str(log),
    'ok_steps': ok,
    'blocked': bad,
    'goal': plan.get('goal',''),
    'success_checks': plan.get('success_checks',[])
  }, indent=2), encoding='utf-8')

  print('LOG', log)
  print('REPORT', report)
  print('OK_STEPS', ok)
  if bad:
    print('BLOCKED', len(bad))

if __name__=='__main__':
  main()
