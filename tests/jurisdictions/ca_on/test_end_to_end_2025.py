"""CA-ON 2025, end to end: CRA's worked example computed from the manifest through the service.

The service is the one the composition root builds (`build_tax_computation`): the real YAML
sources over the jurisdiction packages and the shared registries. Return A's amounts (employment
income 110000 and a capital gain of 20000 to total income 120000, less an RRSP deduction of 3000
to net income 117000; taxable income 115000 through each tax after credits) are checked from the
files under `returns/` by `test_worked_returns.py`; this module pins which capability produces
each line, the order, and the trace that explains them.
"""

from __future__ import annotations

from decimal import Decimal

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import Artifact
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.non_refundable_credit import NonRefundableCredit
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import NO_ROUNDING
from app.domain.trace import (
    CreditAppliedLine,
    RateAppliedLine,
    RoundedTotalLine,
    SubtractedNotBelowZeroLine,
    SumLine,
)
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    CAPITAL_GAIN,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    EMPLOYMENT_INCOME,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    NET_INCOME,
    RRSP_DEDUCTION,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
    TOTAL_INCOME,
)
from app.jurisdictions.ca_on.catalog import ONTARIO_BASIC_TAX, ONTARIO_TAX_AFTER_CREDITS
from app.main import build_tax_computation

D = Decimal
CA_ON = JurisdictionCode("CA-ON")


def service() -> TaxComputationService:
    return build_tax_computation()


def compute(
    employment_income: str, capital_gain: str, rrsp_deduction: str, taxable_income: str
) -> Worksheet:
    return service().compute(
        CA_ON,
        2025,
        Artifact(EMPLOYMENT_INCOME, D(employment_income)),
        Artifact(CAPITAL_GAIN, D(capital_gain)),
        Artifact(RRSP_DEDUCTION, D(rrsp_deduction)),
        Artifact(TAXABLE_INCOME, D(taxable_income)),
    )


def return_a() -> Worksheet:
    """Return A's inputs, as in `returns/2025_return_a.yaml`."""
    return compute("110000", "20000", "3000", "115000")


def test_each_amount_is_produced_by_its_capability() -> None:
    worksheet = return_a()

    assert worksheet.producer_of(EMPLOYMENT_INCOME) is None
    assert worksheet.producer_of(CAPITAL_GAIN) is None
    assert worksheet.producer_of(RRSP_DEDUCTION) is None
    assert worksheet.producer_of(TAXABLE_INCOME) is None
    assert isinstance(worksheet.producer_of(TAXABLE_CAPITAL_GAINS), ApplyRate)
    assert isinstance(worksheet.producer_of(TOTAL_INCOME), Sum)
    assert isinstance(worksheet.producer_of(DEDUCTIONS_FROM_TOTAL_INCOME), Sum)
    assert isinstance(worksheet.producer_of(NET_INCOME), SubtractNotBelowZero)
    assert worksheet.producer_of(TOTAL_INCOME) is not worksheet.producer_of(
        DEDUCTIONS_FROM_TOTAL_INCOME
    )
    assert isinstance(worksheet.producer_of(FEDERAL_BASIC_TAX), ProgressiveTax)
    assert isinstance(worksheet.producer_of(ONTARIO_BASIC_TAX), ProgressiveTax)
    assert isinstance(worksheet.producer_of(FEDERAL_TAX_AFTER_CREDITS), NonRefundableCredit)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_CREDITS), NonRefundableCredit)
    assert worksheet.producer_of(FEDERAL_BASIC_TAX) is not worksheet.producer_of(ONTARIO_BASIC_TAX)


def test_the_trace_explains_the_computation() -> None:
    worksheet = return_a()
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)

    def position(expected: str, amount: str) -> int:
        """The index of the one rendered line reading `expected` whose line has `amount`."""
        (found,) = [
            i
            for i, (text, line) in enumerate(zip(rendered, worksheet.trace, strict=True))
            if text == expected and line.amount == D(amount)
        ]
        return found

    taxable_gains = position(
        "taxable_capital_gains: 50% of capital_gain 20000 (no rounding)", "10000"
    )
    total = position(
        "total_income: employment_income 110000 + taxable_capital_gains 10000.0 = 120000.0",
        "120000",
    )
    deductions = position("deductions_from_total_income: rrsp_deduction 3000 = 3000", "3000")
    net = position(
        "net_income: total_income 120000.0 less deductions_from_total_income 3000, "
        "not below 0 = 117000.0",
        "117000",
    )
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
    assert taxable_gains < total < net
    assert deductions < net
    assert federal_basic < federal_after
    assert ontario_basic < ontario_after


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    trace = return_a().trace

    rated = {line.output: line for line in trace if isinstance(line, RateAppliedLine)}
    sums = {line.output: line for line in trace if isinstance(line, SumLine)}
    floored = {line.output: line for line in trace if isinstance(line, SubtractedNotBelowZeroLine)}
    totals = {line.output: line for line in trace if isinstance(line, RoundedTotalLine)}
    applied = {line.output: line for line in trace if isinstance(line, CreditAppliedLine)}

    assert rated == {
        TAXABLE_CAPITAL_GAINS: RateAppliedLine(
            TAXABLE_CAPITAL_GAINS, CAPITAL_GAIN, D("20000"), Rate(D("0.5")), NO_ROUNDING, D("10000")
        )
    }
    assert sums == {
        TOTAL_INCOME: SumLine(
            TOTAL_INCOME,
            ((EMPLOYMENT_INCOME, D("110000")), (TAXABLE_CAPITAL_GAINS, D("10000"))),
            D("120000"),
        ),
        DEDUCTIONS_FROM_TOTAL_INCOME: SumLine(
            DEDUCTIONS_FROM_TOTAL_INCOME, ((RRSP_DEDUCTION, D("3000")),), D("3000")
        ),
    }
    assert floored == {
        NET_INCOME: SubtractedNotBelowZeroLine(
            output=NET_INCOME,
            minuend=TOTAL_INCOME,
            minuend_amount=D("120000"),
            subtrahend=DEDUCTIONS_FROM_TOTAL_INCOME,
            subtrahend_amount=D("3000"),
            result=D("117000"),
        )
    }

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


def test_each_capability_runs_after_what_it_consumes() -> None:
    order = service().compose(CA_ON, 2025).order

    assert len(order) == 8
    position = {kind: i for i, capability in enumerate(order) for kind in capability.produces}
    assert position[TAXABLE_CAPITAL_GAINS] < position[TOTAL_INCOME] < position[NET_INCOME]
    assert position[DEDUCTIONS_FROM_TOTAL_INCOME] < position[NET_INCOME]
    assert position[FEDERAL_BASIC_TAX] < position[FEDERAL_TAX_AFTER_CREDITS]
    assert position[ONTARIO_BASIC_TAX] < position[ONTARIO_TAX_AFTER_CREDITS]


def test_a_credit_larger_than_the_tax_leaves_zero_not_a_refund() -> None:
    worksheet = compute("10000", "0", "0", "10000")

    assert worksheet.get(TOTAL_INCOME).value == D("10000")
    assert worksheet.get(NET_INCOME).value == D("10000")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("1450")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("0")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("0")


def test_deductions_larger_than_total_income_leave_zero_net_income() -> None:
    worksheet = compute("2000", "0", "3000", "0")

    assert worksheet.get(TOTAL_INCOME).value == D("2000")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("3000")
    assert worksheet.get(NET_INCOME).value == D("0")
