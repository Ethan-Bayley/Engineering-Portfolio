import itertools
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "general" / "design"))
from design_system import (BOX_COLOURS, GREEN, MAIN, ORANGE, PURPLE, RED, DesignError, Doc, Rect,  # noqa: E402
                           grid_colours, heading_text, split)


def test_heading_format_is_two_digits_hyphen_caps():
    assert heading_text(3, "Research findings") == "03 - RESEARCH FINDINGS"
    assert heading_text(12, "rpm table") == "12 - RPM TABLE"


def test_split_puts_exactly_the_gap_between_parts():
    parts = split(Rect(0, 0, 100, 50), [1, 2, 1], gap=10)
    assert parts[1].x - parts[0].r == pytest.approx(10)
    assert parts[2].x - parts[1].r == pytest.approx(10)
    assert parts[-1].r == pytest.approx(100)


def test_gap_is_one_point_six_percent_of_width():
    assert Doc("brochure").fmt.G == pytest.approx(0.016 * 841.89, abs=0.01)    # A3 portrait
    assert Doc("poster").fmt.G == pytest.approx(0.016 * 841.89, abs=0.01)
    assert Doc("slides").fmt.G == pytest.approx(0.016 * 1440, abs=0.01)


def test_brochure_is_a4_landscape_with_page_numbers():
    doc = Doc("brochure")
    assert (doc.fmt.width, doc.fmt.height) == pytest.approx((841.89, 595.28))    # 297 x 210 mm
    assert doc.fmt.page_numbers and not Doc("poster").fmt.page_numbers
    assert (Doc("poster").fmt.width, Doc("poster").fmt.height) == pytest.approx((841.89, 1190.55))   # posters stay A3
    page = doc.page("Design")
    assert any(sh.name == "Page number" for sh in page.slide.shapes)


def test_cover_page_has_no_title_or_page_number_but_counts():
    doc = Doc("brochure")
    cover = doc.page("Cover", cover=True)
    assert not any(sh.name in ("Page title", "Page number") for sh in cover.slide.shapes)
    second = doc.page("Contents")
    assert second.number == 2


def test_status_cells_take_the_verdict_tint_and_flow_and_gantt_build(tmp_path):
    from design_system import ACCENT
    doc = Doc("brochure")
    p = doc.page("Evaluate")
    top, mid, bottom = p.rows(p.area, 1, 1, 1)
    box = p.box(top, "evaluation", "results")
    t = box.table(box.content, [["Criterion", "Verdict"], ["one", "PARTLY MET"], ["two", "NOT MET"], ["three", "MET"]],
                  status_col=1)
    assert str(t.cell(1, 1).fill.fore_color.rgb) == ACCENT[ORANGE]
    assert str(t.cell(2, 1).fill.fore_color.rgb) == ACCENT[RED]
    assert str(t.cell(3, 1).fill.fore_color.rgb) == ACCENT[GREEN]
    pic = str(Path(__file__).resolve().parent / "fixtures" / "sample.png")
    fl = p.box(mid, "method", "flow")
    fl.flow(fl.content, [(pic, "One", "a", "alt"), (pic, "Two", "b", "alt"), (pic, "Three", None, "alt")], cols=3)
    g = p.box(bottom, "planning", "plan")
    g.gantt(g.content, [(8, "T"), (9, "F"), (10, "S")], [("Set up", 8, 9, "good"), ("Due", 10, 10, "warn")])
    assert doc.save(tmp_path / "x.pptx") == []


def test_numbers_run_on_across_pages():
    doc = Doc("brochure")
    p1 = doc.page("Design")
    a, b = p1.cols(p1.area, 1, 1)
    p1.box(a, "research", "one")
    p1.box(b, "design", "two")
    p2 = doc.page("Prototype")
    box = p2.box(p2.area, "testing", "three")
    assert box.heading == "03 - THREE"
    assert doc.check() == []


def test_touching_box_of_same_colour_is_swapped_and_noted():
    doc = Doc("brochure")
    p = doc.page("Design")
    a, b = p.cols(p.area, 1, 1)
    p.box(a, "research", "one")
    second = p.box(b, "results", "two")       # also green by meaning, but it touches box 01
    assert second.colour != GREEN
    assert doc.notes and "touches" in doc.notes[0]
    assert doc.check() == []


def test_check_catches_same_colour_neighbours_and_uneven_gaps():
    doc = Doc("a3")
    p = doc.page("Test")
    G = doc.fmt.G
    left = Rect(p.area.x, p.area.y, 200, 200)
    p.box(left, GREEN, "one")
    p.boxes.append(p.boxes[0].__class__(p, Rect(left.r + G, left.y, 200, 200), GREEN, 2, "two"))   # forced
    p.box(Rect(left.x, left.b + 2 * G * 0.8, 200, 100), ORANGE, "three")                           # gap 1.6 G
    problems = " ".join(doc.check())
    assert "both green" in problems
    assert "not G" in problems


def test_main_colour_is_never_a_box():
    p = Doc("brochure").page("Design")
    with pytest.raises(DesignError):
        p.box(p.area, MAIN, "summary")


def test_highlight_is_box_colour_green_or_yellow_only():
    p = Doc("brochure").page("Design")
    box = p.box(p.area, "method", "code")
    for kind in ("general", "result", "caution"):
        box.highlight(box.content, "text", kind)
    with pytest.raises(DesignError):
        box.highlight(box.content, "text", kind="purple")


def test_stat_cards_avoid_the_colour_of_their_box():
    p = Doc("brochure").page("Design")
    box = p.box(p.area, "design", "numbers")          # orange
    for rows, cols in ((1, 4), (2, 2), (2, 3)):
        g = grid_colours(rows, cols, avoid=box.colour)
        assert all(c != ORANGE for row in g for c in row)
    with pytest.raises(DesignError):
        box.stats(box.content, [("1", "a"), ("2", "b")], colours=[ORANGE, GREEN])


def _card_colours(box):
    """Outline colours of the stat cards drawn in a box (rounded shapes with a tint fill and an outline)."""
    from design_system import ACCENT
    tint_to_colour = {v: k for k, v in ACCENT.items()}
    out = []
    for sh in box.page.slide.shapes:
        try:
            fill = str(sh.fill.fore_color.rgb)
        except (AttributeError, TypeError):
            continue
        if fill in tint_to_colour and sh.line.fill.type == 1 and str(sh.line.color.rgb) == tint_to_colour[fill]:
            out.append(tint_to_colour[fill])
    return out


def test_stat_cards_in_one_box_are_all_different_colours():
    for n in (2, 3, 4):
        p = Doc("brochure").page("Design")
        box = p.box(p.area, "design", "numbers")          # orange
        box.stats(box.content, [(str(i), "x") for i in range(n)])
        cards = _card_colours(box)
        assert len(cards) == n and len(set(cards)) == n   # all different
        if n <= 3:
            assert ORANGE not in cards                      # and not the box's colour
    with pytest.raises(DesignError):
        box.stats(box.content, [("1", "a"), ("2", "b")], colours=[GREEN, GREEN])


def test_table_header_is_the_box_colour():
    p = Doc("brochure").page("Design")
    box = p.box(p.area, "testing", "results")         # red
    t = box.table(box.content, [["h1", "h2"], ["a", "1"], ["b", "2"]])
    assert str(t.cell(0, 0).fill.fore_color.rgb) == RED
    assert str(t.cell(2, 0).fill.fore_color.rgb) == box.accent


def test_grid_colours_never_repeat_beside_or_below():
    for (rows, cols), avoid in itertools.product(((1, 4), (2, 2), (2, 4), (3, 3)), (None, *BOX_COLOURS)):
        g = grid_colours(rows, cols, avoid=avoid)
        for r in range(rows):
            for c in range(cols):
                assert g[r][c] in BOX_COLOURS
                if c + 1 < cols:
                    assert g[r][c] != g[r][c + 1]
                if r + 1 < rows:
                    assert g[r][c] != g[r + 1][c]


def test_every_component_builds_and_saves(tmp_path):
    doc = Doc("brochure")
    p = doc.page("Components")
    top, bottom = p.rows(p.area, 1, 1)
    a_r, b_r = p.cols(top, 1, 1)
    c_r, d_r = p.cols(bottom, 1, 1)
    a = p.box(a_r, "research", "a")
    x, y = p.rows(a.content, 1, 1)
    a.stats(x, [("3", "one"), ("4", "two")])
    a.highlight(y, "**Result** text", "result")
    b = p.box(b_r, "design", "b")
    b.subtopics(b.content, [("t", "x"), ("u", "y")], cols=2)
    c = p.box(c_r, "method", "c")
    x, y = p.rows(c.content, 1, 1)
    c.steps(x, ["one", "two"])
    c.table(y, [["h1", "h2"], ["a", "1.5"]])
    d = p.box(d_r, "testing", "d")
    x, y = p.rows(d.content, 1, 1)
    d.timeline(x, [("1/1", "Start", "notes"), ("2/1", "End", ["more"])])
    d.callout(y, "what to notice")
    assert {b.colour for b in p.boxes} == {GREEN, ORANGE, PURPLE, RED}
    out = tmp_path / "deck.pptx"
    assert doc.save(out) == []
    assert out.stat().st_size > 0


def test_section_label_is_drawn_beside_the_title():
    page = Doc("brochure").page("Problem", label="1  Significance")
    labels = [sh for sh in page.slide.shapes if sh.name == "Section label"]
    assert len(labels) == 1 and labels[0].text_frame.text == "1  SIGNIFICANCE"


def test_highlight_is_only_as_tall_as_its_text():
    p = Doc("brochure").page("Design")
    box = p.box(p.area, "method", "code")
    tall = Rect(box.content.x, box.content.y, box.content.w, 300)
    used = box.highlight(tall, "**Short.** One line.")
    assert used.h < 60 and used.y == tall.y            # fitted, at the top of the space given
    assert box.highlight(tall, "x", fit=False).h == 300


def test_stack_gives_fill_parts_what_text_and_highlights_leave():
    p = Doc("brochure").page("Design")
    box = p.box(p.area, "method", "code")
    drawn = []
    rects = box.stack(box.content, [("text", ["A short paragraph."]), ("fill", 1, drawn.append),
                                    ("highlight", "**Note.** A short highlight.")])
    gap = 0.5 * box.page.fmt.G
    assert drawn and drawn[0] == rects[1]
    assert rects[1].y == pytest.approx(rects[0].b + gap) and rects[2].y == pytest.approx(rects[1].b + gap)
    assert rects[2].b == pytest.approx(box.content.b, abs=0.5)     # the fill took exactly the rest


def test_closing_highlight_sits_at_the_bottom_when_nothing_stretches():
    p = Doc("brochure").page("Design")
    box = p.box(p.area, "method", "code")
    rects = box.stack(box.content, [("text", ["A short paragraph."]), ("highlight", "**Note.** Closing point.")])
    assert rects[0].y == pytest.approx(box.content.y)                 # text at the top
    assert rects[1].b == pytest.approx(box.content.b, abs=0.5)        # highlight at the bottom

