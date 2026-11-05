---
name: hand-in-check
description: Final check before a deliverable is handed in: run general/tools/hand_in_check.py on the PDF (fonts embedded, page limit, page size, placeholders, AI mentions, tiny text, file size, deadline), then a short manual checklist. Use when the user says "check it before I hand it in", "is it ready", "final check", or the deadline in PROJECT.md is close.
---

# Hand-in check

1. Find the deliverable and its limits in `project/PROJECT.md` and `project/brief/ASSESSMENT.md` (page limit, file
   size limit, format, how it is handed in).
2. Export the newest version if there is no PDF for it yet: `python general/tools/export_pdf.py <deck>.pptx --render
   project/outputs/renders/vNN` (fonts embedded, layout flags).
3. Run the check:
   ```bash
   python general/tools/hand_in_check.py --deliverable <name> --max-pages <limit> --max-mb <limit>
   ```
   Fix every FAIL. Look at each WARN and tell the user which are fine (for example a source that names an AI tool on
   purpose).
4. Manual checklist (look at the renders or a contact sheet, skill `pptx-contact-sheet`):
   - Names, class and title on the cover; page numbers run in order; contents page matches the pages.
   - Every required section in the rubric has a page (`project/brief/PAGE_PLAN.md` if there is one).
   - Every result on a page is in `project/logs/TESTS.md` or `DECISIONS.md`; every picture not the user's own is in
     `project/assets/CREDITS.md` and credited on the page; a reference list if the task asks for one.
   - Nothing marked "not tested" is described as working.
   - The PDF opens and looks right in a browser (Canvas preview uses one).
5. Tell the user: the file to hand in (full path), its page count and size, the deadline and time left, and anything
   they still have to do themselves (sign-off, partner's part, a printed copy). Do not upload or submit anything.
6. Log it in `project/logs/DECISIONS.md`: which version was checked, the results, what was fixed.
