"""English rendering of the structured trace: one readable sentence per trace line.

The domain records facts; this adapter turns them into the text a reader sees, line by line, like
the tax authority's own worksheet. Each line class's text is a renderer class registered with
`@english_renderer`, in the module named after its line class's module in `app.domain.trace`;
this package imports every one of them, so importing it fills the shared EnglishRendererRegistry.
A new feature module of trace lines adds its renderer module here. Other languages get their own
package.
"""

from __future__ import annotations

from app.adapters.inbound.trace_english import (
    arithmetic,
    capital_cost,
    choices,
    dependants,
    figures,
    gains,
    placement_credit,
    rate_tables,
    record_lists,
    registry,
    renderer,
    rentals,
)
from app.adapters.inbound.trace_english.renderer import EnglishTraceRenderer

__all__ = [
    "EnglishTraceRenderer",
    "arithmetic",
    "capital_cost",
    "choices",
    "dependants",
    "figures",
    "gains",
    "placement_credit",
    "rate_tables",
    "record_lists",
    "registry",
    "renderer",
    "rentals",
]
