"""Parses `credit` datasets: an amount and a rate into a Credit."""

from __future__ import annotations

from app.adapters.outbound.parameter_parsers.registry import parameter_parser
from app.adapters.outbound.yaml_support import YamlNode
from app.domain.parameters.credit import CREDIT, Credit


@parameter_parser
class CreditParser:
    """Parser for `credit` datasets: an amount and the rate that turns it into tax relief."""

    kind = CREDIT
    body_keys = frozenset({"amount", "rate"})

    def parse(self, document: YamlNode) -> Credit:
        """Build a Credit from the dataset's `amount` and `rate` (both quoted decimals)."""
        return Credit(
            amount=document.field("amount").parse_decimal(),
            rate=document.field("rate").parse_decimal(),
        )
