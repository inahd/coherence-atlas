import os
import faiss
from sentence_transformers import SentenceTransformer

ROOT="/opt/atlas"
INDEX_FILE="/opt/atlas/memory/vector.index"
TEXT_FILE="/opt/atlas/memory/vector_texts.txt"

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_files():
    texts=[]
    paths=[]
    for root,dirs,files in os.walk(ROOT):
        for f in files:
            path=os.path.join(root,f)

            if any(x in path for x in ["venv",".git","__pycache__","memory"]):
                continue

            try:
                with open(path,"r",errors="ignore") as file:
                    content=file.read(2000)

                texts.append(content)
                paths.append(path)
            except:
                pass

    return texts,paths

def build():
    texts,paths=load_files()

    emb=model.encode(texts)

    index=faiss.IndexFlatL2(len(emb[0]))
    index.add(emb)

    os.makedirs("/opt/atlas/memory",exist_ok=True)

    faiss.write_index(index,INDEX_FILE)

    with open(TEXT_FILE,"w") as f:
        for p,t in zip(paths,texts):
            f.write("FILE:"+p+"\n")
            f.write(t+"\n\n")

    print("Vector memory built.")

def search(q,k=3):

    index=faiss.read_index(INDEX_FILE)

    with open(TEXT_FILE) as f:
        chunks=f.read().split("FILE:")

    qv=model.encode([q])
    D,I=index.search(qv,k)

    results=[]
    for i in I[0]:
        if i<len(chunks):
            results.append(chunks[i])

    return "\n".join(results)

if __name__=="__main__":
    build()
