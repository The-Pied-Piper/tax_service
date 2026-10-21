"""DispositionRows: the rows of one Schedule 3 Part 3 property type, added into one line.

The shared parent of `DispositionGains`, `DispositionGainsOnly` and `DispositionProceeds`, not
registered itself. Each row of the consumed record list is a disposition with the form's column 2
"Proceeds of disposition", column 3 "Adjusted cost base" and column 4 "Outlays and expenses"; column
5 "Gain or loss (column 2 minus columns 3 and 4)" is worked out here, exactly and signed. A subclass
says which trace line a row records and what the row adds to the total. The total is 0 when there
are no rows. It records one trace line for each row, by position from 1, then an
`ItemsTotalLine`.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import Capability, CapabilityResult
from app.domain.record_list import RecordList
from app.domain.trace import ItemsTotalLine, TraceLine
from app.jurisdictions.ca.catalog import (
    DISPOSITION_ADJUSTED_COST_BASE,
    DISPOSITION_OUTLAYS,
    DISPOSITION_PROCEEDS,
)


class DispositionRows(Capability):
    """Produces `output`: the total, over the consumed `dispositions`, of what each row adds."""

    CONSUMES: ClassVar[Mapping[str, type]] = {"dispositions": RecordList}
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": Decimal}

    def __init__(self, dispositions: ArtifactKind[RecordList], output: Money) -> None:
        """Wire the capability: the record list it reads, the kind produced."""
        super().__init__(dispositions=dispositions, output=output)
        self._dispositions = dispositions
        self._output = output

    def _row(
        self, position: int, proceeds: Decimal, cost_base: Decimal, outlays: Decimal
    ) -> tuple[TraceLine, Decimal]:
        """The trace line of one row and the figure the row adds to the total, as the subclass
        says."""
        raise NotImplementedError

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        records = self._input(inputs, self._dispositions).value.records
        lines: list[TraceLine] = []
        items: list[tuple[int, Decimal]] = []
        for position, record in enumerate(records, start=1):
            line, added = self._row(
                position,
                Decimal(record[DISPOSITION_PROCEEDS]),
                Decimal(record[DISPOSITION_ADJUSTED_COST_BASE]),
                Decimal(record[DISPOSITION_OUTLAYS]),
            )
            lines.append(line)
            items.append((position, added))
        total = sum((amount for _position, amount in items), Decimal(0))
        return CapabilityResult(
            outputs=(Artifact(self._output, total),),
            trace=(*lines, ItemsTotalLine(self._output, tuple(items), total)),
        )
