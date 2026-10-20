"""OntarioCaregiverAmount: the Ontario caregiver amount, one claim for each dependant.

For Worksheet ON428's "Line 58185 - Ontario caregiver amount", filled in for each dependant: the
`base` dataset's amount less that dependant's net income (a field of each record in the consumed
record list), from 0 up to the `maximum` dataset's amount (line 3), less the amount claimed for
that dependant on line 58160 (line 4), not below 0 (line 5). Line 4 is the consumed
`eligible_dependant_amount` for a dependant whose record says it is the one claimed there, and 0
for any other; the caller flags at most one dependant, and each one flagged takes the whole
`eligible_dependant_amount`. The output is the total of those allowable amounts, 0 when there are
no dependants. Each dependant is worked on its own, never pooled with the others, and its line 3
is rounded once, with the `maximum` dataset's rule, before line 4 is taken off and before the
total. It records one `CaregiverClaimLessClaimedLine` for each dependant, by position from 1, then
an `ItemsTotalLine`.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capability import Capability, CapabilityResult, capability
from app.domain.parameters.amount import AMOUNT, Amount
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.record_list import RecordList
from app.domain.trace import ItemsTotalLine
from app.jurisdictions.ca.catalog import DEPENDANT_NET_INCOME
from app.jurisdictions.ca_on.catalog import CLAIMED_AS_ELIGIBLE_DEPENDANT
from app.jurisdictions.ca_on.trace import CaregiverClaimLessClaimedLine


@capability(identifier="caregiver_amount")
class OntarioCaregiverAmount(Capability):
    """Produces `output`: the total, over the consumed `dependants`, of the `base` dataset's
    amount less each one's net income, from 0 up to the `maximum` dataset's amount, less the
    consumed `eligible_dependant_amount` for the one claimed on line 58160, not below 0."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Amount]]] = {"base": AMOUNT, "maximum": AMOUNT}
    CONSUMES: ClassVar[Mapping[str, type]] = {
        "dependants": RecordList,
        "eligible_dependant_amount": Decimal,
    }
    PRODUCES: ClassVar[Mapping[str, type]] = {"output": Decimal}

    def __init__(
        self,
        base: ParameterDataset[Amount],
        maximum: ParameterDataset[Amount],
        dependants: ArtifactKind[RecordList],
        eligible_dependant_amount: ArtifactKind[Decimal],
        output: Money,
    ) -> None:
        """Wire the capability: its base and maximum datasets, the record list and the amount it
        reads, the kind produced."""
        super().__init__(
            dependants=dependants,
            eligible_dependant_amount=eligible_dependant_amount,
            output=output,
        )
        self._base = base
        self._maximum = maximum
        self._dependants = dependants
        self._eligible_dependant_amount = eligible_dependant_amount
        self._output = output

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        records = self._input(inputs, self._dependants).value.records
        claimed_on_58160 = self._input(inputs, self._eligible_dependant_amount).value
        base, maximum = self._base.values, self._maximum.values
        rounding = self._maximum.rounding
        lines: list[CaregiverClaimLessClaimedLine] = []
        for position, record in enumerate(records, start=1):
            net_income = Decimal(record[DEPENDANT_NET_INCOME])
            lesser = min(max(Decimal(0), base.value - net_income), maximum.value)
            allowable = rounding.apply(lesser)
            claimed = claimed_on_58160 if record[CLAIMED_AS_ELIGIBLE_DEPENDANT] else Decimal(0)
            result = max(Decimal(0), allowable - claimed)
            lines.append(
                CaregiverClaimLessClaimedLine(
                    self._output,
                    position,
                    base,
                    net_income,
                    maximum,
                    allowable,
                    claimed,
                    rounding,
                    result,
                )
            )
        items = tuple((line.position, line.result) for line in lines)
        total = sum((amount for _position, amount in items), Decimal(0))
        return CapabilityResult(
            outputs=(Artifact(self._output, total),),
            trace=(*lines, ItemsTotalLine(self._output, items, total)),
        )
