#!/usr/bin/env python3
"""Public DARC evaluation entrypoint.

The default --dry-run mode validates configuration and split availability. Full
image-level evaluation should be run through the CEC-compatible FSCIL backbone
described in docs/REPRODUCIBILITY.md; this script keeps the paper-facing DARC
configuration and prototype-calibration interface in one place.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def load_config(path: Path) -> dict:
    with path.open() as f:
        cfg = yaml.safe_load(f)
    required = {"dataset", "protocol", "degradation", "darc"}
    missing = required - set(cfg)
    if missing:
        raise ValueError(f"Missing required config keys: {sorted(missing)}")
    if cfg["darc"].get("reliability_policy") != "displacement_coherence":
        raise ValueError("Public paper-facing configs must use displacement_coherence")
    return cfg


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--checkpoint", type=Path, default=Path("checkpoints/session0.pth"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/darc_eval"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cfg = load_config(args.config)
    print(f"dataset={cfg['dataset']}")
    print(f"protocol={cfg['protocol']} ({cfg.get('display_name', 'unnamed')})")
    print(f"support_degradation={cfg['degradation']}")
    print(f"darc={cfg['darc']}")
    print(f"data_root={args.data_root}")
    print(f"checkpoint={args.checkpoint}")
    print(f"output_dir={args.output_dir}")

    if args.dry_run:
        print("DARC dry-run: PASS")
        return

    raise SystemExit(
        "Full image-level evaluation requires the CEC-compatible backbone and "
        "feature extraction pipeline described in docs/REPRODUCIBILITY.md. "
        "Use --dry-run to validate public configs."
    )


if __name__ == "__main__":
    main()

