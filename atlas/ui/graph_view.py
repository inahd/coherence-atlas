import curses

def run(stdscr):

    stdscr.clear()

    stdscr.addstr(1,2,"GRAPH EXPLORER")

    stdscr.addstr(3,2,"Graph system integration coming.")

    stdscr.addstr(5,2,"Press any key")

    stdscr.refresh()
    stdscr.getch()
