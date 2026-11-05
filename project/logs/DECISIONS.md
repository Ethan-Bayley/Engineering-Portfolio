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
