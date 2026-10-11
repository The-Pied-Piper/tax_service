"""The packages whose decorators must run so the shared registries hold their pieces.

Registration happens when a module is imported, and registries never import anything
themselves; the composition root imports this module. An explicit list for now.
"""

import app.adapters.outbound.parameter_parsers.brackets  # noqa: F401  (registers on import)
import app.adapters.outbound.parameter_parsers.credit  # noqa: F401  (registers on import)
import app.domain.capabilities.non_refundable_credit  # noqa: F401  (registers on import)
import app.domain.capabilities.progressive_tax  # noqa: F401  (registers on import)
