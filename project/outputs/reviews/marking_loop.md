# Marking loop: FTC portfolio (11143 Barker Yellowbacks)

Rubric: FTC Competition Manual section 6 award criteria (`project/brief/ASSESSMENT.md`). **There are no mark bands**:
judges deliberate. The verdicts and the mark out of 100 below are my judgement, using `general/guides/RUBRIC_GUIDE.md`
for what "strong" looks like. Not a FIRST score.

## Round 1: portfolio_v01 (2026-11-05)

| Award | Verdict | Evidence (page) | Main gap |
|---|---|---|---|
| Think (R: process, lessons, comparing choices, maths) | partly to strong | process 4; turret iterations 9; intake iterations 8; maths 8 and 13; lessons 15 | no scored comparison of drivetrains or intakes; V1 intake reason missing |
| Control (R: parts, problem each solves, sensors) | partly | parts table 11; aim and speed control 11, 13; software 12 | nothing tested on the robot; autonomous not written; camera status unknown |
| Innovate (R: development, creative mechanism, reliable; E: risks) | partly | rear shooter + whole-robot aim 9, 13; transition sketch 4, 8 | no risk table; reliability not shown |
| Design (R: elegant, efficient, maintainable; E: reasons, fits strategy) | partly | overview 6; reasons 5, 7, 9 | nothing on build or maintenance (swap a pod, print time); strategy text missing |
| Inspire (R: contender in all, inclusive, every member) | partly | team 1; outreach 3 | outreach numbers missing; no photos of people or outreach |

**Estimate: 52 / 100 (range 45-60)**, mostly held back by `<RESULT>` placeholders (53 left) and the missing
outreach numbers, which only the team can supply.

### [Critical] Invented pro on intake V1
- Location: page 8, "What we tried", V1 printed funnels: "+ simple to print".
- Evidence: not in the logs; I added it. Fix: replace with a placeholder. Who: **Claude** (fixed in v02).

### [High] Unsupported absolute claim about X-lock
- Location: page 7. "defence cannot push us off our spot" is untested. Fix: "much harder to push", with the test row
  kept as NOT TESTED. Who: **Claude** (fixed in v02).

### [High] "24 tests run on every change" not shown
- Location: page 12. The report says 24 desktop tests pass on 25 Oct 2026; nothing shows they run on every change.
  Fix: say what was shown. Who: **Claude** (fixed in v02).

### [High] No risks and how they were reduced (Innovate, encouraged)
- Location: none. Fix: a risk table on page 12 from the logged evidence (uncalibrated shooter, turret complexity,
  lost heading sensor, brown-outs, mixed units). Who: **Claude** (added in v02; likelihoods left to the team).

### [High] No real-robot results (Control, Think, Design)
- Location: pages 7, 8, 9, 13, 15 (`<RESULT: ...>`). Fix: run the tests in the tables and fill in the numbers.
  Who: **You**.

### [High] Autonomous route missing
- Location: page 14. Fix: the hand-drawn route (photo into the inbox), then I redraw it. Who: **You**.

### [High] Outreach numbers and dates
- Location: page 3. Fix: students, sessions, dates, people. Who: **You**.

### [Medium] No scored comparison of options
- Location: pages 7 and 8 give reasons but no decision matrix. Fix: the team's scores for swerve / mecanum / tank and
  for the intakes. Who: **You**.

### [Medium] Strategy and scouting text
- Location: page 5 "How we play", "Scouting"; `<why>` for the matchloader. Who: **You** (Will Q., Chloe S.).

### [Medium] Design award: build and maintenance
- Location: none. Fix: how long a pod takes to swap, printed vs machined parts, part count. Who: **You**.

### [Medium] Photos of people (Inspire)
- Location: pages 1 and 3 have initials only. Fix: team and outreach photos into the inbox. Who: **You**.

### [Low] Wording that overstates small points
- Page 6 header said "(CAD)" over counts from the parts list; page 1 "2 leads" (one strategy lead); page 8 "the wheel
  spacing is set from 70.413 mm"; page 11 "the next shot falls short"; page 12 "real field CAD" (it is the official
  field CAD). Who: **Claude** (fixed in v02).

### [Low] Label wraps onto a caption
- Page 4 sketch label "pollen 71.12 mm" wraps and touches the caption. Who: **Claude** (fixed in v02).

## Round 2: portfolio_v02 (2026-11-05)
All **Claude** items from round 1 are fixed (invented pro removed, X-lock and test claims softened, risk table on
page 12 from logged evidence, wording, label). Also corrected while checking the code: a lost heading sensor makes
the robot **stop driving and feeding** (simulation test `lostHeadingSensorStopsDriveAndFeeding`).
Hand-in check: pages, A4, fonts, size 2.5 MB and AI words pass; **placeholders fail (53, on purpose)**; the 51 runs
under 10 pt are the 7.3 pt bullet squares, not words; no upload deadline in PROJECT.md.

**Estimate: 55 / 100 (range 48-62)**, judgement. Only **You** items are left. Most marks first:
1. Real-robot results for every `<RESULT>` (shots in from 3 distances, time between shots, top speed, X-lock push,
   jams per 20 pickups, aim error): Think, Control, Design, Innovate.
2. The autonomous route drawing and what each step scores: Control.
3. Outreach numbers and dates (page 3) and photos of people: Inspire.
4. A scored comparison for drivetrain and intake options: Think.
5. Strategy text ("How we play", scouting, why the matchloader): Design, Think.
6. Build and maintenance facts (pod swap time, part count, printed vs bought): Design.
7. Intake V1: what worked and what went wrong; V2 downsides: Think.
8. Blocker: what it stops; camera status on the robot; meeting times and how decisions are made.

## Round 3: portfolio_v03 (2026-11-05)
- From QUESTIONS.md 1-20: **the robot is not built yet**, so every robot test now reads "not built yet" with status
  NOT TESTED, and no line suggests a built robot (the shooter drawing's alt text said "we built"; fixed). Outreach,
  meetings and decision-making filled in; build-dates table dropped (no dates). Meeting notes added: X-lock friction,
  efficiency, polycarbonate ramps (thickness still to confirm), lookup table from localisation (values still to be
  measured), keeping the robot light.
- Hand-in check: 17 placeholders left (pages 5, 8, 10, 14, 15), all team items; everything else passes.
- **Estimate: 57 / 100 (range 50-63)**, judgement. Up from 55: Inspire evidence is now real (Darkinjung awards,
  1,500 people from 32 countries). Held back mostly because nothing can be tested before the robot is built: Control
  and Design judges look for a working, reliable robot.
- Left for the team: QUESTIONS.md 21-74 (strategy, option scores, intake V1, blocker, auto route, subsystems).

## Round 4: portfolio_v06 (2026-11-06)
- More evidence shown, none invented. Stronger: Control (order of checks before a shot, limits in code, parts table),
  Think (bugs and fixes, sketch to CAD, code milestones), Design (chassis, parts breakdown).
- **Estimate: 62 / 100 (range 55-68)**, judgement. Still held back by no real robot, the auto route, strategy text, option
  scores and photos. Mismatches to settle: lookup table vs solver, X-lock not in code (QUESTIONS 75, 76).
