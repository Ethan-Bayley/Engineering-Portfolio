# project-template

A starting point for school assessments, engineering builds and software projects worked on with Claude Code. Clone it
once per project. Shared tools, skills and rules live in `general/` and `.claude/skills/`; everything about one project
lives in `project/`.

## Start a new project
1. On GitHub, create a new **empty private** repo for the project (no README), for example `my-new-project`.
2. Clone the template under the new name (or clone it in GitHub Desktop and pick the new name):
   ```bash
   git clone https://github.com/Ethan-Bayley/project-template.git my-new-project
   ```
3. Open Claude Code in the folder and say **"set up this project"**. The `setup-project` skill asks what the project is,
   the goal, deadline, team, rubric, deliverables and look, fills `project/`, and connects git for you: it adds the
   `template` remote (or renames `origin` to `template`) and asks once for your project's GitHub URL.
4. Install the Python packages once per computer: `python -m pip install -r requirements.txt`.
5. Install the Inter fonts once per computer (for PDFs with the right font):
   ```bash
   powershell -NoProfile -ExecutionPolicy Bypass -File general/tools/install_fonts.ps1
   ```

## What is where
| Path | What |
|---|---|
| `CLAUDE.md` | rules and the skill list Claude reads every session |
| `general/rules/` | working rules (git, hardware safety, writing, logging, versions) |
| `general/context/` | about me (`ME.md`) and software conventions (`SOFTWARE.md`) |
| `general/exemplars/` | finished past projects with their marking notes (RobotHand AT3 brochure) |
| `general/guides/` | review loop, rubric guide (ISEF and school criteria), Onshape (API or browser) |
| `general/design/` | the design system (`design_system.py`, `DESIGN_SYSTEM.md`), charts (`charts.py`) and fonts (Inter) |
| `general/tools/` | PDF export with fonts embedded, render and overflow checks, contact sheets, deck editing, hand-in check, schedule from git, Onshape CAD images (API) and screen grabs (no API), photo prep, template sync |
| `general/templates/` | starter build scripts (brochure, poster, slides) and a README for `project/src/` |
| `.github/workflows/` | runs the tests on GitHub on every push |
| `.claude/skills/` | setup-project, manage-document, draft-page, design-system, poster-design, pptx-edit, pptx-review, pptx-contact-sheet, marking-loop, research, log-work, build-log, test-plan, schedule, hand-in-check, onshape-capture, pull-template-updates, humanizer, frontend-design |
| `tests/` | tests for the shared tools (`python -m pytest tests -q`) |
| `project/` | this project only: brief and rubric, photos and CAD, logs, outputs, code (see `project/README.md`) |

## Getting tool updates into a project
Improve shared tools in a clone of **project-template**, commit and push there. Then in each project, ask Claude to
"pull template updates" (skill `pull-template-updates`), or run:
```bash
python general/tools/template_sync.py pull
```
It only touches the shared paths, never `project/`. `status` shows what differs; `push-hint` lists shared files you
changed inside a project that should be copied back to the template.

## Requirements
Windows with PowerPoint (for rendering and PDF export), Python 3.11 or later, git. PDF export embeds Inter by using the
static copies in `general/design/fonts/InterStatic/` (install them once with `install_fonts.ps1`; `export_pdf.py` loads
them into the session each run).

## Origin
Built from the RobotHand AT3 project (October to November 2026): the design system, deck tools and skills were made there
and generalised here.
