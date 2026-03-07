import json, os, re, subprocess, sys, time
from pathlib import Path

BASE = Path('/opt/atlas')
CFG_PATH = BASE/'dev/devcycle_config.json'
LOG_DIR = BASE/'logs'
DEV_TODO = BASE/'dev'/'devcycle_todo.txt'
LOG_DIR.mkdir(parents=True, exist_ok=True)

def sh(cmd: str):
    return subprocess.run(cmd, shell=True, text=True, capture_output=True)

def must(cmd: str):
    r = sh(cmd)
    if r.returncode != 0:
        raise SystemExit(f'FAIL: {cmd}\n{r.stdout}\n{r.stderr}')
    return r

def load_cfg():
    if not CFG_PATH.exists():
        raise SystemExit(f'Missing config: {CFG_PATH}')
    return json.loads(CFG_PATH.read_text(encoding='utf-8'))



def load_todo():
    if not DEV_TODO.exists():
        return []
    lines=[]
    for raw in DEV_TODO.read_text(encoding='utf-8', errors='ignore').splitlines():
        s=raw.strip()
        if not s or s.startswith('#'):
            continue
        lines.append(s)
    return lines
def is_allowed(cmd: str, cfg: dict) -> bool:
    c = cmd.strip()
    for tok in cfg.get('blocked_tokens', []):
        if tok in c:
            return False
    return any(c.startswith(p) for p in cfg.get('allowed_cmd_prefixes', []))

def collect_context():
    ctx = {}
    ctx['branch'] = sh('git -C /opt/atlas branch --show-current').stdout.strip()
    ctx['status'] = sh('git -C /opt/atlas status --porcelain').stdout.strip()
    ctx['last_commit'] = sh('git -C /opt/atlas log -1 --oneline --decorate').stdout.strip()
    ctx['diff_stat'] = sh('git -C /opt/atlas diff --stat').stdout.strip()
    # lightweight signals
    ctx['sanity_test'] = sh('python3 -c "import sys; print(\"ok\")"').stdout.strip()
    # try pytest if present
    if (BASE/'tests').exists():
        r = sh('pytest -q')
        ctx['pytest_rc'] = r.returncode
        ctx['pytest_out'] = (r.stdout + '\n' + r.stderr).strip()[:4000]
    return ctx

def propose_plan(ctx: dict):
    todo = load_todo()
    if todo:
        return todo

    # Rules-first plan: fix obvious breakages and generate docs.
    steps = []
    # If tests failing, prioritize tests
    if ctx.get('pytest_rc', 0) != 0:
        steps.append('pytest -q')
    # Always refresh docs if generator exists
    if (BASE/'scripts/generate_docs.py').exists():
        steps.append('python3 /opt/atlas/scripts/generate_docs.py')
    # Always rebuild dashboard (if present)
    if (BASE/'scripts/dashboard.py').exists():
        steps.append('python3 /opt/atlas/scripts/dashboard.py')
    # Always run sanity
    if (BASE/'scripts/run_tests.sh').exists():
        steps.append('bash /opt/atlas/scripts/run_tests.sh')
    # Git hygiene suggestion (no auto-push)
    return steps[:10]

def run_steps(steps, cfg):
    mode = cfg.get('mode', 'dry')
    log_path = LOG_DIR / f"devcycle_{time.strftime('%Y%m%d_%H%M%S')}.log"
    out_lines = []
    out_lines.append(f"mode={mode}")
    out_lines.append(f"steps={len(steps)}")
    out_lines.append('')

    for i, cmd in enumerate(steps, 1):
        out_lines.append(f"[{i}] {cmd}")
        if not is_allowed(cmd, cfg):
            out_lines.append("  BLOCKED (not in allowlist or contains blocked token)")
            continue
        if mode == 'dry':
            out_lines.append("  DRY-RUN (not executed)")
            continue
        r = sh(cmd)
        out_lines.append(f"  rc={r.returncode}")
        if r.stdout.strip():
            out_lines.append("  stdout:\n" + r.stdout.strip()[:2000])
        if r.stderr.strip():
            out_lines.append("  stderr:\n" + r.stderr.strip()[:2000])
        out_lines.append('')

    log_path.write_text('\n'.join(out_lines) + '\n', encoding='utf-8')
    print('Wrote log:', log_path)
    print('\n'.join(out_lines[:120]))

def main():
    cfg = load_cfg()
    ctx = collect_context()
    steps = propose_plan(ctx)

    # Optional: create a branch in apply mode
    if cfg.get('mode') == 'apply':
        b = cfg.get('branch_prefix','autodev/') + time.strftime('%Y%m%d_%H%M%S')
        must(f'git -C /opt/atlas checkout -b {b}')

    run_steps(steps, cfg)

    if cfg.get('mode') == 'apply':
        # commit if changes
        st = sh('git -C /opt/atlas status --porcelain').stdout.strip()
        if st:
            must('git -C /opt/atlas add -A')
            sh('git -C /opt/atlas commit -m "autodev: apply devcycle"')
            print('Committed changes on branch.')
        else:
            print('No changes to commit.')

if __name__ == '__main__':
    main()
