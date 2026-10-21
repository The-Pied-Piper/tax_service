"""ForeignNonBusinessTaxCredit: the federal non-business foreign tax credit, T2209 lines 1 to 3.

Form T2209, "Federal non-business foreign tax credit": line 1 "Non-business income tax paid to a
foreign country (1) 43100"; line 2 "Net foreign non-business income (2) 43300" "× Basic federal tax
(4) = 2" over "Net income (3)"; line 3 "Enter whichever is less: the amount from line 1 or line 2."
Note (2): "If your net foreign non-business income is more than your net income, use your net income
in the calculation." "If you paid tax to more than one foreign country, and the total foreign taxes
paid to all foreign countries was more than $200, do the applicable calculation shown on this form
... to each country on a separate sheet in Canadian dollars. Enter the total amount on this form."

Each country is a record of the consumed `countries` list, holding lines 1 and the income of line
2; `net_income` and `basic_federal_tax` are the return-wide figures of notes (3) and (4). With more
than one country and a total tax paid above the `pooling_threshold` dataset's amount (the printed
$200), each country is worked on its own: its income is capped at net income, line 2 is the income
times basic federal tax over net income, worked by `ApplyRatio.ratio_of` and rounded once with the
`rounding` dataset's rule, line 3 is the lesser of line 1 and line 2, and the output is the sum of
the countries' line 3, 0 when there are no countries. Otherwise one pooled calculation is worked
on the totals (tax paid summed, income summed then capped at net income). A zero net income with
at least one country is refused with a ValidationError. It records one `ForeignTaxCreditLine` for
each country, by position from 1, then an `ItemsTotalLine`; the pooled case records one
`PooledForeignTaxCreditLine` alone.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, ClassVar

from app.domain.artifact import Artifact, ArtifactKind, Money
from app.domain.capabilities.apply_ratio import ApplyRatio
from app.domain.capability import Capability, CapabilityResult, capability
from app.domain.errors import ValidationError
from app.domain.parameters.amount import AMOUNT, Amount
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.domain.record_list import RecordList
from app.domain.trace import ItemsTotalLine
from app.jurisdictions.ca.catalog import (
    FOREIGN_NON_BUSINESS_TAX_PAID,
    NET_FOREIGN_NON_BUSINESS_INCOME,
)
from app.jurisdictions.ca.trace import ForeignTaxCreditLine, PooledForeignTaxCreditLine


@capability(identifier="foreign_non_business_tax_credit")
class ForeignNonBusinessTaxCredit(Capability):
    """Produces `total`: the lesser of tax paid and its share of basic federal tax, for each
    consumed country (or all of them pooled), added."""

    PARAMETERS: ClassVar[Mapping[str, ParameterKind[Any]]] = {
        "rounding": ROUNDING_ONLY,
        "pooling_threshold": AMOUNT,
    }
    CONSUMES: ClassVar[Mapping[str, type]] = {
        "countries": RecordList,
        "net_income": Decimal,
        "basic_federal_tax": Decimal,
    }
    PRODUCES: ClassVar[Mapping[str, type]] = {"total": Decimal}

    def __init__(
        self,
        rounding: ParameterDataset[RoundingOnly],
        pooling_threshold: ParameterDataset[Amount],
        countries: ArtifactKind[RecordList],
        net_income: Money,
        basic_federal_tax: Money,
        total: Money,
    ) -> None:
        """Wire the capability: its rounding and pooling threshold datasets, the record list of
        countries and the two return-wide figures it reads, the kind produced."""
        super().__init__(
            countries=countries,
            net_income=net_income,
            basic_federal_tax=basic_federal_tax,
            total=total,
        )
        self._rounding = rounding
        self._pooling_threshold = pooling_threshold
        self._countries = countries
        self._net_income = net_income
        self._basic_federal_tax = basic_federal_tax
        self._total = total

    def compute(self, inputs: tuple[Artifact[Any], ...]) -> CapabilityResult:
        records = self._input(inputs, self._countries).value.records
        if not records:
            return CapabilityResult(
                outputs=(Artifact(self._total, Decimal(0)),),
                trace=(ItemsTotalLine(self._total, (), Decimal(0)),),
            )
        net_income = self._input(inputs, self._net_income).value
        basic_federal_tax = self._input(inputs, self._basic_federal_tax).value
        if net_income == 0:
            raise ValidationError(
                f"{self._net_income.identifier} is zero, so line 2 of Form T2209, which divides "
                "by it, is undefined"
            )
        rule = self._rounding.rounding
        threshold = self._pooling_threshold.values.value
        taxes = [Decimal(record[FOREIGN_NON_BUSINESS_TAX_PAID]) for record in records]
        incomes = [Decimal(record[NET_FOREIGN_NON_BUSINESS_INCOME]) for record in records]
        if len(records) == 1 or sum(taxes, Decimal(0)) <= threshold:
            tax_paid = sum(taxes, Decimal(0))
            income = min(sum(incomes, Decimal(0)), net_income)
            line_2 = ApplyRatio.ratio_of(income, basic_federal_tax, net_income, rule)
            result = min(tax_paid, line_2)
            return CapabilityResult(
                outputs=(Artifact(self._total, result),),
                trace=(
                    PooledForeignTaxCreditLine(
                        self._total,
                        len(records),
                        tax_paid,
                        income,
                        net_income,
                        basic_federal_tax,
                        threshold,
                        rule,
                        line_2,
                        result,
                    ),
                ),
            )
        lines: list[ForeignTaxCreditLine] = []
        for position, (tax_paid, country_income) in enumerate(
            zip(taxes, incomes, strict=True), start=1
        ):
            income = min(country_income, net_income)
            line_2 = ApplyRatio.ratio_of(income, basic_federal_tax, net_income, rule)
            lines.append(
                ForeignTaxCreditLine(
                    self._total,
                    position,
                    tax_paid,
                    income,
                    net_income,
                    basic_federal_tax,
                    rule,
                    line_2,
                    min(tax_paid, line_2),
                )
            )
        items = tuple((line.position, line.result) for line in lines)
        total = sum((amount for _position, amount in items), Decimal(0))
        return CapabilityResult(
            outputs=(Artifact(self._total, total),),
            trace=(*lines, ItemsTotalLine(self._total, items, total)),
        )
