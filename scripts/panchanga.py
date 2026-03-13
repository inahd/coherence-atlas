import swisseph as swe
import yaml
from datetime import datetime

# Julian day
now = datetime.utcnow()
jd = swe.julday(now.year, now.month, now.day)

# planetary longitudes
sun = swe.calc_ut(jd, swe.SUN)[0][0]
moon = swe.calc_ut(jd, swe.MOON)[0][0]

# tithi
tithi = int(((moon - sun) % 360) / 12) + 1

# nakshatra
nakshatra_index = int(moon / (360/27))

nakshatra_names = [
"Ashwini","Bharani","Krittika","Rohini","Mrigashira",
"Ardra","Punarvasu","Pushya","Ashlesha","Magha",
"Purva Phalguni","Uttara Phalguni","Hasta","Chitra",
"Swati","Vishakha","Anuradha","Jyeshtha","Mula",
"Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta",
"Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"
]

data = {
"date": now.strftime("%Y-%m-%d"),
"sun_longitude": sun,
"moon_longitude": moon,
"tithi": tithi,
"nakshatra": nakshatra_names[nakshatra_index]
}

file = f"/opt/atlas/panchanga/{data['date']}.yaml"

with open(file,"w") as f:
    yaml.dump(data,f)

print("Panchanga saved:", file)
