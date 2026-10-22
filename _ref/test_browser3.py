import sys, os, re
sys.path.insert(0, r"E:\资料\论文抓取\_ref\pylibs")
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

URL = "https://ieeexplore.ieee.org/document/9614460"

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=False,
                          args=["--disable-blink-features=AutomationControlled", "--start-maximized"])
    ctx = b.new_context(locale="en-US", viewport=None,
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36 Edg/155.0.0.0")
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    pg = ctx.new_page()
    pg.goto(URL, wait_until="commit", timeout=60000)
    for i in range(10):
        pg.wait_for_timeout(3000)
        if len(pg.content()) > 20000:
            break
    html = pg.content()
    print("len", len(html))
    for kw in ["XIDIAN", "Access provided", "Sign in to continue", "Get PDF", "purchase", "Sign In"]:
        idx = html.lower().find(kw.lower())
        print(f"{kw!r}: index {idx}")
        if idx > 0:
            print("   ...", re.sub(r"\s+", " ", html[max(0, idx-160):idx+160]))
    # main content region
    try:
        main = pg.inner_text("xpl-document-details, .document-main, #article")
        print("---- main ----")
        print(main[:1500])
    except Exception as e:
        print("no main:", e)
    print("---- title ----", pg.title())
    b.close()
