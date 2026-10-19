"""Ontario capabilities: mechanisms specific to an Ontario form, registered under `ca-on/`.

Each capability registers itself with `@capability` when its module is imported; this package
imports every one of them, so importing the package fills the shared CapabilityRegistry.
`NAMESPACE` comes first because the decorators read it while this file is still being imported.
"""

NAMESPACE = "ca-on"

from app.jurisdictions.ca_on.capabilities import flow_through_share_expenses  # noqa: E402

__all__ = ["NAMESPACE", "flow_through_share_expenses"]
