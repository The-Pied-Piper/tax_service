"""The packages the composition root wires together, listed explicitly.

`CORE_PACKAGES` names the packages whose decorators fill the shared capability and parameter
parser registries, the core ones and the capability packages of a jurisdiction: each one's
`__init__.py` imports its modules, so importing this module runs them. `JURISDICTIONS` lists the
jurisdiction packages; importing one registers nothing, and `JURISDICTIONS.register()`, called by
the composition root at startup, registers their artifact catalogs. Adding a jurisdiction `<x>` is
importing `app.jurisdictions.<x>` and adding it to `JURISDICTIONS`.
"""

import app.adapters.outbound.parameter_parsers
import app.domain.capabilities
import app.jurisdictions.ca
import app.jurisdictions.ca_on
import app.jurisdictions.ca_on.capabilities
from app.adapters.outbound.jurisdiction_packages import JurisdictionPackages

CORE_PACKAGES = (
    app.domain.capabilities,
    app.adapters.outbound.parameter_parsers,
    app.jurisdictions.ca_on.capabilities,
)

JURISDICTIONS = JurisdictionPackages((app.jurisdictions.ca, app.jurisdictions.ca_on))
