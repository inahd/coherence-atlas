import curses

MOCK_NODE={
"name":"Mars",
"type":"planet",
"element":"fire",
"ruler_of":"Aries, Scorpio",
"nakshatra":"Shravana"
}

def run(stdscr):

    stdscr.clear()

    stdscr.addstr(1,2,"NODE INSPECTOR")

    row=3

    for k,v in MOCK_NODE.items():
        stdscr.addstr(row,4,f"{k}: {v}")
        row+=1

    stdscr.addstr(row+2,2,"Press any key")

    stdscr.refresh()
    stdscr.getch()
