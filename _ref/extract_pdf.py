import sys, os, glob, json
sys.path.insert(0, r"E:\资料\论文抓取\_ref\pylibs")
sys.stdout.reconfigure(encoding="utf-8")
import fitz

D = r"E:\资料\论文抓取\曹老师论文"
TXT = r"E:\资料\论文抓取\_ref\txt"
os.makedirs(TXT, exist_ok=True)
out = []
for p in sorted(glob.glob(os.path.join(D, "*.pdf"))):
    doc = fitz.open(p)
    txt = []
    for i, page in enumerate(doc):
        txt.append(f"\n===== PAGE {i+1} =====\n" + page.get_text("text"))
    full = "".join(txt)
    name = os.path.splitext(os.path.basename(p))[0]
    open(os.path.join(TXT, name + ".txt"), "w", encoding="utf-8").write(full)
    meta = doc.metadata or {}
    out.append({"file": os.path.basename(p), "pages": doc.page_count, "chars": len(full),
                "title": meta.get("title"), "author": meta.get("author"), "subject": meta.get("subject")})
    print(f"{doc.page_count:>3} pages {len(full):>7} chars  {os.path.basename(p)}")
json.dump(out, open(os.path.join(TXT, "_index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
