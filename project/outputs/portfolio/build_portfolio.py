"""Build the FTC portfolio for 11143 Barker Yellowbacks (2026-27, BIOBUZZ): the cover plus up to 15 pages.

    python project/outputs/portfolio/build_portfolio.py "what changed"      # saves portfolio_vNN.pptx
    python project/outputs/portfolio/build_portfolio.py --draft x.pptx
    python general/tools/export_pdf.py project/outputs/portfolio/portfolio_vNN.pptx --render project/outputs/renders/vNN
    python general/tools/hand_in_check.py --deliverable portfolio --max-pages 16 --max-mb 15 --min-pt 10

Look: project/design/PORTFOLIO_STYLE.md (the team's cover, colours tightened). FTC A201: cover (team number; not
judged) + at most 15 pages, nothing under 10 pt, first names and last initials only, work since 1 January 2026.
Text drafted from the team's logs, meeting notes and answers (project/logs/, NEXT_STEPS.md, QUESTIONS.md) and the code report (Pinkbacks branch
Isaac, doc/isaac-integration.md); AI credit endnote on page 15 (A201). Anything not measured on the robot is a
<RESULT: ...> or <...> placeholder, which the hand-in check fails on until the team fills it. Drawings: the team's
own, recoloured, in assets/cad/linework_page/. Page plan: project/brief/PAGE_PLAN.md.
"""
import sys
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "general" / "design").is_dir())
sys.path.insert(0, str(ROOT / "project" / "design"))
from portfolio_style import (FILL, FILL_TEXT, G, MUTED, THEME, Portfolio, Rect, bar, polygon, pill,  # noqa: E402
                             pill_width, stripes, width, write)
from design_system import _picture, _shape  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402

A = ROOT / "project" / "assets"
# team's line drawings recoloured to the page: white lines on dark, or dark lines on a light theme
LW = A / "cad" / ("linework_page" if THEME == "dark" else "linework_light")
ROBOT_A = LW / "robot" / "robot_iso.png"             # replaces the low-res cover crops (2026-11-05)
ROBOT_B = LW / "robot" / "robot_side.png"
DELIVERABLE = "portfolio"
NAME = DELIVERABLE if THEME == "paper" else f"portfolio_{THEME}"    # PORTFOLIO_THEME=dark|band saves its own versions
TEAM, TEAM_NAME = "11143", "Barker Yellowbacks"


def trimmed(path):
    """A copy of a see-through drawing cut to what is drawn (no empty margin), so it can be placed larger.
    Saved beside the original as <name>_trim.png and remade when the original is newer."""
    from PIL import Image
    out = path.with_name(path.stem + "_trim.png")
    if not out.exists() or out.stat().st_mtime < path.stat().st_mtime:
        im = Image.open(path)
        box = im.split()[3].getbbox() if im.mode == "RGBA" else im.getbbox()
        im.crop(box).save(out, optimize=True)
    return out


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
    write(s, Rect(a.x, by + 4, bw, bh - 8), [{"text": "ENGINEERING", "size": 24, "bold": True, "colour": FILL_TEXT, "after": 0},
                                              {"text": "PORTFOLIO", "size": 24, "bold": True, "colour": FILL_TEXT,
                                               "after": 0}],
          anchor=MSO_ANCHOR.MIDDLE, sizes=p.sizes)
    stripes(s, 14 + bw + 1.2 * G, by + bh + 0.6 * G, 22, n=5)
    # pill and team name
    py = by + bh + 4.4 * G
    text = "FTC - FIRST Tech Challenge"
    pill(s, Rect(a.x, py, pill_width(text, 11), 22), text, 11, filled=False, sizes=p.sizes)
    if THEME == "dark":
        write(s, Rect(a.x, py + 30, a.w, 40), ["BARKER **YELLOWBACKS**"], 30, bold=True, sizes=p.sizes)
    else:                                       # yellow text cannot be read on a light page: the name sits in a band
        w0 = width("BARKER ", 30, True)
        _shape(s, MSO_SHAPE.RECTANGLE, Rect(a.x + w0 - 5, py + 30, width("YELLOWBACKS", 30, True) + 10, 40), FILL)
        write(s, Rect(a.x, py + 30, w0, 40), ["BARKER"], 30, bold=True, anchor=MSO_ANCHOR.MIDDLE, sizes=p.sizes)
        write(s, Rect(a.x + w0, py + 30, a.w - w0, 40), [{"text": "YELLOWBACKS", "colour": FILL_TEXT}], 30, bold=True,
              anchor=MSO_ANCHOR.MIDDLE, sizes=p.sizes)
    # robot line art, team number box on the right
    ry = py + 80
    rh = 330                                   # down to just above the bottom drawing (user, 2026-11-10: fill the space)
    nb = Rect(a.r - 64, ry, 64, rh)
    _shape(s, MSO_SHAPE.RECTANGLE, nb, None, MUTED, 2)
    write(s, Rect(nb.x + nb.w / 2 - nb.h / 2, nb.y + nb.h / 2 - nb.w / 2, nb.h, nb.w),
          [{"text": TEAM, "size": 54, "bold": True, "colour": MUTED, "align": PP_ALIGN.CENTER, "after": 0}],
          anchor=MSO_ANCHOR.MIDDLE, rotation=90, sizes=p.sizes)
    bar(s, nb.x - 0.8 * G - 5, nb.y + 0.15 * nb.h, nb.h * 0.7, 5)
    _picture(s, trimmed(ROBOT_A), Rect(a.x, ry, nb.x - a.x - 2 * G, rh), "Line drawing of our robot", "left")
    # season block bottom-left, second drawing bottom-right
    yb = a.b - 150
    bar(s, a.x, yb + 0.6 * G, 92, 4)
    write(s, Rect(a.x + 1.4 * G, yb - 20, 200, 135), [{"text": "2026-2027", "size": 22, "bold": True, "after": 2},
                                                  {"text": "Sydney", "size": 20, "after": 0},
                                                  {"text": "Australia", "size": 20, "after": 4},
                                                  {"text": "Barker College", "size": 11, "colour": MUTED, "after": 0},
                                                  {"text": "Supported by Barker Robotics", "size": 11, "colour": MUTED,
                                                   "after": 0}], sizes=p.sizes)
    _picture(s, ROBOT_B, Rect(a.x + 0.35 * a.w, a.b - 245, 0.65 * a.w, 245), "Second line drawing of our robot",
             "right")
    return p


ENDNOTE = ("Endnote: we drafted and laid out this portfolio with help from an AI assistant. All results, photos, "
           "CAD, code and decisions are our own, and we checked every page.")
SW, SH, OD, TU, TR, RB = (LW / k for k in ("swerve", "shooter", "odometry", "turret", "transition", "robot"))
PHOTOS = A / "photos" / "ready"                    # team photos, prepared with general/tools/photo_prep.py
SHL = A / "cad" / "linework_light" / "shooter" / "shooter_exploded_iso_lines.png"   # user's own line drawing, 2026-11-11
SHOTS = A / "cad" / "screenshots_page" / "shooter"     # shaded Onshape views with the background taken out


# ---------------------------------------------------------------- helpers
def stats(p, r, items):
    """A row of filled tiles: [(big number or word, what it means)]. Only numbers and words the team has given."""
    for c, (num, label) in zip(p.cols(r, *[1] * len(items)), items):
        _shape(p.slide, MSO_SHAPE.RECTANGLE, c, FILL, None, 0)
        write(p.slide, c.inset(0.4 * G, 0.2 * G), [
            {"text": num, "size": 16, "bold": True, "colour": FILL_TEXT, "align": PP_ALIGN.CENTER, "after": 1},
            {"text": label, "size": 10, "colour": FILL_TEXT, "align": PP_ALIGN.CENTER, "after": 0}],
            anchor=MSO_ANCHOR.MIDDLE, sizes=p.sizes)


# ---------------------------------------------------------------- 1-5: team, season, outreach, process, strategy
def p01_team(doc):
    p = doc.page("Meet the team")
    top, bottom = p.rows(p.area, 1.45, 1)
    members = [("Ethan B.", "Lead design", "assembly"), ("Brandon L.", "CAD", "assembly"),
               ("Isaac H.", "Lead code", "CAD, assembly"), ("Ryan T.", "Driver", "CAD"),
               ("Will Q.", "Lead strategy", "drive coach"), ("Ivy W.", "Programming", "HR"),
               ("Tina X.", "Programming", "assembly, strategy"), ("Chelsey W.", "Assembly", "scouting"),
               ("Chloe L.", "Electrical", "assembly"), ("Chloe S.", "Strategy", "code, assembly"),
               ("Jemima C.", "Programming", "scouting"),
               ("Lucas T.", "CAD", "assembly")]
    t = p.box(top, "12 members")
    t.team(t.content, [(n, r, None, note) for n, r, note in members], cols=3)
    l, r = p.cols(bottom, 1.1, 1)
    h = p.box(l, "How we split the work")
    h.text(h.content, [
        "- **CAD:** four of us worked on the CAD, mostly at the start of the season. Once the design was done we "
        "joined assembly so the build went faster",
        "- **Code:** five of us wrote the basic structure of the code and our simulator. We were ready to test "
        "as soon as the robot was finished, and we kept the work moving steadily",
        "- **Strategy:** three of us planned our strategy. We worked together on autonomous routes that suit our "
        "robot and the alliances we are likely to play with. Four of us scout",
        "- **Assembly:** eight of us assembled the manufactured parts with the design team once the CAD was done"])
    w = p.box(r, "How we work")
    w.text(w.content, [
        "- We meet **every week**",
        "- **Subteam meetings:** each subteam shares updates from its areas. The programmers cover the shooter, "
        "the swerve and the ball transfer in turn",
        "- **Whole-team meetings:** we share the changes and progress that affect everyone. When the design team "
        "removed the turret, we had to tell the programmers",
        "- Whole-team meetings also keep us on schedule so deadlines do not slip",
        "- Each subteam decides its own area, then tells everyone else"])


def p02_season(doc):
    p = doc.page("Our season")
    top, plan, bottom = p.rows(p.area, 1.05, 1.32, 0.98)
    tl = p.box(top, "2026-2027 season timeline")
    r1, r2 = p.rows(tl.content, 1, 1)
    tl.timeline(r1, [("15 Sep", "Schedule", "everyone adds free times"),
                     ("18 Sep", "First meeting", "subteams chosen"),
                     ("10 Oct", "Refocus", "turret cut"),
                     ("26 Oct-1 Nov", "Swerve built", "goBILDA parts arrive"),
                     ("12 Nov", "Wollongong", "first event")])
    a, b = p.cols(r2, 3, 1.15)
    tl.timeline(a, [("28 Nov", "Macquarie", "second event"),
                    ("4-5 Dec", "Macquarie", "national competition"),
                    ("28 Apr-1 May", "Worlds", "FTC World Championship")], dashed=True)
    tl.text(b, [{"text": "Dotted line: events after Wollongong that we are planning for.", "size": 10,
                 "colour": MUTED}])
    pv = p.box(plan, "Planned on 10 October vs what happened", accent=True)
    pv.stack(pv.content, [
        ("text", ["Our first team meeting was on 18 September. We chose our subteams and roles and began designing "
                  "and programming. On 10 October we held a major meeting to refocus our timeline so the robot would "
                  "be finished in time. We cut the turret (page 9) and planned each week:"]),
        ("fill", 1, lambda rr: pv.table(rr, [
            ["Week", "Planned", "What happened"],
            ["12-18 Oct", "finish the CAD; make the custom swerve parts",
             "goBILDA parts ordered; shooter redesigned and simplified; intake and transfer design done; ball "
             "tracking for autos started; hood and shooter code started"],
            ["19-25 Oct", "goBILDA parts may arrive; make the shooter and transition; assembly",
             "parts machined; assembly began"],
            ["26 Oct-1 Nov", "wiring, programming, fixing mechanical issues", "goBILDA parts arrived; swerve assembled"],
            ["2-8 Nov", "programming and drive practice", "<what happened>"]], col_weights=[0.8, 1.7, 2.3]))])
    l, r = p.cols(bottom, 1.55, 1)
    sc = p.box(l, "How we schedule")
    sc.stack(sc.content, [
        ("fill", 1, lambda rr: sc.picture(rr, A / "screenshots" / "scheduling_page.png",
                                          "Our shared availability spreadsheet: who is free in each time slot, "
                                          "subteams and weekly meetings",
                                          "Our availability spreadsheet (part)")),
        ("text", ["A shared spreadsheet shows who is free each week and what work they are given. It mostly worked, "
                  "but an exam block and outreach made it hard to judge what each week could really fit."])])
    b2 = p.box(r, "Our season goals")
    b2.text(b2.content, ["- Win the national competition",
                         "- Qualify for the FTC World Championship",
                         "- <other season goals>"])


def p03_outreach(doc):
    p = doc.page("Outreach")
    top, a_r, mid, bottom = p.rows(p.area, 0.34, 1.2, 1.78, 0.62)
    stats(p, top, [("6", "of us teach Darkinjung students"), ("Fortnightly", "since February 2026"),
                   ("1,500+", "people at Round Square"), ("32", "countries at Round Square")])
    a = p.box(a_r, "Teaching Darkinjung students", accent=True)
    a.story(a.content, [("What", "Six of us (Ethan B., Brandon L., Chloe S., Ivy W., Ryan T. and Will Q.) teach "
                                 "robotics to Darkinjung students **once a fortnight**, since February 2026."),
                        ("What they learn", "They built robots for this year's **VEX IQ** game and learnt how to "
                                            "build, how to code, how to do interviews and how to write portfolios."),
                        ("Impact", "Some of the students were in competitive teams and won **Skills**, "
                                   "**Teamwork Champion** and **Excellence** awards.")])
    d = p.box(mid, "Round Square International Conference")
    ds, dp = p.cols(d.content, 1.15, 1)
    d.picture(dp, PHOTOS / "round_square_rsic_2026.jpg",
              "Photo from above of our robotics showcase at the Round Square conference: fields, robots and visitors",
              "Our robotics showcase at Round Square")
    d.story(ds, [("What", "In the Term 2-3 holidays eight of us (Ivy W., Ethan B., Ryan T., Chelsey W., Chloe L., "
                          "Isaac H., Tina X. and Will Q.) ran the robotics part of the conference at Barker."),
                 ("Demos", "At the opening fair we showed robots driving, shooting, intaking and scoring."),
                 ("Reach", "**Over 1,500 people** from **32 countries** came. Many of them had not heard of FIRST "
                           "before."),
                 ("For us", "It was a very rewarding experience, and it was great to see so many people there.")])
    l, r = p.cols(bottom, 1, 1)
    b = p.box(l, "Mentoring a VEX team")
    b.text(b.content, ["Three of us (Ethan B., Isaac H. and Brandon L.) mentor the Darkinjung VEX team "
                       "<team name>. It is very rewarding to watch the students flourish in their games and "
                       "competitions."])
    c = p.box(r, "Barker VEX competition")
    c.text(c.content, ["On **14 November 2026** Ethan B., Isaac H. and Brandon L. will referee, queue teams and "
                       "help the competition run smoothly."])


def p04_process(doc):
    p = doc.page("How we design")
    top, mid, bottom = p.rows(p.area, 0.42, 1.2, 0.95)
    c = p.box(top, "Our design loop")
    c.timeline(c.content, [("1", "Goals", "what the game needs"), ("2", "Sketch + CAD", "Onshape layouts"),
                           ("3", "Simulate", "same code, desktop sim"), ("4", "Build", "parts and assembly"),
                           ("5", "Test + change", "back to step 2")])
    s = p.box(mid, "Our CAD process, shown on the transition")
    a, b, c3 = p.cols(s.content, 1, 1, 1)
    s.labelled(a, TR / "transition_ball_path_sketch_dimensions.png",
               "Dimensioned layout sketch of the pollen path through the transition",
               labels=[(0.12, 0.8, "pollen", 0.5, 0.96)],
               caption="1. We sketch the layout first, with the pollen and roller sizes")
    s.labelled(b, TR / "transition_side_ball_path_highlight.png",
               "Side view of the transition built from that sketch, with the pollen path highlighted",
               labels=[(0.1, 0.55, "rollers", 0.1, 0.02), (0.38, 0.38, "gecko wheels", 0.55, 0.02)],
               caption="2. We design the plates and belts around the sketch")
    s.picture(c3, TR / "transition_iso.png", "Line drawing of the complete intake and transition assembly",
              "3. We assemble the whole transition in CAD")
    l, r = p.cols(bottom, 1, 1)
    m = p.box(l, "Coding together")
    m.text(m.content, ["We each code one subsystem on its own branch, so we do not overwrite each other's work. "
                       "Tina X. wrote the intake and Jemima C. wrote the shooter. On **25 October** we merged "
                       "everything into one robot, which showed us some problems:",
                       "- Two branches each hid the other's subsystem",
                       "- We were mixing units (RPM, ticks, degrees), so every value now has one unit",
                       "- The other fixes are on page 12"])
    v = p.box(r, "Ideas from VEX and last season")
    v.text(v.content, ["Four of us (Ethan B., Will Q., Ryan T. and Tina X.) competed in VEX **Push Back**. The match "
                       "loaders in that game worked well for getting pollen out of the flower, so we used the same "
                       "idea (page 10).",
                       "Swerve and logging carried over from last season."])


def p05_strategy(doc):
    p = doc.page("Game and strategy")
    top, how, mid, tab, bottom = p.rows(p.area, 0.62, 0.3, 0.5, 1.25, 0.3)
    g = p.box(top, "What scores points (manual, Table 10-2)")
    g.table(g.content, [["Scoring action", "Points", "Our answer"],
                        ["HIVE TIP, by launching into the upward cell", "20 in auto and 20 in teleop",
                         "shooter, hood and auto-aim"],
                        ["Pollen left in an upward cell at the end", "2 each", "the same launches"]],
            col_weights=[1.6, 1.1, 1.2])
    h = p.box(how, "How we play")
    h.text(h.content, ["<our scoring plan: what we score first, where we shoot from, our role with the alliance "
                       "partner>"])
    c = p.box(mid, "One scoring cycle")
    c.timeline(c.content, [("1", "Collect", "until we hold 4"), ("2", "Hold aim", "robot turns to the goal"),
                           ("3", "Spin up", "flywheels and hood reach target"), ("4", "Settle", "ready for 0.1 s"),
                           ("5", "Feed", "pollen goes to the shooter")])
    r = p.box(tab, "Requirements, and how the robot meets each", accent=True)
    rt, rn = p.rows(r.content, 3.6, 0.7)
    r.text(rn, [r.head("How well it worked"),
                "<a few sentences on how well each answer worked on the robot>"])
    r.table(rt, [["We need to", "Why", "Our answer"],
                 ["Launch from anywhere", "fewer trips across the field", "moving hood"],
                 ["Launch quickly and often", "less waiting between shots", "two flywheels"],
                 ["Launch without turning round", "pollen collects along the wall", "rear-facing shooter"],
                 ["Aim while driving", "save time every cycle", "swerve and auto-aim"],
                 ["Hold our spot", "defence will push us", "swerve X-lock"],
                 ["Avoid defence", "defenders will chase us", "very small frame perimeter"],
                 ["Stop opponents shooting", "fewer points for them", "blocker"],
                 ["Empty the flower", "pollen sits inside it", "flower mechanism"],
                 ["Find pollen and the goal", "drive and aim without guessing", "front and rear cameras"]],
            col_weights=[1.25, 1.35, 1.25])
    s = p.box(bottom, "Scouting")
    s.text(s.content, ["Jemima C., Chelsey W., Chloe L. and Tina X. scout. <what we record and how it changes our "
                       "plan>"])


# ---------------------------------------------------------------- 6-10: the robot
def p06_robot(doc):
    p = doc.page("Robot overview")
    top, mid, bottom = p.rows(p.area, 1.15, 0.85, 0.72)
    o = p.box(top, "Our robot")
    o.labelled(o.content.inset(2.5 * G, 0.2 * G), RB / "robot_iso.png", "Line drawing of the whole robot",
               labels=[(0.55, 0.12, "shooter", 0.85, 0.0), (0.86, 0.5, "swerve pod", 0.93, 0.3),
                       (0.14, 0.6, "intake", 0.02, 0.3), (0.45, 0.45, "transition", 0.25, 1.0)])
    l, r = p.cols(mid, 1, 1.05)
    s = p.box(l, "Pollen path")
    s.labelled(s.content, RB / "robot_side_section_ball_path.png", "Side section of the robot showing the pollen path",
               labels=[(0.16, 0.62, "in", 0.04, 0.3), (0.4, 0.55, "up", 0.62, 0.9), (0.65, 0.25, "out", 0.92, 0.1)],
               caption="In at the front, up the transition, out of the rear shooter")
    k = p.box(r, "Design choices", accent=True)
    k.text(k.content, ["- A **very small frame perimeter**, so defence is easier to avoid",
                       "- **Swerve drive:** we move in any direction and can lock the wheels in an X",
                       "- A **rear-facing shooter**, so we can launch straight after collecting along the wall",
                       "- A **light robot**, so it moves more efficiently"])
    c = p.box(bottom, "Chassis")
    l, r = p.cols(c.content, 1.1, 1)
    c.picture(l, LW / "chassis" / "chassis_exploded_iso.png", "Exploded line drawing of the chassis and swerve pods",
              "Exploded view: pods, plates and side panels")
    c.picture(r, LW / "chassis" / "chassis_bottom.png", "Line drawing of the underside of the chassis",
              "Underneath: a pod in each corner")


def p07_swerve(doc):
    p = doc.page("Swerve drivetrain")
    top, mid, bottom = p.rows(p.area, 1.3, 1.1, 0.4)
    l, r = p.cols(top, 1.1, 1)
    d = p.box(l, "One swerve pod")
    d.labelled(d.content.inset(2.2 * G, 0.6 * G), SW / "swerve_pod_exploded_iso_a.png",
               "Exploded line drawing of one swerve pod",
               labels=[(0.46, 0.1, "angle sensor", 0.0, 0.06), (0.5, 0.33, "steering gears", 0.98, 0.22),
                       (0.62, 0.53, "frame plates", 1.0, 0.44), (0.22, 0.68, "drive motor", -0.03, 0.55),
                       (0.62, 0.82, "bevel gear", 1.03, 0.7), (0.47, 0.86, "wheel", 0.02, 0.97)])
    k = p.box(r, "Why swerve", accent=True)
    k.text(k.content, [
        "- **X-lock:** we can place the wheels in an X. The friction makes us much harder to push, which helps "
        "against defence",
        "- We move more efficiently, which is a big advantage in a match",
        "- Full-grip wheels give more speed and pushing power than mecanum",
        "- We can drive in one direction while facing the goal",
        "- We built swerve last season, so we already knew it",
        k.head("Our pods"),
        "- Each pod has a drive motor and a steering servo",
        "- We designed and machined custom parts for the pods",
        "- Every pod has an **absolute angle sensor**, so each wheel knows where it points from the start"])
    l, r = p.cols(mid, 1, 1)
    a = p.box(l, "Wheel drive")
    a.labelled(a.content.inset(1.5 * G, 0), SW / "swerve_geartrain_wheel_drive_iso_highlight.png",
               "Gear train that drives the wheel, highlighted",
               labels=[(0.15, 0.42, "drive motor", 0.08, 0.12), (0.58, 0.28, "gears", 0.92, 0.06),
                       (0.43, 0.8, "bevel gears", 0.1, 0.97), (0.82, 0.78, "wheel", 1.0, 0.95)],
               caption="Motor, gears, then a bevel gear turn the wheel")
    b = p.box(r, "Module rotation")
    b.labelled(b.content.inset(1.5 * G, 0), SW / "swerve_geartrain_module_rotation_iso_highlight.png",
               "Gear train that turns the pod, highlighted",
               labels=[(0.28, 0.42, "ring gear", 0.02, 0.08), (0.76, 0.26, "steering gears", 0.9, 0.04),
                       (0.17, 0.66, "wheel fork", 0.04, 0.9), (0.55, 0.88, "wheel", 0.98, 0.9)],
               caption="A servo and a ring gear turn the whole pod")
    t = p.box(bottom, "Tests")
    t.table(t.content, [["Test", "Result", "Status"], ["Top speed", "not finished yet", "NOT TESTED"],
                        ["Pushed by another robot in X-lock", "not finished yet", "NOT TESTED"]],
            col_weights=[1.6, 1.2, 1], status_col=2)


def p08_intake(doc):
    p = doc.page("Intake and transition")
    top, mid, bottom = p.rows(p.area, 1.5, 1.0, 0.4)
    l, r = p.cols(top, 1.25, 1)
    d = p.box(l, "Pollen path")
    d.labelled(d.content.inset(0.5 * G, 1.2 * G), TR / "transition_side_ball_path_highlight.png",
               "Side view of the transition with the pollen path highlighted",
               labels=[(0.1, 0.55, "mecanum rollers", 0.15, 0.0), (0.38, 0.38, "gecko wheels", 0.6, 0.0),
                       (0.55, 0.78, "pollen guide", 0.82, 0.86)],
               caption="Rollers pull pollen in and gecko wheels lift it to the shooter")
    k = p.box(r, "How it works", accent=True)
    k.text(k.content, ["- Mecanum rollers at the front pull pollen in",
                       "- Gecko wheels in the transition grip the pollen and carry it up",
                       "- Smaller gecko wheels at the top reduce **backspin** going into the shooter",
                       "- **Polycarbonate ramps** give the pollen a low-friction surface",
                       "- Two motors drive the intake and the transition",
                       "- **4 beam sensors** count the pollen we hold, up to the 4 that rule G407 allows. The "
                       "intake stops when we are full"])
    a = p.box(mid, "Assembly")
    l2, r2 = p.cols(a.content, 1, 1)
    a.picture(l2, TR / "transition_iso.png", "Line drawing of the intake and transition assembly",
              "The intake and transition together")
    a.picture(r2, TR / "transition_front.png", "Front line drawing of the intake and transition",
              "From the front")
    t = p.box(bottom, "Tests")
    t.table(t.content, [["Test", "Result", "Status"], ["Jams per 20 pickups", "not finished yet", "NOT TESTED"]],
            col_weights=[1.6, 1.2, 1], status_col=2)


def p09_shooter(doc):
    p = doc.page("Shooter design")
    top, mid, bottom = p.rows(p.area, 0.82, 1.28, 0.37)
    it = p.box(top, "What we tried")
    it.iterations(it.content, [
        ("Turret, last season", None, "", ["aims without turning the robot"], ["months of tuning (Apr-Jun 2026)"]),
        ("Turret, this season", TU / "turret_iso_rotation_highlight.png",
         "Line drawing of this season's turret design with the turntable highlighted", ["what we wanted first"],
         ["weight and space", "goBILDA parts delayed", "no time: regionals 4 weeks away"]),
        ("Fixed rear shooter", SH / "shooter_iso_rear_a.png", "Line drawing of our fixed rear shooter design",
         ["fewer parts", "shoots out of the flowers without turning"], ["the whole robot must turn to aim"])])
    l, r = p.cols(mid, 1, 1.12)
    w = p.box(l, "What we wanted, and why", accent=True)
    w.text(w.content, [
        "- **Two flywheels,** so there is less waiting between shots",
        "- **A moving hood,** so we can shoot from anywhere on the field. It moves from 33.6 to 67 degrees",
        "- **A shooter that faces backwards.** Pollen collects along the wall, so we can drive up to the wall and "
        "aim without turning round first",
        "- **A lookup table** that gives the flywheel speed and hood angle for where localisation says we are. We "
        "will measure its values once the robot is finished",
        w.head("Why we cut the turret"),
        "At our meeting on 10 October we decided to cut the turret. Regionals were four weeks away and our goBILDA "
        "parts were delayed, so we needed to save time. The turret was the least necessary part. We kept swerve and "
        "the blocker, which still speed up shooting, and spent the time making the intake, transfer, swerve, autos "
        "and code consistent. The swerve base now turns the robot to aim (page 13)."])
    a, b = p.rows(r, 1, 1.25)
    d = p.box(a, "Hood drive")
    d.labelled(d.content.inset(0.5 * G, 0.8 * G), SH / "shooter_side_hood_drive_highlight.png",
               "Side line drawing of the shooter with the hood drive highlighted",
               labels=[(0.6, 0.42, "hood rack", 0.42, 0.0), (0.72, 0.3, "servo gear", 0.9, 0.0),
                       (0.1, 0.3, "flywheel", 0.1, 0.0)],
               caption="A servo gear drives a rack to tilt the hood")
    e = p.box(b, "Exploded view")
    e.labelled(e.content, SHL, "Exploded line drawing of the fixed shooter",
               labels=[(0.47, 0.66, "flywheel", 0.08, 0.9), (0.5, 0.3, "hood", 0.12, 0.08),
                       (0.62, 0.14, "motor", 0.92, 0.04)])
    t = p.box(bottom, "Tests")
    t.table(t.content, [["Test", "Result", "Status"], ["Shots in from 3 distances", "not finished yet", "NOT TESTED"],
                        ["Time between shots", "not finished yet", "NOT TESTED"]], col_weights=[1.6, 1.2, 1], status_col=2)


def p10_loader(doc):
    p = doc.page("Flower, blocker, cameras")
    top, mid, bottom = p.rows(p.area, 0.92, 0.95, 0.82)
    l, r = p.cols(top, 1, 1)
    m = p.box(l, "Flower mechanism", accent=True)
    m.story(m.content, [("Idea", "Four of us competed in VEX **Push Back**. The match loaders in that game worked well "
                                 "for getting pollen out of a container, so we used the same idea for the flower."),
                        ("Problem", "Pollen sits inside the flower and we need to get it out."),
                        ("Result", "Not tested yet: the robot is not finished.")])
    b = p.box(r, "Blocker and gate")
    b.story(b.content, [("Blocker", "The blocker stops opponents from shooting (1 Axon Max servo)."),
                        ("Gate", "The gate stops pollen going into the shooter until the shot is ready (1 Axon "
                                 "servo).")])
    c = p.box(mid, "Two cameras")
    l2, r2 = p.cols(c.content, 1.5, 1)
    c.labelled(l2, TR / "transition_side_cameras_highlight.png", "Side view with the two cameras highlighted",
               labels=[(0.05, 0.12, "front camera", 0.2, -0.02), (0.88, 0.12, "rear camera", 0.78, -0.02)])
    c.text(r2, ["- The **front camera** finds pollen so we can drive a path to it",
                "- The **rear camera** reads AprilTags so we know where the goal is",
                "- Status: not tested yet (robot not finished)"])
    h = p.box(bottom, "How we hold and release pollen")
    l3, r3 = p.cols(h.content, 1, 1.15)
    h.picture(l3, TR / "transition_front.png", "Front line drawing of the intake and transition")
    h.text(r3, ["- **Collect:** the intake runs until the 4 beam sensors say we are full, then it stops",
                "- **Hold:** pollen waits while the robot aims",
                "- **Release:** pollen only feeds once aim, flywheel speed and hood have all been ready for "
                "**0.1 s** (page 13)"])


# ---------------------------------------------------------------- 11-15: control, software, aim, auto, tests
def p11_control(doc):
    p = doc.page("Control system")
    top, bottom = p.rows(p.area, 1.05, 1)
    m = p.box(top, "What each part does")
    m.table(m.content, [
        ["Part", "Problem it solves", "What it does"],
        ["4 drive motors", "moving in any direction", "drive each swerve wheel"],
        ["4 steering servos + 4 angle sensors", "pointing every wheel the right way", "turn each pod and read its angle"],
        ["IMU", "knowing which way we face", "heading for driving and aiming"],
        ["Front and rear cameras", "finding pollen and the goal", "pollen pathing; AprilTags"],
        ["4 beam sensors", "knowing how much pollen we hold", "count the pollen along the transition"],
        ["Gate servo", "pollen reaching the shooter too early", "holds pollen until the shot is ready"],
        ["2 shooter motors", "the same shot every time", "flywheels held at target speed (PIDF)"],
        ["Hood servo", "shooting from different distances", "sets the launch angle"],
        ["Flower mechanism servo", "pollen stuck inside the flower", "gets it out"],
        ["Blocker servo", "opponents shooting at us", "stops their shots"],
        ["Voltage and current checks", "brown-outs and stalled motors", "logged every loop"],
        ["8 motors and 8 servos", "rule R503 limits us to 8 of each", "we use all 16"]],
        col_weights=[1.25, 1.35, 1.6])
    l, r = p.cols(bottom, 1, 1)
    o = p.box(l, "Odometry pod")
    o1, o2 = p.rows(o.content, 1, 1)
    o.labelled(o1, OD / "odom_pod_assembled_iso.png", "Line drawing of the odometry pod",
               labels=[(0.5, 0.3, "mounting plate", 0.08, 0.05), (0.57, 0.93, "odometry wheels", 0.82, 0.72)])
    o.picture(o2, OD / "odom_pod_exploded_iso.png", "Exploded line drawing of the odometry pod",
              "Designed in CAD. The code uses wheels and the IMU for now")
    s = p.box(r, "Speed control")
    s.story(s.content, [("Challenge", "Each shot takes energy from the flywheels, and a slower wheel shoots short."),
                        ("Solution", "A **PIDF** controller holds the target speed. Its feedforward uses battery "
                                     "voltage, so a flat battery does not change the shot."),
                        ("Limits", "The flywheels are limited to **3500 RPM**. They count as ready within **50 RPM** "
                                   "of the target and the hood within **2 degrees**."),
                        ("Result", "Not tested yet: the robot is not finished.")])


def p12_software(doc):
    p = doc.page("Software and simulation")
    top, mid, fixes, bottom = p.rows(p.area, 0.66, 1.08, 1.12, 0.72)
    a = p.box(top, "Same code on the robot and on a laptop", accent=True)
    a.table(a.content, [["Part", "What it holds", "Why"],
                        ["RobotCode", "behaviour: driving, aiming, shooting", "written once, used on both"],
                        ["TeamCode", "the real motors, servos and sensors", "only place that touches hardware"],
                        ["RobotSim", "simulated robot, field and pollen", "test before the robot is finished"]],
            col_weights=[0.9, 1.6, 1.5])
    l, r = p.cols(mid, 1, 1)
    s = p.box(l, "Why we simulate")
    s.story(s.content, [("Challenge", "The robot is not finished yet, but the code needs testing now."),
                        ("Solution", "The same TeleOp runs in our simulator on the official field CAD."),
                        ("Result", "In simulation we score **3 of 3** for both alliances, also while moving.")])
    t = p.box(r, "Automated tests")
    t.text(t.content, ["- **24 desktop tests** pass (25 October 2026)",
                       "- They cover heading wrap, 10 ms loops, a lost heading sensor, manual turn override and "
                       "stop outputs",
                       "- Every loop is logged, so we can replay a run"])
    f = p.box(fixes, "What we found and fixed when we merged the code")
    f.table(f.content, [["Problem", "Fix"],
                        ["Shooter could never reach its shooting state", "a target speed now starts the wheel controller"],
                        ["Updates changed numbers but moved nothing", "read feedback, write a limited motor power every loop"],
                        ["RPM, encoder ticks, degrees and servo positions mixed", "one unit for each value; conversion only in hardware code"],
                        ["The flywheel's controller also drove the hood", "the hood has its own mapping and rate limit"],
                        ["Lookup table divided by zero at its first point", "handles exact points; never guesses past its ends"],
                        ["Simulated aiming stopped about 12 degrees short", "wheel feedforward based on battery voltage"]],
            col_weights=[1.1, 1.1])
    n = p.box(bottom, "Risks and how we reduce them")
    n.table(n.content, [["Risk", "How we reduce it"],
                        ["Simulation is not the real robot", "the code refuses to feed until the shooter is calibrated"],
                        ["Heading sensor lost mid-match", "tested in simulation: stops driving and feeding"],
                        ["Flat battery changes the shot", "feedforward scaled by battery voltage"],
                        ["A complex turret fails", "no turret: the drivetrain aims"]], col_weights=[1, 1.5])


def p13_aim(doc):
    p = doc.page("Auto-aim")
    top, chk, mid, bottom = p.rows(p.area, 0.5, 1.0, 0.86, 0.42)
    s = p.box(top, "The problem")
    s.story(s.content, [("Challenge", "We dropped the turret, so the shooter faces backwards and cannot turn on its "
                                      "own."),
                        ("Solution", "Holding the aim button turns the **whole robot** until it is within **2.5 "
                                     "degrees** of the goal.")])
    c = p.box(chk, "What the robot checks before every shot, in order", accent=True)
    c.table(c.content, [["Check", "If not, the robot says", "Why"],
                        ["Is there a possible shot?", "NO TRAJECTORY", "do not waste pollen"],
                        ["Is the shooter calibrated?", "CALIBRATION REQUIRED", "simulation is not the real robot"],
                        ["Is it aimed and not still turning?", "AIMING", "within 2.5 degrees"],
                        ["Flywheels and hood on target?", "SPINNING UP", "within 50 RPM and 2 degrees"],
                        ["Ready for 0.1 s?", "SETTLING", "it must stay on target, not pass through it"],
                        ["Is there pollen to shoot?", "EMPTY", "the beam sensors know"],
                        ["All yes", "FEEDING", "pollen goes to the shooter"]], col_weights=[1.45, 1.2, 1.3])
    l, r = p.cols(mid, 1, 1)
    h = p.box(l, "Maths: turning to aim")
    h.text(h.content, ["Turn speed = **feedback** on the heading error + **damping** + **feedforward** for a goal "
                       "that moves as we drive + a small push past **static friction**.",
                       "Gains: kP 4.0, kD 0.35, kS 0.06.",
                       "In simulation, aiming first stopped **12 degrees** short because small commands sat inside "
                       "the static friction dead zone."])
    v = p.box(r, "Maths: shooting while moving")
    v.text(v.content, ["The pollen leaves with the shooter's speed **plus the robot's**:",
                       "**v pollen = v shot + v robot + turn rate × r**",
                       "(r is where the pollen leaves, measured from the robot's centre). We look **0.07 s** ahead to "
                       "where the robot will be at release, then a gravity solver finds the speed and hood angle."])
    t = p.box(bottom, "Tests")
    t.table(t.content, [["Test", "Simulation", "Robot"], ["Score while still", "3 of 3", "not finished yet"],
                        ["Score while moving", "3 of 3", "not finished yet"]], col_weights=[1.4, 1, 1.2])


def p14_auto(doc):
    p = doc.page("Autonomous")
    top, mid, bottom = p.rows(p.area, 1.3, 0.66, 0.72)
    r = p.box(top, "Our route", accent=True)
    r.text(r.content, ["<auto route drawing: our hand-drawn route, redrawn cleanly>"])
    l, rr = p.cols(mid, 1, 1)
    s = p.box(l, "Each step")
    s.table(s.content, [["Step", "What", "Points"], ["1", "<step>", "<pts>"], ["2", "<step>", "<pts>"],
                        ["3", "<step>", "<pts>"]], col_weights=[0.6, 2, 0.8])
    st = p.box(rr, "Status")
    st.text(st.content, ["- On 12-18 October we started a **ball-tracking** setup so the robot can find, map and "
                         "intake pollen by itself",
                         "- The full autonomous is **not finished**: NOT TESTED",
                         "- <date we plan to have it running>"])
    u = p.box(bottom, "What it can use")
    u.table(u.content, [["Part", "What it gives the autonomous"],
                        ["Wheels + IMU", "where we are as we drive"],
                        ["Rear camera", "AprilTags, to know where we are on the field"],
                        ["Front camera", "a path to the pollen"],
                        ["Beam sensors", "how much pollen we hold"],
                        ["Auto-aim", "the same shot checks as TeleOp (page 13)"]], col_weights=[1, 2.6])


def p15_tests(doc):
    p = doc.page("Testing and lessons")
    top, mid, bottom, foot = p.rows(p.area, 0.92, 0.74, 0.25, 0.1)
    t = p.box(top, "Test results")
    t.table(t.content, [["Test", "Result", "Status"],
                        ["24 automated code tests", "all pass", "PASS"],
                        ["Simulation: score 3 of 3, still and moving", "3 of 3", "PASS"],
                        ["Simulation: pick up 3, aim, score 3", "3 of 3", "PASS"],
                        ["Simulation: lost heading sensor", "stops drive and feeding", "PASS"],
                        ["Robot: shots in from 3 distances", "not finished yet", "NOT TESTED"],
                        ["Robot: time between shots", "not finished yet", "NOT TESTED"],
                        ["Robot: top speed", "not finished yet", "NOT TESTED"],
                        ["Robot: X-lock push", "not finished yet", "NOT TESTED"],
                        ["Robot: jams per 20 pickups", "not finished yet", "NOT TESTED"],
                        ["Autonomous", "not written yet", "NOT TESTED"]], col_weights=[2, 1.1, 0.9], status_col=2)
    l, r = p.cols(mid, 1, 1)
    a = p.box(l, "Lessons we applied")
    a.text(a.content, ["- A turret cost us months last season, so this season the drivetrain aims",
                       "- We sketch the pollen path before the CAD, starting with sizes",
                       "- Every value in the code has one unit (RPM, radians)",
                       "- We merge subsystems early, because the bugs on page 12 only showed when they met",
                       "- When time is short, we cut the least necessary part and make the rest consistent",
                       "- We plan each week around exams and outreach"])
    b = p.box(r, "Next")
    b.text(b.content, ["- Finish the robot, then run every test on this page",
                       "- Calibrate the shooter on the real robot",
                       "- Measure the lookup table",
                       "- Write and test the autonomous",
                       "- <next design change>"])
    c = p.box(bottom, "Reliability")
    c.text(c.content, ["No matches yet: the robot is not finished. For every match we will record whether it worked "
                       "all match, and any fault and its fix."])
    write(p.slide, foot, [{"text": ENDNOTE, "size": 10, "colour": MUTED, "after": 0}], sizes=p.sizes)


PAGES = [p01_team, p02_season, p03_outreach, p04_process, p05_strategy, p06_robot, p07_swerve, p08_intake,
         p09_shooter, p10_loader, p11_control, p12_software, p13_aim, p14_auto, p15_tests]


def build():
    doc = Portfolio(TEAM, TEAM_NAME)
    cover(doc)
    for page in PAGES:
        page(doc)
    return doc


if __name__ == "__main__":
    doc = build()
    if "--draft" in sys.argv:
        print(doc.save(sys.argv[-1], strict="--loose" not in sys.argv))
    else:
        print(doc.save_versioned(DELIVERABLE, NAME, sys.argv[1] if len(sys.argv) > 1 else "first version"))
