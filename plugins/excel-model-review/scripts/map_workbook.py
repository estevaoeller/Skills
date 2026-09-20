#!/usr/bin/env python3
"""Create a lightweight structural/context map for an Excel workbook."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from model_core import load_book, _text_candidate, _merged


def main():
    p = argparse.ArgumentParser(description="Extract structural anchors/headings from an Excel workbook")
    p.add_argument("file", type=Path)
    p.add_argument("--out", type=Path, default=Path("workbook-map.json"))
    args = p.parse_args()
    wb = load_book(args.file)
    result = {"file": str(args.file.resolve()), "sheets": []}
    for ws in wb.worksheets:
        anchors = []
        for row in ws.iter_rows():
            for c in row:
                if not _text_candidate(c):
                    continue
                bold = bool(getattr(c.font, "bold", False))
                merged = _merged(ws, c.row, c.column)
                size = float(c.font.sz) if getattr(c.font, "sz", None) else None
                if bold or merged or (size and size >= 12) or c.column <= 3:
                    anchors.append({
                        "cell": c.coordinate,
                        "text": str(c.value).strip(),
                        "bold": bold,
                        "merged": merged,
                        "font_size": size,
                    })
        result["sheets"].append({
            "sheet": ws.title,
            "state": ws.sheet_state,
            "max_row": ws.max_row,
            "max_column": ws.max_column,
            "merged_ranges": [str(r) for r in ws.merged_cells.ranges],
            "structural_anchors": anchors,
        })
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Workbook map: {args.out.resolve()}")

if __name__ == "__main__":
    main()
