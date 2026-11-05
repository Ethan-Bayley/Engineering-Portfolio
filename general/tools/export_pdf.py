"""Export a design-system deck to PDF with Inter really embedded, and optionally render PNGs of that same copy.

    python general/tools/export_pdf.py project/outputs/brochure/brochure_v01.pptx
    python general/tools/export_pdf.py <deck.pptx> --render project/outputs/renders/<name>

Why: on this PC Inter is installed as a variable font, and PowerPoint cannot put a variable font in a PDF, so it
silently uses Calibri. A static copy installed under the same family name "Inter" does not help (Windows still picks
the variable one). What works (tested 2026-10-22): the static Regular and Bold from assets/fonts/Inter, renamed to
the family "Inter Static" and installed for this Windows user. This tool copies the deck, changes the copy's font
name from "Inter" to "Inter Static", and exports that copy, so the .pptx itself keeps asking for plain "Inter".
A project can bring its own static fonts in project/design/fonts/ (any folder depth, .ttf): they are loaded too and
allowed in the PDF. The PDF is written next to the deck (<deck>.pdf). It refuses to finish if a font fell back to
Calibri or Arial, or if the PDF has a font that is neither Inter Static nor one of the project's fonts.
PowerPoint is never quit while it has other presentations open (it may be the user's own window).
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[2]
PROJECT_FONTS = ROOT / "project" / "design" / "fonts"


def project_fonts():
    """The project's own static fonts: [(path, PostScript name)]."""
    out = []
    for f in sorted(PROJECT_FONTS.rglob("*.ttf")) if PROJECT_FONTS.is_dir() else []:
        try:
            from fontTools.ttLib import TTFont
            out.append((f, TTFont(f)["name"].getDebugName(6) or f.stem))
        except Exception:                     # fontTools missing or an odd file: fall back to the file name
            out.append((f, f.stem))
    return out

PS_EXPORT = r"""
$pp = New-Object -ComObject PowerPoint.Application
$p = $pp.Presentations.Open('{deck}', $true, $false, $false)
try {{ $p.SaveAs('{pdf}', 32) }} finally {{ $p.Close(); if ($pp.Presentations.Count -eq 0) {{ $pp.Quit() }} }}
"""


def static_copy(deck, out):
    """Copy deck to out with every typeface="Inter" changed to "Inter Static". Returns the number of changes."""
    n = 0
    with zipfile.ZipFile(deck) as zin, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.endswith(".xml"):
                text, k = re.subn(r'typeface="Inter"', 'typeface="Inter Static"', data.decode("utf-8"))
                n += k
                data = text.encode("utf-8")
            zout.writestr(item, data)
    return n


def fonts_in(pdf):
    d = pymupdf.open(pdf)
    return sorted({f[3].split("+")[-1] for pg in d for f in pg.get_fonts()}), len(d)


def load_fonts():
    """Load the static Inter into this Windows session and tell running programs (PowerPoint included) about it.

    Needed on 2026-10-23: after a restart the running PowerPoint did not see "Inter Static" although it was installed,
    and exported Calibri. Loading the files with AddFontResource and broadcasting WM_FONTCHANGE fixed it at once."""
    import ctypes
    import os
    folder = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts"
    loaded = 0
    for name in ("InterStatic-Regular.ttf", "InterStatic-Bold.ttf"):
        f = folder / name
        if f.exists():
            loaded += ctypes.windll.gdi32.AddFontResourceW(str(f))
    for f, _name in project_fonts():
        installed = folder / f.name
        loaded += ctypes.windll.gdi32.AddFontResourceW(str(installed if installed.exists() else f))
    ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001D, 0, 0, 2, 3000, None)
    return loaded


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck")
    ap.add_argument("--render", help="also render PNGs (and the overflow report) of the Inter Static copy into this folder")
    a = ap.parse_args(argv)
    load_fonts()
    deck = Path(a.deck).resolve()
    pdf = deck.with_suffix(".pdf")
    tmp = Path(tempfile.mkdtemp()) / (deck.stem + "_interstatic.pptx")
    n = static_copy(deck, tmp)
    ps = PS_EXPORT.format(deck=str(tmp).replace("'", "''"), pdf=str(pdf).replace("'", "''"))
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    fonts, pages = fonts_in(pdf)
    print(f"{pdf}  ({pages} pages, {n} font references switched)  fonts: {', '.join(fonts)}")
    allowed = ("InterStatic",) + tuple(n for _f, n in project_fonts())
    other = [f for f in fonts if not f.startswith(allowed)]
    if other or not fonts:
        sys.exit(f"PDF uses other fonts: {', '.join(other)}. Install the fonts once with general/tools/install_fonts.ps1.")
    if a.render:
        script = Path(__file__).with_name("render_check.ps1")
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), "-Deck", str(tmp),
                        "-OutDir", a.render, "-Width", "1800"], check=True)
    shutil.rmtree(tmp.parent, ignore_errors=True)


if __name__ == "__main__":
    main()
