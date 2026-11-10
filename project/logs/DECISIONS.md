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
