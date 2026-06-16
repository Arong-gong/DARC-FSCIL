"""Metrics used by DARC result checks."""

from __future__ import annotations


def harmonic_mean(old_acc: float, new_acc: float) -> float:
    """Return the old/new harmonic mean in percentage units."""
    old_acc = float(old_acc)
    new_acc = float(new_acc)
    if old_acc <= 0.0 or new_acc <= 0.0:
        return 0.0
    return 2.0 * old_acc * new_acc / (old_acc + new_acc)

