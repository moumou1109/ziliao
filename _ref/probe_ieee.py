import urllib.request, ssl, sys
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
H = {
 "User-Agent": UA,
 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
 "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
 "Accept-Encoding": "identity",
 "Connection": "keep-alive",
 "Upgrade-Insecure-Requests": "1",
 "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1",
}
urls = [
 "https://ieeexplore.ieee.org/document/10042453",
 "https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10042453",
 "https://ieeexplore.ieee.org/rest/search",
]
for u in urls:
    try:
        req = urllib.request.Request(u, headers=H)
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
            print("OK", r.status, u, r.headers.get("Content-Type"))
            print(r.read(500)[:500])
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, u, dict(list(e.headers.items())[:6]))
        print(e.read(400)[:400])
    except Exception as e:
        print("ERR", u, type(e).__name__, str(e)[:150])
    print("-"*70)
