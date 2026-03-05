import os

ROOT = "/opt/atlas"
OUT = "/opt/atlas/memory/project_index.txt"

def index():
    with open(OUT,"w") as out:
        for root,dirs,files in os.walk(ROOT):
            for f in files:
                path=os.path.join(root,f)

                if any(x in path for x in ["venv",".git","__pycache__"]):
                    continue

                try:
                    with open(path,"r",errors="ignore") as file:
                        content=file.read(2000)

                    out.write("\\n\\nFILE:"+path+"\\n")
                    out.write(content)

                except:
                    pass

    print("Project indexed.")

if __name__=="__main__":
    index()
