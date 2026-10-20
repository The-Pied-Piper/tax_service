"""ShortTermRentalGrossRents: the gross rents for short-term rentals of the T776 properties, added.

Form T776 Part 3 lists the rental properties with "Number of units", "Gross rents for short-term
rentals" and "Gross rents for all units", and line 8140 is the "Total of your gross rents for
short-term rentals in the year you receive them (add amounts under "Gross rents for short-term
rentals")". This capability reads the record list of those properties and adds the "Gross rents
for short-term rentals" field of every record, exactly: it has no dataset, so it never rounds, and
an empty list totals zero. Each item is named by its position from 1 in the trace.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import Capability, CapabilityResult, capability
from app.domain.record_list import RecordList
from app.domain.trace import RecordTotalLine
from app.jurisdictions.ca.catalog import RENTAL_PROPERTY_SHORT_TERM_RENTS


@capability(identifier="short_term_rental_gross_rents")
class ShortTermRentalGrossRents(Capability):
    """Produces `output`: the short-term rents of every record of the consumed `properties`."""

    CONSUMES: ClassVar[Mapping[str, type]] = {"properties": RecordList}
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": Decimal}

    def __init__(self, properties: ArtifactKind[RecordList], output: Money) -> None:
        """Wire the capability: the record-list kind it reads and the kind it produces."""
        super().__init__(properties=properties, output=output)
        self._properties = properties
        self._output = output

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        amounts: list[Decimal] = []
        for record in self._input(inputs, self._properties).value.records:
            amount = record[RENTAL_PROPERTY_SHORT_TERM_RENTS]
            if not isinstance(amount, Decimal):
                raise TypeError(
                    f"{RENTAL_PROPERTY_SHORT_TERM_RENTS.identifier} must be a Decimal, "
                    f"got {type(amount).__name__}"
                )
            amounts.append(amount)
        total = sum(amounts, Decimal(0))
        return CapabilityResult(
            outputs=(Artifact(self._output, total),),
            trace=(
                RecordTotalLine(
                    output=self._output,
                    field=RENTAL_PROPERTY_SHORT_TERM_RENTS,
                    amounts=tuple(amounts),
                    total=total,
                ),
            ),
        )
