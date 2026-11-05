---
name: manage-document
description: Coordinate end-to-end work on the project's main deliverable (brochure, poster, report): page plan, evidence intake, photos, versions, checks and hand-in. Use for broad requests that mix several of these, or "make the brochure", "what's left", "get it ready to hand in".
---

# Manage the deliverable

1. Read `project/PROJECT.md`, `project/brief/ASSESSMENT.md`, `project/logs/PREFERENCES.md` (the user's standing wishes).
2. **Page plan.** Map every required section/criterion to pages (a table in `project/brief/PAGE_PLAN.md`): page, title,
   section, evidence, status. Respect page limits unless the user says otherwise.
3. **Evidence intake.** New photos go to `project/assets/photos/raw/`; prepare them with
   `python general/tools/photo_prep.py` (upright, resized, into `ready/`) and list them in
   `project/assets/CREDITS.md` (own / source and licence).
4. **Build** with skills `design-system` and `draft-page`; one build script per deliverable (start from
   `general/templates/build_brochure.py`); every save is a new version.
5. **Check** with `export_pdf.py --render`, skill `pptx-contact-sheet`, then `marking-loop` before hand-in.
6. **Hand-in.** Skill `hand-in-check` (runs `general/tools/hand_in_check.py`: fonts, page limit, placeholders,
   deadline). Nothing marked "Still to add" that the user can still supply.
7. If the user edits the .pptx by hand, diff a fresh draft build against it and bring the edits into the script before
   rebuilding.
