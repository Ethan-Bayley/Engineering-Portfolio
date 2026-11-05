# Full-marks checklist for brochure_a4_v25 (2026-10-23)

Estimated mark now: about 77/100 (72-82). Judged against the task sheet and the ISEF engineering criteria
([ASSESSMENT.md](ASSESSMENT.md)); the school rubric has no bands, so "full marks" means every element done fully and shown
with evidence. **Due today, Friday 23 October, before 3:20 pm.** "You" = only you can do it. "Claude" = can be done from the repo.

## Before anything else
- [ ] **You:** decide which brochure is handed in: the A4 design-system line (brochure_a4_v25) or your partner's v12-style line (v30). Do not hand in both.
- [ ] **You:** decide the page count. The sheet says 14-16; v25 is 22. Full marks for presentation needs 16.

## 1. Significance (now about 17/20)
- [ ] **Claude:** add one sentence on who would use it (people with a hand amputation using a powered prosthesis) and how many, from the sourced papers.
- [ ] **Claude:** make impact claims measurable or clearly hedged ("could lower cost" -> what it removes: depth camera, GPU, training data).
- [ ] **Claude:** add a one-line comparison table of ours vs the four papers (training data, depth camera, places every fingertip) on page 4.

## 2. Methodological approaches (now about 17/20)
- [ ] **Claude:** expand the risk table: likelihood and consequence columns, and 2-3 more risks (supply sag, servo overheating, wrong finger order), each with what was done.
- [ ] **Claude:** show the time plan against what actually happened (planned vs actual bars), from the dates in the repo logs.
- [ ] **Claude:** say once, clearly, why each criterion's threshold was chosen.
- [ ] **You:** confirm the risk ratings are yours.

## 3. Creativity and innovation (now about 14/20) - biggest gap with section 4
- [ ] **You:** draw your own sketches by hand (pen on paper is fine): the hand with the camera in the palm, the grasp plane, an early idea you dropped. Photograph them. The sheet says "your sketches".
- [ ] **You:** draw a mind map of the project (problem, options, ideas, constraints). Photograph it.
- [ ] **Claude:** put them on the sketches page; the gemini_* sketches are our own pen sketches (Gemini only removed a stray pen), so they count; done in v27.
- [ ] **Claude:** name the inventive steps in one place with a before/after for each (grasp plane, force check, object permanence, steadiness rule).
- [ ] **You:** photo of the final design: the hand with the camera mounted in the palm.

## 4. Execution, construction and testing (now about 14/20) - biggest gap
- [ ] **You:** test real grasps on the real hand. 3-4 everyday objects (for example a ball, a cup, a box, a bottle), 5 tries each, record held / not held for 5 seconds, and whether the vision planner or the sliders moved the fingers.
- [ ] **You:** photograph at least two successful grasps and one failure.
- [ ] **Claude:** add a results table and a bar chart of those tries; update criterion 6 from NOT TESTED; compare with the simulation (80 of 80).
- [ ] **You:** trigger one safety trip on purpose (block a finger gently at low speed) and note what happened; then the trip row can be MET.
- [ ] **You:** if possible, a photo of the camera mounted on the hand and one camera view from it.
- [ ] **Claude:** a single "testing summary" table across all conditions and trials (colour/grey, still/moving, steady/shaken, real hand).
- [ ] **Claude:** final evaluation: one paragraph per criterion on how far it was met, then benefits, limits and further research.

## 5. Presentation and communication (now about 15/20)
- [ ] **Claude:** cut to 16 pages: merge speed + outlines, steadiness + grasp plane, setup + apps, keep testing and evaluation.
- [ ] **Claude:** raise body text from 9.5 pt where space allows; no text under 8 pt.
- [ ] **Claude:** annotations on photos (labels and arrows pointing at parts: servo, linkage, camera).
- [ ] **Claude:** check every page number on the contents page after the cut.
- [ ] **Claude:** spell check (Australian English) and one read-through for repeated sentences.
- [ ] **You:** evidence of independence (5.4): one or two of your own notes or decisions in your words, for example why you chose option C.

## Hand-in
- [ ] **Claude:** export the final PDF with tools/export_pdf.py (Inter embedded), check it opens and has the right page count.
- [ ] **You:** upload the PDF to Canvas before 3:20 pm.
- [ ] **You:** bring the practical (the real hand, and the simulation on a laptop) to class.
- [ ] **You:** commit and push when you are happy.

## Done in brochure_a4_v26 (2026-10-23; the user and partner chose this design; going over the page count is allowed)
- Who it is for (page 3); comparison table of ours vs the four papers (page 4); impact kept specific.
- Criteria with the reason for the thresholds; schedule planned (green) vs actual (purple) from repo dates (page 5).
- Risk assessment page: likelihood, consequence, 8 risks including supply sag, overheating and finger order (page 6).
- Mind map (computer-drawn, labelled as such) and a before/after table of what is new (page 11).
- Test summary of every test, condition and result (page 23); final evaluation, benefits, limits, further research (page 25).
- Labelled photos and screenshots (pages 21, 22); credits on their own page (27); spelling checked (Australian English).
- 27 pages, Inter embedded, render check clean.

**Still needs you (cannot be made from the repo):** counted real grasps and their photos; your own pen sketches and a hand-drawn
mind map (the computer one is labelled); a photo of the camera on the hand; one or two decisions in your own words.
