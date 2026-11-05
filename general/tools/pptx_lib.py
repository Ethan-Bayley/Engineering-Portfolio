"""Generic python-pptx helpers for editing an existing deck (adapted from the Enginnering-Notebook-ai repo, VEX parts removed).

Use these when you edit a deck that already has a look to keep: duplicate the closest slide, then change its text.
For building a new deck from scratch use general/design/design_system.py instead.
"""
import copy

from pptx.oxml.ns import qn


def duplicate_slide(prs, src):
    """Append a copy of slide `src` (same layout, shapes, background, pictures) to the end of `prs`; return it.

    Move it afterwards with move_slide(). Notes are not copied.
    """
    new = prs.slides.add_slide(src.slide_layout)
    tree = new.shapes._spTree
    for el in list(tree):
        if el.tag.endswith(("}sp", "}pic", "}graphicFrame", "}grpSp", "}cxnSp")):
            tree.remove(el)
    rid_map = {}
    for rid, rel in src.part.rels.items():
        if rel.is_external or "slideLayout" in rel.reltype or "notesSlide" in rel.reltype:
            continue
        rid_map[rid] = new.part.relate_to(rel._target, rel.reltype)
    for el in src.shapes._spTree:
        if el.tag.endswith(("}nvGrpSpPr", "}grpSpPr")):
            continue
        tree.append(copy.deepcopy(el))
    src_bg = src._element.cSld.find(qn("p:bg"))
    if src_bg is not None:
        new._element.cSld.insert(0, copy.deepcopy(src_bg))
    for el in new._element.iter():
        for a in (qn("r:embed"), qn("r:link"), qn("r:id")):
            v = el.get(a)
            if v in rid_map:
                el.set(a, rid_map[v])
    return new


def move_slide(prs, slide, new_index):
    """Move `slide` to 0-based position `new_index`."""
    lst = prs.slides._sldIdLst
    ids = list(lst)
    for el in ids:
        if prs.slides.get(int(el.get("id"))) is slide:
            lst.remove(el)
            lst.insert(new_index, el)
            return
    raise ValueError("slide not in presentation")


def remove_shape(shape):
    el = shape._element
    el.getparent().remove(el)


def set_runs_text(tf, text):
    """Replace a text frame's text but keep the first run's formatting (font, size, colour)."""
    p0 = tf.paragraphs[0]
    runs = p0.runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        p0.text = text
    for p in tf.paragraphs[1:]:
        p._p.getparent().remove(p._p)
