import urllib.request, ssl, json, sys, time
sys.stdout.reconfigure(encoding="utf-8")
c = ssl.create_default_context(); c.check_hostname=False; c.verify_mode=ssl.CERT_NONE
UA = "PaperFetch/1.0 (academic use)"
DOIS = ["10.1109/LAWP.2024.3508094", "10.1364/OE.541287", "10.1109/ISAPE62431.2024.10841285",
        "10.23919/ISAP63122.2025.11362042", "10.1021/acsami.5c26257"]

def post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"User-Agent": UA, "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=45, context=c).read().decode())

try:
    data = post("https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,abstract,venue,year,authors",
                {"ids": ["DOI:" + d for d in DOIS]})
except Exception as e:
    print("S2 ERR", e); data = [None] * len(DOIS)

for d in DOIS:
    print("=" * 90); print(d)
# map back by order
for doi, d in zip(DOIS, data):
    print("=" * 90)
    print(doi)
    if d:
        print("TITLE:", d.get("title"))
        print("VENUE:", d.get("venue"), d.get("year"))
        print("AUTHORS:", ", ".join(a["name"] for a in d.get("authors", [])))
        ab = d.get("abstract")
        print("ABSTRACT:", (ab[:900] + "...") if ab else None)
    else:
        print("  (no S2 record)")
