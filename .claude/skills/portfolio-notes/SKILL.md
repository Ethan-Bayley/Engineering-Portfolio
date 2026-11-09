---
name: portfolio-notes
description: The FTC portfolio's running context (this project only, 11143 Barker Yellowbacks). Read project/NEXT_STEPS.md (what comes next, what the team said in meetings) and project/QUESTIONS.md (questions whose answers fill the portfolio) before any portfolio work; put answers into the pages; add the team's spoken or typed meeting notes to it; tick off next steps. Use when the user says "what's next", "add this to the notes", passes on what was said in a meeting, gives design reasons, parts or results, or starts a new session on the portfolio.
---

# Portfolio notes (this project only)

Not part of project-template: do not copy this skill there (`template_sync.py push-hint` will list it; skip it).

The file: [project/NEXT_STEPS.md](../../../project/NEXT_STEPS.md).
- **Part A, Next steps:** what is left, team items (most marks first) and Claude's items.
- **Part B, Team notes:** what the team said in meetings, in their words, with the page each goes on and a status
  (ok / **check** / needs a number).

## At the start of portfolio work
1. Read `project/NEXT_STEPS.md` and `project/QUESTIONS.md` with `project/PROJECT.md`.
2. Say in one or two lines what is next and anything marked **check** that blocks the work.

## When the team gives notes (spoken transcripts, typed notes, answers)
1. Speech-to-text is messy: read for meaning, keep their words, fix only obvious mishearings and mark each guess
   **check** with what was heard (for example "6 ml" read as 6 mm).
2. Add a dated block to part B: one row per fact or reason, the page it goes on, the status.
3. Add nothing the team did not say: no numbers, reasons, materials or results of your own. If something needs a
   number to be useful on the page, set status "needs a number" and add it to part A.
4. Remove or tick items in part A that the notes answer; add new ones they raise.
5. Also append a short dated entry to `project/logs/PREFERENCES.md` (skill `log-work`).
6. Use the notes on the pages only in a new version (`build_portfolio.py`, `_vNN`); where a note disagrees with the
   code or the logs, ask before writing it.

## When the team answers QUESTIONS.md
1. Answers may come in chat or be typed after **Answer:** in `project/QUESTIONS.md`. Copy chat answers into the file
   under their question, dated, in the team's words.
2. Put each answer on the page in brackets, replacing its `<...>` placeholder, in a new version. Results go in
   `project/logs/TESTS.md` too (date, tries, conditions); "don't know" leaves the placeholder.
3. Mark the question `(used in vNN)`. If an answer contradicts the code or the logs, ask before using it.

## When work is done
Tick the item in part A with the date (`done 2026-11-06, v03`) and keep "Current version" at the top current.
