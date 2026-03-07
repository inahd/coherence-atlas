import os
from pathlib import Path

ROOTS = [
    Path('/opt/atlas/research/_incoming'),
    Path('/opt/atlas/research_private/_incoming'),
]

BAD_DIR = Path('/opt/atlas/research/_bad')
BAD_DIR.mkdir(parents=True, exist_ok=True)

def is_pdf_header_ok(path: Path) -> bool:
    try:
        with path.open('rb') as f:
            head = f.read(8)
        return head.startswith(b'%PDF-')
    except Exception:
        return False

def main():
    moved = 0
    scanned = 0
    for root in ROOTS:
        if not root.exists():
            continue
        for p in root.rglob('*.pdf'):
            scanned += 1
            # skip tiny files early (often truncated)
            try:
                if p.stat().st_size < 1024:
                    ok = False
                else:
                    ok = is_pdf_header_ok(p)
            except Exception:
                ok = False

            if ok:
                continue

            # move aside, keep name
            dst = BAD_DIR / p.name
            # avoid collisions
            i = 1
            while dst.exists():
                dst = BAD_DIR / f'{p.stem}__bad{i}{p.suffix}'
                i += 1
            try:
                p.rename(dst)
                moved += 1
                print('[MOVED_BAD]', p, '->', dst)
            except Exception as e:
                print('[FAIL_MOVE]', p, e)

    print(f'sanitize_incoming_pdfs: scanned={scanned} moved_bad={moved} bad_dir={BAD_DIR}')

if __name__ == '__main__':
    main()
