import urllib.request, urllib.parse, ssl, json, sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = "PaperFetch/1.0 (mailto:research@example.com)"
D = r"E:\资料\论文抓取\_ref"

def get_json(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=45, context=ctx) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(3)

def search(url):
    d = get_json(url)
    out = []
    for it in d["message"]["items"]:
        names = [(a.get("given","") + " " + a.get("family","")).strip() for a in it.get("author", [])]
        if any("xianbo" in n.lower() and "cao" in n.lower() for n in names):
            out.append(it)
    return out, d["message"].get("total-results")

pools = {}
# IEEE (member 263) with relevance sort, first 3 pages
for offset in (0, 100, 200):
    url = ("https://api.crossref.org/works?query.author=Xianbo+Cao&filter=member:263"
           f"&rows=100&offset={offset}&select=DOI,title,author,container-title,issued,type,publisher,page,volume,event")
    res, total = search(url)
    print("IEEE offset", offset, "total", total, "hits", len(res))
    for it in res: pools[it["DOI"].lower()] = it

# IEICE (member 77)
for offset in (0, 100):
    url = ("https://api.crossref.org/works?query.author=Xianbo+Cao&filter=member:77"
           f"&rows=100&offset={offset}&select=DOI,title,author,container-title,issued,type,publisher,page,volume,event")
    res, total = search(url)
    print("IEICE offset", offset, "total", total, "hits", len(res))
    for it in res: pools[it["DOI"].lower()] = it

json.dump(pools, open(os.path.join(D, "crossref_ieee.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("unique", len(pools))
for doi, it in sorted(pools.items()):
    y = (it.get("issued", {}).get("date-parts") or [[0]])[0][0]
    print(y, "|", it.get("publisher"), "|", (it.get("container-title") or [""])[0][:55], "|", (it.get("title") or [""])[0][:75], "|", doi)
