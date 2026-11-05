---
name: pptx-edit
description: Safely edit or extend an existing PowerPoint (.pptx) deck by duplicating its closest slide and changing text or images, keeping its masters, layouts and look. Use when the user gives a .pptx to add slides to, fix or restyle, or wants project content placed into an existing deck.
---

# Edit an existing deck

Tools are in `general/tools/`. Also load `anthropic-skills:pptx`.

1. Never edit the user's file in place. Save each result as the next version (`<name>_vNN.pptx`) in
   `project/outputs/<deliverable>/` and add a line to its `VERSIONS.md`. Never overwrite an earlier version.
2. Inventory first: `python general/tools/inspect_pptx.py deck.pptx --output project/outputs/renders/deck.json`
   (or `pptx_ops.ps1 -Action Inspect` for layouts and tables). Find the slide that already does what you need.
3. Render candidate slides and look at them (`render_check.ps1 -Only 3,5`).
4. Duplicate the closest slide rather than inventing a theme: `pptx_lib.duplicate_slide`, `move_slide`, `set_runs_text`
   (keeps run formatting), or a JSON plan for `pptx_ops.ps1 -Action ApplyPlan` (`general/tools/EDIT_PLAN.md`).
5. Images: only ones the user named; add alt text; scale inside the deck, never alter source files.
6. Render every changed slide, look at it, fix overflow and collisions, repeat.
7. Run `.ps1` files as `powershell -NoProfile -ExecutionPolicy Bypass -File ...`.
8. Log the change in `project/logs/DECISIONS.md`.
