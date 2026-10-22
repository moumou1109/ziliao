import urllib.request, ssl, json, sys, time
sys.stdout.reconfigure(encoding="utf-8")
c = ssl.create_default_context(); c.check_hostname=False; c.verify_mode=ssl.CERT_NONE
DOIS = ["10.23919/ISAP47258.2021.9614460","10.1587/comex.2023TCL0008","10.1109/LAWP.2024.3508094",
        "10.1364/OE.541287","10.1109/ISAPE62431.2024.10841285","10.1109/APCAP62011.2024.10881350",
        "10.36227/techrxiv.172710059.98750657/v1","10.23919/ISAP63122.2025.11362042",
        "10.23919/ISAP63122.2025.11361784","10.1049/mia2.70013","10.1364/OE.581263",
        "10.1021/acsami.5c26257","10.1109/LAWP.2026.3729810","10.1049/cp.2018.0432","10.1364/JOSAB.404062"]
for doi in DOIS:
    u = f"https://api.unpaywall.org/v2/{doi}?email=unpaywall@impactstory.org"
    try:
        d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0"}), timeout=30, context=c).read().decode())
    except Exception as e:
        print("ERR", doi, e); continue
    print(f"{doi}  is_oa={d.get('is_oa')}  oa_status={d.get('oa_status')}")
    for loc in (d.get("oa_locations") or []):
        print("    ", loc.get("host_type"), "|", loc.get("version"), "|", loc.get("url_for_pdf") or loc.get("url"))
    time.sleep(0.3)
