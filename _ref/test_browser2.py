import sys, os, time
sys.path.insert(0, r"E:\资料\论文抓取\_ref\pylibs")
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "https://ieeexplore.ieee.org/document/9614460"
os.makedirs(r"E:\资料\论文抓取\_ref\shots", exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=False,
                          args=["--disable-blink-features=AutomationControlled", "--start-maximized"])
    ctx = b.new_context(locale="en-US", viewport=None,
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36 Edg/155.0.0.0")
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    pg = ctx.new_page()
    resp = pg.goto(URL, wait_until="commit", timeout=60000)
    print("status", resp.status if resp else None)
    for i in range(6):
        pg.wait_for_timeout(5000)
        print(i, "url:", pg.url, "| title:", pg.title(), "| len:", len(pg.content()))
        if "ieeexplore.ieee.org/document" in pg.url and len(pg.content()) > 20000:
            break
    pg.screenshot(path=r"E:\资料\论文抓取\_ref\shots\ieee_test2.png")
    body = pg.inner_text("body")[:800]
    print("---- body ----")
    print(body)
    print("---- flags ----")
    c = pg.content().lower()
    for kw in ["sign in", "access provided by", "purchase", "pdf"]:
        print(kw, ":", kw in c)
    b.close()
