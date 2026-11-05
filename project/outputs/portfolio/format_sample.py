"""Format sample for the team to check the look before the real pages: the cover plus 4 pages.

    python project/outputs/portfolio/format_sample.py          # saves format_sample_vNN.pptx beside this file
    python general/tools/export_pdf.py project/outputs/portfolio/format_sample_vNN.pptx --render project/outputs/renders/format_sample_vNN

Not the portfolio: a sample of every building block in the Yellowbacks style. Facts come from the code report
(Pinkbacks branch Isaac, doc/isaac-integration.md, 25 Oct 2026), git dates and the user's answers (2026-11-05).
Anything not measured on the robot is a <RESULT: ...> or <...> placeholder.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_portfolio import LW, TEAM, TEAM_NAME, cover  # noqa: E402
from portfolio_style import (BG, CON, G, LINE, MUTED, PRO, TEXT, YELLOW, Portfolio, Rect,  # noqa: E402
                             write)
from design_system import _shape  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import MSO_ANCHOR  # noqa: E402

ENDNOTE = ("Endnote: text drafted and laid out with help from an AI assistant. All results, photos, CAD, code and "
           "decisions are the team's own; the team checked every page.")


def format_guide(doc):
    p = doc.page("Format guide")
    top, mid, bottom = p.rows(p.area, 1.0, 1.25, 0.42)
    l, r = p.cols(top, 1, 1.25)
    c = p.box(l, "Colours")
    sw = [(BG, "Page", "171616"), ("F2F2F2", "Text", "F2F2F2"), (YELLOW, "Yellow", "F5E660"),
          (MUTED, "Grey", "C4C4C4"), (PRO, "Pro / pass", "6FD98B"), (CON, "Con / fail", "FF7B72")]
    cr = c.content
    rh = (cr.h - 5 * 0.5 * G) / 6
    for i, (hexc, name, code) in enumerate(sw):
        y = cr.y + i * (rh + 0.5 * G)
        _shape(p.slide, MSO_SHAPE.RECTANGLE, Rect(cr.x, y, 2.6 * G, rh), hexc, LINE, 0.75)
        c.write(Rect(cr.x + 3.4 * G, y, cr.w - 3.4 * G, rh), [f"**{name}**  #{code}"], anchor=MSO_ANCHOR.MIDDLE)
    t = p.box(r, "Type")
    t.text(t.content, [
        {"text": "BANNER TITLE 19 PT BOLD CAPS", "size": 19, "bold": True, "after": 3},
        {"text": "BOX HEADING 12 PT BOLD CAPS", "size": 12, "bold": True, "after": 3},
        t.head("Sub-heading 11.5 pt yellow"),
        "Body 10.5 pt Montserrat, with **key words in yellow**, ++pros in green++ and ~~cons in red~~.",
        "- Bullets are small yellow squares",
        {"text": "Captions, tables and footer 10 pt grey (the smallest size: FTC A201)", "size": 10, "colour": MUTED,
         "after": 3},
        {"text": "Handwritten labels 15 pt", "size": 15, "font": "Caveat Static", "bold": True, "colour": YELLOW}])
    l, r = p.cols(mid, 1, 1.1)
    s = p.box(l, "Challenge to solution")
    s.story(s.content, [
        ("Challenge", "In simulation the chassis stopped aiming about **12 degrees** short: small wheel commands "
                      "were inside the static friction dead zone."),
        ("Solution", "Added wheel feedforward based on battery voltage."),
        ("Result", "Simulation aims on target. Real robot: <RESULT: aim error in degrees>.")])
    ra, rb = p.rows(r, 0.8, 1)
    o = p.box(ra, "Options compared")
    o.table(o.content, [["Drivetrain", "Score /25", "Status"], ["Swerve", "<score>", "CHOSEN"],
                        ["Mecanum", "<score>", "NOT CHOSEN"], ["Tank", "<score>", "NOT CHOSEN"]],
            col_weights=[1.3, 1, 1.2], status_col=2)
    it = p.box(rb, "Iterations")
    it.iterations(it.content, [("V1", None, "", ["<pro>"], ["<con>"]), ("V2", None, "", ["<pro>"], ["<con>"]),
                               ("V3", None, "", ["<pro>", "<pro>"], [])])
    tl = p.box(bottom, "Season so far (from our code history)")
    tl.timeline(tl.content, [("23 Sep", "Shooter code", "first shooter files"),
                             ("20 Oct", "Intake code", "intake and transfer"),
                             ("25 Oct", "One robot", "subsystems merged; 3 of 3 in sim"),
                             ("12 Nov", "Wollongong", "first event")])


def swerve(doc):
    p = doc.page("Swerve drivetrain")
    top, mid, bottom = p.rows(p.area, 1.3, 1.1, 0.4)
    l, r = p.cols(top, 1.1, 1)
    d = p.box(l, "One swerve pod")
    d.labelled(d.content.inset(2.2 * G, 0.6 * G), LW / "swerve" / "swerve_pod_exploded_iso_a.png",
               "Exploded line drawing of one swerve pod",
               labels=[(0.46, 0.1, "angle sensor", 0.0, 0.06), (0.5, 0.33, "steering gears", 0.98, 0.22),
                       (0.62, 0.53, "frame plates", 1.0, 0.44), (0.22, 0.68, "drive motor", -0.03, 0.55),
                       (0.62, 0.82, "bevel gear", 1.03, 0.7), (0.47, 0.86, "wheel", 0.02, 0.97)])
    k = p.box(r, "Key features", accent=True)
    k.text(k.content, [
        "- **4 pods**, each with a drive motor and a steering servo",
        "- An **absolute angle sensor** in every pod, so each wheel knows where it points from the start",
        "- Pod centres **239 x 239 mm** apart; wheels **60.9 mm**",
        "- Robot **407.7 x 327.0 mm**, **290.9 mm** tall (CAD)",
        k.head("Why swerve, again"),
        "- **X-lock:** the wheels turn inwards, so defence cannot push us off our spot",
        "- Full-grip wheels: more **speed and pushing power** than mecanum",
        "- **Aim while driving:** drive one way, face the goal",
        "- We built swerve last season, so the risk was low"])
    l, r = p.cols(mid, 1, 1)
    a = p.box(l, "Wheel drive")
    a.labelled(a.content.inset(1.5 * G, 0), LW / "swerve" / "swerve_geartrain_wheel_drive_iso_highlight.png",
               "Gear train that drives the wheel, highlighted",
               labels=[(0.15, 0.42, "drive motor", 0.08, 0.12), (0.58, 0.28, "gears", 0.92, 0.06),
                       (0.43, 0.8, "bevel gears", 0.1, 0.97), (0.82, 0.78, "wheel", 1.0, 0.95)],
               caption="Motor, gears, then a bevel gear turn the wheel")
    b = p.box(r, "Module rotation")
    b.labelled(b.content.inset(1.5 * G, 0), LW / "swerve" / "swerve_geartrain_module_rotation_iso_highlight.png",
               "Gear train that turns the pod, highlighted",
               labels=[(0.28, 0.42, "ring gear", 0.02, 0.08), (0.76, 0.26, "steering gears", 0.9, 0.04),
                       (0.17, 0.66, "wheel fork", 0.04, 0.9), (0.55, 0.88, "wheel", 0.98, 0.9)],
               caption="Servo and ring gear turn the whole pod")
    t = p.box(bottom, "Tests")
    t.table(t.content, [["Test", "Result", "Status"], ["Top speed", "<RESULT: m/s>", "NOT TESTED"],
                        ["Steering angle error", "<RESULT: degrees>", "NOT TESTED"]],
            col_weights=[1.4, 1.2, 1], status_col=2)


def shooter(doc):
    """Design process example (feedback 2026-11-05: show why, not only what)."""
    p = doc.page("Shooter design")
    top, mid, bottom = p.rows(p.area, 0.85, 1.0, 0.42)
    it = p.box(top, "What we tried")
    it.iterations(it.content, [
        ("Turret, last season", None, "", ["aims without turning the robot"],
         ["months of tuning (Apr-Jun 2026)"]),
        ("Turret, this season", None, "", ["what we wanted first"],
         ["weight and space", "1 more motor or servo", "no time to build it"]),
        ("Fixed rear shooter", LW / "shooter" / "shooter_iso_rear_a.png",
         "Line drawing of the fixed rear shooter (the one we built)", ["fewer parts", "shoots out of the flowers without turning"],
         ["the whole robot must turn to aim"])])
    l, r = p.cols(mid, 1, 1.15)
    w = p.box(l, "What we wanted, and why", accent=True)
    w.text(w.content, [
        "- **Two flywheels:** more flywheel means **less waiting** between shots",
        "- **Moving hood:** shoot from anywhere on the field",
        "- **Facing backwards:** balls collect along the wall, so we drive up to the wall and aim, instead of "
        "collecting and then turning round",
        w.head("What we changed"),
        "We drew and coded a turret, but never built it. On **12 October** we removed it: the swerve base turns "
        "the robot to aim instead (auto-aim, page 4)."])
    d = p.box(r, "Hood drive")
    d.labelled(d.content.inset(0.5 * G, 1.5 * G), LW / "shooter" / "shooter_side_hood_drive_highlight.png",
               "Side line drawing of the shooter with the hood drive highlighted",
               labels=[(0.6, 0.42, "hood rack", 0.42, 0.0), (0.72, 0.3, "servo gear", 0.9, 0.0),
                       (0.1, 0.3, "flywheel", 0.1, 0.0)],
               caption="A servo gear drives a rack to tilt the hood")
    t = p.box(bottom, "Tests")
    t.table(t.content, [["Test", "Result", "Status"], ["Shots in from 3 distances", "<RESULT: in / 10>", "NOT TESTED"],
                        ["Time between shots", "<RESULT: s>", "NOT TESTED"]], col_weights=[1.6, 1.2, 1], status_col=2)


def control(doc):
    p = doc.page("Control system")
    top, bottom = p.rows(p.area, 0.9, 1.0)
    m = p.box(top, "What each part does")
    m.table(m.content, [
        ["Part", "Problem it solves", "What it does"],
        ["4 drive motors", "moving in any direction", "drive each swerve wheel"],
        ["4 steering servos + 4 angle sensors", "pointing every wheel the right way", "turn each pod and read its angle"],
        ["IMU", "knowing which way we face", "heading for driving and aiming"],
        ["3 beam sensors", "knowing how many balls we hold", "sense balls at bottom, middle and top of the intake"],
        ["Gate servo", "balls reaching the shooter too early", "holds balls until the shot is ready"],
        ["2 shooter motors", "the same shot every time", "flywheel held at target speed (PIDF)"],
        ["Hood servo", "shooting from different distances", "sets the launch angle from our shot table"],
        ["Voltage and current checks", "brown-outs and stalled motors", "logged every loop"]],
        col_weights=[1.25, 1.35, 1.6])
    l, r = p.cols(bottom, 1, 1)
    o = p.box(l, "Odometry pod")
    o.labelled(o.content.inset(3.0 * G, 0), LW / "odometry" / "odom_pod_assembled_iso.png",
               "Line drawing of the odometry pod",
               labels=[(0.5, 0.3, "mounting plate", 0.3, 0.0), (0.57, 0.93, "odometry wheels", 0.97, 0.72)],
               caption="In CAD; the code uses wheels + IMU for now")
    s = p.box(r, "Auto-aim")
    s.story(s.content, [
        ("Challenge", "We dropped the turret, so the shooter is fixed facing backwards."),
        ("Solution", "Holding aim turns the whole robot until it is within **2.5 degrees** of the goal."),
        ("Result", "Simulation: **3 of 3** scored, also while moving. Robot: <RESULT: shots in / 10>.")])


def team(doc):
    p = doc.page("Meet the team")
    top, mid, foot = p.rows(p.area, 2.7, 0.66, 0.12)
    members = [("Ethan B.", "Lead design", "assembly"), ("Brandon L.", "CAD", "assembly"),
               ("Isaac H.", "Lead code", "CAD, assembly"), ("Ryan T.", "Driver", "CAD"),
               ("Will Q.", "Lead strategy", "drive coach"), ("Ivy W.", "Programming", "HR"),
               ("Tina X.", "Code", "assembly"), ("Chelsea W.", "Code", "assembly"),
               ("Chloe L.", "Electrical", "assembly"), ("Chloe S.", "Strategy", "code, assembly"),
               ("Cooper C.", "Scouting", "assembly"), ("Jemima C.", "Programming", "scouting"),
               ("Lucas T.", "CAD", "assembly")]
    t = p.box(top, "Our team")
    t.team(t.content, [(n, r, None, note) for n, r, note in members], cols=2)
    o = p.box(mid, "Outreach")
    o.text(o.content, [
        "- **7 members** teach robotics to Darkinjung students once a fortnight (<number> students since <month>)",
        "- Ethan B. and Isaac H. mentor <number> VEX teams",
        "- Ethan B., Isaac H. and Brandon L. volunteered at the Barker VEX competition (<date>)",
        "- We ran the robotics part of the Round Square International Conference at Barker (<date>, <number> people)"])
    write(p.slide, foot, [{"text": ENDNOTE, "size": 10, "colour": MUTED, "after": 0}], sizes=p.sizes)


def build():
    doc = Portfolio(TEAM, TEAM_NAME)
    cover(doc)
    format_guide(doc)
    swerve(doc)
    shooter(doc)
    control(doc)
    team(doc)
    return doc


if __name__ == "__main__":
    doc = build()
    if "--draft" in sys.argv:
        print(doc.save(sys.argv[-1]))
    else:
        print(doc.save_versioned("portfolio", "format_sample", sys.argv[1] if len(sys.argv) > 1 else "format sample"))
