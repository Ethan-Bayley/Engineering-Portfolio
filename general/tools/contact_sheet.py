#!/usr/bin/env python3
"""Render slides with PowerPoint and tile them into contact sheets, so many slides can be seen in ONE image (layout review).

Usage:
  python general/tools/contact_sheet.py DECK.pptx [--slides 1-20] [--per-sheet 12] [--cols 4] [--thumb 800] [--out DIR] [--no-render]

Writes DIR/sheet_01.png, sheet_02.png ... (default DIR = project/outputs/renders/sheets/<deck name>) plus the per-slide PNGs in
DIR/slides/. Each tile is labelled with its slide number. Use 12 per sheet (4 x 3) to judge layout and type size, or 20 (5 x 4) to
judge rhythm across a section. Text is only readable at 12 per sheet; look at single slides for wording.
Needs Windows PowerPoint (same as render_check.ps1). The deck is opened read-only.
"""
import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent


def parse_slides(spec, n=None):
    if not spec:
        return None
    out = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def font(size):
    for name in ("segoeui.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck", type=Path)
    ap.add_argument("--slides", default="", help="e.g. 1-20 or 3,5,9-12 (default all)")
    ap.add_argument("--per-sheet", type=int, default=12)
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--thumb", type=int, default=800, help="tile width in px")
    ap.add_argument("--render-width", type=int, default=1600)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--no-render", action="store_true", help="reuse PNGs already in OUT/slides")
    a = ap.parse_args()

    out = a.out or (ROOT.parent / "project" / "outputs" / "renders" / "sheets" / a.deck.stem)
    slides_dir = out / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)
    wanted = parse_slides(a.slides)
    if not a.no_render:
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(TOOLS / "render_check.ps1"),
               "-Deck", str(a.deck.resolve()), "-OutDir", str(slides_dir), "-Width", str(a.render_width)]
        if wanted:
            cmd += ["-Only", ",".join(map(str, wanted))]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(r.stderr or r.stdout)
        print(r.stdout.strip())
    files = sorted(slides_dir.glob("s*.png"))
    if wanted:
        files = [f for f in files if int(f.stem[1:]) in wanted]
    if not files:
        sys.exit("no slide images found")
    for old in out.glob("sheet_*.png"):
        old.unlink()

    w0, h0 = Image.open(files[0]).size
    tw = a.thumb
    th = round(tw * h0 / w0)
    pad, head = 12, 26
    f = font(18)
    sheets = []
    for si in range(0, len(files), a.per_sheet):
        chunk = files[si:si + a.per_sheet]
        rows = -(-len(chunk) // a.cols)
        W = a.cols * (tw + pad) + pad
        H = rows * (th + head + pad) + pad
        sheet = Image.new("RGB", (W, H), (40, 44, 52))
        d = ImageDraw.Draw(sheet)
        for i, fp in enumerate(chunk):
            r, c = divmod(i, a.cols)
            x = pad + c * (tw + pad)
            y = pad + r * (th + head + pad)
            im = Image.open(fp).convert("RGB").resize((tw, th), Image.LANCZOS)
            sheet.paste(im, (x, y + head))
            d.text((x + 2, y + 2), f"slide {int(fp.stem[1:])}", fill=(255, 255, 255), font=f)
        p = out / f"sheet_{len(sheets) + 1:02d}.png"
        sheet.save(p)
        sheets.append(p)
    for p in sheets:
        print(p, Image.open(p).size)


if __name__ == "__main__":
    main()
