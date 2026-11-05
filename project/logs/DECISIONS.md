# Decisions

Append new entries at the bottom, with the date. See skill `log-work`.

## 1. Project set up (2026-11-04)
- **What:** project-template checked out into the user's empty `Engineering-Portfolio` repo (files staged, not
  committed); `template` remote added. No `origin` yet: publish from GitHub Desktop.
- **Rules source:** FTC Competition Manual section 6, TU06 (22 Oct 2026), saved in `project/brief/`. Summary and
  award criteria in `brief/ASSESSMENT.md`.
- **Format:** new `portfolio` format in the shared design system (also added to project-template): A4 portrait
  (595.28 x 841.89 pt), sizes title 26, heading 14, sub 12, body 10.5, table 10, small 10, stat numbers 20 pt, so no
  text is under A201's 10 pt. A4 rather than US Letter (user picked A4 portrait; Australian printers use A4).
- **Dark theme:** the design system can now take `background`, `panel`, `text`, `on_colour` and `on_main` from
  `design.json` (shared change). Box colours were made brighter for the dark panels. Contrast measured with the WCAG
  formula on 2026-11-04: text F2F2F2 on panel 3C3C3C 9.9:1; yellow FBEB33 titles on 333333 10.2:1; box-colour
  headings on the panel: green 3DC48F 5.0, orange F2A541 5.4, purple A39BF0 4.5, red F2756A 4.0 (bold 14 pt needs
  3:1); dark 262626 text on the box colours 5.4 to 7.4. The default box colours would have been 2.4:1 (red) and
  3.2:1 (green) on the dark panel, too low.
- **Not done / not proven:** the dark theme has not been printed; the event date, members and the AI-credit decision
  are missing; no evidence in `project/assets/` yet.

## 2. New look: the portfolio style (2026-11-05)
- **What:** the portfolio now uses a new, separate style, `general/design/portfolio_style.py` (made in
  project-template and copied here, not yet committed in either), instead of the box-colour design system with the
  dark theme from section 1. `project/design.json` now holds only main FBEB33, background 121212 and text F2F2F2.
  `build_portfolio.py` was replaced by the new starter with the team filled in (placeholders only).
- **How it was decided:** three example portfolios measured with PyMuPDF (all US Letter portrait, 16 pages,
  #000000-#0F0F0F pages, near-white text, one accent; boxes differ), then two rounds of questions (PREFERENCES.md).
- **Measured:** contrast on #121212: text 16.7:1, yellow 15.2:1, muted grey 9.1:1, green 10.7:1, red 7.4:1.
  PowerPoint draws Montserrat at 1.2 x the font size (measured in an exported PDF). The starter's three pages export
  with Montserrat and Caveat embedded and pass the style's checks (nothing under 10 pt, gaps, fits).
- **Section 1's dark theme** for the default design system stays in project-template but is not used here.
- **Not done / not proven:** no real page yet (no photos or CAD in `project/assets/`); the dark pages have not been
  printed; dark charts for this style are not done; event date, members and the AI-credit decision are still open.

## 3. The team's cover becomes the look; the style moves into this project (2026-11-05)
- **What changed:** the portfolio style now lives only here, in `project/design/` (code, rules, fonts), with tests
  in `project/tests/`. It was taken out of project-template again, together with section 1's dark theme and
  `portfolio` format and the theme-aware charts (all were uncommitted there; a backup of that diff is kept outside
  the repos). The template keeps three generic changes: `export_pdf.py` and `install_fonts.ps1` load a project's
  own fonts from `project/design/fonts/`, the design.json test no longer assumes the default colours, and the
  setup skill says to save a competition's rules first. This repo's `general/`, `.claude/skills/` and shared tests
  were copied back from the template so they match it.
- **New look:** from the user's cover (colours sampled from the image: page #171616, yellow #F5E660, gold #B8985A,
  cream #FFF4B2, dull yellow #D8CD6C, grey #C4C4C4). Kept the page, the yellow and the grey; dropped gold, cream and
  the dull yellow (user: the gold is ugly). Square thin-outline boxes replace the rounded ones from section 2; the
  title is a yellow banner with hazard stripes; challenge/solution labels are pills like the cover's.
  `project/design.json`: main F5E660, background 171616, text F2F2F2.
- **Measured:** contrast on #171616: text 16.1, yellow 14.1, grey 10.4, outline grey 5.4, green 10.3, red 7.2;
  dark text on yellow 14.1. The draft (cover + 2 placeholder pages) exports with Montserrat and Caveat only; all
  42 tests pass (37 shared, 5 for this style).
- **Mistake on the way:** the first bullet character (U+25AA) is not in Montserrat, so PowerPoint drew it in Times
  New Roman and the PDF check refused the export. Changed to U+25A0, which Montserrat has.
- **Not done / not proven:** robot drawings are low-resolution crops of the cover image (layout only); no FIRST
  logo; not printed; no real content (AI credit still undecided); event date and members still TODO.
