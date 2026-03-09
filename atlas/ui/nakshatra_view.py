import curses

NAKSHATRAS = [
"Ashwini","Bharani","Krittika","Rohini","Mrigashira",
"Ardra","Punarvasu","Pushya","Ashlesha",
"Magha","Purva Phalguni","Uttara Phalguni",
"Hasta","Chitra","Swati","Vishakha",
"Anuradha","Jyeshtha","Mula",
"Purva Ashadha","Uttara Ashadha",
"Shravana","Dhanishta","Shatabhisha",
"Purva Bhadrapada","Uttara Bhadrapada","Revati"
]

def run(stdscr):

    stdscr.clear()
    stdscr.addstr(1,2,"Nakshatra Viewer")

    row = 3

    for n in NAKSHATRAS:
        stdscr.addstr(row,4,n)
        row += 1
        if row > curses.LINES - 2:
            break

    stdscr.addstr(row+1,2,"Press any key")
    stdscr.refresh()
    stdscr.getch()
