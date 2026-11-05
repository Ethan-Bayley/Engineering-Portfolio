# Page plan: FTC portfolio, 11143 Barker Yellowbacks (draft 1, 2026-11-05)

Cover + 15 A4 portrait pages (A201.B). Awards: Inspire (I), Think (T), Control (C), Innovate (N), Design (D).
Evidence keys: **code** = Pinkbacks branch `Isaac` and `doc/isaac-integration.md`; **you** = your answers
(PREFERENCES.md, 2026-11-05); **inbox** = assets you are about to drop in. `<RESULT: ...>` = real-robot number still
needed (the hand-in check fails until it is filled).

| Page | Title | Awards | What goes on it | Evidence | Status |
|---|---|---|---|---|---|
| Cover | Engineering Portfolio | (not judged) | team number, name, school, Barker Robotics, full-size robot line drawings | cover, inbox line drawings | layout done; needs full-size drawings |
| 1 | Meet the team | I | 13 team cards (name, role), how roles are split (design, CAD, code, strategy, assembly), how we meet and decide | you; team photo (inbox) | needs team/head-shot photos |
| 2 | Our season | I T | timeline Sept-Nov 2026 (code history dates, build dates), planned against actual | git history of Pinkbacks, BUILD_LOG | needs build dates / schedule |
| 3 | Outreach and community | I | Darkinjung students fortnightly (7 members), VEX mentoring, Barker VEX competition volunteers, Round Square conference robotics | you; photos (inbox) | needs dates and numbers (students, sessions, teams) |
| 4 | How we engineer | T | our design cycle (strategy -> CAD -> simulate -> build -> test), git branches per subsystem merged into one robot, lessons from last season (background only, A201.E) | code (branch/merge history) | ready to draft |
| 5 | Strategy and requirements | T D | what we score, where we shoot from, requirements each mechanism must meet | strategy (skipped for now) | **needs strategy from Will Q. / Chloe S.** |
| 6 | Robot overview | D | labelled line drawing; size 407.7 x 327.0 x 290.9 mm; subsystem list; motor and servo count | code (CAD geometry), Onshape views | needs Onshape capture |
| 7 | Swerve drivetrain | N T D | why swerve (compared with mecanum and tank, scored table), 4 pods, goBILDA motors + super servos, 239 x 239 mm module spacing, 60.9 mm wheels, calculated top speed (marked calculated) | you, code, CAD | needs pod photos/CAD; real speed `<RESULT>` |
| 8 | Intake and transition | N D | vector + gecko wheels linked to the transition, 2 motors, 3 beam sensors count balls, gate servo; iterations | you, code, photos | needs versions tried and why changed |
| 9 | Shooter and hood | N T | 2-motor wheel, PIDF speed control, Axon Max hood, shot lookup table; maths: launch angle and speed from distance | code, photos | real shots in per 10 `<RESULT>` |
| 10 | Matchloader, blocker and gate | N D | Push Back-style matchloader for the flower, blocker, gate (3 Axon servos); challenge -> solution for each | you, photos/CAD | needs what each one fixed |
| 11 | Control system map | C | every motor, servo and sensor: the challenge it solves and its function (table + wiring sketch); control hub / expansion hub | code (hardware names) | ready to draft |
| 12 | Software and simulation | C N | shared code runs on the robot and in our simulator; logging and replay; battery and motor-current health checks; 24 automated tests | code | ready to draft |
| 13 | Auto-aim and shooting on the move | C T | rear shooter, so the chassis turns to aim (heading PD + feedforward, 2.5 degree tolerance); shot solver allows for robot speed; maths shown | code | sim results only; real `<RESULT>` |
| 14 | Autonomous | C | your auto route, redrawn cleanly; what each step scores; status | hand-drawn route (inbox) | **route not written in code yet: marked untested** |
| 15 | Testing and lessons learned | T C | test table (sim and real), the bugs found and fixed while merging (lessons applied), what we change next; AI-credit endnote | code report, TESTS.md | real results `<RESULT>` |

## Notes
- Nothing from before 1 January 2026 except as background (A201.E). Last season's DECODE autos (June-July 2026,
  `ball-tracking-greyvision`) are in-season dates but a different robot: at most one line on page 4.
- No links or QR codes for judges (A201); the code repo is named, not linked.
- Connect, Reach and Sustain are not targeted, but page 3 also helps Reach.
- Page 5 can merge into page 4 if strategy stays empty, freeing a page for CAD iterations.

## Design process on every mechanism page (feedback, 2026-11-05)
Judges want to know **why**, not only what is there. Each mechanism page (7-10, 13) gets: what we wanted (goals),
what we tried (iterations with pros and cons), what we changed and why, then tests. Stories so far: turret (last
season, then CAD + code this season, removed 12 Oct 2026) -> fixed rear shooter; intake (printed funnels with gecko
wheels at the front -> vector + gecko wheels linked to the transition); shooter and hood goals; matchloader from VEX
Push Back (Ethan B., Will Q., Ryan T., Tina X.). Shown in `outputs/portfolio/format_sample_v02` page 3.
