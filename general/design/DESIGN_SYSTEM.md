# Design system

The look for every brochure, poster and slide deck made from this template. **Formats:** `Doc("brochure")` = A4 landscape
with page numbers, `Doc("poster")` = A3 portrait, `Doc("slides")` = 16:9. **Per-project colours:** `project/design.json`
(keys `main`, `green`, `orange`, `purple`, `red` and `*_tint`, hex without #); anything left out keeps the defaults below.

- **Code:** [design_system.py](design_system.py) draws every part below and checks the rules before it saves.
- **Skill:** `design-system` in [../../.claude/skills/design-system/SKILL.md](../../.claude/skills/design-system/SKILL.md).
- **Tests:** [../../tests/test_design_system.py](../../tests/test_design_system.py).
- **PDF:** `python general/tools/export_pdf.py <deck> --render <dir>` (embeds Inter, reports overflow).

Origin: built for the RobotHand AT3 brochure (October 2026) from two example PDFs and the user's colour choices; the
history below is kept because it explains why each rule exists.

---

## 1. Colours

| Token | Hex | Tint (accent) | Use |
|---|---|---|---|
| MAIN | `#1d497d` | | Page titles, the cover and other top-level items. **Never a content box.** |
| GREEN (1) | `#1c9d75` | `#d8ede8` | Box colour: research, results, findings, conclusion. Green highlight = a result. |
| ORANGE (2) | `#cb8429` | `#fef4d0` | Box colour: design, process, build, planning. Yellow highlight = a caution. |
| PURPLE (3) | `#635ca8` | `#ededf6` | Box colour: method, code, software, analysis. |
| RED (4) | `#d43e2e` | `#fdeceb` | Box colour: problem, testing, risk, evaluation. |
| SLATE | `#2b3e50` | | All body text (measured from the reference). |
| WHITE | `#ffffff` | | Page background and box panels. |

**Choosing a box colour: by meaning** (user's choice). Give the box a role from the table and the role sets the
colour. If that would put it next to a box of the same colour, it changes to the first other colour that fits, and
`doc.notes` records the swap.

**No two boxes of the same colour may be next to each other.** "Next to" means **sharing an edge**: side by side, or one
above the other with only the gap between them. Boxes that only meet at a corner may match, and so may the last box on
one page and the first on the next. Parts inside a box (stat cards, columns, badges) may use any colour, including the
box's own, **except stat cards: every card in a box is a different colour, and up to 3 cards never use the box's
colour; with 4 cards each colour is used once** (user, 2026-10-19). Parts next to
each other inside a box still differ.

### Contrast (measured with the WCAG formula, 2026-10-19)
| Text colour | on white | on its own tint |
|---|---|---|
| MAIN | 9.1 : 1 | |
| GREEN | 3.4 : 1 | 2.8 : 1 |
| ORANGE | 3.1 : 1 | 2.8 : 1 |
| PURPLE | 5.8 : 1 | 5.0 : 1 |
| RED | 4.6 : 1 | 4.1 : 1 |
| SLATE | 11.0 : 1 | 9.0 to 10.0 : 1 on any tint |

Green and orange only pass for **large text** (3 : 1, which means at least 14 pt bold). So:
- **Box headings are bold and at least 14 pt** (20 pt brochure, 14 pt A3).
- **Text inside highlights and stat-card labels is slate**, with the colour carried by the bar, fill and outline. Coloured text appears only in headings, subheadings, stat-card numbers and timeline stage names: short, bold
  and large. This differs from the reference PDF, where the wind-farm highlight's whole paragraph is orange text on a
  yellow tint (2.8 : 1). That was my decision for legibility; the user can reverse it.

## 2. Type: Inter only

Inter is installed on this PC as a variable font. PowerPoint lists it as `Inter`, `Inter SemiBold`, `Inter ExtraBold`,
`Inter Black` and others. Page titles use **Inter Bold** (changed 2026-10-22 from ExtraBold, which exists only in the variable font and does not survive
PDF export); everything else uses **Inter** (bold where stated). **Export PDFs with `python general/tools/export_pdf.py <deck>`.** PowerPoint cannot embed the variable Inter in a
PDF and falls back to Calibri; a static copy also called "Inter" does not help (Windows still picks the variable one).
The tool exports a copy whose font is renamed to **"Inter Static"** (static Regular and Bold renamed with fontTools, in
`assets/fonts/InterStatic/`, SIL OFL licence alongside, installed for this Windows user) and refuses to finish unless the PDF embeds Inter.
**Inter is not a standard Office font:** on another computer the .pptx falls back to a substitute font unless Inter is
installed there. The PDF exported here embeds it, so hand in the PDF.

| Token | A3 portrait poster | 16:9 slides (only if a talk deck is needed) | Style |
|---|---|---|---|
| title (page title) | 64 pt | 72 pt | Inter Bold, CAPITALS, MAIN |
| heading (box heading) | 14 pt | 20 pt | Inter Bold, `NN - CAPITALS`, box colour |
| sub (subheading, timeline stage) | 11.5 pt | 17 pt | Inter Bold, sentence case, its colour |
| body | 10 pt | 15 pt | Inter, SLATE, line spacing 1.15 |
| stat_num | 20 pt | 32 pt | Inter Bold, card colour |
| table | 9 pt | 13 pt | Inter, header bold white |
| small (captions, page number) | 8.5 pt | 12 pt | Inter, SLATE |

How these were chosen: the A3 body size of 10 pt matches the weather-station poster (measured at 10.0 pt). The
reference DESIGN pages use 7.5 pt body on US Letter. The A3 headings were raised to 14 pt bold for contrast. The 16:9
sizes were **chosen by me, not measured**, and are not used for the brochure (it is A3 portrait, user 2026-10-19). The
existing render check flags text under 12 pt, so it will list the A3 body text; at A3, held at arm's length, that is
expected.

## 3. Spacing: everything comes from one gap, G

**G = 1.6 % of the page width** (the reference: 9.8 pt on a 612 pt page).
- A4 landscape brochure and A3 portrait poster (same width): G = **13.5 pt** (4.75 mm). 16:9 slides: G = 23.0 pt.
- **A4 landscape brochure sizes** (chosen 2026-10-22, not measured): title 36 pt, heading 14 pt, sub 10.5 pt, body 9.5 pt,
  stat number 18 pt, table 8.5 pt, small 7.5 pt.

| Thing | Value |
|---|---|
| **Gap between any two boxes** | **G, everywhere, always** (checked on save) |
| Left/right page margin | 3 G |
| Above the page title | 1.2 G; below it, G before the first box |
| Bottom margin | 2.5 G (the brochure page number sits here, bottom-right) |
| Corner radius, both box rectangles | G (equal on both, as the user asked and as the reference has) |
| Coloured band at the top of a box | 0.8 G |
| Coloured edge on the sides and bottom | 0.15 G |
| Padding inside the white panel | 0.75 G |
| Gap between parts inside a box | 0.5 G (stat cards, steps); G between sub-topic columns |
| Stat card / highlight corner radius | 0.5 G |
| Stat card / highlight outline | 0.1 G (at least 1 pt) |
| Sub-topic rule, timeline line and rings | 0.22 G |
| Callout left bar | 0.35 G |

Use `page.rows()` and `page.cols()` to split the page. They put exactly G between the parts, so the gap stays the same
without measuring by hand.

## 4. Page

- White background.
- **Page title:** one word or a short phrase in CAPITALS, top-left, in MAIN (as "DESIGN", "PROTOTYPE" and "EVALUATE" in
  the reference). **No photo or image beside the title** (user, 2026-10-19).
- No gradient banners and no decorative strips (the user did not choose them).
- Brochure pages carry a two-digit page number, bottom-right, small, slate. It must equal the PDF page number.
- **Sources and credits:** one small slate line in the bottom margin, left (`page.sources(text)`): where the numbers
  come from and every outside photo's title, author, site and licence.
- **Sources and credits:** one small slate line in the bottom margin, left (`page.sources(text)`): where the numbers
  come from and every outside photo's title, author, site and licence.
- Boxes fill the area under the title in rows and columns with G between them. Size boxes to their content;
  white space inside a box is fine, but avoid a half-empty box. Shrink the row instead.

## 5. Content box (the main building block)

```
   .-----------------------------.
  /###############################\    coloured rounded rectangle behind (box colour, radius G)
 |#################################|   <- top band 0.8 G
 |#.-----------------------------.#|
 |#| 03 - HEADING IN CAPITALS    |#|   white rounded rectangle on top (same radius G)
 |#|                             |#|   <- sides and bottom 0.15 G
 |#| body text in slate ...      |#|
 |#'-----------------------------'#|
  '-------------------------------'
```

- Two rounded rectangles with **equal corner radius**. The one behind is the solid box colour; the one on top is solid
  white, inset 0.15 G on the left, right and bottom and 0.8 G at the top. The effect is a thin outline all round that
  thickens at the top.
- **Heading:** `NN - TITLE IN CAPITALS`, bold, in the box colour. NN is two digits with a space, hyphen and space after it.
  **Numbering runs continuously** across the whole brochure or poster set (01, 02 ... 15 over three pages, as in the
  reference). It does not restart on a new page.
- Body text in slate. Bullets are `•` in the box colour.
- Content boxes are only ever GREEN, ORANGE, PURPLE or RED.

## 6. Components (all inside a content box)

| Component | Looks like | Use for | Helper |
|---|---|---|---|
| **Highlight** | Rounded tint panel (radius 0.5 G) with a thick bar down the left in the colour (0.35 G); the bar follows the rounded corners. Slate text, bold lead phrase. | **Key information in words.** Three kinds only: `general` = the box's own colour; `result` = green (finding, measured number, conclusion); `caution` = yellow, i.e. orange bar on yellow tint (limit, assumption, not tested). | `box.highlight(r, text, kind)` |
| **Callout** | A highlight with a bold label first ("Key Finding:") | Under a chart or picture: what to notice in it | `box.callout(r, text, label, kind)` |
| **Stat cards** | Tint fill, **full outline** in the colour, radius 0.5 G; big bold number in the colour, bold slate label below | **Only for a key statistic or number.** Every card in a box a different colour: 1 to 3 cards never use the box's colour; 4 cards use each colour once (box colour last); over 4, only neighbours differ. Every number still needs its MEASURED / PROPOSED / NOT TESTED status somewhere on the page. | `box.stats(r, [(num, label)], cols=2)` |
| **Sub-topic columns** | Coloured rule on top, bold coloured subheading, short slate paragraph | Breaking one idea into 2 to 4 parts | `box.subtopics(r, [(title, text)], cols=4)` |
| **Numbered steps** | Rounded square badge (radius 20 % of its side) in solid box colour with a big white digit, text to the right | A process in order | `box.steps(r, [text, ...])` |
| **Table** | Header row in **the box's colour** with bold white text; white and box-tint alternate rows; slate text; numbers right-aligned | Results and comparisons | `box.table(r, rows, col_weights)` |
| **Timeline** | Vertical line with white ring nodes; each stage's line, ring and "date - stage" label in its colour, notes in slate | Record of production / project timeline | `box.timeline(r, [(date, stage, notes)])` |
| **Picture** | Fitted inside its area, centred, caption below in small slate | Evidence, CAD, renders | `box.picture(r, path, alt, caption)` |
| **Labelled picture** | A picture with small white labels (box-colour outline) joined by arrows to points on it | Build photos and CAD: naming the parts | `box.labelled(r, path, alt, caption, labels=[(fx, fy, text, lx, ly)])` |
| **Mind map** | Main-colour centre node; 2 to 5 branch nodes in tint with a coloured outline, each its own box colour, joined by lines | Ideas, options and constraints at the start of a project | `box.mind_map(r, centre, [(title, [points])])` |
| **Chart** | PNG drawn at its placed size, text at the format's table size, Inter, slate; green = kept / result, red = before / problem, grey = the rest | Measured numbers | `charts.bars`, `charts.before_after`, `charts.lines` in `general/design/charts.py`, then `box.picture` |

**The full-outline style is reserved for stat cards (numbers).** Any highlighted text uses the left-bar highlight.

Neighbouring stat cards and sub-topic columns get different colours automatically (`grid_colours`, +1 colour across a
row, +2 down a column). Stat cards follow their own rule in the table above.

## 7. Checks (run by `doc.save()` / `doc.save_versioned()`; it refuses to save if any fail)

1. No two boxes that share an edge are the same colour.
2. Every gap between neighbouring boxes is G (to within 0.5 pt), and no boxes overlap.
3. No content box uses MAIN or any colour outside the four.
4. Every heading matches `NN - CAPITALS`, and numbers are continuous across pages.
5. Boxes stay inside the page margins.
6. Every picture has alt text (checked when it is placed).

What the checks **do not** catch: text overflowing its box (use `general/tools/export_pdf.py --render` and look at the PNGs),
diagonal same-colour corners (allowed), and whether the content is true (check it against `project/logs/`).

## 8. Measured from the reference PDFs (PyMuPDF, 2026-10-19)

`ISTEAM (2).pdf`: 3 pages, US Letter portrait (612 x 792 pt).
| Item | Measured |
|---|---|
| Box | coloured rounded rect + white rounded rect, both 1 pt stroke in the box colour, **radius 10 pt on both** |
| White panel offset | top: 9.8 pt (box 01), 3.9 pt (box 02), 8.1 pt (box 03), inconsistent; sides and bottom: 0 (shared outline) |
| Gap between boxes | 10.1 pt and 10.5 pt; page margin 31.3 pt |
| Page title | Inter, 48 pt, bold caps, `#1b4a7e` |
| Box heading | Inter, 8.5 pt, bold caps, box colour, `NN - ` prefix |
| Body | Inter, 7.0 to 7.5 pt, `#2b3e50` |
| Stat cards | 100 x 35 pt, radius 5 pt, 1 pt outline, tint fill; number 13.8 pt, label 9.9 pt |
| Colours | `#1b4a7e`, `#169f76`, `#cd852a`, `#635da9`, `#d63f2f`, `#894b9d`; tints `#d8eee8`, `#fff5d1`, `#eeeff8`, `#feedec` |

`iSTEAM Posters (4).pdf`: 2 pages, A3 portrait (842 x 1190 pt); Inter body text at 10.0 pt; gradient title banner; "Key
Finding" callouts with a left bar; a timeline with ring nodes; solid spec cards with monospace pin lines.

**What changed from the reference, and why:**
- The top band is a fixed 0.8 G and the sides are inset 0.15 G (the user's choice of "thin sides, thick top"). The
  reference has no side inset and a varying top.
- The main colour is never a box (the user's rule). The reference uses navy for boxes 01 and 07.
- Highlight text is slate rather than coloured, for contrast (section 1).
- Text highlights use a rounded left-bar panel, not the reference's full-outline box; the full outline is only for
  stat cards. Table headers take the box colour rather than navy. Step badges are rounded. (User, 2026-10-19.)
- Not carried over (the user did not pick them): the gradient banner, solid spec cards, the second purple `#894b9d`.

## 9. Not done / not proven
- The rules have only been tried on the two reference decks. No real brochure page or poster has been built with them yet.
- The brochure type sizes are chosen, not tested on a printed or projected page.
- Charts (`charts.py`, 2026-11-04): only tested for size and that they draw; not yet used in a real project's pages.
- The existing brochure draft (navy/teal) has not been converted.

## 10. Change log
- **2026-10-19, v01:** first version from the reference PDFs and the user's four rounds of answers.
- **2026-10-19, v02 (user feedback on v01):** the full-outline style is now only for stat cards (key numbers). Text
  highlights use the left-bar style with rounded corners in three kinds (box colour, green result, yellow caution).
  Stat cards avoid their box's colour. Table header rows are in the box colour, with box-tint alternate rows (the tint
  rows were my choice to match the header). Step badges are rounded. The photo beside the page title was removed.
  Bug found by the new test while doing this: the first grid-colour rule repeated a colour vertically in 3-column
  grids; fixed (+1 across, +2 down).
- **Contrast of the new table headers:** white bold text on green is 3.4 : 1 and on orange 3.1 : 1, which passes only
  as large or bold text. Header text is bold, but at A3 it is 9 pt, below the 14 pt "large" size. Not changed; flagged.
- **2026-10-19, v03 (user: "make the stats highlights be different colours"):** v02 repeated a colour in 2 x 2 and
  1 x 4 stat grids (only neighbours differed). Now every stat card in a box is a different colour. Four cards cannot all
  differ while avoiding the box's colour (only three remain), so the user chose: up to 3 cards avoid the box colour;
  with 4, each colour appears once and the box colour is used last. New test: `test_stat_cards_in_one_box_are_all_different_colours`.
- **2026-10-19, first real page:** `posters/example_page/vision_page_v01.pptx` (RobotHand repo)
  (build script beside it). Added `page.sources()` for the credit line. Stat-card top/bottom padding cut from 0.35 G to
  0.2 G because the number and label overflowed 64 pt cards (render check); the design_system reference decks were not
  rebuilt for this small change.
- **2026-10-19, first real page:** `posters/example_page/vision_page_v01.pptx` (RobotHand repo)
  (build script beside it). Added `page.sources()` for the credit line. Stat-card top/bottom padding cut from 0.35 G to
  0.2 G because the number and label overflowed 64 pt cards (render check); the design_system reference decks were not
  rebuilt for this small change.
- **2026-10-19, brochure is A3 portrait (user):** the "brochure" format was 16:9 (20 x 11.25 in, copied from the old Canva
  draft); it is now A3 portrait with the poster's sizes plus page numbers. The 16:9 set is kept as "slides". Reference decks
  rebuilt as v04 (brochure sample re-laid out for portrait, two pages); example page rebuilt as
  `vision_page_v02.pptx` (RobotHand repo). New test: `test_brochure_is_a3_portrait_with_page_numbers`.
- **2026-10-22, brochure is A4 landscape (user):** `Doc("brochure")` is now 841.89 x 595.28 pt with its own smaller type
  (above); posters stay A3 portrait. New parts for the real brochure: `doc.page(..., cover=True)` (no title or page number),
  `box.table(..., status_col=, bold_col=)` (verdict words such as PARTLY MET get their colour's tint: MET/CHOSEN green,
  PARTLY MET yellow, NOT MET red, NOT TESTED/MEASURED ONLY purple), `box.flow()` (picture steps with tint labels and arrows;
  `arrows=False` for a comparison row), `box.gantt()` (schedule bars), `box.head()` (a coloured sub-heading paragraph),
  `box.arrow()`, and `highlight(..., size=)`. Long box headings now get a second line automatically (they overflowed in
  narrow boxes), and flow labels get the lines they need. Titles changed to Inter Bold. The real brochure is built with it
  from v15: the RobotHand build script.
- **2026-10-22, section labels:** `doc.page(title, label="1  Significance")` puts the required section name, bold in the main colour, at the right of the title band (task sheet: "sectional headers for each required element").
- **2026-10-22, tables sized from their text:** `box.table()` used to stretch every row evenly to fill its slot; PowerPoint
  then grows any row whose text wraps, so tables ran past their box (page 8 of brochure v18, found by the user). Rows now get the height
  their text needs (estimated with `lines_needed`) and only the space left over is shared out. `tools/render_check.ps1` now measures
  table rows from their text and reports **PAST-BOX** for anything (table, picture, text) that ends less than 5 pt inside its box's
  white panel, and **TABLE-GROWS** when rows need more height than the table frame. Before this, tables and pictures were never checked.
- **2026-10-22, fitted highlights and `box.stack()` (user):** a highlight is only as tall as its text (`fit=True`, estimated with
  `text_height`). `box.stack(r, [("text", paras), ("highlight", text, kind), ("fill", weight, draw)])` places parts one under another:
  text and highlights get the height their words need, fill parts (pictures, charts, tables) share the rest. With nothing to stretch,
  **a highlight that closes a box sits at the bottom of the box**, lined up with the closing highlights beside it, and the spare space
  goes above it. The height estimate is approximate (Inter about 0.5 em a character); the render check catches misses.
- **2026-10-22, text measured with the real font:** `lines_needed()` now word-wraps with the widths of the static Inter files
  (`assets/fonts/InterStatic`, measured with Pillow; bold runs measured bold), falling back to the old per-character guess only if the
  fonts are missing. The guess had predicted a second line that never came in narrow boxes, so a fitted highlight was drawn two lines
  tall around one line of text (brochure v20, page 3, box 05: the text is 167.2 pt wide in a 168 pt line). Headings, flow labels,
  table rows and stacks all use the measurement.
- **2026-11-04, project-template:** added `box.labelled()` and `box.mind_map()` (moved from the RobotHand brochure
  build script, where they were page-level helpers) and `general/design/charts.py` (bar, before/after and line charts in
  the design system's colours, drawn at the placed size; based on RobotHand's `make_charts_a4.py`). Starter scripts for
  a poster and slides beside the brochure one in `general/templates/`. Tests: `tests/test_template_tools.py`.
