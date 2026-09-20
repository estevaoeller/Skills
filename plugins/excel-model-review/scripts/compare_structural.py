#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from model_core import compare_pair, write_area_csv, write_evidence_csv, write_pair_markdown


def main():
    p = argparse.ArgumentParser(description="Compare two Excel model versions by structural areas/blocks.")
    p.add_argument("old_file", type=Path)
    p.add_argument("new_file", type=Path)
    p.add_argument("--out", type=Path, default=Path("excel-model-diff-report"))
    p.add_argument("--row-gap", type=int, default=2)
    p.add_argument("--col-gap", type=int, default=2)
    p.add_argument("--abs-tol", type=float, default=0.0)
    p.add_argument("--rel-tol", type=float, default=0.0)
    args = p.parse_args()
    for f in (args.old_file, args.new_file):
        if not f.exists(): p.error(f"File not found: {f}")
        if f.suffix.lower() not in {".xlsx", ".xlsm"}: p.error(f"Unsupported Excel format: {f.suffix}")
    args.out.mkdir(parents=True, exist_ok=True)
    report = compare_pair(args.old_file, args.new_file, args.row_gap, args.col_gap, args.abs_tol, args.rel_tol)
    (args.out / "diff.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_area_csv(report, args.out / "areas.csv")
    write_evidence_csv(report, args.out / "evidence_cells.csv")
    write_pair_markdown(report, args.out / "summary.md")
    print(f"Areas changed: {report['summary']['areas_changed']}")
    print(f"Cell evidence: {report['summary']['cell_evidence_count']}")
    print(f"Reports: {args.out.resolve()}")

if __name__ == "__main__":
    main()
