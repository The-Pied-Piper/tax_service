"""Parses `surcharge_tiers` datasets: a list of {threshold, rate} into SurchargeTiers."""

from __future__ import annotations

from app.adapters.outbound.parameter_parsers.registry import parameter_parser
from app.adapters.outbound.yaml_support import YamlNode
from app.domain.errors import DomainError, InvalidSurchargeTiersError
from app.domain.parameters.rate import Rate
from app.domain.parameters.surcharge_tiers import SURCHARGE_TIERS, SurchargeTier, SurchargeTiers

_TIER_KEYS = frozenset({"threshold", "rate"})


@parameter_parser
class SurchargeTiersParser:
    """Parser for `surcharge_tiers` datasets: a list of thresholds and rates."""

    kind = SURCHARGE_TIERS
    body_keys = frozenset({"tiers"})

    def parse(self, document: YamlNode) -> SurchargeTiers:
        """Build SurchargeTiers from the dataset's `tiers` list of {threshold, rate} entries."""
        return SurchargeTiers(tuple(self._tier(entry) for entry in document.field("tiers").items()))

    @staticmethod
    def _tier(entry: YamlNode) -> SurchargeTier:
        fields = entry.require_mapping(_TIER_KEYS)
        threshold = fields.field("threshold").parse_decimal()
        rate = fields.field("rate").parse_decimal()
        try:
            return SurchargeTier(threshold=threshold, rate=Rate(rate))
        except DomainError as exc:
            # Name the tier: the value objects do not know where in the list they sit.
            raise InvalidSurchargeTiersError(f"{entry.where}: {exc}") from exc
