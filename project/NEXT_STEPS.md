# What comes next, and what we said in meetings

Context for every session on the portfolio (skill `portfolio-notes` reads and updates it). Two parts:
**A. Next steps** (what is left, in order), **B. Team notes** (what the team said in meetings, in their words,
with where it goes in the portfolio). Anyone can add to part B: say or type it, and Claude writes it here with the
date, then uses it on the pages. Notes are the team's words: Claude does not add facts, numbers or reasons to them.

- Event: FTC Wollongong, **Thursday 12 November 2026**. The portfolio is **printed** (user, 2026-11-06); earlier a PDF
  upload was recorded: **ask the Event Director** if an upload is also needed, and by when.
- Current version: `outputs/portfolio/portfolio_v06.pdf` (cover + 15 pages, option A; pictures in
  `outputs/portfolio/pages_v06/`). Marking review: `outputs/reviews/marking_loop.md` (57 / 100 on v03's content,
  judgement). **The robot is not built yet** (2026-11-05): every robot test shows "not built yet / NOT TESTED" until it is.

---

## A. Next steps

### Decide first (2026-11-06)
Look: **A chosen** (white, yellow bands), the default. Yellow: **keep #F5E660** (user, 2026-11-06). Both done.

### The team (most marks first)
**Easiest way: answer the questions in [QUESTIONS.md](QUESTIONS.md)** (77 questions, each tied to a page; 1-20 answered). The table below is the same work, grouped.

"Suggested" names come from the roles in PROJECT.md; change them as you like.

| # | What | Page | Suggested | Done |
|---|---|---|---|---|
| 1 | Real-robot tests: shots in from 3 distances (out of 10), time between shots (s), top speed (m/s), X-lock push (mm moved), jams per 20 pickups, aim error (degrees). Write each one down with the date and number of tries. | 7, 8, 9, 13, 15 | Ryan T., Will Q., Isaac H. | waiting: robot not built (the pages say so) |
| 2 | Photo of the hand-drawn autonomous route into `assets/inbox/`, plus what each step scores | 14 | Isaac H., Chloe S. | |
| 3 | Outreach: number of Darkinjung students and sessions and since when; VEX teams mentored; dates of the Barker VEX competition and Round Square conference; people reached | 3 | Ethan B. | partly, v03: Darkinjung and Round Square in; VEX mentoring and Barker comp numbers unknown |
| 4 | Photos: team, members, outreach (into `assets/inbox/`); page 3 has a frame waiting for them | 1, 3 | anyone | |
| 5 | Scores comparing swerve / mecanum / tank, and intake V1 / V2 (a decision matrix) | 7, 8 | Ethan B., Brandon L. | |
| 6 | Strategy: how we play, what scouting records, why the matchloader | 5, 10 | Will Q., Chloe S., Cooper C. | |
| 7 | Build and maintenance: robot mass, time to swap a pod, printed vs bought parts, part count | 6, 7 | Lucas T., Chloe L. | |
| 8 | Intake V1: what worked and what went wrong; any V2 downsides | 8 | Tina X. | |
| 9 | What the blocker stops; are the cameras working on the robot; when we meet and how we decide | 1, 10 | anyone | meetings and decisions done (v03); blocker and cameras open |
| 10 | Print one page of v06 (page 8 or 9): check the yellow and whether the edge bar reaches the paper's edge | | anyone | |
| 11 | Confirm the meeting notes in part B marked **check** | | Ethan B. | |

### Claude (when the team's items come in)
- v03 and v04 done (part B's notes, QUESTIONS.md 1-20, option A). Next version: new answers and any results.
- Redraw the autonomous route cleanly from the photo (same route, nothing added).
- Rerun the hand-in check and marking loop; save page images as `pages_vNN/`.
- Shared fixes to send to project-template: `hand_in_check.py` Windows console fix; `--deliverable` picks the
  wrong PDF when a format sample sits beside the portfolio. Pull the template's 2 newer files.

---

## B. Team notes (what we said in meetings)

### 2026-11-05 (spoken by the team, typed up by Claude)
| What the team said | Goes on | Status |
|---|---|---|
| We use **6 mm polycarbonate ramps** as a low-friction surface for the ball. | 8 (pollen path; maybe the curved guide in the drawing) | **check**: heard as "6 ml"; is the curved guide on page 8 the ramp? |
| **Gecko wheels** grip the ball. | 8 | ok |
| Motors: "any mark motors" (not clear in the recording). | 6, 11 | **check**: which motors? (earlier: goBILDA bare motors) |
| We chose a **swerve chassis** because it moves a lot more efficiently, which gives us a big advantage in competition. | 7 | ok |
| We first wanted a **turret shooter**, but because of **time restrictions** we could not build it, so we chose a **fixed shooter**. | 9 | ok (matches the 2026-11-05 answers) |
| The fixed shooter still has a **hood**, so we can adapt to wherever we are on the field and shoot from different places. | 9 | ok |
| A **lookup table** in our code tells the robot what flywheel speed and hood angle to use, depending on where **localisation** says it is, so it shoots accurately and efficiently. | 9, 13 | **check**: the code has the shot table, but on branch `Isaac` it has **no values yet** (`SHOT_VALUES = {}`); say "measured" only once it is filled (question 64) |
| **Weight saving:** we made the robot as light as possible so it moves more efficiently. | 6, 7 | needs a number: robot mass, or what we lightened |
| The ramp: the speaker did not know the details; "just say what we said in meetings". | | so nothing more is added about the ramp |

### 2026-11-05, later (typed by Ethan B.)
| What the team said | Goes on | Status |
|---|---|---|
| We also chose swerve for **X-lock**: the wheels are positioned in an X, which makes us a lot harder to defend or push because of the friction. | 7 | ok |

### Earlier answers (2026-11-05, in `logs/PREFERENCES.md`)
Turret reasons (time, weight and space, complex, fewer motors/servos); why swerve (X-lock, knew it, speed and
pushing, aim while driving); intake V1 printed funnels with front gecko wheels; shooter goals (two flywheels, moving
hood, rear-facing because pollen collects along the wall); matchloader from VEX Push Back; cameras (front: pathing to
pollen, rear: AprilTags); transition sketch sizes (pollen 71.12 mm, rollers 50 mm, gecko 48 and 32 mm, belt spacing
45, 58.5, 54, 44 mm, cross-section 70.413 mm).
