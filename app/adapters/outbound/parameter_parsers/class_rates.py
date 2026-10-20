"""Parses `class_rates` datasets: a mapping of class numbers to their rates, rules and factors
into ClassRates."""

from __future__ import annotations

from app.adapters.outbound.parameter_parsers.fraction import FractionParser
from app.adapters.outbound.parameter_parsers.registry import parameter_parser
from app.adapters.outbound.yaml_support import YamlNode
from app.domain.errors import DomainError, InvalidClassRatesError
from app.domain.parameters.class_rates import (
    CLASS_RATES,
    ClassRate,
    ClassRates,
    HalfYearRule,
    RecaptureAndTerminalLoss,
)
from app.domain.parameters.rate import Rate

_CLASS_KEYS = frozenset(
    {"rate", "half_year_rule", "recapture_and_terminal_loss", "aiip_factor", "riip_factor"}
)
# Each factor is read as a `fraction` dataset's body is: the same keys, the same parts.
_FRACTIONS = FractionParser()


@parameter_parser
class ClassRatesParser:
    """Parser for `class_rates` datasets: `classes`, keyed by each class number as a quoted
    decimal, each a `rate`, a `half_year_rule`, a `recapture_and_terminal_loss`, an `aiip_factor`
    and a `riip_factor`, each a quoted whole `numerator` and `denominator` read as a `fraction`
    dataset's are."""

    kind = CLASS_RATES
    body_keys = frozenset({"classes"})

    def parse(self, document: YamlNode) -> ClassRates:
        """Build ClassRates from the dataset's `classes`, in the file's order."""
        return ClassRates(
            tuple(self._class(key, entry) for key, entry in document.field("classes").fields())
        )

    def _class(self, key: str, entry: YamlNode) -> ClassRate:
        class_number = YamlNode(key, entry.where).parse_decimal()
        fields = entry.require_mapping(_CLASS_KEYS)
        rate = fields.field("rate").parse_decimal()
        half_year_rule = fields.field("half_year_rule").parse_choice(HalfYearRule)
        recapture_and_terminal_loss = fields.field("recapture_and_terminal_loss").parse_choice(
            RecaptureAndTerminalLoss
        )
        aiip_factor = fields.field("aiip_factor").require_mapping(_FRACTIONS.body_keys)
        riip_factor = fields.field("riip_factor").require_mapping(_FRACTIONS.body_keys)
        try:
            return ClassRate(
                class_number,
                Rate(rate),
                half_year_rule,
                recapture_and_terminal_loss,
                _FRACTIONS.parse(aiip_factor),
                _FRACTIONS.parse(riip_factor),
            )
        except DomainError as exc:
            # Name the class: the value objects do not know where in the table they sit.
            raise InvalidClassRatesError(f"{entry.where}: {exc}") from exc
