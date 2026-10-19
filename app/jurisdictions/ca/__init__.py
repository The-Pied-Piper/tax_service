"""Federal Canada (`CA`): the federal artifact catalog, the `ca/...` parameter datasets and its
capabilities.

Importing the package imports its `capabilities` package, which registers the federal capabilities.
"""

NAMESPACE = "ca"

from app.jurisdictions.ca import capabilities  # noqa: E402

__all__ = ["NAMESPACE", "capabilities"]
