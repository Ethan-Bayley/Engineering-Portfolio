# Decisions

Append new entries at the bottom, with the date. See skill `log-work`.

## 1. Project set up (2026-11-04)
- **What:** project-template checked out into the user's empty `Engineering-Portfolio` repo (files staged, not
  committed); `template` remote added. No `origin` yet: publish from GitHub Desktop.
- **Rules source:** FTC Competition Manual section 6, TU06 (22 Oct 2026), saved in `project/brief/`. Summary and
  award criteria in `brief/ASSESSMENT.md`.
- **Format:** new `portfolio` format in the shared design system (also added to project-template): A4 portrait
  (595.28 x 841.89 pt), sizes title 26, heading 14, sub 12, body 10.5, table 10, small 10, stat numbers 20 pt, so no
  text is under A201's 10 pt. A4 rather than US Letter (user picked A4 portrait; Australian printers use A4).
- **Dark theme:** the design system can now take `background`, `panel`, `text`, `on_colour` and `on_main` from
  `design.json` (shared change). Box colours were made brighter for the dark panels. Contrast measured with the WCAG
  formula on 2026-11-04: text F2F2F2 on panel 3C3C3C 9.9:1; yellow FBEB33 titles on 333333 10.2:1; box-colour
  headings on the panel: green 3DC48F 5.0, orange F2A541 5.4, purple A39BF0 4.5, red F2756A 4.0 (bold 14 pt needs
  3:1); dark 262626 text on the box colours 5.4 to 7.4. The default box colours would have been 2.4:1 (red) and
  3.2:1 (green) on the dark panel, too low.
- **Not done / not proven:** the dark theme has not been printed; the event date, members and the AI-credit decision
  are missing; no evidence in `project/assets/` yet.

## 2. New look: the portfolio style (2026-11-05)
- **What:** the portfolio now uses a new, separate style, `general/design/portfolio_style.py` (made in
  project-template and copied here, not yet committed in either), instead of the box-colour design system with the
  dark theme from section 1. `project/design.json` now holds only main FBEB33, background 121212 and text F2F2F2.
  `build_portfolio.py` was replaced by the new starter with the team filled in (placeholders only).
- **How it was decided:** three example portfolios measured with PyMuPDF (all US Letter portrait, 16 pages,
  #000000-#0F0F0F pages, near-white text, one accent; boxes differ), then two rounds of questions (PREFERENCES.md).
- **Measured:** contrast on #121212: text 16.7:1, yellow 15.2:1, muted grey 9.1:1, green 10.7:1, red 7.4:1.
  PowerPoint draws Montserrat at 1.2 x the font size (measured in an exported PDF). The starter's three pages export
  with Montserrat and Caveat embedded and pass the style's checks (nothing under 10 pt, gaps, fits).
- **Section 1's dark theme** for the default design system stays in project-template but is not used here.
- **Not done / not proven:** no real page yet (no photos or CAD in `project/assets/`); the dark pages have not been
  printed; dark charts for this style are not done; event date, members and the AI-credit decision are still open.

## 3. The team's cover becomes the look; the style moves into this project (2026-11-05)
- **What changed:** the portfolio style now lives only here, in `project/design/` (code, rules, fonts), with tests
  in `project/tests/`. It was taken out of project-template again, together with section 1's dark theme and
  `portfolio` format and the theme-aware charts (all were uncommitted there; a backup of that diff is kept outside
  the repos). The template keeps three generic changes: `export_pdf.py` and `install_fonts.ps1` load a project's
  own fonts from `project/design/fonts/`, the design.json test no longer assumes the default colours, and the
  setup skill says to save a competition's rules first. This repo's `general/`, `.claude/skills/` and shared tests
  were copied back from the template so they match it.
- **New look:** from the user's cover (colours sampled from the image: page #171616, yellow #F5E660, gold #B8985A,
  cream #FFF4B2, dull yellow #D8CD6C, grey #C4C4C4). Kept the page, the yellow and the grey; dropped gold, cream and
  the dull yellow (user: the gold is ugly). Square thin-outline boxes replace the rounded ones from section 2; the
  title is a yellow banner with hazard stripes; challenge/solution labels are pills like the cover's.
  `project/design.json`: main F5E660, background 171616, text F2F2F2.
- **Measured:** contrast on #171616: text 16.1, yellow 14.1, grey 10.4, outline grey 5.4, green 10.3, red 7.2;
  dark text on yellow 14.1. The draft (cover + 2 placeholder pages) exports with Montserrat and Caveat only; all
  42 tests pass (37 shared, 5 for this style).
- **Mistake on the way:** the first bullet character (U+25AA) is not in Montserrat, so PowerPoint drew it in Times
  New Roman and the PDF check refused the export. Changed to U+25A0, which Montserrat has.
- **Not done / not proven:** robot drawings are low-resolution crops of the cover image (layout only); no FIRST
  logo; not printed; no real content (AI credit still undecided); event date and members still TODO.

## 4. Content inputs, AI credit and the code evidence (2026-11-05)
- **AI credit:** Claude drafts the text; one endnote on the last page credits AI help (FTC A201). The team reviews
  every page before upload.
- **Template remote:** `template` added fetch-only (push URL `no_push`) beside the published `origin`.
  `template_sync.py status`: 2 shared files are older here than the template (`.claude/skills/setup-project/SKILL.md`,
  `general/tools/template_sync.py`; fetch-only remote guidance). Not pulled yet.
- **Code read (branch `Isaac`, commits 2026-09-23 to 2026-10-26; `doc/isaac-integration.md`, 25 Oct 2026):** swerve
  with 4 drive motors, 4 continuous-rotation steering servos and 4 analog angle encoders; REV IMU; 3 digital beam
  sensors for ball count in the intake (bottom, middle, top); gate servo; two-motor shooter wheel with a PIDF
  controller; hood servo; shot lookup table (interpolation map, refuses extrapolation); rear-facing fixed shooter, so
  a held aim button turns the chassis (heading PD + static feedforward, tolerance 2.5 degrees); battery-voltage and
  motor-current monitoring. CAD-derived size 407.7 x 327.0 x 290.9 mm, module spacing 239 x 239 mm, wheel diameter
  60.9 mm. 24 desktop tests pass; in **simulation** the TeleOp scores 3 of 3 balls for both alliances, including
  moving shots. **Not proven on the robot:** `PHYSICAL_SHOT_CALIBRATION_CONFIRMED = false`; hood endpoints, muzzle
  point and RPM-to-ball-speed still need measuring. No autonomous OpMode for this robot on this branch.
- **Branch `ball-tracking-greyvision`:** mostly June-July 2026 commits for last season's DECODE robot (far-zone
  autos, Limelight heading reset) by people including some not on the team list: background only, if used.
- **Real results:** placeholders `<RESULT: ...>`, which make the hand-in check fail until filled.

## 5. CAD line drawings sorted (2026-11-05)
- **What:** 32 team-made line drawings from `assets/inbox/` moved and renamed into `assets/cad/linework/` by
  subsystem: swerve 14 (exploded x3, assembled x4, gear train x3, wheel-drive train highlighted x2, module-rotation
  train highlighted x2), odometry pod 5, shooter 6 (incl. hood drive and belt drive highlighted), chassis 4,
  whole robot 3 (incl. a side section showing the ball path). Old-to-new names in `cad/linework/README.md`.
- **Classified by looking:** wheel-drive vs module-rotation highlights were read from the gear paths (motor pinion
  -> coaxial gear -> bevel -> wheel; big ring gear -> pod fork). User to confirm.
- **Measured:** background #333333 (51, 51, 51), not the page #171616, so the drawings would show as grey boxes;
  highlights are orange, not the portfolio yellow #F5E660. Sizes 450-800 px on the long side: about 200 dpi at
  half page width (fine), soft at full page width (cover).
- **Not done:** no recolouring yet (needs the user's OK: it changes their drawings' colours).

## 6. Line drawings recoloured to the page (2026-11-05)
- **What:** `src/recolour_linework.py` makes copies of all 32 drawings in `assets/cad/linework_page/` (same folders
  and names); the originals in `assets/cad/linework/` are unchanged. Use the `_page` copies in the portfolio.
- **How:** each pixel is solved as a mix of background #333333, white line and orange highlight #FFA500 (sampled:
  fills read about 45 % orange over the background), then rebuilt as page #171616, line #F2F2F2 and yellow
  #F5E660. Edges and see-through fills keep their strength. Test: `project/tests/test_recolour_linework.py`.
- **Measured:** after the run, background pixels read (22, 22, 22) against the page's (23, 22, 22): JPEG rounding,
  1 level, not visible. No orange pixels left in the sampled files. Copies 3.3 MB in total (JPEG quality 95).
- **Seen:** the highlight fills come out olive-yellow on the dark page (yellow at about 45 % strength). Fine on
  screen; check on the test print and raise the fill strength if it looks muddy.

## 7. Highlight fill strengths 50-100 %, colour-corrected (2026-11-05)
- **What (user asked):** the 6 highlighted drawings at fill strength 50, 60, 70, 80, 90 and 100 %, each
  colour-corrected towards the team yellow: 36 files in `assets/cad/linework_page/strengths/<folder>/<name>_sNN.jpg`
  (`python project/src/recolour_linework.py --strengths`). Comparison of plain against corrected:
  `outputs/reviews/linework_strengths_v01.png`.
- **Measured fill:** the drawn fills are about 40 % orange (mode of 5 of the 6 drawings; the belt-drive one is mostly
  lines). Highlight lines stay full yellow at every strength.
- **Correction:** keeps the plain mix's OKLab lightness and sets the yellow's hue (102.9 degrees) with as much of its
  chroma (0.153) as sRGB allows. Fill colours (plain -> corrected, chroma as % of the yellow's):
  50 % #867E3B 58 % -> #8A7E00 80 %; 60 % #9C9342 67 % -> #A09300 90 %; 70 % #B2A84A 76 % -> #B7A800 99 %;
  80 % #C9BC51 84 % -> #CCBC2D 100 %; 90 % #DFD159 92 % -> #E0D148 100 %; 100 % #F5E660 both.
  The plain mix was already within 0.6 degrees of the yellow's hue: the olive look came from lost chroma, not hue.
  At 50-60 % full chroma is not possible in sRGB at that lightness, so the closest colour is a dark mustard.
- **Contrast of the near-white detail lines on the fill:** 3.7:1 at 50 %, 2.8 at 60, 2.2 at 70, 1.7 at 80,
  1.4 at 90, 1.1 at 100 (lines inside the fill disappear at 90-100 %). Dark #171616 lines on the fill would be
  4.4 to 14.1:1.
- **Seen on the sheet:** corrected 80-90 % look closest to the team yellow; corrected 50-70 % read mustard/gold.
- **Not done:** not printed; no strength chosen yet.

## 8. Show the design process: why, not only what (2026-11-05)
- **Feedback (passed on by the user):** judges want to understand why we designed it this way; example: the turret.
- **Evidence for the turret story:** last season's robot (2025-26, DECODE) had a turret, tuned April to June 2026
  (commits: turret feedforward, encoder, CR turret 22 Jun). This season's shooter code had a turret until
  2026-10-12 ("removed turret"); the fixed rear shooter with whole-robot aiming was merged 2026-10-25. Turret this
  season: CAD and code, never built (user). Reasons (user): time, weight and space, complexity / reliability,
  fewer motors and servos.
- **Change:** every mechanism page gets a "what we wanted / what we tried / why we changed" part (PAGE_PLAN.md);
  the format sample gets a shooter design-process page and the real "why swerve" reasons.
- **Yellow:** stays #F5E660 (user chose it over three softer options).

## 9. Format sample v01 and v02 (2026-11-05)
- **What:** `outputs/portfolio/format_sample.py` builds a style sample (not the portfolio): cover plus format guide,
  swerve drivetrain, shooter design (design process), control system and team pages. v02 PDF:
  `outputs/portfolio/format_sample_v02.pdf` (6 pages, Montserrat and Caveat embedded); renders in
  `outputs/renders/format_sample_v02/`.
- **Drawings:** `linework_page` copies are now see-through PNGs (page colour made transparent), with a 3 px border
  and JPEG noise under 3 % cleared: the originals have a faint lighter frame (edge rows about 71 against 51) that
  showed as boxes on the page. Measured after: page pixels around the drawings equal the page.
- **Cover:** now uses the team's full drawings `robot_iso` and `robot_side` instead of the low-res crops.
- **Labels:** 16 handwritten labels on 6 drawings, placed by eye on a tenths grid; the labelling is my reading of
  the drawings (flywheel, hood rack, servo gear, steering gears, angle sensor, odometry wheels): team to check.
- **Shooter screenshots:** 5 shaded Onshape exploded views filed in `assets/cad/screenshots/shooter/`; not line
  drawings, so not recoloured and not used yet.
- **Not done / not proven:** not printed; placeholders `<...>` remain on purpose; turret cards have no picture.

## 10. Portfolio v01 and v02 built; first marking loop (2026-11-05)
- **What:** `build_portfolio.py` now builds the cover plus the 15 pages of PAGE_PLAN.md. v01 then v02
  (`outputs/portfolio/portfolio_v02.pdf`, 16 pages, 2.5 MB, Montserrat and Caveat embedded). Cover adds Barker
  College and "Supported by Barker Robotics". New drawings sorted: 5 turret (this season, CAD only) and 9 transition
  (`assets/cad/linework/turret`, `transition`), recoloured to `linework_page` (46 drawings now).
- **Maths added (page 8):** the sketch plane cuts the 71.12 mm pollen in a 70.413 mm circle, so the plane is
  sqrt(35.56^2 - 35.21^2) = 5.0 mm from its centre (calculated 2026-11-05 from the user's sketch numbers).
- **Checked against the code before stating:** shooter feedforward is scaled by battery voltage (Shooter.java);
  aim gains kP 4.0, kD 0.35, kS 0.06 (RobotConfig); lost heading sensor stops drive and feeding (sim test).
- **Marking loop:** `outputs/reviews/marking_loop.md`, 2 rounds, estimate 52 then 55 / 100 (judgement; FTC has no
  bands). Round 1 found one invented pro on intake V1 ("simple to print"), removed in v02.
- **Shared tool fix (should also go into project-template):** `general/tools/hand_in_check.py` crashed on the
  Windows console printing U+25A0; `main()` now reconfigures stdout with `errors="replace"`. Also noticed:
  `--deliverable portfolio` picks `format_sample_v02.pdf` (sorted by name) instead of the newest portfolio PDF, so
  pass the PDF path. Project test updated for 15 pages.
- **Montserrat has no ω:** written as "turn rate"; √, ², −, × are in the font.
- **Not done / not proven:** 53 placeholders; not printed (A202 printed spare; upload is a PDF); no autonomous
  drawing; upload deadline unknown.

## 11. Question sheet for the team (2026-11-05)
- `project/QUESTIONS.md`: 38 questions for every placeholder, then 36 subsystem questions (39-74) written from the
  drawings and the code, so each page can say why a part is built that way. Read by the skill `portfolio-notes`.
- **Found in the code while writing them** (branch `Isaac`, ShooterConstants.java): flywheel limit 3500 RPM, ready
  within 50 RPM; hood 33.579 to 67 degrees, ready within 2 degrees; shooter motors 28 counts per turn (bare
  motors); drive encoders 537.7 counts per turn (a 19.2:1 gearbox, while the user said "bare motor": question 39);
  intake motors at 50 % power. **The shot table is empty** (`SHOT_VALUES = {}`), so pages 9 and 13 must not say
  it has been measured until question 64 is answered.

## 12. Portfolio v03: robot not built yet (2026-11-05)
- **Why:** the user said none of the tests can be answered because the robot has not been built. Every robot test
  now reads "not built yet" (status NOT TESTED) instead of a `<RESULT>` placeholder, so the pages are honest and the
  hand-in check only fails on real team gaps. Page 2 says where we are (CAD + simulation, not built). One wrong
  phrase fixed: the shooter drawing's alt text said "the fixed rear shooter we built".
- **Answers used (QUESTIONS.md 12-19):** Darkinjung (7 members, fortnightly since about February 2026, VEX IQ,
  Skills / Teamwork Champion / Excellence awards); Round Square (28 September 2026, about 7 of us, over 1,500 people,
  around 32 countries); meetings every week or two; decisions within specialties. VEX mentoring and the Barker VEX
  competition stay without numbers; the build-dates table was removed.
- **Meeting notes used:** X-lock friction, efficiency, polycarbonate ramps (no thickness until "6 mm" is confirmed),
  lookup table from localisation ("values still to be measured", since the code's table is empty), keep it light.
- **Result:** `portfolio_v03.pdf`, 16 pages, 2.5 MB; 17 placeholders left; page images in `pages_v03/`.

## 13. Two light options for printing (2026-11-06)
- **What:** themes in `project/design/portfolio_style.py`, chosen with `PORTFOLIO_THEME=paper|band`; the default stays
  dark and portfolio v03 is unchanged. Same content as v03. Outputs: `outputs/portfolio/portfolio_paper_v01.pdf`
  (**A**, white page, yellow bands with dark text and thin dark outlines) and `portfolio_band_v01.pdf` (**B**,
  near-white #FAF9F5, near-black bands with yellow text, yellow hazard stripes). Comparison:
  `outputs/reviews/light_options_v01.png`. Neither is chosen yet.
- **Why more than a new background:** yellow on white measures 1.28:1, so key words, sub-headings, handwritten labels
  and arrows became near-black, and yellow is only a fill. Pros and cons were darkened. Contrast on the page, measured
  with the WCAG formula: A text 18.1, grey 8.5, green 5.4, red 5.6, outlines 3.4; B text 17.1, grey 8.0, green 5.1,
  red 5.3, outlines 3.2; text on bands 14.1 in both.
- **Drawings:** `src/recolour_linework.py --light` makes `assets/cad/linework_light/` (46 PNGs): near-black lines, yellow
  fills with dark outlines, page see-through. Faint yellow specks around some highlights come from the JPEG sources.
- **Checks:** 16 pages, A4, fonts embedded, 1.3 MB each (half the dark PDF); same 17 placeholders as v03. Tests: 49 pass
  (added theme contrast, light build, see-through page).
- **Not done / not proven:** neither has been printed. The full-height edge bar and B's tinted page may stop at the
  printer's unprintable margin, leaving a thin white border unless printed borderless or scaled to fit. White (A) has
  no such border except at the edge bar.

## 14. Option A is the look; yellow compared on white (2026-11-06)
- **What:** `PORTFOLIO_THEME` now defaults to `paper`, so the next save is `portfolio_v04` in option A. Dark and band still
  build (`portfolio_dark_vNN`, `portfolio_band_vNN`). Existing files were not rebuilt.
- **Yellow on white, measured (`outputs/reviews/yellow_on_white_v01.png`):** #F5E660 now: 1.28:1 on white, dark text on it
  14.1:1, OKLCH chroma 0.153, hue 103. #F7E339: 1.31, 13.8, chroma 0.175 (114 %), hue 102. #F2DC12: 1.40, 12.9, chroma
  0.183 (120 %), hue 102. #FDD711: 1.41, 12.8, chroma 0.180 (118 %), hue 96, starts towards gold.
- **Advice given:** a small move to #F7E339 for paper; not the warmer one (the user called gold ugly). No change made: the
  user decides, and only a printed page can settle it. Note: the earlier "keep #F5E660" was about softer yellows for the
  dark page, the opposite direction.
- **Decided (user, 2026-11-06):** keep #F5E660 on the white page. Saved as `portfolio_v04` (same content as v03, option A; 1.3 MB; same 17 placeholders).
- **Mistake found:** the v03 update to `NEXT_STEPS.md` was never saved (the script changed the text but did not write the file), so it still said v02. Fixed with this update.
- **v05 (2026-11-06):** table rules and straight arrows inherited a theme shadow (`effectRef idx=1`), hidden on the dark page but a grey smudge on white. `_straight` now sets an empty `a:effectLst`; test added. Same content as v03 and v04.

## 15. Portfolio v06: fuller pages (2026-11-06)
- **Why:** the user said there was lots of empty space. Filled with what already exists, nothing invented: more of the team's
  drawings (chassis, odometry exploded, transition, shaded shooter exploded view, whose flat #333333 background is keyed out
  into `assets/cad/screenshots_page/`) and more detail from the code report and code on branch `Isaac`.
- **Added:** page 2 code milestones from commit dates; page 3 number tiles and a photo frame; page 4 sketch beside its CAD;
  page 5 one scoring cycle; page 6 chassis, parts breakdown; page 8 sketch beside the maths; page 9 exploded view, hood range;
  page 10 how pollen is held and released; page 11 odometry exploded, code limits; page 12 the bugs found when merging; page 13
  the order of checks before a shot (`Robot.java`: no trajectory, calibration, aiming, spinning up, settling 0.1 s, empty,
  feeding); page 14 what the autonomous can use; page 15 more simulation results.
- **Found and corrected:** pages 9 and 13 implied the lookup table sets the shot. On branch `Isaac` the table is empty and not
  called: `Robot.update` uses `RearAim` and `Ballistics` (a gravity solver). Page 13 now says solver, page 9 says the table is
  started and measured once the robot is built. **Mismatch with the team's meeting note, question 75.** No X-lock code on the
  branch either: question 76. Also removed "print, cut, assemble" from page 4 (not stated by the team).
- **Result:** `portfolio_v06.pdf`, 16 pages. Placeholders: 18 (one more than v05, the photo frame). Labels on drawings are my
  reading: question 77.

## 16. Portfolio v07: people corrections (2026-11-09)
- **What:** the user's corrections (PREFERENCES.md, 2026-11-09), plus the counts they change on page 1: 12 members; code 5
  (Isaac H., Ivy W., Tina X., Chloe S., Jemima C.); strategy planned by 3 (Will Q., Chloe S., Tina X.) and 4 scout (Jemima
  C., Chelsey W., Chloe L., Tina X.); assembly 8 of 12. Round Square now names 8 people instead of "about 7". Cover's second
  drawing about 12 % larger (box 0.65 of the width, 245 pt high, was 0.58 and 230 pt).
- Also changed: PROJECT.md members, NEXT_STEPS suggested names, QUESTIONS 12 and 22, PAGE_PLAN, and the old format sample's
  source (its saved files were not rebuilt). Older log entries still say 13 members and 7: they were right when written.

## 17. Portfolio v08: Round Square photo (2026-11-10)
- **What:** `assets/photos/raw/round_square_2026-09-28.jpg` (800 x 600 px, from the inbox; an identical second copy was
  removed), prepared to `photos/ready/` with `photo_prep.py` (no crop, no edits). On page 3 it sits beside the Round Square
  story, in the space the empty "Photos" frame took; that frame and its placeholder are gone (18 -> 17 placeholders).
- **Not proven:** 800 px wide prints at about 160 dpi at this size, a little soft; a larger original would print sharper.
  No Darkinjung photo yet. Photographer not recorded (CREDITS.md).

## 18. Portfolio v09: the turret meeting and plan against what happened (2026-11-10)
- **From the team's notes (NEXT_STEPS.md part B, 2026-11-10):** page 2 now shows the plan made at the 10 October meeting
  against what happened each week (12 Oct to 1 Nov; 2-8 Nov left for the team), the scheduling spreadsheet and its
  lesson. Page 9 gives the meeting's reasons for cutting the turret (regionals 4 weeks away, goBILDA parts delayed, least
  necessary part; kept swerve and the blocker; consistency first). Page 3 adds the Round Square demos and that many
  delegates had not heard of FIRST. Page 7: custom pod parts, machined. Page 14: ball tracking for autos started 12-18
  Oct. Page 15: two lessons (cut the least necessary part; plan around exams and outreach).
- **Removed from page 2:** the code-milestones table and "what we kept from last season" (pages 4 and 9 cover the same).
- **Wording:** "not built" became "not finished" everywhere, because the notes say the swerve was assembled.
- **Not used:** the mentoring write-up (its author asked not to put it into Claude). **To check:** Round Square in the
  Term 2-3 holidays (notes) or 28 September (user); Dhupuma or Darkinjung.

## 19. Portfolio v10: bigger cover drawing (2026-11-10)
- **What (user asked):** the cover's top robot drawing fills most of the white space. It is now cut to what is drawn (`trimmed()` in the build script saves `<name>_trim.png`; the original had empty margins of about 10 %) and placed in a box 330 pt high instead of 270 pt, about 1.4 x wider on the page. The team-number box grows to the same height. Nothing else changed.

## 20. Portfolio v11: saved as it stood (2026-11-11)
- The user asked for v11 "as it is" while I was partway through a first-person pass. `portfolio_v11.pdf` has their
  2026-11-10 page edits (roles, how we split and run the work, season timeline, 10 Oct meeting, schedule image, outreach,
  requirements note) but not the wording clean-up. Superseded by v12.

## 21. Portfolio v12: corrections, plain wording, and what the examples have (2026-11-11)
- **Manual TU08** (read for this): max 4 scoring elements controlled (G407) and 4 pollen preloaded per robot: so 4, not 3;
  a HIVE TIP is 20 points in auto and in teleop and needs a launch into the upward cell (10.5.1); tips also give ranking
  points at 4 and 7 tips at most events; R503 limits a robot to 8 motors and 8 servos (we use 8 and 8); portfolio rules
  A201/A202 unchanged (printed copy by default). Page 5 now has "What scores points" from Table 10-2.
- **Examples** (22105, 1002-2, 12635, all US Letter, 16 pages): see NEXT_STEPS "What the example portfolios have that ours
  still lacks": mainly real photos, iteration photos, graphs, comparison tables, team photo and quotes. v12 adds the CAD
  process example, a game-points table and design choices; the rest needs the team's evidence.
- **Rewritten** (all 15 pages) in the first person with plain headings. Removed: Numbers, belt spacing, pollen-touch maths,
  V1 printed funnels, "again", "in our code", the AI-sounding box names. Renamed matchloader to flower mechanism everywhere
  in the pages, questions and notes (older logs keep the team's words).
- **Beam sensors:** the pages say 4 (user, and G407). The code on branch `Isaac` still counts to 3: QUESTIONS 82.
- **Two readings to check:** the user said "exploded turret isometric" but the image shows the fixed shooter, so it is on
  page 9 labelled flywheel, hood and motor (QUESTIONS 83); first team meeting was 17 Sep, then 18 Sep (QUESTIONS 81).
- **Not done:** the Darkinjung team name (placeholder), "champs, Wollongong, Macquarie" for the 14 Nov competition (not
  clear what to say: QUESTIONS 79), more season goals (80).
- **Image:** new line drawing saved as `assets/cad/linework_light/shooter/shooter_exploded_iso_lines.png` (black lines made
  see-through, original in `assets/cad/screenshots/shooter/`).

## 22. Portfolio v13: answers applied (2026-11-11)
- Team name Darkinjung Maliyan (page 3); beam sensors back to 3 (pages 8, 10, 11) and the scoring cycle says "until the
  intake is full" instead of a number, because the robot has 3 sensors but rule G407 allows 4: question 84.
- Three season goals were **drafted by me at the user's request** (judged awards, consistent robot, outreach); they are
  intentions, not results, and are marked for confirmation. No result or test claim was added.

## 23. Portfolio v14: team portraits (2026-11-11)
- 12 photos (120 x 120 px each, about 170 dpi at the size printed) filed in `assets/photos/raw/team_<name>.png` and prepared
  to `ready/` with `photo_prep.py` (no edits). They are matched to the cards **by the order the user gave**, not by looking
  at faces: the user must confirm. A201 allows student photos with first name and last initial only. CREDITS.md says to
  confirm each member agreed to appear.

## 24. Portfolio v15: the auto route redrawn (2026-11-11)
- **Method:** `project/src/trace_auto_route.py` finds the black line in the hand-drawn picture (one connected stroke),
  follows its centre, keeps the out-and-back to the top marker, smooths it (RDP then two Chaikin passes) and draws it on the
  blank field (3x enlarged). The blank field is the hand-drawn one **turned 90 degrees anticlockwise**: checked on the four
  gold markers, both gardens and both loading zones. Point (u, v) of the hand-drawn field goes to (v, 1 - u). A check overlay
  (the smoothed line on the original) matched the drawing. Pictures kept in `assets/auto/source/`.
- **Read from the drawing, not decided by me:** the line starts beside the red loading zone, goes out to a marker on a wall,
  comes back across the field, turns sharply near the opposite wall marker, and ends at a wall. Marked with a start ring and
  an end arrow; **the direction is my assumption** (start at the loading zone): to confirm. Colour is the page's yellow with a
  dark outline. Steps, points and the date are still the team's (QUESTIONS 35, 36).
- **Credit:** the field pictures come from a field diagram whose source I do not know: check we may use it (CREDITS.md).

## 25. Portfolio v16 and v17: straight route, subteam grid (2026-11-11)
- **Route (v16):** `trace_auto_route.py` now keeps straight segments (RDP corner points only, 12 points, no rounding).
- **Team grid (v16):** a header over each column (Design and CAD, Programming, Strategy and scouting); leads Ethan B., Isaac H.
  and Will Q. on top. The grid fills row by row, so the lists in `p01_team` run across. Roles changed to fit the columns:
  Ryan T. CAD (driver second); Chelsey W. scouting (assembly second); Chloe L. electrical (scouting, assembly); Chloe S.
  strategy (scouting, code, assembly); Tina X. programming (strategy, scouting, assembly). I kept Chloe S.'s code and assembly so
  the user's earlier counts still hold (assembly 8 of 12, code 5) and made scouts **five** (Jemima, Chelsey, Chloe L., Tina,
  Chloe S.), also on page 5. **To confirm** with the user.
- **v17:** page 14 step table widths (the headers wrapped) and a larger route picture; same content as v16.
- **Rule reached:** the five-version limit for the page 5 success note (v11 + 5 = v16) has passed with the note still empty.
  Asked the user before writing anything (memory: portfolio-honesty).

## 26. Portfolio v18: route as four points, role changes (2026-11-11)
- **Route:** `trace_auto_route.py` now only joins four key points read off the sketch with straight lines: start beside the
  red loading zone, the wall marker at the top of the sketch, the wall marker at the left, and the end at the bottom wall
  (mapped onto the blank field by turning it 90 degrees anticlockwise). The earlier pixel tracing was dropped: it followed
  the hand wobble. The direction (start at the loading zone, arrow at the end) is still my assumption.
- **Roles:** Chloe L. is Scouting first (electrical, assembly); Chloe S. is Strategy (scouting, assembly), no code. Code is
  now **four** of us (Isaac H., Ivy W., Tina X., Jemima C.) on page 1. Assembly is still eight, scouts still five.
- **v19:** the page 14 caption now says the route is the sketch redrawn as straight lines between its points.

## 27. Portfolio v20: route on the grid, reversed; parking and flowers on page 5 (2026-11-11)
- **What the gold hexagons are:** the manual (TU08) says the four FLOWERS are attached to the perimeter, so they are the gold
  hexagons on the walls, not "markers". Pollen can be removed from the bottom of a flower.
- **Route:** `trace_auto_route.py` now draws horizontal and vertical lines on the grid (corners on grid lines or tile
  midpoints), **reversed**: it starts at the right wall, goes into the bottom flower and the left flower (each out and back, as in
  the sketch, the way back drawn 22 px to the side) and ends in the red loading zone. **My reading of "backwards" and of "out
  from the flowers" is to be confirmed**; the start point on the wall is the sketch's end point, moved to a tile midpoint.
- **Page 5 scoring table:** PARK is 5 in auto and 5 in teleop and needs the robot at least partly in its loading zone (manual
  10.5.4 and Table 10-2). Added a Park row (our answer: swerve, we park in our loading zone) and a "pollen in a flower we own"
  row (2 each) answered "we do not do this: not enough points", as the user said.

## 28. Portfolio v21: general auto route with seven steps (2026-11-11)
- Page 14 is now "Our autonomous route" (no "elimination"); the image is `assets/auto/auto_route.png` (renamed; the script
  `trace_auto_route.py` writes it). In and out of each flower run along the same line; numbered circles 1 to 7 match the steps.
- **Points column** (manual TU08 Table 10-2): step 1 = 20 (a HIVE TIP is 20 in auto), step 7 = 5 (PARK is 5 in auto), the
  pollen steps score nothing themselves ("-"), and steps 4 and 6 are `<pts>` because the user did not say whether those shots
  cause tips (QUESTIONS 35). LEAVE (3 points in auto for leaving the wall) is not claimed: nobody said the start is on the wall.
- **My placement, to confirm:** the flowers are the bottom one first and then the left one; the shooting position is on the left
  of the field after the bottom flower ("the other side"); step 6 is at the left flower's line before parking; the start is on
  the right wall. Steps 3 and 4 share the shooting position.
- **v22:** page 14 layout only: the Points header no longer wraps and the route picture is larger. Same content as v21.

## 29. Portfolio v23: auto points, page 2 without the plan table (2026-11-11)
- **Page 14:** step 4 scores 0, step 6 scores 20 (a HIVE TIP is 20 in auto, manual Table 10-2); with step 1 (20) and park (5) the
  total is **45**. Non-scoring steps now say 0.
- **Page 2:** the "Planned on 10 October vs what happened" box and its table were removed at the user's request (this also removes
  the `<what happened>` placeholder and the 2-8 Nov row). The timeline now carries what happened (15 Sep, 18 Sep, 10 Oct, 19-25 Oct,
  26 Oct-1 Nov) and a second dotted row for what is still to come (12 Nov Wollongong, 28 Nov, 4-5 Dec, 28 Apr-1 May); Wollongong
  moved to the dotted row because it has not happened yet. The freed space goes to a bigger schedule picture and the goals.
- The 12-18 Oct facts (parts ordered, shooter redesigned, intake and transfer design, ball tracking started) are no longer on page 2;
  the ball tracking stays on page 14 and the turret reasons on page 9.
- **v24:** page 14 layout only: the Step header no longer wraps and the route picture is larger. Same content as v23.
- **v25:** the page 14 step table headers are now No. and Pts so neither can wrap. Same content as v23.

## 30. Portfolio v26 and v27: choices on every subsystem page, last page reworked (2026-11-11)
- **Page 5:** scouting is two general sentences (what scouting shows us; we use it to choose alliance partners and plan each
  match): purpose only, no claims about what the team records. The "How well it worked" note is gone, so the five-version rule
  about writing "overall successful" is void and nothing like it was written.
- **Page 14:** the "date we plan to have it running" line is gone.
- **Last page** (now "Lessons and risks"): Test results, Next and Reliability removed. It holds a lessons table with what we
  changed, "What we found and fixed when we merged the code" (moved from page 12), "Risks and how we reduce them" (moved from
  page 12) and the AI endnote. The simulation results are still on pages 12 and 13; robot tests stay in the Tests boxes.
- **"Choices we compared"** (Choice, We chose, Instead of, Why) on pages 7, 8, 9, 10, 11, 12 and 13, from what the team said
  (7 swerve vs mecanum; 8 32 mm vs 48 mm top wheels and the ramps; 9 turret, flywheels, hood, direction; 10 flower mechanism and
  blocker; 11 speed control and position tracking; 12 simulator and code structure; 13 gravity solver vs lookup table).
  Not filled from evidence, so marked as such: page 9's "one flywheel / fixed hood / facing forwards" are my reading of the
  user's words (QUESTIONS 87); `<what else we compared>` x 3 and `<why we start with wheels and the IMU>` are placeholders. Page 6
  (overview) has no section: it is not a subsystem.
- **Removed to make room:** page 9's separate turret box (its reasons are in the Aiming row and the turret cards); page 11's
  3500 RPM limit (page 13 has the 50 RPM and 2 degree limits) and the R503 motors-and-servos row; page 13's turret row (page 9 has it).
- Layout: row heights are weights (proportional): the checker's "needs X but has Y" numbers are content heights, a box adds about
  39 pt of heading and padding.
- **v28:** page 12 now has "What the simulator shows" (pick up 3, aim and score 3; score while still and moving, both alliances; lose the heading sensor: all PASS in simulation, from the code report of 25 Oct 2026). These rows were on the removed test table; the user asked for that table to go from the last page, and this fills the space left on the software page. Robot tests are still not claimed.

## 31. Portfolio v29: instead-of answers, no blocker (2026-11-11)
- Page 8 ramps: polycarbonate instead of 3D printed ramps. Page 10 flower mechanism: the VEX Push Back match-loader idea instead of
  side vertical intake wheels (**my reading** of an answer given in page order: the user's second item). Page 11 position tracking:
  odometry and the IMU instead of motor encoders, because it is much more accurate. Only one placeholder is left (page 5, how we play).
- **Blocker removed** from page 5 (requirements row), page 9 (Aiming row), page 10 (title, box, choices row) and page 11 (parts table).
  Page 10 is now "Flower mechanism, gate, cameras". An unused servo count is not claimed anywhere.
- **Page 11 / 14 odometry:** the parts table has an Odometry pod row; the caption no longer says the code uses wheels and the IMU, and
  page 14 says Odometry + IMU. **Note:** the code on branch `Isaac` still uses wheel (motor-encoder) odometry with the IMU
  (`localisationSource` = wheel-imu-odometry), so the portfolio states a choice the code has not caught up with yet.
- **v30:** page 10's Gate box is plain text (it had a GATE label under a GATE title). Same content as v29.

## 32. Portfolio v31: the first robot results (2026-11-11)
- Pages 7, 8, 9, 13 and 14 now show the user's results (TESTS.md has the exact words and what is missing). Tests boxes are titled
  "Tests on the robot" and use the status TESTED, because no pass mark was given. Shots: only "from the furthest distance, all but 1
  went in" is claimed (the other distances and the number of shots were not given). Jams: "Intake jams", not "per 20 pickups" (no
  pickup count). Page 12 changed tense ("the robot was not finished"); the lookup-table clause "once the robot is finished" was dropped.
  Page 15 lessons gained: the intake jammed once, reversing the rollers cleared it.
- **Left as visible placeholders** (so the hand-in check fails until filled): flower mechanism result and camera status (page 10),
  flywheel speed drop and recovery (page 11), and how we play (page 5).

## 33. Portfolio v32: 4 pollen, 6.5 kg, 3 minutes (2026-11-11)
- Page 5 collect step is "until we hold 4"; page 8 says 3 beam sensors count the pollen and we hold up to 4 (the most G407 allows); page 10
  says the beam sensors tell us we are full (4 pollen). The sensor count (3) was not changed: it is a separate fact (Q84 open on where the
  4th sits). Page 6: light robot, 6.5 kg. Page 7: a pod swap takes 3 minutes (**my reading** of an unlabelled "3 minutes", in the order of
  the questions I had listed). Page 11 caption now just "Our odometry pod" (the team uses odometry). The user confirmed the page 9 and
  page 10 instead-of cells and that the 25 Oct test and simulation results are current, so those pages are unchanged.

## 34. Portfolio v33: three more results (2026-11-11)
- Page 10: flower mechanism result and "both cameras work"; page 11: the speed-drop result (about 200 encoder ticks). Only one
  placeholder is left, page 5 "how we play", kept on purpose at the user's request. Not claimed: the recovery time, or the unit of the 200.

## 35. Portfolio v34: strategy on page 5 (2026-11-12)
- "How we play" is now the team's four points, written in the first person with "RP" spelled out once (ranking points). Nothing was added to
  them. That was the last bracketed placeholder, so the portfolio has none left (the hand-in check also reports none). The scoring plan
  detail (what we score first, where we shoot from, our role with an alliance partner) was not given.

## 36. Portfolio v35 and v36: final check and marking round 5 (2026-11-12)
- **v35 (final check):** serial comma removed on page 7, a noun-comma phrase reworded on page 8, box title "Lessons and
  what we changed"; bullet squares at full size so nothing in the file is under 10 pt (`portfolio_style.py`, `buSzPct`
  100000). Hand-in check: 0 FAIL, 1 WARN (no upload deadline in PROJECT.md).
- **Marking round 5** (`outputs/reviews/marking_loop.md`): about 70 / 100 (range 64-76), a judgement; FTC has no bands.
- **v36 fixes, all from evidence already in the portfolio or logs:** page 7 measured top speed with the sum (3.6 m field
  at 250 cm/s is about 1.5 s, not counting speeding up); page 11 adds the 2 intake motors (page 8) so all 8 motors are
  listed, the 200-tick drop moves to Challenge and Result points to the shots on page 9; page 14 "Planned total";
  page 15 risks add X-lock (tested), jams (tested) and G407 (beam sensors stop at 4), and the 12-degree fix now reads
  "a push past static friction (kS), scaled by battery voltage" to match page 13 (kS 0.06, RobotConfig) and the
  battery-voltage feedforward checked in the code on 2026-11-05. The team should confirm that wording.
- **Left for the team:** real-robot photos; solver or lookup table (pages 13 and 15 disagree); tries behind each result;
  the unit and recovery time of the 200 ticks; the real autonomous score; a cost for each choice; a flower mechanism picture.

## 37. Portfolio v37: design loop on the robot and outreach impact (2026-11-12)
- **Why:** the team's mentor asked for more on how we used the design process on the robot and more on the impact of
  our volunteering.
- **Page 4:** new table "How we used the loop on our robot": the five loop steps for the shooter, the intake and
  transition, and the code and auto-aim. Every cell comes from another page (5, 9, 12, 13, 15) or the logs; nothing new
  is claimed. The CAD process box is now the height of its pictures, and "Coding together" is one paragraph (its
  bug list is on page 15).
- **Page 3** (now "Outreach and impact"): tiles 20+ students and about 15 sessions; the Darkinjung impact (own teams,
  first competitions, awards with our help); Round Square "Reach" renamed "Impact"; mentoring and the Barker VEX
  competition share one box; new box "What outreach did for us" (explaining our robot, leading a group, Round Square
  very rewarding). Numbers and outcomes are the user's answers of 2026-11-12. The mentoring write-up is still not used.
- **Checks:** style checks pass; hand-in check 0 FAIL, 1 WARN (no upload deadline in PROJECT.md); no placeholders.


## 38. Submission check of portfolio_v37 (2026-11-12)
- Hand-in check: 16 pages (cover + 15), A4 portrait, fonts embedded, no placeholders, no AI tool names, nothing under
  10 pt, 2.0 MB; 0 FAIL, 1 WARN (no upload deadline in PROJECT.md).
- Own scans: no links, emails or URLs; PDF metadata has no author or title (no personal details); members as first
  name + last initial only; "AI" only in the endnote; no serial commas; every "(page N)" points to the right page; all
  dates 2026-2027 (A201.E). All 16 pages looked over on a contact sheet: no overflow, overlap or cut-off text.
- Not done: no test print (edge bar against printer margins); pages 13 and 15 still disagree on solver vs lookup table.

## 39. Merged Ethan's v13-v37 here; v38 and v39 (2026-11-28)
- **Found:** Ethan B. pushed commit d49175f ("RAWR", 2026-11-27) with portfolio v13-v37 (made 11-12 Nov). This computer had a
  separate v13 (Claude, 2026-11-27) and the user's hand-edited PDF (2026-11-28), with clashing names. Local work was backed up
  (scratchpad `backup_before_v37/`, patch and copies) and stashed ("local work before merging Ethan v37"), then main was
  fast-forwarded to d49175f. Nothing committed or pushed.
- **Kept from the local work:** `brief/ASSESSMENT.md` (Inspire categories, Sustain, Reach, Connect criteria, how judging works);
  QUESTIONS 89-96 (were 84-91: money, next year, goals, tracking, Wollongong, recruiting, outreach goals, learning plan). The
  user's hand-edited PDF is in `outputs/portfolio/user_edits/portfolio_hand_edited_2026-11-28.pdf`. Claude's earlier v13 is
  superseded and only in the backup.
- **The user chose v37 as the base:** 3 beam sensors; blocker removed; jams, shooting speed and roles as in v37 (not the
  hand-edited PDF); shooting: "we kinda just shoot from one spot now but we're still saying that it works from other
  positions", so v37's tested claim (furthest distance) and design claim (moving hood, shoot from anywhere) stay and the
  hand-edited distance results (0.5 m 6.5/10, 1 m 9/10, 1.5 m 8/10) are not used.
- **v38:** page 2 timeline: Wollongong moved to what happened (13 Nov, Think Award), Macquarie 29 Nov, nationals 5-6 Dec, and a
  line with the Wollongong record from ftc-events (6 matches, 2-3-1, 7th of 10, Think Award).
- **v39:** page 14 uses the team's path picture from the hand-edited PDF (`assets/auto/auto_path_team.png`, 359 x 362 px,
  about 100 dpi printed: a little soft) instead of Ethan's traced route; the seven steps, 45-point plan and status stay as in
  v37 (user). Caption no longer says the numbers match the steps. Source of the field picture not recorded (CREDITS).
- Hand-in check v39: 0 FAIL, 1 WARN (no upload deadline). Interview: Sun 29 Nov 2026 at Macquarie (AUMPQ2).

## 40. Portfolio v40: what Wollongong taught us (2026-11-28)
- **From the user's Wollongong summary** (won Think; electrical inconsistency in the swerve; shooter not tuned; backspin issues,
  no counter roller; no autonomous; poor battery management) and their answers on what changed since (rewired / fixed the swerve
  connectors; tuned the shooter; added a counter roller; the autonomous works now; numbered batteries, charged in rotation and
  checked before each match).
- **Page 15:** new box "Our first event: Wollongong, 13 November (Think Award)" with what went wrong and what we changed.
  To make room, rows that repeat other pages were cut: lessons on mixed units and late merging (the merged-code table and page 4
  cover them), the lookup-table bug (the robot uses the solver), risks for a lost heading sensor (page 12), the turret (lessons
  row 1) and rule G407 (page 8). **Page 9:** choices row "Backspin: a counter roller instead of none". **Page 2:** pointer to page 15.
- Hand-in check: 0 FAIL, 1 WARN (no upload deadline).

## 41. Portfolio v41-v43: the team's 28 November notes (2026-11-28)
- **Source:** the user's pasted notes (roles, competition debrief, page-by-page changes) and answers: 2 counter rollers;
  connectors hot-glued; the simulation interface is our own (no name); no jams in 20 pickups.
- **Page 1:** Isaac H. lead programming (electrical, design, manufacturing); Brandon L. lead assembly (electrical, design);
  Ethan B. assembly. First column renamed "Design and assembly" with Brandon on top.
- **Page 2:** timeline shortened; the spreadsheet removed for a Wollongong debrief table (problem, cause, what we changed)
  and "Goals for Macquarie" (qualify for nationals, auto every match, 3-4 in 4 shots, no brownouts: **drafted from the
  debrief, to confirm**). "Poor battery management" is now "poor coordination of which batteries we used" (user).
- **Pages 7-10:** "What it needs to do" first. Page 7: swerve versions 2022 (Rory, a former member), last season, this
  season (only what we know; no pictures); silicone grease. Page 8: no beam sensors; WD-40 and new belts; no jams in 20
  pickups. Page 9: cards turret 2025-26 → turret 2026-27 → fixed shooter → counter rollers; why a fixed rear shooter (the
  user's five points); counter roller shooter: 63.5 mm flywheel, 2 x 27 mm counter rollers geared to the same surface
  speed, so they spin 63.5 ÷ 27 ≈ 2.35 times faster (**derived by me from "match surface speed"; the team should
  check their real gear ratio**); 1 in 4 → 3-4 in 4 shots per run. Page 10: Push Back inspiration from another team's
  match loader (team not named), our own version; rear camera only, PhotonVision.
- **Page 11:** no beam sensors or front camera; 4 odometry pods averaged; swerve code flow (input, kinematics, optimise,
  output) as in FRC's WPILib; odometry drawing no longer cut off. **Isaac H. to check.**
- **Page 12:** how our simulator works (our hardware I/O interface fakes encoder ticks; same idea as FRC's hardware map
  behind an I/O interface; lets us run the auto before the robot).
- **Page 13 rewritten:** 4 odometry pods averaged, rear camera AprilTag pose by trigonometry, extended Kalman filter;
  aim vector from the goal to the robot 0.4 s ahead (feedforward) with a diagram (`project/src/auto_aim_diagram.py` →
  `assets/diagrams/auto_aim_vector.png`, a sketch not to scale); lookup table chosen over a gravity solver and why. The
  old shot-check table, PD gains and 0.07 s look-ahead were removed as "very incorrect" (user).
- **Page 14:** "What it can use" removed; status says no auto at Wollongong, written and run since.
- **Page 15:** code lessons and the merged-code table replaced by the Wollongong lessons; risks add loose connectors and
  no jams in 20 pickups. AI endnote kept (user: keep it for now; removing it would break A201's credit rule).
- **v42:** the Greek letter ω made PowerPoint fall back to Cambria, so the maths is in words. **v43:** page 7 gear
  drawings larger, page 9 card names shorter, diagram text bigger. Hand-in check v43: 0 FAIL, 1 WARN.

## 42. Portfolio v44-v46: annotated pictures and a full review (2026-11-28)
- **Asked for:** "review everything, make sure it's all perfect", annotate diagrams and photos.
- **Labels added** (handwritten style, arrows): page 6 chassis exploded view (side panel, swerve pod, base plate); page 8
  assembly views (gecko wheels, gears, intake; mecanum rollers, gears); page 10 rear camera drawing (the old front-camera
  highlight removed, since the robot now has the rear camera only) and a side section labelled collect, hold, release.
  Not labelled: the chassis underside and the Round Square photo (no clear space; text on a photo is low contrast, A201),
  and the team's auto path (which step is where is not recorded).
- **New sketch:** page 9 counter roller shooter (`project/src/counter_roller_diagram.py`): pollen squeezed between the
  flywheel (63.5 mm) and 2 counter rollers (27 mm) on the opposite side (user, 2026-11-28), turning opposite ways so the
  pollen leaves with no spin. Marked "sketch, not to scale". The test table moved under "Why a fixed rear shooter".
- **Page 2:** Wollongong in three tiles (2-3-1, 7th of 10, Think Award). **Page 14:** the auto path is now full width.
- **Matched to the new auto-aim (user: "use the information from the updated portfolio"):** page 4 simulate row (no
  12-degree line), page 5 scoring cycle (Collect, Aim along the aim vector, Spin up from the lookup table, Feed; no 0.1 s
  settle), page 10 release (the gate opens once the shot is ready), page 15 risk (Kalman filter instead of the removed
  calibration check). Page 11: 3-4 in 4 now credited to the counter rollers as well as the speed control.
- **Checks:** hand-in check 0 FAIL, 1 WARN (no upload deadline); 36 pictures all with alt text; every "(page N)" correct;
  no serial commas; tests 50 pass (a dark-theme copy of the new camera drawing was needed).

## 43. Portfolio v49: the teammate's v48 merged with v44-v46 (2026-11-28)
- **Source:** `user_edits/portfolio_v48_teammate_2026-11-28.pdf` (built at 19:27 from a script not in this repo). Its text
  was compared with v43 page by page: changes on pages 1, 2, 9, 10, 14 and 15 only. Those pages were rewritten in
  `build_portfolio.py` to match it word for word (inline bold inside table cells is not supported here, so dropped).
  Its 3 pictures not in the repo were rendered from the PDF (flower mechanism 1243 x 965 px; blocker 267 x 405 px: soft).
- **Kept from v44-v46:** labels on pages 6 and 8, Wollongong tiles (page 2), page 4 simulate row, page 5 cycle, page 11
  speed control, the counter roller sketch, the larger auto route picture. **Replaced by v48:** page 10's camera drawing
  and hold/release section (v48 rebuilt page 10 with the gate, camera text and blocker).
- **Where v48 and v44-v46 disagreed:** v48's gate 'ready for 0.1 s' (page 10) is the team's newest words, so page 5's
  Feed step says the same; v48's new lesson 'aiming 12 degrees short was fixed in the simulator' kept (added by the
  teammate); v48's calibration risk dropped (it came from the auto-aim the user called incorrect, and v48 already has
  'Localisation drifts' for the camera and filter).
- **New:** Ethan B. manufacturing (Isaac H. no longer lists it); page 9 counter roller CAD from the user, highlight
  recoloured to the page yellow, labelled counter rollers, flywheel and gears; V4 card uses the plain view; the sketch is
  in 'Why no backspin'; page 9's one-row test table removed for room (the Fix says 'tested on the robot: 3-4 in 4');
  page 4 shooter build row adds the counter rollers; page 10 flower mechanism labelled.
- **Numbering:** v47 and v48 were made on the teammate's computer, so this is v49 (built with --draft to that name,
  since save_versioned only sees local .pptx files). Hand-in check 0 FAIL, 1 WARN; tests 50 pass.
