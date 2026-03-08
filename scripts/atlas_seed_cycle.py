import os, yaml, random, datetime

DATASETS="datasets"
seeds=[]

def extract_entities():
    entities=[]
    for root,dirs,files in os.walk(DATASETS):
        for f in files:
            if f.endswith(".yaml") or f.endswith(".yml"):
                path=os.path.join(root,f)
                try:
                    data=yaml.safe_load(open(path))
                    if isinstance(data,dict):
                        entities.extend(list(data.keys()))
                    if isinstance(data,list):
                        for item in data:
                            if isinstance(item,dict):
                                entities.extend(list(item.keys()))
                except:
                    pass
    return list(set(entities))

def generate_seeds(entities):
    random.shuffle(entities)
    for e in entities[:25]:
        seeds.append(f"""
## SEED

TITLE: {e}

CATEGORY: RESEARCH

STATUS: EXPERIMENTAL

SOURCE: Atlas dataset inference

SUMMARY:
Investigate the concept "{e}" and its relationships across
jyotish, ritual, plants, texts, and symbolic systems.

NEXT ACTION:
Map relations in Atlas graph and search scriptural references.
""")

entities=extract_entities()
generate_seeds(entities)

out="research/seeds/auto_generated_seeds.md"

with open(out,"a") as f:
    f.write(f"\n\n# Atlas Seed Cycle {datetime.datetime.now()}\n")
    for s in seeds:
        f.write(s)

print("\nGenerated",len(seeds),"research seeds")
print("Written to",out)
