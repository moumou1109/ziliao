import urllib.request, ssl, json, sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = "Mozilla/5.0 (research; mailto:research@example.com)"
D = r"E:\资料\论文抓取\_ref"

def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept":"application/json"})
            with urllib.request.urlopen(req, timeout=40, context=ctx) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if i == tries-1: raise
            time.sleep(2)

rows = []
cursor = "*"
while True:
    u = ("https://api.openalex.org/works?filter=author.id:A5015198160"
         f"&per_page=200&cursor={cursor}&select=id,doi,title,publication_year,type,"
         "primary_location,authorships,open_access,best_oa_location,ids,cited_by_count")
    d = get(u)
    rows += d["results"]
    cursor = d["meta"].get("next_cursor")
    if not cursor: break

print("works:", len(rows))
json.dump(rows, open(os.path.join(D, "openalex_works.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for w in sorted(rows, key=lambda x: (x.get("publication_year") or 0)):
    loc = w.get("primary_location") or {}
    src = (loc.get("source") or {}).get("display_name")
    oa = w.get("open_access") or {}
    print(w.get("publication_year"), "|", (w.get("title") or "")[:90], "|", src, "|", w.get("type"), "|", oa.get("is_oa"), oa.get("oa_url"))
