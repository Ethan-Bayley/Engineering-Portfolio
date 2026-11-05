---
name: draft-page
description: Draft one or more pages of a brochure, poster or report from the project's own evidence (logs, results, photos, CAD, research) in the design system. Use when the user asks for a page, a section, documentation of progress, or to add something to the deliverable.
---

# Draft a page

1. Read `project/PROJECT.md`, `project/brief/ASSESSMENT.md` (which criterion this page serves) and the logs
   (`project/logs/`). Load skill `design-system`.
2. Gather the evidence: numbers from the logs (each with where it came from), the user's photos
   (`project/assets/photos/ready/`), CAD and screenshots. If a needed fact is missing, ask; do not invent it.
3. Plan the page: one idea, 2-5 boxes, a picture or chart where it explains better than words. Section label = the
   rubric section it serves. Box headings are plain words.
4. Build it in the project's build script (`project/outputs/<deliverable>/build_<deliverable>.py`) with
   `general/design/design_system.py`. Keep text short; label anything planned, assumed or not tested.
5. Save a new version, export the PDF, check the render report and look at the page. Fix flags.
6. Log what changed in `project/logs/DECISIONS.md`.

Writing: the voice the user chose (default "we"), Australian English, no serial comma, plain words; use skill
`humanizer` on long text.
