import sys, os, re, json, time
sys.path.insert(0, r"E:\资料\论文抓取\_ref\pylibs")
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

OUT = r"E:\资料\论文抓取\曹老师论文"
os.makedirs(OUT, exist_ok=True)

ITEMS = [
 ("10.23919/ISAP47258.2021.9614460", "2021_ISAP_switchable_ground_plane", "IEEE"),
 ("10.1587/comex.2023TCL0008",       "2023_IEICE_COMEX_DOA_TMRA",         "J-STAGE"),
 ("10.1109/LAWP.2024.3508094",       "2024_AWPL_GAN_bifunctional",        "IEEE"),
 ("10.1364/OE.541287",               "2024_OE_DCGAN_quadchannel",         "Optica"),
 ("10.1109/ISAPE62431.2024.10841285","2024_ISAPE_freeform_holography",    "IEEE"),
 ("10.1109/APCAP62011.2024.10881350","2024_APCAP_Bessel_OAM",             "IEEE"),
 ("10.36227/techrxiv.172710059.98750657/v1", "2024_TechRxiv_transmitarray", "TechRxiv"),
 ("10.23919/ISAP63122.2025.11362042","2025_ISAP_GAN_multifunctional",     "IEEE"),
 ("10.23919/ISAP63122.2025.11361784","2025_ISAP_beamforming_TMRA",        "IEEE"),
 ("10.1049/mia2.70013",              "2025_IET_leakywave",                "Wiley"),
 ("10.1364/OE.581263",               "2026_OE_TM_metasurface_amp_phase",  "Optica"),
 ("10.1021/acsami.5c26257",          "2026_ACS_encryption_holography",    "ACS"),
 ("10.1109/LAWP.2026.3729810",       "2026_AWPL_pol_mux_metasurface",     "IEEE"),
 ("10.1049/cp.2018.0432",            "2018_EuCAP_smartwatch_antenna",     "IET"),
 ("10.1364/JOSAB.404062",            "2020_JOSAB_THz_absorber",           "Optica"),
]

report = []

def try_pdf(ctx, url, tag):
    """Fetch url with browser cookies; return bytes if PDF."""
    try:
        r = ctx.request.get(url, timeout=60000)
        body = r.body()
        if body[:4] == b"%PDF":
            return body
        head = body[:200].decode("utf-8", "ignore")
        return None
    except Exception:
        return None

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=False,
                          args=["--disable-blink-features=AutomationControlled", "--start-maximized"])
    ctx = b.new_context(locale="en-US", viewport=None,
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36 Edg/155.0.0.0")
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    pg = ctx.new_page()

    for doi, tag, site in ITEMS:
        path = os.path.join(OUT, tag + ".pdf")
        if os.path.exists(path) and os.path.getsize(path) > 50000:
            report.append((doi, tag, "skip-exists")); continue
        status = "fail"
        try:
            pg.goto("https://doi.org/" + doi, wait_until="commit", timeout=60000)
            # wait for WAF/challenge to settle
            for _ in range(12):
                pg.wait_for_timeout(2500)
                if len(pg.content()) > 15000:
                    break
            html = pg.content()
            m = re.search(r'<meta[^>]+name="citation_pdf_url"[^>]+content="([^"]+)"', html, re.I)
            cands = []
            if m:
                cands.append(m.group(1))
            if site == "Optica":
                mm = re.search(r'viewmedia\.cfm\?uri=([^"&]+)', html)
                if mm:
                    cands.append("https://opg.optica.org/oe/viewmedia.cfm?uri=" + mm.group(1) + "&seq=0")
            if site == "Wiley" or site == "IET":
                mm = re.search(r'(https?://[^"\']+/doi/(?:pdfdirect|pdf|epdf)/[^"\']+)', html)
                if mm: cands.append(mm.group(1))
            for u in cands:
                body = try_pdf(ctx, u, tag)
                if body:
                    open(path, "wb").write(body)
                    status = f"ok {len(body)//1024}KB"
                    break
            if status == "fail":
                # inspect why
                low = html.lower()
                why = []
                if "sign in" in low or "signin" in low: why.append("signin")
                if "purchase" in low: why.append("purchase")
                if "captcha" in low or "validate.perfdrive" in low: why.append("botwall")
                if "cloudflare" in low: why.append("cloudflare")
                status = "fail:" + ",".join(why)
        except Exception as e:
            status = "err:" + type(e).__name__
        print(f"{status:32s} {doi}")
        report.append((doi, tag, status))
    b.close()

json.dump(report, open(r"E:\资料\论文抓取\_ref\download_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
