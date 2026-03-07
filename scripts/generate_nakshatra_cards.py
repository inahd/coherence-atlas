import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DATA = Path("datasets/astro/nakshatra_core.csv")
OUT  = Path("memory/card_images")

OUT.mkdir(parents=True,exist_ok=True)

rows=list(csv.DictReader(open(DATA)))

font = ImageFont.load_default()

for r in rows:

    name=r["nakshatra"]
    graha=r["graha"]
    deity=r["deity"]

    img=Image.new("RGB",(600,900),(12,12,36))
    d=ImageDraw.Draw(img)

    d.text((50,80),name.upper(),fill=(255,255,255),font=font)

    d.text((50,200),"Ruler: "+graha,fill=(200,200,220),font=font)
    d.text((50,260),"Deity: "+deity,fill=(200,200,220),font=font)

    path=OUT/f"{name}.png"
    img.save(path)

print("Generated",len(rows),"nakshatra cards")
print("Location:",OUT)
