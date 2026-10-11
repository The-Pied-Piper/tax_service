"""Parsers for the kind-specific part of YAML parameter datasets.

Each parser handles one parameter kind: the keys it adds to a dataset file and
how to turn them into that kind's values. Parsers register themselves with
`@parameter_parser`, and YamlParameterSource looks them up by kind in a
ParameterParserRegistry, so adding a kind means adding a parser and nothing else.
"""

from __future__ import annotations

from app.adapters.outbound.parameter_parsers.parser import ParameterParser

__all__ = ["ParameterParser"]
