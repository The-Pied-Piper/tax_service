"""Parses `amount` datasets: one quoted decimal into an Amount, which checks it is not negative."""

from __future__ import annotations

from app.adapters.outbound.parameter_parsers.registry import parameter_parser
from app.adapters.outbound.yaml_support import YamlNode
from app.domain.parameters.amount import AMOUNT, Amount


@parameter_parser
class AmountParser:
    """Parser for `amount` datasets: a single `amount`."""

    kind = AMOUNT
    body_keys = frozenset({"amount"})

    def parse(self, document: YamlNode) -> Amount:
        """Build an Amount from the dataset's `amount` (a quoted decimal)."""
        return Amount(document.field("amount").parse_decimal())
