import json
import ephem
from datetime import datetime

DATA_FILE="/opt/atlas/data/cosmology.json"

def lunar_tithi():

    moon=ephem.Moon()
    moon.compute(datetime.utcnow())

    phase=moon.phase

    tithi=int((phase/100)*30)+1

    return tithi

def run():

    with open(DATA_FILE) as f:
        data=json.load(f)

    tithi_index=lunar_tithi()

    tithi=data["tithis"][(tithi_index-1) % len(data["tithis"])]

    print("\nAtlas Ritual Calendar\n")

    print("Current Lunar Phase (approx tithi):",tithi_index)
    print("Tithi:",tithi["name"])
    print("Associated Devi:",tithi["associated_devi"])

    if tithi["weapons"]:
        print("Weapons:",", ".join(tithi["weapons"]))

    if tithi["nakshatra_associations"]:
        print("Nakshatra:",", ".join(tithi["nakshatra_associations"]))

    if tithi["music_associations"]:
        print("Music:",", ".join(tithi["music_associations"]))

if __name__=="__main__":
    run()
