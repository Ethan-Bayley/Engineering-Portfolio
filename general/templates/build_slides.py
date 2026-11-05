"""Starter build script for a 16:9 slide deck (a talk) in the design system. Copy it to project/outputs/<deliverable>/ and fill it in.

    python project/outputs/slides/build_slides.py            # saves the next version, slides_vNN.pptx
    python project/outputs/slides/build_slides.py --draft x.pptx
    python general/tools/export_pdf.py project/outputs/brochure/slides_vNN.pptx --render project/outputs/renders/vNN

Every fact on a page should come from project/logs/ or a cited source. Pictures from project/assets/.
"""
import sys
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "general" / "design").is_dir())
sys.path.insert(0, str(ROOT / "general" / "design"))
from design_system import Doc, Rect  # noqa: E402

A = ROOT / "project" / "assets"
DELIVERABLE = "slides"


def build():
    doc = Doc("slides")
    f = doc.fmt

    # ---- title slide: one box with the goal; the title is the page title
    p = doc.page("<Project title>")
    a = p.box(p.area, "design", "What we set out to do")
    a.stack(a.content, [("text", ["<one or two sentences: the problem and what was made>"]),
                        ("highlight", "**Goal:** <one measurable sentence>", "general")])

    # ---- one idea per slide: few words, big type, one picture or number
    p = doc.page("The problem")
    l, r = p.cols(p.area, 1.2, 1)
    b = p.box(l, "problem", "Why it matters")
    b.text(b.content, ["- <point>", "- <point>", "- <point>"])
    c = p.box(r, "research", "Key number")
    c.stack(c.content, [("text", ["<one line of context for the number>"]),
                        ("fill", 1, lambda rr: c.stats(Rect(rr.x, rr.y, rr.w, min(rr.h, 4 * f.stat_num)),
                                                       [("<00>", "<what it measures>")], cols=1))])

    p = doc.page("Results")
    d = p.box(p.area, "results", "What we found")
    d.stack(d.content, [("text", ["<results from project/logs/TESTS.md>"]),
                        ("highlight", "**Result:** <the headline number>", "result")])
    p.sources("Sources: <where each fact comes from>")
    return doc


if __name__ == "__main__":
    doc = build()
    if "--draft" in sys.argv:
        print(doc.save(sys.argv[-1]), *doc.notes, sep="\n  ")
    else:
        print(doc.save_versioned(DELIVERABLE, DELIVERABLE, sys.argv[1] if len(sys.argv) > 1 else "first version"))
