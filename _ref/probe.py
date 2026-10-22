import urllib.request, ssl, json, sys
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
for url in ["https://ieeexplore.ieee.org/", "https://ieeexplore.ieee.org/xpl/author/37085768500",
            "https://api.crossref.org/works?query.author=Xianbo+Cao&rows=2"]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language":"en-US,en;q=0.9"})
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
            body = r.read(3000)
            print("OK", r.status, url, "len>", len(body))
            print(body[:300])
    except Exception as e:
        print("ERR", url, type(e).__name__, str(e)[:200])
    print("-"*60)
