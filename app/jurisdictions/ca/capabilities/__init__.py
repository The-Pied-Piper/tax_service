"""Federal Canada's capabilities: mechanisms specific to its forms, parameters from data.

Each capability registers itself with `@capability` when its module is imported; this package
imports every one of them, so importing the package fills the shared CapabilityRegistry.
`NAMESPACE` comes first because the decorators read it while this file is still being imported.
"""

NAMESPACE = "ca"

from app.jurisdictions.ca.capabilities import caregiver_amount  # noqa: E402

__all__ = ["NAMESPACE", "caregiver_amount"]
