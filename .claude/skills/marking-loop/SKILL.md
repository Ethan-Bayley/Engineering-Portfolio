---
name: marking-loop
description: Mark a deliverable (brochure, poster, report) against the project's rubric, fix what can be fixed from the repo, and mark again until only items that need the user are left. Use when the user asks for a mark, "how do I get full marks", "mark it and fix it", or a review loop.
---

# Mark, fix, mark again

1. Read `project/brief/ASSESSMENT.md` (task sheet and rubric). If the rubric has no mark bands, say so and use
   `general/guides/RUBRIC_GUIDE.md` (ISEF engineering criteria, mapped) for what "strong" means. Never quote invented bands.
2. **Mark (read-only pass).** For each criterion: a mark or a strong / partly / missing verdict, and the evidence (page,
   section). Give an overall estimate with a range and say it is a judgement.
3. **List every gap** in `project/outputs/reviews/marking_loop.md` as
   `### [Critical|High|Medium|Low] title` with location, evidence, fix, and who can fix it: **Claude** (from the repo) or
   **You** (needs the user: photos, results, sketches, own words, decisions). Critical = false or unsafe content;
   High = a required item missing or an unsupported claim.
4. **Fix the Claude items** in the build script, rebuild as a new version (`_vNN`), export with
   `python general/tools/export_pdf.py <deck> --render <dir>` and fix every overflow/PAST-BOX/OVERLAP flag.
5. **Mark again.** Repeat 2-4 until only You items remain. Log each round in the review file.
6. Hand the user the You list, most marks first. Never fill a You item with invented content: mark it "Still to add".
7. Write a short `FULL_MARKS_CHECKLIST.md` in `project/outputs/reviews/` if the user wants a checklist.
