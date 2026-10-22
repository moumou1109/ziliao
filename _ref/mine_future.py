import sys, os, re
sys.stdout.reconfigure(encoding="utf-8")
TXT = r"E:\资料\论文抓取\_ref\txt"
FILES = {
 "TAP2023_TMRA": "A_1-bit_Time-Modulated_Reflectarray_for_Reconfigurable-Intelligent-Surface_Applications",
 "TAP2023_WPT": "A_Systematic_Method_for_Efficient_Wireless_Powering_to_Implantable_Biomedical_Devices",
 "AWPL2026_ELEM": "An_Ultrawideband_1-Bit_Reconfigurable_Reflectarray_Element_With_Improved_Angular_Stability",
 "AWPL2026_HORN": "Broadband_2_GHz_to_14_GHz_Dual-Polarized_Horn_Antenna_With_Stable_Unidirectional_Radiation_Patterns",
 "COMEX2023": "2023_IEICE_COMEX_DOA_TMRA",
}
PAT = re.compile(r"(future|further|limitation|limitations|however|drawback|remaining|next step|beyond the scope|not considered|remains)", re.I)
for tag, f in FILES.items():
    t = open(os.path.join(TXT, f + ".txt"), encoding="utf-8").read()
    t = re.sub(r"\n\s*\d{1,2}\s*\n", "\n", t)
    t = re.sub(r"\s+", " ", t)
    print("=" * 100); print(tag)
    sents = re.split(r"(?<=[.!?])\s+", t)
    for s in sents:
        if 20 < len(s) < 400 and PAT.search(s) and not re.search(r"\[\d+\]", s[:40]):
            print("  •", s.strip()[:330])
