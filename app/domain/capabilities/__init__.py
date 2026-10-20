"""Capabilities: jurisdiction-agnostic mechanisms; parameters come from data.

Each capability registers itself with `@capability` when its module is imported; this package
imports every one of them, so importing the package fills the shared CapabilityRegistry.
`NAMESPACE` comes first because the decorators read it while this file is still being imported.
"""

NAMESPACE = "core"

from app.domain.capabilities import (  # noqa: E402
    apply_fraction,
    apply_rate,
    at_most,
    capped_amount,
    choose_by_count,
    contribution_tier,
    credit_amount,
    greater_of,
    lesser_of,
    multiple_over,
    per_unit_amount,
    progressive_tax,
    subtract,
    subtract_not_below_zero,
    sum,
    tapered_amount,
    tiered_surcharge,
    times_count,
)

__all__ = [
    "NAMESPACE",
    "apply_fraction",
    "apply_rate",
    "at_most",
    "capped_amount",
    "choose_by_count",
    "contribution_tier",
    "credit_amount",
    "greater_of",
    "lesser_of",
    "multiple_over",
    "per_unit_amount",
    "progressive_tax",
    "subtract",
    "subtract_not_below_zero",
    "sum",
    "tapered_amount",
    "tiered_surcharge",
    "times_count",
]
