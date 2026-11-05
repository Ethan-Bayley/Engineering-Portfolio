---
name: build-log
description: Turn the user's build photos (phone photos dropped in project/assets/photos/raw/) and their notes into dated build-log entries in project/logs/BUILD_LOG.md, with the photos prepared for the deliverable. Use when the user adds build photos, says what they built today, or asks to write up the build.
---

# Build log from photos

1. **Find new photos.** List `project/assets/photos/raw/` and compare with what `BUILD_LOG.md` and
   `project/assets/CREDITS.md` already mention. Only new ones.
2. **Prepare them:** `python general/tools/photo_prep.py` (upright, 1600 px, JPEG into `ready/`). Never edit the raw files.
3. **Date and order them.** Use the photo's EXIF date (`python general/tools/photo_prep.py --dates` prints file, date,
   size); fall back to the file's modified date and say so. Group photos taken the same day into one entry.
4. **Look at each photo** (Read the ready copy) and describe only what is visible: parts, tools, stage of the build.
   Do not guess what isn't shown (measurements, whether it worked). Ask the user (AskUserQuestion, one round) for
   what the photos can't say: what was done, what went wrong, how it was fixed, time taken, parts used.
5. **Write the entry** (append to `project/logs/BUILD_LOG.md`):

```markdown
## <date>: <stage, e.g. "Fingers assembled">
- Done: <steps, from the user>
- Parts and tools: <...>
- Problems and fixes: <what went wrong, what was changed> (or "none reported")
- Time: <hours, from the user> (or "not recorded")
- Photos: `ready/<file>.jpg` (<what it shows>), ...
```

6. **Credits.** Add each photo to `project/assets/CREDITS.md` as "own photo, <date>" unless the user says otherwise.
7. **Decisions.** If a problem led to a design change, also add a section to `DECISIONS.md` (skill `log-work`).
8. For the deliverable: a build-process page is a `box.timeline` or `box.steps` of the entries plus photos with
   `box.labelled(...)` arrows to the parts (skill `draft-page`). Real photos are never edited beyond crop and
   rotation (WORKING_RULES.md).
