import sys, os, re
sys.path.insert(0, r"E:\资料\论文抓取\_ref\pylibs")
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

TESTS = [
 ("10.1364/OE.541287", "opg.optica.org"),
 ("10.1049/mia2.70013", "wiley.com"),
 ("10.36227/techrxiv.172710059.98750657/v1", "techrxiv"),
]

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=False,
                          args=["--disable-blink-features=AutomationControlled", "--start-maximized"])
    ctx = b.new_context(locale="en-US", viewport=None,
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36 Edg/155.0.0.0")
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    pg = ctx.new_page()
    for doi, host in TESTS:
        print("=" * 80)
        print(doi)
        try:
            pg.goto("https://doi.org/" + doi, wait_until="commit", timeout=60000)
            ok = False
            for i in range(14):
                pg.wait_for_timeout(3000)
                u = pg.url
                if host.split(".")[0] in u and "validate" not in u and "captcha" not in u:
                    ok = True
                    break
            print("  url:", pg.url[:120], "| settled:", ok, "| title:", pg.title()[:80])
            if ok:
                html = pg.content()
                m = re.search(r'<meta[^>]+name="citation_pdf_url"[^>]+content="([^"]+)"', html, re.I)
                print("  citation_pdf_url:", m.group(1) if m else None)
                links = re.findall(r'href="([^"]+\.pdf[^"]*)"', html, re.I)
                print("  pdf links:", links[:5])
        except Exception as e:
            print("  ERR", type(e).__name__, str(e)[:120])
    b.close()
