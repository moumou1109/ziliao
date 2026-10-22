import urllib.request, urllib.parse, ssl, json, sys
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

DOIS = [
 "10.23919/ISAP47258.2021.9614460",
 "10.1587/comex.2023TCL0008",
 "10.1109/LAWP.2024.3508094",
 "10.1364/OE.541287",
 "10.1109/ISAPE62431.2024.10841285",
 "10.1109/APCAP62011.2024.10881350",
 "10.36227/techrxiv.172710059.98750657/v1",
 "10.23919/ISAP63122.2025.11362042",
 "10.23919/ISAP63122.2025.11361784",
 "10.1049/mia2.70013",
 "10.1364/OE.581263",
 "10.1021/acsami.5c26257",
 "10.1109/LAWP.2026.3729810",
 "10.1049/cp.2018.0432",
 "10.1364/JOSAB.404062",
]

for doi in DOIS:
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email=research@example.com"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        d = json.loads(urllib.request.urlopen(req, timeout=30, context=ctx).read().decode())
    except Exception as e:
        print("ERR", doi, e); continue
    print("="*90)
    print(doi, "| is_oa:", d.get("is_oa"), "|", d.get("journal_name") or d.get("publisher"))
    for loc in (d.get("oa_locations") or []):
        print("   ->", loc.get("host_type"), "|", loc.get("url_for_pdf"), "|", loc.get("url"), "|", loc.get("version"))
