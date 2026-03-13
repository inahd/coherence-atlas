import curses
from atlas.core.mandala import layout
from atlas.core.output import render_output

def run(stdscr):

    stdscr.clear()

    h,w=stdscr.getmaxyx()

    nodes=layout()

    cx=w//2
    cy=h//2

    for name,x,y in nodes:

        try:
            stdscr.addstr(cy+y,cx+x,name[:6])
        except:
            pass

    stdscr.addstr(2,2,"Atlas Mandala")

    stdscr.refresh()
    stdscr.getch()

    curses.endwin()

    render_output("mandala")
