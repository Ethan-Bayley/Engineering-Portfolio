#!/usr/bin/env python3
"""Heuristic first-pass audit of a deck from an inspect_pptx.py inventory: placeholders, empty/wordy slides, missing notes.

This is a keyword scan, not a quality score. Always look at the rendered slides too.
Usage: python general/tools/audit_deck.py inventory.json --output audit.md [--max-words 120]
"""
import argparse
import json
import re
from pathlib import Path

PLACEHOLDERS = {
    "TODO marker": re.compile(r"\bTODO\b", re.I),
    "lorem ipsum": re.compile(r"lorem ipsum", re.I),
    "click to add / placeholder text": re.compile(r"click to (add|edit)|your (title|text) here", re.I),
    "placeholder figure number": re.compile(r"\b(Figure|Table)\s+X\b", re.I),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inventory", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--max-words", type=int, default=120)
    a = ap.parse_args()
    data = json.loads(a.inventory.read_text(encoding="utf-8-sig"))
    out = [f"# Heuristic deck audit", "", f"Inventory: `{a.inventory}`  |  slides: {len(data['slides'])}", "",
           "> Keyword scan only. Check the renders and the sources.", ""]
    flags = []
    for s in data["slides"]:
        text = "\n".join(t.get("text", "") for t in s.get("text_shapes", []))
        words = len(text.split())
        n = s["number"]
        if words == 0:
            flags.append(f"- Slide {n}: no text")
        elif words > a.max_words:
            flags.append(f"- Slide {n}: {words} words (over {a.max_words}); consider cutting")
        for label, pat in PLACEHOLDERS.items():
            if pat.search(text):
                flags.append(f"- Slide {n}: {label}")
        if not s.get("notes", "").strip():
            flags.append(f"- Slide {n}: no speaker notes / source note")
    out += ["## Flags", ""] + (flags or ["- none"]) + [""]
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text("\n".join(out), encoding="utf-8")
    print("wrote", a.output)


if __name__ == "__main__":
    main()
