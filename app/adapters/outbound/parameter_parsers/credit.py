"""Parses `credit` datasets: an amount and a rate into a Credit."""

from __future__ import annotations

from app.adapters.outbound.yaml_support import YamlNode
from app.domain.parameters.credit import CREDIT, Credit


class CreditParser:
    kind = CREDIT
    body_keys = frozenset({"amount", "rate"})

    def parse(self, document: YamlNode) -> Credit:
        return Credit(
            amount=document.field("amount").parse_decimal(),
            rate=document.field("rate").parse_decimal(),
        )
