"""Parses `brackets` datasets: a list of {from, rate, tax_at_start} into a BracketSchedule."""

from __future__ import annotations

from app.adapters.outbound.parameter_parsers.registry import parameter_parser
from app.adapters.outbound.yaml_support import YamlNode
from app.domain.parameters.brackets import BRACKETS, Bracket, BracketSchedule

_BRACKET_KEYS = frozenset({"from", "rate", "tax_at_start"})


@parameter_parser
class BracketsParser:
    """Parser for `brackets` datasets: a list of thresholds, rates and printed constants."""

    kind = BRACKETS
    body_keys = frozenset({"brackets"})

    def parse(self, document: YamlNode) -> BracketSchedule:
        """Build a BracketSchedule from the dataset's `brackets` list of entries."""
        return BracketSchedule(
            tuple(self._bracket(entry) for entry in document.field("brackets").items())
        )

    @staticmethod
    def _bracket(entry: YamlNode) -> Bracket:
        fields = entry.require_mapping(_BRACKET_KEYS)
        return Bracket(
            lower=fields.field("from").parse_decimal(),
            rate=fields.field("rate").parse_decimal(),
            tax_at_start=fields.field("tax_at_start").parse_decimal(),
        )
