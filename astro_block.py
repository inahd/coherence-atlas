#!/usr/bin/env python3

import sys
import json
import swisseph as swe

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

RASHI = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE
}

DASHA_SEQUENCE = [
    ("Ketu", 7),
    ("Venus", 20),
    ("Sun", 6),
    ("Moon", 10),
    ("Mars", 7),
    ("Rahu", 18),
    ("Jupiter", 16),
    ("Saturn", 19),
    ("Mercury", 17),
]

def normalize_lon(lon):
    return lon % 360.0

def rashi_name(lon):
    lon = normalize_lon(lon)
    return RASHI[int(lon // 30)]

def nakshatra_name(lon):
    lon = normalize_lon(lon)
    size = 360.0 / 27.0
    return NAKSHATRAS[int(lon // size)]

def pada_number(lon):
    lon = normalize_lon(lon)
    size = 360.0 / 108.0
    return int(lon // size) % 4 + 1

def navamsa_sign_index(lon):
    lon = normalize_lon(lon)
    sign_index = int(lon // 30.0)
    part_index = int((lon % 30.0) // (30.0 / 9.0))
    return (sign_index * 9 + part_index) % 12

def navamsa_name(lon):
    return RASHI[navamsa_sign_index(lon)]

def build_body_record(lon):
    lon = normalize_lon(lon)
    return {
        "longitude": round(lon, 2),
        "rashi": rashi_name(lon),
        "nakshatra": nakshatra_name(lon),
        "pada": pada_number(lon),
        "navamsa_sign": navamsa_name(lon),
    }

def compute_planets(jd):
    data = {}

    for name, body in PLANETS.items():
        lon = swe.calc_ut(jd, body)[0][0]
        data[name] = build_body_record(lon)

        if name == "Rahu":
            ketu_lon = normalize_lon(lon + 180.0)
            data["Ketu"] = build_body_record(ketu_lon)

    return data

def compute_houses(jd, lat, lon):
    cusps, ascmc = swe.houses(jd, lat, lon)

    house_data = {}
    for i in range(12):
        cusp_lon = normalize_lon(cusps[i])
        house_data[f"house_{i+1}"] = {
            "longitude": round(cusp_lon, 2),
            "rashi": rashi_name(cusp_lon),
            "nakshatra": nakshatra_name(cusp_lon),
        }

    asc = normalize_lon(ascmc[0])
    return asc, house_data

def moon_dasha_start(moon_lon):
    size = 360.0 / 27.0
    nak_index = int(normalize_lon(moon_lon) // size)
    fraction_elapsed = (normalize_lon(moon_lon) % size) / size
    lord, years = DASHA_SEQUENCE[nak_index % 9]
    balance = years * (1.0 - fraction_elapsed)
    return lord, balance, nak_index

def generate_vimshottari_dasha(moon_lon):
    _, balance, nak_index = moon_dasha_start(moon_lon)

    dasha = []
    index = nak_index % 9

    dasha.append({
        "lord": DASHA_SEQUENCE[index][0],
        "years": round(balance, 2)
    })

    index = (index + 1) % 9

    for _ in range(8):
        lord, years = DASHA_SEQUENCE[index]
        dasha.append({
            "lord": lord,
            "years": years
        })
        index = (index + 1) % 9

    return dasha

def house_from_lagna(body_lon, asc_lon):
    diff = normalize_lon(body_lon - asc_lon)
    return int(diff // 30.0) + 1

def add_house_placements(planets, asc_lon):
    placed = {}
    for name, rec in planets.items():
        body_lon = rec["longitude"]
        enriched = dict(rec)
        enriched["house_from_lagna"] = house_from_lagna(body_lon, asc_lon)
        placed[name] = enriched
    return placed

def generate_chart(year, month, day, hour, lat, lon):
    jd = swe.julday(year, month, day, hour)

    planets = compute_planets(jd)
    asc_lon, houses = compute_houses(jd, lat, lon)
    planets = add_house_placements(planets, asc_lon)

    lagna = {
        "longitude": round(asc_lon, 2),
        "rashi": rashi_name(asc_lon),
        "nakshatra": nakshatra_name(asc_lon),
        "pada": pada_number(asc_lon),
        "navamsa_sign": navamsa_name(asc_lon),
    }

    moon_lon = planets["Moon"]["longitude"]
    vimshottari_dasha = generate_vimshottari_dasha(moon_lon)

    navamsa = {}
    for name, rec in planets.items():
        navamsa[name] = {
            "navamsa_sign": rec["navamsa_sign"]
        }

    return {
        "input": {
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "latitude": lat,
            "longitude": lon,
        },
        "lagna": lagna,
        "planets": planets,
        "houses": houses,
        "navamsa": navamsa,
        "vimshottari_dasha": vimshottari_dasha,
    }

def main():
    if len(sys.argv) != 7:
        print("usage: python /opt/atlas/astro_block.py YEAR MONTH DAY HOUR LAT LON")
        sys.exit(1)

    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])
    hour = float(sys.argv[4])
    lat = float(sys.argv[5])
    lon = float(sys.argv[6])

    chart = generate_chart(year, month, day, hour, lat, lon)
    print(json.dumps(chart, indent=2))

if __name__ == "__main__":
    main()
