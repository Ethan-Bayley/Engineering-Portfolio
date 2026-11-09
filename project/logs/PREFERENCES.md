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
- Event: FTC Wollongong, Thursday 2026-11-12; hand-in is a PDF upload before the event (deadline not given).
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
