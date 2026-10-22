import sys, os, re
sys.path.insert(0, r"E:\资料\论文抓取\_ref\pylibs")
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "https://ieeexplore.ieee.org/document/9614460"

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True,
                          args=["--disable-blink-features=AutomationControlled"])
    ctx = b.new_context(locale="en-US", viewport={"width": 1440, "height": 900},
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36 Edg/155.0.0.0")
    pg = ctx.new_page()
    try:
        resp = pg.goto(URL, wait_until="domcontentloaded", timeout=60000)
        print("status", resp.status if resp else None)
    except Exception as e:
        print("goto err", e)
    pg.wait_for_timeout(8000)
    print("title:", pg.title())
    txt = pg.inner_text("body")[:1200]
    print("---- body head ----")
    print(txt)
    print("---- flags ----")
    for kw in ["Sign In", "Access Provided by", "Institutional Sign In", "Purchase", "Download PDF", "PDF"]:
        print(kw, ":", kw.lower() in pg.content().lower())
    os.makedirs(r"E:\资料\论文抓取\_ref\shots", exist_ok=True)
    pg.screenshot(path=r"E:\资料\论文抓取\_ref\shots\ieee_test.png", full_page=False)
    b.close()
