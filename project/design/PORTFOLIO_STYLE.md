# Yellowbacks portfolio style

The look of team 11143's FTC engineering portfolio. **This project only:** it is not part of project-template
(user, 2026-11-05). Code: [portfolio_style.py](portfolio_style.py). Build script:
`project/outputs/portfolio/build_portfolio.py`. Tests: `project/tests/test_portfolio_style.py`. Fonts:
[fonts/](fonts/) (Montserrat and Caveat, SIL Open Font License), loaded by `general/tools/export_pdf.py` and installed
by `general/tools/install_fonts.ps1` from `project/design/fonts/`.

## 1. How it was decided
1. **2026-11-05, morning:** three example FTC portfolios (teams 12635, 1002, 22105) measured with PyMuPDF: all US
   Letter portrait, 16 pages, near-black pages (#000000 to #0F0F0F), near-white text, one bright accent (red #E06666,
   green #20D54D, pink #F37D9C); 5 to 11 images a page. The user chose thin outline boxes like 22105, a near-black
   page, yellow with green/red only for pros/cons, A4 portrait, Montserrat, handwritten labels with curved arrows,
   title left and team right, and these parts: challenge → solution, iteration row, team cards, timeline.
2. **2026-11-05, afternoon:** the user sent the team's own cover (saved as
   `project/assets/cover/cover_v0_user.png`) and asked for that look on every page, with tighter colours ("the gold
   is ugly") and the schematic line drawings kept. The cover's colours (sampled from the image): page #171616,
   yellow #F5E660, gold #B8985A / #AA8D53, cream #FFF4B2, a duller title yellow #D8CD6C, grey #C4C4C4.
   **Tightened to:** one yellow #F5E660 for everything the gold, cream and dull yellow did; grey #C4C4C4; the page
   #171616. The user also said not to build a CAD-to-schematic tool: line drawings come from the team.

## 2. Colours (project/design.json can change main, background, text, muted, line, pro, con)
| Token | Hex | Use | Contrast on #171616 |
|---|---|---|---|
| BG | 171616 | page (the cover's; not pure black) | |
| TEXT | F2F2F2 | body text (not pure white) | 16.1:1 |
| YELLOW | F5E660 | edge bar, banners, stripes, pills, `**key words**`, labels, arrows, table header, page number | 14.1:1 |
| INK | 171616 | dark text on yellow | 14.1:1 on yellow |
| MUTED | C4C4C4 | captions, team number, footer | 10.4:1 |
| LINE | 8C8C8C | box outlines, table rules (thin, like a drawing frame) | 5.4:1 |
| PRO | 6FD98B | `++pros++`, pass, better: nothing else | 10.3:1 |
| CON | FF7B72 | `~~cons~~`, fail, worse, late: nothing else | 7.2:1 |

Measured with the WCAG formula on 2026-11-05.

## 3. Type
Montserrat for everything (bold caps for titles, headings, pills, labels in tables); Caveat Static Bold for the
handwritten labels on drawings. Sizes: banner title 19, box heading 12 (caps), sub-heading 11.5, body 10.5,
captions/tables/footer/pills 10, handwritten labels 15. **Nothing under 10 pt** (FTC A201); `save()` refuses.
Montserrat line height measured in a PowerPoint PDF: 1.2 x size. Bullets are a small yellow square (U+25A0 at 70 %;
Montserrat has no U+25AA, which fell back to Times New Roman in the first try).

## 4. Page (A4 portrait, 595.28 x 841.89 pt; one gap G = 10 pt)
- A yellow bar (14 pt) down the whole left edge of every page, as on the cover.
- Header: the cover's banner (yellow, straight left end at the edge bar, slanted right end) with the page title in
  dark bold caps, then four yellow hazard stripes; the team number in a grey outlined box top-right with a yellow bar
  beside it (the cover's number box). Checked: a title too long for the banner is refused.
- Footer: "11143  BARKER YELLOWBACKS" grey bold left, "PAGE 01" yellow bold right. The cover is not numbered.
- Cover: built in the build script, following the user's cover: two-line banner, stripes, outlined pill
  "FTC - FIRST TECH CHALLENGE", "BARKER **YELLOWBACKS**", robot line drawings, the vertical team number in a box,
  "2026-2027 / Sydney / Australia" beside a yellow bar. No FIRST logo yet: add the official file if wanted, following
  FIRST's logo rules.

## 5. Components
| Component | Call | Look |
|---|---|---|
| Box | `page.box(rect, "Heading", accent=False)` | square corners, 1 pt grey outline; yellow bar + caps heading; `accent=True` = yellow outline (once a page at most) |
| Text | `box.text(r, paras)` | `**yellow**`, `++pro++`, `~~con~~`, "- " bullets; warns if it needs more room |
| Picture | `box.picture(r, path, alt, caption)` | alt text required; caption grey |
| Labelled drawing | `box.labelled(r, path, alt, labels=[(fx, fy, text, lx, ly)])` | handwritten yellow labels, curved yellow arrows; labels stay inside the box |
| Challenge → solution | `box.story(r, [(label, text)])` | yellow pills (outlined, the last filled) above each paragraph |
| Iterations | `box.iterations(r, [(name, pic, alt, pros, cons)])` | outlined cards, name pills, yellow arrows; the kept version in yellow |
| Team cards | `box.team(r, [(name, role, photo, note)])` | photo or initials square, yellow bar, caps yellow role; warns on full surnames (A201) |
| Timeline | `box.timeline(r, [(when, title, text)])` | yellow line, yellow diamond nodes |
| Planned against actual | `box.plan_vs_actual(r, periods, rows)` | grey outline = planned, yellow = actual, red = late |
| Table | `box.table(r, rows, status_col=)` | yellow header band with dark caps, thin grey rules, coloured status words |
| Shapes | `banner`, `stripes`, `pill`, `bar`, `polygon` | the cover's pieces, for the cover and special pages |

## 6. Robot line drawings
White lines on the page colour, like the cover. The two on the cover and page 2 now are **low-resolution crops of
the user's cover image** (`project/assets/cover/robot_schematic_*_lowres.png`, about 450 x 300 px): fine for
layout, too soft to print. Replace them with the full-size drawings the team made the cover from.

## 7. Not done / not proven
- Not printed yet: a near-black page may print dark and muddy (A202's default is one printed copy). Print one page.
- Only placeholder pages so far; no real content (see PROJECT.md, AI credit).
- The text-height check uses Pillow measurements of Montserrat; checked against PowerPoint only for line height.
- Charts in this look are not done (`general/design/charts.py` draws the default look).
