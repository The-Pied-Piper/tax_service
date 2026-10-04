"""Parsers for the kind-specific part of YAML parameter datasets.

Each parser handles one parameter kind: the keys it adds to a dataset file and
how to turn them into that kind's values. YamlParameterSource looks parsers up
by kind, so adding a kind means adding a parser here and nothing else.
"""

from __future__ import annotations

from typing import Any, Protocol

from app.adapters.outbound.parameter_parsers.brackets import BracketsParser
from app.adapters.outbound.parameter_parsers.credit import CreditParser
from app.adapters.outbound.yaml_support import YamlNode
from app.domain.parameters.kind import ParameterKind


class ParameterParser[T](Protocol):
    @property
    def kind(self) -> ParameterKind[T]: ...

    @property
    def body_keys(self) -> frozenset[str]:
        """The keys this kind adds to a dataset file, beyond the shared ones."""
        ...

    def parse(self, document: YamlNode) -> T: ...


DEFAULT_PARSERS: tuple[ParameterParser[Any], ...] = (BracketsParser(), CreditParser())
