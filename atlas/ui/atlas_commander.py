import curses
import subprocess
import sys

MENU = [
    ("Wiki Explorer", "wiki"),
    ("Tarot / Card Decks", "cards"),
    ("Cosmology Mandala", "mandala"),
    ("Graph Explorer", "graph"),
    ("Documentation", "docs"),
    ("Research Seeds", "seeds"),
    ("Quit", "quit"),
]

def draw_menu(stdscr, selected):

    stdscr.clear()
    h, w = stdscr.getmaxyx()

    title = "COHERENCE ATLAS"
    subtitle = "Relational Cosmology Environment"

    stdscr.addstr(1, (w-len(title))//2, title, curses.A_BOLD)
    stdscr.addstr(3, (w-len(subtitle))//2, subtitle)

    for i,(label,_) in enumerate(MENU):

        x = w//2 - 20
        y = 6 + i

        if i == selected:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y,x,label)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y,x,label)

    legend="↑ ↓ move • Enter open • q quit"
    stdscr.addstr(h-2,(w-len(legend))//2,legend)

    stdscr.refresh()


def launch(action):

    if action == "mandala":
        subprocess.call(["python","-m","atlas.ui.mandala_view"])

    elif action == "graph":
        subprocess.call(["python","tools/merge_all_graphs.py"])

    elif action == "seeds":
        subprocess.call(["python","tools/weak_node_seeds.py"])

    elif action == "wiki":
        subprocess.call(["python","-m","atlas.ui.node_view"])

    elif action == "cards":
        subprocess.call(["python","-m","atlas.ui.nakshatra_view"])

    elif action == "docs":
        subprocess.call(["less","README.md"])


def main(stdscr):

    curses.curs_set(0)

    selected = 0

    while True:

        draw_menu(stdscr,selected)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(MENU)

        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(MENU)

        elif key in [10,13]:

            label,action = MENU[selected]

            if action == "quit":
                break

            curses.endwin()
            launch(action)
            stdscr.refresh()

        elif key == ord("q"):
            break


curses.wrapper(main)
