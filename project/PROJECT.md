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
  Members: TODO
- Deadline: TODO (YYYY-MM-DD HH:MM), FTC event in Wollongong; submission method TODO (default in A202: one printed copy
  at the Initial Interview)
- Contact for the rules: the team coach / Event Director (TODO: name)

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
- **AI credit (A201): undecided.** The rule says AI help must be credited with a footnote or endnote. The user asked
  for no mention. Claude will not write the portfolio's content without the credit, so until the user decides,
  Claude does set-up, layout tools, checks, page planning and evidence handling only.
- Hand-in check: `python general/tools/hand_in_check.py --deliverable portfolio --max-pages 16 --max-mb 15 --min-pt 10`.

## Status
2026-11-04: set up from project-template in the user's empty Engineering-Portfolio repo. Evidence the team has: robot
photos, Onshape CAD, the code repo (not yet linked here). Next: team members, event date, the AI-credit decision,
photos into `project/assets/photos/raw/`, page plan.
