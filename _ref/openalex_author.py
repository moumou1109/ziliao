import urllib.request, ssl, json, sys, os
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = "Mozilla/5.0 (research; mailto:research@example.com)"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept":"application/json"})
    with urllib.request.urlopen(req, timeout=40, context=ctx) as r:
        return json.loads(r.read().decode("utf-8"))

a = get("https://api.openalex.org/authors?search=Xianbo%20Cao&per_page=25")
for x in a["results"]:
    insts = x.get("last_known_institutions") or []
    inst_name = insts[0].get("display_name") if insts else None
    print(x["id"], "|", x["display_name"], "|", x["works_count"], "|", inst_name, "| alt:", x.get("display_name_alternatives"))
