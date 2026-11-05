---
name: setup-project
description: Set up a new project cloned from project-template. Interview the user (what the project is, goal, deadline, team, rubric, deliverables, look) and fill the project/ folder, PROJECT.md, the brief, the logs and design.json, then connect the template remote. Use when the user says "set up this project", "new project", or project/PROJECT.md still has its placeholder text.
---

# Set up a new project

Run this once, right after the repo is cloned for a new project. Check first: if `project/PROJECT.md` no longer contains
`<!-- NOT SET UP -->`, the project is already set up; ask before redoing anything.

## 1. Interview (use AskUserQuestion; up to 4 questions per round, 2-4 rounds)
Ask, in plain words, and offer sensible defaults:
1. **Name and type.** Project name (used for folder names and the deck name); type: school assessment, engineering build,
   software, or a mix.
2. **What it is.** One or two sentences: the problem and what will be made. The goal, ideally measurable.
3. **People and dates.** Team names (cover only) and the deadline (date and time). Who to ask about the rules (teacher).
4. **The task.** Is there a task sheet or rubric? Ask the user to paste it or drop the file in `project/brief/`.
   Page or word limits; required sections; how it is handed in (PDF, Canvas, printed).
5. **Deliverables.** Brochure (A4 landscape), poster (A3 portrait), slides (16:9), report, code, a physical build. Several is fine.
   For a competition entry, find and save the official rules (page limits, sizes, minimum font size, what must be
   credited) before anything else. A deliverable with its own look keeps it in `project/design/` (its own fonts in
   `project/design/fonts/`, picked up by `export_pdf.py` and `install_fonts.ps1`), not in `general/`.
6. **Look.** Keep the default colours (navy title, green/orange/purple/red boxes, Inter) or give new ones (hex). Australian
   English unless told otherwise.
7. **Hardware.** Does the project drive motors or devices? (turns on the hardware safety rule's reminders.)

Do not guess answers that matter for marks (deadline, limits, rubric). If the user does not know, write `TODO` and say so.

## 2. Fill the project folder
- `project/PROJECT.md`: replace every placeholder; remove the `<!-- NOT SET UP -->` line. Keep the section headings.
  Write the deadline as `Deadline: YYYY-MM-DD HH:MM, <how it is handed in>` (the hand-in check reads it).
- `project/brief/SCHEDULE.md`: if the user knows the main stages, one row each with planned dates (skill `schedule`).
- `project/brief/ASSESSMENT.md`: the task sheet text as given (verbatim), deadline, limits, required sections, and a
  criteria table (criterion, what it asks, where it will be shown). If there is no rubric, write "None given".
- `project/logs/PREFERENCES.md`: a dated entry with everything the user said in the interview.
- `project/logs/DECISIONS.md`: first section "Project set up" with the date and the choices made.
- `project/design.json` only if the user changed the look (keys: main, green, orange, purple, red, and *_tint; hex
  without #). Delete nothing else.
- Rename nothing in `general/` or `.claude/`; those are shared with the template.
- For each deliverable, copy its starter from `general/templates/` (`build_brochure.py`, `build_poster.py` or
  `build_slides.py`) to `project/outputs/<deliverable>/build_<deliverable>.py`, set `DELIVERABLE` (and `SECTIONS`, the
  rubric's sections, for a brochure) and run it once to check it builds (`--draft`). Delete nothing else.
- Software (or a mix with code): make `project/src/` as in `general/context/SOFTWARE.md`, with `README.md` from
  `general/templates/src_README.md` filled in as far as known.

## 3. Connect git (do this yourself; adding or renaming remotes is local and safe)
The template is `https://github.com/Ethan-Bayley/project-template.git`.
1. Run `git remote -v` and handle each case without asking:
   - `origin` points at project-template (the user cloned the template): `git remote rename origin template`.
   - No `template` remote and `origin` is something else (the user cloned or created the project repo):
     `git remote add template https://github.com/Ethan-Bayley/project-template.git`.
   - No git repo at all (files were copied): `git init -b main`, then add `template` as above.
2. If there is no `origin` now, ask the user once (in the interview's last round) for the project's GitHub URL
   (they create an empty private repo first; offer "I'll add it later") and run `git remote add origin <url>`.
3. Check with `python general/tools/template_sync.py status` (it fetches the template) and show `git remote -v`.
4. Commit and push only when the user says (CLAUDE.md). Offer: "Commit the set-up?" No Claude attribution lines.

## 4. Finish
Tell the user what was filled, what is still TODO, and the next steps: put photos in `project/assets/photos/raw/`,
start the log, and which skill builds the first deliverable (`draft-page`, `poster-design`, `design-system`).
