"""Risk-controlled old/new logit calibration utilities."""

from __future__ import annotations

from typing import Iterable, Tuple

import torch


def apply_incremental_bias(
    logits: torch.Tensor,
    *,
    base_class_count: int,
    class_count: int,
    beta: float,
) -> torch.Tensor:
    """Apply a logit-level bias to currently introduced incremental classes."""
    if class_count < base_class_count:
        raise ValueError("class_count must be >= base_class_count")
    adjusted = logits.clone()
    if class_count > base_class_count and beta != 0:
        adjusted[:, base_class_count:class_count] += float(beta)
    return adjusted


def _accuracy(logits: torch.Tensor, labels: torch.Tensor) -> float:
    pred = torch.argmax(logits, dim=1)
    return float((pred == labels).float().mean().item() * 100.0)


def select_largest_feasible_bias(
    base_logits: torch.Tensor,
    base_labels: torch.Tensor,
    *,
    base_class_count: int,
    class_count: int,
    beta_candidates: Iterable[float],
    epsilon: float = 1.5,
) -> Tuple[float, float, float]:
    """Select the largest beta satisfying a bounded empirical base-risk rule.

    The constraint is evaluated on base-class calibration logits. No novel
    validation labels are used.
    """
    candidates = sorted({0.0, *[float(beta) for beta in beta_candidates]})
    scores = []
    for beta in candidates:
        adjusted = apply_incremental_bias(
            base_logits,
            base_class_count=base_class_count,
            class_count=class_count,
            beta=beta,
        )
        scores.append((beta, _accuracy(adjusted, base_labels)))

    reference = next(acc for beta, acc in scores if abs(beta) < 1e-12)
    threshold = reference - float(epsilon)
    feasible = [(beta, acc) for beta, acc in scores if acc >= threshold]
    beta, acc = max(feasible, key=lambda item: item[0])
    return beta, acc, reference

