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
            if i == tries - 1:
                raise
            time.sleep(3)

items = {}
queries = [
    "Xianbo Cao",
    "Cao Xianbo",
]
for q in queries:
    cursor = "*"
    while True:
        url = ("https://api.crossref.org/works?query.author=" + urllib.parse.quote(q)
               + "&rows=200&cursor=" + urllib.parse.quote(cursor)
               + "&select=DOI,title,author,container-title,issued,type,publisher,link,member,event,page,volume")
        d = get_json(url)
        msg = d["message"]
        res = msg["items"]
        for it in res:
            names = [(a.get("given","")+" "+a.get("family","")).strip() for a in it.get("author",[])]
            hit = any(("xianbo" in n.lower() and "cao" in n.lower()) for n in names)
            if hit:
                items[it["DOI"].lower()] = it
        cursor = msg.get("next-cursor")
        print(q, "page", len(res), "total hit", len(items))
        if not cursor or len(res) == 0:
            break
        if msg["total-results"] and len(res) < 200:
            break

json.dump(items, open(os.path.join(D, "crossref_items.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved", len(items))
for doi, it in sorted(items.items(), key=lambda kv: kv[1].get("issued",{}).get("date-parts",[[0]])[0][0]):
    y = it.get("issued",{}).get("date-parts",[[0]])[0][0]
    print(y, "|", it.get("publisher"), "|", (it.get("container-title") or [""])[0][:60], "|", (it.get("title") or [""])[0][:70], "|", doi)
