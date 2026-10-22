import urllib.request, urllib.parse, ssl, json, sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = "Mozilla/5.0 PaperFetch/1.0"

def get(url, tries=4, accept="application/json"):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
            with urllib.request.urlopen(req, timeout=45, context=ctx) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if i == tries - 1:
                print("FAIL", url, e); return None
            time.sleep(4)

# --- Semantic Scholar author search
d = get("https://api.semanticscholar.org/graph/v1/author/search?query=Xianbo%20Cao&fields=name,affiliations,paperCount,externalIds")
print("S2 authors:", json.dumps(d, ensure_ascii=False)[:1500] if d else None)

# --- DBLP
d2 = get("https://dblp.org/search/publ/api?q=Xianbo+Cao&format=json&h=100")
if d2:
    hits = d2.get("result", {}).get("hits", {}).get("hit", [])
    print("\nDBLP hits:", len(hits))
    for h in hits:
        info = h["info"]
        auths = info.get("authors", {}).get("author", [])
        if isinstance(auths, dict): auths = [auths]
        names = [a.get("text") for a in auths]
        print(info.get("year"), "|", info.get("venue"), "|", info.get("title")[:80], "|", info.get("doi"), "|", names)
