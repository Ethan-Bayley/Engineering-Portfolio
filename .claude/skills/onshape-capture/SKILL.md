---
name: onshape-capture
description: Get CAD pictures and drawings out of Onshape without the Onshape API (no API keys, no API calls): drive Onshape in the user's Chrome with Claude in Chrome to set up views or make a drawing, then save the window with general/tools/screen_grab.py. Use when the user wants CAD screenshots, views, renders or drawings from Onshape, especially when they mention API credits or have no API keys.
---

# Onshape pictures and drawings, no API

Two routes; this skill is route B. Background and set-up for both: `general/guides/ONSHAPE.md`.
- A. `general/tools/onshape_images.py`: Onshape REST API, needs the user's API keys, uses API calls.
- **B. This skill:** Claude in Chrome clicks in Onshape like a person; `screen_grab.py` saves what is on screen. No keys, no
  API calls. Slower and depends on the screen, so check every picture.

## Before starting
1. Read the `anthropic-skills:chrome-browser` skill, then load the Chrome tools in one ToolSearch call (tabs_context,
   tabs_create, navigate, computer, read_page, find). Computer use cannot click inside browsers, so use Claude in Chrome.
2. Ask the user for the Onshape document link (or the part / assembly name). Work in a **new tab**; leave their tabs alone.
3. If Onshape shows a sign-in page, ask the user to sign in themselves in that tab. Never type their password.
4. Ask before changing their document (adding a drawing tab, hiding parts, changing appearances). Viewing,
   rotating and zooming change nothing and need no asking. Onshape keeps a version history, so say what you changed.

## Views (pictures of the model)
1. Open the Part Studio or Assembly tab. Take a screenshot to see the layout.
2. Clean the view: hide the default planes and origin if shown (eye icons in the feature list); close dialogs. Collapse
   the feature list only if the user agrees it can stay collapsed.
3. Set the view with the view cube (top right of the graphics area) or keyboard shortcuts. Onshape's usual shortcuts
   are `Shift+1` to `Shift+7` (front, back, left, right, top, bottom, isometric) and `F` (zoom to fit); check them in
   Onshape's shortcut list the first time and fix this line if they differ.
4. Save it:
   ```bash
   python general/tools/screen_grab.py --window Onshape --name <part>_<view> --crop <l,t,r,b> --trim --note "<what it shows>"
   ```
   Find the crop from a first grab without `--crop` (Read the PNG: the graphics area without the browser bar, toolbar,
   feature list and view cube), then reuse the same crop for every view so they match. Chrome must be on screen,
   not minimised or covered. Bigger window = more pixels: maximise Chrome first.
5. Read every saved PNG and check: the whole model in frame, no menus or cursor, no planes, background trimmed.
   Delete and redo bad ones.

## Drawings (2D, dimensioned)
Only after the user says to create one (it adds a tab to their document).
1. From the Part Studio: the `+` button (bottom left) → Create Drawing (or right-click the Part Studio tab) → pick the
   part, a template and sheet size (A4 landscape or A3 to suit the page).
2. Place views: front, top, right and an isometric; let Onshape align them.
3. Dimensions: the Dimension tool; overall sizes first, then the ones the design depends on (ask the user which
   matter). Units in mm.
4. Take a screenshot after every few steps; if a click went wrong, undo (`Ctrl+Z`) and say so.
5. Get it out: `screen_grab.py --window Onshape --name <part>_drawing --crop ...` (no download needed). If the user
   wants Onshape's own PDF or DXF export, ask before downloading (state the file name), then move it from Downloads to
   `project/assets/cad/`.

## After
- List each picture in `project/assets/CREDITS.md` as "own CAD (Onshape), <date>". The grab log is
  `project/assets/cad/SCREEN_GRAB_LOG.md`.
- In the deliverable: `box.picture(...)` or `box.labelled(...)` with arrows to the parts.
- If a step in this skill was wrong for the current Onshape (menu names move), fix this file in project-template.
