import urllib.request, urllib.parse, ssl, json, sys, time
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = "PaperFetch/1.0 (academic use)"

def get(url, data=None, hdr=None, tries=4, wait=20):
    for i in range(tries):
        try:
            h = {"User-Agent": UA}
            if hdr: h.update(hdr)
            req = urllib.request.Request(url, data=data, headers=h)
            with urllib.request.urlopen(req, timeout=45, context=ctx) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception as e:
            code = getattr(e, "code", None)
            print(f"  attempt {i+1}: {code or e}")
            if i == tries - 1: return ""
            time.sleep(wait)

print("== arXiv ==")
x = get("https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote('au:"Xianbo Cao"') + "&max_results=50")
import re
ents = re.findall(r"<entry>(.*?)</entry>", x, re.S)
print("entries", len(ents))
for e in ents:
    t = re.search(r"<title>(.*?)</title>", e, re.S)
    i = re.search(r"<id>(.*?)</id>", e)
    print(" ", (t.group(1).strip().replace("\n"," ") if t else "?")[:90], "|", i.group(1) if i else "?")

print("\n== S2 ==")
DOIS = ["10.23919/ISAP47258.2021.9614460","10.1109/LAWP.2024.3508094","10.1364/OE.541287",
        "10.1109/ISAPE62431.2024.10841285","10.1109/APCAP62011.2024.10881350","10.23919/ISAP63122.2025.11362042",
        "10.23919/ISAP63122.2025.11361784","10.1049/mia2.70013","10.1364/OE.581263",
        "10.1021/acsami.5c26257","10.1109/LAWP.2026.3729810","10.1049/cp.2018.0432","10.1364/JOSAB.404062",
        "10.36227/techrxiv.172710059.98750657/v1"]
body = json.dumps({"ids": ["DOI:" + d for d in DOIS]}).encode()
raw = get("https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,openAccessPdf,isOpenAccess",
          data=body, hdr={"Content-Type": "application/json"}, wait=25)
if raw:
    data = json.loads(raw)
    for doi, d in zip(DOIS, data):
        if not d: print("  none", doi); continue
        print(" ", doi, "| OA:", d.get("isOpenAccess"), "|", (d.get("openAccessPdf") or {}).get("url"))
