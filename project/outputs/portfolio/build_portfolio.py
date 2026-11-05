"""Build the FTC portfolio for 11143 Barker Yellowbacks (2026-27, BIOBUZZ): the cover plus up to 15 pages.

    python project/outputs/portfolio/build_portfolio.py "what changed"      # saves portfolio_vNN.pptx
    python project/outputs/portfolio/build_portfolio.py --draft x.pptx
    python general/tools/export_pdf.py project/outputs/portfolio/portfolio_vNN.pptx --render project/outputs/renders/vNN
    python general/tools/hand_in_check.py --deliverable portfolio --max-pages 16 --max-mb 15 --min-pt 10

Look: project/design/PORTFOLIO_STYLE.md (the team's cover, colours tightened). FTC A201: cover (team number; not
judged) + at most 15 pages, nothing under 10 pt, first names and last initials only, work since 1 January 2026.
Text drafted from the team's logs and answers (project/logs/, 2026-11-05) and the code report (Pinkbacks branch
Isaac, doc/isaac-integration.md); AI credit endnote on page 15 (A201). Anything not measured on the robot is a
<RESULT: ...> or <...> placeholder, which the hand-in check fails on until the team fills it. Drawings: the team's
own, recoloured, in assets/cad/linework_page/. Page plan: project/brief/PAGE_PLAN.md.
"""
import sys
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "general" / "design").is_dir())
sys.path.insert(0, str(ROOT / "project" / "design"))
from portfolio_style import (G, INK, MUTED, Portfolio, Rect, bar, polygon, pill, pill_width,  # noqa: E402
                             stripes, width, write)
from design_system import _picture, _shape  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402

A = ROOT / "project" / "assets"
LW = A / "cad" / "linework_page"                    # team's line drawings, recoloured to the page (100 % fills)
ROBOT_A = LW / "robot" / "robot_iso.png"             # replaces the low-res cover crops (2026-11-05)
ROBOT_B = LW / "robot" / "robot_side.png"
DELIVERABLE = "portfolio"
TEAM, TEAM_NAME = "11143", "Barker Yellowbacks"


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
    write(s, Rect(a.x, by + 4, bw, bh - 8), [{"text": "ENGINEERING", "size": 24, "bold": True, "colour": INK, "after": 0},
                                              {"text": "PORTFOLIO", "size": 24, "bold": True, "colour": INK, "after": 0}],
          anchor=MSO_ANCHOR.MIDDLE, sizes=p.sizes)
    stripes(s, 14 + bw + 1.2 * G, by + bh + 0.6 * G, 22, n=5)
    # pill and team name
    py = by + bh + 4.4 * G
    text = "FTC - FIRST Tech Challenge"
    pill(s, Rect(a.x, py, pill_width(text, 11), 22), text, 11, filled=False, sizes=p.sizes)
    write(s, Rect(a.x, py + 30, a.w, 40), ["BARKER **YELLOWBACKS**"], 30, bold=True, sizes=p.sizes)
    # robot line art, team number box on the right
    ry = py + 80
    nb = Rect(a.r - 64, ry, 64, 270)
    _shape(s, MSO_SHAPE.RECTANGLE, nb, None, MUTED, 2)
    write(s, Rect(nb.x + nb.w / 2 - nb.h / 2, nb.y + nb.h / 2 - nb.w / 2, nb.h, nb.w),
          [{"text": TEAM, "size": 54, "bold": True, "colour": MUTED, "align": PP_ALIGN.CENTER, "after": 0}],
          anchor=MSO_ANCHOR.MIDDLE, rotation=90, sizes=p.sizes)
    bar(s, nb.x - 0.8 * G - 5, nb.y + 0.15 * nb.h, nb.h * 0.7, 5)
    _picture(s, ROBOT_A, Rect(a.x - 0.5 * G, ry, nb.x - a.x - 2 * G, 270), "Line drawing of our robot", "left")
    # season block bottom-left, second drawing bottom-right
    yb = a.b - 150
    bar(s, a.x, yb + 0.6 * G, 92, 4)
    write(s, Rect(a.x + 1.4 * G, yb - 20, 200, 135), [{"text": "2026-2027", "size": 22, "bold": True, "after": 2},
                                                  {"text": "Sydney", "size": 20, "after": 0},
                                                  {"text": "Australia", "size": 20, "after": 4},
                                                  {"text": "Barker College", "size": 11, "colour": MUTED, "after": 0},
                                                  {"text": "Supported by Barker Robotics", "size": 11, "colour": MUTED,
                                                   "after": 0}], sizes=p.sizes)
    _picture(s, ROBOT_B, Rect(a.x + 0.42 * a.w, a.b - 230, 0.58 * a.w, 230), "Second line drawing of our robot",
             "right")
    return p


ENDNOTE = ("Endnote: text drafted and laid out with help from an AI assistant. All results, photos, CAD, code and "
           "decisions are the team's own; the team checked every page.")
SW, SH, OD, TU, TR, RB = (LW / k for k in ("swerve", "shooter", "odometry", "turret", "transition", "robot"))


# ---------------------------------------------------------------- 1-5: team, season, outreach, process, strategy
def p01_team(doc):
    p = doc.page("Meet the team")
    top, bottom = p.rows(p.area, 2.75, 1)
    members = [("Ethan B.", "Lead design", "assembly"), ("Brandon L.", "CAD", "assembly"),
               ("Isaac H.", "Lead code", "CAD, assembly"), ("Ryan T.", "Driver", "CAD"),
               ("Will Q.", "Lead strategy", "drive coach"), ("Ivy W.", "Programming", "HR"),
               ("Tina X.", "Code", "assembly"), ("Chelsea W.", "Code", "assembly"),
               ("Chloe L.", "Electrical", "assembly"), ("Chloe S.", "Strategy", "code, assembly"),
               ("Cooper C.", "Scouting", "assembly"), ("Jemima C.", "Programming", "scouting"),
               ("Lucas T.", "CAD", "assembly")]
    t = p.box(top, "13 members")
    t.team(t.content, [(n, r, None, note) for n, r, note in members], cols=2)
    l, r = p.cols(bottom, 1, 1)
    h = p.box(l, "How we split the work")
    h.text(h.content, ["- **CAD:** 4 members in Onshape, with our lead designer",
                       "- **Code:** 6 members write and test the code",
                       "- **Strategy:** 2 strategists plus 2 scouts",
                       "- **Assembly:** 9 of 13 members build"])
    w = p.box(r, "How we work")
    w.text(w.content, ["- We meet <when, how often>",
                       "- Each subsystem has its own code branch, merged into one robot",
                       "- <how we make decisions as a team>"])


def p02_season(doc):
    p = doc.page("Our season")
    top, mid, bottom = p.rows(p.area, 0.5, 1.0, 0.55)
    tl = p.box(top, "2026 so far (dates from our code history)")
    tl.timeline(tl.content, [("23 Sep", "Shooter", "first shooter code"), ("12 Oct", "No turret", "turret removed"),
                             ("20 Oct", "Intake", "intake and transfer code"),
                             ("25 Oct", "One robot", "all subsystems merged"),
                             ("12 Nov", "Wollongong", "first event")])
    l, r = p.cols(mid, 1, 1)
    a = p.box(l, "What we kept from last season")
    a.text(a.content, ["Last season's robot (background only) taught us:",
                       "- ++Swerve works for us:++ we kept it",
                       "- ~~A turret takes months to tune:~~ April to June 2026, so this year we dropped it",
                       "- Logging and replay carried over to this season's code"])
    b = p.box(r, "This season's goals", accent=True)
    b.text(b.content, ["- Shoot from **anywhere** on the field",
                       "- **Less waiting** between shots",
                       "- Collect along the wall and shoot **without turning round**",
                       "- Hold our spot against **defence**"])
    pl = p.box(bottom, "Build dates")
    pl.table(pl.content, [["Stage", "Planned", "Actual"], ["CAD finished", "<date>", "<date>"],
                          ["Robot built", "<date>", "<date>"], ["First drive", "<date>", "<date>"]],
             col_weights=[1.4, 1, 1])


def p03_outreach(doc):
    p = doc.page("Outreach")
    top, bottom = p.rows(p.area, 1, 1)
    l, r = p.cols(top, 1, 1)
    a = p.box(l, "Darkinjung students", accent=True)
    a.story(a.content, [("What", "**7 members** teach robotics to Darkinjung students once a fortnight."),
                        ("Reach", "<number> students, <number> sessions since <month>."),
                        ("Impact", "<what the students built or learned>")])
    b = p.box(r, "Mentoring VEX teams")
    b.story(b.content, [("What", "Ethan B. and Isaac H. mentor <number> VEX teams."),
                        ("Reach", "<number> students, <how often>."),
                        ("Impact", "<a result, e.g. a team's award>")])
    l, r = p.cols(bottom, 1, 1)
    c = p.box(l, "Barker VEX competition")
    c.story(c.content, [("What", "Ethan B., Isaac H. and Brandon L. volunteered at the Barker VEX competition."),
                        ("When", "<date>, <number> teams")])
    d = p.box(r, "Round Square conference")
    d.story(d.content, [("What", "We ran the robotics part of the Round Square International Conference at Barker."),
                        ("When", "<date>, <number> people")])


def p04_process(doc):
    p = doc.page("How we engineer")
    top, mid, bottom = p.rows(p.area, 0.45, 1.15, 0.6)
    c = p.box(top, "Our design loop")
    c.timeline(c.content, [("1", "Goals", "what the game needs"), ("2", "Sketch + CAD", "Onshape layouts"),
                           ("3", "Simulate", "same code, desktop sim"), ("4", "Build", "print, cut, assemble"),
                           ("5", "Test + change", "back to step 2")])
    l, r = p.cols(mid, 1.1, 1)
    s = p.box(l, "Example: from sketch to part")
    s.labelled(s.content.inset(0.5 * G, 1.2 * G), TR / "transition_ball_path_sketch_dimensions.png",
               "Dimensioned layout sketch of the pollen path through the transition",
               labels=[(0.12, 0.8, "pollen", 0.5, 0.96), (0.52, 0.18, "belt spacing", 0.35, -0.02)],
               caption="Layout sketch first: pollen size, roller sizes and belt spacing (mm)")
    m = p.box(r, "One robot, many branches")
    m.text(m.content, ["Each subsystem was coded on its own branch: **intake** (Tina X.), **shooter** (Jemima C.), "
                       "then merged into one robot on **25 October**.",
                       m.head("What merging taught us"),
                       "- Two branches each hid the other's subsystem: fixed",
                       "- The shot table divided by zero at its first point: fixed and tested",
                       "- Units were mixed (RPM, ticks, degrees): one unit per value now"])
    v = p.box(bottom, "Ideas we brought in")
    v.story(v.content, [("From VEX", "Ethan B., Will Q., Ryan T. and Tina X. played VEX **Push Back**. The game was "
                                     "very similar, so our matchloader follows the same idea (page 10)."),
                        ("From last season", "Swerve and logging carried over; the turret did not (page 9).")])


def p05_strategy(doc):
    p = doc.page("Strategy and requirements")
    top, mid, bottom = p.rows(p.area, 0.45, 1.0, 0.3)
    g = p.box(top, "How we play")
    g.text(g.content, ["<our scoring plan: what we score first, where we shoot from, our role with the alliance "
                       "partner>",
                       "Pollen collects along the wall, so we collect there and shoot from there."])
    r = p.box(mid, "Requirements, and how the robot meets each", accent=True)
    r.table(r.content, [["We need to", "Why", "Our answer"],
                        ["Shoot from anywhere", "fewer trips across the field", "moving hood + shot table"],
                        ["Shoot quickly, again and again", "less waiting between shots", "two flywheels"],
                        ["Shoot without turning round", "pollen collects along the wall", "rear-facing shooter"],
                        ["Aim while driving", "save time every cycle", "swerve + auto-aim"],
                        ["Hold our spot", "defence will push us", "swerve X-lock"],
                        ["Load the flower fast", "<why>", "matchloader"],
                        ["Find pollen and the goal", "drive and aim without guessing", "front + rear cameras"]],
            col_weights=[1.25, 1.35, 1.25])
    s = p.box(bottom, "Scouting")
    s.text(s.content, ["Cooper C. and Jemima C. scout: <what we record and how it changes our plan>"])


# ---------------------------------------------------------------- 6-10: the robot
def p06_robot(doc):
    p = doc.page("Robot overview")
    top, bottom = p.rows(p.area, 1.55, 1)
    o = p.box(top, "Our robot")
    o.labelled(o.content.inset(2.5 * G, 0.6 * G), RB / "robot_iso.png", "Line drawing of the whole robot",
               labels=[(0.55, 0.12, "shooter", 0.85, 0.0), (0.86, 0.5, "swerve pod", 0.93, 0.3),
                       (0.14, 0.6, "intake", 0.02, 0.3), (0.45, 0.45, "transition", 0.25, 1.0)])
    l, r = p.cols(bottom, 1.1, 1)
    s = p.box(l, "Pollen path")
    s.picture(s.content, RB / "robot_side_section_ball_path.png", "Side section of the robot showing the pollen path",
              "In at the front, up the transition, out of the rear shooter")
    k = p.box(r, "Numbers", accent=True)
    k.table(k.content, [["Item", "Value"], ["Length (CAD)", "407.7 mm"], ["Width (CAD)", "327.0 mm"], ["Height (CAD)", "290.9 mm"],
                        ["Motors", "8"], ["Servos", "8"], ["Cameras", "2"]], col_weights=[1, 1])


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
        "- **X-lock:** the wheels turn inwards, so defence finds us much harder to push",
        "- Full-grip wheels: more **speed and pushing power** than mecanum",
        "- **Aim while driving:** drive one way, face the goal",
        "- We built swerve last season, so the risk was low",
        k.head("Key features"),
        "- **4 pods**, each with a drive motor and a steering servo",
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
    t.table(t.content, [["Test", "Result", "Status"], ["Top speed", "<RESULT: m/s>", "NOT TESTED"],
                        ["Pushed by another robot in X-lock", "<RESULT: mm moved>", "NOT TESTED"]],
            col_weights=[1.6, 1.2, 1], status_col=2)


def p08_intake(doc):
    p = doc.page("Intake and transition")
    top, mid, bottom = p.rows(p.area, 0.85, 1.25, 0.95)
    it = p.box(top, "What we tried")
    it.iterations(it.content, [
        ("V1 printed funnels", None, "", ["<what worked>"], ["gecko wheels at the front only", "<what went wrong>"]),
        ("V2 rollers + transition", None, "", ["mecanum rollers sweep pollen in", "gecko wheels carry it up"],
         ["<downside, if any>"])])
    l, r = p.cols(mid, 1.2, 1)
    d = p.box(l, "Pollen path")
    d.labelled(d.content.inset(0.5 * G, 1.5 * G), TR / "transition_side_ball_path_highlight.png",
               "Side view of the transition with the pollen path highlighted",
               labels=[(0.1, 0.55, "mecanum rollers", 0.15, 0.0), (0.38, 0.38, "gecko wheels", 0.6, 0.0),
                       (0.55, 0.78, "pollen guide", 0.8, 1.0)],
               caption="Rollers pull pollen in; gecko wheels lift it to the shooter")
    k = p.box(r, "Key sizes", accent=True)
    k.text(k.content, ["- Pollen **71.12 mm**",
                       "- Intake mecanum rollers **50 mm**",
                       "- Gecko wheels **48 mm**",
                       "- Small gecko wheels **32 mm** at the top, so less **backspin** goes into the shooter",
                       "- Belt spacing **45, 58.5, 54, 44 mm**",
                       "- 2 motors drive the intake and transition"])
    l, r = p.cols(bottom, 1.2, 1)
    m = p.box(l, "Maths: where the pollen touches")
    m.text(m.content, ["Our two rows of gecko wheels sit apart, so each row meets the pollen off its centre. The "
                       "sketch plane cuts the pollen in a circle of **70.413 mm**:",
                       "**d = √(35.56² − 35.21²) = 5.0 mm**",
                       "So the plane is 5.0 mm from the pollen's centre, and the sketch uses 70.413 mm there, not 71.12 mm."])
    s = p.box(r, "Sensing")
    s.text(s.content, ["- **3 beam sensors** (bottom, middle, top) count the pollen we hold",
                       "- A **gate servo** holds pollen until the shooter is ready",
                       "- Jam rate: <RESULT: jams per 20 pickups>"])


def p09_shooter(doc):
    p = doc.page("Shooter design")
    top, mid, bottom = p.rows(p.area, 0.95, 1.0, 0.42)
    it = p.box(top, "What we tried")
    it.iterations(it.content, [
        ("Turret, last season", None, "", ["aims without turning the robot"], ["months of tuning (Apr-Jun 2026)"]),
        ("Turret, this season", TU / "turret_iso_rotation_highlight.png",
         "Line drawing of this season's turret design with the turntable highlighted", ["what we wanted first"],
         ["weight and space", "1 more motor or servo", "no time to build it"]),
        ("Fixed rear shooter", SH / "shooter_iso_rear_a.png", "Line drawing of the fixed rear shooter we built",
         ["fewer parts", "shoots out of the flowers without turning"], ["the whole robot must turn to aim"])])
    l, r = p.cols(mid, 1, 1.15)
    w = p.box(l, "What we wanted, and why", accent=True)
    w.text(w.content, [
        "- **Two flywheels:** more flywheel means **less waiting** between shots",
        "- **Moving hood:** shoot from anywhere on the field",
        "- **Facing backwards:** pollen collects along the wall, so we drive up to the wall and aim, instead of "
        "collecting and then turning round",
        w.head("What we changed"),
        "The turret got as far as CAD and code, never built. On **12 October** we removed it: the swerve base turns "
        "the robot to aim instead (page 13)."])
    d = p.box(r, "Hood drive")
    d.labelled(d.content.inset(0.5 * G, 1.5 * G), SH / "shooter_side_hood_drive_highlight.png",
               "Side line drawing of the shooter with the hood drive highlighted",
               labels=[(0.6, 0.42, "hood rack", 0.42, 0.0), (0.72, 0.3, "servo gear", 0.9, 0.0),
                       (0.1, 0.3, "flywheel", 0.1, 0.0)],
               caption="A servo gear drives a rack to tilt the hood")
    t = p.box(bottom, "Tests")
    t.table(t.content, [["Test", "Result", "Status"], ["Shots in from 3 distances", "<RESULT: in / 10>", "NOT TESTED"],
                        ["Time between shots", "<RESULT: s>", "NOT TESTED"]], col_weights=[1.6, 1.2, 1], status_col=2)


def p10_loader(doc):
    p = doc.page("Matchloader and cameras")
    top, bottom = p.rows(p.area, 1, 1.05)
    l, r = p.cols(top, 1, 1)
    m = p.box(l, "Matchloader", accent=True)
    m.story(m.content, [("Idea", "Four of us played VEX **Push Back**, a very similar game. We used the same kind "
                                 "of matchloader for the flower."),
                        ("Problem", "<what the matchloader fixes, with a number>"),
                        ("Result", "<RESULT: time to load the flower, s>")])
    b = p.box(r, "Blocker and gate")
    b.story(b.content, [("Blocker", "<what the blocker stops> (1 Axon Max servo)"),
                        ("Gate", "Stops pollen going into the shooter until the shot is ready (1 Axon servo).")])
    c = p.box(bottom, "Two cameras")
    l2, r2 = p.cols(c.content, 1.25, 1)
    c.labelled(l2, TR / "transition_side_cameras_highlight.png", "Side view with the two cameras highlighted",
               labels=[(0.05, 0.12, "front camera", 0.2, -0.02), (0.88, 0.12, "rear camera", 0.78, -0.02)])
    c.text(r2, ["- **Front camera:** finds pollen, so we can path to it",
                "- **Rear camera:** reads AprilTags, so we know where the goal is",
                "- Status: <tested on the robot?>"])


# ---------------------------------------------------------------- 11-15: control, software, aim, auto, tests
def p11_control(doc):
    p = doc.page("Control system")
    top, bottom = p.rows(p.area, 1.2, 1)
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
        ["Hood servo", "shooting from different distances", "sets the launch angle from our shot table"],
        ["Voltage and current checks", "brown-outs and stalled motors", "logged every loop"]],
        col_weights=[1.25, 1.35, 1.6])
    l, r = p.cols(bottom, 1, 1)
    o = p.box(l, "Odometry pod")
    o.labelled(o.content.inset(3.0 * G, 0), OD / "odom_pod_assembled_iso.png", "Line drawing of the odometry pod",
               labels=[(0.5, 0.3, "mounting plate", 0.3, 0.0), (0.57, 0.93, "odometry wheels", 0.97, 0.72)],
               caption="Designed in CAD; the code uses wheels + IMU for now")
    s = p.box(r, "Speed control")
    s.story(s.content, [("Challenge", "Each shot takes energy from the flywheels, and a slower wheel shoots short."),
                        ("Solution", "A **PIDF** controller holds the target speed; feedforward uses battery "
                                     "voltage, so a flat battery does not change the shot."),
                        ("Result", "<RESULT: speed drop and recovery time per shot>")])


def p12_software(doc):
    p = doc.page("Software and simulation")
    top, mid, bottom = p.rows(p.area, 0.55, 0.85, 0.75)
    a = p.box(top, "Same code on the robot and on a laptop", accent=True)
    a.table(a.content, [["Part", "What it holds", "Why"],
                        ["RobotCode", "behaviour: driving, aiming, shooting", "written once, used everywhere"],
                        ["TeamCode", "the real motors, servos and sensors", "only place that touches hardware"],
                        ["RobotSim", "simulated robot, field and pollen", "test before the robot is built"]],
            col_weights=[0.9, 1.6, 1.5])
    l, r = p.cols(mid, 1, 1)
    s = p.box(l, "Why we simulate")
    s.story(s.content, [("Challenge", "The robot was still being built, but the code needed testing."),
                        ("Solution", "The same TeleOp runs in our simulator on the official field CAD."),
                        ("Result", "Simulation: scores **3 of 3** for both alliances, also while moving.")])
    t = p.box(r, "Automated tests")
    t.text(t.content, ["- **24 desktop tests** pass (25 October 2026)",
                       "- They cover heading wrap, 10 ms loops, a lost heading sensor, manual turn override and "
                       "stop outputs",
                       "- Every loop is logged, so a run can be replayed"])
    n = p.box(bottom, "Risks and how we reduce them")
    n.table(n.content, [["Risk", "How we reduce it"],
                        ["Simulation is not the real robot", "calibrate hood travel, release point and wheel speed "
                                                             "before shooting for real: <RESULT: date>"],
                        ["Heading sensor lost mid-match", "tested in simulation: the robot stops driving and stops feeding pollen"],
                        ["Flat battery changes the shot", "feedforward scaled by battery voltage"],
                        ["A complex turret fails", "no turret: the drivetrain aims"]], col_weights=[1, 1.9])


def p13_aim(doc):
    p = doc.page("Auto-aim")
    top, mid, bottom = p.rows(p.area, 0.55, 1.0, 0.4)
    s = p.box(top, "The problem")
    s.story(s.content, [("Challenge", "We dropped the turret, so the shooter faces backwards and cannot turn on "
                                      "its own."),
                        ("Solution", "Holding the aim button turns the **whole robot** until it is within "
                                     "**2.5 degrees** of the goal; the driver can still drive.")])
    l, r = p.cols(mid, 1, 1)
    h = p.box(l, "Maths: turning to aim")
    h.text(h.content, ["Turn speed = **feedback** on the heading error + **damping** + **feedforward** for a goal "
                       "that moves as we drive + a small push past **static friction**.",
                       "Gains in our code: kP 4.0, kD 0.35, kS 0.06.",
                       "In simulation aiming first stopped **12 degrees** short: small commands were inside the "
                       "static friction dead zone. Adding voltage feedforward fixed it."])
    v = p.box(r, "Maths: shooting while moving")
    v.text(v.content, ["The pollen leaves with the shooter's speed **plus the robot's**:",
                       "**v pollen = v shot + v robot + turn rate × r**",
                       "(r = where the pollen leaves, from the robot's centre). The solver aims so the sum hits the goal, and the shot "
                       "table picks flywheel speed and hood angle from the distance."])
    t = p.box(bottom, "Tests")
    t.table(t.content, [["Test", "Simulation", "Robot"], ["Score while still", "3 of 3", "<RESULT: in / 10>"],
                        ["Score while moving", "3 of 3", "<RESULT: in / 10>"]], col_weights=[1.4, 1, 1.2])


def p14_auto(doc):
    p = doc.page("Autonomous")
    top, bottom = p.rows(p.area, 1.5, 1)
    r = p.box(top, "Our route", accent=True)
    r.text(r.content, ["<auto route drawing: the team's hand-drawn route, redrawn cleanly>"])
    l, rr = p.cols(bottom, 1, 1)
    s = p.box(l, "Each step")
    s.table(s.content, [["Step", "What", "Points"], ["1", "<step>", "<pts>"], ["2", "<step>", "<pts>"],
                        ["3", "<step>", "<pts>"]], col_weights=[0.6, 2, 0.8])
    st = p.box(rr, "Status")
    st.text(st.content, ["- The autonomous for this robot is **not written yet**: NOT TESTED",
                         "- It will use the rear camera's AprilTags to know where we are",
                         "- <date we plan to have it running>"])


def p15_tests(doc):
    p = doc.page("Testing and lessons")
    top, mid, bottom, foot = p.rows(p.area, 0.95, 0.85, 0.4, 0.11)
    t = p.box(top, "Test results")
    t.table(t.content, [["Test", "Result", "Status"],
                        ["24 automated code tests", "all pass", "PASS"],
                        ["Simulation: score 3 of 3, still and moving", "3 of 3", "PASS"],
                        ["Robot: shots in from 3 distances", "<RESULT>", "NOT TESTED"],
                        ["Robot: top speed", "<RESULT>", "NOT TESTED"],
                        ["Robot: jams per 20 pickups", "<RESULT>", "NOT TESTED"],
                        ["Autonomous", "<RESULT>", "NOT TESTED"]], col_weights=[2, 1, 1], status_col=2)
    l, r = p.cols(mid, 1, 1)
    a = p.box(l, "Lessons we applied")
    a.text(a.content, ["- A turret cost months last season, so we let the drivetrain aim",
                       "- Sketch the pollen path before CAD: sizes and spacing first",
                       "- One unit for each value in code (RPM, radians)"])
    b = p.box(r, "Next")
    b.text(b.content, ["- Calibrate the shooter on the real robot",
                       "- Write and test the autonomous",
                       "- <next design change>"])
    c = p.box(bottom, "Reliability")
    c.text(c.content, ["Matches played: <number>. Matches the robot worked all match: <number>. "
                       "Faults and fixes: <list>"])
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
        print(doc.save_versioned(DELIVERABLE, DELIVERABLE, sys.argv[1] if len(sys.argv) > 1 else "first version"))
