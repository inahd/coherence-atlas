import json
from pathlib import Path

REPORTS = Path("/opt/atlas/memory/reports")
GAPS = REPORTS / "gaps.json"
OUT = REPORTS / "next_domain.txt"

# Map gap buckets to wget manifest domains (your wget_cycle.sh uses these)
BUCKET_TO_DOMAIN = {
    "nakshatra_deity": "nakshatra",
    "nakshatra_graha": "nakshatra",
    "nakshatra_plants": "plants",
    "devi_weapon": "tithi_nitya",
    "ritual_calendar": "ritual",
    "raga_ritual": "music",
}

def main():
    if not GAPS.exists():
        OUT.write_text("nakshatra\n", encoding="utf-8")
        print("No gaps.json; defaulting to nakshatra")
        return

    data = json.loads(GAPS.read_text(encoding="utf-8"))
    prioritized = data.get("prioritized", [])
    if not prioritized:
        OUT.write_text("nakshatra\n", encoding="utf-8")
        print("Empty prioritized; defaulting to nakshatra")
        return

    # Pick first bucket with non-zero score that maps to a domain
    for item in prioritized:
        b = item.get("bucket")
        score = item.get("score", 0)
        if score <= 0:
            continue
        dom = BUCKET_TO_DOMAIN.get(b)
        if dom:
            OUT.write_text(dom + "\n", encoding="utf-8")
            print("Picked domain:", dom, "from bucket:", b, "score:", int(score))
            return

    OUT.write_text("nakshatra\n", encoding="utf-8")
    print("No matching buckets; defaulting to nakshatra")

if __name__ == "__main__":
    main()
