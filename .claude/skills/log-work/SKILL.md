---
name: log-work
description: Record what was done, decided, built or tested in the project logs. Use at the end of any piece of work that changed behaviour, results, the build or the deliverable, and when the user reports a result or a preference.
---

# Log the work

Logs live in `project/logs/`. Append; never rewrite old entries. If an old conclusion was wrong, add a new entry saying so.

| What | File |
|---|---|
| Decisions: what changed, options considered, why, how it was measured | `DECISIONS.md` |
| Build steps, parts, photos taken, problems and fixes | `BUILD_LOG.md` |
| Tests: what, conditions, trials, result, date | `TESTS.md` |
| What the user asked for or said they prefer (dated) | `PREFERENCES.md` |

Rules:
- Numbers with units and where they came from (a run, a file, the user). Say when a figure is assumed or from a small sample.
- Results the user reports go in as "reported by the user on <date>"; ask for the details (object, tries, conditions).
- Keep a "Not done / not proven" line current in DECISIONS.md.
