import urllib.request, urllib.parse, ssl, json, sys, os, re
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
OUT = r"E:\资料\论文抓取\曹老师论文"

def fetch(url, data=None, headers=None, timeout=45):
    h = {"User-Agent": UA}
    if headers: h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h)
    return urllib.request.urlopen(req, timeout=timeout, context=ctx)

# 1) J-STAGE direct
u = "https://www.jstage.jst.go.jp/article/comex/12/8/12_2023TCL0008/_pdf"
try:
    r = fetch(u)
    body = r.read()
    print("JSTAGE", r.status, r.headers.get("Content-Type"), body[:4], len(body))
    if body[:4] == b"%PDF":
        open(os.path.join(OUT, "2023_IEICE_COMEX_DOA_TMRA.pdf"), "wb").write(body)
        print("saved JSTAGE")
except Exception as e:
    print("JSTAGE ERR", e)

# 2) Semantic Scholar batch
DOIS = [
 "10.23919/ISAP47258.2021.9614460","10.1587/comex.2023TCL0008","10.1109/LAWP.2024.3508094",
 "10.1364/OE.541287","10.1109/ISAPE62431.2024.10841285","10.1109/APCAP62011.2024.10881350",
 "10.36227/techrxiv.172710059.98750657/v1","10.23919/ISAP63122.2025.11362042",
 "10.23919/ISAP63122.2025.11361784","10.1049/mia2.70013","10.1364/OE.581263",
 "10.1021/acsami.5c26257","10.1109/LAWP.2026.3729810","10.1049/cp.2018.0432","10.1364/JOSAB.404062",
]
try:
    payload = json.dumps({"ids": ["DOI:" + d for d in DOIS]}).encode()
    r = fetch("https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,openAccessPdf,isOpenAccess,externalIds,venue,year",
              data=payload, headers={"Content-Type": "application/json"})
    data = json.loads(r.read().decode())
    print("\n=== S2 ===")
    for doi, d in zip(DOIS, data):
        if not d:
            print("none", doi); continue
        oa = d.get("openAccessPdf") or {}
        print(f"{doi}\n   isOA={d.get('isOpenAccess')} url={oa.get('url')} | {d.get('title','')[:60]}")
except Exception as e:
    print("S2 ERR", e)

# 3) arXiv search
try:
    q = urllib.parse.quote('au:"Xianbo Cao"')
    r = fetch(f"http://export.arxiv.org/api/query?search_query={q}&max_results=50")
    xml = r.read().decode("utf-8", "ignore")
    entries = re.findall(r"<entry>(.*?)</entry>", xml, re.S)
    print("\n=== arXiv entries:", len(entries))
    for e in entries:
        t = re.search(r"<title>(.*?)</title>", e, re.S).group(1).strip().replace("\n", " ")
        i = re.search(r"<id>(.*?)</id>", e).group(1)
        print(" ", t[:80], "|", i)
except Exception as e:
    print("arXiv ERR", e)
