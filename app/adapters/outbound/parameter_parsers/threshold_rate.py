"""Parses `threshold_rate` datasets: a threshold and a rate."""

from __future__ import annotations

from app.adapters.outbound.parameter_parsers.registry import parameter_parser
from app.adapters.outbound.yaml_support import YamlNode
from app.domain.parameters.rate import Rate
from app.domain.parameters.threshold_rate import THRESHOLD_RATE, ThresholdRate


@parameter_parser
class ThresholdRateParser:
    """Parser for `threshold_rate` datasets: `rate` and `threshold`."""

    kind = THRESHOLD_RATE
    body_keys = frozenset({"rate", "threshold"})

    def parse(self, document: YamlNode) -> ThresholdRate:
        """Build a ThresholdRate from the dataset's quoted decimals `rate` and `threshold`."""
        return ThresholdRate(
            Rate(document.field("rate").parse_decimal()),
            document.field("threshold").parse_decimal(),
        )
