"""Starter build script for an A3 portrait poster (one page) in the design system. Copy it to project/outputs/<deliverable>/ and fill it in.

    python project/outputs/poster/build_poster.py            # saves the next version, poster_vNN.pptx
    python project/outputs/poster/build_poster.py --draft x.pptx
    python general/tools/export_pdf.py project/outputs/brochure/poster_vNN.pptx --render project/outputs/renders/vNN

Every fact on a page should come from project/logs/ or a cited source. Pictures from project/assets/.
"""
import sys
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "general" / "design").is_dir())
sys.path.insert(0, str(ROOT / "general" / "design"))
from design_system import Doc, Rect  # noqa: E402

A = ROOT / "project" / "assets"
DELIVERABLE = "poster"


def build():
    doc = Doc("poster")
    f = doc.fmt
    p = doc.page("<Project title>")
    top, mid, low, bottom = p.rows(p.area, 0.8, 1.3, 1.3, 0.8)

    l, r = p.cols(top, 1.4, 1)
    a = p.box(l, "problem", "The problem")
    a.stack(a.content, [("text", ["<the problem, with a source>"]),
                        ("highlight", "**Goal:** <one measurable sentence>", "general")])
    b = p.box(r, "research", "Key numbers")
    b.stats(b.content, [("<00>", "<what it measures>"), ("<00>", "<what it measures>")], cols=1)

    l, r = p.cols(mid, 1, 1)
    c = p.box(l, "design", "Our design")
    c.text(c.content, ["<what was made and why; a labelled photo or CAD view goes well here>"])
    d = p.box(r, "method", "How it works")
    d.steps(d.content, ["**Step one:** <what happens>", "**Step two:** <what happens>", "**Step three:** <what happens>"])

    l, r = p.cols(low, 1, 1)
    e = p.box(l, "testing", "Testing")
    rows = [["Test", "Result", "Status"], ["<test>", "<number and unit>", "MET"],
            ["<test>", "<number and unit>", "PARTLY MET"]]
    e.stack(e.content, [("text", ["<what was tested and how>"]),          # a table only as tall as its rows
                        ("fill", 1, lambda rr: e.table(Rect(rr.x, rr.y, rr.w, min(rr.h, len(rows) * 2.6 * f.table)),
                                                       rows, status_col=2))])
    g = p.box(r, "results", "Results")
    g.stack(g.content, [("text", ["<results from project/logs/TESTS.md>"]),
                        ("highlight", "**Result:** <the headline number>", "result")])

    h = p.box(bottom, "planning", "Evaluation and next steps")
    h.text(h.content, ["- <what worked>", "- <what did not>", "- <what we would do next>"])
    p.sources("Sources: <where each fact on this poster comes from>")
    return doc


if __name__ == "__main__":
    doc = build()
    if "--draft" in sys.argv:
        print(doc.save(sys.argv[-1]), *doc.notes, sep="\n  ")
    else:
        print(doc.save_versioned(DELIVERABLE, DELIVERABLE, sys.argv[1] if len(sys.argv) > 1 else "first version"))
