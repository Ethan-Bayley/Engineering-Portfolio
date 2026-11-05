# Independent review loop (for substantial decks and posters)

Adapted from the Enginnering-Notebook-ai repo, with the notebook/rubric parts removed.

1. Build from the brief (`project/brief/`) into `project/outputs/<deliverable>/`.
2. Render every slide (`general/tools/export_pdf.py --render`), then run `general/tools/inspect_pptx.py` and `general/tools/audit_deck.py`.
3. Review in a **separate, read-only** pass: a sub-agent if the user asked for one, otherwise a clearly separate second
   pass by you, saying so in the log. The reviewer does not edit.
4. Save findings under `project/outputs/reviews/` as `### [Critical|High|Medium|Low] Title`, then Location, Evidence, Risk, Fix,
   Resolution (fixed / rejected with reason / TODO).
5. Fix valid findings, rebuild, re-render, review again until no Critical or High remain.

| Check | Question |
|---|---|
| Accuracy | Every number matches the project logs (`project/logs/`) and its source; simulated or assumed values are labelled |
| Honesty | Nothing beyond the evidence; untested things say so |
| Brief | Uses the images and message the user chose, nothing else |
| Layout | No clipping, overlap, text under 14 pt (poster) or 18 pt (slides), no big dead space |
| Accessibility | Alt text on pictures, contrast, reading order |
| Safety | No source deck overwritten; nothing sent to real hardware |

Severity: Critical = false or unsafe content, unreadable output. High = unsupported claim, contradiction, item from the
brief missing. Medium = weak hierarchy, inconsistent terms. Low = wording, alignment.
