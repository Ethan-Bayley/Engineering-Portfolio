---
name: pull-template-updates
description: Bring the latest shared tools, skills and rules from the project-template repo into this project without touching project/ content. Use when the user says "update from the template", "pull the new tools", or a general tool is out of date.
---

# Pull updates from the template

1. Check `git status` is clean (commit or stash the user's work first, with their OK).
2. Run `python general/tools/template_sync.py pull` (fetches the `template` remote and checks out only the shared paths:
   `general/`, `.claude/skills/`, `tests/test_design_system.py`, `tests/test_onshape_images.py`, `tests/fixtures/`, `CLAUDE.md`).
   It lists what changed and never touches `project/`.
3. Run `python -m pytest tests -q`. If a project build script breaks, fix the script (not the shared tool) unless the tool
   has a bug; tool bugs are fixed in the template repo.
4. Show the user the changed files; commit only when they say.

**Sending an improvement back:** make the change in a clone of project-template (not in the project), commit and push
there, then pull it into each project with this skill. `template_sync.py push-hint` prints the files that differ from the
template so you can copy them across.
