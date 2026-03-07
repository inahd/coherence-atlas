import json, sys, urllib.parse, urllib.request
from pathlib import Path

MANI = Path("/opt/atlas/manifests")
MANI.mkdir(parents=True, exist_ok=True)

# Internet Archive AdvancedSearch API:
# https://archive.org/advancedsearch.php?q=...&fl[]=identifier&rows=50&page=1&output=json
BASE = "https://archive.org/advancedsearch.php"

QUERIES = {
    # Tune these freely; these are "starter" queries that usually return relevant scans/ebooks.
    "nakshatra": [
        'title:(nakshatra OR "book of nakshatras") OR (jyotish AND nakshatra) OR (astrology AND nakshatra)',
        'subject:(nakshatra OR jyotisha OR vedic-astrology) AND (text OR book OR handbook)'
    ],
    "tithi_nitya": [
        'title:(tithi OR "nitya devi" OR "nitya-devi" OR panchanga) OR (tithi AND mantra)',
        'subject:(panchanga OR tithi OR lunar) AND (vrata OR mantra OR devi)'
    ],
    "ritual": [
        'title:(vrata OR "vrata katha" OR "ritual calendar" OR panchanga) OR subject:(vrata OR vrata-katha)',
        'subject:(ritual OR vrata OR upavasa OR puja) AND (calendar OR lunar OR panchanga)'
    ],
    "music": [
        'title:(raga OR kirtan OR kirtana OR bhajan) OR subject:(raga OR kirtan OR bhajan)',
        'subject:(indian-music OR carnatic OR hindustani) AND (raga OR tala)'
    ],
    "plants": [
        'title:(ayurveda AND plants) OR title:(dravyaguna) OR subject:(medicinal-plants AND ayurveda)',
        'subject:(ayurveda OR dravyaguna) AND (plants OR materia-medica OR herbs)'
    ],
}

FL = ["identifier", "title", "mediatype", "collection"]

def fetch_ids(q: str, rows: int = 50, page: int = 1):
    params = {
        "q": q,
        "fl[]": FL,
        "rows": str(rows),
        "page": str(page),
        "output": "json",
    }
    url = BASE + "?" + urllib.parse.urlencode(params, doseq=True)
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8", errors="ignore"))
    docs = (data.get("response") or {}).get("docs") or []
    return docs

def make_urls(docs):
    # Use item details pages (stable). Downloader can later fetch PDFs/zip inside each item.
    out=[]
    for d in docs:
        ident = d.get("identifier")
        if not ident: 
            continue
        out.append(f"https://archive.org/details/{ident}")
    # de-dupe preserving order
    seen=set(); uniq=[]
    for u in out:
        if u in seen: 
            continue
        seen.add(u); uniq.append(u)
    return uniq

def write_manifest(domain: str, urls):
    path = MANI / f"wget_{domain}.txt"
    header = [
        "# Auto-generated from Internet Archive AdvancedSearch",
        "# Tip: prune to direct .pdf/.zip inside each item if desired.",
        "# One URL per line.",
        "",
    ]
    txt = "\n".join(header + urls) + "\n"
    path.write_text(txt, encoding="utf-8")
    print("Wrote:", path, "links:", len(urls))

def build(domain: str, n: int):
    qs = QUERIES.get(domain)
    if not qs:
        raise SystemExit(f"Unknown domain: {domain}. Use one of: {', '.join(sorted(QUERIES))} or 'all'.")

    all_docs=[]
    # pull multiple queries and a couple pages each
    for q in qs:
        for page in (1,2):
            docs = fetch_ids(q, rows=min(50, n), page=page)
            all_docs.extend(docs)

    urls = make_urls(all_docs)[:n]
    write_manifest(domain, urls)

def main():
    if len(sys.argv) < 2:
        print("Usage: ia_manifest.py <domain|all> [N]")
        raise SystemExit(2)
    domain = sys.argv[1].strip()
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 50

    if domain == "all":
        for d in QUERIES.keys():
            build(d, n)
    else:
        build(domain, n)

if __name__ == "__main__":
    main()
