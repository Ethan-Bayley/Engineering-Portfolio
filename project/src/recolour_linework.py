"""Recolour the team's CAD line drawings to the portfolio colours. The originals are never changed.

    python project/src/recolour_linework.py              # every drawing -> assets/cad/linework_page/*.png (100 % fills, see-through page)
    python project/src/recolour_linework.py --strengths  # also highlighted drawings at fill 50..100 %, colour-corrected
    python project/src/recolour_linework.py --light      # dark-line copies for a white page -> assets/cad/linework_light

Each pixel of a drawing is read as a mix of three colours: the background (#333333), the white lines and the orange
highlight (#FFA500). The mix is solved per pixel (least squares) and rebuilt with the portfolio's colours: page
#171616, near-white lines #F2F2F2 and yellow #F5E660 (project/design/PORTFOLIO_STYLE.md). Anti-aliased edges keep
their strength, so only the colours change, not the drawing.

Fill strength: the see-through highlight fills measure about 40 % orange (FILL). With a strength s, fill pixels are
given strength s instead; highlight lines stay full yellow and edges are scaled in between.

Colour correction: a see-through yellow over a near-black page is a plain RGB mix, which loses colour as well as
light and reads olive. The corrected fill keeps the mix's lightness (OKLab L, so the strength looks the same) but
takes the team yellow's hue exactly and as much of its chroma as sRGB can show at that lightness.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "project" / "assets" / "cad" / "linework"
DST = ROOT / "project" / "assets" / "cad" / "linework_page"
DST_STRENGTH = DST / "strengths"
DST_LIGHT = ROOT / "project" / "assets" / "cad" / "linework_light"

OLD = {"bg": (51, 51, 51), "line": (255, 255, 255), "hi": (255, 165, 0)}       # sampled 2026-11-05
NEW = {"bg": (0x17, 0x16, 0x16), "line": (0xF2, 0xF2, 0xF2), "hi": (0xF5, 0xE6, 0x60)}
# light pages: near-black lines, yellow fills with a dark outline (yellow lines alone would vanish on white)
LIGHT = {"bg": (255, 255, 255), "line": (0x17, 0x16, 0x16), "hi": (0x17, 0x16, 0x16)}
LIGHT_FILL = (0xF5, 0xE6, 0x60)
FILL = 0.40                       # measured mode of the highlight fills (5 of 6 drawings), 2026-11-05
STRENGTHS = (50, 60, 70, 80, 90, 100)
NOISE = 0.03                      # weights under this are JPEG noise, not drawing
EDGE_PX = 3                       # border cleared on every drawing (measured frame 1-2 px, 2026-11-05)
DEFAULT_STRENGTH = 1.0          # user chose 100 % fills, 2026-11-05 (linework_page uses this)


# ---- OKLab (Ottosson 2020), sRGB 0..255 in and out
def _lin(c):
    c = np.asarray(c, float) / 255
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _unlin(c):
    c = np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.clip(c, 0, None) ** (1 / 2.4) - 0.055)
    return c * 255


_M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566],
                [0.0883024619, 0.2817188376, 0.6299787005]])
_M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099],
                [0.0259040371, 0.7827717662, -0.8086757660]])


def to_oklab(rgb):
    return _M2 @ np.cbrt(_M1 @ _lin(rgb))


def from_oklab_linear(lab):
    return np.linalg.inv(_M1) @ (np.linalg.inv(_M2) @ np.asarray(lab, float)) ** 3


def from_oklab(lab):
    return _unlin(from_oklab_linear(lab))


def lch(rgb):
    L, a, b = to_oklab(rgb)
    return L, float(np.hypot(a, b)), float(np.degrees(np.arctan2(b, a)) % 360)


def fill_colour(strength, correct=True, new=NEW):
    """The fill colour at a strength (0..1): the RGB mix, or (correct) the mix's lightness in the yellow's hue."""
    bg, y = np.array(new["bg"], float), np.array(new["hi"], float)
    mix = bg + strength * (y - bg)
    if not correct or strength >= 1:
        return mix
    L = to_oklab(mix)[0]
    _, cy, hy = lch(y)
    h = np.radians(hy)
    lo, hi = 0.0, cy                                   # largest chroma (up to the yellow's) that sRGB can show
    for _ in range(40):
        c = (lo + hi) / 2
        lin = from_oklab_linear([L, c * np.cos(h), c * np.sin(h)])
        lo, hi = (c, hi) if (lin >= -1e-9).all() and (lin <= 1 + 1e-9).all() else (lo, c)
    return from_oklab([L, lo * np.cos(h), lo * np.sin(h)])


def _weights(img, old):
    a = np.asarray(img.convert("RGB"), dtype=float)
    bg = np.array(old["bg"], float)
    basis = np.stack([np.array(old["line"], float) - bg, np.array(old["hi"], float) - bg], axis=1)  # 3 x 2
    w, *_ = np.linalg.lstsq(basis, (a - bg).reshape(-1, 3).T, rcond=None)                      # 2 x N
    w = np.clip(w, 0, 1)
    w[w < NOISE] = 0              # JPEG noise around the drawings (up to about 3 levels in 255)
    s = w.sum(0)
    w[:, s > 1] /= s[s > 1]
    if EDGE_PX and min(a.shape[:2]) > 10 * EDGE_PX:   # the exports have a faint lighter frame (edge rows ~71 against 51 inside): clear it
        g = w.reshape(2, *a.shape[:2])
        g[:, :EDGE_PX], g[:, -EDGE_PX:], g[:, :, :EDGE_PX], g[:, :, -EDGE_PX:] = 0, 0, 0, 0
    return a.shape, w


def recolour(img, old=OLD, new=NEW, strength=None, correct=True, fill=FILL, fill_rgb=None):
    """Return a recoloured copy of an RGB image (PIL). strength=None keeps the fills as drawn. fill_rgb sets the fill
    colour directly, so new["hi"] is used only for the highlight's lines."""
    shape, (wl, wh) = _weights(img, old)
    nbg, nline, ny = (np.array(new[k], float)[:, None] for k in ("bg", "line", "hi"))
    if strength is None:
        hi_part = wh * (ny - nbg)
    else:
        f = (np.array(fill_rgb, float) if fill_rgb is not None else fill_colour(strength, correct, new))[:, None]
        t1 = np.clip(wh / fill, 0, 1)                             # 0..fill: page -> fill colour
        t2 = np.clip((wh - fill) / (1 - fill), 0, 1)              # fill..1: fill colour -> full yellow line
        hi_part = np.where(wh <= fill, t1 * (f - nbg), (f - nbg) + t2 * (ny - f))
    out = (nbg + wl * (nline - nbg) + hi_part).T.reshape(shape)
    return Image.fromarray(np.clip(out.round(), 0, 255).astype(np.uint8))


def with_alpha(img, bg=NEW["bg"]):
    """Make the page colour see-through (RGBA). For each channel, alpha is how far the colour is from the page as a
    share of the furthest it could be on that side; the colour is then un-mixed from the page. Put back on the page it
    gives the same pixels, and no box edge shows (a JPEG cannot hold the page colour exactly)."""
    a = np.asarray(img.convert("RGB"), dtype=float)
    b = np.array(bg, float)
    room = np.where(a >= b, 255 - b, b)
    alpha = np.clip((np.abs(a - b) / np.where(room > 0, room, 1)).max(2), 0, 1)
    safe = np.where(alpha > 0, alpha, 1)[..., None]
    rgb = np.clip(b + (a - b) / safe, 0, 255)
    return Image.fromarray(np.dstack([rgb, alpha * 255]).round().astype(np.uint8), "RGBA")


def _save(img, out, bg=NEW["bg"]):
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix == ".png":
        with_alpha(img, bg).save(out, optimize=True)
    else:
        img.save(out, quality=95, subsampling=0)
    print(out.relative_to(ROOT))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strengths", action="store_true", help="also save highlighted drawings at 50..100 %% fill")
    ap.add_argument("--light", action="store_true", help="make only the dark-line copies for a white page")
    a = ap.parse_args(argv)
    files = sorted([*SRC.rglob("*.jpg"), *SRC.rglob("*.png")])
    if not files:
        sys.exit(f"no drawings in {SRC}")
    if a.light:
        for f in files:
            img = recolour(Image.open(f), new=LIGHT, strength=DEFAULT_STRENGTH, fill_rgb=LIGHT_FILL)
            _save(img, (DST_LIGHT / f.relative_to(SRC)).with_suffix(".png"), LIGHT["bg"])
        print(f"{len(files)} drawings made for a light page")
        return
    for f in files:
        _save(recolour(Image.open(f), strength=DEFAULT_STRENGTH), (DST / f.relative_to(SRC)).with_suffix(".png"))
    n = 0
    if a.strengths:
        for f in (f for f in files if "highlight" in f.stem):
            for s in STRENGTHS:
                rel = f.relative_to(SRC)
                _save(recolour(Image.open(f), strength=s / 100), DST_STRENGTH / rel.parent / f"{f.stem}_s{s}.jpg")
                n += 1
    print(f"{len(files)} drawings recoloured; {n} strength copies")


if __name__ == "__main__":
    main()
