"""Counterfactual prototype construction for degraded-support FSCIL."""

from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn.functional as F

from .reliability import displacement_coherence


@dataclass(frozen=True)
class DARCPrototype:
    """Output of one DARC prototype correction."""

    prototype: torch.Tensor
    rho: float
    eta: float
    reliability: float
    neighbor_indices: torch.Tensor


def darc_prototype(
    degraded_support_proto: torch.Tensor,
    clean_base_anchors: torch.Tensor,
    degraded_base_anchors: torch.Tensor,
    *,
    k: int = 3,
    alpha: float = 1.0,
    rho_min: float = 0.6,
    rho_max: float = 1.0,
    eta_min: float = 0.0,
    eta_max: float = 0.05,
    tau: float = 1.0,
    eps: float = 1e-8,
) -> DARCPrototype:
    """Construct a clean-domain aligned novel prototype.

    Angularly normalized degraded anchors are used only for neighbor retrieval.
    The actual counterfactual anchors and residual transport are computed in the
    base-learned classifier-coordinate feature space, followed by norm
    restoration to the raw degraded support prototype norm.
    """
    if degraded_support_proto.ndim != 1:
        raise ValueError("degraded_support_proto must be a 1-D tensor")
    if clean_base_anchors.shape != degraded_base_anchors.shape:
        raise ValueError("clean_base_anchors and degraded_base_anchors must match")
    if clean_base_anchors.ndim != 2:
        raise ValueError("base anchors must be 2-D tensors")
    if k < 1:
        raise ValueError("k must be positive")

    raw_norm = degraded_support_proto.norm(p=2).clamp_min(eps)
    degraded_norm = F.normalize(degraded_base_anchors, p=2, dim=-1, eps=eps)
    support_dir = F.normalize(degraded_support_proto.unsqueeze(0), p=2, dim=-1, eps=eps).squeeze(0)
    sims = torch.mv(degraded_norm, support_dir)
    values, indices = torch.topk(sims, min(k, degraded_norm.size(0)))
    weights = F.softmax(values / float(tau), dim=0)

    clean_neighbors = clean_base_anchors[indices]
    degraded_neighbors = degraded_base_anchors[indices]
    degraded_anchor = torch.sum(degraded_neighbors * weights.unsqueeze(1), dim=0)
    clean_anchor = torch.sum(clean_neighbors * weights.unsqueeze(1), dim=0)

    reliability = displacement_coherence(values, clean_neighbors, degraded_neighbors, tau=tau)
    rho = rho_min + (rho_max - rho_min) * reliability
    eta = eta_min + (eta_max - eta_min) * (1.0 - reliability)

    transported = clean_anchor + alpha * rho * (degraded_support_proto - degraded_anchor)
    corrected = (1.0 - eta) * transported + eta * clean_anchor
    restored = F.normalize(corrected.unsqueeze(0), p=2, dim=-1, eps=eps).squeeze(0) * raw_norm

    return DARCPrototype(
        prototype=restored,
        rho=float(rho.detach().cpu()),
        eta=float(eta.detach().cpu()),
        reliability=float(reliability.detach().cpu()),
        neighbor_indices=indices.detach().cpu(),
    )

