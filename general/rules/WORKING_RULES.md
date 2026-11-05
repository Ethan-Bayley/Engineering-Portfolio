# Working rules

These apply to every project made from project-template. A project can add its own rules in `project/PROJECT.md`
("Project rules"); where they differ, the project's rule wins for that project.

## Git
- Commit and push **only when the user says so**. Show what will be committed first.
- No Claude attribution in commits or PRs: no "Co-Authored-By: Claude" trailer, no "Generated with Claude Code" footer.
- Never force-push, rewrite history or delete branches without asking.
- Large generated files (renders, contact sheets) stay out of git (`.gitignore`); versioned decks and PDFs go in.

## Hardware safety
- No test, script or tool sends commands to real motors, servos or other devices on its own. Dry run first (print what
  would be sent); the user runs real moves themselves.
- New hardware: one part at a time, low speed, with limits and a stop.

## Writing
- Australian English (colour, centre, analyse, metre, grey, programme only for TV, "program" for software).
- No serial comma: "red, green and blue".
- Plain words; define a term once. Voice as the user chose in `project/PROJECT.md` (default "we").
- Use skill `humanizer` on long text before it goes in a deliverable.

## Logging (skill `log-work`)
- After any change to behaviour, results, the build or a deliverable: what changed and where, options considered and why,
  how it was measured (numbers with units), what did not work, and what is still not done.
- Append; never delete old entries. If an earlier conclusion was wrong, add a new entry saying so.

## Files and versions
- Deliverables: `project/outputs/<deliverable>/<name>_vNN.pptx` (+ PDF), logged in that folder's `VERSIONS.md`.
- If the user edits a generated file by hand, diff a fresh draft build against it and bring the edits into the build
  script before the next rebuild.
- Photos: originals stay untouched in `project/assets/photos/raw/`; prepared copies go in `ready/`
  (`general/tools/photo_prep.py`). Credit anything not the user's own in `project/assets/CREDITS.md`.
