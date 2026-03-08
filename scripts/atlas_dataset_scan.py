import os, yaml, json

DATASETS="datasets"
report={}

for root,dirs,files in os.walk(DATASETS):
    for f in files:
        if f.endswith(".yaml") or f.endswith(".yml"):
            path=os.path.join(root,f)
            try:
                data=yaml.safe_load(open(path))
                size=0
                if isinstance(data,list):
                    size=len(data)
                if isinstance(data,dict):
                    size=len(data.keys())
                report[path]=size
            except Exception as e:
                report[path]="error"

out="memory/reports/dataset_report.json"
os.makedirs("memory/reports",exist_ok=True)

with open(out,"w") as f:
    json.dump(report,f,indent=2)

print("\nAtlas dataset scan complete\n")
for k,v in report.items():
    print(k,"→",v)
print("\nReport written to",out)
