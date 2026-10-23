"""English text for the Ontario trace lines: one renderer class per line class.

Each module renders the lines of the module of the same name in `app.jurisdictions.ca_on.trace`,
registering its renderers with `@english_renderer`; this package imports every one of them.
"""

from __future__ import annotations

from app.jurisdictions.ca_on.trace_english import dependants, foreign_tax, placement_credit

__all__ = ["dependants", "foreign_tax", "placement_credit"]
