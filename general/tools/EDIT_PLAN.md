# PowerPoint edit plan (pptx_ops.ps1)

Adapted from the Enginnering-Notebook-ai repo. Needs Windows PowerPoint. Always run with `-ExecutionPolicy Bypass` (scripts are blocked otherwise; it only affects that one process). Paths are examples.

The editor supports `Inspect`, `ApplyPlan`, and `Render` actions. It uses the installed Windows PowerPoint application so the deck's native formatting is retained.

## Inspect

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File general\tools\pptx_ops.ps1 `
  -Action Inspect `
  -InputPath "project\outputs\source.pptx" `
  -ReportPath "project\outputs\renders\source.json"
```

## Edit plan schema

```json
{
  "operations": [
    {
      "op": "duplicate_slide",
      "id": "new-slide",
      "source_slide": 120,
      "after_slide": 130,
      "replacements": [
        {"find": "Old title", "replace": "Slide title"}
      ]
    },
    {
      "op": "replace_text",
      "slide": "new-slide",
      "find": "Old body text",
      "replace": "Replacement text"
    },
    {
      "op": "set_shape_text",
      "slide": "new-slide",
      "shape": "Title 1",
      "text": "Slide title"
    },
    {
      "op": "add_image",
      "slide": "new-slide",
      "path": "C:\\path\\to\\test-photo.jpg",
      "left": 500,
      "top": 180,
      "width": 360,
      "height": 240,
      "alt_text": "intake test setup"
    },
    {
      "op": "set_notes",
      "slide": "new-slide",
      "text": "Sources: testing log path; photo path"
    }
  ]
}
```

Coordinates and sizes are PowerPoint points. One inch is 72 points.

`slide` accepts a 1-based slide number or the `id` of an earlier `duplicate_slide` operation. `after_slide` accepts the same forms. A duplicated slide is inserted immediately after its source when `after_slide` is omitted.

Use `replace_text` to retain styled runs. Use `set_shape_text` only when the target shape name is known from the inventory and replacing existing text is impractical.

## Apply to a copy

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File general\tools\pptx_ops.ps1 `
  -Action ApplyPlan `
  -InputPath "project\outputs\source.pptx" `
  -OutputPath "project\outputs\working-copy.pptx" `
  -PlanPath "project\outputs\edit-plan.json"
```

The script refuses an existing output file and refuses to overwrite the input unless `-AllowOverwrite` is deliberately supplied.

## Render

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File general\tools\pptx_ops.ps1 `
  -Action Render `
  -InputPath "project\outputs\working-copy.pptx" `
  -OutputPath "project\outputs\renders\working-copy" `
  -Slides "120,131-133"
```

Inspect every changed PNG. Saving without errors does not prove the slide is visually correct.
