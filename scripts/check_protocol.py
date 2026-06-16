#!/usr/bin/env python3
"""Check public split/index files for degraded-support FSCIL experiments."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


def read_csv(path: Path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def assert_relative(paths, name):
    bad = [p for p in paths if Path(p).is_absolute()]
    if bad:
        raise AssertionError(f"{name} contains absolute paths, e.g. {bad[0]}")


def check_no_overlap(*named_sets):
    for i, (name_i, set_i) in enumerate(named_sets):
        for name_j, set_j in named_sets[i + 1 :]:
            overlap = set_i & set_j
            if overlap:
                sample = sorted(overlap)[0]
                raise AssertionError(f"{name_i}/{name_j} overlap: {len(overlap)}; sample={sample}")


def check_mcure(root: Path) -> None:
    split = root / "splits/mcure171/csv"
    base = read_csv(split / "base_train_all.csv")
    support = read_csv(split / "incremental_support_5shot_seed2021_actual.csv")
    query = read_csv(split / "query_strict_excluding_incremental_support_seed2021.csv")
    classes = read_csv(split / "classes.csv")

    if len(classes) != 171:
        raise AssertionError(f"mCURE class count expected 171, got {len(classes)}")
    if len(support) != 400:
        raise AssertionError(f"mCURE support expected 400, got {len(support)}")
    if len(query) != 3720:
        raise AssertionError(f"mCURE strict query expected 3720, got {len(query)}")

    assert_relative([r["path"] for r in base + support + query], "mCURE split")
    check_no_overlap(
        ("base", {r["path"] for r in base}),
        ("support", {r["path"] for r in support}),
        ("query", {r["path"] for r in query}),
    )

    per_session = Counter(int(r["session"]) for r in support)
    for session in range(1, 9):
        if per_session[session] != 50:
            raise AssertionError(f"mCURE session {session} expected 50 support rows")
    per_class = Counter(int(r["new_class_id"]) for r in support)
    bad = {cls: n for cls, n in per_class.items() if n != 5}
    if bad:
        raise AssertionError(f"mCURE support must be 5-shot per incremental class: {bad}")
    if len({r["new_class_id"] for r in query}) != 171:
        raise AssertionError("mCURE strict query must cover all 171 classes")

    for shot in (1, 3, 5):
        rows = read_csv(split / f"incremental_support_{shot}shot_seed2021_actual.csv")
        counts = Counter(int(r["new_class_id"]) for r in rows)
        if set(counts.values()) != {shot}:
            raise AssertionError(f"mCURE {shot}-shot support is not exactly {shot}-shot")
    print("mCURE-171 protocol check: PASS")


def check_flowers(root: Path) -> None:
    split = root / "splits/flowers102/csv"
    base = read_csv(split / "base_train_all.csv")
    support = read_csv(split / "incremental_support_5shot_seed2021.csv")
    query = read_csv(split / "query_all_test.csv")
    classes = read_csv(split / "classes.csv")

    if len(classes) != 102:
        raise AssertionError(f"Flowers102 class count expected 102, got {len(classes)}")
    if len(support) != 200:
        raise AssertionError(f"Flowers102 support expected 200, got {len(support)}")
    assert_relative([r["image_path"] for r in base + support + query], "Flowers102 split")
    check_no_overlap(
        ("base", {r["image_path"] for r in base}),
        ("support", {r["image_path"] for r in support}),
        ("query", {r["image_path"] for r in query}),
    )

    per_session = Counter(int(r["session"]) for r in support)
    for session in range(1, 9):
        if per_session[session] != 25:
            raise AssertionError(f"Flowers102 session {session} expected 25 support rows")
    per_class = Counter(int(r["new_class_id"]) for r in support)
    bad = {cls: n for cls, n in per_class.items() if n != 5}
    if bad:
        raise AssertionError(f"Flowers102 support must be 5-shot per incremental class: {bad}")

    for shot in (1, 3, 5):
        rows = read_csv(split / f"incremental_support_{shot}shot_seed2021.csv")
        counts = Counter(int(r["new_class_id"]) for r in rows)
        if set(counts.values()) != {shot}:
            raise AssertionError(f"Flowers102 {shot}-shot support is not exactly {shot}-shot")
    print("Flowers102-FSCIL protocol check: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["mcure171", "flowers102", "all"], default="all")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    if args.dataset in ("mcure171", "all"):
        check_mcure(args.root)
    if args.dataset in ("flowers102", "all"):
        check_flowers(args.root)


if __name__ == "__main__":
    main()

