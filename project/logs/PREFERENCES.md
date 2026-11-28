# Preferences

Append new entries at the bottom, with the date. See skill `log-work`.

## 2026-11-04: set-up interview
- Project: FTC engineering portfolio for team 11143 Barker Yellowbacks, Barker College, 2026-27 season (BIOBUZZ).
- Use the existing empty `Engineering-Portfolio` repo.
- Format: A4 portrait.
- Awards aimed for: Inspire, Think, Control, Innovate, Design.
- First event: Wollongong FTC (date not given).
- Evidence the team has: robot photos, Onshape CAD, a code repo.
- Look: `#fbeb33` main, `#333333` background, near-white text: "nothing should be exactly white or black".
- AI credit: the user asked for the portfolio to be made with no mention of AI. FTC A201 requires a credit for AI
  help, so this is recorded as undecided (see PROJECT.md).

## 2026-11-05: new design system from three example portfolios
- Examples given: FTC portfolios of teams 12635, 1002 and 22105 (PDFs in the user's Downloads).
- Chosen: thin outline boxes like 22105; near-black #121212 page; yellow accent with green/red for pros/cons only;
  A4 portrait; Montserrat; handwritten labels with curved arrows; title left, team right; building blocks:
  challenge -> solution, iteration row V1 -> V4, team cards and timeline. Not chosen: quotes and stat bubbles.
- Agreed to download Montserrat and Caveat (SIL OFL) into project-template.

## 2026-11-05: the team's cover is the look
- The new formatting is only for the engineering portfolio: keep it out of project-template.
- The team's cover image (saved as `project/assets/cover/cover_v0_user.png`) "is kinda what we want it to look like
  throughout"; "tighten up the colours because the gold is ugly"; "we like the schematic styling".
- No CAD-to-schematic tool: the team makes the line drawings.

## 2026-11-05: content interview
- Members and roles: 13 (listed in PROJECT.md), first name + last initial.
- Event: FTC Wollongong, Thursday 2026-11-11; hand-in is a PDF upload before the event (deadline not given).
- Sponsor: Barker Robotics.
- Outreach since 1 January 2026 (user's words, no dates or numbers yet): 7 members teach robotics to Darkinjung
  students once a fortnight; Ethan B. and Isaac H. mentor VEX teams; Ethan B., Isaac H. and Brandon L. volunteered at
  the Barker VEX competition; the team ran the robotics part of the Round Square International Conference at Barker.
- Mechanisms (user's words): swerve drive, goBILDA bare motors and super servos, 4 pods; intake with vector wheels and
  gecko wheels linked to the transition; transition with gecko wheels, 2 motors; shooter, 2 motors; hood, 1 Axon Max;
  blocker, 1 Axon Max; VEX Push Back-style matchloader for the flower, 1 Axon Max; gate that stops balls going into the
  shooter, 1 Axon.
- Code: Pinkbacks repo, branches `Isaac` and `ball-tracking-greyvision`.
- Autonomous: the user has a hand-drawn auto route; wants it redrawn cleanly (same route).
- Real-robot results: "leave placeholders".
- Strategy: skip for now.
- AI credit: first asked for no mention; after being told A201 requires the credit, chose "write it and add the endnote".

## 2026-11-05: feedback on format sample v01 (passed on by the user)
- Show the design process, not only what is physically there: a judge wants to know **why** we designed it this
  way. Example given: how we were first going to use a turret, and what changed.
- Yellow: "can it be slightly a nicer shade of yellow - it's a bit blinding to the eyes".
- Earlier the same day: highlight fills at 100 %; more labels on the drawings.
- Yellow: shown softer options (#E9DB6F, #E2D377, #DCCC7E; `outputs/reviews/yellow_options_v01.png`); user chose
  **keep #F5E660**.

## 2026-11-05: design-process answers (user's words, summarised)
- Turret dropped this season because of: time, weight and space, complex / unreliable, fewer motors/servos. It got
  as far as CAD and code, never built ("CAD and code but no physical").
- Why swerve: X-lock makes us immune to defence; we already knew it; speed and pushing power; aim while driving;
  fits the game (no detail given).
- Intake before: printed funnels with only gecko wheels at the front.
- Shooter goals: we wanted a turret; more flywheel = less downtime between shots; moving hood = shoot from anywhere;
  rear-facing so we can shoot out of the flowers without turning around, and because balls collect along the wall
  we can drive up to the wall and aim instead of collecting and then turning.
- Matchloader/blocker: Ethan B., Will Q., Ryan T. and Tina X. were in VEX (Redbacks) for Push Back, saw the game was
  very similar and used a similar matchloader.

## 2026-11-05: turret, cameras and transition sketch (user's answers)
- The 5 turret drawings are **this season's turret, CAD only** (never built).
- Two cameras: the front one is for pathing to pollen, the rear one looks at AprilTags.
- Transition layout sketch (mm): pollen diameter 71.12; intake mecanum rollers 50; gecko wheels 48; smaller gecko
  wheels 32, used to minimise backspin into the shooter; spacings 45, 58.5, 54 and 44 are belt (centre) spacings;
  70.413 is the ball's cross-section on the sketch plane, because the two rows of gecko wheels sit apart.
- Go-ahead to build the 15 real pages in the format of format sample v02.

## 2026-11-05: meeting notes and a context file (spoken, typed up from a transcript)
- Wants a markdown file of what comes next, kept as context, with a skill that refers to it: made
  `project/NEXT_STEPS.md` and the project-only skill `.claude/skills/portfolio-notes/`.
- Notes from the team (their words; details in NEXT_STEPS.md part B): 6 mm polycarbonate ramps for a low-friction
  surface on the ball (heard as "6 ml"); gecko wheels grip the ball; motors unclear ("any mark motors"); swerve
  chosen to move more efficiently, a big advantage; turret wanted but time restrictions, so a fixed shooter with a
  hood to shoot from different places; a lookup table gives flywheel speed and hood angle from where localisation
  says the robot is; weight saving to keep the robot light so it moves more efficiently.
- "Just say what we said in meetings": add nothing beyond what the team said (no ramp details).
- (later) Swerve also chosen for X-lock: wheels positioned in an X, a lot harder to defend or push because of the
  friction. Asked for a set of questions to answer, with the answers then used in the portfolio.

## 2026-11-05: answers to QUESTIONS.md 1-20 (user's words in QUESTIONS.md)
- Tests: don't know yet, **the robot has not been built**.
- Darkinjung: 7 team members, fortnightly since about February; students built robots for this year's VEX IQ game;
  learnt building, coding, interviews, portfolios; some were in competitive teams and won Skills, Teamwork Champion
  and Excellence awards. VEX mentoring and the Barker VEX competition: don't know.
- Round Square: 28 September, about 7 team members, over 1,500 people from around 32 countries, introduced to FIRST.
- Meetings about every week or second week; decisions made within each specialty, then shared with the team.
- Build dates: not now.

## 2026-11-06: light page for printing
- "It is printed portfolio and black doesn't print nicely": asked for a draft with a white or near-white background,
  "a couple options". Earlier the hand-in was recorded as a PDF upload (2026-11-05): the portfolio will be printed;
  whether a PDF upload is also needed is still to confirm.
- Chose option A ("the top row is best"). Asked whether it is wise to change the yellow.
- Yellow on paper: **keep #F5E660** (offered #F7E339, #F2DC12, #FDD711).
- "Can you add more because there is lots of empty": asked mid-way through a commit, so nothing was committed; asked to fill
  the empty space on the pages.

## 2026-11-09: corrections to people and names (user)
- Cover: the bottom-right robot drawing slightly larger.
- "Chelsea W." is **Chelsey W.**; her roles are assembly and scouting. Tina X. also does strategy.
- **Cooper C. removed from the portfolio entirely** (team is now 12).
- Darkinjung: **6** members (Ethan B., Brandon L., Chloe S., Ivy W., Ryan T., Will Q.), not 7.
- VEX mentoring: Ethan B., Isaac H. and Brandon L.
- Round Square: Ivy W., Ethan B., Ryan T., Chelsey W., Chloe L., Isaac H., Tina X. and Will Q.
- Scouting: Jemima C., Chelsey W., Chloe L. and Tina X.

## 2026-11-10: Round Square photo
- Added the photo from the inbox ("round square robotics.jpg") to the outreach page. The inbox held two identical copies
  (same SHA-256); one was filed, the other removed.

## 2026-11-10: notes pasted by the user
- Turret-removal meeting notes (10 Oct 2026), the plan and what happened each week, scheduling, a Round Square write-up and
  a mentoring write-up. Recorded in NEXT_STEPS.md part B.
- The mentoring write-up's author asked for it not to be put into Claude, so it is not used until the user confirms.
- Round Square timing conflict to settle: "Term 2-3 holidays" in the write-up against 28 September 2026 given earlier.
- 2026-11-10: make the cover's top drawing fill most of the white space.

## 2026-11-11: corrections and answers (user, pasted)
- Answers: Round Square was in the **Term 2-3 holidays**; the mentoring team is **Darkinjung**.
- Writing: first person for the team ("we learned"); never the "noun, noun phrase," construction; do not sound like AI
  (slogan headings such as "One robot, many branches" were removed). Saved to memory.
- Page 1: Tina X. is Programming; add what CAD, code, strategy and assembly did; meetings every week, subteam and
  whole-team meetings. Page 2: timeline named "2026-2027 season timeline" with 15 Sep, 18 Sep, 10 Oct and a dotted line for
  28 Nov (Macquarie), 4-5 Dec (nationals) and 28 Apr-1 May (worlds); plan vs what happened; schedule image; season goals
  (win nationals, qualify for worlds). Page 3: no "about"; Round Square "very rewarding"; mentoring team; Barker VEX
  competition on 14/11 as referee and queuer.
- Page 4: show the CAD process; replace "One robot, many branches"; "competed in" Push Back; drop "the turret did not".
- Possession limit is 4 (rule G407), so 4 beam sensors. Removed: the Numbers box, belt spacing, the pollen-touch maths, the
  V1 printed funnels. "Chassis", "Why swerve" without "again", "Range" without "in our code".
- There is no matchloader in this game: call it the **flower mechanism**. The blocker stops opponents from shooting.
  The robot has a very small frame perimeter, which makes defence easier to avoid.
- New image: an exploded shooter line drawing (the user called it "turret"; it shows the fixed shooter).
- Asked me to look at the three example portfolios again (22105, 1002, 12635) and the manual TU08.

## 2026-11-11: answers to QUESTIONS 78-83
- Darkinjung VEX team: **Darkinjung Maliyan**. First team meeting: **18 September**. Beam sensors: **3** (not 4). The new
  exploded image is the **shooter**, not the turret.
- Season goals: "just add whatever season goals, make them up": drafted from what the user said (judged awards, a
  consistent robot, teaching and FIRST) and marked in QUESTIONS 80 for the user to confirm.

## 2026-11-11: team portraits
- Sent 12 head-and-shoulders photos, "left to right, top to bottom". Used in the order of the team cards on page 1 (Ethan B.,
  Brandon L., Isaac H., Ryan T., Will Q., Ivy W., Tina X., Chelsey W., Chloe L., Chloe S., Jemima C., Lucas T.). The user
  should check each photo is on the right card.

## 2026-11-11: the auto route
- Sent "elims auto" (a hand-drawn route on a field picture) and a blank field to redraw it on. Page 14 shows it as the
  elimination-match route.

## 2026-11-11: route lines and the team grid
- Make the auto route out of **straight lines**.
- Team grid: **one column per subteam, lead on top.** Design (Ethan, Brandon, Ryan, Lucas), Programming (Isaac, Ivy, Tina,
  Jemima), Strategy (Will, Chelsey, Chloe L., Chloe S.). Chloe S.: strategy first, then scouting. "Whatever else to make it
  work best" was left to me.

## 2026-11-11: route is the sketch's intent; two role changes
- The route image was only a sketch: draw straight lines to where it is trying to say the robot goes (start, wall marker,
  wall marker, end), not the wiggles.
- Chloe L.: **scouting** is her primary role (electrical and assembly after). Chloe S.: **code removed** (strategy, scouting,
  assembly).

## 2026-11-11: route direction and grid; page 5 scoring rows
- "You have it backwards": the route runs the other way. It should go **out from the flowers and then in straight horizontal or
  vertical lines into them**, with the points on the grid lines (tile midpoints allowed).
- Page 5: "pollen in flowers" answer = we do not do it, not enough points to be worth it. Add **parking** as a way we score.

## 2026-11-11: the auto route is general, with seven steps
- Not elimination-specific: it is just the autonomous route. Go into and out of each flower on the **same line**.
- Steps: 1 shoot (causing a tip), 2 get pollen from the flower, 3 go to the shooting position on the other side, 4 shoot,
  5 collect pollen from the flower, 6 shoot, 7 park.

## 2026-11-11: auto points; drop the plan-vs-happened box
- The second shot scores nothing and the third scores 20 points (so the auto is 20 + 0 + 20 + park 5 = 45).
- "The planned on 10 October vs what happened section is stupid": removed from page 2.

## 2026-11-11: scouting, sections removed, choices compared
- Page 5: write one or two sentences on why scouting is good and what it is used for. Remove "How well it worked". Page 14: remove
  the date line.
- Last page: remove Test results, Next and Reliability, and put other content on it. Add a "Choices we compared" section to each
  subsystem page.
- Asked first whether the testing and lessons page was necessary; I said no and suggested moving the lessons to page 4 and adding a
  choices page. The user chose to keep the page as a lessons page and put the choices on each subsystem page.

## 2026-11-11: instead-of answers; the blocker is gone
- Ramps: instead of 3D printed ramps. Side vertical intake wheels (read as the flower mechanism's alternative). Position tracking:
  odometry and the IMU instead of motor encoders, because it is much more accurate.
- Remove every mention of the blocker: there will not be one at competition.

## 2026-11-11: test results
- Top speed 250 cm/s; X-lock: it did not move; 1 jam solved by reversing the rollers; all but 1 shot from the furthest distance went in;
  time between shots under 0.1 s; auto routes really consistent; 3 of 3 score while still, 2 of 3 while moving.
- Asked me to list anything else that is not complete.

## 2026-11-11 (later): answers
- Holds 4 pollen; 6.5 kg; 3 minutes; "yes correct" for the instead-of cells; "we use odometry"; the tests are in date.

## 2026-11-11 (later): results and a placeholder
- Flower mechanism: empties the flower really well in under a second. Cameras work. Speed drop about 200 encoder ticks.
- Keep a placeholder for "how we play" (the user will write it).

## 2026-11-12: strategy
- Strategy points: score pollen to maximise RP; outscore teams to maximise output; cycle fast and be robust; a simple robot that can be made quickly.

## 2026-11-12: mentor feedback and outreach impact
- Mentor asked for more on how the design process was used on the robot and more on the impact of volunteering.
- Darkinjung: over 20 students, about 15 sessions; students formed their own teams and competed for the first time;
  they won a couple of awards with our help. For us: better at explaining (interviews) and leading a group.


## 2026-11-28
- Award aim: **Design, Control and Innovate** (earlier, 2026-11-21: try for Inspire). Base for printing: Ethan's v37 plus
  newer facts. Answers: 3 beam sensors; remove the blocker; jams, shooting speed and roles as v37; keep the path picture from
  the hand-edited PDF, everything else on page 14 as v37; "we kinda just shoot from one spot now but we're still saying
  that it works from other positions".
