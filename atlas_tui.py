import curses
import os

DATA_DIR = "/opt/atlas/data/seeds"


def load_seeds():
    seeds = []
    if not os.path.exists(DATA_DIR):
        return seeds

    for f in os.listdir(DATA_DIR):
        if f.endswith(".md"):
            seeds.append(f[:-3])
    seeds.sort()
    return seeds


def draw_menu(stdscr, seeds, index):
    stdscr.clear()

    h, w = stdscr.getmaxyx()

    title = "Coherence Atlas — Seed Browser"
    stdscr.addstr(0, w//2 - len(title)//2, title)

    for i, seed in enumerate(seeds):
        if i == index:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(i+2, 2, seed)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(i+2, 2, seed)

    stdscr.addstr(h-2, 2, "↑↓ navigate | enter view | n new seed | q quit")

    stdscr.refresh()


def view_seed(stdscr, seed_name):
    path = os.path.join(DATA_DIR, seed_name + ".md")

    stdscr.clear()

    if not os.path.exists(path):
        stdscr.addstr(0,0,"Seed not found")
        stdscr.getch()
        return

    with open(path) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        stdscr.addstr(i, 0, line.strip())

    stdscr.addstr(len(lines)+2,0,"Press any key to return")
    stdscr.refresh()
    stdscr.getch()

def new_seed(stdscr):
    curses.echo()
    curses.curs_set(1)

    stdscr.clear()
    stdscr.addstr(0, 0, "New seed title: ")
    stdscr.refresh()

    title = stdscr.getstr(0, 16, 80).decode().strip()

    curses.noecho()
    curses.curs_set(0)

    if not title:
        return

    filename = title.lower().replace(" ", "_") + ".md"
    path = os.path.join(DATA_DIR, filename)

    if os.path.exists(path):
        return

    with open(path, "w") as f:
        f.write(f"title: {title}\n")
        f.write("tags:\n")
        f.write("links:\n\n")
        f.write("Describe the seed here.\n")



def main(stdscr):

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

    index = 0

    while True:

        seeds = load_seeds()

        draw_menu(stdscr, seeds, index)

        key = stdscr.getch()

        if key == curses.KEY_UP and index > 0:
            index -= 1

        elif key == curses.KEY_DOWN and index < len(seeds)-1:
            index += 1

        elif key == ord("q"):
            break

        elif key == ord("n"):
            new_seed(stdscr)

        elif key == 10 and seeds:
            view_seed(stdscr, seeds[index])


curses.wrapper(main)
