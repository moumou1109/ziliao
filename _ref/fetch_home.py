import urllib.request, ssl, os, re, sys, io

sys.stdout.reconfigure(encoding="utf-8")
D = r"E:\资料\论文抓取\_ref"
os.makedirs(D, exist_ok=True)

url = "https://hz.xidian.edu.cn/info/1277/25374.htm"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
})
with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
    raw = r.read()
print("bytes", len(raw))
open(os.path.join(D, "homepage.html"), "wb").write(raw)

# decode
for enc in ("utf-8", "gbk", "gb18030"):
    try:
        html = raw.decode(enc)
        if "<html" in html.lower() or "<div" in html.lower():
            print("decoded with", enc)
            break
    except UnicodeDecodeError:
        continue
open(os.path.join(D, "homepage.decoded.html"), "w", encoding="utf-8").write(html)

# strip scripts/styles, extract text
t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
t = re.sub(r"(?is)<br\s*/?>", "\n", t)
t = re.sub(r"(?is)</(p|div|li|tr|h\d|table)>", "\n", t)
t = re.sub(r"(?s)<[^>]+>", " ", t)
import html as h
t = h.unescape(t)
lines = [re.sub(r"[ \t\u3000\xa0]+", " ", ln).strip() for ln in t.splitlines()]
lines = [ln for ln in lines if ln]
text = "\n".join(lines)
open(os.path.join(D, "homepage.txt"), "w", encoding="utf-8").write(text)
print("text lines", len(lines))
print(text[:3000])
