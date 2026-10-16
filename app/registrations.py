"""The packages whose decorators must run so the shared registries hold their pieces.

Registration happens when a module is imported, and registries never import anything
themselves; the composition root imports this module. An explicit list for now.
`JURISDICTIONS` lists the jurisdiction packages, whose directories hold their manifests and
parameter data. Adding a jurisdiction `<x>` takes two lines in this module: import
`app.jurisdictions.<x>.catalog` and add `app.jurisdictions.<x>` to `JURISDICTIONS`.
"""

import app.adapters.outbound.parameter_parsers.brackets  # noqa: F401  (registers on import)
import app.adapters.outbound.parameter_parsers.credit  # noqa: F401  (registers on import)
import app.adapters.outbound.parameter_parsers.rate  # noqa: F401  (registers on import)
import app.domain.capabilities.non_refundable_credit  # noqa: F401  (registers on import)
import app.domain.capabilities.progressive_tax  # noqa: F401  (registers on import)
import app.jurisdictions.ca.catalog  # noqa: F401  (registers on import)
import app.jurisdictions.ca_on.catalog  # noqa: F401  (registers on import)
from app.adapters.outbound.jurisdiction_packages import JurisdictionPackages

JURISDICTIONS = JurisdictionPackages((app.jurisdictions.ca, app.jurisdictions.ca_on))
