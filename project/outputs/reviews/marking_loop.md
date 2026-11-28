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

## Round 5: portfolio_v35 (2026-11-12)
Marked against the FTC award criteria in `project/brief/ASSESSMENT.md`. FTC has no mark bands (judges deliberate), so
the verdicts use `general/guides/RUBRIC_GUIDE.md` for what "strong" means. The number is a judgement, not a score.

| Award | Verdict | Evidence |
|---|---|---|
| Think | strong | design loop and CAD process (p4); "Choices we compared" on every subsystem page (p7-13); turret iterations (p9); maths for aiming and shooting while moving (p13); lessons and code fixes (p15) |
| Control | strong, partly proven | parts table with the problem each part solves (p11); checks before every shot (p13); simulator and 24 tests (p12); sensors used for feedback (beam sensors, IMU, angle sensors, cameras); robot results on p7-9 and p13, but few tries are counted |
| Innovate | partly | flower mechanism idea from VEX (p10) has no picture; shooting while moving (p13) and the shared robot/simulator code (p12) are the most original parts |
| Design | partly | small frame, 6.5 kg, 3-minute pod swap, CAD views and exploded views (p6-9); no photo of the real robot anywhere |
| Inspire | strong | every member on p1 with a photo and roles; outreach with numbers (p3); season goals (p2) |

**Estimate: 70 / 100 (range 64-76)**, judgement. Up from 62 (v06): real robot results, strategy, the auto route,
team photos and choice tables. Held back by no real-robot photos, results with no count of tries and one
contradiction (solver or lookup table).

### [High] No photo of the real robot or the build
- Location: whole portfolio (every robot picture is CAD). Evidence: the robot is built and tested (p7-9, p13), but a
  judge cannot see it. Fix: 2-4 photos (whole robot, intake or pod close-up, build day) into `assets/inbox/`; they go on
  p6 and p8. Who: **You**.

### [High] Solver or lookup table: the pages disagree
- Location: p13 "Choices we compared" (gravity solver instead of a lookup table) and p15 fix row ("Lookup table divided
  by zero"). The 10 Oct meeting notes say a lookup table from localisation; the code has both. Fix: say which one the
  robot uses for matches, then one row changes. Who: **You**.

### [High] Results with no count of tries
- Location: p9 "all but 1 went in" (out of how many?), p8 "1 jam" (in how many pickups?), p14 "very consistent" (how
  many runs, how many points?), p7 X-lock push (by what?). Fix: the numbers behind each. Who: **You**.

### [Medium] Speed control result shows the problem, not the fix
- Location: p11 Speed control, Result. Evidence: "drops by about 200 encoder ticks" is the challenge. Fix: put the
  drop in Challenge and link the result to the measured shots on p9. Who: **Claude** (still needs **You**: recovery
  time and the unit of the 200 ticks).

### [Medium] Parts table leaves out the intake motors
- Location: p11 "What each part does". Evidence: p8 says two motors drive the intake and transition; p11 lists 6 of the
  8 motors. Fix: add the row. Who: **Claude**.

### [Medium] Risks table ignores the robot results
- Location: p15 "Risks and how we reduce them" (4 rows, room for more). Fix: add defence (X-lock, tested), jams
  (reverse rollers, tested) and holding too much pollen (beam sensors stop at 4, rule G407). Who: **Claude**.

### [Medium] Two fixes on the same 12-degree bug read differently
- Location: p13 says the aim stopped short because of static friction; p15 says the fix was battery-voltage
  feedforward. Fix: one wording that has both (kS push past static friction, scaled by battery voltage). Who: **Claude**.

### [Low] Vague line on the swerve page
- Location: p7 "We move more efficiently, which is a big advantage in a match". Fix: use the measured 250 cm/s
  (about 1.5 s to cross the field). Who: **Claude**.

### [Low] Autonomous total reads as a result
- Location: p14 "Total 45" is the plan. Fix: "Planned total". Who: **Claude** (the real score needs **You**).

### [Low] Choices show only the upside
- Location: p7-13 "Why" columns. Judges like the cost of each choice too (swerve costs 4 servos and more code; a fixed
  shooter means the whole robot turns). Fix: one short cost per row from the team. Who: **You**.

### [Low] Flower mechanism has no picture
- Location: p10. Fix: a CAD screenshot or photo of the flower mechanism. Who: **You**.

## Round 6: portfolio_v36 (2026-11-12)
All **Claude** items from round 5 are fixed: intake motors in the parts table (p11, all 8 motors now listed), speed
control Result points to the measured shots (p11), measured top speed with the sum (p7), "Planned total" (p14), three
risks from the robot tests and one wording for the 12-degree fix (p15). Layout checks pass; hand-in check 0 FAIL,
1 WARN (no upload deadline in PROJECT.md); no placeholders; tests 50 pass.

**Estimate: 72 / 100 (range 66-77)**, judgement. Only **You** items are left. Most marks first:
1. Photos of the real robot and the build (Design, Innovate, Control). Still to add.
2. Solver or lookup table: which the robot uses in matches (p13 and p15 disagree; Think, Control). Still to add.
3. Tries behind each result: shots (p9), jams (p8), auto runs and points (p14), X-lock push (p7). Still to add.
4. Unit and recovery time of the 200-tick drop (p11). Still to add.
5. One cost for each choice (p7-13 Why columns; Think). Still to add.
6. A picture of the flower mechanism (p10; Innovate). Still to add.
7. Confirm the p15 wording "a push past static friction (kS), scaled by battery voltage" against the code.

## Round 7: portfolio_v37 (2026-11-12)
Re-marked after the mentor's feedback (design process on the robot, impact of outreach). FTC has no mark bands; the
verdicts use `general/guides/RUBRIC_GUIDE.md` and the number is a judgement.

| Award | Verdict | Change since v36 |
|---|---|---|
| Think | strong | up: page 4 now shows each loop step on the shooter, intake and code, with page links to the evidence |
| Control | strong, partly proven | same: results still lack a count of tries |
| Innovate | partly | same: flower mechanism has no picture |
| Design | partly | same: no photo of the real robot |
| Inspire | strong | up: page 3 has numbers (20+ students, about 15 sessions), outcomes (own teams, first competitions, awards) and what outreach did for us |

**Estimate: 75 / 100 (range 69-80)**, judgement. No new **Claude** items: the text is consistent across pages
(the 12-degree fix reads the same on pages 4, 13 and 15) and the style and hand-in checks pass.

### [Medium] "Test + change" shows the tests but not the change
- Location: page 4 table, row 5. The intake has a fix (reverse the rollers); the shooter (all but 1 in) and the code
  (2 of 3 while moving) show no change after testing. Judges reading the loop look for the "change" half. Fix: one
  thing changed (or planned) after each test. Who: **You**.

### [Low] Impact on the Maliyan team is a feeling, not a result
- Location: page 3, "Mentoring and volunteering" ("very rewarding to watch the students flourish"). Fix: one result
  (a competition, an award, a skill they now have). Who: **You**.

### [Low] No photo or quote from Darkinjung
- Location: page 3. Fix: a session photo or a one-line quote from a student or teacher. Who: **You**.

**You list, most marks first:** (1) real-robot photos; (2) solver or lookup table (pages 13 and 15 disagree);
(3) tries behind each result; (4) what changed after each test (page 4, row 5); (5) unit and recovery time of the
200 ticks; (6) one cost for each choice; (7) flower mechanism picture; (8) a Maliyan result and a Darkinjung photo or
quote.

## Round 8: portfolio_v46 (2026-11-28)
Judgement against the FTC award criteria (no mark bands). Since round 7 (v37) the team and other sessions added the
Wollongong debrief, counter rollers, the new auto-aim, swerve code and simulator; this round added labels and a sketch.

| Award | Verdict | Evidence |
|---|---|---|
| Think | strong | Think Award at Wollongong; design loop on the robot (p4); debrief problem, cause, change (p2, p15); counter roller maths (p9); choices tables |
| Control | strong | parts table (p11), swerve code steps (p11), odometry + camera + Kalman filter + aim vector (p13), simulator (p12); counts of tries still thin |
| Innovate | partly to strong | counter roller sketch (p9), aim 0.4 s ahead (p13), our own simulator interface (p12) |
| Design | partly | annotated CAD on every subsystem page; still no photo of the real robot |
| Inspire | strong | team (p1), outreach numbers and impact (p3) |

**Estimate: 79 / 100 (range 73-84)**, judgement. No Claude items left. **You**, most marks first:
1. Photos of the real robot (whole robot, counter rollers, swerve pod). Still to add.
2. How many runs behind "3-4 in 4" (p9), "very consistent" auto (p14) and "2 of 3 while moving" (p13). Still to add.
3. Confirm the Macquarie goals (p2, drafted from the debrief) and the counter roller gear ratio (p9).
4. Which step happens where on the auto path picture (p14), so the steps can be numbered on it.

## Round 9: portfolio_v49 (2026-11-28)
The teammate's v48 adds a stronger Wollongong debrief (why each problem happened), V1-V4 shooter versions, the blocker
plan and an honest 'running now' column for the autonomous. With the labelled counter roller CAD and sketch:
**estimate 81 / 100 (range 75-85)**, judgement. Still You: real-robot photos; tries behind 3-4 in 4 and 'very
consistent'; confirm the Macquarie goals and the counter roller gearing.
