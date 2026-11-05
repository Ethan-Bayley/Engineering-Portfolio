import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "general" / "tools"))
import photo_prep  # noqa: E402
import template_sync  # noqa: E402


def test_photo_prep_makes_an_upright_resized_jpeg(tmp_path):
    src = tmp_path / "big.png"
    Image.new("RGB", (3000, 1500), "white").save(src)
    w, h = photo_prep.prepare(src, tmp_path / "out.jpg", longest=1600)
    assert (w, h) == (1600, 800) and (tmp_path / "out.jpg").exists()


def test_photo_prep_applies_exif_rotation(tmp_path):
    src = tmp_path / "rotated.jpg"
    im = Image.new("RGB", (400, 200), "white")
    exif = im.getexif()
    exif[0x0112] = 6                      # "rotate 90 degrees": the photo is really portrait
    im.save(src, exif=exif)
    w, h = photo_prep.prepare(src, tmp_path / "up.jpg", longest=1600)
    assert (w, h) == (200, 400)


def test_template_sync_never_touches_project_files():
    assert not any(p == "project" or p.startswith("project/") for p in template_sync.SHARED)
    assert "general" in template_sync.SHARED and ".claude/skills" in template_sync.SHARED


def test_starter_build_script_saves_a_valid_deck(tmp_path):
    sys.path.insert(0, str(ROOT / "general" / "templates"))
    import build_brochure
    doc = build_brochure.build()
    assert doc.save(tmp_path / "starter.pptx") == []
    assert len(doc.pages) == 4


def test_project_look_overrides_colours(tmp_path, monkeypatch):
    import importlib
    sys.path.insert(0, str(ROOT / "general" / "design"))
    import design_system
    fake = tmp_path / "project"
    fake.mkdir()
    (fake / "design.json").write_text(json.dumps({"main": "112233", "green": "00AA00"}), encoding="utf-8")
    monkeypatch.setattr(design_system, "ROOT", tmp_path)
    look = design_system._project_look()
    assert look["main"] == "112233" and look["green"] == "00AA00"
    importlib.reload(design_system)       # back to this repo's own look: its design.json, or the default
    real = ROOT / "project" / "design.json"
    want = json.loads(real.read_text(encoding="utf-8")).get("main", "1D497D") if real.exists() else "1D497D"
    assert design_system.MAIN == want


def test_poster_and_slides_starters_build(tmp_path):
    sys.path.insert(0, str(ROOT / "general" / "templates"))
    import build_poster
    import build_slides
    assert build_poster.build().save(tmp_path / "poster.pptx") == []
    assert build_slides.build().save(tmp_path / "slides.pptx") == []


def test_charts_are_drawn_at_the_placed_size(tmp_path):
    sys.path.insert(0, str(ROOT / "general" / "design"))
    import charts
    p = charts.bars(tmp_path / "b.png", ["A", "B", "C"], [3, 10, 1], size=(4, 1.5), unit=" ms", kept=[2], before=[1])
    with Image.open(p) as im:
        assert abs(im.width / 220 - 4) < 0.05 and abs(im.height / 220 - 1.5) < 0.05
    charts.before_after(tmp_path / "ba.png", [("Loop", 254, 104), ("Frame", 2349, 104)], size=(4, 1.6), unit=" ms")
    charts.lines(tmp_path / "l.png", [1, 2, 3], [("Grip", [1, 3, 2], "kept")], size=(3, 2), target=(2.5, "goal"))
    assert (tmp_path / "ba.png").exists() and (tmp_path / "l.png").exists()


def test_mind_map_and_labelled_picture(tmp_path):
    sys.path.insert(0, str(ROOT / "general" / "design"))
    from design_system import Doc
    doc = Doc("brochure")
    p = doc.page("Ideas")
    l, r = p.cols(p.area, 1, 1)
    a = p.box(l, "research", "Mind map")
    a.mind_map(a.content, "Idea", [("Cost", ["cheap"]), ("Speed", ["fast"]), ("Size", ["small"])])
    b = p.box(r, "design", "The build")
    b.labelled(b.content, ROOT / "tests" / "fixtures" / "sample.png", "A test picture", caption="Caption",
               labels=[(0.5, 0.5, "centre", 0.2, 0.2)])
    assert doc.save(tmp_path / "m.pptx") == []


def test_photo_prep_reads_the_date_taken(tmp_path):
    src = tmp_path / "dated.jpg"
    im = Image.new("RGB", (100, 80), "white")
    exif = im.getexif()
    exif[0x0132] = "2026:03:14 09:26:00"
    im.save(src, exif=exif)
    assert photo_prep.taken(src) == ("2026-03-14 09:26", "exif")
    plain = tmp_path / "plain.png"
    Image.new("RGB", (10, 10)).save(plain)
    assert photo_prep.taken(plain)[1] == "file"


def test_hand_in_check_finds_placeholders_and_page_limit(tmp_path):
    import datetime
    import hand_in_check
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz
    pdf = tmp_path / "x_v01.pdf"
    doc = fitz.open()
    for _ in range(3):
        doc.new_page(width=841.9, height=595.3).insert_text((72, 72), "Results: <number and unit>  TODO", fontsize=10)
    doc.save(pdf)
    res = dict((msg.split(":")[0].split(" (")[0], lvl) for lvl, msg in hand_in_check.check(pdf, max_pages=2))
    assert res["3 pages"] == "FAIL" and res["placeholder text"] == "FAIL"
    assert res["page size"] == "PASS"
    due = hand_in_check.deadline(tmp_path / "missing.md")
    assert due is None
    md = tmp_path / "P.md"
    md.write_text("- Deadline: 2026-11-20 15:30, PDF to Canvas\n", encoding="utf-8")
    assert hand_in_check.deadline(md) == datetime.datetime(2026, 11, 20, 15, 30)


def test_schedule_compares_plan_with_commit_dates(tmp_path):
    import datetime as dt
    import os
    import subprocess
    import schedule
    repo = tmp_path / "r"
    repo.mkdir()
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")

    def commit(path, date, msg):
        (repo / path).parent.mkdir(parents=True, exist_ok=True)
        (repo / path).write_text(msg)
        subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True, env=env)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm", msg, "--date", f"{date}T12:00:00"], check=True,
                       env=dict(env, GIT_COMMITTER_DATE=f"{date}T12:00:00"))
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    commit("src/a.py", "2026-03-02", "start code")
    commit("src/b.py", "2026-03-12", "more code")
    commit("notes.md", "2026-03-04", "Research notes")
    plan = tmp_path / "SCHEDULE.md"
    plan.write_text("| Task | Planned start | Planned end | Evidence |\n|---|---|---|---|\n"
                    "| Code | 2026-03-01 | 2026-03-10 | src/ |\n| Research | 2026-03-01 | 2026-03-05 | msg:research |\n"
                    "| Test | 2026-03-20 | 2026-03-25 | tests/ |\n", encoding="utf-8")
    rows = schedule.compare(schedule.read_plan(plan), repo, today=dt.date(2026, 3, 15))
    assert rows[0][3:] == (dt.date(2026, 3, 2), dt.date(2026, 3, 12), 2, "last commit 2 days after the planned end")
    assert rows[1][5:] == (1, "last commit 1 day before the planned end")
    assert rows[2][6] == "not started"
    days, tasks = schedule.week_columns(rows)
    assert days[0] == ("23/02", "wk") and ("Code (actual)", "02/03", "09/03", "warn") in tasks


def test_screen_grab_crop_and_trim():
    import screen_grab
    assert screen_grab.crop_box((100, 50, 1100, 850), frac=(0.1, 0.25, 0.9, 1.0)) == (200, 250, 1000, 850)
    assert screen_grab.crop_box((100, 50, 1100, 850), px=(10, 20, 30, 40)) == (110, 70, 1070, 810)
    im = Image.new("RGB", (400, 300), (240, 240, 245))
    im.paste((40, 60, 90), (150, 100, 250, 180))          # the "model"
    out = screen_grab.trim(im, margin=10)
    assert out.size == (120, 100)
