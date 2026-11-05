"""Build the FTC portfolio for 11143 Barker Yellowbacks (2026-27, BIOBUZZ): the cover plus up to 15 pages.

    python project/outputs/portfolio/build_portfolio.py "what changed"      # saves portfolio_vNN.pptx
    python project/outputs/portfolio/build_portfolio.py --draft x.pptx
    python general/tools/export_pdf.py project/outputs/portfolio/portfolio_vNN.pptx --render project/outputs/renders/vNN
    python general/tools/hand_in_check.py --deliverable portfolio --max-pages 16 --max-mb 15 --min-pt 10

Look: project/design/PORTFOLIO_STYLE.md (the team's cover, colours tightened). FTC A201: cover (team number; not
judged) + at most 15 pages, nothing under 10 pt, first names and last initials only, work since 1 January 2026.
Placeholders only so far: the content is the team's (PROJECT.md, AI credit). The robot drawings are low-resolution
crops of the user's cover image, for layout only: replace them with full-size line art.
"""
import sys
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "general" / "design").is_dir())
sys.path.insert(0, str(ROOT / "project" / "design"))
from portfolio_style import (G, INK, MUTED, Portfolio, Rect, bar, polygon, pill, pill_width,  # noqa: E402
                             stripes, width, write)
from design_system import _picture, _shape  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402

A = ROOT / "project" / "assets"
ROBOT_A = A / "cover" / "robot_schematic_a_lowres.png"
ROBOT_B = A / "cover" / "robot_schematic_b_lowres.png"
DELIVERABLE = "portfolio"
TEAM, TEAM_NAME = "11143", "Barker Yellowbacks"


def cover(doc):
    """The user's cover (2026-11-05) with one yellow instead of gold and cream; no FIRST logo yet (add the official
    file if the team wants it, following FIRST's logo rules)."""
    p = doc.cover()
    s = p.slide
    a = p.area
    # banner: two lines of dark caps on yellow, slanted right end, hazard stripes under it
    by, bh = a.y + 1.2 * G, 64
    bw = width("ENGINEERING", 24, True) + 3.5 * G
    polygon(s, [(14, by), (14 + bw + 30, by), (14 + bw, by + bh), (14, by + bh)])
    write(s, Rect(a.x, by + 4, bw, bh - 8), [{"text": "ENGINEERING", "size": 24, "bold": True, "colour": INK, "after": 0},
                                              {"text": "PORTFOLIO", "size": 24, "bold": True, "colour": INK, "after": 0}],
          anchor=MSO_ANCHOR.MIDDLE, sizes=p.sizes)
    stripes(s, 14 + bw + 1.2 * G, by + bh + 0.6 * G, 22, n=5)
    # pill and team name
    py = by + bh + 4.4 * G
    text = "FTC - FIRST Tech Challenge"
    pill(s, Rect(a.x, py, pill_width(text, 11), 22), text, 11, filled=False, sizes=p.sizes)
    write(s, Rect(a.x, py + 30, a.w, 40), ["BARKER **YELLOWBACKS**"], 30, bold=True, sizes=p.sizes)
    # robot line art, team number box on the right
    ry = py + 80
    nb = Rect(a.r - 64, ry, 64, 270)
    _shape(s, MSO_SHAPE.RECTANGLE, nb, None, MUTED, 2)
    write(s, Rect(nb.x + nb.w / 2 - nb.h / 2, nb.y + nb.h / 2 - nb.w / 2, nb.h, nb.w),
          [{"text": TEAM, "size": 54, "bold": True, "colour": MUTED, "align": PP_ALIGN.CENTER, "after": 0}],
          anchor=MSO_ANCHOR.MIDDLE, rotation=90, sizes=p.sizes)
    bar(s, nb.x - 0.8 * G - 5, nb.y + 0.15 * nb.h, nb.h * 0.7, 5)
    _picture(s, ROBOT_A, Rect(a.x - 0.5 * G, ry, nb.x - a.x - 2 * G, 270), "Line drawing of our robot", "left")
    # season block bottom-left, second drawing bottom-right
    yb = a.b - 150
    bar(s, a.x, yb + 0.6 * G, 92, 4)
    write(s, Rect(a.x + 1.4 * G, yb, 200, 110), [{"text": "2026-2027", "size": 22, "bold": True, "after": 2},
                                                  {"text": "Sydney", "size": 20, "after": 0},
                                                  {"text": "Australia", "size": 20, "after": 0}], sizes=p.sizes)
    _picture(s, ROBOT_B, Rect(a.x + 0.42 * a.w, a.b - 230, 0.58 * a.w, 230), "Second line drawing of our robot",
             "right")
    return p


def build():
    doc = Portfolio(TEAM, TEAM_NAME)
    cover(doc)

    # ---- 1: team (layout example; replace with the page plan)
    p = doc.page("Meet the team")
    top, mid, bottom = p.rows(p.area, 1.6, 1, 1.1)
    t = p.box(top, "Our team")
    t.team(t.content, [("<Name I.>", "<Role>", None, "<one line>"), ("<Name I.>", "<Role>", None, "<one line>"),
                       ("<Name I.>", "<Role>", None, "<one line>"), ("<Name I.>", "<Role>", None, "<one line>")])
    tl = p.box(mid, "Our season")
    tl.timeline(tl.content, [("<Month>", "<Stage>", "<what happened>"), ("<Month>", "<Stage>", "<what happened>"),
                             ("<Month>", "<Stage>", "<what happened>"), ("<Month>", "<Stage>", "<what happened>")])
    pv = p.box(bottom, "Planned against actual")
    pv.plan_vs_actual(pv.content, ["<M1>", "<M2>", "<M3>", "<M4>"], [("<Design>", 0, 1, 0, 1), ("<Build>", 1, 2, 1, 3),
                                                                      ("<Code>", 2, 3, 2, 3)])

    # ---- 2: a mechanism: labelled line art, challenge -> solution, comparison, iterations
    p = doc.page("<Mechanism>")
    top, mid, bottom = p.rows(p.area, 1.35, 1.05, 1)
    l_r, r_r = p.cols(top, 1.2, 1)
    cad = p.box(l_r, "<Mechanism> overview")
    cad.labelled(cad.content.inset(2.5 * G, 1.5 * G), ROBOT_A, "<line drawing of the mechanism>",
                 labels=[(0.45, 0.2, "<roller intake>", 0.12, 0.0), (0.3, 0.8, "<drivetrain>", 0.95, 1.0)])
    st = p.box(r_r, "How it got here")
    st.story(st.content, [("Challenge", "<what went wrong, with a number>"), ("Solution", "<what we changed>"),
                          ("Final solution", "<result, with a **number**>")])
    l_r, r_r = p.cols(mid, 1, 1)
    k = p.box(l_r, "Key features", accent=True)
    k.text(k.content, ["- **<0:0 ratio>** <why>", "- **<0 mm>** <why>", "- <feature>"])
    c = p.box(r_r, "Options compared")
    c.table(c.content, [["Option", "Score", "Status"], ["<option A>", "<0>", "CHOSEN"], ["<option B>", "<0>", "NOT CHOSEN"]],
            status_col=2)
    it = p.box(bottom, "Iterations")
    it.iterations(it.content, [("V1 <name>", None, "", ["<pro>"], ["<con>"]),
                               ("V2 <name>", None, "", ["<pro>"], ["<con>"]),
                               ("V3 <name>", None, "", ["<pro>", "<pro>"], [])])
    return doc


if __name__ == "__main__":
    doc = build()
    if "--draft" in sys.argv:
        print(doc.save(sys.argv[-1]))
    else:
        print(doc.save_versioned(DELIVERABLE, DELIVERABLE, sys.argv[1] if len(sys.argv) > 1 else "first version"))
