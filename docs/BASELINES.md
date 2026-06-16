# Baseline methods

The public DARC release does not vendor third-party baseline implementations.
To reproduce the full comparison, use the official repositories and apply the
same degraded-support split/index files released here.

Reported comparison set:

- CEC
- FACT
- LIMIT
- SAVC
- TEEN
- BiDistFSCIL
- DARC

All methods are evaluated under the same class order, support manifest, clean
query set, and support-only degradation protocol. External repositories remain
under their original licenses.

Recommended workflow:

1. Reproduce the CEC-compatible base representation for each dataset.
2. Verify split compatibility with `scripts/check_protocol.py`.
3. Run each baseline using the released support/query manifests.
4. Export Table-I style session-wise HM and final-session old/new metrics.
5. Compare against the CSV files in `results/paper_ready/`.

