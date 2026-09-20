#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from model_core import compare_pair, consolidate_evolution, write_evolution_markdown


def main():
    p = argparse.ArgumentParser(description="Reconstruct Excel model evolution across ordered workbook versions.")
    p.add_argument("files", nargs="+", type=Path, help="Ordered Excel versions, oldest to newest")
    p.add_argument("--out", type=Path, default=Path("excel-model-evolution-report"))
    p.add_argument("--row-gap", type=int, default=2)
    p.add_argument("--col-gap", type=int, default=2)
    args = p.parse_args()
    if len(args.files) < 2: p.error("Provide at least two workbook versions")
    for f in args.files:
        if not f.exists(): p.error(f"File not found: {f}")
        if f.suffix.lower() not in {".xlsx", ".xlsm"}: p.error(f"Unsupported Excel format: {f.suffix}")
    args.out.mkdir(parents=True, exist_ok=True)
    pairs = [compare_pair(args.files[i], args.files[i+1], args.row_gap, args.col_gap) for i in range(len(args.files)-1)]
    names = [f.name for f in args.files]
    report = consolidate_evolution(pairs, names)
    (args.out / "evolution.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_evolution_markdown(report, args.out / "evolution.md")
    print(f"Versions: {len(names)}")
    print(f"Evolution threads: {len(report['threads'])}")
    print(f"Reports: {args.out.resolve()}")

if __name__ == "__main__":
    main()
