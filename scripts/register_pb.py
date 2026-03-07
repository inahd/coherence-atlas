from pathlib import Path, PurePath
import re
p = Path("/opt/atlas/atlas.py")
t = p.read_text(encoding="utf-8", errors="ignore")
cmd = "\"pb\": \"bash /opt/atlas/scripts/pb_cli.sh\""
if "\"pb\":" not in t:
    t = re.sub(r"COMMANDS\s*=\s*\{", "COMMANDS = {\n    " + cmd + ",", t, count=1)
    p.write_text(t, encoding="utf-8")
    print("REGISTERED pb command")
else:
    print("pb command already present")
