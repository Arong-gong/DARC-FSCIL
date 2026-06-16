"""Reliability policies used by the paper-facing DARC implementation."""

from __future__ import annotations

import torch
import torch.nn.functional as F


RELIABILITY_POLICY = "displacement_coherence"


def displacement_coherence(
    similarities: torch.Tensor,
    clean_neighbors: torch.Tensor,
    degraded_neighbors: torch.Tensor,
    tau: float = 1.0,
) -> torch.Tensor:
    """Return directional agreement among local counterfactual displacements.

    The returned scalar lies in [0, 1]. It is high when the selected clean-to-
    degraded displacement directions agree, and low when local base neighbors
    imply conflicting degradation directions.
    """
    weights = F.softmax(similarities / float(tau), dim=0)
    directions = F.normalize(clean_neighbors - degraded_neighbors, p=2, dim=-1)
    reliability = torch.sum(directions * weights.unsqueeze(1), dim=0).norm(p=2)
    return reliability.clamp(0.0, 1.0)

