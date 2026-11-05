---
name: schedule
description: Make or update the project schedule (planned dates per task in project/brief/SCHEDULE.md) and compare it with what really happened, using git history (general/tools/schedule.py). Use when the user asks for a timeline, Gantt chart, project plan, "are we on track", or a planned-versus-actual page for the deliverable.
---

# Schedule: planned against actual

1. **Plan.** If `project/brief/SCHEDULE.md` has no table yet, make one with the user (AskUserQuestion: the main
   tasks, start and end dates, the deadline from `PROJECT.md`). Columns: Task, Planned start, Planned end (YYYY-MM-DD),
   Evidence (the folders or files the task's work goes in, and/or `msg:<word>` for commit messages). Keep the first
   plan; if it changes, add a dated "Plan changed" note below the table rather than editing old dates.
2. **Actual.** Run `python general/tools/schedule.py` (add `--by week` for Gantt rows). Actual dates are the first and
   last commit that touches the evidence. Say plainly that uncommitted work (paper sketches, workshop sessions,
   printing) is missing, and ask the user to correct dates from `BUILD_LOG.md` or their memory; mark any date they
   give as "from the user".
3. **On track?** For each task: in progress, not started, or how far past the planned end its last commit was.
   Suggest what to cut or move if the deadline is at risk.
4. **Into the deliverable.** A Gantt with `box.gantt(r, days, tasks)` using the `--by week` rows (planned bars green,
   actual purple, actual past the plan red) and a short paragraph on why dates slipped, from the logs. A planned
   versus actual comparison with reasons usually earns marks under project management / evaluation.
