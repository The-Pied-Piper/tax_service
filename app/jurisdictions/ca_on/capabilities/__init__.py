"""Ontario capabilities: mechanisms specific to an Ontario form, registered under `ca-on/`.

Each capability registers itself with `@capability` when its module is imported; this package
imports every one of them, so importing the package fills the shared CapabilityRegistry.
`NAMESPACE` comes first because the decorators read it while this file is still being imported.
"""

NAMESPACE = "ca-on"

from app.jurisdictions.ca_on.capabilities import (  # noqa: E402
    apply_chosen_rate,
    choose_by_range,
    flow_through_share_expenses,
    rate_by_income_band,
)

__all__ = [
    "NAMESPACE",
    "apply_chosen_rate",
    "choose_by_range",
    "flow_through_share_expenses",
    "rate_by_income_band",
]
