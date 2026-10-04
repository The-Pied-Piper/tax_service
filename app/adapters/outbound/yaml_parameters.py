"""Reads parameter datasets from YAML files. Implements ParameterSource.

A dataset for family `ca-on/brackets` and tax year 2025 lives at
`<directory>/ca-on/brackets/2025.yaml` and must declare the same family and
year inside. An absent file is NotFoundError: a year is never carried forward.
Decimals are written as YAML strings ("0.145") so they never pass through float.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from app.adapters.outbound.yaml_support import YamlNode, YamlShapeError
from app.domain.errors import DomainError, InvalidParameterDataError, NotFoundError
from app.domain.parameters.brackets import Bracket, BracketSchedule
from app.domain.parameters.credit import Credit
from app.domain.parameters.datasets import BracketParameters, CreditParameters
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundingRule, RoundTo

_FAMILY = re.compile(r"[a-z0-9]+([_-][a-z0-9]+)*(/[a-z0-9]+([_-][a-z0-9]+)*)+")
_ENVELOPE_KEYS = frozenset({"family", "tax_year", "sources", "rounding"})
_BRACKET_KEYS = frozenset({"from", "rate"})
_ROUNDING_KEYS = frozenset({"increment", "mode"})


class YamlParameterSource:
    def __init__(self, directory: Path) -> None:
        self._directory = directory

    def get_brackets(self, family: str, tax_year: int) -> BracketParameters:
        path, doc = self._load(family, tax_year, frozenset({"brackets"}))
        try:
            return BracketParameters(
                family=family,
                tax_year=tax_year,
                schedule=BracketSchedule(
                    tuple(self._bracket(entry) for entry in doc.field("brackets").items())
                ),
                rounding=self._rounding(doc.field("rounding")),
                sources=self._sources(doc.field("sources")),
            )
        except (YamlShapeError, DomainError) as exc:
            raise InvalidParameterDataError(f"{path}: {exc}") from exc

    def get_credit(self, family: str, tax_year: int) -> CreditParameters:
        path, doc = self._load(family, tax_year, frozenset({"amount", "rate"}))
        try:
            return CreditParameters(
                family=family,
                tax_year=tax_year,
                credit=Credit(
                    amount=doc.field("amount").parse_decimal(),
                    rate=doc.field("rate").parse_decimal(),
                ),
                rounding=self._rounding(doc.field("rounding")),
                sources=self._sources(doc.field("sources")),
            )
        except (YamlShapeError, DomainError) as exc:
            raise InvalidParameterDataError(f"{path}: {exc}") from exc

    def _load(self, family: str, tax_year: int, body_keys: frozenset[str]) -> tuple[Path, YamlNode]:
        if not _FAMILY.fullmatch(family):
            raise ValueError(f"invalid parameter family {family!r}: expected e.g. 'ca-on/brackets'")
        path = self._directory / family / f"{tax_year}.yaml"
        if not path.is_file():
            raise NotFoundError(
                f"no {family} dataset for tax year {tax_year} (expected {path}); "
                "an absent year is never carried forward"
            )
        try:
            doc = YamlNode.load(path, "dataset").require_mapping(_ENVELOPE_KEYS | body_keys)
            declared_family = doc.field("family").require_string()
            declared_year = doc.field("tax_year").require_integer()
        except (OSError, yaml.YAMLError, YamlShapeError) as exc:
            raise InvalidParameterDataError(f"{path}: {exc}") from exc
        if declared_family != family:
            raise InvalidParameterDataError(
                f"{path}: family {declared_family!r} does not match {family!r}"
            )
        if declared_year != tax_year:
            raise InvalidParameterDataError(
                f"{path}: tax_year {declared_year} does not match {tax_year}"
            )
        return path, doc

    @staticmethod
    def _bracket(entry: YamlNode) -> Bracket:
        fields = entry.require_mapping(_BRACKET_KEYS)
        return Bracket(
            lower=fields.field("from").parse_decimal(),
            rate=fields.field("rate").parse_decimal(),
        )

    @staticmethod
    def _rounding(node: YamlNode) -> RoundingRule:
        if node.value == "none":
            return NO_ROUNDING
        if not isinstance(node.value, dict):
            raise YamlShapeError("rounding must be 'none' or a mapping of increment and mode")
        fields = node.require_mapping(_ROUNDING_KEYS)
        mode_name = fields.field("mode").require_string()
        modes = {mode.value: mode for mode in RoundingMode}
        if mode_name not in modes:
            raise YamlShapeError(f"rounding.mode {mode_name!r} is not one of {sorted(modes)}")
        return RoundTo(increment=fields.field("increment").parse_decimal(), mode=modes[mode_name])

    @staticmethod
    def _sources(node: YamlNode) -> tuple[str, ...]:
        entries = node.items()
        if not entries:
            raise YamlShapeError("sources must list at least one source")
        return tuple(entry.require_string() for entry in entries)
