import sys, os, glob, re
sys.stdout.reconfigure(encoding="utf-8")
TXT = r"E:\资料\论文抓取\_ref\txt"
files = [
 "A_1-bit_Time-Modulated_Reflectarray_for_Reconfigurable-Intelligent-Surface_Applications",
 "A_Systematic_Method_for_Efficient_Wireless_Powering_to_Implantable_Biomedical_Devices",
 "An_Ultrawideband_1-Bit_Reconfigurable_Reflectarray_Element_With_Improved_Angular_Stability",
 "Broadband_2_GHz_to_14_GHz_Dual-Polarized_Horn_Antenna_With_Stable_Unidirectional_Radiation_Patterns",
]
for f in files:
    t = open(os.path.join(TXT, f + ".txt"), encoding="utf-8").read()
    t = re.sub(r"\n(\d{1,2})\n", "\n", t)  # drop line numbers footnote noise
    print("#"*100); print(f)
    print("\n-- section headings --")
    for m in re.finditer(r"(?m)^\s*([IVX]{1,4}\.\s+[A-Z][A-Z \-]{2,60})$", t):
        print("  ", m.group(1).strip())
    print("\n-- figure captions --")
    for m in re.finditer(r"(?m)^Fig\.\s*\d+\.[^\n]{0,200}", t):
        print("  ", m.group(0).strip())
    print("\n-- conclusion --")
    i = t.upper().rfind("CONCLUSION")
    if i > 0:
        print(t[i:i+2600])
