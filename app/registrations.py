"""The packages the composition root wires together, listed explicitly.

`CORE_PACKAGES` names the core packages whose decorators fill the shared capability, parameter
parser and English trace renderer registries: each one's `__init__.py` imports its modules, so
importing this module runs them. `JURISDICTIONS` lists the jurisdiction packages; importing one
registers only its own capabilities and trace line renderers, through the `capabilities` and
`trace_english` packages its `__init__.py` imports, and `JURISDICTIONS.register()`, called by the
composition root at startup, registers their artifact catalogs. Adding a jurisdiction `<x>` is
importing `app.jurisdictions.<x>` and adding it to `JURISDICTIONS`.
"""

import app.adapters.inbound.trace_english
import app.adapters.outbound.parameter_parsers
import app.domain.capabilities
import app.jurisdictions.ca
import app.jurisdictions.ca_on
from app.adapters.outbound.jurisdiction_packages import JurisdictionPackages

CORE_PACKAGES = (
    app.domain.capabilities,
    app.adapters.outbound.parameter_parsers,
    app.adapters.inbound.trace_english,
)

JURISDICTIONS = JurisdictionPackages((app.jurisdictions.ca, app.jurisdictions.ca_on))
