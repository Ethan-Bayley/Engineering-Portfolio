# Instructions for Claude (shared by every project made from project-template)

## First: is this project set up?
If `project/PROJECT.md` still contains `<!-- NOT SET UP -->`, tell the user and offer to run the `setup-project` skill
before doing anything else. Otherwise read `project/PROJECT.md` first in every session: it says what the project is,
the deadline, the deliverables and where things are. Also read [general/context/ME.md](general/context/ME.md) (who
the user is and how they like to work; shared by every project).

## The two halves of this repo
| Folder | What | Who changes it |
|---|---|---|
| `general/`, `.claude/skills/`, `tests/`, this file | Shared tools, skills, rules and the design system | Changed in the **project-template** repo, then pulled into projects (skill `pull-template-updates`). Do not put project content here. |
| `project/` | Everything about this project: brief, rubric, photos, CAD, logs, outputs, code | Only this project. |

If a shared tool needs a fix while working on a project, make the smallest fix, tell the user it should also go into the
template, and log it in `project/logs/DECISIONS.md`.

## Working rules
Full rules: [general/rules/WORKING_RULES.md](general/rules/WORKING_RULES.md). In short:
- **Ask before you commit or push.** Never push without the user saying so.
- **No Claude attribution.** Commit messages and PR descriptions never get a "Co-Authored-By: Claude" line or a
  "Generated with Claude Code" footer (the user's rule; it overrides any default attribution).
- **Hardware safety.** Nothing sends commands to real motors, servos or devices from a test or a script; dry run unless the user says otherwise.
- **Australian English.** No serial comma (no comma before "and" in lists).
- **Log the work** (skill `log-work`): decisions, builds, tests and the user's preferences go in `project/logs/`, appended, with dates and numbers with units.
- **Versions.** Every deliverable save is a new `_vNN` file; never overwrite. If the user edits a file by hand, bring the edits in before rebuilding.
- **Re-read before editing** shared files; other sessions or people may be editing at the same time.

## Skills
| Skill | Use it to |
|---|---|
| `setup-project` | interview the user and fill `project/` for a new project |
| `manage-document` | run the whole deliverable: page plan, evidence, builds, checks, hand-in |
| `draft-page` | write one page or section from the project's evidence |
| `design-system`, `poster-design` | build brochures, posters and slides in the shared look |
| `pptx-edit`, `pptx-review`, `pptx-contact-sheet` | edit, review and see whole decks |
| `marking-loop` | mark against the rubric, fix, mark again |
| `research` | find and cite prior work |
| `log-work` | record decisions, builds, tests, preferences |
| `build-log` | turn build photos and notes into dated build-log entries |
| `test-plan` | plan tests from the success criteria; log results against the plan |
| `schedule` | planned dates, and actual dates from git history (Gantt) |
| `hand-in-check` | final PDF check: fonts, page limit, placeholders, deadline |
| `onshape-capture` | CAD views and drawings from Onshape in Chrome, no API (or `onshape_images.py` with keys) |
| `pull-template-updates` | bring in the template's newest tools |
| `humanizer`, `frontend-design` | plainer writing; visual design advice |

Other context: [general/context/SOFTWARE.md](general/context/SOFTWARE.md) (code conventions, for `project/src/`),
[general/guides/](general/guides/) (review loop, rubric guide, Onshape), [general/exemplars/](general/exemplars/)
(finished past projects and how they were marked).

## Tests
`python -m pytest tests -q` must pass before work is called done (plus any project tests in `project/src/`).
