import os,re
from datetime import datetime

SOURCE_DIRS=["docs","architecture","datasets","transcripts"]
SEED_DIR="seeds"
os.makedirs(SEED_DIR,exist_ok=True)

def topics(text):
    words=re.findall(r"[A-Za-z]{6,}",text.lower())
    freq={}
    for w in words:
        freq[w]=freq.get(w,0)+1
    return sorted(freq,key=freq.get,reverse=True)[:5]

for root in SOURCE_DIRS:
    if not os.path.exists(root): continue
    for f in os.listdir(root):
        p=os.path.join(root,f)
        if not os.path.isfile(p): continue
        text=open(p,errors="ignore").read()
        for t in topics(text):
            name=f"seed_{t}_{datetime.now().strftime('%H%M%S')}.md"
            open(os.path.join(SEED_DIR,name),"w").write(f"TITLE\n{t}\n")
