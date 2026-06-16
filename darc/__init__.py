"""DARC: Degraded-support Adaptive Risk-aware Counterfactual calibration."""

from .calibration import apply_incremental_bias, select_largest_feasible_bias
from .prototypes import DARCPrototype, darc_prototype
from .reliability import RELIABILITY_POLICY, displacement_coherence

__all__ = [
    "DARCPrototype",
    "RELIABILITY_POLICY",
    "apply_incremental_bias",
    "darc_prototype",
    "displacement_coherence",
    "select_largest_feasible_bias",
]

