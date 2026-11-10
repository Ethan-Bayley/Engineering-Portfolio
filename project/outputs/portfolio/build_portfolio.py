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


ENDNOTE = ("Endnote: text drafted and laid out with help from an AI assistant. All results, photos, CAD, code and "
           "decisions are the team's own; the team checked every page.")
SW, SH, OD, TU, TR, RB = (LW / k for k in ("swerve", "shooter", "odometry", "turret", "transition", "robot"))
PHOTOS = A / "photos" / "ready"                    # team photos, prepared with general/tools/photo_prep.py
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
    top, bottom = p.rows(p.area, 3.3, 1)
    members = [("Ethan B.", "Lead design", "assembly"), ("Brandon L.", "CAD", "assembly"),
               ("Isaac H.", "Lead code", "CAD, assembly"), ("Ryan T.", "Driver", "CAD"),
               ("Will Q.", "Lead strategy", "drive coach"), ("Ivy W.", "Programming", "HR"),
               ("Tina X.", "Code", "assembly, strategy"), ("Chelsey W.", "Assembly", "scouting"),
               ("Chloe L.", "Electrical", "assembly"), ("Chloe S.", "Strategy", "code, assembly"),
               ("Jemima C.", "Programming", "scouting"),
               ("Lucas T.", "CAD", "assembly")]
    t = p.box(top, "12 members")
    t.team(t.content, [(n, r, None, note) for n, r, note in members], cols=2)
    l, r = p.cols(bottom, 1, 1)
    h = p.box(l, "How we split the work")
    h.text(h.content, ["- **CAD:** 4 members in Onshape, with our lead designer",
                       "- **Code:** 5 members write and test the code",
                       "- **Strategy:** 3 members plan it; 4 members scout",
                       "- **Assembly:** 8 of 12 members build"])
    w = p.box(r, "How we work")
    w.text(w.content, ["- We meet **every week or two**",
                       "- Each specialty decides its own area (mechanics decide mechanical changes), then tells "
                       "the whole team",
                       "- Each subsystem has its own code branch, merged into one robot"])


def p02_season(doc):
    p = doc.page("Our season")
    top, plan, bottom = p.rows(p.area, 0.5, 1.2, 0.95)
    tl = p.box(top, "2026 so far")
    tl.timeline(tl.content, [("10 Oct", "Turret cut", "team meeting"), ("12-18 Oct", "Design done", "intake, transfer, shooter"),
                             ("19-25 Oct", "Machining", "assembly began"), ("26 Oct-1 Nov", "Swerve built", "goBILDA parts here"),
                             ("12 Nov", "Wollongong", "first event")])
    pv = p.box(plan, "Planned on 10 October, and what happened", accent=True)
    pv.table(pv.content, [["Week", "Planned", "What happened"],
                          ["12-18 Oct", "finish the CAD; make the custom swerve parts",
                           "goBILDA parts ordered; shooter redesigned and simplified; intake and transfer design done; "
                           "ball tracking for autos started; hood and shooter code started"],
                          ["19-25 Oct", "goBILDA parts may arrive; make the shooter and transition; assembly",
                           "parts machined; assembly began"],
                          ["26 Oct-1 Nov", "wiring, programming, fixing mechanical issues",
                           "goBILDA parts arrived; swerve assembled"],
                          ["2-8 Nov", "programming and drive practice", "<what happened>"]],
             col_weights=[0.8, 1.7, 2.3])
    l, r = p.cols(bottom, 1.15, 1)
    sc = p.box(l, "How we schedule")
    sc.story(sc.content, [("How", "A spreadsheet shared with students and mentors shows who is free each week and what "
                                  "work they are given."),
                          ("Lesson", "It mostly worked, but an exam block and outreach made it hard to judge what each "
                                     "week could really fit.")])
    b = p.box(r, "This season's goals")
    b.text(b.content, ["- Shoot from **anywhere** on the field",
                       "- **Less waiting** between shots",
                       "- Collect along the wall and shoot **without turning round**",
                       "- Hold our spot against **defence**",
                       "- Keep the robot **light**, so it moves more efficiently"])


def p03_outreach(doc):
    p = doc.page("Outreach")
    top, a_r, mid, bottom = p.rows(p.area, 0.34, 1.12, 1.7, 0.5)
    stats(p, top, [("6", "members teach Darkinjung students"), ("Fortnightly", "since about February 2026"),
                   ("1,500+", "people at Round Square"), ("About 32", "countries at Round Square")])
    a = p.box(a_r, "Teaching Darkinjung students", accent=True)
    a.story(a.content, [("What", "**6 members** of our team (Ethan B., Brandon L., Chloe S., Ivy W., Ryan T. and "
                                 "Will Q.) teach robotics to Darkinjung students **once a fortnight**, since about "
                                 "February 2026."),
                        ("What they learn", "They built robots for this year's **VEX IQ** game and learnt how to "
                                            "build, how to code, how to do interviews and how to write portfolios."),
                        ("Impact", "Some of the students were in competitive teams and won **Skills**, "
                                   "**Teamwork Champion** and **Excellence** awards.")])
    d = p.box(mid, "Round Square International Conference")
    ds, dp = p.cols(d.content, 1, 1.15)
    d.picture(dp, PHOTOS / "round_square_2026-09-28.jpg",
              "Photo from above of our robotics showcase at the Round Square conference: fields, robots and visitors",
              "Our robotics showcase at Round Square, 28 September 2026")
    d.story(ds, [("What", "On **28 September 2026** Ivy W., Ethan B., Ryan T., Chelsey W., Chloe L., Isaac H., "
                                 "Tina X. and Will Q. ran the robotics part of the conference at Barker."),
                        ("Demos", "At the opening fair we showed robots driving, shooting, intaking and "
                                  "scoring."),
                        ("Reach", "**Over 1,500 people** from around **32 countries**, many of whom had not heard of "
                                  "FIRST before.")])
    l, r = p.cols(bottom, 1, 1)
    b = p.box(l, "Mentoring VEX teams")
    b.text(b.content, ["Ethan B., Isaac H. and Brandon L. mentor VEX teams."])
    c = p.box(r, "Barker VEX competition")
    c.text(c.content, ["Ethan B., Isaac H. and Brandon L. volunteered."])


def p04_process(doc):
    p = doc.page("How we engineer")
    top, mid, bottom = p.rows(p.area, 0.42, 1.2, 0.95)
    c = p.box(top, "Our design loop")
    c.timeline(c.content, [("1", "Goals", "what the game needs"), ("2", "Sketch + CAD", "Onshape layouts"),
                           ("3", "Simulate", "same code, desktop sim"), ("4", "Build", "parts and assembly"),
                           ("5", "Test + change", "back to step 2")])
    s = p.box(mid, "Example: from sketch to part")
    l, r = p.cols(s.content, 1, 1)
    s.labelled(l, TR / "transition_ball_path_sketch_dimensions.png",
               "Dimensioned layout sketch of the pollen path through the transition",
               labels=[(0.12, 0.8, "pollen", 0.5, 0.96), (0.52, 0.18, "belt spacing", 0.35, -0.02)],
               caption="1. Layout sketch first: pollen size, roller sizes and belt spacing (mm)")
    s.labelled(r, TR / "transition_side_ball_path_highlight.png",
               "Side view of the transition built from that sketch, with the pollen path highlighted",
               labels=[(0.1, 0.55, "rollers", 0.1, 0.02), (0.38, 0.38, "gecko wheels", 0.55, 0.02)],
               caption="2. Then the plates and belts are designed around it in CAD")
    l, r = p.cols(bottom, 1, 1)
    m = p.box(l, "One robot, many branches")
    m.text(m.content, ["Each subsystem was coded on its own branch: **intake** (Tina X.), **shooter** (Jemima C.), "
                       "then merged into one robot on **25 October**.",
                       m.head("What merging taught us"),
                       "- Two branches each hid the other's subsystem: fixed",
                       "- Units were mixed (RPM, ticks, degrees): one unit per value now",
                       "- All the fixes are on page 12"])
    v = p.box(r, "Ideas we brought in")
    v.story(v.content, [("From VEX", "Ethan B., Will Q., Ryan T. and Tina X. played VEX **Push Back**. The game was "
                                     "very similar, so our matchloader follows the same idea (page 10)."),
                        ("From last season", "Swerve and logging carried over; the turret did not (page 9).")])


def p05_strategy(doc):
    p = doc.page("Strategy and requirements")
    top, mid, tab, bottom = p.rows(p.area, 0.42, 0.62, 1.1, 0.27)
    g = p.box(top, "How we play")
    g.text(g.content, ["<our scoring plan: what we score first, where we shoot from, our role with the alliance "
                       "partner>",
                       "Pollen collects along the wall, so we collect there and shoot from there."])
    c = p.box(mid, "One scoring cycle, as our code runs it")
    c.timeline(c.content, [("1", "Collect", "until 3 are held"), ("2", "Hold aim", "robot turns to the goal"),
                           ("3", "Spin up", "flywheels and hood reach target"), ("4", "Settle", "ready for 0.1 s"),
                           ("5", "Feed", "pollen goes to the shooter")])
    r = p.box(tab, "Requirements, and how the robot meets each", accent=True)
    r.table(r.content, [["We need to", "Why", "Our answer"],
                        ["Shoot from anywhere", "fewer trips across the field", "moving hood"],
                        ["Shoot quickly, again and again", "less waiting between shots", "two flywheels"],
                        ["Shoot without turning round", "pollen collects along the wall", "rear-facing shooter"],
                        ["Aim while driving", "save time every cycle", "swerve + auto-aim"],
                        ["Hold our spot", "defence will push us", "swerve X-lock"],
                        ["Move efficiently", "a big advantage in matches", "swerve; a light robot"],
                        ["Load the flower fast", "<why>", "matchloader"],
                        ["Find pollen and the goal", "drive and aim without guessing", "front + rear cameras"]],
            col_weights=[1.25, 1.35, 1.25])
    s = p.box(bottom, "Scouting")
    s.text(s.content, ["Jemima C., Chelsey W., Chloe L. and Tina X. scout: <what we record and how it changes our plan>"])


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
    k = p.box(r, "Numbers", accent=True)
    k.table(k.content, [["Item", "Value"], ["Size (CAD)", "407.7 x 327.0 x 290.9 mm"],
                        ["Pod centres (CAD)", "239 x 239 mm"], ["Wheels (CAD)", "60.9 mm"],
                        ["Motors", "8: drive 4, intake 2, shooter 2"],
                        ["Servos", "8: steering 4, hood, blocker, matchloader, gate"], ["Cameras", "2: front, rear"]],
            col_weights=[0.8, 1.35])
    c = p.box(bottom, "Chassis: light, so it moves more efficiently")
    l, r = p.cols(c.content, 1.1, 1)
    c.picture(l, LW / "chassis" / "chassis_exploded_iso.png", "Exploded line drawing of the chassis and swerve pods",
              "Exploded: pods, plates and side panels")
    c.picture(r, LW / "chassis" / "chassis_bottom.png", "Line drawing of the underside of the chassis",
              "Underneath: pods in the corners")


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
    k = p.box(r, "Why swerve, again", accent=True)
    k.text(k.content, [
        "- **X-lock:** the wheels sit in an X, and the friction makes us a lot harder to push or defend",
        "- Moves a lot more **efficiently**: a big advantage in matches",
        "- Full-grip wheels: more **speed and pushing power** than mecanum",
        "- **Aim while driving:** drive one way, face the goal",
        "- We built swerve last season, so the risk was low",
        k.head("Key features"),
        "- **4 pods**, each with a drive motor and a steering servo; custom parts we designed, machined",
        "- An **absolute angle sensor** in every pod, so each wheel knows where it points from the start",
        "- Pod centres **239 x 239 mm** apart; wheels **60.9 mm**"])
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
               caption="Servo and ring gear turn the whole pod")
    t = p.box(bottom, "Tests")
    t.table(t.content, [["Test", "Result", "Status"], ["Top speed", "not finished yet", "NOT TESTED"],
                        ["Pushed by another robot in X-lock", "not finished yet", "NOT TESTED"]],
            col_weights=[1.6, 1.2, 1], status_col=2)


def p08_intake(doc):
    p = doc.page("Intake and transition")
    top, mid, bottom = p.rows(p.area, 0.82, 1.05, 0.72)
    it = p.box(top, "What we tried")
    it.iterations(it.content, [
        ("V1 printed funnels", None, "", ["<what worked>"], ["gecko wheels at the front only", "<what went wrong>"]),
        ("V2 rollers + transition", TR / "transition_iso.png", "Line drawing of the intake and transition assembly",
         ["mecanum rollers sweep pollen in", "gecko wheels grip it and carry it up"], ["<downside, if any>"])])
    l, r = p.cols(mid, 1.2, 1)
    d = p.box(l, "Pollen path")
    d.labelled(d.content.inset(0.5 * G, 1.2 * G), TR / "transition_side_ball_path_highlight.png",
               "Side view of the transition with the pollen path highlighted",
               labels=[(0.1, 0.55, "mecanum rollers", 0.15, 0.0), (0.38, 0.38, "gecko wheels", 0.6, 0.0),
                       (0.55, 0.78, "pollen guide", 0.82, 0.86)],
               caption="Rollers pull pollen in; gecko wheels lift it to the shooter")
    k = p.box(r, "Key sizes and sensing", accent=True)
    k.text(k.content, ["- Pollen **71.12 mm**; intake rollers **50 mm**",
                       "- Gecko wheels **48 mm**",
                       "- Small gecko wheels **32 mm** at the top, so less **backspin** goes into the shooter",
                       "- Belt spacing **45, 58.5, 54, 44 mm**",
                       "- 2 motors drive the intake and transition",
                       "- **Polycarbonate ramps** give the pollen a low-friction surface",
                       "- **3 beam sensors** count the pollen (empty, one, two, full); the intake stops when full",
                       "- Jams: not tested yet (robot not finished)"])
    m = p.box(bottom, "Maths: where the pollen touches")
    l, r = p.cols(m.content, 1, 1.2)
    m.picture(l, TR / "transition_ball_path_sketch.png", "Layout sketch of the pollen's path past each roller")
    m.text(r, ["Our two rows of gecko wheels sit apart, so each row meets the pollen off its centre. The sketch plane "
               "cuts the pollen in a circle of **70.413 mm**:",
               "**d = √(35.56² − 35.21²) = 5.0 mm**",
               "So the plane is 5.0 mm from the pollen's centre, and the sketch uses 70.413 mm there, not 71.12 mm."])


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
        "- **Two flywheels:** more flywheel means **less waiting** between shots",
        "- **Moving hood:** shoot from anywhere on the field. Range in our code: **33.6 to 67 degrees**",
        "- **Facing backwards:** pollen collects along the wall, so we drive up to the wall and aim, instead of "
        "collecting and then turning round",
        "- **Lookup table:** speed and hood angle from where localisation says we are; values measured once the "
        "robot is finished",
        w.head("Why we cut the turret (meeting, 10 October)"),
        "Regionals were **4 weeks** away and our goBILDA parts were delayed, so something had to go. The turret was "
        "the least necessary part. We kept swerve and the blocker, which still speed up shooting, and spent the time "
        "on a consistent intake, transfer, swerve, autos and code. The swerve base now turns the robot to aim "
        "(page 13)."])
    a, b = p.rows(r, 1, 1.25)
    d = p.box(a, "Hood drive")
    d.labelled(d.content.inset(0.5 * G, 0.8 * G), SH / "shooter_side_hood_drive_highlight.png",
               "Side line drawing of the shooter with the hood drive highlighted",
               labels=[(0.6, 0.42, "hood rack", 0.42, 0.0), (0.72, 0.3, "servo gear", 0.9, 0.0),
                       (0.1, 0.3, "flywheel", 0.1, 0.0)],
               caption="A servo gear drives a rack to tilt the hood")
    e = p.box(b, "Exploded view")
    e.labelled(e.content, SHOTS / "shooter_exploded_iso.png", "Exploded CAD view of the fixed shooter",
               labels=[(0.42, 0.65, "flywheels", 0.08, 0.72), (0.62, 0.32, "hood", 0.88, 0.1)])
    t = p.box(bottom, "Tests")
    t.table(t.content, [["Test", "Result", "Status"], ["Shots in from 3 distances", "not finished yet", "NOT TESTED"],
                        ["Time between shots", "not finished yet", "NOT TESTED"]], col_weights=[1.6, 1.2, 1], status_col=2)


def p10_loader(doc):
    p = doc.page("Matchloader and cameras")
    top, mid, bottom = p.rows(p.area, 0.92, 0.95, 0.82)
    l, r = p.cols(top, 1, 1)
    m = p.box(l, "Matchloader", accent=True)
    m.story(m.content, [("Idea", "Four of us played VEX **Push Back**, a very similar game. We used the same kind "
                                 "of matchloader for the flower."),
                        ("Problem", "<what the matchloader fixes, with a number>"),
                        ("Result", "Not tested yet: the robot is not finished.")])
    b = p.box(r, "Blocker and gate")
    b.story(b.content, [("Blocker", "<what the blocker stops> (1 Axon Max servo)"),
                        ("Gate", "Stops pollen going into the shooter until the shot is ready (1 Axon servo).")])
    c = p.box(mid, "Two cameras")
    l2, r2 = p.cols(c.content, 1.5, 1)
    c.labelled(l2, TR / "transition_side_cameras_highlight.png", "Side view with the two cameras highlighted",
               labels=[(0.05, 0.12, "front camera", 0.2, -0.02), (0.88, 0.12, "rear camera", 0.78, -0.02)])
    c.text(r2, ["- **Front camera:** finds pollen, so we can path to it",
                "- **Rear camera:** reads AprilTags, so we know where the goal is",
                "- Status: not tested yet (robot not finished)"])
    h = p.box(bottom, "How pollen is held, then released")
    l3, r3 = p.cols(h.content, 1, 1.15)
    h.picture(l3, TR / "transition_front.png", "Front line drawing of the intake and transition")
    h.text(r3, ["- **Collect:** the intake runs until the 3 beam sensors say we are full, then it stops",
                "- **Hold:** pollen waits while the robot aims",
                "- **Release:** pollen only feeds once aim, flywheel speed and hood have all been ready for "
                "**0.1 s** (page 13)"])


# ---------------------------------------------------------------- 11-15: control, software, aim, auto, tests
def p11_control(doc):
    p = doc.page("Control system")
    top, bottom = p.rows(p.area, 0.95, 1)
    m = p.box(top, "What each part does")
    m.table(m.content, [
        ["Part", "Problem it solves", "What it does"],
        ["4 drive motors", "moving in any direction", "drive each swerve wheel"],
        ["4 steering servos + 4 angle sensors", "pointing every wheel the right way", "turn each pod and read its angle"],
        ["IMU", "knowing which way we face", "heading for driving and aiming"],
        ["Front and rear cameras", "finding pollen and the goal", "pollen pathing; AprilTags"],
        ["3 beam sensors", "knowing how much pollen we hold", "sense pollen at bottom, middle and top"],
        ["Gate servo", "pollen reaching the shooter too early", "holds pollen until the shot is ready"],
        ["2 shooter motors", "the same shot every time", "flywheels held at target speed (PIDF)"],
        ["Hood servo", "shooting from different distances", "sets the launch angle"],
        ["Voltage and current checks", "brown-outs and stalled motors", "logged every loop"]],
        col_weights=[1.25, 1.35, 1.6])
    l, r = p.cols(bottom, 1, 1)
    o = p.box(l, "Odometry pod")
    o1, o2 = p.rows(o.content, 1, 1)
    o.labelled(o1, OD / "odom_pod_assembled_iso.png", "Line drawing of the odometry pod",
               labels=[(0.5, 0.3, "mounting plate", 0.08, 0.05), (0.57, 0.93, "odometry wheels", 0.82, 0.72)])
    o.picture(o2, OD / "odom_pod_exploded_iso.png", "Exploded line drawing of the odometry pod",
              "Designed in CAD; the code uses wheels + IMU for now")
    s = p.box(r, "Speed control")
    s.story(s.content, [("Challenge", "Each shot takes energy from the flywheels, and a slower wheel shoots short."),
                        ("Solution", "A **PIDF** controller holds the target speed; feedforward uses battery "
                                     "voltage, so a flat battery does not change the shot."),
                        ("In our code", "Flywheels are limited to **3500 RPM** and count as ready within **50 RPM** "
                                        "of the target; the hood within **2 degrees**."),
                        ("Result", "Not tested yet: the robot is not finished.")])


def p12_software(doc):
    p = doc.page("Software and simulation")
    top, mid, fixes, bottom = p.rows(p.area, 0.66, 1.08, 1.12, 0.72)
    a = p.box(top, "Same code on the robot and on a laptop", accent=True)
    a.table(a.content, [["Part", "What it holds", "Why"],
                        ["RobotCode", "behaviour: driving, aiming, shooting", "written once, used everywhere"],
                        ["TeamCode", "the real motors, servos and sensors", "only place that touches hardware"],
                        ["RobotSim", "simulated robot, field and pollen", "test before the robot is finished"]],
            col_weights=[0.9, 1.6, 1.5])
    l, r = p.cols(mid, 1, 1)
    s = p.box(l, "Why we simulate")
    s.story(s.content, [("Challenge", "The robot is not finished yet, but the code needs testing now."),
                        ("Solution", "The same TeleOp runs in our simulator on the official field CAD."),
                        ("Result", "Simulation: scores **3 of 3** for both alliances, also while moving.")])
    t = p.box(r, "Automated tests")
    t.text(t.content, ["- **24 desktop tests** pass (25 October 2026)",
                       "- They cover heading wrap, 10 ms loops, a lost heading sensor, manual turn override and "
                       "stop outputs",
                       "- Every loop is logged, so a run can be replayed"])
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
                        ("Solution", "Holding aim turns the **whole robot** until it is within **2.5 degrees** of the "
                                     "goal.")])
    c = p.box(chk, "What the robot checks before every shot, in order", accent=True)
    c.table(c.content, [["Check", "If not, the robot says", "Why"],
                        ["Is there a possible shot?", "NO TRAJECTORY", "do not waste pollen"],
                        ["Is the shooter calibrated?", "CALIBRATION REQUIRED", "simulation is not the real robot"],
                        ["Is it aimed and not still turning?", "AIMING", "within 2.5 degrees"],
                        ["Flywheels and hood on target?", "SPINNING UP", "within 50 RPM and 2 degrees"],
                        ["Ready for 0.1 s?", "SETTLING", "must stay on target, not pass through it"],
                        ["Is there pollen to shoot?", "EMPTY", "the beam sensors know"],
                        ["All yes", "FEEDING", "pollen goes to the shooter"]], col_weights=[1.45, 1.2, 1.3])
    l, r = p.cols(mid, 1, 1)
    h = p.box(l, "Maths: turning to aim")
    h.text(h.content, ["Turn speed = **feedback** on the heading error + **damping** + **feedforward** for a goal "
                       "that moves as we drive + a small push past **static friction**.",
                       "Gains in our code: kP 4.0, kD 0.35, kS 0.06.",
                       "In simulation aiming first stopped **12 degrees** short: small commands were inside the "
                       "static friction dead zone."])
    v = p.box(r, "Maths: shooting while moving")
    v.text(v.content, ["The pollen leaves with the shooter's speed **plus the robot's**:",
                       "**v pollen = v shot + v robot + turn rate × r**",
                       "(r = where the pollen leaves, from the robot's centre). The code looks **0.07 s** ahead to "
                       "where the robot will be at release, then a gravity solver finds the speed and hood angle."])
    t = p.box(bottom, "Tests")
    t.table(t.content, [["Test", "Simulation", "Robot"], ["Score while still", "3 of 3", "not finished yet"],
                        ["Score while moving", "3 of 3", "not finished yet"]], col_weights=[1.4, 1, 1.2])


def p14_auto(doc):
    p = doc.page("Autonomous")
    top, mid, bottom = p.rows(p.area, 1.3, 0.66, 0.72)
    r = p.box(top, "Our route", accent=True)
    r.text(r.content, ["<auto route drawing: the team's hand-drawn route, redrawn cleanly>"])
    l, rr = p.cols(mid, 1, 1)
    s = p.box(l, "Each step")
    s.table(s.content, [["Step", "What", "Points"], ["1", "<step>", "<pts>"], ["2", "<step>", "<pts>"],
                        ["3", "<step>", "<pts>"]], col_weights=[0.6, 2, 0.8])
    st = p.box(rr, "Status")
    st.text(st.content, ["- Started 12-18 Oct: a **ball-tracking** setup so the robot can find, map and intake "
                         "pollen by itself",
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
    top, mid, bottom, foot = p.rows(p.area, 0.98, 0.62, 0.25, 0.1)
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
    a.text(a.content, ["- A turret cost months last season, so we let the drivetrain aim",
                       "- Sketch the pollen path before CAD: sizes and spacing first",
                       "- One unit for each value in code (RPM, radians)",
                       "- Merge subsystems early: the bugs on page 12 only showed when they met",
                       "- Short on time? Cut the least necessary part, make the rest consistent (10 Oct)",
                       "- Plan weeks around exams and outreach"])
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
