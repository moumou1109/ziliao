import sys, os
sys.path.insert(0, r"E:\资料\论文抓取\_ref\pylibs")
sys.stdout.reconfigure(encoding="utf-8")
import pymupdf
p = r"E:\资料\论文抓取\曹老师论文\2023_IEICE_COMEX_DOA_TMRA.pdf"
doc = pymupdf.open(p)
print("pages", doc.page_count, "meta", doc.metadata.get("title"))
t = "".join(pg.get_text("text") for pg in doc)
open(r"E:\资料\论文抓取\_ref\txt\2023_IEICE_COMEX_DOA_TMRA.txt", "w", encoding="utf-8").write(t)
print(t[:2600])
