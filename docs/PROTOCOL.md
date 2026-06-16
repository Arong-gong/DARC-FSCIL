# Degraded-support FSCIL protocol

The benchmark isolates classifier-construction failure under degraded support.

- Base training images are clean.
- Query/test images are clean.
- Only incremental support images are degraded.
- Main support availability is 5-shot.
- Defocus-Support uses defocus blur with radius 4.0.
- Motion-Support uses motion blur with length 15.

DARC does not alter the base representation or session-0 classifier. It
constructs corrected incremental prototypes in the established base recognition
space and applies empirically risk-controlled old/new calibration.

Paper-facing DARC configurations use:

```text
reliability_policy = displacement_coherence
k = 3
rho_max = 1.0
eta_min = 0.0
epsilon = 1.5
```

Dataset/protocol-specific values are listed in `configs/*.yaml`.

