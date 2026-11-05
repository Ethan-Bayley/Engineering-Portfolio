"""Planned against actual schedule: the plan from project/brief/SCHEDULE.md, the actual dates from git history.

    python general/tools/schedule.py                 # table: task, planned, actual, commits, status
    python general/tools/schedule.py --by week       # also print the rows for box.gantt(), one column per week

project/brief/SCHEDULE.md holds one table (the setup-project skill or the user fills it):

    | Task | Planned start | Planned end | Evidence |
    |---|---|---|---|
    | Research | 2026-10-01 | 2026-10-07 | project/brief/, msg:research |
    | Build | 2026-10-08 | 2026-10-20 | project/src/, project/logs/BUILD_LOG.md |

Evidence: paths (files or folders) whose commits count as work on the task, and/or msg:<word> to count commits whose
message contains the word. Actual start and end are the first and last such commit. Work not committed (paper
sketches, workshop time) does not show up: say so when using the result, and let the user correct dates by hand.
"""
import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "project" / "brief" / "SCHEDULE.md"


def read_plan(path=PLAN):
    """[(task, start, end, [evidence])] from the first markdown table with ISO dates."""
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[1]) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[2]):
            ev = [e.strip() for e in cells[3].split(",")] if len(cells) > 3 and cells[3] else []
            rows.append((cells[0], dt.date.fromisoformat(cells[1]), dt.date.fromisoformat(cells[2]), ev))
    return rows


def commit_dates(evidence, repo=ROOT):
    """Dates (sorted, with repeats) of commits that touch the evidence paths or whose message has a msg: word."""
    paths = [e for e in evidence if not e.startswith("msg:")]
    words = [e[4:] for e in evidence if e.startswith("msg:")]
    dates = []
    base = ["git", "-C", str(repo), "log", "--format=%ad", "--date=short"]
    if paths:
        dates += subprocess.run(base + ["--", *paths], capture_output=True, text=True).stdout.split()
    for w in words:
        dates += subprocess.run(base + ["-i", f"--grep={w}"], capture_output=True, text=True).stdout.split()
    return sorted(dt.date.fromisoformat(d) for d in dates)


def _days(delta):
    return f"{delta.days} day" + ("s" if delta.days != 1 else "")


def compare(plan, repo=ROOT, today=None):
    """[(task, planned start, planned end, actual start, actual end, commits, status)]."""
    today = today or dt.date.today()
    out = []
    for task, a, b, ev in plan:
        ds = commit_dates(ev, repo) if ev else []
        s, e = (ds[0], ds[-1]) if ds else (None, None)
        if not ev:
            status = "no evidence listed"
        elif not ds:
            status = "not started" if today <= b else f"no commits; due {b}"
        elif e > b:
            status = f"last commit {_days(e - b)} after the planned end"
        elif today <= b:
            status = "in progress"
        elif e < b:
            status = f"last commit {_days(b - e)} before the planned end"
        else:
            status = "on time"
        out.append((task, a, b, s, e, len(ds), status))
    return out


def week_columns(rows):
    """For box.gantt(): days = one column per week (Monday), tasks = planned bar ('good') and actual bar ('actual',
    or 'warn' when it ended after the plan)."""
    starts = [d for r in rows for d in (r[1], r[3]) if d]
    ends = [d for r in rows for d in (r[2], r[4]) if d]
    monday = lambda d: d - dt.timedelta(days=d.weekday())  # noqa: E731
    first, last = monday(min(starts)), monday(max(ends))
    weeks = [first + dt.timedelta(weeks=k) for k in range((last - first).days // 7 + 1)]
    days = [(f"{w:%d/%m}", "wk") for w in weeks]
    key = lambda d: f"{monday(d):%d/%m}"  # noqa: E731
    tasks = []
    for task, a, b, s, e, _n, _st in rows:
        tasks.append((f"{task} (plan)", key(a), key(b), "good"))
        if s:
            tasks.append((f"{task} (actual)", key(s), key(e), "warn" if e > b else "actual"))
    return days, tasks


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plan", type=Path, default=PLAN)
    ap.add_argument("--by", choices=["week"], help="also print gantt rows")
    a = ap.parse_args(argv)
    if not a.plan.exists():
        sys.exit(f"no plan at {a.plan}: make the table described in this script's help first")
    rows = compare(read_plan(a.plan))
    print("| Task | Planned | Actual (from commits) | Commits | Status |\n|---|---|---|---|---|")
    for task, pa, pb, s, e, n, status in rows:
        actual = f"{s} to {e}" if s else "none"
        print(f"| {task} | {pa} to {pb} | {actual} | {n} | {status} |")
    if a.by:
        days, tasks = week_columns(rows)
        print("\ndays =", days, "\ntasks =", tasks)


if __name__ == "__main__":
    main()
