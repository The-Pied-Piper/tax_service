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
1, then an `ItemsTotalLine`.

Line 2 note (1), when "you have to pay minimum tax" (the consumed `minimum_tax_applies` count, Form
T691 Part 5 line 11 above 0, is 1): for a resident of Ontario at the end of the year, "If the total
non-business income taxes you paid to all foreign countries is $200 or less", line 1 of this form
divided by "the sum of line 1 of this form and the amount on line 8 of Part 4 of Form T691", times
"the special foreign tax credit on line 11 of Part 4 of Form T691"; "If the total non-business
income taxes you paid to all foreign countries is more than $200", for each country line 1 of that
country divided by "the total foreign taxes paid for 2025 (to get this total, add the amount on
line 7 of Part 4 of Form T691, Alternative Minimum Tax, divided by 66.6666% and the amount on line
8 of Part 4 of Form T691)", times the same line 11. The total of the sheets' line 1 is tested
against the `threshold` dataset (the $200); line 7 is the consumed `non_business_tax_paid`, line 8
`business_tax_paid`, line 11 `special_foreign_tax_credit`, and the 66.6666% the `rate` dataset. At
or under the threshold the sheets share the one form's line 2, each as its line 1 times line 11
over the total of line 1 plus line 8 (each sheet's line 2 rounded on its own, so the sheets add to
the form's line 2 to within a cent); over it each sheet is its line 1 times line 11 over line 7
divided by the rate plus line 8. Line 2 is worked as an exact fraction and rounded once with the
`rounding` dataset's rule; a zero divisor is refused with a ValidationError. With the count 0 line
2 is the sheet's line 3 of Form T2209.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from fractions import Fraction as ExactFraction
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capabilities.apply_ratio import ApplyRatio
from app.domain.capability import Capability, CapabilityResult, capability
from app.domain.errors import ValidationError
from app.domain.parameters.amount import AMOUNT, Amount
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rate import RATE, Rate
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
    its line 2 (its federal credit, or its share of the special foreign tax credit when minimum
    tax is payable) and its share of `provincial_tax`, added."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Any]]] = {
        "rounding": ROUNDING_ONLY,
        "threshold": AMOUNT,
        "rate": RATE,
    }
    CONSUMES: ClassVar[Mapping[str, type]] = {
        "minimum_tax_applies": int,
        "sheets": RecordList,
        "net_income": Decimal,
        "provincial_tax": Decimal,
        "non_business_tax_paid": Decimal,
        "business_tax_paid": Decimal,
        "special_foreign_tax_credit": Decimal,
    }
    PRODUCES: ClassVar[Mapping[str, type]] = {"total": Decimal}

    def __init__(
        self,
        rounding: ParameterDataset[RoundingOnly],
        threshold: ParameterDataset[Amount],
        rate: ParameterDataset[Rate],
        minimum_tax_applies: ArtifactKind[int],
        sheets: ArtifactKind[RecordList],
        net_income: Money,
        provincial_tax: Money,
        non_business_tax_paid: Money,
        business_tax_paid: Money,
        special_foreign_tax_credit: Money,
        total: Money,
    ) -> None:
        """Wire the capability: its rounding, threshold and rate datasets, the minimum tax count,
        the sheets and the return-wide figures it reads, the kind produced."""
        super().__init__(
            minimum_tax_applies=minimum_tax_applies,
            sheets=sheets,
            net_income=net_income,
            provincial_tax=provincial_tax,
            non_business_tax_paid=non_business_tax_paid,
            business_tax_paid=business_tax_paid,
            special_foreign_tax_credit=special_foreign_tax_credit,
            total=total,
        )
        self._rounding = rounding
        self._threshold = threshold
        self._rate = rate
        self._minimum_tax_applies = minimum_tax_applies
        self._non_business_tax_paid = non_business_tax_paid
        self._business_tax_paid = business_tax_paid
        self._special_foreign_tax_credit = special_foreign_tax_credit
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
        minimum_tax = self._input(inputs, self._minimum_tax_applies).value == 1
        line_7 = self._input(inputs, self._non_business_tax_paid).value
        business_tax = self._input(inputs, self._business_tax_paid).value
        line_11 = self._input(inputs, self._special_foreign_tax_credit).value
        divisor: ExactFraction | None = None
        separate_sheet = False
        special_credit: Decimal | None = None
        if minimum_tax:
            special_credit = line_11
            total_tax_paid = sum(
                (Decimal(record[FOREIGN_NON_BUSINESS_TAX_PAID]) for record in records), Decimal(0)
            )
            separate_sheet = total_tax_paid > self._threshold.values.value
            if separate_sheet:
                divisor = ExactFraction(line_7) / ExactFraction(
                    self._rate.values.value
                ) + ExactFraction(business_tax)
            else:
                divisor = ExactFraction(total_tax_paid) + ExactFraction(business_tax)
            if divisor == 0:
                raise ValidationError(
                    "the total of tax paid plus the business tax is zero, so line 2 of Form "
                    "T2036, which divides by it, is undefined"
                )
        lines: list[ProvincialForeignTaxCreditLine] = []
        for position, record in enumerate(records, start=1):
            tax_paid = Decimal(record[FOREIGN_NON_BUSINESS_TAX_PAID])
            income = Decimal(record[NET_FOREIGN_NON_BUSINESS_INCOME])
            if divisor is not None and special_credit is not None:
                federal_credit = rule.apply(
                    ExactFraction(tax_paid) * ExactFraction(special_credit) / divisor
                )
            else:
                federal_credit = Decimal(record[FOREIGN_TAX_CREDIT_SHEET_LINE_3])
            if federal_credit > tax_paid:
                raise ValidationError(
                    f"line 2 of Form T2036, {federal_credit}, is more than the {tax_paid} of its "
                    "line 1, so line 3 would be negative; the amounts on lines 7, 8 and 11 of "
                    "Part 4 of Form T691 do not fit the tax paid on the sheets"
                )
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
                    special_credit,
                    divisor,
                    separate_sheet,
                )
            )
        items = tuple((line.position, line.result) for line in lines)
        total = sum((amount for _position, amount in items), Decimal(0))
        return CapabilityResult(
            outputs=(Artifact(self._total, total),),
            trace=(*lines, ItemsTotalLine(self._total, items, total)),
        )
