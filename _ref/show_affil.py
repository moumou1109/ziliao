import json, sys, os
sys.stdout.reconfigure(encoding="utf-8")
D = r"E:\资料\论文抓取\_ref"
rows = json.load(open(os.path.join(D, "openalex_works.json"), encoding="utf-8"))
for w in sorted(rows, key=lambda x: (x.get("publication_year") or 0)):
    print("="*100)
    print(w.get("publication_year"), w.get("title"))
    print("DOI:", w.get("doi"))
    for a in w.get("authorships", []):
        insts = [i.get("display_name") for i in a.get("institutions", [])]
        print("   -", a.get("author", {}).get("display_name"), "|", insts, "| raw:", (a.get("raw_affiliation_strings") or [None])[0])
