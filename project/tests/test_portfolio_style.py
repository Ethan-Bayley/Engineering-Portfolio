"""Tests for this project's portfolio style (project/design/portfolio_style.py) and build script."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "project" / "design"))
sys.path.insert(0, str(ROOT / "project" / "outputs" / "portfolio"))
import portfolio_style as ps  # noqa: E402


def test_build_script_saves_cover_and_pages(tmp_path):
    import build_portfolio
    doc = build_portfolio.build()
    assert doc.save(tmp_path / "p.pptx") == []
    assert doc.pages[0].cover and [p.number for p in doc.pages[1:]] == [1, 2]


def test_refuses_small_text_and_a_16th_page(tmp_path):
    doc = ps.Portfolio("11143", "T")
    doc.page("Small").text(ps.Rect(60, 100, 200, 40), ["tiny"], 9)
    assert any("under 10 pt" in x for x in doc.check())
    doc = ps.Portfolio("11143", "T")
    for i in range(16):
        doc.page(f"P{i}")
    with pytest.raises(ps.DesignError):
        doc.save(tmp_path / "x.pptx")


def test_flags_full_names_and_long_titles():
    doc = ps.Portfolio("11143", "T")
    p = doc.page("Team")
    b = p.box(p.area, "Team")
    b.team(b.content, [("Ethan Bayley", "Lead", None, ""), ("Sam K.", "Build", None, "")])
    doc.page("A very long page title that cannot possibly fit in the banner")
    probs = doc.check()
    assert any("Ethan Bayley" in x for x in probs) and not any("Sam K." in x for x in probs)
    assert any("too long for the banner" in x for x in probs)


def test_colours_are_readable_on_the_page():
    for c in (ps.TEXT, ps.YELLOW, ps.MUTED, ps.PRO, ps.CON):
        assert ps.contrast(c, ps.BG) >= 4.5
    assert ps.contrast(ps.INK, ps.YELLOW) >= 4.5          # dark text on the yellow banner, pills and table header


def test_markup_runs():
    r = [(t, c) for t, c, _b in ps.runs("a **b** ++d++ ~~e~~") if t.strip()]
    assert r == [("a ", ps.TEXT), ("b", ps.YELLOW), ("d", ps.PRO), ("e", ps.CON)]
