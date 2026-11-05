# Brochure marking loop (started 2026-10-22)

The user asked for a loop: mark the brochure, change it to act on the feedback, mark it again, until nothing is left that
can be fixed from the repo. Marking uses the school rubric (five criteria, /20 each, no bands) and the ISEF engineering
criteria (presentation/ASSESSMENT.md). Each pass is read-only; fixes happen between passes. Severity as in REVIEW_LOOP.md:
Critical = false or unsafe content or unreadable output; High = unsupported claim, contradiction, or a required item missing;
Medium = weak hierarchy or inconsistency; Low = wording or alignment. Page limit for this loop: up to 20 (user, 2026-10-22;
the task sheet says 14-16, so this is a known risk the user accepted).

## Iteration 1: brochure_v21 (16 pages)

### [Critical] The brochure says the real hand has not arrived or been tried
- Location: page 2 (key events), 3 (constraints), 7 (options intro), 8 (why we simulated; tools table), 15 (practical note,
  limitations), 16 (reflection; next steps). 11 places in build_brochure_a4.py.
- Evidence: the user says the hand is built and tested (2026-10-22). APP_DECISIONS.md section 13 records a test on the real
  hand: 8 of 8 servos answered (IDs 1-8, COM3, 1 Mbaud, 5.1-5.3 V, 17-20 C), every +-30 deg spin and the middle position within
  0.6 deg: ALL PASS.
- Risk: false statements in the hand-in.
- Fix: say the hand arrived late and was built; keep statements that were true at the time (for example the options page) in
  the past tense.
- Resolution: fixed in v22.

### [High] No pages on the physical hand: build, testing, evaluation (user request; criteria 3, 4.1, 4.2, 4.3)
- Evidence: nothing about the real build in v21. The repo has: the build and servo tools (tools/setup_servos.py,
  center_servos.py, open_close_hand.py, hand_viewer.py, servo_config_tool.py), servo_config.json (directions, limits), the
  servo test results above, and two mistakes found (false FAILs from spinning around start angles near the end of travel, up to
  317 deg of wrap-around; servos 7 and 8 silent at first from a power/adapter problem).
- Fix: four pages before the reflection: build, control and safety, testing, evaluation of the physical hand.
- Resolution: added in v22. **Photos of the build and the grasp-test results on the real hand are not in the repo**; the pages
  show marked spaces for them (TODO for the user).

### [High] Section 4 page budget
- Evidence: with the four new pages, section 4 (Execution) runs pages 13-20 (8 pages) against the sheet's 4-6.
- Fix: none without dropping content; the user chose up to 20 pages. Noted, not fixed.

### [Medium] Option pictures on page 7 are small since the reasons were added
- Resolution: left as is; the reasons matter more (user asked for them).

### [Low] Page 9 "What is new" table rows are tall and sparse
- Resolution: see iteration 2.

## Iteration 2: brochure_v22 (20 pages) - in progress
- [High] Contents list ran 42 pt past its box on page 2 (20 pages listed). Fixed before saving v22: taller box, columns rebalanced.
- [High] Real grasp results and photos still missing (pages 16, 18, 19). Needs the user. Six new photos in presentation/Photos
  (Image 35-40) may be of the hand: to check.
- [Medium] Page 17 tool names wrap mid-word ("open_close_hand.p y"); table rows sparse. To fix.
- [Medium] Page 19 bottom boxes half empty. To fix.
- Resolution (v23): page 17 tool column widened (no mid-word wraps); page 19 tightened and two sourced points added.

## Iteration 3: v23 drafts
- [High] User's photos 36-40 of the real build placed: page 16 (four build photos), page 18 (test set-up). Photo 35 shows a person,
  not the hand, so it was left out (names and people stay off inside pages). Fixed.
- [Medium] Page 16 steps spread thin and photos small; page 18 portrait photo tiny in a short box; page 19 bottom boxes half
  empty. Fixed (narrower steps column, full-height photo column, two more sourced points).
- [High] Page 16 servo-map table grew into the line under it. Not caught by the check, found by looking. Fixed, and the render
  check now reports OVERLAP when a table grows into anything placed below it.

## Iteration 4: brochure_v23 (20 pages) - nothing left that can be fixed from the repo
Render check (text, past-box, table growth, overlap): clean on all 20 pages; Inter embedded. Remaining findings all need the user:
- [High] Grasp tests on real objects (page 18 box 57, page 19 table): object, tries, held 5 s. Verdict NOT TESTED until added.
- [High] Criterion 3 asks for sketches and a mind map: none in the repo.
- [Medium] Section 4 runs 8 pages (13-20) against the sheet's 4-6; the brochure is 20 pages against 14-16 (user chose 20).
- [Low] The guide's per-servo fine-tuning is not done (stated on pages 16, 19, 20).

## v24
- [Medium] Page 6 had spare space and small CAD images; plan table moved left, four CAD/board images right. Overlap check fixed (it missed grown tables) and proven on a broken test deck. Still open: real grasp-test results (High), sketches/mind map (High).
