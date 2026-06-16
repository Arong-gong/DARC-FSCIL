# DARC-FSCIL

Official implementation of **DARC: Degraded-support Adaptive
Risk-aware Counterfactual calibration**.

DARC is a representation-preserving framework for degradation-aware
incremental classifier construction in few-shot class-incremental learning
(FSCIL). It assumes that a base recognition space has already been learned, and
focuses on constructing incremental classifiers when novel support examples are
degraded by defocus blur or motion blur while query/test images remain clean.

The paper-facing method uses three components:

1. **Base-anchored counterfactual geometry** estimates degradation-induced
   prototype displacement from paired clean/degraded base anchors.
2. **Reliability-adaptive residual transport** corrects degraded novel support
   prototypes while preserving reliable class-specific residuals.
3. **Empirically risk-controlled decision calibration** selects the largest
   feasible incremental-class bias under a bounded base-risk criterion.

## Repository contents

```text
darc/          Core DARC prototype and calibration utilities.
configs/       Paper-ready mCURE-171 and Flowers102-FSCIL DARC configs.
splits/        Public split/index files with relative paths only.
scripts/       Protocol checks, config dry-runs, and table sanity checks.
results/       Paper-ready CSV summaries without local source paths.
docs/          Dataset, protocol, baseline, and reproducibility notes.
checkpoints/   Placeholder for externally hosted session-0 checkpoints.
```

Raw images and trained weights are **not** stored in this repository.

## Quick start

```bash
git clone https://github.com/Arong-gong/DARC-FSCIL.git
cd DARC-FSCIL
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/check_protocol.py --dataset all
python scripts/run_darc_eval.py --config configs/flowers102_defocus.yaml --dry-run
python scripts/export_tables.py --check-only
```

Expected output:

```text
mCURE-171 protocol check: PASS
Flowers102-FSCIL protocol check: PASS
DARC dry-run: PASS
paper-ready table checks: PASS
```

## Data

This repository releases split/index files only. See
[`docs/DATASETS.md`](docs/DATASETS.md) for dataset acquisition and expected
directory layouts.

- mCURE-171: 91 base classes and 8 incremental sessions of 10-way 5-shot.
- Flowers102-FSCIL: 62 base classes and 8 incremental sessions of 5-way 5-shot.
- The main degraded-support benchmark uses Defocus-Support and Motion-Support.
- Degradation is applied only to incremental support images; query/test images
  remain clean.

## Reproducing paper-facing results

The included CSV files are the paper-ready result summaries. For full
image-level reproduction, prepare the datasets, install a CEC-compatible FSCIL
backbone, and place session-0 checkpoints under `checkpoints/`. See
[`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md).

Baseline methods are not vendored into this repository. Their official sources
and adaptation notes are listed in [`docs/BASELINES.md`](docs/BASELINES.md).

## Citation

```bibtex
@article{darc2026,
  title   = {Adaptive Counterfactual Prototype Calibration for Degraded-Support Few-Shot Class-Incremental Learning},
  author  = {Anonymous},
  journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence},
  year    = {2026},
  note    = {Manuscript under review}
}
```

## License

This DARC release is distributed under the MIT License. External baseline
repositories and datasets are governed by their own licenses and terms.
