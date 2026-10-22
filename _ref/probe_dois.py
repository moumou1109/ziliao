import urllib.request, urllib.parse, ssl, json, sys, os, re, time
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
H = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8",
     "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8"}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return urllib.request.HTTPRedirectHandler.redirect_request(self, req, fp, code, msg, headers, newurl)

def open_url(url, timeout=40):
    req = urllib.request.Request(url, headers=H)
    return urllib.request.urlopen(req, timeout=timeout, context=ctx)

DOIS = [
 ("10.23919/ISAP47258.2021.9614460", "ISAP2021_switchable_ground"),
 ("10.1587/comex.2023TCL0008", "IEICE2023_DOA_TMRA"),
 ("10.1109/LAWP.2024.3508094", "AWPL2024_GAN_bifunctional"),
 ("10.1364/OE.541287", "OE2024_DCGAN_quadchannel"),
 ("10.1109/ISAPE62431.2024.10841285", "ISAPE2024_freeform_holography"),
 ("10.1109/APCAP62011.2024.10881350", "APCAP2024_Bessel_OAM"),
 ("10.36227/techrxiv.172710059.98750657/v1", "TechRxiv2024_transmitarray"),
 ("10.23919/ISAP63122.2025.11362042", "ISAP2025_GAN_multifunctional"),
 ("10.23919/ISAP63122.2025.11361784", "ISAP2025_beamforming_TMRA"),
 ("10.1049/mia2.70013", "IET2025_leakywave"),
 ("10.1364/OE.581263", "OE2026_TM_meta_amp_phase"),
 ("10.1021/acsami.5c26257", "ACS2026_encryption_holography"),
 ("10.1109/LAWP.2026.3729810", "AWPL2026_pol_mux_metasurface"),
 ("10.1049/cp.2018.0432", "EuCAP2018_smartwatch"),
 ("10.1364/JOSAB.404062", "JOSAB2020_THz_absorber"),
]

for doi, tag in DOIS:
    url = "https://doi.org/" + doi
    try:
        r = open_url(url)
        final = r.geturl()
        ctype = r.headers.get("Content-Type", "")
        body = r.read()
    except Exception as e:
        print(f"[ERR ] {doi} {type(e).__name__}: {str(e)[:110]}")
        continue
    head = body[:4]
    print(f"[{'PDF ' if head == b'%PDF' else 'HTML'}] {doi}\n       -> {final} ({ctype.split(';')[0]}, {len(body)}B)")
    if head == b"%PDF":
        open(os.path.join(r"E:\资料\论文抓取\_ref\dl", tag + ".pdf"), "wb").write(body)
        continue
    html = body.decode("utf-8", "ignore")
    m = re.search(r'<meta[^>]+name="citation_pdf_url"[^>]+content="([^"]+)"', html, re.I)
    cands = []
    if m: cands.append(("citation_pdf_url", m.group(1)))
    for mm in re.finditer(r'href="([^"]*(?:\.pdf|pdfdirect|viewmedia|/pdf/)[^"]*)"', html, re.I):
        u = mm.group(1)
        if u.startswith("/"):
            u = urllib.parse.urljoin(final, u)
        if u not in [c[1] for c in cands]:
            cands.append(("link", u))
    for kind, u in cands[:4]:
        print(f"       cand[{kind}] {u[:120]}")
