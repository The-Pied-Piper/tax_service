"""English text for the federal Canada trace lines: one renderer class per line class.

Each module renders the lines of the module of the same name in `app.jurisdictions.ca.trace`,
registering its renderers with `@english_renderer`; this package imports every one of them.
"""

from __future__ import annotations

from app.jurisdictions.ca.trace_english import (
    apprenticeship,
    capital_cost,
    dependants,
    foreign_tax,
    gains,
    rentals,
)

__all__ = ["apprenticeship", "capital_cost", "dependants", "foreign_tax", "gains", "rentals"]
