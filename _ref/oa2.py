import urllib.request, urllib.parse, ssl, json, sys, re, time
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=45, context=ctx) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception as e:
            if i == tries - 1:
                print("ERR", url, e); return ""
            time.sleep(5)

# arXiv
xml = get("https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote('au:"Xianbo Cao"') + "&max_results=50")
entries = re.findall(r"<entry>(.*?)</entry>", xml, re.S)
print("arXiv entries:", len(entries))
for e in entries:
    t = re.search(r"<title>(.*?)</title>", e, re.S)
    i = re.search(r"<id>(.*?)</id>", e)
    print("  ", t.group(1).strip().replace("\n", " ")[:90] if t else "?", "|", i.group(1) if i else "?")

# CiNii (Tohoku repository / Japanese literature)
d = get("https://ci.nii.ac.jp/opensearch/search?q=" + urllib.parse.quote("Cao Xianbo") + "&format=json&count=50")
try:
    j = json.loads(d)
    items = j.get("@graph", [{}])[0].get("items", [])
    print("\nCiNii items:", len(items))
    for it in items[:20]:
        print("  ", (it.get("title") or "")[:80], "|", it.get("dc:date"), "|", it.get("link", {}).get("@id"))
except Exception as e:
    print("CiNii parse err", e, d[:200])
