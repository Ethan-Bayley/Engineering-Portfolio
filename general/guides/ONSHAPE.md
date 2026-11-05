# Onshape: getting CAD pictures into a project

| | A. API tool | B. Browser + screen grab |
|---|---|---|
| Tool | `general/tools/onshape_images.py` | skill `onshape-capture` + `general/tools/screen_grab.py` |
| Needs | the user's Onshape API keys | Chrome with Claude in Chrome, signed in to Onshape |
| Uses API calls | yes (one per picture) | no |
| Picture quality | clean shaded views at any size, white background | what is on screen; size set by the window; crop and trim |
| Drawings | no | yes: Claude can build a drawing in Onshape step by step (asks first) |
| Speed and reliability | fast, repeatable | slower; depends on Onshape's layout, so check each picture |
| Status | written, tests pass, **not yet run against a real document** | screen grab tested on a Windows window; the Onshape clicks **not yet tried** on a real document |

## A. API keys (only for route A)
1. Make keys at https://dev-portal.onshape.com/keys with **read** permission only.
2. Either set `ONSHAPE_ACCESS_KEY` and `ONSHAPE_SECRET_KEY`, or save `{"access_key": "...", "secret_key": "..."}` as
   `%USERPROFILE%\.onshape\keys.json` (outside every repo). Never paste keys into chat or commit them.
3. Each picture is an API call. Check your plan's API allowance in Onshape before making many.

## B. Browser route
1. Install the Claude in Chrome extension and connect it to Claude (the app's settings) once per computer.
2. Open Onshape in Chrome and sign in yourself.
3. Ask Claude: "get an isometric and a front view of <part> from Onshape" (skill `onshape-capture`).

## Tips for both
- Hide planes and the origin; pick one view per idea (isometric for the whole thing, front or side for sizes).
- Use the same view and crop for before/after pictures so they compare.
- Label parts with `box.labelled(...)` arrows instead of text on the CAD image.
