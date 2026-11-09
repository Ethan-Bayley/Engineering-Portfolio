"""The line-drawing recolour maps the drawing's three colours to the portfolio's and keeps blends in between."""
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from recolour_linework import NEW, OLD, recolour  # noqa: E402


def test_three_colours_and_a_blend_map_across():
    img = Image.new("RGB", (4, 1))
    half = tuple((b + h) // 2 for b, h in zip(OLD["bg"], OLD["hi"]))
    for x, c in enumerate([OLD["bg"], OLD["line"], OLD["hi"], half]):
        img.putpixel((x, 0), c)
    out = recolour(img)
    for x, key in enumerate(["bg", "line", "hi"]):
        assert all(abs(a - b) <= 1 for a, b in zip(out.getpixel((x, 0)), NEW[key])), key
    mid = tuple((b + h) / 2 for b, h in zip(NEW["bg"], NEW["hi"]))
    assert all(abs(a - b) <= 2 for a, b in zip(out.getpixel((3, 0)), mid))


def test_strength_sets_fill_and_correction_keeps_the_yellow_hue():
    from recolour_linework import FILL, fill_colour, lch
    fill_px = tuple(round(b + FILL * (h - b)) for b, h in zip(OLD["bg"], OLD["hi"]))
    img = Image.new("RGB", (1, 1), fill_px)
    assert all(abs(a - b) <= 2 for a, b in zip(recolour(img, strength=1.0).getpixel((0, 0)), NEW["hi"]))
    _, cy, hy = lch(NEW["hi"])
    for s in (0.5, 0.6, 0.7, 0.8, 0.9):
        Lp, cp, _ = lch(fill_colour(s, correct=False))
        Lc, cc, hc = lch(fill_colour(s, correct=True))
        assert abs(Lp - Lc) < 1e-3                # same lightness, so the strength looks the same
        assert abs(hc - hy) < 0.5                 # the team yellow's hue
        assert cp <= cc <= cy + 1e-6              # at least as much colour as the plain mix, never more than the yellow


def test_alpha_puts_back_the_same_pixels_on_a_light_page():
    import numpy as np
    from recolour_linework import LIGHT, LIGHT_FILL, with_alpha
    img = Image.new("RGB", (3, 1), LIGHT["bg"])
    img.putpixel((1, 0), LIGHT["line"])
    img.putpixel((2, 0), LIGHT_FILL)
    a = np.asarray(with_alpha(img, LIGHT["bg"]), dtype=float)
    assert a[0, 0, 3] == 0                                 # the page is see-through
    page = np.array(LIGHT["bg"], float)
    back = page + (a[..., :3] - page) * a[..., 3:] / 255
    assert abs(back - np.asarray(img, dtype=float)).max() <= 1
