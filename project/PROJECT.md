# Project: FTC engineering portfolio, team 11143 Barker Yellowbacks

## What it is
The team's engineering portfolio for the 2026-27 FIRST Tech Challenge season (BIOBUZZ presented by RTX): a cover page
plus up to 15 A4 pages that show the judges the robot, the engineering process and the team.

## Goal
A portfolio that meets every rule in Competition Manual section 6 (A201, A202) and gives strong evidence for the
Inspire, Think, Control, Innovate and Design awards.

## Type
Competition portfolio (engineering build + software).

## People and dates
- Team (cover only): 11143 Barker Yellowbacks, Barker College. Students as first name + last initial only (A201).
  Members (13; user, 2026-11-05): Ethan B. (lead design, assembly), Brandon L. (CAD, assembly), Isaac H. (CAD,
  assembly, lead code), Ryan T. (CAD, driver), Will Q. (lead strategy, drive coach), Ivy W. (programming, HR), Tina X.
  (code, assembly), Chelsea W. (code, assembly), Chloe L. (assembly, electrical), Chloe S. (strategy, code,
  assembly), Cooper C. (assembly, scouting), Jemima C. (programming, scouting), Lucas T. (CAD, assembly).
- Sponsor/supporter: Barker Robotics (Barker College).
- Event: FTC Wollongong, **Thursday 12 November 2026**. Hand-in: **PDF upload before the event** (under 15 MB);
  upload deadline TODO (ask the Event Director; assume it is before 2026-11-12). Bring a printed spare (A202).
- Contact for the rules: the team coach / Event Director (TODO: name)
- Code: https://github.com/BarkerRedbacks-FTC/Pinkbacks, branches `Isaac` (this season's robot: swerve, intake,
  rear shooter, simulation) and `ball-tracking-greyvision` (mostly June-July 2026, last season's DECODE robot and
  people outside the team: background only). Not a link in the portfolio (A201: judges do not follow links).

## Deliverables
| Deliverable | Format | Limits | Folder |
|---|---|---|---|
| Portfolio | A4 portrait PDF, Yellowbacks style (`project/design/portfolio_style.py`) | 1 cover + 15 content pages, under 15 MB, no text under 10 pt | `project/outputs/portfolio/` |

## The task and rubric
See [brief/ASSESSMENT.md](brief/ASSESSMENT.md) (rules and the award criteria, from the manual saved beside it).

## Look
The team's own cover look on every page (2026-11-05; rules in `project/design/PORTFOLIO_STYLE.md`, this project
only): page #171616, one yellow #F5E660 (no gold or cream), near-white text, a yellow bar down the left edge, a
slanted yellow title banner with hazard stripes, square thin-outline boxes, white robot line drawings, handwritten
yellow labels with curved arrows, Montserrat. Judges get a printed copy by default, so print one test page early.

## Project rules
- FTC A201: first names and last initials only; nothing from before 1 January 2026 except as background; no links,
  videos or QR codes the judges must follow; everything the judges should see is in the 15 pages.
- **AI credit (A201): decided 2026-11-05.** Claude drafts the text from the team's logs and answers, and the
  portfolio carries one short endnote on the last page crediting AI help with drafting and layout (A201 requires it).
  The team checks and edits every page. The endnote names no tool, so hand_in_check's AI-word check stays clean.
- Real-robot results: none given yet. Pages use marked placeholders `<RESULT: ...>` that the hand-in check fails on;
  simulation results are labelled "simulation".
- Hand-in check: `python general/tools/hand_in_check.py --deliverable portfolio --max-pages 16 --max-mb 15 --min-pt 10`.

## Status
2026-11-04: set up from project-template in the user's empty Engineering-Portfolio repo. Evidence the team has: robot
photos, Onshape CAD, the code repo (not yet linked here).
2026-11-05: members, event, hand-in, sponsor, outreach, mechanisms and code filled in; AI credit decided (endnote);
template remote added (fetch-only). Next: the team drops assets in `project/assets/inbox/`, page plan approved, then
pages built. Seven days to the event.
2026-11-05 (later): portfolio v02 built (cover + 15 pages, `outputs/portfolio/portfolio_v02.pdf`), marked 55 / 100
(judgement). Left for the team: real results, the auto route, outreach numbers, strategy, photos (see
`outputs/reviews/marking_loop.md`). Event in 7 days.
