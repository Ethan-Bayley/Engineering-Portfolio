---
name: pptx-contact-sheet
description: View many PowerPoint slides at once as one contact-sheet image (10 to 20 slides per picture) to judge layout, type size and rhythm across a deck. Use after building or editing any brochure, poster or deck, and whenever the user asks to see the whole thing or complains about layout or font sizes.
---

# Contact sheet of slides

1. Run (needs Windows PowerPoint; the deck is opened read-only):
   `python general/tools/contact_sheet.py <deck.pptx> --per-sheet 12 --cols 4 --thumb 800`
   Options: `--slides 1-20`, `--per-sheet 20 --cols 5 --thumb 640`, `--out DIR`, `--no-render` to reuse PNGs.
   Output: `project/outputs/renders/sheets/<deck>/sheet_01.png` ... (renders are git-ignored).
2. Read each sheet: header consistency, type sizes that differ between slides, empty or crowded areas, charts and images
   that are too small, anything running off a page.
3. Then read single slides for wording, small text and chart labels.
4. Fix in the build script, rebuild as a new version (`_vNN`), and run the contact sheet again.
