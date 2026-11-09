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
    n = len(doc.pages) - 1
    assert doc.pages[0].cover and [p.number for p in doc.pages[1:]] == list(range(1, n + 1)) and n <= 15


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
    for c in (ps.TEXT, ps.KEY, ps.MUTED, ps.PRO, ps.CON):
        assert ps.contrast(c, ps.BG) >= 4.5
    assert ps.contrast(ps.INK, ps.YELLOW) >= 4.5          # dark text on the yellow banner, pills and table header


def test_markup_runs():
    r = [(t, c) for t, c, _b in ps.runs("a **b** ++d++ ~~e~~") if t.strip()]
    assert r == [("a ", ps.TEXT), ("b", ps.KEY), ("d", ps.PRO), ("e", ps.CON)]


@pytest.mark.parametrize("theme", ["dark", "paper", "band"])
def test_every_theme_is_readable(theme):
    t = ps._THEMES[theme]
    for k in ("TEXT", "KEY", "MUTED", "PRO", "CON"):
        assert ps.contrast(t[k], t["BG"]) >= 4.5, k        # body text and labels on the page
    assert ps.contrast(t["FILL_TEXT"], t["FILL"]) >= 4.5   # text on banners, pills and table headers
    assert ps.contrast(t["LINE"], t["BG"]) >= 3            # box outlines and table rules


def test_other_themes_still_build(tmp_path):
    import subprocess
    env = {**__import__("os").environ, "PORTFOLIO_THEME": "dark"}
    script = ROOT / "project" / "outputs" / "portfolio" / "build_portfolio.py"
    r = subprocess.run([sys.executable, str(script), "--draft", str(tmp_path / "p.pptx")], env=env, capture_output=True,
                       text=True)
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "p.pptx").exists()


def test_lines_have_no_theme_shadow():
    import build_portfolio
    from pptx.oxml.ns import qn
    doc = build_portfolio.build()
    lines = [sh for slide in doc.prs.slides for sh in slide.shapes if sh._element.tag == qn("p:cxnSp")]
    assert lines and all(sh._element.spPr.find(qn("a:effectLst")) is not None for sh in lines)
