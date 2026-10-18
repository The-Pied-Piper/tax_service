"""Parsers for the kind-specific part of YAML parameter datasets.

Each parser handles one parameter kind: the keys it adds to a dataset file and
how to turn them into that kind's values. Parsers register themselves with
`@parameter_parser` when their module is imported, and YamlParameterSource looks them up by kind
in a ParameterParserRegistry. This package imports every parser module, so importing it fills the
shared registry; adding a kind means adding a parser and importing it here.
"""

from __future__ import annotations

from app.adapters.outbound.parameter_parsers import (
    amount,
    brackets,
    contribution_tier,
    credit,
    factor,
    fraction,
    parser,
    rate,
    registry,
    surcharge_tiers,
    taper,
)
from app.adapters.outbound.parameter_parsers.parser import ParameterParser

__all__ = [
    "ParameterParser",
    "amount",
    "brackets",
    "contribution_tier",
    "credit",
    "factor",
    "fraction",
    "parser",
    "rate",
    "registry",
    "surcharge_tiers",
    "taper",
]
