import curses

from atlas.ui.mandala_view import run as mandala
from atlas.runtime.cycle import run as cycle
from atlas.core.graph import node_count, edge_count

MENU=[
("Mandala","View mandala"),
("Cycle","Run atlas cycle"),
("Stats","Graph stats"),
("Quit","Exit")
]

def draw(stdscr,sel):

    stdscr.clear()

    h,w=stdscr.getmaxyx()

    stdscr.addstr(1,w//2-7,"ATLAS COMMANDER",curses.A_BOLD)

    for i,(name,_) in enumerate(MENU):

        y=5+i
        x=w//2-8

        if i==sel:
            stdscr.attron(curses.A_REVERSE)

        stdscr.addstr(y,x,name)

        if i==sel:
            stdscr.attroff(curses.A_REVERSE)

    stdscr.refresh()

def stats(stdscr):

    stdscr.clear()

    n=node_count()
    e=edge_count()

    stdscr.addstr(2,2,"Graph statistics")
    stdscr.addstr(4,2,f"Nodes: {n}")
    stdscr.addstr(5,2,f"Edges: {e}")

    stdscr.refresh()
    stdscr.getch()

def main(stdscr):

    curses.curs_set(0)

    sel=0

    while True:

        draw(stdscr,sel)

        k=stdscr.getch()

        if k==curses.KEY_UP:
            sel=(sel-1)%len(MENU)

        elif k==curses.KEY_DOWN:
            sel=(sel+1)%len(MENU)

        elif k in [10,13]:

            name=MENU[sel][0]

            if name=="Quit":
                break

            if name=="Mandala":
                mandala(stdscr)

            if name=="Cycle":
                cycle()

            if name=="Stats":
                stats(stdscr)

if __name__=="__main__":
    curses.wrapper(main)
