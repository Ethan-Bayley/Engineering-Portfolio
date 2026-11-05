# Software projects: conventions

For any project with code in `project/src/` (the whole project, or the software part of a build). Shared by every
project; change it in project-template.

## Layout
```
project/src/
  README.md            what it does, how to run it, how to test it (start from general/templates/src_README.md)
  requirements.txt     the project's own packages, pinned to the versions that work (pip freeze, trimmed)
  <package>/           the code
  tests/               pytest tests, one file per module (test_<module>.py)
  config/              settings files (no secrets)
  scripts/             one-off tools, each with a docstring saying what it does and how to run it
```

## Code
- Python 3.11+, standard library first. A new package only when it saves real work; add it to requirements.txt.
- Every module starts with a docstring: what it does, how to run it, what it needs.
- Settings and magic numbers live in one place (a config file or constants at the top), with units in the name or a
  comment (`grip_force_n`, `TIMEOUT_S = 2.0`).
- Small functions with plain names. Comments say why, not what.
- No secrets in the repo: API keys from environment variables or a file in the user's home folder (see
  `general/tools/onshape_images.py`). `.env` files stay out of git.
- Hardware: every script that can move something has a dry-run default and needs an explicit flag (and the user's
  go-ahead in chat) to drive real devices. Tests never talk to hardware; use fakes.

## Tests
- `python -m pytest -q` from the repo root runs the shared tests and `project/src/tests/`. They must pass before
  work is called done; the GitHub Action (`.github/workflows/tests.yml`) runs them on every push.
- Test the logic (maths, parsing, decisions) with small fixed inputs. Keep test data in `project/src/tests/data/`.
- A bug fix comes with a test that failed before the fix.
- Timing or accuracy claims for the deliverable come from a script that measures them and writes the numbers to
  `project/logs/TESTS.md` (date, machine, inputs, n runs, median and range).

## Git
- Small commits with a message that says what changed and why. Ask before committing or pushing (WORKING_RULES.md).
- Work on a branch for anything big; main should always run.
- Generated files (renders, caches, model weights over 50 MB) stay out of git; add them to `.gitignore`.

## Writing it up
- Decisions (which algorithm, which library, what was measured) go in `project/logs/DECISIONS.md` as they are made.
- Screenshots of the running program go in `project/assets/screenshots/` with the date and version in the name.
- For the deliverable: a system diagram (`box.flow`), the key numbers (`box.stats`), a results chart
  (`general/design/charts.py`) and what is not done.
