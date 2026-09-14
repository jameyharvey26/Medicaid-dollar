import pathlib, subprocess, sys
import typst
ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "Medicaid_Dollars_National_TYPST.pdf"
typst.compile(str(ROOT / "paper_national.typ"), output=str(OUT),
              root=str(ROOT), font_paths=[str(ROOT / "paper_fonts")])
print("wrote", OUT, OUT.stat().st_size, "bytes")
sys.exit(subprocess.call(["python3", "whitespace.py", str(OUT)])
         or subprocess.call(["python3", "figurefit.py", str(OUT), "paper_national_v3.html"]))
