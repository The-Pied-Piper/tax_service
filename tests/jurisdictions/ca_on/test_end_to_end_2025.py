"""CA-ON 2025, end to end: CRA's worked example computed from the manifest through the service.

The service is the one the composition root builds (`build_tax_computation`): the real YAML
sources over the jurisdiction packages and the shared registries. The example's amounts (taxable
income 115000 through each tax after credits) are checked from the files under `returns/`
by `test_worked_returns.py`; this module pins which capability produces each line, the order,
and the trace that explains them.
"""

from __future__ import annotations

from decimal import Decimal

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import Artifact
from app.domain.capabilities.non_refundable_credit import NonRefundableCredit
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.trace import CreditAppliedLine, RoundedTotalLine
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    TAXABLE_INCOME,
)
from app.jurisdictions.ca_on.catalog import ONTARIO_BASIC_TAX, ONTARIO_TAX_AFTER_CREDITS
from app.main import build_tax_computation

D = Decimal
CA_ON = JurisdictionCode("CA-ON")


def service() -> TaxComputationService:
    return build_tax_computation()


def compute(taxable_income: str) -> Worksheet:
    return service().compute(CA_ON, 2025, Artifact(TAXABLE_INCOME, D(taxable_income)))


def test_each_amount_is_produced_by_its_capability() -> None:
    worksheet = compute("115000")

    assert worksheet.producer_of(TAXABLE_INCOME) is None
    assert isinstance(worksheet.producer_of(FEDERAL_BASIC_TAX), ProgressiveTax)
    assert isinstance(worksheet.producer_of(ONTARIO_BASIC_TAX), ProgressiveTax)
    assert isinstance(worksheet.producer_of(FEDERAL_TAX_AFTER_CREDITS), NonRefundableCredit)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_CREDITS), NonRefundableCredit)
    assert worksheet.producer_of(FEDERAL_BASIC_TAX) is not worksheet.producer_of(ONTARIO_BASIC_TAX)


def test_the_trace_explains_the_computation() -> None:
    worksheet = compute("115000")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)

    def position(expected: str, amount: str) -> int:
        """The index of the one rendered line reading `expected` whose line has `amount`."""
        (found,) = [
            i
            for i, (text, line) in enumerate(zip(rendered, worksheet.trace, strict=True))
            if text == expected and line.amount == D(amount)
        ]
        return found

    federal_basic = position("federal_basic_tax on taxable_income 115000 (no rounding)", "20146.25")
    federal_after = position(
        "federal_tax_after_credits: federal_basic_tax 20146.250 less credit, not below 0",
        "17807.545",
    )
    ontario_basic = position(
        "ontario_basic_tax on taxable_income 115000 (no rounding)", "8539.5965"
    )
    ontario_after = position(
        "ontario_tax_after_credits: ontario_basic_tax 8539.5965 less credit, not below 0",
        "7895.873",
    )
    assert federal_basic < federal_after
    assert ontario_basic < ontario_after


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    trace = compute("115000").trace

    totals = {line.output: line for line in trace if isinstance(line, RoundedTotalLine)}
    applied = {line.output: line for line in trace if isinstance(line, CreditAppliedLine)}

    assert totals[FEDERAL_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[FEDERAL_BASIC_TAX].base_amount == D("115000")
    assert totals[FEDERAL_BASIC_TAX].amount == D("20146.25")
    assert totals[ONTARIO_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[ONTARIO_BASIC_TAX].amount == D("8539.5965")
    assert applied[FEDERAL_TAX_AFTER_CREDITS].tax == FEDERAL_BASIC_TAX
    assert applied[FEDERAL_TAX_AFTER_CREDITS].tax_amount == D("20146.25")
    assert applied[FEDERAL_TAX_AFTER_CREDITS].amount == D("17807.545")
    assert applied[ONTARIO_TAX_AFTER_CREDITS].tax == ONTARIO_BASIC_TAX
    assert applied[ONTARIO_TAX_AFTER_CREDITS].tax_amount == D("8539.5965")
    assert applied[ONTARIO_TAX_AFTER_CREDITS].amount == D("7895.873")


def test_each_progressive_tax_runs_before_its_credit() -> None:
    order = service().compose(CA_ON, 2025).order

    assert len(order) == 4
    position = {kind: i for i, capability in enumerate(order) for kind in capability.produces}
    assert position[FEDERAL_BASIC_TAX] < position[FEDERAL_TAX_AFTER_CREDITS]
    assert position[ONTARIO_BASIC_TAX] < position[ONTARIO_TAX_AFTER_CREDITS]


def test_a_credit_larger_than_the_tax_leaves_zero_not_a_refund() -> None:
    worksheet = compute("10000")

    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("1450")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("0")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("0")
