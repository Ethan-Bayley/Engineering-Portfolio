"""Yellowbacks portfolio style: the team's cover look (2026-11-05) used on every page. This project only.

Taken from the cover the user made: near-black page, a yellow bar down the left edge, a slanted yellow banner with
hazard stripes, white schematic line drawings of the robot, a yellow bar beside key text, a pill label, a boxed team
number. Colours tightened at the user's request: one yellow (#F5E660, the cover's own), no gold or cream.
Rules: PORTFOLIO_STYLE.md beside this file. Line art from CAD: schematic.py beside this file.

    from portfolio_style import Portfolio
    doc = Portfolio(team="11143", team_name="Barker Yellowbacks")
    p = doc.page("Drivetrain")                          # yellow banner title with hazard stripes
    left, right = p.cols(p.area, 1, 1)
    b = p.box(left, "Key features")                     # square outline, yellow bar + caps heading
    b.text(b.content, ["**13.6:1 ratio** for speed", "- ++Pro:++ light", "- ~~Con:~~ costly"])
    doc.save_versioned("portfolio", "portfolio", "what changed")

Text markup: **yellow bold**, ++green bold++ (pro, pass), ~~red bold~~ (con, fail); "- " starts a bullet.
Nothing under 10 pt (FTC A201); save() refuses. Colours can be changed in project/design.json: main (yellow),
background, text, muted, line, pro, con.
"""
import json
import math
import os
import re
import sys
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Pt

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "general" / "design").is_dir())
sys.path.insert(0, str(ROOT / "general" / "design"))
from design_system import DesignError, Rect, _gap, _picture, _rgb, _shape, split  # noqa: E402
from design_system import save_versioned as _save_versioned  # noqa: E402


def _look():
    f = ROOT / "project" / "design.json"
    try:
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    except (OSError, ValueError):
        return {}


_L = _look()
# ---- colours (hex without #): measured contrast on the page is in PORTFOLIO_STYLE.md ----
YELLOW = ACCENT = _L.get("main", "F5E660")   # the cover's yellow: edge bar, banners, stripes, key words, labels
BG = _L.get("background", "171616")          # the cover's page colour (not pure black)
INK = "171616"                               # dark text on yellow
TEXT = _L.get("text", "F2F2F2")              # body text (not pure white)
MUTED = _L.get("muted", "C4C4C4")            # the cover's grey: captions, header and footer, team number
LINE = _L.get("line", "8C8C8C")              # box outlines and table rules (thin, like a drawing frame)
PRO = _L.get("pro", "6FD98B")                # pros, pass, better: only these
CON = _L.get("con", "FF7B72")                # cons, fail, worse: only these

# ---- themes: paper is the look for the printed portfolio (default, user chose it 2026-11-06); dark is the team's
# cover look; band is the option not chosen. PORTFOLIO_THEME=dark|band picks another. Yellow text cannot be read on a light page (1.3:1), so on light themes key words,
# labels and arrows are near-black and yellow is only ever a fill with dark text on it (or dark bands with yellow text).
THEME = os.environ.get("PORTFOLIO_THEME", "paper").lower()
_THEMES = {
    "dark": dict(BG=BG, TEXT=TEXT, MUTED=MUTED, LINE=LINE, PRO=PRO, CON=CON, KEY=YELLOW, STROKE=YELLOW, FILL=YELLOW,
                 FILL_TEXT=INK, EDGE_FILL=YELLOW, BAR_FILL=YELLOW, STRIPE=YELLOW, SHAPE_LINE=None, NODE=YELLOW,
                 SQUARE=None),
    # A: white page, yellow bands with dark text, thin dark outlines so the yellow keeps an edge on paper
    "paper": dict(BG="FFFFFF", TEXT=INK, MUTED="4D4D4D", LINE="8C8C8C", PRO="1B7A3A", CON="C62828", KEY=INK, STROKE=INK,
                  FILL=YELLOW, FILL_TEXT=INK, EDGE_FILL=YELLOW, BAR_FILL=YELLOW, STRIPE=YELLOW, SHAPE_LINE=INK,
                  NODE=YELLOW, SQUARE=YELLOW),
    # B: near-white page, near-black bands with yellow text, closest to the cover's black and yellow
    "band": dict(BG="FAF9F5", TEXT=INK, MUTED="4D4D4D", LINE="8C8C8C", PRO="1B7A3A", CON="C62828", KEY=INK, STROKE=INK,
                 FILL=INK, FILL_TEXT=YELLOW, EDGE_FILL=INK, BAR_FILL=INK, STRIPE=YELLOW, SHAPE_LINE=INK, NODE=INK,
                 SQUARE=INK),
}
if THEME not in _THEMES:
    raise ValueError(f"unknown PORTFOLIO_THEME {THEME!r}: use {', '.join(_THEMES)}")
_T = _THEMES[THEME]
BG, TEXT, MUTED, LINE, PRO, CON = (_T[k] for k in ("BG", "TEXT", "MUTED", "LINE", "PRO", "CON"))
KEY, STROKE, FILL, FILL_TEXT = _T["KEY"], _T["STROKE"], _T["FILL"], _T["FILL_TEXT"]   # key words + labels; lines; bands
EDGE_FILL, BAR_FILL, STRIPE, SHAPE_LINE, NODE, SQUARE = (_T[k] for k in ("EDGE_FILL", "BAR_FILL", "STRIPE", "SHAPE_LINE",
                                                                         "NODE", "SQUARE"))

FONT = "Montserrat"
HAND = "Caveat Static"                       # handwritten labels on CAD and photos (user's choice, 2026-11-05)
FONT_DIR = Path(__file__).resolve().parent / "fonts"

# ---- sizes (pt), A4 portrait; nothing under 10 pt ----
W, H = 595.28, 841.89
G = 10.0                                     # the one gap between boxes
EDGE = 14.0                                  # yellow bar down the left edge (the cover's bar, 3.7 % of its width)
LEFT, RIGHT, TOP, BOTTOM = EDGE + 2.2 * G, 2.6 * G, 2.4 * G, 3.0 * G
BANNER_H = 32.0
TITLE, HEAD, SUB, BODY, SMALL, LABEL = 19, 12, 11.5, 10.5, 10, 15
MIN_PT = 10
PAD = 0.9 * G
STATUS = {"MET": PRO, "PASS": PRO, "CHOSEN": PRO, "YES": PRO, "BETTER": PRO,
          "NOT MET": CON, "FAIL": CON, "NOT CHOSEN": CON, "NO": CON, "WORSE": CON,
          "PARTLY MET": KEY, "NOT TESTED": MUTED}
LEADING = 1.2            # PowerPoint draws Montserrat at 1.2 x the size (measured in an exported PDF, 2026-11-05)

_MARK = re.compile(r"(\*\*|\+\+|~~)(.+?)\1")
_MARK_COLOUR = {"**": KEY, "++": PRO, "~~": CON}


def plain(s):
    return _MARK.sub(lambda m: m.group(2), s)


def runs(s, colour=TEXT):
    """'plain **yellow** ++pro++ ~~con~~' -> [(text, colour, bold)]"""
    out, pos = [], 0
    for m in _MARK.finditer(s):
        if m.start() > pos:
            out.append((s[pos:m.start()], colour, False))
        out.append((m.group(2), _MARK_COLOUR[m.group(1)], True))
        pos = m.end()
    if pos < len(s):
        out.append((s[pos:], colour, False))
    return out


# ---- measuring with the real fonts ----
_CACHE = {}


def _pil(font, bold, italic=False):
    key = (font, bold, italic)
    if key not in _CACHE:
        from PIL import ImageFont
        if font == HAND:
            path = FONT_DIR / "Caveat" / ("CaveatStatic-Bold.ttf" if bold else "CaveatStatic-Regular.ttf")
        else:
            style = ("Bold" if bold else "") + ("Italic" if italic else "") or "Regular"
            path = FONT_DIR / "Montserrat" / f"Montserrat-{style}.ttf"
        try:
            _CACHE[key] = ImageFont.truetype(str(path), 100)
        except OSError:
            _CACHE[key] = None
    return _CACHE[key]


def width(text, size, bold=False, font=FONT, italic=False):
    f = _pil(font, bold, italic)
    return len(text) * size * 0.62 if f is None else f.getlength(text) * size / 100


def lines(text, size, w, bold=False, font=FONT):
    words = []
    for t, _c, b in runs(text):
        words += [(x, b or bold) for x in t.split()]
    n, cur = 1, 0.0
    for word, b in words:
        wl = width(word, size, b, font)
        add = wl if cur == 0 else wl + width(" ", size, b, font)
        if cur + add > w and cur > 0:
            n, cur = n + 1, wl
        else:
            cur += add
    return n


def text_height(paras, size, w, after=None):
    h = 0.0
    for p in paras:
        p = p if isinstance(p, dict) else {"text": p}
        s = p.get("size", size)
        bullet = p["text"].startswith("- ")
        txt = p["text"][2:] if bullet else p["text"]
        h += lines(txt, s, w - (s * 1.1 if bullet else 0), p.get("bold", False), p.get("font", FONT)) * s * LEADING
        h += p.get("after", s * 0.4 if after is None else after)
    return h


def write(slide, r, paras, size=BODY, colour=TEXT, bold=False, italic=False, font=FONT, align=PP_ALIGN.LEFT,
          anchor=MSO_ANCHOR.TOP, after=None, name=None, sizes=None, rotation=0):
    """Text box. paras: str (markup, '- ' bullet) or dict {text, size, colour, bold, italic, font, align, after}."""
    box = slide.shapes.add_textbox(Pt(r.x), Pt(r.y), Pt(r.w), Pt(r.h))
    if name:
        box.name = name
    box.rotation = rotation
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, p in enumerate(paras):
        p = p if isinstance(p, dict) else {"text": p}
        s = p.get("size", size)
        if sizes is not None:
            sizes.append(s)
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = p.get("align", align)
        para.line_spacing = 1.0
        para.space_after = Pt(p.get("after", s * 0.4 if after is None else after))
        txt = p["text"]
        if txt.startswith("- "):
            txt = txt[2:]
            pPr = para._p.get_or_add_pPr()
            pPr.set("marL", str(Pt(s * 1.1)))
            pPr.set("indent", str(-Pt(s * 1.1)))
            bc = etree.SubElement(pPr, qn("a:buClr"))
            etree.SubElement(bc, qn("a:srgbClr"), val=KEY)
            etree.SubElement(pPr, qn("a:buSzPct"), val="70000")
            etree.SubElement(pPr, qn("a:buChar"), char="■")        # square bullet, shrunk (Montserrat has U+25A0, not U+25AA)
        for t, c, b in runs(txt, p.get("colour", colour)):
            run = para.add_run()
            run.text = t
            run.font.name = p.get("font", font)
            run.font.size = Pt(s)
            run.font.bold = b or p.get("bold", bold)
            run.font.italic = p.get("italic", italic)
            run.font.color.rgb = _rgb(c)
    return box


# ---- the cover's shapes ----
def polygon(slide, pts, fill=FILL, line=SHAPE_LINE, width_pt=0.75):
    """A filled polygon from [(x, y)] in pt."""
    fb = slide.shapes.build_freeform(Pt(pts[0][0]), Pt(pts[0][1]), scale=1.0)
    fb.add_line_segments([(Pt(x), Pt(y)) for x, y in pts[1:]], close=True)
    s = fb.convert_to_shape()
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = _rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = _rgb(line)
        s.line.width = Pt(width_pt)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def banner(slide, x, y, h, text, size=TITLE, slant=None, min_w=0, sizes=None):
    """The cover's banner: a yellow band, straight on the left and slanted on the right, dark bold caps text.
    Returns the banner's right edge (top corner)."""
    slant = h * 0.6 if slant is None else slant
    tw = width(text.upper(), size, True)
    w = max(min_w, tw + 1.4 * G + slant)
    polygon(slide, [(x, y), (x + w, y), (x + w - slant, y + h), (x, y + h)])
    write(slide, Rect(x + 0.8 * G, y, tw + 4, h), [{"text": text.upper(), "size": size, "bold": True, "colour": FILL_TEXT,
                                                   "after": 0}], anchor=MSO_ANCHOR.MIDDLE, sizes=sizes, name="Page title")
    return x + w


def stripes(slide, x, y, h, n=4, w=None, gap=None, slant=None):
    """Hazard stripes: n yellow slanted bars starting at x. Returns the right edge."""
    w = w or h * 0.42
    gap = gap or h * 0.3
    slant = h * 0.6 if slant is None else slant
    for i in range(n):
        x0 = x + i * (w + gap)
        polygon(slide, [(x0 + slant, y), (x0 + slant + w, y), (x0 + w, y + h), (x0, y + h)], fill=STRIPE)
    return x + n * (w + gap) + slant


def pill(slide, r, text, size=SMALL, filled=True, sizes=None):
    """A rounded label: yellow with dark caps text, or a yellow outline with yellow text."""
    s = _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, r, FILL if filled else None, None if filled else STROKE, 1.2)
    s.adjustments[0] = 0.5
    write(slide, r, [{"text": text.upper(), "size": size, "bold": True, "colour": FILL_TEXT if filled else KEY,
                      "align": PP_ALIGN.CENTER, "after": 0}], anchor=MSO_ANCHOR.MIDDLE, sizes=sizes)
    return r


def pill_width(text, size=SMALL):
    return width(text.upper(), size, True) + 1.6 * G


def bar(slide, x, y, h, w=3.0):
    """The yellow bar the cover puts beside key text."""
    return _shape(slide, MSO_SHAPE.RECTANGLE, Rect(x, y, w, h), BAR_FILL)


def _arrowhead(shape):
    etree.SubElement(shape.line._get_or_add_ln(), qn("a:tailEnd"), type="triangle", w="med", len="med")


def curved_arrow(slide, x0, y0, x1, y1, colour=STROKE, bend=0.25, width_pt=1.6):
    """A curved arrow from (x0, y0) to (x1, y1): a quadratic curve bent sideways by `bend` x its length."""
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy) or 1
    cx, cy = (x0 + x1) / 2 - dy / length * bend * length, (y0 + y1) / 2 + dx / length * bend * length
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t ** 2 * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t ** 2 * y1)
           for t in (i / 20 for i in range(21))]
    fb = slide.shapes.build_freeform(Pt(pts[0][0]), Pt(pts[0][1]), scale=1.0)
    fb.add_line_segments([(Pt(x), Pt(y)) for x, y in pts[1:]], close=False)
    s = fb.convert_to_shape()
    s.fill.background()
    s.line.color.rgb = _rgb(colour)
    s.line.width = Pt(width_pt)
    s.shadow.inherit = False
    _arrowhead(s)
    return s


def _straight(slide, x0, y0, x1, y1, colour=LINE, w=1.0, arrow=False):
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Pt(x0), Pt(y0), Pt(x1), Pt(y1))
    ln.line.color.rgb = _rgb(colour)
    ln.line.width = Pt(w)
    if arrow:
        _arrowhead(ln)
    etree.SubElement(ln._element.spPr, qn("a:effectLst"))     # no theme shadow: it shows as a grey smudge on a light page
    return ln


class Box:
    """A square-cornered thin outline (like a drawing frame) with a yellow bar and caps heading inside.
    accent=True: yellow outline, for the one thing on the page the judges must not miss."""

    def __init__(self, page, rect, title=None, accent=False):
        self.page, self.rect, self.title, self.accent = page, rect, title, accent
        slide = page.slide
        _shape(slide, MSO_SHAPE.RECTANGLE, rect, None, STROKE if accent else LINE, 1.5 if accent else 1.0)
        inner = rect.inset(PAD)
        top = inner.y
        if title:
            hh = lines(title.upper(), HEAD, inner.w - 0.8 * G, True) * HEAD * LEADING
            bar(slide, inner.x, inner.y, hh)
            self.write(Rect(inner.x + 0.8 * G, inner.y, inner.w - 0.8 * G, hh),
                       [{"text": title.upper(), "size": HEAD, "bold": True, "after": 0}], anchor=MSO_ANCHOR.MIDDLE)
            top = inner.y + hh + 0.7 * G
        self.content = Rect(inner.x, top, inner.w, inner.b - top)

    def write(self, r, paras, size=BODY, **kw):
        return write(self.page.slide, r, paras, size, sizes=self.page.sizes, **kw)

    def text(self, r, paras, size=BODY, **kw):
        need = text_height(paras, size, r.w)
        if need > r.h + 1:
            self.page.problems.append(f"text needs {need:.0f} pt but has {r.h:.0f} pt: {str(paras[0])[:40]!r}")
        return self.write(r, paras, size, **kw)

    def head(self, text):
        return {"text": text, "size": SUB, "colour": KEY, "bold": True, "after": 0.25 * BODY}

    def picture(self, r, path, alt, caption=None, align="center"):
        if caption:
            ch = text_height([caption], SMALL, r.w)
            img = _picture(self.page.slide, path, Rect(r.x, r.y, r.w, r.h - ch - 0.3 * G), alt, align)
            self.write(Rect(r.x, img.b + 0.3 * G, r.w, ch), [caption], SMALL, colour=MUTED, align=PP_ALIGN.CENTER)
            return img
        return _picture(self.page.slide, path, r, alt, align)

    def labelled(self, r, path, alt, labels=(), caption=None):
        """Picture (best: white line art from schematic.py) with handwritten yellow labels and curved arrows:
        labels = [(fx, fy, text, lx, ly)], point and label centre as fractions of the picture."""
        img = self.picture(r, path, alt, caption)
        for fx, fy, text, lx, ly in labels:
            self.label(img, fx, fy, text, lx, ly)
        return img

    def label(self, img, fx, fy, text, lx, ly, bend=0.25):
        px, py = img.x + fx * img.w, img.y + fy * img.h
        cx, cy = img.x + lx * img.w, img.y + ly * img.h
        lw = min(max(width(w, LABEL, True, HAND) for w in text.split()) * 2.2, width(text, LABEL, True, HAND)) + 4
        lh = lines(text, LABEL, lw, True, HAND) * LABEL * 1.05
        lab = Rect(cx - lw / 2, cy - lh / 2, lw, lh)
        box = self.rect.inset(1)
        if lab.x < box.x - 1 or lab.r > box.r + 1 or lab.y < box.y - 1 or lab.b > box.b + 1:
            self.page.problems.append(f"label {text!r} goes outside its box")
        self.write(lab, [{"text": text, "size": LABEL, "font": HAND, "colour": KEY, "bold": True, "after": 0,
                          "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
        if lab.x <= px <= lab.r:
            sx, sy = cx, (lab.b + 2 if py > lab.b else lab.y - 2)
        else:
            sx, sy = (lab.x - 2 if px < lab.x else lab.r + 2), cy
        curved_arrow(self.page.slide, sx, sy, px, py, bend=bend if fx >= lx else -bend)
        return lab

    def stack(self, r, items, gap=None):
        """("text", paras) get their height; ("fill", weight, draw) share the rest; draw(rect) draws it."""
        gap = 0.6 * G if gap is None else gap
        need = [text_height(it[1], it[2] if len(it) > 2 else BODY, r.w) if it[0] == "text" else None for it in items]
        spare = max(0.0, r.h - sum(h for h in need if h) - gap * (len(items) - 1))
        weights = sum(it[1] for it in items if it[0] == "fill") or 1
        y, out = r.y, []
        for it, h in zip(items, need):
            h = h if h is not None else spare * it[1] / weights
            rr = Rect(r.x, y, r.w, h)
            out.append(rr)
            if it[0] == "text":
                self.write(rr, it[1], it[2] if len(it) > 2 else BODY)
            else:
                it[2](rr)
            y += h + gap
        return out

    def story(self, r, items):
        """Challenge -> solution: items = [(label, text)]. Each label is a yellow pill (the cover's 'FTC' pill), the
        last one filled, earlier ones outlined. Returns the rects; spare space stays at the bottom."""
        y, out = r.y, []
        ph = SMALL * 1.9
        for k, (label, body) in enumerate(items):
            last = k == len(items) - 1
            pill(self.page.slide, Rect(r.x, y, pill_width(label), ph), label, filled=last, sizes=self.page.sizes)
            bh = text_height([body], BODY, r.w)
            self.write(Rect(r.x, y + ph + 0.35 * G, r.w, bh), [body])
            out.append(Rect(r.x, y, r.w, ph + 0.35 * G + bh))
            y += ph + 0.35 * G + bh + 0.6 * G
        if y - 0.6 * G > r.b + 1:
            self.page.problems.append(f"story needs {y - r.y:.0f} pt but has {r.h:.0f} pt")
        return out

    def iterations(self, r, items, arrow_gap=None):
        """Versions in a row: items = [(name, picture or None, alt, pros, cons)]; name in a pill, pros green '+',
        cons red minus; yellow arrows between; the last (kept) card has the yellow outline."""
        ag = arrow_gap or 2.2 * G
        n = len(items)
        cw = (r.w - ag * (n - 1)) / n
        for i, (name, pic, alt, pros, cons) in enumerate(items):
            c = Rect(r.x + i * (cw + ag), r.y, cw, r.h)
            last = i == n - 1
            _shape(self.page.slide, MSO_SHAPE.RECTANGLE, c, None, STROKE if last else LINE, 1.5 if last else 1.0)
            inner = c.inset(0.6 * G)
            ph = SMALL * 1.9
            pw = min(inner.w, pill_width(name))
            pill(self.page.slide, Rect(inner.x + (inner.w - pw) / 2, inner.y, pw, ph), name, filled=last,
                 sizes=self.page.sizes)
            paras = [{"text": "+ " + p, "colour": PRO, "after": 2} for p in pros] + \
                    [{"text": "− " + x, "colour": CON, "after": 2} for x in cons]
            th = text_height(paras, SMALL, inner.w)
            top = inner.y + ph + 0.5 * G
            if pic:
                pic_h = inner.b - top - th - 0.4 * G
                if pic_h < 3 * G:
                    self.page.problems.append(f"iteration {name!r}: no room for the picture")
                _picture(self.page.slide, pic, Rect(inner.x, top, inner.w, max(pic_h, 1)), alt)
                top += pic_h + 0.4 * G
            self.write(Rect(inner.x, top, inner.w, th), paras, SMALL)
            if inner.y + ph + 0.5 * G + th > inner.b + 1:
                self.page.problems.append(f"iteration {name!r}: text does not fit")
            if not last:
                y = c.y + c.h / 2
                _straight(self.page.slide, c.r + 0.3 * G, y, c.r + ag - 0.3 * G, y, STROKE, 2, arrow=True)

    def team(self, r, members, cols=2):
        """Member cards: [(name, role, photo or None, note)], first name + last initial (A201)."""
        rows = -(-len(members) // cols)
        cells = [c for row in split(r, [1] * rows, 0.6 * G, vertical=True) for c in split(row, [1] * cols, 0.6 * G)]
        for (name, role, photo, note), c in zip(members, cells):
            if re.search(r"\b[A-Z][a-z]+ [A-Z][a-z]{2,}", name):
                self.page.problems.append(f"team card {name!r}: use first name and last initial only (A201)")
            _shape(self.page.slide, MSO_SHAPE.RECTANGLE, c, None, LINE, 1.0)
            inner = c.inset(0.6 * G)
            side = min(inner.h, inner.w * 0.32)
            pr = Rect(inner.x, inner.y + (inner.h - side) / 2, side, side)
            if photo:
                _picture(self.page.slide, photo, pr, f"Photo of {name}")
            else:
                _shape(self.page.slide, MSO_SHAPE.RECTANGLE, pr, SQUARE, STROKE, 1.5)
                initials = "".join(w[0] for w in plain(name).replace(".", "").split()[:2] if w)
                self.write(pr, [{"text": initials, "size": max(SUB, side * 0.33), "bold": True, "colour": FILL_TEXT if SQUARE else KEY,
                                 "align": PP_ALIGN.CENTER, "after": 0}], anchor=MSO_ANCHOR.MIDDLE)
            tx = pr.r + 0.7 * G
            bar(self.page.slide, tx, inner.y + inner.h * 0.2, inner.h * 0.6, 2.5)
            self.write(Rect(tx + 0.7 * G, inner.y, inner.r - tx - 0.7 * G, inner.h),
                       [{"text": name, "size": SUB, "bold": True, "after": 1},
                        {"text": role.upper(), "colour": KEY, "bold": True, "size": SMALL, "after": 2}]
                       + ([{"text": note, "colour": MUTED, "size": SMALL}] if note else []), anchor=MSO_ANCHOR.MIDDLE)

    def timeline(self, r, items, dashed=False):
        """Horizontal season timeline: [(when, title, text)]; square yellow nodes on a yellow line.
        dashed=True: a dotted line and hollow nodes, for planned events that have not happened yet."""
        n = len(items)
        cw = r.w / n
        when_h = SMALL * LEADING + 0.3 * G
        node = 0.9 * G
        ly = r.y + when_h + node / 2
        ln = _straight(self.page.slide, r.x + cw / 2, ly, r.r - cw / 2, ly, STROKE, 2)
        if dashed:
            ln.line.dash_style = MSO_LINE.ROUND_DOT
        for i, (when, title, text) in enumerate(items):
            cx = r.x + (i + 0.5) * cw
            self.write(Rect(cx - cw / 2, r.y, cw, when_h), [{"text": when.upper(), "size": SMALL, "bold": True,
                       "colour": KEY, "align": PP_ALIGN.CENTER, "after": 0}])
            s = _shape(self.page.slide, MSO_SHAPE.RECTANGLE, Rect(cx - node / 2, ly - node / 2, node, node),
                       None if dashed else NODE, STROKE if dashed else SHAPE_LINE, 1.2 if dashed else 0.75)
            s.rotation = 45
            body = Rect(cx - cw / 2 + 0.2 * G, ly + node / 2 + 0.5 * G, cw - 0.4 * G, r.b - (ly + node / 2 + 0.5 * G))
            paras = [{"text": title, "bold": True, "align": PP_ALIGN.CENTER, "after": 2},
                     {"text": text, "size": SMALL, "align": PP_ALIGN.CENTER}]
            if text_height(paras, BODY, body.w) > body.h + 1:
                self.page.problems.append(f"timeline {title!r}: text does not fit")
            self.write(body, paras)

    def plan_vs_actual(self, r, periods, rows, label_w=None):
        """Planned against actual: rows = [(task, plan_start, plan_end, actual_start, actual_end)] as period indexes.
        Planned = grey outline bar, actual = yellow bar, the part past the planned end = red."""
        label_w = label_w or r.w * 0.28
        col = (r.w - label_w) / len(periods)
        head = SMALL * LEADING + 0.4 * G
        rh = (r.h - head - SMALL * LEADING - 0.4 * G) / len(rows)
        x0 = r.x + label_w
        for k, p in enumerate(periods):
            self.write(Rect(x0 + k * col, r.y, col, head), [{"text": p.upper(), "size": SMALL, "bold": True,
                       "colour": MUTED, "align": PP_ALIGN.CENTER, "after": 0}])
        for i, (task, ps, pe, a_s, a_e) in enumerate(rows):
            y = r.y + head + i * rh
            self.write(Rect(r.x, y, label_w - 0.4 * G, rh), [{"text": task, "size": SMALL, "after": 0}],
                       anchor=MSO_ANCHOR.MIDDLE)
            bh = min(rh * 0.32, 0.9 * G)
            _shape(self.page.slide, MSO_SHAPE.RECTANGLE, Rect(x0 + ps * col + 0.1 * col, y + rh / 2 - bh - 1,
                   (pe - ps + 0.8) * col, bh), None, MUTED, 1)
            if a_s is not None:
                end = min(a_e, pe)
                _shape(self.page.slide, MSO_SHAPE.RECTANGLE, Rect(x0 + a_s * col + 0.1 * col, y + rh / 2 + 1,
                       (end - a_s + 0.8) * col, bh), YELLOW)
                if a_e > pe:
                    _shape(self.page.slide, MSO_SHAPE.RECTANGLE, Rect(x0 + (pe + 0.9) * col, y + rh / 2 + 1,
                           (a_e - pe - 0.1) * col, bh), CON)
        self.write(Rect(r.x, r.b - SMALL * LEADING, r.w, SMALL * LEADING),
                   ["Outline: planned.   **Yellow:** actual.   ~~Red:~~ later than planned."], SMALL, colour=MUTED)

    def table(self, r, rows, col_weights=None, status_col=None):
        """Header row as a yellow band with dark caps (like the banner); rows split by thin grey rules; a status
        column colours its words. Only as tall as its rows. Returns the rect used."""
        m = len(rows[0])
        widths = [r.w * w / sum(col_weights or [1] * m) for w in (col_weights or [1] * m)]
        pad = 0.4 * G
        hs = [max(text_height([str(c).upper() if i == 0 else str(c)], SMALL, w - 2 * pad, after=0)
                  for c, w in zip(row, widths)) + 2 * pad for i, row in enumerate(rows)]
        total = sum(hs)
        if total > r.h + 1:
            self.page.problems.append(f"table needs {total:.0f} pt but has {r.h:.0f} pt")
        _shape(self.page.slide, MSO_SHAPE.RECTANGLE, Rect(r.x, r.y, r.w, hs[0]), FILL)
        y = r.y
        for i, (row, h) in enumerate(zip(rows, hs)):
            x = r.x
            for j, (cell, w) in enumerate(zip(row, widths)):
                word = str(cell).upper()
                colour = FILL_TEXT if i == 0 else STATUS.get(word, TEXT) if j == status_col else TEXT
                self.write(Rect(x + pad, y + pad, w - 2 * pad, h - 2 * pad),
                           [{"text": word if i == 0 else str(cell), "size": SMALL, "colour": colour,
                             "bold": i == 0 or (j == status_col and word in STATUS), "after": 0}], anchor=MSO_ANCHOR.MIDDLE)
                x += w
            y += h
            if i:
                _straight(self.page.slide, r.x, y, r.r, y, LINE, 0.6)
        return Rect(r.x, r.y, r.w, total)


class Page:
    def __init__(self, doc, title, cover=False):
        self.doc, self.title, self.cover = doc, title, cover
        self.slide = doc.prs.slides.add_slide(doc.prs.slide_layouts[6])
        self.boxes, self.sizes, self.problems = [], [], []
        bg = self.slide.background.fill
        bg.solid()
        bg.fore_color.rgb = _rgb(BG)
        _shape(self.slide, MSO_SHAPE.RECTANGLE, Rect(0, 0, EDGE, H), EDGE_FILL).name = "Edge bar"
        self.number = len([p for p in doc.pages if not p.cover]) + (0 if cover else 1)
        if cover:
            self.area = Rect(LEFT, TOP, W - LEFT - RIGHT, H - TOP - BOTTOM)
            return
        # header: the cover's banner from the edge bar, hazard stripes, team number boxed on the right
        t = plain(title)
        right = banner(self.slide, EDGE, TOP, BANNER_H, t, sizes=self.sizes, min_w=LEFT - EDGE + 4 * G)
        sx = stripes(self.slide, right + 0.5 * G, TOP, BANNER_H, n=4)
        num_w = width(doc.team, SUB, True) + 1.4 * G
        nb = Rect(W - RIGHT - num_w, TOP, num_w, BANNER_H)
        if sx > nb.x - G:
            self.problems.append("title is too long for the banner")
        _shape(self.slide, MSO_SHAPE.RECTANGLE, nb, None, MUTED, 1.2)
        write(self.slide, nb, [{"text": doc.team, "size": SUB, "bold": True, "colour": MUTED, "align": PP_ALIGN.CENTER,
              "after": 0}], anchor=MSO_ANCHOR.MIDDLE, sizes=self.sizes)
        bar(self.slide, nb.x - 0.5 * G - 3, TOP, BANNER_H)
        # footer
        fy = H - BOTTOM + 0.9 * G
        write(self.slide, Rect(LEFT, fy, 300, SMALL * LEADING), [{"text": f"{doc.team}  {doc.team_name.upper()}",
              "size": SMALL, "bold": True, "colour": MUTED, "after": 0}], sizes=self.sizes)
        write(self.slide, Rect(W - RIGHT - 100, fy, 100, SMALL * LEADING),
              [{"text": f"PAGE {self.number:02d}", "size": SMALL, "bold": True, "colour": KEY, "align": PP_ALIGN.RIGHT,
                "after": 0}], name="Page number", sizes=self.sizes)
        top = TOP + BANNER_H + 1.2 * G
        self.area = Rect(LEFT, top, W - LEFT - RIGHT, H - BOTTOM - top)

    def cols(self, r, *weights):
        return split(r, weights or [1], G)

    def rows(self, r, *weights):
        return split(r, weights or [1], G, vertical=True)

    def box(self, rect, title=None, accent=False):
        b = Box(self, rect, title, accent)
        self.boxes.append(b)
        return b

    def text(self, r, paras, size=BODY, **kw):
        return write(self.slide, r, paras, size, sizes=self.sizes, **kw)

    def check(self):
        out = list(self.problems)
        for b in self.boxes:
            r = b.rect
            if r.x < LEFT - 0.5 or r.r > W - RIGHT + 0.5 or r.y < TOP - 0.5 or r.b > H - BOTTOM + 0.5:
                out.append(f"box {b.title!r} goes outside the margins")
        for i, a in enumerate(self.boxes):
            for b in self.boxes[i + 1:]:
                gap = _gap(a.rect, b.rect)
                if gap is None:
                    continue
                if gap < -0.5:
                    out.append(f"boxes {a.title!r} and {b.title!r} overlap")
                elif gap < 1.75 * G and abs(gap - G) > 0.5:
                    out.append(f"gap between {a.title!r} and {b.title!r} is {gap:.1f} pt, not G = {G} pt")
        small = sorted({s for s in self.sizes if s < MIN_PT})
        if small:
            out.append(f"text under {MIN_PT} pt: {small}")
        name = "cover" if self.cover else f"page {self.number}"
        return [f"{name} ({plain(self.title)}): {p}" for p in out]


class Portfolio:
    """One cover (not counted, not judged) plus content pages numbered from 1; FTC A201: at most 15."""

    def __init__(self, team="", team_name="", max_pages=15):
        self.team, self.team_name, self.max_pages = team, team_name, max_pages
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = Pt(W), Pt(H)
        self.pages = []

    def cover(self):
        p = Page(self, "Cover", cover=True)
        self.pages.append(p)
        return p

    def page(self, title):
        p = Page(self, title)
        self.pages.append(p)
        return p

    def check(self):
        out = [x for p in self.pages for x in p.check()]
        n = len([p for p in self.pages if not p.cover])
        if n > self.max_pages:
            out.append(f"{n} content pages; the limit is {self.max_pages}")
        if sum(p.cover for p in self.pages) > 1:
            out.append("more than one cover page")
        return out

    def save(self, path, strict=True):
        problems = self.check()
        if problems and strict:
            raise DesignError("portfolio style check failed:\n  " + "\n  ".join(problems))
        self.prs.save(path)
        return problems

    def save_versioned(self, project, name, note, strict=True):
        problems = self.check()
        if problems and strict:
            raise DesignError("portfolio style check failed:\n  " + "\n  ".join(problems))
        return _save_versioned(self.prs, project, name, note)


def contrast(a, b):
    """WCAG contrast ratio of two hex colours."""
    def lum(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
