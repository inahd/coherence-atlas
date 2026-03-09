#!/usr/bin/env python3

import os

OUT = "/opt/atlas/cards/nakshatra"

nakshatras = [

("Ashwini","Ashvini Kumaras","horse head","healing","Ketu"),
("Bharani","Yama","yoni","restraint","Venus"),
("Krittika","Agni","blade","purification","Sun"),
("Rohini","Prajapati","chariot","growth","Moon"),
("Mrigashira","Soma","deer head","search","Mars"),
("Ardra","Rudra","teardrop","destruction","Rahu"),
("Punarvasu","Aditi","quiver","renewal","Jupiter"),
("Pushya","Brihaspati","lotus","nourishment","Saturn"),
("Ashlesha","Nagas","serpent","entwining","Mercury"),
("Magha","Pitrs","throne","ancestry","Ketu"),
("Purva Phalguni","Bhaga","bed","enjoyment","Venus"),
("Uttara Phalguni","Aryaman","bed","contracts","Sun"),
("Hasta","Savitar","hand","manifestation","Moon"),
("Chitra","Tvashtar","pearl","creation","Mars"),
("Swati","Vayu","young shoot","independence","Rahu"),
("Vishakha","Indra-Agni","triumphal arch","achievement","Jupiter"),
("Anuradha","Mitra","lotus","devotion","Saturn"),
("Jyeshtha","Indra","earring","authority","Mercury"),
("Mula","Nirriti","roots","destruction","Ketu"),
("Purva Ashadha","Apas","fan","invigoration","Venus"),
("Uttara Ashadha","Vishvadevas","elephant tusk","victory","Sun"),
("Shravana","Vishnu","ear","listening","Moon"),
("Dhanishta","Vasus","drum","abundance","Mars"),
("Shatabhisha","Varuna","circle","healing","Rahu"),
("Purva Bhadrapada","Aja Ekapada","sword","transformation","Jupiter"),
("Uttara Bhadrapada","Ahirbudhnya","serpent","depth","Saturn"),
("Revati","Pushan","fish","protection","Mercury"),

]

template = """
# {name}

Node ID: nakshatra.{id}

---

## Core Symbolism

Deity: {deity}  
Symbol: {symbol}  
Shakti: {shakti}  
Ruling Planet: {planet}

---

## Cosmological Role

Nakshatra {name} represents a specific field of lunar consciousness within the Vedic cosmological system.

It functions as a node connecting:

• Graha influence  
• Mythic deity archetypes  
• Ritual symbolism  
• Psychological qualities  

---

## Research Notes

This card acts as a research surface.

Future layers may include:

• associated Rig Veda hymns
• deity mythology
• temple traditions
• yantra forms
• mantra correspondences
• Ayurvedic correlations

---

## Graph Relationships

nakshatra.{id}
→ system.jyotisha
→ deity.{deity_id}
→ graha.{planet_id}

"""

for n,deity,symbol,shakti,planet in nakshatras:

    nid = n.lower().replace(" ","_")
    deity_id = deity.lower().replace(" ","_")
    planet_id = planet.lower()

    text = template.format(
        name=n,
        id=nid,
        deity=deity,
        symbol=symbol,
        shakti=shakti,
        planet=planet,
        deity_id=deity_id,
        planet_id=planet_id
    )

    with open(f"{OUT}/{nid}.md","w") as f:
        f.write(text)

print("27 Nakshatra cards generated in:",OUT)
