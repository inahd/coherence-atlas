import os
from sentence_transformers import SentenceTransformer
import chromadb

RESEARCH_DIR="/opt/atlas/research"

model=SentenceTransformer("all-MiniLM-L6-v2")

client=chromadb.Client()
collection=client.get_or_create_collection("research")

def chunk(text,size=500):

    words=text.split()
    chunks=[]

    for i in range(0,len(words),size):
        chunks.append(" ".join(words[i:i+size]))

    return chunks

def read_file(path):

    try:
        with open(path,"r",errors="ignore") as f:
            return f.read()
    except:
        return ""

def ingest_file(path):

    text=read_file(path)

    chunks=chunk(text)

    for i,c in enumerate(chunks):

        emb=model.encode(c).tolist()

        collection.add(
            embeddings=[emb],
            documents=[c],
            ids=[path+"_"+str(i)]
        )

    print("Indexed:",path)

def run():

    for root,dirs,files in os.walk(RESEARCH_DIR):

        for f in files:

            path=os.path.join(root,f)

            ingest_file(path)

if __name__=="__main__":
    run()
