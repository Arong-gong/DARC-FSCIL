# Reproducibility notes

## Minimal verification

Run:

```bash
python scripts/check_protocol.py --dataset all
python scripts/run_darc_eval.py --config configs/mcure171_defocus.yaml --dry-run
python scripts/export_tables.py --check-only
```

These commands validate public split files, paper-facing DARC configs, and
included result-table arithmetic.

## Full image-level reproduction

Full reproduction requires:

1. Raw datasets prepared according to `docs/DATASETS.md`.
2. A CEC-compatible FSCIL backbone implementation.
3. Session-0 checkpoints for mCURE-171 and Flowers102-FSCIL.
4. The released split/index files in `splits/`.

Checkpoints are not committed to git. If released, store them externally and
place them under:

```text
checkpoints/mcure171/session0.pth
checkpoints/flowers102/session0.pth
```

The paper-facing DARC parameters are in `configs/`. The public `darc/` package
contains the prototype correction and risk-controlled calibration logic used by
the reported method.

## Result files

```text
results/paper_ready/main/
results/paper_ready/ablation/
results/paper_ready/shot_sensitivity/
results/paper_ready/severity_robustness/
results/paper_ready/p1_validation/
results/paper_ready/audits/
```

The CSVs are sanitized public summaries and do not contain local experiment
paths.

