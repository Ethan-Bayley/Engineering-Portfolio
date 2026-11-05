---
name: poster-design
description: Design and build posters, slide decks and PowerPoint (.pptx) files for this project. Use when the user asks for a poster, presentation, slides or PowerPoint, or to add the project's images or results to one.
---

# Poster and presentation design

1. Read `project/PROJECT.md` (what, who, deliverables, look) and load skill `design-system`
   (`general/design/DESIGN_SYSTEM.md`, built with `general/design/design_system.py`).
2. For `.pptx` work also load `anthropic-skills:pptx`. Use `pptx-edit` to change an existing deck and `pptx-review` to check one.
3. Choose images from `project/assets/` and write the text yourself, but only true, sourced content; list the choices so the
   user can change them.
4. Every new PowerPoint is versioned: `doc.save_versioned("<deliverable>", "<name>", "what changed")` writes
   `project/outputs/<deliverable>/<name>_vNN.pptx` and logs `VERSIONS.md`.
5. One build script per deliverable in `project/outputs/<deliverable>/`. Do not hand-edit generated files; if the user
   does, bring their edits into the script before rebuilding.
6. Export and check: `python general/tools/export_pdf.py <deck> --render <dir>`; fix every flag.
7. Alt text on every picture; credits for anything not the user's own (`project/assets/CREDITS.md`).
8. Log the work in `project/logs/DECISIONS.md`.
