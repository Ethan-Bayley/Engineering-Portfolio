---
name: design-system
description: The visual design system (colours, Inter type, double-rectangle content boxes, numbered caps headings, highlights, stat cards, tables, timeline, spacing). Use whenever building or restyling any brochure page, poster, slide or PowerPoint or when asked how something should look.
---

# Design system

Applies to every brochure page, poster and slide deck made in this repo. Colours can be changed per project in `project/design.json`.

1. Read `general/design/DESIGN_SYSTEM.md` in full before drawing anything. It is the rulebook; this skill is the summary.
2. Build with `general/design/design_system.py` (python-pptx), not with hand-placed shapes:
   ```python
   import sys; sys.path.insert(0, "general/design")
   from design_system import Doc
   doc = Doc("brochure")            # A4 landscape + page numbers  |  Doc("poster") = A3 portrait, no page numbers
   page = doc.page("Design")        # big caps title in the main colour, no image beside it
   top, bottom = page.rows(page.area, 1, 1)          # rows()/cols() put exactly the gap G between boxes
   box = page.box(top, "research", "Research findings")   # -> "01 - RESEARCH FINDINGS", green by meaning
   box.text(box.content, ["Paragraph with **bold**.", "- a bullet"])
   doc.save_versioned("<deliverable>", "<name>", "what changed")   # project/outputs/<deliverable>/<name>_vNN.pptx; refuses if a rule is broken
   ```
3. The rules that are easy to get wrong:
   - Box colour **by meaning**: green = research/results, orange = design/process, purple = method/code, red =
     problem/testing. **Two boxes sharing an edge are never the same colour** (the code swaps and notes it).
   - **The main colour `#1d497d` is never a content box.** It is only for page titles and top-level items.
   - Headings are `NN - CAPITALS`, numbered **continuously** across the whole document.
   - **One gap G between all boxes** (1.6 % of page width): always lay out with `page.rows()` / `page.cols()`.
   - **Highlighted text** = `box.highlight(r, text, kind)`: a rounded left-bar panel. kind `general` (box colour),
     `result` (green) or `caution` (yellow). **Full-outline stat cards are only for key numbers**; every card in a box is a
     different colour (1-3 cards avoid the box colour; 4 cards use each colour once). Table header rows are in the box colour. Step badges are rounded.
   - Inter only (titles Inter Bold; static Inter must be installed for the PDF). Small text is slate, never green or orange (contrast, section 1 of the spec).
4. Render and look: `powershell -NoProfile -ExecutionPolicy Bypass -File general/tools/render_check.ps1 -Deck <pptx> -OutDir <dir>`.
   The save check does not catch text overflow; the render report and the PNGs do.
5. Every new PowerPoint is versioned (`_vNN`) through `save_versioned`. Content rules (never fabricate, credit sources,
   MEASURED / PROPOSED / NOT TESTED) come from `project/logs/`.
6. If the user changes a rule: update `DESIGN_SYSTEM.md` (and its change log), `design_system.py`,
   `tests/test_design_system.py` in the project-template repo, then pull them into projects (skill `pull-template-updates`).
7. **PDF:** always `python general/tools/export_pdf.py <deck> --render <dir>` (plain PowerPoint export gives Calibri on this PC).
8. Extra parts: `page(..., cover=True, label=...)`, `box.flow()`, `box.gantt()`, `box.table(status_col=)`, `box.head()`,
   `box.stack()`, `box.highlight()`, `box.stats()`, `box.steps()`, `box.timeline()`, `box.annotate()`.
