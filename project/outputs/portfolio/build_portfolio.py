"""Build the FTC portfolio for 11143 Barker Yellowbacks (2026-27, BIOBUZZ): the cover plus up to 15 pages.

    python project/outputs/portfolio/build_portfolio.py "what changed"      # saves portfolio_vNN.pptx
    python project/outputs/portfolio/build_portfolio.py --draft x.pptx
    python general/tools/export_pdf.py project/outputs/portfolio/portfolio_vNN.pptx --render project/outputs/renders/vNN
    python general/tools/hand_in_check.py --deliverable portfolio --max-pages 16 --max-mb 15 --min-pt 10

Look: project/design/PORTFOLIO_STYLE.md (the team's cover, colours tightened). FTC A201: cover (team number; not
judged) + at most 15 pages, nothing under 10 pt, first names and last initials only, work since 1 January 2026.
Text drafted from the team's logs, meeting notes and answers (project/logs/, NEXT_STEPS.md, QUESTIONS.md) and the code report (Pinkbacks branch
Isaac, doc/isaac-integration.md); AI credit endnote on page 15 (A201). Results are the team's own (reported 2026-11-11); anything not measured on the robot is a
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
def choices(p, rect, rows):
    """'Choices we compared' (user, 2026-11-11): what we chose, what we chose it over and why. Only options the team has
    told us about are filled in; <...> marks what the team still has to tell us."""
    c = p.box(rect, "Choices we compared")
    c.table(c.content, [["Choice", "We chose", "Instead of", "Why"]] + rows, col_weights=[0.75, 1.1, 0.95, 2.8])
    return c


def needs(p, rect, text):
    """'What it needs to do' at the top of each subsystem page (user, 2026-11-28)."""
    n = p.box(rect, "What it needs to do", accent=True)
    n.text(n.content, [text])
    return n


def p01_team(doc):
    p = doc.page("Meet the team")
    top, bottom = p.rows(p.area, 1.5, 1)
    # one column per subteam, lead at the top (user, 2026-11-11): the grid fills row by row, so the lists run across
    design = [("Brandon L.", "Lead assembly", "electrical, design"), ("Ethan B.", "Assembly", ""),
              ("Ryan T.", "CAD", "driver"), ("Lucas T.", "CAD", "assembly")]
    code = [("Isaac H.", "Lead programming", "electrical, design, manufacturing"), ("Ivy W.", "Programming", "HR"),
            ("Tina X.", "Programming", "strategy, scouting, assembly"), ("Jemima C.", "Programming", "scouting")]
    strat = [("Will Q.", "Lead strategy", "drive coach"), ("Chelsey W.", "Scouting", "assembly"),
             ("Chloe L.", "Scouting", "electrical, assembly"), ("Chloe S.", "Strategy", "scouting, assembly")]
    members = [m for row in zip(design, code, strat) for m in row]
    t = p.box(top, "Our subteams")
    head_h = 2.4 * G
    heads, grid = t.content.y, None
    hr = Rect(t.content.x, t.content.y, t.content.w, head_h)
    gr = Rect(t.content.x, t.content.y + head_h + 0.5 * G, t.content.w, t.content.h - head_h - 0.5 * G)
    cw = (hr.w - 2 * 0.6 * G) / 3
    for k, title in enumerate(["Design and assembly", "Programming", "Strategy and scouting"]):
        c = Rect(hr.x + k * (cw + 0.6 * G), hr.y, cw, hr.h)
        _shape(p.slide, MSO_SHAPE.RECTANGLE, c, FILL, None, 0)
        write(p.slide, c, [{"text": title.upper(), "size": 10, "bold": True, "colour": FILL_TEXT,
                            "align": PP_ALIGN.CENTER, "after": 0}], anchor=MSO_ANCHOR.MIDDLE, sizes=p.sizes)
    t.team(gr, [(n, r, PHOTOS / f"team_{n.lower().replace('.', '').replace(' ', '_')}.jpg", note)
                for n, r, note in members], cols=3)
    l, r = p.cols(bottom, 1.1, 1)
    h = p.box(l, "How we split the work")
    h.text(h.content, [
        "- **CAD:** four of us worked on the CAD, mostly at the start of the season. Once the design was done we "
        "joined assembly so the build went faster",
        "- **Code:** four of us wrote the basic structure of the code and our simulator. We were ready to test "
        "as soon as the robot was finished, and we kept the work moving steadily",
        "- **Strategy:** three of us planned our strategy. We worked together on autonomous routes that suit our "
        "robot and the alliances we are likely to play with. Five of us scout",
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
    top, deb, bottom = p.rows(p.area, 205, 330, 180)
    tl = p.box(top, "2026-2027 season timeline")
    r1, r2 = p.rows(tl.content, 1, 0.8)
    tl.timeline(r1, [("15 Sep", "Schedule", "everyone adds when they are free"),
                     ("18 Sep", "First meeting", "subteams chosen"),
                     ("10 Oct", "Refocus", "turret cut"),
                     ("26 Oct-1 Nov", "Swerve built", "goBILDA parts arrive"),
                     ("13 Nov", "Wollongong", "Think Award")])
    tl.timeline(r2, [("29 Nov", "Macquarie", "second event"),
                     ("5-6 Dec", "Macquarie", "nationals"),
                     ("28 Apr-1 May", "Worlds", "if we qualify")], dashed=True)
    d = p.box(deb, "Wollongong debrief: 6 matches, 2 wins, 3 losses, 1 tie, 7th of 10, Think Award", accent=True)
    d.table(d.content, [["Problem", "Cause", "What we changed"],
                        ["Shooter backspin: 1 in 4 shots went in", "no counter rollers",
                         "rebuilt the shooter with counter rollers geared to the flywheel: now 3-4 in 4 (page 9)"],
                        ["Brownouts and electrical issues", "poor coordination of which batteries we used",
                         "batteries numbered and charged in rotation; all wiring redone for room and easier "
                         "debugging; every connector hot-glued"],
                        ["High friction in our subsystems", "belts and pods turning stiffly",
                         "WD-40 and new belt sizes in the transition; silicone grease in the swerve pods"],
                        ["No autonomous", "not written in time", "we wrote and ran our route (page 14)"]],
            col_weights=[1.15, 1.05, 2.0])
    l, r = p.cols(bottom, 1, 1)
    g = p.box(l, "Goals for Macquarie")
    g.text(g.content, ["- Qualify for nationals",
                       "- Run our autonomous every match",
                       "- Keep 3-4 in 4 shots in matches",
                       "- No brownouts"])
    s = p.box(r, "Our season goals")
    s.text(s.content, ["- Win nationals and qualify for the FTC World Championship",
                       "- Be a strong contender for the Design, Control and Innovate awards",
                       "- Keep teaching Darkinjung students and spread FIRST"])


def p03_outreach(doc):
    p = doc.page("Outreach and impact")
    top, a_r, mid, bottom = p.rows(p.area, 0.34, 1.2, 1.5, 0.85)
    stats(p, top, [("20+", "Darkinjung students taught"), ("About 15", "sessions since February 2026"),
                   ("1,500+", "people at Round Square"), ("32", "countries at Round Square")])
    a = p.box(a_r, "Teaching Darkinjung students", accent=True)
    a.story(a.content, [("What", "Six of us (Ethan B., Brandon L., Chloe S., Ivy W., Ryan T. and Will Q.) have run "
                                 "**about 15 sessions** for **over 20 Darkinjung students**, once a fortnight since "
                                 "February 2026."),
                        ("What they learn", "They built robots for this year's **VEX IQ** game and learnt how to "
                                            "build, how to code, how to do interviews and how to write portfolios."),
                        ("Impact", "Students from our sessions formed their own teams and competed for the first "
                                   "time. With our help they won **Skills**, **Teamwork Champion** and "
                                   "**Excellence** awards.")])
    d = p.box(mid, "Round Square International Conference")
    ds, dp = p.cols(d.content, 1.15, 1)
    d.picture(dp, PHOTOS / "round_square_rsic_2026.jpg",
              "Photo from above of our robotics showcase at the Round Square conference: fields, robots and visitors",
              "Our robotics showcase at Round Square")
    d.story(ds, [("What", "In the Term 2-3 holidays eight of us (Ivy W., Ethan B., Ryan T., Chelsey W., Chloe L., "
                          "Isaac H., Tina X. and Will Q.) ran the robotics part of the conference at Barker."),
                 ("Demos", "At the opening fair we showed robots driving, shooting, intaking and scoring."),
                 ("Impact", "**Over 1,500 people** from **32 countries** came. Many of them had not heard of FIRST "
                            "before.")])
    l, r = p.cols(bottom, 1, 1)
    b = p.box(l, "Mentoring and volunteering")
    b.text(b.content, ["Three of us (Ethan B., Isaac H. and Brandon L.) mentor the Darkinjung Maliyan VEX team. It "
                       "is very rewarding to watch the students flourish in their games and competitions.",
                       "On **14 November 2026** the same three refereed, queued teams and helped the Barker VEX "
                       "competition run smoothly."])
    c = p.box(r, "What outreach did for us", accent=True)
    c.text(c.content, ["- Teaching made us better at **explaining our robot** and why we made each choice, which "
                       "helps in judging interviews",
                       "- Planning lessons taught us to **lead a group**",
                       "- Round Square was very rewarding, and it was great to see so many people there"])


def p04_process(doc):
    p = doc.page("How we design")
    top, loop, mid, bottom = p.rows(p.area, 117, 300, 170, 140)
    c = p.box(top, "Our design loop")
    c.timeline(c.content, [("1", "Goals", "what the game needs"), ("2", "Sketch + CAD", "Onshape layouts"),
                           ("3", "Simulate", "same code, desktop sim"), ("4", "Build", "parts and assembly"),
                           ("5", "Test + change", "back to step 2")])
    t = p.box(loop, "How we used the loop on our robot", accent=True)
    t.table(t.content, [
        ["Step", "Shooter", "Intake and transition", "Code and auto-aim"],
        ["1 Goals", "launch from anywhere, quickly (page 5)", "hold 4 pollen (rule G407) with little backspin",
         "aim and shoot while we drive"],
        ["2 Sketch + CAD", "a turret first; on 10 Oct we cut it for a fixed rear shooter (page 9)",
         "the pollen path first, then the plates and belts (below)",
         "one behaviour code for the robot and the simulator (page 12)"],
        ["3 Simulate", "3 of 3 shots in, also while moving", "pick up 3, aim and score 3",
         "aiming stopped 12 degrees short, so we added a push past static friction"],
        ["4 Build", "a flywheel, a moving hood and a gate", "polycarbonate ramps; 32 mm gecko wheels at the top",
         "subsystems merged on 25 Oct; the bugs it showed are fixed"],
        ["5 Test + change", "backspin: 1 in 4 shots; counter rollers made it 3-4 in 4", "no jams in 20 pickups; WD-40 and new belts",
         "on the robot: 3 of 3 while still, 2 of 3 while moving (page 13)"]],
        col_weights=[0.8, 1.3, 1.3, 1.3])
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
                       "Tina X. wrote the intake and Jemima C. wrote the shooter. Merging on **25 October** showed "
                       "bugs that only appear when subsystems meet, such as mixed units (RPM, ticks, degrees)."])
    v = p.box(r, "Ideas from VEX and last season")
    v.text(v.content, ["Four of us (Ethan B., Will Q., Ryan T. and Tina X.) competed in VEX **Push Back**. The match "
                       "loaders in that game worked well for getting pollen out, so we made our own version for the "
                       "flower (page 10).",
                       "Swerve and logging carried over from last season."])


def p05_strategy(doc):
    p = doc.page("Game and strategy")
    top, how, mid, tab, bottom = p.rows(p.area, 168, 110, 116, 234, 86)
    g = p.box(top, "What scores points (manual, Table 10-2)")
    g.table(g.content, [["Scoring action", "Points", "Our answer"],
                        ["HIVE TIP, by launching into the upward cell", "20 in auto and 20 in teleop",
                         "shooter, hood and auto-aim"],
                        ["Pollen left in an upward cell at the end", "2 each", "the same launches"],
                        ["Pollen in a flower we own", "2 each", "we do not do this: too few points"],
                        ["Park, at least partly in our loading zone", "5 in auto and 5 in teleop",
                         "we park in our loading zone"]],
            col_weights=[1.6, 1.1, 1.2])
    h = p.box(how, "How we play")
    h.text(h.content, ["- We score pollen to maximise our ranking points (RP)",
                       "- We need to outscore other teams to maximise our output",
                       "- We cycle fast and stay robust",
                       "- We want a simple robot that we can make quickly"])
    c = p.box(mid, "One scoring cycle")
    c.timeline(c.content, [("1", "Collect", "until we hold 4"), ("2", "Hold aim", "robot turns to the goal"),
                           ("3", "Spin up", "flywheel and hood reach target"), ("4", "Settle", "ready for 0.1 s"),
                           ("5", "Feed", "pollen goes to the shooter")])
    r = p.box(tab, "Requirements, and how the robot meets each", accent=True)
    r.table(r.content, [["We need to", "Why", "Our answer"],
                 ["Launch from anywhere", "fewer trips across the field", "moving hood"],
                 ["Launch the same way every time", "backspin spoils shots", "counter rollers geared to the flywheel"],
                 ["Launch without turning round", "pollen collects along the wall", "rear-facing shooter"],
                 ["Aim while driving", "save time every cycle", "swerve and auto-aim"],
                 ["Hold our spot", "defence will push us", "swerve X-lock"],
                 ["Avoid defence", "defenders will chase us", "very small frame perimeter"],
                 ["Empty the flower", "pollen sits inside it", "flower mechanism"],
                 ["Find the goal", "aim without guessing", "rear camera reads AprilTags"]],
            col_weights=[1.25, 1.35, 1.25])
    s = p.box(bottom, "Scouting")
    s.text(s.content, ["Jemima C., Chelsey W., Chloe L., Tina X. and Chloe S. scout. Scouting shows us what other "
                       "teams' robots can and cannot do. We use it to choose alliance partners whose strengths cover our "
                       "weaknesses and to plan how we play each match."])


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
                       "- A **light robot**, 6.5 kg, so it moves more efficiently"])
    c = p.box(bottom, "Chassis")
    l, r = p.cols(c.content, 1.1, 1)
    c.picture(l, LW / "chassis" / "chassis_exploded_iso.png", "Exploded line drawing of the chassis and swerve pods",
              "Exploded view: pods, plates and side panels")
    c.picture(r, LW / "chassis" / "chassis_bottom.png", "Line drawing of the underside of the chassis",
              "Underneath: a pod in each corner")


def p07_swerve(doc):
    p = doc.page("Swerve drivetrain")
    nd, top, ver, mid, ch, bottom = p.rows(p.area, 64, 200, 117, 125, 106, 102)
    needs(p, nd, "Move any way, turn the whole robot to aim while driving, and hold our spot.")
    l, r = p.cols(top, 1.1, 1)
    d = p.box(l, "One swerve pod")
    d.labelled(d.content.inset(2.2 * G, 0.4 * G), SW / "swerve_pod_exploded_iso_a.png",
               "Exploded line drawing of one swerve pod",
               labels=[(0.46, 0.1, "angle sensor", 0.0, 0.06), (0.5, 0.33, "steering gears", 0.98, 0.22),
                       (0.62, 0.53, "frame plates", 1.0, 0.44), (0.22, 0.68, "drive motor", -0.03, 0.55),
                       (0.62, 0.82, "bevel gear", 1.03, 0.7), (0.47, 0.86, "wheel", 0.02, 0.97)])
    k = p.box(r, "Our pods")
    k.text(k.content, [
        "- A drive motor and a steering servo in each pod",
        "- We can swap a pod in **3 minutes**",
        "- An **absolute angle sensor** in every pod",
        "- **X-lock:** wheels in an X, so we are much harder to push",
        "- Top speed **250 cm/s**: across the 3.6 m field in about 1.5 s",
        "- Silicone grease after Wollongong, so the pods turn more freely"])
    v = p.box(ver, "Our swerve versions")
    v.timeline(v.content, [("2022", "First swerve", "by Rory, a former member"),
                           ("2025-2026", "Last season", "our own swerve"),
                           ("2026-2027", "This season", "custom machined pods")])
    l, r = p.cols(mid, 1, 1)
    a = p.box(l, "Wheel drive")
    a.labelled(a.content.inset(1.5 * G, 0), SW / "swerve_geartrain_wheel_drive_iso_highlight.png",
               "Gear train that drives the wheel, highlighted",
               labels=[(0.15, 0.42, "drive motor", 0.08, 0.12), (0.58, 0.28, "gears", 0.92, 0.06),
                       (0.43, 0.8, "bevel gears", 0.1, 0.97), (0.82, 0.78, "wheel", 1.0, 0.95)])
    b = p.box(r, "Module rotation")
    b.labelled(b.content.inset(1.5 * G, 0), SW / "swerve_geartrain_module_rotation_iso_highlight.png",
               "Gear train that turns the pod, highlighted",
               labels=[(0.28, 0.42, "ring gear", 0.02, 0.08), (0.76, 0.26, "steering gears", 0.9, 0.04),
                       (0.17, 0.66, "wheel fork", 0.04, 0.9), (0.55, 0.88, "wheel", 0.98, 0.9)])
    choices(p, ch, [["Drivetrain", "Swerve", "Mecanum",
                     "X-lock makes us much harder to push. Full-grip wheels give more speed and pushing power. We can "
                     "drive one way while facing the goal"]])
    t = p.box(bottom, "Tests on the robot")
    t.table(t.content, [["Test", "Result", "Status"], ["Top speed", "250 cm/s", "TESTED"],
                        ["Pushed while in X-lock", "it did not move", "TESTED"]],
            col_weights=[1.6, 1.2, 1], status_col=2)


def p08_intake(doc):
    p = doc.page("Intake and transition")
    nd, top, mid, ch, bottom = p.rows(p.area, 64, 272, 150, 128, 100)
    needs(p, nd, "Pick up pollen quickly, hold up to 4 (rule G407) and pass it up to the shooter without backspin.")
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
                       "- We hold up to **4 pollen**, the most rule G407 allows",
                       "- After Wollongong: **WD-40** and new belt sizes so it spins freely"])
    a = p.box(mid, "Assembly")
    l2, r2 = p.cols(a.content, 1, 1)
    a.picture(l2, TR / "transition_iso.png", "Line drawing of the intake and transition assembly",
              "The intake and transition together")
    a.picture(r2, TR / "transition_front.png", "Front line drawing of the intake and transition",
              "From the front")
    choices(p, ch, [["Top wheels", "32 mm gecko wheels", "48 mm gecko wheels", "Less backspin goes into the shooter"],
                    ["Ramps", "Polycarbonate", "3D printed ramps", "A low-friction surface for the pollen"]])
    t = p.box(bottom, "Tests on the robot")
    t.table(t.content, [["Test", "Result", "Status"], ["Intake jams", "no jams in 20 pickups", "TESTED"]],
            col_weights=[1.6, 1.2, 1], status_col=2)


def p09_shooter(doc):
    p = doc.page("Shooter design")
    nd, top, mid, ch, bottom = p.rows(p.area, 64, 158, 248, 146, 98)
    needs(p, nd, "Launch pollen into the upward cell the same way every time, from anywhere on the field.")
    it = p.box(top, "What we tried")
    it.iterations(it.content, [
        ("Turret 2025-26", None, "", ["aims without turning"], ["months of tuning"]),
        ("Turret 2026-27", TU / "turret_iso_rotation_highlight.png",
         "Line drawing of this season's turret design with the turntable highlighted", [],
         ["weight and space", "no time"]),
        ("Fixed shooter", SHL, "Exploded line drawing of our fixed rear shooter", ["fewer parts"],
         ["backspin"]),
        ("Counter rollers", None, "", ["no backspin", "3-4 in 4 shots in"], [])])
    l, r = p.cols(mid, 0.9, 1.25)
    w = p.box(l, "Why a fixed rear shooter")
    w.text(w.content, ["- No turret: time for the swerve and a consistent robot",
                       "- Less fixing at competitions, so more reliable",
                       "- Quicker to assemble, so time for other things",
                       "- Swerve makes the **whole robot a moving turret**",
                       "- X-lock holds us in place while we shoot"])
    c = p.box(r, "Counter roller shooter (after Wollongong)", accent=True)
    c.story(c.content, [("Problem", "Backspin: **1 in 4** shots went in."),
                        ("Fix", "A **63.5 mm** flywheel and **2 counter rollers** (27 mm) at the back, geared so their "
                                "surfaces match. Now **3-4 in 4** shots go in per run."),
                        ("Maths", "Same surface speed, so the rollers spin **63.5 ÷ 27 ≈ 2.35×** faster.")
                        ])  # team result (3-4 in 4), 2026-11-28
    choices(p, ch, [
        ["Aiming", "A fixed shooter (page 13)", "A turret",
         "Short on time and parts, so we cut the least necessary part"],
        ["Hood", "A moving hood", "A fixed hood", "Shoot from anywhere: 33.6 to 67 degrees"],
        ["Backspin", "Counter rollers", "No counter rollers", "Backspin cost us shots at Wollongong"]])
    t = p.box(bottom, "Tests on the robot")
    t.table(t.content, [["Test", "Result", "Status"], ["Shots in per run of 4", "1 in 4 before; 3-4 in 4 now", "TESTED"]],
            col_weights=[1.6, 1.4, 0.8], status_col=2)


def p10_loader(doc):
    p = doc.page("Flower, gate, camera")
    nd, top, mid, bottom, ch = p.rows(p.area, 64, 248, 150, 147, 105)
    needs(p, nd, "Get pollen out of the flower, hold it until the shot is ready and find the goal.")
    l, r = p.cols(top, 1.3, 1)
    m = p.box(l, "Flower mechanism", accent=True)
    m.story(m.content, [("Inspiration", "Another team's **match loader** design in VEX **Push Back** got pollen out of "
                                        "a container quickly."),
                        ("Our version", "Four of us competed in Push Back, so we used that experience to design our "
                                        "own version for the flower."),
                        ("Result", "It empties the flower really well, in under a second.")])
    b = p.box(r, "Gate")
    b.text(b.content, ["The gate stops pollen going into the shooter until the shot is ready. It uses 1 Axon servo."])
    c = p.box(mid, "Rear camera")
    c.text(c.content, ["- One camera, on the back, running **PhotonVision**",
                       "- It reads the AprilTags so we know where we are and where the goal is (page 13)",
                       "- It works on the robot"])
    h = p.box(bottom, "How we hold and release pollen")
    l3, r3 = p.cols(h.content, 1, 1.4)
    h.picture(l3, TR / "transition_front.png", "Front line drawing of the intake and transition")
    h.text(r3, ["- **Collect:** the intake pulls in up to 4 pollen",
                "- **Hold:** pollen waits while the robot aims",
                "- **Release:** pollen only feeds once aim, flywheel speed and hood have all been ready for "
                "**0.1 s**"])
    choices(p, ch, [["Flower mechanism", "Our own version of a Push Back match loader", "Side vertical intake wheels",
                     "Match loaders were proven at getting pollen out of a container"]])


# ---------------------------------------------------------------- 11-15: control, software, aim, auto, tests
def p11_control(doc):
    p = doc.page("Control system")
    top, code, bottom = p.rows(p.area, 340, 184, 190)
    m = p.box(top, "What each part does")
    m.table(m.content, [
        ["Part", "Problem it solves", "What it does"],
        ["4 drive motors", "moving in any direction", "drive each swerve wheel"],
        ["4 steering servos + 4 angle sensors", "pointing every wheel the right way", "turn each pod and read its angle"],
        ["IMU", "knowing which way we face", "heading for driving and aiming"],
        ["4 odometry pods", "knowing where we are on the field", "averaged to track our position"],
        ["Rear camera (PhotonVision)", "finding the goal", "reads AprilTags to correct our position"],
        ["2 intake motors", "moving pollen in and up", "drive the rollers and the gecko wheels"],
        ["2 shooter motors", "the same shot every time", "flywheel and counter rollers held at target speed"],
        ["Gate servo", "pollen reaching the shooter too early", "holds pollen until the shot is ready"],
        ["Hood servo", "shooting from different distances", "sets the launch angle"],
        ["Flower mechanism servo", "pollen stuck inside the flower", "empties the flower"]],
        col_weights=[1.25, 1.35, 1.6])
    s = p.box(code, "How our swerve code works (the same logic FRC teams use in WPILib)", accent=True)
    s1, s2 = p.rows(s.content, 1.25, 0.5)
    s.timeline(s1, [("1", "Driver input", "forward, sideways and turn speed"),
                    ("2", "Kinematics", "work out each pod's wheel speed and angle"),
                    ("3", "Optimise", "turn the short way; reverse the wheel if needed"),
                    ("4", "Output", "servo angle and motor power to each pod")])
    s.text(s2, ["Optimising: if a pod would turn more than 90 degrees, it reverses its wheel instead, so it never turns more than 90."])
    l, r = p.cols(bottom, 0.9, 1.3)
    o = p.box(l, "Odometry pod")
    o.labelled(o.content.inset(1.2 * G, 0.6 * G), OD / "odom_pod_assembled_iso.png", "Line drawing of the odometry pod",
               labels=[(0.5, 0.3, "mounting plate", 0.15, 0.04), (0.57, 0.9, "odometry wheels", 0.85, 0.75)])
    sp = p.box(r, "Speed control")
    sp.story(sp.content, [("Challenge", "Each shot drops the flywheel by about **200 encoder ticks**; a slower wheel "
                                        "shoots short."),
                          ("Solution", "A **PIDF** controller with battery-voltage feedforward holds the target "
                                       "speed: **3-4 in 4** shots in per run (page 9).")])


def p12_software(doc):
    p = doc.page("Software and simulation")
    top, how, mid, ch = p.rows(p.area, 125, 258, 170, 150)
    a = p.box(top, "Same code on the robot and on a laptop", accent=True)
    a.table(a.content, [["Part", "What it holds", "Why"],
                        ["RobotCode", "behaviour: driving, aiming, shooting", "written once, used on both"],
                        ["TeamCode", "the real motors, servos and sensors", "only place that touches hardware"],
                        ["RobotSim", "simulated robot, field and pollen", "test without the robot"]],
            col_weights=[0.9, 1.6, 1.5])
    h = p.box(how, "How our simulator works")
    h.story(h.content, [("Interface", "Our code talks to the hardware through our own **hardware I/O interface**. On the "
                                      "robot it reads the real motors and sensors."),
                        ("Simulation", "On a computer the same interface **fakes the encoder ticks**, so our team code "
                                       "runs without the robot."),
                        ("Like FRC", "This is the same idea FRC teams use: a hardware map behind an I/O interface, with "
                                     "one version for the robot and one for simulation."),
                        ("Why", "We can run things like our **autonomous route** before we put it on the robot.")])
    l, r = p.cols(mid, 1, 1.3)
    t = p.box(l, "Automated tests")
    t.text(t.content, ["- **24 desktop tests** pass (25 October 2026)",
                       "- They cover heading wrap, 10 ms loops, a lost heading sensor and stop outputs",
                       "- Every loop is logged, so we can replay a run"])
    r_ = p.box(r, "What the simulator shows")
    r_.table(r_.content, [["Test (in simulation)", "Result", "Status"],
                          ["Pick up 3, aim and score 3", "3 of 3", "PASS"],
                          ["Score while still and moving", "3 of 3", "PASS"],
                          ["Lose the heading sensor", "stops driving", "PASS"]],
             col_weights=[2.0, 1.2, 0.8], status_col=2)
    choices(p, ch, [["Testing the code", "Our own simulator", "Waiting for the finished robot", "We can test the code now"],
                    ["Code structure", "One behaviour code with separate hardware code",
                     "Separate code for the robot and the simulator", "We write the behaviour once and use it on both"]])


def p13_aim(doc):
    p = doc.page("Auto-aim")
    loc, aim, ch, bottom = p.rows(p.area, 210, 285, 120, 99)
    l = p.box(loc, "Knowing where we are", accent=True)
    l.story(l.content, [("Odometry", "We average our **4 odometry pods** to track how far we have moved."),
                        ("Camera", "The rear camera images the **AprilTags** and solves our pose with trigonometry."),
                        ("Filter", "An **extended Kalman filter** checks which camera results are believable, then "
                                   "updates our pose from those.")])
    a, b = p.cols(aim, 1.45, 1)
    d = p.box(a, "Aiming: a vector from the goal")
    d.picture(d.content, A / "diagrams" / "auto_aim_vector.png",
              "Diagram: an aim vector runs from the goal to where the robot will be in 0.4 seconds; the robot turns so "
              "its rear shooter points along it")
    f = p.box(b, "Why 0.4 s ahead")
    f.text(f.content, ["We draw the aim vector from the goal to where the robot **will be 0.4 s from now**, not where "
                       "it is.",
                       "By the time we read the sensors and send a command, it is already a new loop. Aiming ahead "
                       "(feedforward) makes us **more accurate while moving**."])
    choices(p, ch, [["Working out the shot", "A lookup table of measured shots", "A gravity solver",
                     "A solver needs very advanced maths with many unknowns. We needed 3-4 in 4 shots in the time we had, "
                     "so measuring shots was our best answer"]])
    t = p.box(bottom, "Tests on the robot")
    t.table(t.content, [["Test", "Simulation", "Robot"], ["Score while still", "3 of 3", "3 of 3"],
                        ["Score while moving", "3 of 3", "2 of 3"]], col_weights=[1.4, 1, 1.2])


def p14_auto(doc):
    p = doc.page("Autonomous")
    l, r = p.cols(p.area, 1.6, 1)
    rt = p.box(l, "Our autonomous route", accent=True)
    rt.picture(rt.content, A / "auto" / "auto_path_team.png",
               "Our autonomous path drawn in yellow on the field: from the start to a flower, a curve to the "
               "shooting position, back to the flower, then to the loading zone",
               "Our autonomous path on the field")
    a, b2 = p.rows(r, 1.7, 0.9)
    s1 = p.box(a, "Each step")
    s1.table(s1.content, [["No.", "What we do", "Pts"],
                          ["1", "Shoot, causing a HIVE TIP", "20"],
                          ["2", "Get pollen from the flower", "0"],
                          ["3", "Go to the shooting position on the other side", "0"],
                          ["4", "Shoot", "0"],
                          ["5", "Collect pollen from the flower", "0"],
                          ["6", "Shoot, causing a HIVE TIP", "20"],
                          ["7", "Park in our loading zone", "5"],
                          ["", "Planned total", "45"]], col_weights=[0.8, 2.7, 1.0])
    st = p.box(b2, "Status")
    st.text(st.content, ["- We had no autonomous at Wollongong",
                         "- We have since written and run this route, and it is very consistent",
                         "- It uses the same position tracking as auto-aim (page 13)"])


def p15_tests(doc):
    p = doc.page("Lessons and risks")
    top, bot, foot = p.rows(p.area, 380, 280, 24)
    a = p.box(top, "Lessons and what we changed", accent=True)
    a.table(a.content, [["What we learned", "What we changed"],
                        ["A turret cost us months last season", "this season the drivetrain aims"],
                        ["Time ran short in October", "we cut the least necessary part and made the rest consistent"],
                        ["Backspin makes shots inconsistent", "counter rollers geared to the flywheel: 1 in 4 to 3-4 in 4"],
                        ["Brownouts came from not coordinating our batteries", "numbered batteries, charged in rotation"],
                        ["Vibration can pull connectors out in a match", "every connector is hot-glued"],
                        ["Messy wiring is hard to debug", "we redid all the wiring with more room"],
                        ["Friction slows our subsystems", "WD-40 and new belts in the transition; grease in the pods"],
                        ["Exams and outreach changed what a week could fit", "we plan each week around them"]],
            col_weights=[1.4, 1.5])
    n = p.box(bot, "Risks and how we reduce them")
    n.table(n.content, [["Risk", "How we reduce it"],
                        ["Simulation is not the real robot", "the code refuses to feed until the shooter is calibrated"],
                        ["Flat battery changes the shot", "feedforward scaled by battery voltage"],
                        ["Defence pushes us off our spot", "X-lock: pushed in testing, the robot did not move"],
                        ["Pollen jams in the intake", "no jams in 20 pickups in testing"],
                        ["A connector comes loose mid-match", "hot glue on every connector"]],
            col_weights=[1, 1.5])
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
