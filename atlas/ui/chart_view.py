import subprocess
import json
import curses

def run(stdscr):

```
stdscr.clear()

stdscr.addstr(1,2,"ASTRO CHART VIEWER")
stdscr.addstr(3,2,"Press any key to load demo chart")

stdscr.getch()

try:

    cmd=["atlas","chart","1990","3","12","14","28.6139","77.2090"]
    result=subprocess.check_output(cmd)

    data=json.loads(result)

except:
    data={"error":"astro engine not reachable"}

stdscr.clear()

row=2

for k,v in data.items():

    stdscr.addstr(row,2,f"{k}: {v}")
    row+=1

    if row>20:
        break

stdscr.addstr(row+2,2,"Press any key")

stdscr.refresh()
stdscr.getch()
```

