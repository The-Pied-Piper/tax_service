"""Capabilities: jurisdiction-agnostic mechanisms; parameters come from data.

Each capability registers itself with `@capability` when its module is imported; this package
imports every one of them, so importing the package fills the shared CapabilityRegistry.
`NAMESPACE` comes first because the decorators read it while this file is still being imported.
"""

NAMESPACE = "core"

from app.domain.capabilities import (  # noqa: E402
    apply_rate,
    capped_amount,
    credit_amount,
    lesser_of,
    non_refundable_credit,
    progressive_tax,
    subtract,
    subtract_not_below_zero,
    sum,
)

__all__ = [
    "NAMESPACE",
    "apply_rate",
    "capped_amount",
    "credit_amount",
    "lesser_of",
    "non_refundable_credit",
    "progressive_tax",
    "subtract",
    "subtract_not_below_zero",
    "sum",
]
