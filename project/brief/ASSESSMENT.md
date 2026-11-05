# Task and rubric: FTC portfolio rules and award criteria

Source: FIRST Tech Challenge 2026-2027 Competition Manual, Section 6 Awards (A), version TU06 (updated 22 Oct 2026),
https://ftc-resources.firstinspires.org/ftc/game/manual-06, saved as
[ftc_manual_section6_awards_TU06.pdf](ftc_manual_section6_awards_TU06.pdf) on 2026-11-04. Re-check before the event,
because Team Updates can change it. Below is a summary with rule numbers; the PDF is the authority.

- Task sheet file: `ftc_manual_section6_awards_TU06.pdf`
- Deadline: FTC Wollongong event, Thursday 2026-11-12; PDF upload before it (exact upload deadline TODO: Event Director)
- Limits: 1 cover page + no more than 15 pages of content; US Letter or A4; digital submissions under 15 MB
- Hand-in: as the Event Director says; with no instructions, 1 printed copy at the Initial Interview (A202)

## Portfolio rules (A201, A202)
| Rule | What it says (summary) | How this project meets it |
|---|---|---|
| A201.A | One cover page with the team number; may also have team name, contents, organisations, sponsors, logo, motto, robot or team photo. Judges do not mark the cover. | Cover built separately from the 15 pages |
| A201.B | No more than 15 pages of content; pages past 15 are not read | hand-in check `--max-pages 16` (cover + 15) |
| A201.C | US Letter or A4 pages only | `Doc("portfolio")` is A4 portrait |
| A201.D | Digital submission under 15 MB in total | `--max-mb 15` |
| A201.E | Only progress, challenges and accomplishments since 1 January 2026 | dates on every log entry; earlier seasons only as background for growth |
| A201 note | Minimise personal information: first names and last initials only; photos allowed | members listed as first name + initial |
| A201 note | Avoid fonts under 10 pt and low-contrast text on images | portfolio format has nothing under 10 pt; dark-theme contrast measured (DECISIONS.md 1) |
| A201 note | Judges will not follow links, websites or videos, or take extra papers | everything is in the PDF |
| A201 note | AI and research aids are allowed if credited with a footnote or endnote | one endnote on the last page (decided 2026-11-05, PROJECT.md) |
| A202 | Submit on time as the Event Director says; default 1 printed copy at the Initial Interview; keep a spare copy in the pit | PDF upload before the event (user, 2026-11-05); upload deadline TODO; printed spare in the pit |
| A203 | The team must take part in an Initial Interview to be considered for judged awards | interview prep is outside this repo |

## Award criteria the team is aiming for
| Award | Portfolio needed? | Required (R) and encouraged (E) criteria, summarised | Where it will be shown |
|---|---|---|---|
| Inspire | yes | R: submit a portfolio; be a strong contender in each of: machine/creativity/innovation awards, team attributes awards, Think; positive and inclusive, every member contributes; can share experiences with the judges | whole portfolio; team page |
| Think | yes | R: at least one of: evidence of the engineering process; lessons learned and applied to the robot design; comparing choices and why one was chosen; using maths to make robot or programming decisions. E: easy to read and find | design process, options and maths pages |
| Control | yes | R: show the hardware and software control components, the challenge each solves and the function of each; use external feedback (sensors) to control the robot. E: works in most matches; reliability shown or improvements explained; what was learned through the engineering process | control page(s): sensors, software, auto |
| Innovate | no (helps) | R: examples of engineering work showing how the design was developed; creative or unique robot or mechanism; stable and reliable. E: risks and how they were reduced | mechanism page |
| Design | no (helps) | R: robot is elegant, efficient (simple to build and operate) and/or practical to maintain; the whole robot or the process, not one part. E: stands out in appearance and function; reasons behind design choices; consistent and fits the game strategy | robot overview and CAD pages |

Teams can also show Connect, Reach and Sustain evidence (learning plan, outreach, partners, finances); not targeted
for now.

## Mark bands
None: judges deliberate against the criteria above. See also `general/guides/RUBRIC_GUIDE.md`.
