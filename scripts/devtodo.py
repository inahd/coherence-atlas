import sys
from pathlib import Path
TODO=Path('/opt/atlas/dev/devcycle_todo.txt')
TODO.parent.mkdir(parents=True, exist_ok=True)

def main():
  if len(sys.argv)<2:
    print('Usage: devtodo.py "<cmd>" | --clear')
    raise SystemExit(2)
  if sys.argv[1] == '--clear':
    TODO.write_text('', encoding='utf-8')
    print('cleared', TODO)
    return
  cmd=' '.join(sys.argv[1:]).strip()
  if not cmd:
    raise SystemExit('empty cmd')
  with TODO.open('a', encoding='utf-8') as f:
    f.write(cmd+'\n')
  print('added:', cmd)
  print('todo:', TODO)

if __name__=='__main__': main()
