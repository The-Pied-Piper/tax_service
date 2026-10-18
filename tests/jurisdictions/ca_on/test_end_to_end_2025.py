"""CA-ON 2025, end to end: CRA's worked example computed from the manifest through the service.

The service is the one the composition root builds (`build_tax_computation`): the real YAML
sources over the jurisdiction packages and the shared registries. Return A's amounts (employment
income 110000 and a capital gain of 20000 to total income 120000, less an RRSP deduction of 1926,
union dues of 2000 and enhanced CPP contributions of 1074.00 to net income 115000, less no
deductions from net income to taxable income 115000, and from each basic personal amount (16129
federal, 12747 Ontario) plus the base CPP contributions of 3356.10 and the EI premiums of 1077.48
through each total of credit amounts to each tax after credits) are checked from the files under
`returns/` by `test_worked_returns.py`, as are Returns C and D; this module pins which capability
produces each line, the order, and the trace that explains them.
"""

from __future__ import annotations

from decimal import Decimal

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import Artifact
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.non_refundable_credit import NonRefundableCredit
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.parameters.credit import Credit
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import NO_ROUNDING
from app.domain.trace import (
    CreditAmountLine,
    CreditAppliedLine,
    CreditLine,
    RateAppliedLine,
    RoundedTotalLine,
    SubtractedNotBelowZeroLine,
    SumLine,
)
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    BASIC_PERSONAL_AMOUNT,
    CAPITAL_GAIN,
    CPP_BASE_CONTRIBUTIONS,
    CPP_ENHANCED_CONTRIBUTIONS,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    EI_PREMIUMS,
    EMPLOYMENT_INCOME,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    NET_INCOME,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    RRSP_DEDUCTION,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    UNION_DUES,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import ONTARIO_BASIC_TAX, ONTARIO_TAX_AFTER_CREDITS
from app.main import build_tax_computation

D = Decimal
CA_ON = JurisdictionCode("CA-ON")


def service() -> TaxComputationService:
    return build_tax_computation()


def compute(
    employment_income: str,
    capital_gain: str,
    rrsp_deduction: str,
    union_dues: str,
    cpp_base_contributions: str,
    cpp_enhanced_contributions: str,
    ei_premiums: str,
) -> Worksheet:
    return service().compute(
        CA_ON,
        2025,
        Artifact(EMPLOYMENT_INCOME, D(employment_income)),
        Artifact(CAPITAL_GAIN, D(capital_gain)),
        Artifact(RRSP_DEDUCTION, D(rrsp_deduction)),
        Artifact(UNION_DUES, D(union_dues)),
        Artifact(CPP_BASE_CONTRIBUTIONS, D(cpp_base_contributions)),
        Artifact(CPP_ENHANCED_CONTRIBUTIONS, D(cpp_enhanced_contributions)),
        Artifact(EI_PREMIUMS, D(ei_premiums)),
    )


def return_a() -> Worksheet:
    """Return A's inputs, as in `returns/2025_return_a.yaml`."""
    return compute("110000", "20000", "1926", "2000", "3356.10", "1074.00", "1077.48")


def test_each_amount_is_produced_by_its_capability() -> None:
    worksheet = return_a()

    assert worksheet.producer_of(EMPLOYMENT_INCOME) is None
    assert worksheet.producer_of(CAPITAL_GAIN) is None
    assert worksheet.producer_of(RRSP_DEDUCTION) is None
    assert worksheet.producer_of(UNION_DUES) is None
    assert worksheet.producer_of(CPP_BASE_CONTRIBUTIONS) is None
    assert worksheet.producer_of(CPP_ENHANCED_CONTRIBUTIONS) is None
    assert worksheet.producer_of(EI_PREMIUMS) is None
    assert isinstance(worksheet.producer_of(TAXABLE_CAPITAL_GAINS), ApplyRate)
    assert isinstance(worksheet.producer_of(TOTAL_INCOME), Sum)
    assert isinstance(worksheet.producer_of(DEDUCTIONS_FROM_TOTAL_INCOME), Sum)
    assert isinstance(worksheet.producer_of(NET_INCOME), SubtractNotBelowZero)
    assert worksheet.producer_of(TOTAL_INCOME) is not worksheet.producer_of(
        DEDUCTIONS_FROM_TOTAL_INCOME
    )
    assert isinstance(worksheet.producer_of(DEDUCTIONS_FROM_NET_INCOME), Sum)
    assert isinstance(worksheet.producer_of(TAXABLE_INCOME), SubtractNotBelowZero)
    assert worksheet.producer_of(TAXABLE_INCOME) is not worksheet.producer_of(NET_INCOME)
    assert worksheet.producer_of(DEDUCTIONS_FROM_NET_INCOME) is not worksheet.producer_of(
        TOTAL_INCOME
    )
    assert worksheet.producer_of(DEDUCTIONS_FROM_NET_INCOME) is not worksheet.producer_of(
        DEDUCTIONS_FROM_TOTAL_INCOME
    )
    assert isinstance(worksheet.producer_of(FEDERAL_BASIC_TAX), ProgressiveTax)
    assert isinstance(worksheet.producer_of(ONTARIO_BASIC_TAX), ProgressiveTax)
    assert worksheet.producer_of(FEDERAL_BASIC_TAX) is not worksheet.producer_of(ONTARIO_BASIC_TAX)
    assert isinstance(worksheet.producer_of(BASIC_PERSONAL_AMOUNT), CreditAmount)
    assert isinstance(worksheet.producer_of(ontario.BASIC_PERSONAL_AMOUNT), CreditAmount)
    assert worksheet.producer_of(BASIC_PERSONAL_AMOUNT) is not worksheet.producer_of(
        ontario.BASIC_PERSONAL_AMOUNT
    )
    assert isinstance(worksheet.producer_of(NON_REFUNDABLE_CREDIT_AMOUNTS), Sum)
    assert isinstance(worksheet.producer_of(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS), Sum)
    assert worksheet.producer_of(NON_REFUNDABLE_CREDIT_AMOUNTS) is not worksheet.producer_of(
        ontario.NON_REFUNDABLE_CREDIT_AMOUNTS
    )
    assert isinstance(worksheet.producer_of(FEDERAL_TAX_AFTER_CREDITS), NonRefundableCredit)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_CREDITS), NonRefundableCredit)
    assert worksheet.producer_of(FEDERAL_TAX_AFTER_CREDITS) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_CREDITS
    )


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
    deductions = position(
        "deductions_from_total_income: rrsp_deduction 1926 + union_dues 2000 "
        "+ cpp_enhanced_contributions 1074.00 = 5000.00",
        "5000",
    )
    net = position(
        "net_income: total_income 120000.0 less deductions_from_total_income 5000.00, "
        "not below 0 = 115000.00",
        "115000",
    )
    net_deductions = position("deductions_from_net_income: no parts = 0", "0")
    taxable = position(
        "taxable_income: net_income 115000.00 less deductions_from_net_income 0, "
        "not below 0 = 115000.00",
        "115000",
    )
    federal_basic = position(
        "federal_basic_tax on taxable_income 115000.00 (no rounding)", "20146.25"
    )
    federal_amount = position("basic_personal_amount: credit amount 16129 (no rounding)", "16129")
    federal_amounts = position(
        "non_refundable_credit_amounts: basic_personal_amount 16129 "
        "+ cpp_base_contributions 3356.10 + ei_premiums 1077.48 = 20562.58",
        "20562.58",
    )
    federal_credit = position(
        "credit: 14.5% of non_refundable_credit_amounts 20562.58 (no rounding)", "2981.5741"
    )
    federal_after = position(
        "federal_tax_after_credits: federal_basic_tax 20146.2500 less credit, not below 0",
        "17164.6759",
    )
    ontario_basic = position(
        "ontario_basic_tax on taxable_income 115000.00 (no rounding)", "8539.5965"
    )
    ontario_amount = position("basic_personal_amount: credit amount 12747 (no rounding)", "12747")
    ontario_amounts = position(
        "non_refundable_credit_amounts: basic_personal_amount 12747 "
        "+ cpp_base_contributions 3356.10 + ei_premiums 1077.48 = 17180.58",
        "17180.58",
    )
    ontario_credit = position(
        "credit: 5.05% of non_refundable_credit_amounts 17180.58 (no rounding)", "867.61929"
    )
    ontario_after = position(
        "ontario_tax_after_credits: ontario_basic_tax 8539.596500 less credit, not below 0",
        "7671.97721",
    )
    assert taxable_gains < total < net
    assert deductions < net
    assert net < taxable
    assert net_deductions < taxable
    assert taxable < federal_basic < federal_after
    assert taxable < ontario_basic
    assert ontario_basic < ontario_after
    assert federal_amount < federal_amounts < federal_credit < federal_after
    assert ontario_amount < ontario_amounts < ontario_credit < ontario_after


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    trace = return_a().trace

    rated = {line.output: line for line in trace if isinstance(line, RateAppliedLine)}
    sums = {line.output: line for line in trace if isinstance(line, SumLine)}
    floored = {line.output: line for line in trace if isinstance(line, SubtractedNotBelowZeroLine)}
    totals = {line.output: line for line in trace if isinstance(line, RoundedTotalLine)}
    amounts = {line.output: line for line in trace if isinstance(line, CreditAmountLine)}
    credits = {line.amounts: line for line in trace if isinstance(line, CreditLine)}
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
            DEDUCTIONS_FROM_TOTAL_INCOME,
            (
                (RRSP_DEDUCTION, D("1926")),
                (UNION_DUES, D("2000")),
                (CPP_ENHANCED_CONTRIBUTIONS, D("1074.00")),
            ),
            D("5000"),
        ),
        DEDUCTIONS_FROM_NET_INCOME: SumLine(DEDUCTIONS_FROM_NET_INCOME, (), D("0")),
        NON_REFUNDABLE_CREDIT_AMOUNTS: SumLine(
            NON_REFUNDABLE_CREDIT_AMOUNTS,
            (
                (BASIC_PERSONAL_AMOUNT, D("16129")),
                (CPP_BASE_CONTRIBUTIONS, D("3356.10")),
                (EI_PREMIUMS, D("1077.48")),
            ),
            D("20562.58"),
        ),
        # ON428 lines 58240 and 58300 read the federal amounts (lines 30800 and 31200).
        ontario.NON_REFUNDABLE_CREDIT_AMOUNTS: SumLine(
            ontario.NON_REFUNDABLE_CREDIT_AMOUNTS,
            (
                (ontario.BASIC_PERSONAL_AMOUNT, D("12747")),
                (CPP_BASE_CONTRIBUTIONS, D("3356.10")),
                (EI_PREMIUMS, D("1077.48")),
            ),
            D("17180.58"),
        ),
    }
    assert amounts == {
        BASIC_PERSONAL_AMOUNT: CreditAmountLine(
            BASIC_PERSONAL_AMOUNT, Credit(amount=D("16129")), NO_ROUNDING, D("16129")
        ),
        ontario.BASIC_PERSONAL_AMOUNT: CreditAmountLine(
            ontario.BASIC_PERSONAL_AMOUNT, Credit(amount=D("12747")), NO_ROUNDING, D("12747")
        ),
    }
    # The rate is applied once, to each form's total of credit amounts.
    assert credits == {
        NON_REFUNDABLE_CREDIT_AMOUNTS: CreditLine(
            NON_REFUNDABLE_CREDIT_AMOUNTS,
            D("20562.58"),
            Rate(D("0.145")),
            NO_ROUNDING,
            D("2981.5741"),
        ),
        ontario.NON_REFUNDABLE_CREDIT_AMOUNTS: CreditLine(
            ontario.NON_REFUNDABLE_CREDIT_AMOUNTS,
            D("17180.58"),
            Rate(D("0.0505")),
            NO_ROUNDING,
            D("867.61929"),
        ),
    }
    assert floored == {
        NET_INCOME: SubtractedNotBelowZeroLine(
            output=NET_INCOME,
            minuend=TOTAL_INCOME,
            minuend_amount=D("120000"),
            subtrahend=DEDUCTIONS_FROM_TOTAL_INCOME,
            subtrahend_amount=D("5000"),
            result=D("115000"),
        ),
        TAXABLE_INCOME: SubtractedNotBelowZeroLine(
            output=TAXABLE_INCOME,
            minuend=NET_INCOME,
            minuend_amount=D("115000"),
            subtrahend=DEDUCTIONS_FROM_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("115000"),
        ),
    }

    assert totals[FEDERAL_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[FEDERAL_BASIC_TAX].base_amount == D("115000")
    assert totals[FEDERAL_BASIC_TAX].amount == D("20146.25")
    assert totals[ONTARIO_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[ONTARIO_BASIC_TAX].amount == D("8539.5965")
    assert applied[FEDERAL_TAX_AFTER_CREDITS].tax == FEDERAL_BASIC_TAX
    assert applied[FEDERAL_TAX_AFTER_CREDITS].tax_amount == D("20146.25")
    assert applied[FEDERAL_TAX_AFTER_CREDITS].amount == D("17164.6759")
    assert applied[ONTARIO_TAX_AFTER_CREDITS].tax == ONTARIO_BASIC_TAX
    assert applied[ONTARIO_TAX_AFTER_CREDITS].tax_amount == D("8539.5965")
    assert applied[ONTARIO_TAX_AFTER_CREDITS].amount == D("7671.97721")


def test_each_capability_runs_after_what_it_consumes() -> None:
    order = service().compose(CA_ON, 2025).order

    assert len(order) == 14
    position = {kind: i for i, capability in enumerate(order) for kind in capability.produces}
    assert position[TAXABLE_CAPITAL_GAINS] < position[TOTAL_INCOME] < position[NET_INCOME]
    assert position[DEDUCTIONS_FROM_TOTAL_INCOME] < position[NET_INCOME]
    assert position[NET_INCOME] < position[TAXABLE_INCOME]
    assert position[DEDUCTIONS_FROM_NET_INCOME] < position[TAXABLE_INCOME]
    assert position[TAXABLE_INCOME] < position[FEDERAL_BASIC_TAX]
    assert position[TAXABLE_INCOME] < position[ONTARIO_BASIC_TAX]
    assert position[FEDERAL_BASIC_TAX] < position[FEDERAL_TAX_AFTER_CREDITS]
    assert position[ONTARIO_BASIC_TAX] < position[ONTARIO_TAX_AFTER_CREDITS]
    assert position[BASIC_PERSONAL_AMOUNT] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert position[NON_REFUNDABLE_CREDIT_AMOUNTS] < position[FEDERAL_TAX_AFTER_CREDITS]
    assert position[ontario.BASIC_PERSONAL_AMOUNT] < position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS] < position[ONTARIO_TAX_AFTER_CREDITS]


def test_a_credit_larger_than_the_tax_leaves_zero_not_a_refund() -> None:
    # Employment income of 10000, with CPP and EI from Schedule 8's and the EI table's
    # arithmetic: base 4.95% x (10000 - 3500) = 321.75, enhanced 1% x 6500 = 65.00,
    # EI 1.64% x 10000 = 164.00.
    worksheet = compute("10000", "0", "0", "0", "321.75", "65.00", "164.00")

    assert worksheet.get(TOTAL_INCOME).value == D("10000")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("65.00")
    assert worksheet.get(NET_INCOME).value == D("9935.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("9935.00")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("1440.575")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("16614.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("13232.75")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("0")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("0")
