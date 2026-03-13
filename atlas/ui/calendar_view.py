import curses
import datetime

def run(stdscr):

    stdscr.clear()

    today=datetime.date.today()

    stdscr.addstr(1,2,"COSMIC CALENDAR")

    stdscr.addstr(3,2,f"Date: {today}")

    stdscr.addstr(5,2,"Moon Nakshatra: (future)")
    stdscr.addstr(6,2,"Planetary Day: (future)")

    stdscr.addstr(8,2,"Press any key")

    stdscr.refresh()
    stdscr.getch()
