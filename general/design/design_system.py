"""Design system for PowerPoint (python-pptx): tokens, components and layout checks.

The rules are written out in DESIGN_SYSTEM.md; this file draws them. Build scripts choose the words and pictures,
this file chooses nothing about content.

    from design_system import Doc
    doc = Doc("brochure")                       # A4 landscape with page numbers; "poster" = A3 portrait without
    page = doc.page("DESIGN")                   # big caps page title in the main colour
    left, right = page.cols(page.area, 2, 1)    # split with the one consistent gap G
    box = page.box(left, "research", "Research findings")    # heading becomes "01 - RESEARCH FINDINGS"
    box.text(box.content, ["Plain paragraph with **bold** words."])
    doc.save_versioned("brochure", "brochure", "what changed")   # -> project/outputs/brochure/brochure_vNN.pptx

All sizes are in points. Every spacing value comes from one number, the gap G = 1.6% of the page width.
"""
import re
from dataclasses import dataclass, field
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Pt

ROOT = Path(__file__).resolve().parents[2]          # repo root (this file is general/design/design_system.py)
OUTPUTS = ROOT / "project" / "outputs"


def _project_look():
    """Optional per-project colours: project/design.json, written by the setup-project skill. Missing keys keep the defaults."""
    import json
    f = ROOT / "project" / "design.json"
    try:
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    except (OSError, ValueError):
        return {}


_LOOK = _project_look()
# ---- colours: defaults are the RobotHand look; project/design.json can change them (hex without #) ----
MAIN = _LOOK.get("main", "1D497D")                     # page titles, cover, top-level items. Never a content box.
GREEN, ORANGE, PURPLE, RED = (_LOOK.get(k, d) for k, d in (("green", "1C9D75"), ("orange", "CB8429"),
                                                           ("purple", "635CA8"), ("red", "D43E2E")))
ACCENT = {GREEN: _LOOK.get("green_tint", "D8EDE8"), ORANGE: _LOOK.get("orange_tint", "FEF4D0"),
          PURPLE: _LOOK.get("purple_tint", "EDEDF6"), RED: _LOOK.get("red_tint", "FDECEB")}
BOX_COLOURS = (GREEN, ORANGE, PURPLE, RED)
NAMES = {MAIN: "main", GREEN: "green", ORANGE: "orange", PURPLE: "purple", RED: "red"}
SLATE = "2B3E50"                    # body text (measured from the reference PDF)
WHITE = "FFFFFF"

# Box colour by meaning (user chose "by meaning", 2026-10-19). Swapped only when two touching boxes would match.
ROLES = {
    "research": GREEN, "results": GREEN, "findings": GREEN, "conclusion": GREEN,
    "design": ORANGE, "process": ORANGE, "build": ORANGE, "planning": ORANGE,
    "method": PURPLE, "code": PURPLE, "software": PURPLE, "analysis": PURPLE,
    "problem": RED, "testing": RED, "risk": RED, "evaluation": RED,
}
HIGHLIGHT = {"result": GREEN, "caution": ORANGE}
# Verdict words in a table's status column: tint fill, bold slate text (colour by meaning)
STATUS = {"MET": GREEN, "CHOSEN": GREEN, "PARTLY MET": ORANGE, "NOT MET": RED, "NOT CHOSEN": RED,
          "NOT TESTED": PURPLE, "MEASURED ONLY": PURPLE}     # plus "general" = the box's own colour

FONT, FONT_TITLE = "Inter", "Inter"      # titles are Inter Bold: a static font, so PDF export keeps it


@dataclass(frozen=True)
class Format:
    name: str
    width: float          # pt
    height: float         # pt
    title: float          # page title, caps
    heading: float        # "01 - BOX HEADING", bold caps, box colour (>= 14 pt so green/orange pass 3:1)
    sub: float            # sub-topic heading, bold, colour
    body: float           # body text, slate
    small: float          # captions, sources, page number
    stat_num: float       # stat card number
    table: float          # table text
    page_numbers: bool = False   # two-digit page number bottom-right (brochure)

    @property
    def G(self):          # the one gap: between boxes, and the unit every other spacing is built from
        return round(0.016 * self.width, 2)


FORMATS = {
    # AT3 brochure: A4 landscape pages, 297 x 210 mm, with page numbers (user, 2026-10-22; was A3 portrait)
    "brochure": Format("brochure", 841.89, 595.28, title=36, heading=14, sub=10.5, body=9.5, small=7.5, stat_num=18,
                       table=8.5, page_numbers=True),
    # iSTEAM poster: A3 portrait, same sizes, no page numbers
    "poster": Format("poster", 841.89, 1190.55, title=64, heading=14, sub=11.5, body=10, small=8.5, stat_num=20, table=9),
    # 16:9 slides (20 x 11.25 in), only if a talk deck is ever needed; not the brochure
    "slides": Format("slides", 1440, 810, title=72, heading=20, sub=17, body=15, small=12, stat_num=32, table=13),
}
FORMATS["a3"] = FORMATS["poster"]          # older name


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    w: float
    h: float

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    def inset(self, left, top=None, right=None, bottom=None):
        top = left if top is None else top
        right = left if right is None else right
        bottom = top if bottom is None else bottom
        return Rect(self.x + left, self.y + top, self.w - left - right, self.h - top - bottom)


class DesignError(ValueError):
    pass


def heading_text(number, title):
    """The required box heading format: two-digit number, space, hyphen, space, title in capitals."""
    return f"{number:02d} - {title.upper()}"


HEADING_RE = re.compile(r"^\d{2,3} - [^a-z]+$")   # two digits, or three once a long document passes box 99 (2026-10-22)


def split(rect, weights, gap, vertical=False):
    """Split rect into parts sized by weights, with exactly `gap` between neighbours."""
    total = (rect.h if vertical else rect.w) - gap * (len(weights) - 1)
    out, pos = [], (rect.y if vertical else rect.x)
    for wt in weights:
        size = total * wt / sum(weights)
        out.append(Rect(rect.x, pos, rect.w, size) if vertical else Rect(pos, rect.y, size, rect.h))
        pos += size + gap
    return out


def grid_colours(rows, cols, start=0, avoid=None):
    """Colours for a grid of small parts (stat cards, sub-topic columns) so no two side-by-side or stacked match.

    avoid: a colour to leave out (stat cards leave out the colour of the box they sit in)."""
    pal = [c for c in BOX_COLOURS if c != avoid]
    return [[pal[(start + c + 2 * r) % len(pal)] for c in range(cols)] for r in range(rows)]   # +1 across, +2 down


_FONT_DIR = Path(__file__).resolve().parent / "fonts" / "InterStatic"
_FONT_CACHE = {}


def _font(bold):
    """The static Inter the PDF embeds (assets/fonts/InterStatic), loaded at 100 pt for measuring; None if missing."""
    if bold not in _FONT_CACHE:
        path = _FONT_DIR / ("InterStatic-Bold.ttf" if bold else "InterStatic-Regular.ttf")
        try:
            from PIL import ImageFont
            _FONT_CACHE[bold] = ImageFont.truetype(str(path), 100)
        except (OSError, ImportError):
            _FONT_CACHE[bold] = None
    return _FONT_CACHE[bold]


def text_width(text, size, bold=False, em=0.6):
    """Width in pt of plain text at `size` pt, measured with the real font (estimate from `em` if it is missing)."""
    font = _font(bold)
    if font is None:
        return len(text) * size * em
    return font.getlength(text) * size / 100


def lines_needed(text, size, width, em=0.6, bold=False):
    """Lines `text` needs at `size` pt in `width` pt, word-wrapped with real Inter widths ('**bold**' runs measured bold).

    Measured since 2026-10-22: the earlier per-character guess (0.5-0.7 em) predicted a second line that never came in
    narrow boxes, so fitted highlights were drawn too tall (brochure v20, page 3, box 05)."""
    words = []                                    # (word, bold) in reading order
    for run, b in _runs(text):
        words += [(w, b or bold) for w in run.split()]
    lines, cur = 1, 0.0
    for w, b in words:
        wl = text_width(w, size, b, em)
        add = wl if cur == 0 else wl + text_width(" ", size, b, em)
        if cur + add > width and cur > 0:
            lines, cur = lines + 1, wl
        else:
            cur += add
        while cur > width:                        # a single word longer than the line
            lines, cur = lines + 1, cur - width
    return lines


def _rgb(h):
    return RGBColor.from_string(h)


def _shape(slide, kind, r, fill, line=None, width=0, radius=None):
    s = slide.shapes.add_shape(kind, Pt(r.x), Pt(r.y), Pt(r.w), Pt(r.h))
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = _rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = _rgb(line)
        s.line.width = Pt(width)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    if radius is not None and kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = min(0.5, radius / min(r.w, r.h))     # same radius in points whatever the shape size
    if s.has_text_frame:
        s.text_frame.text = ""
    return s


_BOLD = re.compile(r"\*\*(.+?)\*\*")


def _runs(s):
    """'plain **bold** plain' -> [(text, bold)]"""
    out, pos = [], 0
    for m in _BOLD.finditer(s):
        if m.start() > pos:
            out.append((s[pos:m.start()], False))
        out.append((m.group(1), True))
        pos = m.end()
    if pos < len(s):
        out.append((s[pos:], False))
    return out


def _text(slide, r, paras, size, color=SLATE, bold=False, font=FONT, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT,
          after=None, bullet_color=None, line=1.15, name=None):
    """paras: list of str ('**bold**' allowed; a leading '- ' makes a bullet) or dicts {text, size, color, bold, align}."""
    box = slide.shapes.add_textbox(Pt(r.x), Pt(r.y), Pt(r.w), Pt(r.h))
    if name:
        box.name = name
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, p in enumerate(paras):
        p = p if isinstance(p, dict) else {"text": p}
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = p.get("align", align)
        para.line_spacing = line
        para.space_after = Pt(p.get("after", size * 0.45 if after is None else after))
        txt = p["text"]
        is_bullet = txt.startswith("- ")
        if is_bullet:
            txt = txt[2:]
            pPr = para._p.get_or_add_pPr()
            pPr.set("marL", str(Pt(size * 1.1)))
            pPr.set("indent", str(-Pt(size * 1.1)))
            ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
            bc = etree.SubElement(pPr, ns + "buClr")
            etree.SubElement(bc, ns + "srgbClr", val=bullet_color or p.get("color", color))
            etree.SubElement(pPr, ns + "buChar", char="•")
        for t, b in _runs(txt):
            run = para.add_run()
            run.text = t
            run.font.name = p.get("font", font)
            run.font.size = Pt(p.get("size", size))
            run.font.bold = b or p.get("bold", bold)
            run.font.color.rgb = _rgb(p.get("color", color))
    return box


def _picture(slide, path, r, alt, align="center"):
    if not alt:
        raise DesignError("every picture needs alt text")
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    iw, ih = Image.open(path).size
    s = min(r.w / iw, r.h / ih)
    pw, ph = iw * s, ih * s
    x = r.x + (r.w - pw) / 2 if align == "center" else (r.r - pw if align == "right" else r.x)
    pic = slide.shapes.add_picture(str(path), Pt(x), Pt(r.y + (r.h - ph) / 2), Pt(pw), Pt(ph))
    pic._element.nvPicPr.cNvPr.set("descr", alt)
    return Rect(x, r.y + (r.h - ph) / 2, pw, ph)


@dataclass
class Box:
    """A content box: coloured rounded rectangle behind, white rounded rectangle on top (thin sides, thick top)."""
    page: "Page"
    rect: Rect
    colour: str
    number: int
    title: str
    content: Rect = None
    notes: list = field(default_factory=list)

    @property
    def accent(self):
        return ACCENT[self.colour]

    @property
    def heading(self):
        return heading_text(self.number, self.title)

    # ---- components placed inside the box (pass a sub-rect of box.content) ----
    def text(self, r, paras, size=None, **kw):
        return _text(self.page.slide, r, paras, size or self.page.fmt.body, bullet_color=self.colour, **kw)

    def picture(self, r, path, alt, caption=None, align="center"):
        f = self.page.fmt
        if caption:
            cap_h = f.small * 2.6
            img = _picture(self.page.slide, path, Rect(r.x, r.y, r.w, r.h - cap_h - 0.3 * f.G), alt, align)
            _text(self.page.slide, Rect(r.x, img.b + 0.3 * f.G, r.w, cap_h), [caption], f.small, align=PP_ALIGN.CENTER)
            return img
        return _picture(self.page.slide, path, r, alt, align)

    def highlight(self, r, text, kind="general", label=None, size=None, fit=True):
        """Highlighted paragraph: rounded tint panel with a thick coloured bar down the left, slate text.

        kind: "general" = this box's colour, "result" = green, "caution" = yellow. label: optional bold first line."""
        if kind == "general":
            c = self.colour
        elif kind in HIGHLIGHT:
            c = HIGHLIGHT[kind]
        else:
            raise DesignError(f"highlight kind must be 'general', 'result' or 'caution', not {kind!r}")
        f = self.page.fmt
        paras = text if isinstance(text, list) else [text]
        if label:
            paras = [f"**{label}**"] + paras
        size = size or f.body
        if fit:                       # only as tall as its text (user, 2026-10-22), at the top of the space given
            r = Rect(r.x, r.y, r.w, min(r.h, self.highlight_height(r.w, paras, size)))
        _shape(self.page.slide, MSO_SHAPE.ROUNDED_RECTANGLE, r, c, radius=f.small_radius)          # colour behind
        _shape(self.page.slide, MSO_SHAPE.ROUNDED_RECTANGLE, r.inset(f.bar, 0, 0, 0), ACCENT[c],    # tint on top,
               radius=f.small_radius)                                                             # inset on the left
        body = r.inset(f.bar + 0.6 * f.G, 0.3 * f.G, 0.6 * f.G, 0.3 * f.G)
        _text(self.page.slide, body, paras, size, anchor=MSO_ANCHOR.MIDDLE, after=0.25 * f.body)
        return r

    def text_height(self, width, paras, size=None, after=None):
        """Estimated height of paras (as given to text()) set in `width` pt. Used to stack parts without gaps."""
        f = self.page.fmt
        total = 0.0
        for q in paras:
            q = q if isinstance(q, dict) else {"text": q}
            sz = q.get("size", size or f.body)
            t = q["text"]
            w = width
            if t.startswith("- "):
                t, w = t[2:], width - sz * 1.1
            plain = t.replace("**", "")
            bold = q.get("bold", False) or (t.startswith("**") and t.endswith("**"))
            n = lines_needed(t, sz, w, bold=bold)
            sp = q.get("after", sz * 0.45 if after is None else after)
            total += n * sz * 1.2 * 1.15 + sp
        return total + 2

    def highlight_height(self, width, paras, size=None):
        f = self.page.fmt
        inner = width - (f.bar + 1.2 * f.G)
        return self.text_height(inner, paras, size, after=0.25 * f.body) + 0.6 * f.G + 2

    def stack(self, r, items, gap=None):
        """Place parts one under another: ("text", paras), ("highlight", text, kind), ("fill", weight, draw).

        Text and highlights get the height their words need; "fill" parts (pictures, charts, tables) share what is
        left, by weight, and draw(rect) puts them in. With no fill part, closing highlights go to the bottom and the
        rest sit at the top. Returns the rects."""
        f = self.page.fmt
        gap = 0.5 * f.G if gap is None else gap
        need = []
        for it in items:
            if it[0] == "text":
                need.append(self.text_height(r.w, it[1], it[2] if len(it) > 2 else None))
            elif it[0] == "highlight":
                need.append(self.highlight_height(r.w, it[1] if isinstance(it[1], list) else [it[1]]))
            else:
                need.append(None)
        fixed = sum(h for h in need if h is not None) + gap * (len(items) - 1)
        weights = [it[1] for it in items if it[0] == "fill"]
        spare = max(0.0, r.h - fixed)
        # With nothing to stretch, highlights that close the box sit at its bottom (user, 2026-10-22), so they line
        # up with the closing highlights in the boxes beside it; the spare space goes above them.
        first_closing = len(items)
        while first_closing > 0 and items[first_closing - 1][0] == "highlight":
            first_closing -= 1
        y, rects = r.y, []
        for k, (it, h) in enumerate(zip(items, need)):
            if not weights and k == first_closing and k > 0:
                y += spare
            h = h if h is not None else spare * it[1] / sum(weights)
            rr = Rect(r.x, y, r.w, h)
            rects.append(rr)
            if it[0] == "text":
                self.text(rr, it[1], it[2] if len(it) > 2 else None)
            elif it[0] == "highlight":
                self.highlight(rr, it[1], it[2] if len(it) > 2 else "general")
            else:
                it[2](rr)
            y += h + gap
        return rects

    def callout(self, r, text, label="Key Finding:", kind="general"):
        """A highlight with a bold label, e.g. under a chart: what to notice in it."""
        return self.highlight(r, text, kind, label)

    def stats(self, r, items, cols=2, colours=None):
        """Key numbers only. items = [(number, label)]. Tint fill, full colour outline, big bold number in colour,
        slate label. Every card in the box is a different colour: up to 3 cards never use the box's colour; with 4,
        each of the four colours is used once (the box's colour last). Over 4, only neighbouring cards differ."""
        f = self.page.fmt
        n = len(items)
        rows = -(-n // cols)
        others = [c for c in BOX_COLOURS if c != self.colour]
        if colours is None:
            colours = (others + [self.colour])[:n] if n <= 4 else [c for row in grid_colours(rows, cols) for c in row]
        colours = list(colours)[:n]
        if n <= 4 and len(set(colours)) < n:
            raise DesignError("stat cards in one box must all be different colours")
        if n <= 3 and self.colour in colours:
            raise DesignError("up to 3 stat cards must not use the colour of the box they sit in")
        cells = [c for row in split(r, [1] * rows, 0.5 * f.G, vertical=True) for c in split(row, [1] * cols, 0.5 * f.G)]
        for (num, label), cell, c in zip(items, cells, colours):
            _shape(self.page.slide, MSO_SHAPE.ROUNDED_RECTANGLE, cell, ACCENT[c], c, f.outline, f.small_radius)
            inner = cell.inset(0.55 * f.G, 0.2 * f.G)
            _text(self.page.slide, inner, [{"text": str(num), "size": f.stat_num, "color": c, "bold": True, "after": 0},
                                           {"text": label, "bold": True}], f.body, anchor=MSO_ANCHOR.MIDDLE, line=1.0)

    def subtopics(self, r, items, cols=4, colours=None):
        """Sub-topic grid: coloured rule on top, bold coloured subheading, slate paragraph. items = [(title, text)]."""
        f = self.page.fmt
        rows = -(-len(items) // cols)
        colours = colours or [c for row in grid_colours(rows, cols) for c in row]
        cells = [c for row in split(r, [1] * rows, 0.8 * f.G, vertical=True) for c in split(row, [1] * cols, f.G)]
        for (title, body), cell, c in zip(items, cells, colours):
            _shape(self.page.slide, MSO_SHAPE.RECTANGLE, Rect(cell.x, cell.y, cell.w, f.rule), c)
            top = cell.y + f.rule + 0.5 * f.G
            _text(self.page.slide, Rect(cell.x, top, cell.w, cell.b - top),
                  [{"text": title, "size": f.sub, "color": c, "bold": True, "after": 0.3 * f.body}, body], f.body)

    def steps(self, r, items, colour=None):
        """Numbered steps: rounded square badge in solid colour with a white digit, text to the right."""
        f, c = self.page.fmt, colour or self.colour
        side = 2.6 * f.body
        for i, (cell, t) in enumerate(zip(split(r, [1] * len(items), 0.5 * f.G, vertical=True), items), 1):
            badge = Rect(cell.x, cell.y + (cell.h - side) / 2, side, side)
            _shape(self.page.slide, MSO_SHAPE.ROUNDED_RECTANGLE, badge, c, radius=0.2 * side)
            _text(self.page.slide, badge, [str(i)], 1.9 * f.body, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE,
                  align=PP_ALIGN.CENTER, after=0, line=1.0)
            _text(self.page.slide, Rect(badge.r + 0.8 * f.G, cell.y, cell.r - badge.r - 0.8 * f.G, cell.h), [t], f.body,
                  anchor=MSO_ANCHOR.MIDDLE)

    def table(self, r, rows, col_weights=None, align_numbers=True, status_col=None, bold_col=None):
        """Table: header row in the box colour with white bold text, white and box-tint alternate rows, slate text.

        status_col: a column of verdict words (STATUS); those cells get the verdict's tint and bold text.
        bold_col: a column shown in bold (e.g. the row names)."""
        f = self.page.fmt
        n, m = len(rows), len(rows[0])
        t = self.page.slide.shapes.add_table(n, m, Pt(r.x), Pt(r.y), Pt(r.w), Pt(r.h)).table
        weights = col_weights or [1] * m
        col_w = [r.w * wt / sum(weights) for wt in weights]
        for j, cw in enumerate(col_w):
            t.columns[j].width = Pt(cw)
        # Row heights from the text each row holds (PowerPoint grows a row whose text wraps, so stretching every row
        # evenly pushed tables past their box); only the space left over is shared out, so the table fills its slot
        # when it fits and is no taller than its text when it does not.
        pad_y, pad_x = 0.3 * f.G, 0.8 * f.G
        need = [max(lines_needed(str(rows[i][j]), f.table, col_w[j] - pad_x, bold=(i == 0 or j in (bold_col, status_col)))
                    for j in range(m)) * f.table * 1.2 + pad_y + 2 for i in range(n)]
        extra = max(0.0, (r.h - sum(need)) / n)
        for i in range(n):
            t.rows[i].height = Pt(need[i] + extra)
            for j in range(m):
                cell = t.cell(i, j)
                cell.fill.solid()
                verdict = STATUS.get(str(rows[i][j]).upper()) if (i > 0 and j == status_col) else None
                cell.fill.fore_color.rgb = _rgb(self.colour if i == 0 else ACCENT[verdict] if verdict
                                                else (WHITE if i % 2 else self.accent))
                cell.margin_left = cell.margin_right = Pt(0.4 * f.G)
                cell.margin_top = cell.margin_bottom = Pt(0.15 * f.G)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                tf = cell.text_frame
                tf.text = ""
                val = str(rows[i][j])
                p = tf.paragraphs[0]
                numeric = bool(re.fullmatch(r"[-+~]?[\d.,]+\s*%?\S{0,4}", val))
                p.alignment = PP_ALIGN.RIGHT if (align_numbers and numeric and i > 0) else PP_ALIGN.LEFT
                run = p.add_run()
                run.text = val
                run.font.name = FONT
                run.font.size = Pt(f.table)
                run.font.bold = i == 0 or j == bold_col or (i > 0 and j == status_col)
                run.font.color.rgb = _rgb(WHITE if i == 0 else SLATE)
        return t

    def head(self, text):
        """A sub-heading paragraph for box.text(): bold, in the box colour."""
        return {"text": text, "size": self.page.fmt.sub, "color": self.colour, "bold": True,
                "after": 0.25 * self.page.fmt.body}

    def annotate(self, img, fx, fy, text, lx, ly):
        """Label a point on a picture: (fx, fy) and the label centre (lx, ly) are fractions of the picture's rect `img`.
        A small white label with the box's colour outline, joined to the point by an arrow."""
        f = self.page.fmt
        tw = text_width(text, f.small, True) + 0.9 * f.G
        th = f.small * 2.0
        cx = min(max(img.x + lx * img.w, img.x + tw / 2), img.r - tw / 2)
        cy = min(max(img.y + ly * img.h, img.y + th / 2), img.b - th / 2)
        lab = Rect(cx - tw / 2, cy - th / 2, tw, th)
        self.arrow(cx, cy, img.x + fx * img.w, img.y + fy * img.h)
        _shape(self.page.slide, MSO_SHAPE.ROUNDED_RECTANGLE, lab, WHITE, self.colour, f.outline, radius=0.3 * f.G)
        _text(self.page.slide, lab, [text], f.small, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER,
              after=0, line=1.0)
        return lab

    def labelled(self, r, path, alt, caption=None, labels=()):
        """A picture with arrows to its parts: labels = [(fx, fy, text, lx, ly)], the point and the label centre as
        fractions of the picture (see annotate). Use for photos of a build or CAD views."""
        img = self.picture(r, path, alt, caption=caption)
        for fx, fy, text, lx, ly in labels:
            self.annotate(img, fx, fy, text, lx, ly)
        return img

    def mind_map(self, r, centre, branches, size=None):
        """A mind map: a centre node in the main colour, 2 to 5 branches = [(title, [points])] around it, each in its
        own box colour (tint fill, coloured outline), joined to the centre by lines. size: point text (default small+1)."""
        if not 2 <= len(branches) <= 5:
            raise DesignError("mind_map takes 2 to 5 branches")
        f, G, slide = self.page.fmt, self.page.fmt.G, self.page.slide
        size = size or f.small + 1
        spots = [(0.0, 0.0), (0.68, 0.0), (0.0, 0.53), (0.68, 0.53), (0.34, 0.6)][:len(branches)]
        w = r.w * 0.32
        cbox = Rect(r.x + r.w * 0.36, r.y + r.h * 0.14, r.w * 0.28, r.h * 0.3)
        nodes = []
        for (title, points), (sx, sy), colour in zip(branches, spots, BOX_COLOURS + (BOX_COLOURS[0],)):
            h = r.h * (0.47 if sx != 0.34 else 0.4)
            nodes.append((Rect(r.x + sx * r.w, r.y + sy * r.h, w, h), title, points, colour))
        for node, _t, _p, colour in nodes:               # lines first, so the boxes sit on top
            ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Pt(cbox.x + cbox.w / 2), Pt(cbox.y + cbox.h / 2),
                                            Pt(node.x + node.w / 2), Pt(node.y + node.h / 2))
            ln.line.color.rgb = _rgb(colour)
            ln.line.width = Pt(max(1.0, f.rule))
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cbox, MAIN, radius=G)
        _text(slide, cbox.inset(0.6 * G), [centre], f.sub + 3, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE,
              align=PP_ALIGN.CENTER, after=0)
        for node, title, points, colour in nodes:
            _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, node, ACCENT[colour], colour, f.outline, radius=0.6 * G)
            _text(slide, node.inset(0.5 * G, 0.4 * G), [{"text": title, "size": f.sub, "color": colour, "bold": True,
                                                         "after": 2}] + ["- " + x for x in points], size, after=1,
                  bullet_color=colour)
        return cbox

    def arrow(self, x1, y1, x2, y2, colour=None):
        """A straight arrow (used between flow steps)."""
        ln = self.page.slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Pt(x1), Pt(y1), Pt(x2), Pt(y2))
        ln.line.color.rgb = _rgb(colour or self.colour)
        ln.line.width = Pt(max(1.0, self.page.fmt.rule))
        etree.SubElement(ln.line._get_or_add_ln(), qn("a:tailEnd"), type="triangle", w="med", len="med")
        return ln

    def flow(self, r, items, cols=None, arrows=True, cap_lines=2.7):
        """Flowchart of pictures: items = [(picture, label, caption, alt)]; arrows join neighbours in a row.

        Each step: picture, a rounded tint label (bold slate), a small caption. The output of one step is the input of
        the next. Rows wrap after `cols` steps. arrows=False for a side-by-side comparison. cap_lines: caption height
        in lines of small text (raise it for longer captions)."""
        f = self.page.fmt
        cols = cols or len(items)
        rows = -(-len(items) // cols)
        gap_x, gap_y = 1.6 * f.G, 0.6 * f.G
        for ri, rr in enumerate(split(r, [1] * rows, gap_y, vertical=True)):
            cells = split(rr, [1] * cols, gap_x)
            chunk = items[ri * cols:(ri + 1) * cols]
            n_lab = max(lines_needed(it[1], f.sub, cells[0].w - 0.6 * f.G, bold=True) for it in chunk)
            lab_h = f.sub * (0.8 + 1.25 * n_lab)
            cap_h = f.small * cap_lines if any(it[2] for it in chunk) else 0
            pic_h = rr.h - lab_h - cap_h - 0.6 * f.G
            for ci, ((path, label, caption, alt), cell) in enumerate(zip(chunk, cells)):
                _picture(self.page.slide, path, Rect(cell.x, cell.y, cell.w, pic_h), alt)
                lab = Rect(cell.x, cell.y + pic_h + 0.3 * f.G, cell.w, lab_h)
                _shape(self.page.slide, MSO_SHAPE.ROUNDED_RECTANGLE, lab, self.accent, radius=0.4 * f.G)
                _text(self.page.slide, lab.inset(0.3 * f.G, 0), [label], f.sub, bold=True, anchor=MSO_ANCHOR.MIDDLE,
                      align=PP_ALIGN.CENTER, after=0, line=1.0)
                if caption:
                    _text(self.page.slide, Rect(cell.x, lab.b + 0.3 * f.G, cell.w, cap_h), [caption], f.small,
                          align=PP_ALIGN.CENTER, after=0)
                if arrows and ci + 1 < len(chunk):
                    y = lab.y + lab.h / 2
                    self.arrow(cell.r + 0.2 * f.G, y, cell.r + gap_x - 0.2 * f.G, y)

    def gantt(self, r, days, tasks, label_w=None):
        """Schedule: days = [(date, weekday letter)], tasks = [(name, first date, last date, "good" or "warn")]."""
        f = self.page.fmt
        label_w = label_w or r.w * 0.3
        col_w = (r.w - label_w) / len(days)
        head_h = f.small * 2.6
        row_h = (r.h - head_h) / len(tasks)
        x0 = r.x + label_w
        for k, (d, letter) in enumerate(days):
            _text(self.page.slide, Rect(x0 + k * col_w, r.y, col_w, head_h), [f"**{d}**", letter], f.small,
                  align=PP_ALIGN.CENTER, after=0, line=1.0)
        idx = {d: k for k, (d, _l) in enumerate(days)}
        for i, (name, a, b, kind) in enumerate(tasks):
            y = r.y + head_h + i * row_h
            if i % 2 == 0:
                _shape(self.page.slide, MSO_SHAPE.RECTANGLE, Rect(r.x, y, r.w, row_h), self.accent)
            _text(self.page.slide, Rect(r.x + 0.3 * f.G, y, label_w - 0.4 * f.G, row_h), [name], f.table,
                  anchor=MSO_ANCHOR.MIDDLE, after=0)
            bar = Rect(x0 + idx[a] * col_w + 0.1 * col_w, y + row_h * 0.2, (idx[b] - idx[a] + 0.8) * col_w, row_h * 0.6)
            _shape(self.page.slide, MSO_SHAPE.ROUNDED_RECTANGLE, bar, {"warn": RED, "actual": PURPLE}.get(kind, GREEN),
                   radius=bar.h / 2)

    def timeline(self, r, items, colours=None):
        """Vertical timeline: items = [(date, stage, notes)]. Ring nodes and line segments cycle the box colours."""
        f = self.page.fmt
        colours = colours or [BOX_COLOURS[i % 4] for i in range(len(items))]
        node = 1.0 * f.G
        cells = split(r, [1] * len(items), 0.4 * f.G, vertical=True)
        lx = r.x + node / 2
        for i, ((date, stage, notes), cell, c) in enumerate(zip(items, cells, colours)):
            cy = cell.y + node / 2
            if i + 1 < len(items):
                ln = self.page.slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Pt(lx), Pt(cy), Pt(lx), Pt(cells[i + 1].y + node / 2))
                ln.line.color.rgb = _rgb(c)
                ln.line.width = Pt(f.rule)
            _shape(self.page.slide, MSO_SHAPE.OVAL, Rect(r.x, cell.y, node, node), WHITE, c, f.rule)
            tx = r.x + node + 0.6 * f.G
            _text(self.page.slide, Rect(tx, cell.y - 0.15 * f.body, r.r - tx, cell.h),
                  [{"text": f"{date} - {stage}", "size": f.sub, "color": c, "bold": True, "after": 0.2 * f.body}]
                  + (notes if isinstance(notes, list) else [notes]), f.body)


class Page:
    def __init__(self, doc, title, cover=False, label=None):
        self.doc, self.fmt = doc, doc.fmt
        self.slide = doc.prs.slides.add_slide(doc.prs.slide_layouts[6])
        self.title = title.upper()
        self.boxes: list[Box] = []
        self.number = len(doc.pages) + 1
        f, G = self.fmt, self.fmt.G
        bg = self.slide.background.fill
        bg.solid()
        bg.fore_color.rgb = _rgb(WHITE)
        if cover:                     # the cover draws its own title; no page number
            self.area = Rect(f.margin, f.top + G, f.width - 2 * f.margin, f.height - f.bottom - f.top - G)
            return
        band = Rect(f.margin, f.top, f.width - 2 * f.margin, f.title * 1.15)
        _text(self.slide, band, [self.title], f.title, color=MAIN, font=FONT_TITLE, bold=True,
              anchor=MSO_ANCHOR.MIDDLE, after=0, line=1.0, name="Page title")
        if label:                     # the required section this page belongs to, right of the title
            _text(self.slide, Rect(band.x + band.w * 0.45, band.y, band.w * 0.55, band.h), [label.upper()], f.sub,
                  color=MAIN, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT, after=0, name="Section label")
        if f.page_numbers:
            _text(self.slide, Rect(f.width - f.margin - 4 * G, f.height - f.bottom + 0.5 * G, 4 * G, f.small * 1.4),
                  [f"{self.number:02d}"], f.small, align=PP_ALIGN.RIGHT, name="Page number")
        top = band.b + G
        self.area = Rect(f.margin, top, f.width - 2 * f.margin, f.height - f.bottom - top)

    def sources(self, text):
        """Credits and sources: one small slate line in the bottom margin, left (the page number is on the right)."""
        f, G = self.fmt, self.fmt.G
        return _text(self.slide, Rect(f.margin, f.height - f.bottom + 0.5 * G, f.width - 2 * f.margin - 5 * G, f.small * 2.6),
                     [text], f.small, name="Sources")

    def cols(self, r, *weights):
        return split(r, weights or [1], self.fmt.G)

    def rows(self, r, *weights):
        return split(r, weights or [1], self.fmt.G, vertical=True)

    def neighbours(self, rect):
        return [b for b in self.boxes if _touching(rect, b.rect, self.fmt.G)]

    def box(self, rect, colour, title, number=None):
        """colour: a role ('research', 'design', 'method', 'testing', ...) or one of BOX_COLOURS."""
        f, G = self.fmt, self.fmt.G
        want = ROLES.get(colour, colour) if isinstance(colour, str) else colour
        want = want.upper()
        if want == MAIN:
            raise DesignError("the main colour is for page titles and top-level items, never a content box")
        if want not in BOX_COLOURS:
            raise DesignError(f"unknown box colour or role: {colour!r}")
        used = {b.colour for b in self.neighbours(rect)}
        notes = []
        if want in used:
            alt = next((c for c in BOX_COLOURS if c not in used), None)
            if alt is None:
                raise DesignError(f"box '{title}' touches all four colours; change the layout")
            notes.append(f"'{title}': wanted {NAMES[want]} ({colour}) but it touches a {NAMES[want]} box, so {NAMES[alt]}")
            want = alt
        number = number if number is not None else self.doc.next_number()
        b = Box(self, rect, want, number, title, notes=notes)
        _shape(self.slide, MSO_SHAPE.ROUNDED_RECTANGLE, rect, want, radius=f.radius).name = f"Box {number:02d} back"
        inner = rect.inset(f.side, f.band, f.side, f.side)
        _shape(self.slide, MSO_SHAPE.ROUNDED_RECTANGLE, inner, WHITE, radius=f.radius).name = f"Box {number:02d} panel"
        pad = inner.inset(f.pad)
        n_lines = lines_needed(b.heading, f.heading, pad.w, bold=True)
        head_h = f.heading * (1.3 + 1.2 * (n_lines - 1))
        _text(self.slide, Rect(pad.x, pad.y, pad.w, head_h), [b.heading], f.heading, color=want, bold=True,
              after=0, line=1.0, name=f"Box {number:02d} heading")
        top = pad.y + head_h + 0.5 * G
        b.content = Rect(pad.x, top, pad.w, pad.b - top)
        self.boxes.append(b)
        self.doc.notes += notes
        return b

    def check(self):
        """Problems with this page: touching boxes the same colour, uneven gaps, overlaps, boxes outside the margins."""
        f, G, out = self.fmt, self.fmt.G, []
        for b in self.boxes:
            if b.colour not in BOX_COLOURS:
                out.append(f"box {b.number:02d} uses a non-box colour")
            if not HEADING_RE.match(b.heading):
                out.append(f"box {b.number:02d} heading not 'NN - CAPS': {b.heading!r}")
            r = b.rect
            if r.x < f.margin - 0.5 or r.r > f.width - f.margin + 0.5 or r.b > f.height - f.bottom + 0.5:
                out.append(f"box {b.number:02d} goes outside the page margins")
        for i, a in enumerate(self.boxes):
            for b in self.boxes[i + 1:]:
                gap = _gap(a.rect, b.rect)
                if gap is None:
                    continue
                if gap < -0.5:
                    out.append(f"boxes {a.number:02d} and {b.number:02d} overlap")
                elif gap < 1.75 * G:
                    if abs(gap - G) > 0.5:
                        out.append(f"gap between boxes {a.number:02d} and {b.number:02d} is {gap:.1f} pt, not G = {G} pt")
                    if a.colour == b.colour:
                        out.append(f"boxes {a.number:02d} and {b.number:02d} touch and are both {NAMES[a.colour]}")
        return [f"page {self.number} ({self.title}): {p}" for p in out]


def _gap(a, b):
    """Gap between two rects that face each other across one edge (overlapping in the other direction), else None."""
    over_x = min(a.r, b.r) - max(a.x, b.x)
    over_y = min(a.b, b.b) - max(a.y, b.y)
    if over_y > 1:                                   # side by side
        return max(a.x, b.x) - min(a.r, b.r) if over_x <= 0 else -over_x
    if over_x > 1:                                   # one above the other
        return max(a.y, b.y) - min(a.b, b.b) if over_y <= 0 else -over_y
    return None


def _touching(a, b, G):
    g = _gap(a, b)
    return g is not None and g < 1.75 * G


class Doc:
    """One brochure or poster set. Box numbers run on continuously across every page."""

    def __init__(self, fmt="brochure", first_number=1):
        self.fmt = _derived(FORMATS[fmt] if isinstance(fmt, str) else fmt)
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = Pt(self.fmt.width), Pt(self.fmt.height)
        self.pages: list[Page] = []
        self._next = first_number
        self.notes: list[str] = []

    def next_number(self):
        n = self._next
        self._next += 1
        return n

    def page(self, title, cover=False, label=None):
        p = Page(self, title, cover, label)
        self.pages.append(p)
        return p

    def check(self):
        out = [p for page in self.pages for p in page.check()]
        nums = [b.number for page in self.pages for b in page.boxes]
        if nums and nums != list(range(nums[0], nums[0] + len(nums))):
            out.append(f"box numbers are not continuous: {nums}")
        return out

    def save(self, path, strict=True):
        problems = self.check()
        if problems and strict:
            raise DesignError("design system check failed:\n  " + "\n  ".join(problems))
        self.prs.save(path)
        return problems

    def save_versioned(self, project, name, note, strict=True):
        problems = self.check()
        if problems and strict:
            raise DesignError("design system check failed:\n  " + "\n  ".join(problems))
        return save_versioned(self.prs, project, name, note)


def save_versioned(prs, project, name, note):
    """Save as project/outputs/<project>/<name>_vNN.pptx (next free number, never overwrites) and log it in VERSIONS.md."""
    import datetime
    folder = OUTPUTS / project
    folder.mkdir(parents=True, exist_ok=True)
    nums = [int(m.group(1)) for f in folder.glob(f"{name}_v*.pptx")
            if (m := re.fullmatch(rf"{re.escape(name)}_v(\d+)\.pptx", f.name))]
    path = folder / f"{name}_v{max(nums, default=0) + 1:02d}.pptx"
    prs.save(path)
    log = folder / "VERSIONS.md"
    if not log.exists():
        log.write_text(f"# {project}: versions\n\n| File | Date | What changed |\n|---|---|---|\n", encoding="utf-8")
    with log.open("a", encoding="utf-8") as fh:
        fh.write(f"| {path.name} | {datetime.date.today()} | {note} |\n")
    return path


class _Derived:
    """A Format plus every spacing value built from G (see DESIGN_SYSTEM.md, 'Spacing')."""

    def __init__(self, f):
        self._f = f
        G = f.G
        self.margin = 3 * G           # left and right page margin
        self.top = 1.2 * G            # above the page title
        self.bottom = 2.5 * G         # below the last box (brochure page number sits here)
        self.radius = G               # corner radius of both box rectangles (equal)
        self.band = 0.8 * G           # coloured band at the top of a box
        self.side = 0.15 * G          # coloured edge on the sides and bottom
        self.pad = 0.75 * G           # white space inside the white panel
        self.small_radius = 0.5 * G   # stat cards, highlights
        self.outline = max(1.0, 0.1 * G)   # stat card and highlight outline
        self.rule = 0.22 * G          # sub-topic top rule, timeline line and rings
        self.bar = 0.35 * G           # left bar of a callout

    def __getattr__(self, k):
        return getattr(self._f, k)


def _derived(f):
    return _Derived(f)
