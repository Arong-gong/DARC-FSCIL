#!/usr/bin/env python3
"""Sanity-check paper-ready CSV tables included in the public release."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from darc.metrics import harmonic_mean


def read_csv(path: Path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def check_final_table(path: Path) -> None:
    rows = read_csv(path)
    for row in rows:
        old = float(row.get("Old/Base Acc.") or row.get("Old") or row.get("old_base_acc"))
        new = float(row.get("New/Inc. Acc.") or row.get("New") or row.get("new_incremental_acc"))
        hm = float(row.get("HM") or row.get("harmonic_mean"))
        expected = harmonic_mean(old, new)
        if abs(expected - hm) > 0.01:
            raise AssertionError(f"HM mismatch in {path}: {row}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    result_root = args.root / "results/paper_ready"

    for rel in [
        "main/mcure_table2_final_comparison.csv",
        "main/flowers102_table2_final_comparison.csv",
        "ablation/tableB_all_ablation_final_old_new.csv",
        "shot_sensitivity/flowers102_shot_final_old_new.csv",
        "severity_robustness/flowers102_severity_final_old_new.csv",
    ]:
        check_final_table(result_root / rel)
    print("paper-ready table checks: PASS")


if __name__ == "__main__":
    main()
