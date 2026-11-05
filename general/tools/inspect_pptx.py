#!/usr/bin/env python3
"""Create a portable JSON text-and-geometry inventory for a PowerPoint deck."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from pptx import Presentation


EMU_PER_POINT = 12700


def points(value: int) -> float:
    return round(value / EMU_PER_POINT, 2)


def record(name: str, kind: str, left: int, top: int, width: int, height: int, text: str) -> dict:
    return {
        "name": name,
        "type": kind,
        "left": points(left),
        "top": points(top),
        "width": points(width),
        "height": points(height),
        "text": text,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("presentation", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    presentation = Presentation(args.presentation)
    slides = []
    for number, slide in enumerate(presentation.slides, start=1):
        text_shapes = []
        for shape in slide.shapes:
            if getattr(shape, "has_table", False):
                row_top = shape.top
                for row_index, row in enumerate(shape.table.rows, start=1):
                    column_left = shape.left
                    for column_index, cell in enumerate(row.cells, start=1):
                        if cell.text:
                            text_shapes.append(
                                record(
                                    f"{shape.name}[r{row_index}c{column_index}]",
                                    "table_cell",
                                    column_left,
                                    row_top,
                                    shape.table.columns[column_index - 1].width,
                                    row.height,
                                    cell.text,
                                )
                            )
                        column_left += shape.table.columns[column_index - 1].width
                    row_top += row.height
            elif getattr(shape, "has_text_frame", False) and shape.text:
                text_shapes.append(
                    record(shape.name, str(shape.shape_type), shape.left, shape.top, shape.width, shape.height, shape.text)
                )
        notes = ""
        try:
            notes = slide.notes_slide.notes_text_frame.text
        except (AttributeError, ValueError):
            pass
        slides.append(
            {
                "number": number,
                "slide_id": slide.slide_id,
                "name": f"Slide {number}",
                "layout": slide.slide_layout.name,
                "hidden": False,
                "text_shapes": text_shapes,
                "notes": notes,
            }
        )

    inventory = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "source": str(args.presentation.resolve()),
        "slide_width": points(presentation.slide_width),
        "slide_height": points(presentation.slide_height),
        "slide_count": len(presentation.slides),
        "designs": [],
        "slides": slides,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote inventory: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
