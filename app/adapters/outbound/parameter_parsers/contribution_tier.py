"""Parses `contribution_tier` datasets: a rate and three quoted decimals into a ContributionTier."""

from __future__ import annotations

from app.adapters.outbound.parameter_parsers.registry import parameter_parser
from app.adapters.outbound.yaml_support import YamlNode
from app.domain.parameters.contribution_tier import CONTRIBUTION_TIER, ContributionTier
from app.domain.parameters.rate import Rate


@parameter_parser
class ContributionTierParser:
    """Parser for `contribution_tier` datasets: a `rate`, `lower`, `upper` and `maximum`."""

    kind = CONTRIBUTION_TIER
    body_keys = frozenset({"rate", "lower", "upper", "maximum"})

    def parse(self, document: YamlNode) -> ContributionTier:
        """Build a ContributionTier from the dataset's four quoted decimals."""
        return ContributionTier(
            rate=Rate(document.field("rate").parse_decimal()),
            lower=document.field("lower").parse_decimal(),
            upper=document.field("upper").parse_decimal(),
            maximum=document.field("maximum").parse_decimal(),
        )
