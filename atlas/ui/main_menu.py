import curses
from atlas.data_loader import load_graph
from atlas.modes import kala

def menu(stdscr):

    graph = load_graph()

    while True:

        stdscr.clear()

        stdscr.addstr(2,5,"COHERENCE ATLAS")
        stdscr.addstr(4,5,"1  Kala Explorer")
        stdscr.addstr(6,5,"q  Quit")

        k = stdscr.getkey()

        if k == "q":
            break

        if k == "1":
            stdscr.clear()
            stdscr.addstr(2,5,"Launching Kala Explorer")
            stdscr.refresh()
            kala.run(graph)
            stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(menu)
