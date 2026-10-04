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

from app.adapters.outbound import yaml_support as y
from app.adapters.outbound.yaml_support import YamlShapeError
from app.domain.errors import DomainError, InvalidParameterDataError, NotFoundError
from app.domain.parameters.brackets import Bracket, BracketSchedule
from app.domain.parameters.datasets import BracketParameters
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
            entries = y.sequence(doc["brackets"], "brackets")
            schedule = BracketSchedule(
                tuple(self._bracket(entry, f"brackets[{i}]") for i, entry in enumerate(entries))
            )
            return BracketParameters(
                family=family,
                tax_year=tax_year,
                schedule=schedule,
                rounding=self._rounding(doc["rounding"]),
                sources=self._sources(doc["sources"]),
            )
        except (YamlShapeError, DomainError) as exc:
            raise InvalidParameterDataError(f"{path}: {exc}") from exc

    def _load(
        self, family: str, tax_year: int, body_keys: frozenset[str]
    ) -> tuple[Path, dict[str, object]]:
        if not _FAMILY.fullmatch(family):
            raise ValueError(f"invalid parameter family {family!r}: expected e.g. 'ca-on/brackets'")
        path = self._directory / family / f"{tax_year}.yaml"
        if not path.is_file():
            raise NotFoundError(
                f"no {family} dataset for tax year {tax_year} (expected {path}); "
                "an absent year is never carried forward"
            )
        try:
            doc = y.mapping(y.load(path), "dataset", _ENVELOPE_KEYS | body_keys)
            declared_family = y.string(doc["family"], "family")
            declared_year = y.integer(doc["tax_year"], "tax_year")
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
    def _bracket(entry: object, where: str) -> Bracket:
        fields = y.mapping(entry, where, _BRACKET_KEYS)
        return Bracket(
            lower=y.decimal(fields["from"], f"{where}.from"),
            rate=y.decimal(fields["rate"], f"{where}.rate"),
        )

    @staticmethod
    def _rounding(value: object) -> RoundingRule:
        if value == "none":
            return NO_ROUNDING
        if not isinstance(value, dict):
            raise YamlShapeError("rounding must be 'none' or a mapping of increment and mode")
        fields = y.mapping(value, "rounding", _ROUNDING_KEYS)
        mode_name = y.string(fields["mode"], "rounding.mode")
        modes = {mode.value: mode for mode in RoundingMode}
        if mode_name not in modes:
            raise YamlShapeError(f"rounding.mode {mode_name!r} is not one of {sorted(modes)}")
        return RoundTo(
            increment=y.decimal(fields["increment"], "rounding.increment"),
            mode=modes[mode_name],
        )

    @staticmethod
    def _sources(value: object) -> tuple[str, ...]:
        entries = y.sequence(value, "sources")
        if not entries:
            raise YamlShapeError("sources must list at least one source")
        return tuple(y.string(entry, f"sources[{i}]") for i, entry in enumerate(entries))
