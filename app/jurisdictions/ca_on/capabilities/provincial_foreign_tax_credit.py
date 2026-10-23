"""ProvincialForeignTaxCredit: the Ontario non-business foreign tax credit, T2036 lines 1 to 5.

Form T2036, "Provincial or Territorial Foreign Tax Credit": line 1 "Enter the amount from line 1 of
Form T2209."; line 2 "Enter the amount from line 3 of Form T2209, unless you have to pay minimum
tax.(1)"; line 3 "Line 1 minus line 2"; line 4 "Net foreign non-business income (2)" "×
Provincial or territorial tax otherwise payable (4)" over "Net income (3)"; line 5 "Enter
whichever amount is less: line 3 or line 4." "Provincial or territorial foreign tax credit".
"Enter the total from line 5 (for each country if applicable) on the line for the provincial or
territorial foreign tax credit of Form 428." Notes (2) and (3) take the net foreign non-business
income and the net income from line 2 of Form T2209.

Each sheet of Form T2209 is a record of the consumed `sheets` list, holding its line 1 (tax paid),
the income used on its line 2 and its line 3; `net_income` and `provincial_tax` are the
return-wide figures of notes (3) and (4). For each sheet, line 3 is line 1 less the sheet's line 3
of Form T2209, line 4 is the sheet's income times `provincial_tax` over `net_income`, worked by
`ApplyRatio.ratio_of` and rounded once with the `rounding` dataset's rule, line 5 is the lesser of
line 3 and line 4, and the output is the sum of the sheets' line 5, 0 when there are no sheets (net
income is then not read). A zero net income with at least one sheet is refused with a
ValidationError. It records one `ProvincialForeignTaxCreditLine` for each sheet, by position from
1, then an `ItemsTotalLine`. The minimum tax variant of line 2 is not wired.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capabilities.apply_ratio import ApplyRatio
from app.domain.capability import Capability, CapabilityResult, capability
from app.domain.errors import ValidationError
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.domain.record_list import RecordList
from app.domain.trace import ItemsTotalLine
from app.jurisdictions.ca.catalog import (
    FOREIGN_NON_BUSINESS_TAX_PAID,
    FOREIGN_TAX_CREDIT_SHEET_LINE_3,
    NET_FOREIGN_NON_BUSINESS_INCOME,
)
from app.jurisdictions.ca_on.trace import ProvincialForeignTaxCreditLine


@capability(identifier="provincial_foreign_tax_credit")
class ProvincialForeignTaxCredit(Capability):
    """Produces `total`: for each consumed sheet of Form T2209, the lesser of its tax paid less
    its federal credit and its share of `provincial_tax`, added."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Any]]] = {"rounding": ROUNDING_ONLY}
    CONSUMES: ClassVar[Mapping[str, type]] = {
        "sheets": RecordList,
        "net_income": Decimal,
        "provincial_tax": Decimal,
    }
    PRODUCES: ClassVar[Mapping[str, type]] = {"total": Decimal}

    def __init__(
        self,
        rounding: ParameterDataset[RoundingOnly],
        sheets: ArtifactKind[RecordList],
        net_income: Money,
        provincial_tax: Money,
        total: Money,
    ) -> None:
        """Wire the capability: its rounding dataset, the sheets and the two return-wide figures
        it reads, the kind produced."""
        super().__init__(
            sheets=sheets, net_income=net_income, provincial_tax=provincial_tax, total=total
        )
        self._rounding = rounding
        self._sheets = sheets
        self._net_income = net_income
        self._provincial_tax = provincial_tax
        self._total = total

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        records = self._input(inputs, self._sheets).value.records
        if not records:
            return CapabilityResult(
                outputs=(Artifact(self._total, Decimal(0)),),
                trace=(ItemsTotalLine(self._total, (), Decimal(0)),),
            )
        net_income = self._input(inputs, self._net_income).value
        provincial_tax = self._input(inputs, self._provincial_tax).value
        if net_income == 0:
            raise ValidationError(
                f"{self._net_income.identifier} is zero, so line 4 of Form T2036, which divides "
                "by it, is undefined"
            )
        rule = self._rounding.rounding
        lines: list[ProvincialForeignTaxCreditLine] = []
        for position, record in enumerate(records, start=1):
            tax_paid = Decimal(record[FOREIGN_NON_BUSINESS_TAX_PAID])
            income = Decimal(record[NET_FOREIGN_NON_BUSINESS_INCOME])
            federal_credit = Decimal(record[FOREIGN_TAX_CREDIT_SHEET_LINE_3])
            line_3 = tax_paid - federal_credit
            line_4 = ApplyRatio.ratio_of(income, provincial_tax, net_income, rule)
            lines.append(
                ProvincialForeignTaxCreditLine(
                    self._total,
                    position,
                    tax_paid,
                    federal_credit,
                    line_3,
                    income,
                    net_income,
                    provincial_tax,
                    rule,
                    line_4,
                    min(line_3, line_4),
                )
            )
        items = tuple((line.position, line.result) for line in lines)
        total = sum((amount for _position, amount in items), Decimal(0))
        return CapabilityResult(
            outputs=(Artifact(self._total, total),),
            trace=(*lines, ItemsTotalLine(self._total, items, total)),
        )
