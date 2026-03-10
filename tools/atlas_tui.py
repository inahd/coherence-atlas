#!/usr/bin/env python3
from pathlib import Path
import curses
import textwrap

ROOT = Path("/opt/atlas")
SEEDS = ROOT / "seeds"
AXIOMS = ROOT / "docs" / "axioms"
LOGS = ROOT / "logs"
TASKS = ROOT / "tasks"


def list_items(path: Path):
    if not path.exists():
        return []
    return sorted([p.stem for p in path.glob("*.md")])


def read_file(stem: str, section: str):
    if section == "Seeds":
        path = SEEDS / f"{stem}.md"
    elif section == "Axioms":
        path = AXIOMS / f"{stem}.md"
    elif section == "Logs":
        path = LOGS / f"{stem}.md"
    else:
        path = TASKS / f"{stem}.md"

    if not path.exists():
        return f"[Missing] {path}"

    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"[Read error] {e}"


def wrap_lines(text: str, width: int):
    out = []
    for raw in text.splitlines():
        if not raw.strip():
            out.append("")
            continue
        out.extend(textwrap.wrap(raw, width=width, replace_whitespace=False, drop_whitespace=False) or [""])
    return out


class AtlasTUI:
    def __init__(self):
        self.sections = ["Seeds", "Axioms", "Logs", "Tasks"]
        self.section_index = 0
        self.item_index = 0
        self.scroll = 0
        self.status = "h/l switch panes | j/k move | Enter open | r refresh | q quit"

    def current_section(self):
        return self.sections[self.section_index]

    def current_items(self):
        sec = self.current_section()
        if sec == "Seeds":
            return list_items(SEEDS)
        if sec == "Axioms":
            return list_items(AXIOMS)
        if sec == "Logs":
            return list_items(LOGS)
        return list_items(TASKS)

    def current_item(self):
        items = self.current_items()
        if not items:
            return None
        self.item_index = max(0, min(self.item_index, len(items) - 1))
        return items[self.item_index]

    def draw_box(self, stdscr, y, x, h, w, title):
        stdscr.addstr(y, x + 2, f"[ {title} ]")
        for i in range(x, x + w):
            stdscr.addch(y + 1, i, curses.ACS_HLINE)
            stdscr.addch(y + h - 1, i, curses.ACS_HLINE)
        for i in range(y + 1, y + h):
            stdscr.addch(i, x, curses.ACS_VLINE)
            stdscr.addch(i, x + w - 1, curses.ACS_VLINE)
        stdscr.addch(y + 1, x, curses.ACS_ULCORNER)
        stdscr.addch(y + 1, x + w - 1, curses.ACS_URCORNER)
        stdscr.addch(y + h - 1, x, curses.ACS_LLCORNER)
        stdscr.addch(y + h - 1, x + w - 1, curses.ACS_LRCORNER)

    def draw(self, stdscr):
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        header = "Coherence Atlas  |  🌱 seed → 🪷 relation → 🔱 principle → ✨ insight"
        stdscr.addstr(0, 2, header[: max(0, w - 4)], curses.A_BOLD)

        left_w = max(24, w // 3)
        right_w = w - left_w - 3

        self.draw_box(stdscr, 1, 1, h - 3, left_w, "Fields")
        self.draw_box(stdscr, 1, left_w + 2, h - 3, right_w, "Detail")

        # Left pane: sections + items
        y = 3
        for i, sec in enumerate(self.sections):
            attr = curses.A_REVERSE if i == self.section_index else curses.A_BOLD
            stdscr.addstr(y, 3, sec[: left_w - 5], attr)
            y += 1

        y += 1
        items = self.current_items()
        if not items:
            stdscr.addstr(y, 3, "_none yet_", curses.A_DIM)
        else:
            visible_h = h - y - 3
            start = max(0, min(self.item_index - visible_h // 2, max(0, len(items) - visible_h)))
            subset = items[start : start + visible_h]
            for idx, item in enumerate(subset, start=start):
                attr = curses.A_REVERSE if idx == self.item_index else curses.A_NORMAL
                stdscr.addstr(y, 3, item[: left_w - 5], attr)
                y += 1

        # Right pane: detail
        item = self.current_item()
        content = f"[{self.current_section()}] {item}\n\n" + read_file(item, self.current_section()) if item else f"[{self.current_section()}]\n\n_no items_"
        wrapped = wrap_lines(content, max(10, right_w - 4))
        visible_h = h - 6
        self.scroll = max(0, min(self.scroll, max(0, len(wrapped) - visible_h)))

        ry = 3
        for line in wrapped[self.scroll : self.scroll + visible_h]:
            stdscr.addstr(ry, left_w + 4, line[: right_w - 4])
            ry += 1

        stdscr.addstr(h - 1, 2, self.status[: max(0, w - 4)], curses.A_DIM)
        stdscr.refresh()

    def run(self, stdscr):
        curses.curs_set(0)
        stdscr.keypad(True)

        while True:
            self.draw(stdscr)
            key = stdscr.getch()

            if key == ord("q"):
                break
            elif key in (ord("h"), curses.KEY_LEFT):
                self.section_index = max(0, self.section_index - 1)
                self.item_index = 0
                self.scroll = 0
            elif key in (ord("l"), curses.KEY_RIGHT):
                self.section_index = min(len(self.sections) - 1, self.section_index + 1)
                self.item_index = 0
                self.scroll = 0
            elif key in (ord("j"), curses.KEY_DOWN):
                items = self.current_items()
                if items:
                    self.item_index = min(len(items) - 1, self.item_index + 1)
                    self.scroll = 0
            elif key in (ord("k"), curses.KEY_UP):
                items = self.current_items()
                if items:
                    self.item_index = max(0, self.item_index - 1)
                    self.scroll = 0
            elif key == curses.KEY_NPAGE:
                self.scroll += 10
            elif key == curses.KEY_PPAGE:
                self.scroll = max(0, self.scroll - 10)
            elif key in (10, 13, curses.KEY_ENTER):
                self.scroll = 0
            elif key == ord("r"):
                self.status = "Refreshed."
            else:
                self.status = "h/l switch panes | j/k move | Enter open | PgUp/PgDn scroll | r refresh | q quit"


def main():
    curses.wrapper(AtlasTUI().run)


if __name__ == "__main__":
    main()
