"""Starter build script for a brochure in the design system. Copy it to project/outputs/<deliverable>/ and fill it in.

    python project/outputs/brochure/build_brochure.py            # saves the next version, brochure_vNN.pptx
    python project/outputs/brochure/build_brochure.py --draft x.pptx
    python general/tools/export_pdf.py project/outputs/brochure/brochure_vNN.pptx --render project/outputs/renders/vNN

Every fact on a page should come from project/logs/ or a cited source. Pictures from project/assets/.
"""
import sys
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "general" / "design").is_dir())
sys.path.insert(0, str(ROOT / "general" / "design"))
from design_system import Doc  # noqa: E402

A = ROOT / "project" / "assets"
DELIVERABLE = "brochure"
SECTIONS = ("1  Section one", "2  Section two")      # the rubric's required sections, as page labels


def build():
    doc = Doc("brochure")
    f = doc.fmt

    # ---- cover
    p = doc.page("Cover", cover=True)
    left, right = p.cols(p.area, 1, 1.05)
    box = p.box(right, "design", "Design goal")
    box.text(box.content, ["<the design goal in one or two sentences>"])

    # ---- contents
    p = doc.page("Contents")
    c = p.box(p.area, "planning", "Contents")
    c.text(c.content, [c.head(SECTIONS[0]), "**03**   First page", c.head(SECTIONS[1]), "**04**   Second page"])

    # ---- a content page
    p = doc.page("Problem", label=SECTIONS[0])
    top, bottom = p.rows(p.area, 1, 1)
    a = p.box(top, "problem", "The problem")
    a.stack(a.content, [("text", ["<the problem, with a source>"]),
                        ("highlight", "**Key point:** <one sentence>", "general")])
    l_r, r_r = p.cols(bottom, 1, 1)
    g = p.box(l_r, "planning", "Our goal")
    g.text(g.content, ["<measurable goal>"])
    i = p.box(r_r, "research", "Constraints")
    i.text(i.content, ["- <time>", "- <budget>", "- <hardware>"])
    p.sources("Sources: <where each fact on this page comes from>")

    p = doc.page("Next page", label=SECTIONS[1])
    b = p.box(p.area, "results", "Results")
    b.text(b.content, ["<results from project/logs/TESTS.md>"])
    return doc


if __name__ == "__main__":
    doc = build()
    if "--draft" in sys.argv:
        print(doc.save(sys.argv[-1]), *doc.notes, sep="\n  ")
    else:
        print(doc.save_versioned(DELIVERABLE, DELIVERABLE, sys.argv[1] if len(sys.argv) > 1 else "first version"))
