---
name: test-plan
description: Plan the project's tests from its goal and success criteria (what to measure, how, how many trials, pass marks), write TEST_PLAN.md and record results against it in project/logs/TESTS.md. Use when the user asks "how should we test this", "make a test plan", wants a results table, or reports test results.
---

# Test plan

Marks for testing come from a plan made *before* testing, fair conditions, enough trials and honest results. This skill
makes the plan, then logs results against it.

## 1. Plan (write `project/brief/TEST_PLAN.md`)
1. Read `project/PROJECT.md` (goal, success criteria), `project/brief/ASSESSMENT.md` (what the rubric asks of testing)
   and `project/logs/DECISIONS.md`.
2. One test per success criterion; if a criterion can't be measured, say so and ask the user how they would judge it.
3. For each test fill this table; ask the user (AskUserQuestion) for anything that depends on what they have
   (equipment, objects, time) rather than guessing:

| ID | Criterion | What is measured (unit) | How (equipment, set-up) | Kept the same | Trials | Pass mark | Safety |
|---|---|---|---|---|---|---|---|
| T1 | ... | ... | ... | ... | 10 | ... | ... |

4. Rules for a fair test: change one thing at a time; write down what is kept the same; at least 5 trials (10 if time
   allows) so a success rate or average means something; note the date, who ran it and the version tested.
5. Hardware: plan the dry run (no motors) first, then the powered test, which the user runs themselves (CLAUDE.md,
   hardware safety). Note limits (current, travel, temperature) to stop at.
6. Add a blank results sheet per test the user can fill in on paper or a phone (trial, result, notes), as a table in
   the same file.

## 2. Results (append to `project/logs/TESTS.md`)
- One entry per test run: date, test ID, version or commit tested, conditions, every trial's result (not only the
  average), the summary (success rate n/N, mean and range with units), pass/fail against the plan's pass mark.
- Results the user reports: "reported by the user on <date>", and ask for the details the plan needs (trials,
  conditions) before calling a test passed. Never fill in a trial that was not run.
- Failed or odd trials stay in, with what happened. Say when the sample is small.
- Update the plan's table with a Status column: MET / PARTLY MET / NOT MET / NOT TESTED (the design system's table
  colours these).

## 3. Into the deliverable
- The results table goes in with `box.table(..., status_col=...)`; a chart with `general/design/charts.py`
  (`bars` or `before_after`), numbers only from `TESTS.md`.
- Evaluation: for each NOT MET or PARTLY MET, the likely cause and what would be changed next.
