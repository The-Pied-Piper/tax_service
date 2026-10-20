"""Ontario (`CA-ON`): its artifact catalog, the CA-ON manifest and the `ca-on/...` datasets.

The manifest also selects federal capabilities, whose kinds and data live in `app.jurisdictions.ca`.
Importing the package imports its `capabilities` package, which registers Ontario's capabilities.
"""

NAMESPACE = "ca-on"

from app.jurisdictions.ca_on import capabilities  # noqa: E402

__all__ = ["NAMESPACE", "capabilities"]
