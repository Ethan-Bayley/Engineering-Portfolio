---
name: pptx-review
description: Review a finished poster or PowerPoint for accuracy, honesty, layout and accessibility using the independent review loop. Use before calling a poster or deck done, or when asked to check, audit or critique one.
---

# Review a poster or deck

1. Read `general/guides/REVIEW_LOOP.md` and the project's logs (`project/logs/`).
2. Render and check: `python general/tools/export_pdf.py <pptx> --render project/outputs/renders/<name>`; read the report
   (OVERFLOW-H, PAST-BOX, TABLE-GROWS, OVERLAP) and look at every PNG.
3. `python general/tools/inspect_pptx.py <pptx> --output <inv.json>`, then
   `python general/tools/audit_deck.py <inv.json> --output project/outputs/reviews/<name>-audit.md` (heuristics only).
4. Review read-only (a separate sub-agent only if the user asked; otherwise a separate pass, stated). Check every number
   against the logs, that nothing overstates what was tested, that only the user's chosen images are used, text size, alt text.
5. Write findings (Critical/High/Medium/Low, location, evidence, fix) to `project/outputs/reviews/`. Fix, rebuild, re-review.
6. Never present a quality score as official.
