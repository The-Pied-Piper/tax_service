"""CA-ON 2025, end to end: CRA's worked example computed from the manifest through the service.

The service is the one the composition root builds (`build_tax_computation`): the real YAML sources
over the jurisdiction packages and the shared registries. Return A's amounts (employment income
110000 and a capital gain of 20000 to total income 120000; the CPP contributions computed from
employment income by Schedule 8's tiers, each at its maximum: base 3356.10, first additional 678.00
and second additional 396.00, the enhanced contributions 1074.00; the EI premiums computed from
employment income, at the maximum 1077.48; the RRSP contributions available to deduct of 1926, no
unused contributions plus the contributions of 1926 (Schedule 7 line 10), the most that may be
deducted, 1926, the lesser of them and the deduction limit of 19800 (Schedule 7 line 17), the amount
deducted of 1926 (line 18), at most that, as the RRSP deduction (line 20), and the unused
contributions carried forward of 0 (line 23), the contributions available less the deduction; less
that RRSP deduction, union dues of 2000 and the enhanced contributions to net income 115000, less no
deductions from net income to taxable income 115000, and from each basic personal amount (16129
federal, the Federal Worksheet's taper on net income, here at or below the 177882 threshold so not
reduced; 12747 Ontario) plus the base CPP contributions and the EI premiums, and federally the
Canada employment amount of 1471 (the lesser of employment income and 1471), through each total of
credit amounts and each form's non-refundable tax credits (T1 line 35000, ON428 line 61500) to each
tax after credits, the Ontario surtax on the Ontario tax after credits (ON428 lines 66 to 68) to the
Ontario tax with surtax of line 69, and with no dependent children and no dependants the Ontario tax
reduction amounts of 294.00 (lines 74 to 77), twice them less the tax with surtax (line 73), not
below zero, the Ontario tax reduction of 0 (line 80), to the Ontario tax after the reduction (line
81); Schedule ON428-A's LIFT credit, 5.05% of employment income, 5555, at most 875 (lines 5 and 14),
less 5% of net income over 32500, 4125 (line 19), not below zero, 0 (line 20, ON428 line 85), taken
off the Ontario tax after the reduction, not below zero (line 86); and the Ontario health premium on
taxable income by the chart of line 89, 750, added to it to the Ontario tax of line 90; and on the
T1, the federal tax after credits carried to the net federal tax (line 42000), added to the Ontario
tax (line 42800) to the total payable (line 43500); Schedule 6's Canada workers benefit, from the
working income of 110000 (line 5, employment income), 27% of it over 3000 at most 1633 (line 22),
less 15% of the adjusted family net income (line 15, net income) of 115000 over 26855, 13221.75
(line 27), not below zero, 0 (line 28, T1 line 45300); less the total credits (line 48200), here
the chosen income tax deducted of 25000 (line 43700) plus that benefit, to the refund or balance
owing (line 167), 897.1508076, positive so a balance owing) are checked from the files under
`returns/` by `test_worked_returns.py`, as are Returns B, C, D, E and F; this module pins which
capability produces each line, the order, and the trace that explains them. Return A has no
eligible dependant and no infirm child: its amounts for an eligible dependant (T1 line 30400,
Schedule 5 line 5, the federal basic personal amount less the dependant's net income of 0;
ON428 line 58160, the 11,905.00 base less it, at most 10,823) are each claimed for 0 eligible
dependants, and its amount for infirm children (line 30500) is 0 x 2,687, so each total of
credit amounts is unchanged.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import Artifact
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.at_most import AtMost
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.multiple_over import MultipleOver
from app.domain.capabilities.per_unit_amount import PerUnitAmount
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.tapered_amount import TaperedAmount
from app.domain.capabilities.tiered_surcharge import TieredSurcharge
from app.domain.capabilities.times_count import TimesCount
from app.domain.errors import InputAboveBoundError
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.parameters.amount import Amount
from app.domain.parameters.contribution_tier import ContributionTier
from app.domain.parameters.credit import Credit
from app.domain.parameters.factor import Factor
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundTo
from app.domain.parameters.taper import Taper
from app.domain.trace import (
    AtMostLine,
    BracketColumnLine,
    CappedAmountLine,
    ContributionTierLine,
    CreditAmountLine,
    LesserOfLine,
    MultipleOverLine,
    PerUnitAmountLine,
    RateAppliedLine,
    RoundedTotalLine,
    SubtractedLine,
    SubtractedNotBelowZeroLine,
    SumLine,
    SurchargeTierLine,
    TaperedAmountLine,
    TimesCountLine,
)
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    ADJUSTED_FAMILY_NET_INCOME,
    BASIC_PERSONAL_AMOUNT,
    CANADA_EMPLOYMENT_AMOUNT,
    CANADA_WORKERS_BENEFIT,
    CAPITAL_GAIN,
    CPP_BASE_CONTRIBUTIONS,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CWB_BEFORE_REDUCTION,
    CWB_REDUCTION,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    DEPENDANT_NET_INCOME,
    EI_PREMIUMS,
    ELIGIBLE_DEPENDANT_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
    ELIGIBLE_DEPENDANTS,
    EMPLOYMENT_INCOME,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    INCOME_TAX_DEDUCTED,
    INFIRM_CHILDREN,
    INFIRM_CHILDREN_AMOUNT,
    NET_FEDERAL_TAX,
    NET_INCOME,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    REFUND_OR_BALANCE_OWING,
    RRSP_AMOUNT_DEDUCTED,
    RRSP_CONTRIBUTIONS,
    RRSP_CONTRIBUTIONS_AVAILABLE,
    RRSP_DEDUCTION,
    RRSP_DEDUCTION_LIMIT,
    RRSP_DEDUCTION_MAXIMUM,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
    TOTAL_CREDITS,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
    UNION_DUES,
    UNUSED_RRSP_CONTRIBUTIONS,
    UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
    WORKING_INCOME,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
    ELIGIBLE_DEPENDANT_BASE,
    LIFT_CREDIT,
    LIFT_CREDIT_BEFORE_MAXIMUM,
    LIFT_MAXIMUM_CREDIT,
    LIFT_REDUCTION,
    ONTARIO_BASIC_TAX,
    ONTARIO_HEALTH_PREMIUM,
    ONTARIO_SURTAX,
    ONTARIO_TAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_AFTER_LIFT_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
    ONTARIO_TAX_REDUCTION,
    ONTARIO_TAX_WITH_SURTAX,
    TAX_REDUCTION_AMOUNTS,
    TAX_REDUCTION_BASIC,
    TAX_REDUCTION_FOR_CHILDREN,
    TAX_REDUCTION_FOR_DEPENDANTS,
)
from app.main import build_tax_computation

D = Decimal
CA_ON = JurisdictionCode("CA-ON")
# Schedule 8 Part 3a lines 25 and 28: "(in dollars and cents)"; the EI premiums are in dollars and
# cents too, and the federal basic personal amount is rounded half-up to the cent by T4127's BPAF
# rounding footnote.
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)


def service() -> TaxComputationService:
    return build_tax_computation()


def compute(
    employment_income: str,
    capital_gain: str,
    unused_rrsp_contributions: str,
    rrsp_contributions: str,
    rrsp_deduction_limit: str,
    rrsp_amount_deducted: str,
    union_dues: str,
    *,
    dependent_children: int = 0,
    dependants: int = 0,
    eligible_dependants: int = 0,
    dependant_net_income: str = "0",
    infirm_children: int = 0,
    income_tax_deducted: str = "0",
) -> Worksheet:
    return service().compute(
        CA_ON,
        2025,
        Artifact(EMPLOYMENT_INCOME, D(employment_income)),
        Artifact(CAPITAL_GAIN, D(capital_gain)),
        Artifact(UNUSED_RRSP_CONTRIBUTIONS, D(unused_rrsp_contributions)),
        Artifact(RRSP_CONTRIBUTIONS, D(rrsp_contributions)),
        Artifact(RRSP_DEDUCTION_LIMIT, D(rrsp_deduction_limit)),
        Artifact(RRSP_AMOUNT_DEDUCTED, D(rrsp_amount_deducted)),
        Artifact(UNION_DUES, D(union_dues)),
        Artifact(DEPENDENT_CHILDREN, dependent_children),
        Artifact(DEPENDANTS, dependants),
        Artifact(ELIGIBLE_DEPENDANTS, eligible_dependants),
        Artifact(DEPENDANT_NET_INCOME, D(dependant_net_income)),
        Artifact(INFIRM_CHILDREN, infirm_children),
        Artifact(INCOME_TAX_DEDUCTED, D(income_tax_deducted)),
    )


def return_a() -> Worksheet:
    """Return A's inputs, as in `returns/2025_return_a.yaml`, with its chosen tax deducted."""
    return compute(
        "110000", "20000", "0", "1926", "19800", "1926", "2000", income_tax_deducted="25000"
    )


def return_f(dependant_net_income: str = "0", eligible_dependants: int = 1) -> Worksheet:
    """Return F's inputs, as in `returns/2025_return_f.yaml`: one dependent child, an eligible
    dependant with no net income, and its chosen limit and tax deducted."""
    return compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=eligible_dependants,
        dependant_net_income=dependant_net_income,
        income_tax_deducted="8000",
    )


def test_each_amount_is_produced_by_its_capability() -> None:
    worksheet = return_a()

    assert worksheet.producer_of(EMPLOYMENT_INCOME) is None
    assert worksheet.producer_of(CAPITAL_GAIN) is None
    assert worksheet.producer_of(UNUSED_RRSP_CONTRIBUTIONS) is None
    assert worksheet.producer_of(RRSP_CONTRIBUTIONS) is None
    assert worksheet.producer_of(RRSP_DEDUCTION_LIMIT) is None
    assert worksheet.producer_of(RRSP_AMOUNT_DEDUCTED) is None
    assert worksheet.producer_of(UNION_DUES) is None
    assert worksheet.producer_of(DEPENDENT_CHILDREN) is None
    assert worksheet.producer_of(DEPENDANTS) is None
    assert worksheet.producer_of(ELIGIBLE_DEPENDANTS) is None
    assert worksheet.producer_of(DEPENDANT_NET_INCOME) is None
    assert worksheet.producer_of(INFIRM_CHILDREN) is None
    assert worksheet.producer_of(INCOME_TAX_DEDUCTED) is None
    assert isinstance(worksheet.producer_of(RRSP_CONTRIBUTIONS_AVAILABLE), Sum)
    assert isinstance(worksheet.producer_of(RRSP_DEDUCTION_MAXIMUM), LesserOf)
    # Schedule 7 line 18 "cannot be more than the amount on line 17": checked, not capped.
    assert isinstance(worksheet.producer_of(RRSP_DEDUCTION), AtMost)
    assert isinstance(worksheet.producer_of(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD), Subtract)
    assert worksheet.producer_of(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD) is not (
        worksheet.producer_of(REFUND_OR_BALANCE_OWING)
    )
    assert isinstance(worksheet.producer_of(CPP_BASE_CONTRIBUTIONS), TieredContribution)
    assert isinstance(worksheet.producer_of(CPP_FIRST_ADDITIONAL_CONTRIBUTIONS), TieredContribution)
    assert isinstance(
        worksheet.producer_of(CPP_SECOND_ADDITIONAL_CONTRIBUTIONS), TieredContribution
    )
    tiers = {
        worksheet.producer_of(kind)
        for kind in (
            CPP_BASE_CONTRIBUTIONS,
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
        )
    }
    assert len(tiers) == 3
    assert isinstance(worksheet.producer_of(EI_PREMIUMS), TieredContribution)
    assert worksheet.producer_of(EI_PREMIUMS) not in tiers
    assert isinstance(worksheet.producer_of(CPP_ENHANCED_CONTRIBUTIONS), Sum)
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
    assert isinstance(worksheet.producer_of(BASIC_PERSONAL_AMOUNT), TaperedAmount)
    assert isinstance(worksheet.producer_of(ontario.BASIC_PERSONAL_AMOUNT), CreditAmount)
    assert worksheet.producer_of(BASIC_PERSONAL_AMOUNT) is not worksheet.producer_of(
        ontario.BASIC_PERSONAL_AMOUNT
    )
    assert isinstance(worksheet.producer_of(CANADA_EMPLOYMENT_AMOUNT), CappedAmount)
    # Schedule 5 line 5 and T1 line 30400; T1 line 30500; ON428 lines 14 to 16 (line 58160).
    assert isinstance(
        worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT), TimesCount)
    assert isinstance(worksheet.producer_of(INFIRM_CHILDREN_AMOUNT), PerUnitAmount)
    assert worksheet.producer_of(INFIRM_CHILDREN_AMOUNT) is not worksheet.producer_of(
        TAX_REDUCTION_FOR_CHILDREN
    )
    assert isinstance(worksheet.producer_of(ELIGIBLE_DEPENDANT_BASE), CreditAmount)
    assert worksheet.producer_of(ELIGIBLE_DEPENDANT_BASE) is not worksheet.producer_of(
        ontario.BASIC_PERSONAL_AMOUNT
    )
    assert isinstance(
        worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM), SubtractNotBelowZero
    )
    assert worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM) is not (
        worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT)
    )
    assert isinstance(
        worksheet.producer_of(ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT), CappedAmount
    )
    assert isinstance(worksheet.producer_of(ontario.ELIGIBLE_DEPENDANT_AMOUNT), TimesCount)
    assert worksheet.producer_of(ontario.ELIGIBLE_DEPENDANT_AMOUNT) is not (
        worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT)
    )
    assert isinstance(worksheet.producer_of(NON_REFUNDABLE_CREDIT_AMOUNTS), Sum)
    assert isinstance(worksheet.producer_of(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS), Sum)
    assert worksheet.producer_of(NON_REFUNDABLE_CREDIT_AMOUNTS) is not worksheet.producer_of(
        ontario.NON_REFUNDABLE_CREDIT_AMOUNTS
    )
    assert isinstance(worksheet.producer_of(NON_REFUNDABLE_TAX_CREDITS), ApplyRate)
    assert isinstance(worksheet.producer_of(ontario.NON_REFUNDABLE_TAX_CREDITS), ApplyRate)
    assert worksheet.producer_of(NON_REFUNDABLE_TAX_CREDITS) is not worksheet.producer_of(
        ontario.NON_REFUNDABLE_TAX_CREDITS
    )
    assert worksheet.producer_of(NON_REFUNDABLE_TAX_CREDITS) is not worksheet.producer_of(
        TAXABLE_CAPITAL_GAINS
    )
    assert isinstance(worksheet.producer_of(FEDERAL_TAX_AFTER_CREDITS), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_CREDITS), SubtractNotBelowZero)
    assert worksheet.producer_of(FEDERAL_TAX_AFTER_CREDITS) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_CREDITS
    )
    assert isinstance(worksheet.producer_of(ONTARIO_SURTAX), TieredSurcharge)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_WITH_SURTAX), Sum)
    assert worksheet.producer_of(ONTARIO_TAX_WITH_SURTAX) is not worksheet.producer_of(TOTAL_INCOME)
    assert isinstance(worksheet.producer_of(TAX_REDUCTION_BASIC), CreditAmount)
    assert worksheet.producer_of(TAX_REDUCTION_BASIC) is not worksheet.producer_of(
        ontario.BASIC_PERSONAL_AMOUNT
    )
    assert isinstance(worksheet.producer_of(TAX_REDUCTION_FOR_CHILDREN), PerUnitAmount)
    assert isinstance(worksheet.producer_of(TAX_REDUCTION_FOR_DEPENDANTS), PerUnitAmount)
    assert worksheet.producer_of(TAX_REDUCTION_FOR_CHILDREN) is not worksheet.producer_of(
        TAX_REDUCTION_FOR_DEPENDANTS
    )
    assert isinstance(worksheet.producer_of(TAX_REDUCTION_AMOUNTS), Sum)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_REDUCTION), MultipleOver)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_REDUCTION), SubtractNotBelowZero)
    assert worksheet.producer_of(ONTARIO_TAX_AFTER_REDUCTION) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_CREDITS
    )
    assert isinstance(worksheet.producer_of(LIFT_CREDIT_BEFORE_MAXIMUM), ApplyRate)
    assert worksheet.producer_of(LIFT_CREDIT_BEFORE_MAXIMUM) is not worksheet.producer_of(
        TAXABLE_CAPITAL_GAINS
    )
    assert isinstance(worksheet.producer_of(LIFT_MAXIMUM_CREDIT), CappedAmount)
    assert worksheet.producer_of(LIFT_MAXIMUM_CREDIT) is not worksheet.producer_of(
        CANADA_EMPLOYMENT_AMOUNT
    )
    assert isinstance(worksheet.producer_of(LIFT_REDUCTION), TieredSurcharge)
    assert worksheet.producer_of(LIFT_REDUCTION) is not worksheet.producer_of(ONTARIO_SURTAX)
    assert isinstance(worksheet.producer_of(LIFT_CREDIT), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_LIFT_CREDIT), SubtractNotBelowZero)
    assert worksheet.producer_of(LIFT_CREDIT) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_LIFT_CREDIT
    )
    assert worksheet.producer_of(ONTARIO_TAX_AFTER_LIFT_CREDIT) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_REDUCTION
    )
    assert isinstance(worksheet.producer_of(ONTARIO_HEALTH_PREMIUM), TieredSurcharge)
    assert worksheet.producer_of(ONTARIO_HEALTH_PREMIUM) is not worksheet.producer_of(
        ONTARIO_SURTAX
    )
    assert worksheet.producer_of(ONTARIO_HEALTH_PREMIUM) is not worksheet.producer_of(
        LIFT_REDUCTION
    )
    assert isinstance(worksheet.producer_of(ONTARIO_TAX), Sum)
    assert worksheet.producer_of(ONTARIO_TAX) is not worksheet.producer_of(ONTARIO_TAX_WITH_SURTAX)
    assert isinstance(worksheet.producer_of(NET_FEDERAL_TAX), Sum)
    assert isinstance(worksheet.producer_of(TOTAL_PAYABLE), Sum)
    assert isinstance(worksheet.producer_of(WORKING_INCOME), Sum)
    assert isinstance(worksheet.producer_of(ADJUSTED_FAMILY_NET_INCOME), Sum)
    assert worksheet.producer_of(WORKING_INCOME) is not worksheet.producer_of(
        ADJUSTED_FAMILY_NET_INCOME
    )
    assert worksheet.producer_of(WORKING_INCOME) is not worksheet.producer_of(TOTAL_INCOME)
    assert isinstance(worksheet.producer_of(CWB_BEFORE_REDUCTION), TieredSurcharge)
    assert isinstance(worksheet.producer_of(CWB_REDUCTION), TieredSurcharge)
    assert worksheet.producer_of(CWB_BEFORE_REDUCTION) is not worksheet.producer_of(CWB_REDUCTION)
    assert worksheet.producer_of(CWB_REDUCTION) is not worksheet.producer_of(LIFT_REDUCTION)
    assert isinstance(worksheet.producer_of(CANADA_WORKERS_BENEFIT), SubtractNotBelowZero)
    assert worksheet.producer_of(CANADA_WORKERS_BENEFIT) is not worksheet.producer_of(LIFT_CREDIT)
    assert isinstance(worksheet.producer_of(TOTAL_CREDITS), Sum)
    assert worksheet.producer_of(NET_FEDERAL_TAX) is not worksheet.producer_of(TOTAL_PAYABLE)
    assert worksheet.producer_of(NET_FEDERAL_TAX) is not worksheet.producer_of(TOTAL_CREDITS)
    assert worksheet.producer_of(TOTAL_PAYABLE) is not worksheet.producer_of(TOTAL_CREDITS)
    assert worksheet.producer_of(TOTAL_PAYABLE) is not worksheet.producer_of(ONTARIO_TAX)
    # Not floored: T1 line 167 is negative for a refund.
    assert isinstance(worksheet.producer_of(REFUND_OR_BALANCE_OWING), Subtract)


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
        "total_income: employment_income 110000 + taxable_capital_gains 10000 = 120000",
        "120000",
    )
    cpp_base = position(
        "cpp_base_contributions: 4.95% of employment_income between 3500 and 71300 (67800), "
        "at most 3356.1 (half-up to 0.01)",
        "3356.10",
    )
    cpp_first = position(
        "cpp_first_additional_contributions: 1% of employment_income between 3500 and 71300 "
        "(67800), at most 678 (half-up to 0.01)",
        "678.00",
    )
    cpp_second = position(
        "cpp_second_additional_contributions: 4% of employment_income between 71300 and 81200 "
        "(9900), at most 396 (half-up to 0.01)",
        "396.00",
    )
    cpp_enhanced = position(
        "cpp_enhanced_contributions: cpp_first_additional_contributions 678 "
        "+ cpp_second_additional_contributions 396 = 1074",
        "1074.00",
    )
    ei = position(
        "ei_premiums: 1.64% of employment_income between 0 and 65700 (65700), "
        "at most 1077.48 (half-up to 0.01)",
        "1077.48",
    )
    rrsp_available = position(
        "rrsp_contributions_available: unused_rrsp_contributions 0 "
        "+ rrsp_contributions 1926 = 1926",
        "1926",
    )
    rrsp_maximum = position(
        "rrsp_deduction_maximum: lesser of rrsp_contributions_available 1926 "
        "and rrsp_deduction_limit 19800 = 1926",
        "1926",
    )
    rrsp = position(
        "rrsp_deduction: rrsp_amount_deducted 1926, at most rrsp_deduction_maximum 1926",
        "1926",
    )
    rrsp_carried = position(
        "unused_rrsp_contributions_carried_forward: rrsp_contributions_available 1926 "
        "less rrsp_deduction 1926 = 0",
        "0",
    )
    deductions = position(
        "deductions_from_total_income: rrsp_deduction 1926 + union_dues 2000 "
        "+ cpp_enhanced_contributions 1074 = 5000",
        "5000",
    )
    net = position(
        "net_income: total_income 120000 less deductions_from_total_income 5000, "
        "not below 0 = 115000",
        "115000",
    )
    net_deductions = position("deductions_from_net_income: no parts = 0", "0")
    taxable = position(
        "taxable_income: net_income 115000 less deductions_from_net_income 0, not below 0 = 115000",
        "115000",
    )
    # T1 Part A, the column "more than $114,750 but not more than $177,882": line 72 is
    # 115000 - 114750 = 250, line 74 is 26% of it, 65.00, and line 76 adds line 75's 20,081.25.
    federal_column = position("26% on 250 over 114750 plus 20081.25", "20146.25")
    federal_basic = position("federal_basic_tax on taxable_income 115000 (no rounding)", "20146.25")
    federal_amount = position(
        "basic_personal_amount: 14538 plus 1591 less 0 for net_income 115000 over 177882 "
        "(range 75532), not below 14538 (half-up to 0.01)",
        "16129",
    )
    employment_amount = position(
        "canada_employment_amount: lesser of employment_income 110000 and 1471 (no rounding)",
        "1471",
    )
    # Schedule 5 line 5, then T1 line 30400 for 0 eligible dependants; line 30500.
    federal_dependant = position(
        "eligible_dependant_amount_before_count: basic_personal_amount 16129 "
        "less dependant_net_income 0, not below 0 = 16129",
        "16129",
    )
    federal_dependant_claimed = position(
        "eligible_dependant_amount: eligible_dependant_amount_before_count 16129 "
        "for each of 0 eligible_dependants = 0",
        "0",
    )
    infirm_children = position(
        "infirm_children_amount: 2687 for each of 0 infirm_children = 0 (no rounding)", "0"
    )
    federal_amounts = position(
        "non_refundable_credit_amounts: basic_personal_amount 16129 "
        "+ eligible_dependant_amount 0 + infirm_children_amount 0 "
        "+ cpp_base_contributions 3356.1 + ei_premiums 1077.48 "
        "+ canada_employment_amount 1471 = 22033.58",
        "22033.58",
    )
    federal_credit = position(
        "non_refundable_tax_credits: 14.5% of non_refundable_credit_amounts 22033.58 (no rounding)",
        "3194.8691",
    )
    federal_after = position(
        "federal_tax_after_credits: federal_basic_tax 20146.25 "
        "less non_refundable_tax_credits 3194.8691, not below 0 = 16951.3809",
        "16951.3809",
    )
    # ON428 Part A, the column "more than $105,775 but not more than $150,000": line 4 is
    # 115000 - 105775 = 9225, line 6 is 11.16% of it, 1029.51, and line 8 adds line 7's 7,510.09.
    ontario_column = position("11.16% on 9225 over 105775 plus 7510.09", "8539.60")
    ontario_basic = position("ontario_basic_tax on taxable_income 115000 (no rounding)", "8539.60")
    ontario_amount = position("basic_personal_amount: credit amount 12747 (no rounding)", "12747")
    # ON428 lines 14 to 16 (line 58160), for 0 eligible dependants.
    ontario_base = position("eligible_dependant_base: credit amount 11905 (no rounding)", "11905")
    ontario_before_maximum = position(
        "eligible_dependant_amount_before_maximum: eligible_dependant_base 11905 "
        "less dependant_net_income 0, not below 0 = 11905",
        "11905",
    )
    ontario_dependant = position(
        "eligible_dependant_amount_before_count: lesser of "
        "eligible_dependant_amount_before_maximum 11905 and 10823 (no rounding)",
        "10823",
    )
    ontario_dependant_claimed = position(
        "eligible_dependant_amount: eligible_dependant_amount_before_count 10823 "
        "for each of 0 eligible_dependants = 0",
        "0",
    )
    ontario_amounts = position(
        "non_refundable_credit_amounts: basic_personal_amount 12747 "
        "+ eligible_dependant_amount 0 "
        "+ cpp_base_contributions 3356.1 + ei_premiums 1077.48 = 17180.58",
        "17180.58",
    )
    ontario_credit = position(
        "non_refundable_tax_credits: 5.05% of non_refundable_credit_amounts 17180.58 (no rounding)",
        "867.61929",
    )
    ontario_after = position(
        "ontario_tax_after_credits: ontario_basic_tax 8539.6 "
        "less non_refundable_tax_credits 867.61929, not below 0 = 7671.98071",
        "7671.98071",
    )
    surtax_first = position(
        "ontario_surtax: 20% of ontario_tax_after_credits 7671.98071 over 5710 (no rounding)",
        "392.396142",
    )
    surtax_second = position(
        "ontario_surtax: 36% of ontario_tax_after_credits 7671.98071 over 7307 (no rounding)",
        "131.3930556",
    )
    with_surtax = position(
        "ontario_tax_with_surtax: ontario_tax_after_credits 7671.98071 "
        "+ ontario_surtax 523.7891976 = 8195.7699076",
        "8195.7699076",
    )
    reduction_basic = position(
        "tax_reduction_basic: credit amount 294 (no rounding)",
        "294.00",
    )
    reduction_children = position(
        "tax_reduction_for_children: 544 for each of 0 dependent_children = 0 (no rounding)",
        "0",
    )
    reduction_dependants = position(
        "tax_reduction_for_dependants: 544 for each of 0 dependants = 0 (no rounding)",
        "0",
    )
    reduction_amounts = position(
        "tax_reduction_amounts: tax_reduction_basic 294 + tax_reduction_for_children 0 "
        "+ tax_reduction_for_dependants 0 = 294",
        "294.00",
    )
    reduction = position(
        "ontario_tax_reduction: 2 × tax_reduction_amounts 294 "
        "over ontario_tax_with_surtax 8195.7699076, not below 0 (no rounding)",
        "0",
    )
    after_reduction = position(
        "ontario_tax_after_reduction: ontario_tax_with_surtax 8195.7699076 "
        "less ontario_tax_reduction 0, not below 0 = 8195.7699076",
        "8195.7699076",
    )
    lift_before_maximum = position(
        "lift_credit_before_maximum: 5.05% of employment_income 110000 (no rounding)", "5555"
    )
    lift_maximum = position(
        "lift_maximum_credit: lesser of lift_credit_before_maximum 5555 and 875 (no rounding)",
        "875",
    )
    lift_reduction = position(
        "lift_reduction: 5% of net_income 115000 over 32500 (no rounding)", "4125"
    )
    lift = position(
        "lift_credit: lift_maximum_credit 875 less lift_reduction 4125, not below 0 = 0", "0"
    )
    after_lift = position(
        "ontario_tax_after_lift_credit: ontario_tax_after_reduction 8195.7699076 "
        "less lift_credit 0, not below 0 = 8195.7699076",
        "8195.7699076",
    )
    premium_first = position(
        "ontario_health_premium: 6% of taxable_income 115000 over 20000, at most 300 (no rounding)",
        "300",
    )
    premium_second = position(
        "ontario_health_premium: 6% of taxable_income 115000 over 36000, at most 150 (no rounding)",
        "150",
    )
    premium_third = position(
        "ontario_health_premium: 25% of taxable_income 115000 over 48000, at most 150 "
        "(no rounding)",
        "150",
    )
    premium_fourth = position(
        "ontario_health_premium: 25% of taxable_income 115000 over 72000, at most 150 "
        "(no rounding)",
        "150",
    )
    premium_fifth = position(
        "ontario_health_premium: 25% of taxable_income 115000 over 200000, at most 150 "
        "(no rounding)",
        "0",
    )
    ontario_tax = position(
        "ontario_tax: ontario_tax_after_lift_credit 8195.7699076 "
        "+ ontario_health_premium 750 = 8945.7699076",
        "8945.7699076",
    )
    net_federal = position(
        "net_federal_tax: federal_tax_after_credits 16951.3809 = 16951.3809", "16951.3809"
    )
    payable = position(
        "total_payable: net_federal_tax 16951.3809 + ontario_tax 8945.7699076 = 25897.1508076",
        "25897.1508076",
    )
    working = position("working_income: employment_income 110000 = 110000", "110000")
    family_net = position("adjusted_family_net_income: net_income 115000 = 115000", "115000")
    cwb_before_reduction = position(
        "cwb_before_reduction: 27% of working_income 110000 over 3000, at most 1633 (no rounding)",
        "1633",
    )
    cwb_reduction = position(
        "cwb_reduction: 15% of adjusted_family_net_income 115000 over 26855 (no rounding)",
        "13221.75",
    )
    cwb = position(
        "canada_workers_benefit: cwb_before_reduction 1633 less cwb_reduction 13221.75, "
        "not below 0 = 0",
        "0",
    )
    credits = position(
        "total_credits: income_tax_deducted 25000 + canada_workers_benefit 0 = 25000", "25000"
    )
    balance = position(
        "refund_or_balance_owing: total_payable 25897.1508076 "
        "less total_credits 25000 = 897.1508076",
        "897.1508076",
    )
    assert taxable_gains < total < net
    assert cpp_first < cpp_enhanced < deductions < net
    assert rrsp_available < rrsp_maximum < rrsp < deductions
    assert rrsp < rrsp_carried
    assert cpp_second < cpp_enhanced
    assert cpp_base < federal_amounts
    assert cpp_base < ontario_amounts
    assert ei < federal_amounts
    assert ei < ontario_amounts
    assert net < taxable
    assert net_deductions < taxable
    assert taxable < federal_column < federal_basic < federal_after
    assert taxable < ontario_column < ontario_basic
    assert ontario_basic < ontario_after
    assert net < federal_amount < federal_amounts < federal_credit < federal_after
    assert employment_amount < federal_amounts
    assert federal_amount < federal_dependant < federal_dependant_claimed < federal_amounts
    assert infirm_children < federal_amounts
    assert ontario_base < ontario_before_maximum < ontario_dependant
    assert ontario_dependant < ontario_dependant_claimed < ontario_amounts
    assert ontario_amount < ontario_amounts < ontario_credit < ontario_after
    assert ontario_after < surtax_first < surtax_second < with_surtax
    assert reduction_basic < reduction_amounts
    assert reduction_children < reduction_amounts
    assert reduction_dependants < reduction_amounts
    assert with_surtax < reduction < after_reduction
    assert reduction_amounts < reduction
    assert taxable < premium_first < premium_second < premium_third < premium_fourth
    assert premium_fourth < premium_fifth < ontario_tax
    assert lift_before_maximum < lift_maximum < lift < after_lift < ontario_tax
    assert net < lift_reduction < lift
    assert after_reduction < after_lift
    assert federal_after < net_federal < payable
    assert ontario_tax < payable < balance
    assert working < cwb_before_reduction < cwb
    assert net < family_net < cwb_reduction < cwb < credits
    assert credits < balance


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    trace = return_a().trace

    rated = {line.output: line for line in trace if isinstance(line, RateAppliedLine)}
    sums = {line.output: line for line in trace if isinstance(line, SumLine)}
    floored = {line.output: line for line in trace if isinstance(line, SubtractedNotBelowZeroLine)}
    subtracted = {line.output: line for line in trace if isinstance(line, SubtractedLine)}
    totals = {line.output: line for line in trace if isinstance(line, RoundedTotalLine)}
    amounts = {line.output: line for line in trace if isinstance(line, CreditAmountLine)}
    tapered = {line.output: line for line in trace if isinstance(line, TaperedAmountLine)}
    capped = {line.output: line for line in trace if isinstance(line, CappedAmountLine)}
    tiers = {line.output: line for line in trace if isinstance(line, ContributionTierLine)}
    lesser = {line.output: line for line in trace if isinstance(line, LesserOfLine)}
    at_most = {line.output: line for line in trace if isinstance(line, AtMostLine)}
    surcharged = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == ONTARIO_SURTAX
    ]
    lift_tiers = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == LIFT_REDUCTION
    ]
    premium_tiers = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == ONTARIO_HEALTH_PREMIUM
    ]
    cwb_basic_tiers = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == CWB_BEFORE_REDUCTION
    ]
    cwb_reduction_tiers = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == CWB_REDUCTION
    ]
    per_unit = {line.output: line for line in trace if isinstance(line, PerUnitAmountLine)}
    multiples = {line.output: line for line in trace if isinstance(line, MultipleOverLine)}
    times = {line.output: line for line in trace if isinstance(line, TimesCountLine)}

    # The rate is applied once, to each form's total of credit amounts (T1 line 33800, ON428
    # line 58840), giving its non-refundable tax credits (T1 line 35000, ON428 line 61500).
    assert rated == {
        TAXABLE_CAPITAL_GAINS: RateAppliedLine(
            TAXABLE_CAPITAL_GAINS, CAPITAL_GAIN, D("20000"), Rate(D("0.5")), NO_ROUNDING, D("10000")
        ),
        NON_REFUNDABLE_TAX_CREDITS: RateAppliedLine(
            NON_REFUNDABLE_TAX_CREDITS,
            NON_REFUNDABLE_CREDIT_AMOUNTS,
            D("22033.58"),
            Rate(D("0.145")),
            NO_ROUNDING,
            D("3194.8691"),
        ),
        ontario.NON_REFUNDABLE_TAX_CREDITS: RateAppliedLine(
            ontario.NON_REFUNDABLE_TAX_CREDITS,
            ontario.NON_REFUNDABLE_CREDIT_AMOUNTS,
            D("17180.58"),
            Rate(D("0.0505")),
            NO_ROUNDING,
            D("867.61929"),
        ),
        # Schedule ON428-A line 5 "Line 3 multiplied by the percentage from line 4 (maximum
        # $875)", before its maximum: line 3 is employment income (line 10100), as line 2 (line
        # 10400) is not triggered.
        LIFT_CREDIT_BEFORE_MAXIMUM: RateAppliedLine(
            LIFT_CREDIT_BEFORE_MAXIMUM,
            EMPLOYMENT_INCOME,
            D("110000"),
            Rate(D("0.0505")),
            NO_ROUNDING,
            D("5555.0000"),
        ),
    }
    assert sums == {
        TOTAL_INCOME: SumLine(
            TOTAL_INCOME,
            ((EMPLOYMENT_INCOME, D("110000")), (TAXABLE_CAPITAL_GAINS, D("10000"))),
            D("120000"),
        ),
        # Schedule 8 Part 3a line 28 "Line 26 plus line 27", to T1 line 22215.
        CPP_ENHANCED_CONTRIBUTIONS: SumLine(
            CPP_ENHANCED_CONTRIBUTIONS,
            (
                (CPP_FIRST_ADDITIONAL_CONTRIBUTIONS, D("678.00")),
                (CPP_SECOND_ADDITIONAL_CONTRIBUTIONS, D("396.00")),
            ),
            D("1074.00"),
        ),
        # Schedule 7 line 5 "Line 1 plus line 4 ... Total contributions", to line 10
        # "Contributions available to deduct" with no HBP or LLP repayments (line 9).
        RRSP_CONTRIBUTIONS_AVAILABLE: SumLine(
            RRSP_CONTRIBUTIONS_AVAILABLE,
            ((UNUSED_RRSP_CONTRIBUTIONS, D("0")), (RRSP_CONTRIBUTIONS, D("1926"))),
            D("1926"),
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
                (ELIGIBLE_DEPENDANT_AMOUNT, D("0")),
                (INFIRM_CHILDREN_AMOUNT, D("0")),
                (CPP_BASE_CONTRIBUTIONS, D("3356.10")),
                (EI_PREMIUMS, D("1077.48")),
                (CANADA_EMPLOYMENT_AMOUNT, D("1471")),
            ),
            D("22033.58"),
        ),
        # ON428 has no Canada employment amount; its lines 58240 and 58300 read the federal
        # amounts (lines 30800 and 31200).
        ontario.NON_REFUNDABLE_CREDIT_AMOUNTS: SumLine(
            ontario.NON_REFUNDABLE_CREDIT_AMOUNTS,
            (
                (ontario.BASIC_PERSONAL_AMOUNT, D("12747")),
                (ontario.ELIGIBLE_DEPENDANT_AMOUNT, D("0")),
                (CPP_BASE_CONTRIBUTIONS, D("3356.10")),
                (EI_PREMIUMS, D("1077.48")),
            ),
            D("17180.58"),
        ),
        # ON428 line 69 "Line 62 plus line 68": the Ontario tax after credits plus the surtax.
        ONTARIO_TAX_WITH_SURTAX: SumLine(
            ONTARIO_TAX_WITH_SURTAX,
            ((ONTARIO_TAX_AFTER_CREDITS, D("7671.98071")), (ONTARIO_SURTAX, D("523.7891976"))),
            D("8195.7699076"),
        ),
        # ON428 line 77 "Add lines 74 to 76.", in line order.
        TAX_REDUCTION_AMOUNTS: SumLine(
            TAX_REDUCTION_AMOUNTS,
            (
                (TAX_REDUCTION_BASIC, D("294.00")),
                (TAX_REDUCTION_FOR_CHILDREN, D("0")),
                (TAX_REDUCTION_FOR_DEPENDANTS, D("0")),
            ),
            D("294.00"),
        ),
        # ON428 line 90 "Line 88 plus line 89 Enter this amount on line 42800 of your return.
        # Ontario tax": line 88 carries line 86, as line 87 is not triggered.
        ONTARIO_TAX: SumLine(
            ONTARIO_TAX,
            (
                (ONTARIO_TAX_AFTER_LIFT_CREDIT, D("8195.7699076")),
                (ONTARIO_HEALTH_PREMIUM, D("750")),
            ),
            D("8945.7699076"),
        ),
        # T1 line 142 (line 42000) "Add lines 139 to 141. Net federal tax": line 139 carries the
        # federal tax after credits (line 126, 42900, through line 134, 40600), and lines 140
        # and 141 are not modelled.
        NET_FEDERAL_TAX: SumLine(
            NET_FEDERAL_TAX, ((FEDERAL_TAX_AFTER_CREDITS, D("16951.3809")),), D("16951.3809")
        ),
        # T1 line 148 (line 43500) "Add lines 143 to 147. Total payable", in line order: line
        # 143 "Amount from line 42000" and line 147 (42800), the Ontario tax.
        TOTAL_PAYABLE: SumLine(
            TOTAL_PAYABLE,
            ((NET_FEDERAL_TAX, D("16951.3809")), (ONTARIO_TAX, D("8945.7699076"))),
            D("25897.1508076"),
        ),
        # Schedule 6 line 5 "Add lines 1 to 4. Enter the result, even if it is "0". Working
        # income": line 1 "Employment income and other employment income from line 10100 and line
        # 10400 of the return" alone, as lines 2 to 4 are not triggered.
        WORKING_INCOME: SumLine(WORKING_INCOME, ((EMPLOYMENT_INCOME, D("110000")),), D("110000")),
        # Schedule 6 line 15 "Line 13 minus line 14 Enter this amount on line 23 and line 35.
        # Adjusted family net income": line 7, net income (line 23600), carried unchanged.
        ADJUSTED_FAMILY_NET_INCOME: SumLine(
            ADJUSTED_FAMILY_NET_INCOME, ((NET_INCOME, D("115000")),), D("115000")
        ),
        # T1 line 166 (line 48200) "Add lines 150 to 165. Total credits": line 150 (43700) and
        # line 155 (45300), the Canada workers benefit, in line order.
        TOTAL_CREDITS: SumLine(
            TOTAL_CREDITS,
            ((INCOME_TAX_DEDUCTED, D("25000")), (CANADA_WORKERS_BENEFIT, D("0"))),
            D("25000"),
        ),
    }
    assert subtracted == {
        # Schedule 7 line 23 "Line 21 minus line 22 Your unused contributions available to carry
        # forward to a future year": all of the 1926 available is deducted, so nothing is left.
        UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD: SubtractedLine(
            output=UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
            minuend=RRSP_CONTRIBUTIONS_AVAILABLE,
            minuend_amount=D("1926"),
            subtrahend=RRSP_DEDUCTION,
            subtrahend_amount=D("1926"),
            result=D("0"),
        ),
        # T1 line 167 "Line 149 minus line 166 ... Refund or balance owing": exact, not floored,
        # and positive here, so a balance owing (line 48500).
        REFUND_OR_BALANCE_OWING: SubtractedLine(
            output=REFUND_OR_BALANCE_OWING,
            minuend=TOTAL_PAYABLE,
            minuend_amount=D("25897.1508076"),
            subtrahend=TOTAL_CREDITS,
            subtrahend_amount=D("25000"),
            result=D("897.1508076"),
        ),
    }
    # T1 line 30000 and the Federal Worksheet (5000-D1): net income of 115000 is at or below
    # the 177882 threshold, so the reduction (line 9) is 0 and the amount is the base plus the
    # whole supplement, 14538 + 1591 = 16129, rounded half-up to the cent.
    assert tapered == {
        BASIC_PERSONAL_AMOUNT: TaperedAmountLine(
            output=BASIC_PERSONAL_AMOUNT,
            base=NET_INCOME,
            base_amount=D("115000"),
            taper=Taper(
                base=D("14538"), supplement=D("1591"), threshold=D("177882"), range=D("75532")
            ),
            rounding=CENT,
            reduction=D("0"),
            result=D("16129.00"),
        )
    }
    # ON428 line 58040 has no reduction: the Ontario amount is the dataset's credit amount. ON428
    # line 74 "Basic reduction 294.00" is claimed whole too.
    assert amounts == {
        ontario.BASIC_PERSONAL_AMOUNT: CreditAmountLine(
            ontario.BASIC_PERSONAL_AMOUNT, Credit(amount=D("12747")), NO_ROUNDING, D("12747")
        ),
        TAX_REDUCTION_BASIC: CreditAmountLine(
            TAX_REDUCTION_BASIC, Credit(amount=D("294.00")), NO_ROUNDING, D("294.00")
        ),
        # ON428 line 14 "Base amount 11,905.00".
        ELIGIBLE_DEPENDANT_BASE: CreditAmountLine(
            ELIGIBLE_DEPENDANT_BASE, Credit(amount=D("11905.00")), NO_ROUNDING, D("11905.00")
        ),
    }
    # ON428 line 75 (line 60969) "Number of dependent children multiplied by $544" and line 76
    # (line 60970) "Number of dependants multiplied by $544": Return A has neither.
    assert per_unit == {
        TAX_REDUCTION_FOR_CHILDREN: PerUnitAmountLine(
            output=TAX_REDUCTION_FOR_CHILDREN,
            count_kind=DEPENDENT_CHILDREN,
            count=0,
            per_unit=Amount(D("544")),
            rounding=NO_ROUNDING,
            result=D("0"),
        ),
        TAX_REDUCTION_FOR_DEPENDANTS: PerUnitAmountLine(
            output=TAX_REDUCTION_FOR_DEPENDANTS,
            count_kind=DEPENDANTS,
            count=0,
            per_unit=Amount(D("544")),
            rounding=NO_ROUNDING,
            result=D("0"),
        ),
        # T1 line 30500 "Number of children you are claiming this amount for Line 30499"
        # "multiplied by $2,687": Return A has no infirm child.
        INFIRM_CHILDREN_AMOUNT: PerUnitAmountLine(
            output=INFIRM_CHILDREN_AMOUNT,
            count_kind=INFIRM_CHILDREN,
            count=0,
            per_unit=Amount(D("2687")),
            rounding=NO_ROUNDING,
            result=D("0"),
        ),
    }
    # T1 line 30400 and ON428 line 58160: Schedule 5 line 5 and ON428 line 16, each claimed for
    # the 0 eligible dependants of Return A, a plain 0.
    assert times == {
        ELIGIBLE_DEPENDANT_AMOUNT: TimesCountLine(
            output=ELIGIBLE_DEPENDANT_AMOUNT,
            amount_kind=ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
            amount_value=D("16129.00"),
            count_kind=ELIGIBLE_DEPENDANTS,
            count=0,
            result=D("0"),
        ),
        ontario.ELIGIBLE_DEPENDANT_AMOUNT: TimesCountLine(
            output=ontario.ELIGIBLE_DEPENDANT_AMOUNT,
            amount_kind=ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
            amount_value=D("10823"),
            count_kind=ELIGIBLE_DEPENDANTS,
            count=0,
            result=D("0"),
        ),
    }
    # ON428 line 78 "Amount from line 77 above multiplied by 2", line 79 "Amount from line 73
    # above" and line 80 "Line 78 minus line 79 (if negative, enter "0") Ontario tax reduction":
    # 588.00 is below the tax with surtax of 8195.7699076, so the reduction is 0.
    assert multiples == {
        ONTARIO_TAX_REDUCTION: MultipleOverLine(
            output=ONTARIO_TAX_REDUCTION,
            base=TAX_REDUCTION_AMOUNTS,
            base_amount=D("294.00"),
            factor=Factor(D("2")),
            less=ONTARIO_TAX_WITH_SURTAX,
            less_amount=D("8195.7699076"),
            rounding=NO_ROUNDING,
            result=D("0"),
        )
    }
    # T1 line 92 (line 31260) "Enter whichever is less: $1,471 or line 1 plus line 2.":
    # employment income of 110000 is above the cap, so the amount is the cap.
    assert capped == {
        CANADA_EMPLOYMENT_AMOUNT: CappedAmountLine(
            CANADA_EMPLOYMENT_AMOUNT,
            EMPLOYMENT_INCOME,
            D("110000"),
            Amount(D("1471")),
            NO_ROUNDING,
            D("1471"),
        ),
        # Schedule ON428-A line 5's "(maximum $875)" and line 14 "Amount from line 5 above
        # (maximum $875)": 5555.0000 is above it.
        LIFT_MAXIMUM_CREDIT: CappedAmountLine(
            LIFT_MAXIMUM_CREDIT,
            LIFT_CREDIT_BEFORE_MAXIMUM,
            D("5555.0000"),
            Amount(D("875")),
            NO_ROUNDING,
            D("875"),
        ),
        # ON428 line 16's "(maximum $10,823)": 11905.00 is above it.
        ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT: CappedAmountLine(
            ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
            ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
            D("11905.00"),
            Amount(D("10823")),
            NO_ROUNDING,
            D("10823"),
        ),
    }
    # Schedule 7 line 17 "Enter whichever is less: amount from line 13 or line 16.": the
    # contributions available to deduct of 1926 are below the deduction limit of 19800, so the
    # most that may be deducted is the contributions available to deduct.
    assert lesser == {
        RRSP_DEDUCTION_MAXIMUM: LesserOfLine(
            RRSP_DEDUCTION_MAXIMUM,
            ((RRSP_CONTRIBUTIONS_AVAILABLE, D("1926")), (RRSP_DEDUCTION_LIMIT, D("19800"))),
            D("1926"),
        )
    }
    # Schedule 7 line 18 "(cannot be more than the amount on line 17)": the full 1926 is
    # deducted, equal to line 17, so line 20 is line 18.
    assert at_most == {
        RRSP_DEDUCTION: AtMostLine(
            output=RRSP_DEDUCTION,
            amount_kind=RRSP_AMOUNT_DEDUCTED,
            amount_value=D("1926"),
            bound=RRSP_DEDUCTION_MAXIMUM,
            bound_value=D("1926"),
        )
    }
    # Schedule 8 Part 3 lines 11, 12 and 22: employment income of 110000 is above both
    # ceilings, so each band is full and each contribution is its maximum. T1 line 31200: it
    # is above the $65,700 maximum insurable earnings, so the EI premiums are their maximum.
    assert tiers == {
        CPP_BASE_CONTRIBUTIONS: ContributionTierLine(
            CPP_BASE_CONTRIBUTIONS,
            EMPLOYMENT_INCOME,
            D("110000"),
            ContributionTier(Rate(D("0.0495")), D("3500"), D("71300"), D("3356.10")),
            CENT,
            D("67800"),
            D("3356.10"),
        ),
        CPP_FIRST_ADDITIONAL_CONTRIBUTIONS: ContributionTierLine(
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
            EMPLOYMENT_INCOME,
            D("110000"),
            ContributionTier(Rate(D("0.01")), D("3500"), D("71300"), D("678.00")),
            CENT,
            D("67800"),
            D("678.00"),
        ),
        CPP_SECOND_ADDITIONAL_CONTRIBUTIONS: ContributionTierLine(
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
            EMPLOYMENT_INCOME,
            D("110000"),
            ContributionTier(Rate(D("0.04")), D("71300"), D("81200"), D("396.00")),
            CENT,
            D("9900"),
            D("396.00"),
        ),
        EI_PREMIUMS: ContributionTierLine(
            EI_PREMIUMS,
            EMPLOYMENT_INCOME,
            D("110000"),
            ContributionTier(Rate(D("0.0164")), D("0"), D("65700"), D("1077.48")),
            CENT,
            D("65700"),
            D("1077.48"),
        ),
    }
    # ON428 line 66 "(Line 65 minus $5,710) multiplied by 20% (if negative, enter "0")" and line
    # 67 "(Line 65 minus $7,307) multiplied by 36% (if negative, enter "0")", in that order, on
    # the Ontario tax after credits (line 65, as line 64 is not modelled); no rounding stated.
    assert surcharged == [
        SurchargeTierLine(
            output=ONTARIO_SURTAX,
            base=ONTARIO_TAX_AFTER_CREDITS,
            base_amount=D("7671.98071"),
            threshold=D("5710"),
            rate=Rate(D("0.20")),
            rounding=NO_ROUNDING,
            part=D("392.396142"),
        ),
        SurchargeTierLine(
            output=ONTARIO_SURTAX,
            base=ONTARIO_TAX_AFTER_CREDITS,
            base_amount=D("7671.98071"),
            threshold=D("7307"),
            rate=Rate(D("0.36")),
            rounding=NO_ROUNDING,
            part=D("131.3930556"),
        ),
    ]
    # ON428 line 89 and its chart, on line 1 "Enter your taxable income from line 26000 of your
    # return", in threshold order: taxable income of 115000 is "more than $72,600 but not more
    # than $200,000", so the four lower tiers each charge their maximum, 300 + 150 + 150 + 150 =
    # 750, and the top tier nothing; the chart states no rounding.
    assert premium_tiers == [
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("20000"),
            rate=Rate(D("0.06")),
            rounding=NO_ROUNDING,
            part=D("300"),
            maximum=D("300"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("36000"),
            rate=Rate(D("0.06")),
            rounding=NO_ROUNDING,
            part=D("150"),
            maximum=D("150"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("48000"),
            rate=Rate(D("0.25")),
            rounding=NO_ROUNDING,
            part=D("150"),
            maximum=D("150"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("72000"),
            rate=Rate(D("0.25")),
            rounding=NO_ROUNDING,
            part=D("150"),
            maximum=D("150"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("200000"),
            rate=Rate(D("0.25")),
            rounding=NO_ROUNDING,
            part=D("0"),
            maximum=D("150"),
        ),
    ]
    # Schedule ON428-A line 17 "Line 15 minus line 16 (if negative, enter "0")" and line 19 "Line
    # 17 multiplied by the percentage from line 18": net income (line 15, from line 13) of 115000
    # less the 32,500.00 threshold (line 16), times 5% (line 18); no rounding stated.
    assert lift_tiers == [
        SurchargeTierLine(
            output=LIFT_REDUCTION,
            base=NET_INCOME,
            base_amount=D("115000"),
            threshold=D("32500"),
            rate=Rate(D("0.05")),
            rounding=NO_ROUNDING,
            part=D("4125.00"),
        )
    ]
    # Schedule 6 line 18 "Line 16 minus line 17 (if negative, enter "0")", line 20 "Line 18
    # multiplied by the percentage from line 19" and line 22 "Enter whichever is less: amount from
    # line 20 or line 21.": (110000 - 3000) x 27% is above the $1,633 of line 21, so line 22 is
    # 1633; no rounding stated.
    assert cwb_basic_tiers == [
        SurchargeTierLine(
            output=CWB_BEFORE_REDUCTION,
            base=WORKING_INCOME,
            base_amount=D("110000"),
            threshold=D("3000"),
            rate=Rate(D("0.27")),
            rounding=NO_ROUNDING,
            part=D("1633"),
            maximum=D("1633"),
        )
    ]
    # Schedule 6 line 25 "Line 23 minus line 24 (if negative, enter "0")" and line 27 "Line 25
    # multiplied by the percentage from line 26": (115000 - 26855) x 15%; no rounding stated.
    assert cwb_reduction_tiers == [
        SurchargeTierLine(
            output=CWB_REDUCTION,
            base=ADJUSTED_FAMILY_NET_INCOME,
            base_amount=D("115000"),
            threshold=D("26855"),
            rate=Rate(D("0.15")),
            rounding=NO_ROUNDING,
            part=D("13221.75"),
        )
    ]
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
        # Each form's credits come off its basic tax, not below zero; here both taxes exceed
        # their credits.
        FEDERAL_TAX_AFTER_CREDITS: SubtractedNotBelowZeroLine(
            output=FEDERAL_TAX_AFTER_CREDITS,
            minuend=FEDERAL_BASIC_TAX,
            minuend_amount=D("20146.25"),
            subtrahend=NON_REFUNDABLE_TAX_CREDITS,
            subtrahend_amount=D("3194.8691"),
            result=D("16951.3809"),
        ),
        ONTARIO_TAX_AFTER_CREDITS: SubtractedNotBelowZeroLine(
            output=ONTARIO_TAX_AFTER_CREDITS,
            minuend=ONTARIO_BASIC_TAX,
            minuend_amount=D("8539.60"),
            subtrahend=ontario.NON_REFUNDABLE_TAX_CREDITS,
            subtrahend_amount=D("867.61929"),
            result=D("7671.98071"),
        ),
        # Schedule 5 line 5 "Line 3 minus line 4 (if negative, enter "0")": line 3 is line 1,
        # the basic personal amount, as line 2 is not triggered; line 4 the dependant's net
        # income, entered as 0.
        ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT: SubtractedNotBelowZeroLine(
            output=ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
            minuend=BASIC_PERSONAL_AMOUNT,
            minuend_amount=D("16129.00"),
            subtrahend=DEPENDANT_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("16129.00"),
        ),
        # ON428 line 16 "Line 14 minus line 15 (if negative, enter "0")", before its maximum.
        ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM: SubtractedNotBelowZeroLine(
            output=ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
            minuend=ELIGIBLE_DEPENDANT_BASE,
            minuend_amount=D("11905.00"),
            subtrahend=DEPENDANT_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("11905.00"),
        ),
        # ON428 line 81 "Line 73 minus line 80 (if negative, enter "0")".
        ONTARIO_TAX_AFTER_REDUCTION: SubtractedNotBelowZeroLine(
            output=ONTARIO_TAX_AFTER_REDUCTION,
            minuend=ONTARIO_TAX_WITH_SURTAX,
            minuend_amount=D("8195.7699076"),
            subtrahend=ONTARIO_TAX_REDUCTION,
            subtrahend_amount=D("0"),
            result=D("8195.7699076"),
        ),
        # Schedule ON428-A line 20 "Line 14 minus line 19 (if negative, enter "0")": the
        # reduction of 4125.00 exceeds the 875, so the credit (ON428 line 85) is 0.
        LIFT_CREDIT: SubtractedNotBelowZeroLine(
            output=LIFT_CREDIT,
            minuend=LIFT_MAXIMUM_CREDIT,
            minuend_amount=D("875"),
            subtrahend=LIFT_REDUCTION,
            subtrahend_amount=D("4125.00"),
            result=D("0"),
        ),
        # ON428 line 86 "Line 84 minus line 85 (if negative, enter "0")".
        ONTARIO_TAX_AFTER_LIFT_CREDIT: SubtractedNotBelowZeroLine(
            output=ONTARIO_TAX_AFTER_LIFT_CREDIT,
            minuend=ONTARIO_TAX_AFTER_REDUCTION,
            minuend_amount=D("8195.7699076"),
            subtrahend=LIFT_CREDIT,
            subtrahend_amount=D("0"),
            result=D("8195.7699076"),
        ),
        # Schedule 6 line 28 "Line 22 minus line 27 (if negative, enter "0")": the reduction of
        # 13221.75 exceeds the 1633, so the benefit (T1 line 45300) is 0.
        CANADA_WORKERS_BENEFIT: SubtractedNotBelowZeroLine(
            output=CANADA_WORKERS_BENEFIT,
            minuend=CWB_BEFORE_REDUCTION,
            minuend_amount=D("1633"),
            subtrahend=CWB_REDUCTION,
            subtrahend_amount=D("13221.75"),
            result=D("0"),
        ),
    }

    assert totals[FEDERAL_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[FEDERAL_BASIC_TAX].base_amount == D("115000")
    assert totals[FEDERAL_BASIC_TAX].amount == D("20146.25")
    assert totals[ONTARIO_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[ONTARIO_BASIC_TAX].amount == D("8539.60")
    # One line per tax for the bracket column the taxable income falls in, read like the form:
    # T1 lines 71 to 76 and ON428 lines 3 to 8.
    columns = [line for line in trace if isinstance(line, BracketColumnLine)]
    assert len(columns) == 2
    assert set(columns) == {
        BracketColumnLine(
            lower=D("114750"),
            rate=D("0.26"),
            excess=D("250"),
            tax_at_start=D("20081.25"),
            tax=D("20146.25"),
        ),
        BracketColumnLine(
            lower=D("105775"),
            rate=D("0.1116"),
            excess=D("9225"),
            tax_at_start=D("7510.09"),
            tax=D("8539.60"),
        ),
    }


def test_each_capability_runs_after_what_it_consumes() -> None:
    order = service().compose(CA_ON, 2025).order

    assert len(order) == 57
    position = {kind: i for i, capability in enumerate(order) for kind in capability.produces}
    assert position[TAXABLE_CAPITAL_GAINS] < position[TOTAL_INCOME] < position[NET_INCOME]
    assert position[DEDUCTIONS_FROM_TOTAL_INCOME] < position[NET_INCOME]
    assert position[RRSP_CONTRIBUTIONS_AVAILABLE] < position[RRSP_DEDUCTION_MAXIMUM]
    assert position[RRSP_DEDUCTION_MAXIMUM] < position[RRSP_DEDUCTION]
    assert position[RRSP_DEDUCTION] < position[UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD]
    assert position[RRSP_DEDUCTION] < position[DEDUCTIONS_FROM_TOTAL_INCOME]
    assert position[CPP_FIRST_ADDITIONAL_CONTRIBUTIONS] < position[CPP_ENHANCED_CONTRIBUTIONS]
    assert position[CPP_SECOND_ADDITIONAL_CONTRIBUTIONS] < position[CPP_ENHANCED_CONTRIBUTIONS]
    assert position[CPP_ENHANCED_CONTRIBUTIONS] < position[DEDUCTIONS_FROM_TOTAL_INCOME]
    assert position[CPP_BASE_CONTRIBUTIONS] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert position[CPP_BASE_CONTRIBUTIONS] < position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert position[EI_PREMIUMS] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert position[EI_PREMIUMS] < position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert position[NET_INCOME] < position[TAXABLE_INCOME]
    assert position[DEDUCTIONS_FROM_NET_INCOME] < position[TAXABLE_INCOME]
    assert position[TAXABLE_INCOME] < position[FEDERAL_BASIC_TAX]
    assert position[TAXABLE_INCOME] < position[ONTARIO_BASIC_TAX]
    assert position[FEDERAL_BASIC_TAX] < position[FEDERAL_TAX_AFTER_CREDITS]
    assert position[ONTARIO_BASIC_TAX] < position[ONTARIO_TAX_AFTER_CREDITS]
    assert position[NET_INCOME] < position[BASIC_PERSONAL_AMOUNT]
    assert position[BASIC_PERSONAL_AMOUNT] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert position[CANADA_EMPLOYMENT_AMOUNT] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert (
        position[BASIC_PERSONAL_AMOUNT]
        < position[ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT]
        < position[ELIGIBLE_DEPENDANT_AMOUNT]
        < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    )
    assert position[INFIRM_CHILDREN_AMOUNT] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert (
        position[ELIGIBLE_DEPENDANT_BASE]
        < position[ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM]
        < position[ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT]
        < position[ontario.ELIGIBLE_DEPENDANT_AMOUNT]
        < position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
    )
    assert position[NON_REFUNDABLE_CREDIT_AMOUNTS] < position[NON_REFUNDABLE_TAX_CREDITS]
    assert position[NON_REFUNDABLE_TAX_CREDITS] < position[FEDERAL_TAX_AFTER_CREDITS]
    assert position[ontario.BASIC_PERSONAL_AMOUNT] < position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert (
        position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
        < position[ontario.NON_REFUNDABLE_TAX_CREDITS]
        < position[ONTARIO_TAX_AFTER_CREDITS]
    )
    assert (
        position[ONTARIO_TAX_AFTER_CREDITS]
        < position[ONTARIO_SURTAX]
        < position[ONTARIO_TAX_WITH_SURTAX]
    )
    assert position[TAX_REDUCTION_BASIC] < position[TAX_REDUCTION_AMOUNTS]
    assert position[TAX_REDUCTION_FOR_CHILDREN] < position[TAX_REDUCTION_AMOUNTS]
    assert position[TAX_REDUCTION_FOR_DEPENDANTS] < position[TAX_REDUCTION_AMOUNTS]
    assert position[TAX_REDUCTION_AMOUNTS] < position[ONTARIO_TAX_REDUCTION]
    assert (
        position[ONTARIO_TAX_WITH_SURTAX]
        < position[ONTARIO_TAX_REDUCTION]
        < position[ONTARIO_TAX_AFTER_REDUCTION]
        < position[ONTARIO_TAX]
    )
    assert position[TAXABLE_INCOME] < position[ONTARIO_HEALTH_PREMIUM] < position[ONTARIO_TAX]
    assert position[LIFT_CREDIT_BEFORE_MAXIMUM] < position[LIFT_MAXIMUM_CREDIT]
    assert position[NET_INCOME] < position[LIFT_REDUCTION]
    assert position[LIFT_MAXIMUM_CREDIT] < position[LIFT_CREDIT]
    assert position[LIFT_REDUCTION] < position[LIFT_CREDIT]
    assert position[LIFT_CREDIT] < position[ONTARIO_TAX_AFTER_LIFT_CREDIT] < position[ONTARIO_TAX]
    assert position[ONTARIO_TAX_AFTER_REDUCTION] < position[ONTARIO_TAX_AFTER_LIFT_CREDIT]
    assert position[FEDERAL_TAX_AFTER_CREDITS] < position[NET_FEDERAL_TAX]
    assert position[NET_FEDERAL_TAX] < position[TOTAL_PAYABLE]
    assert position[ONTARIO_TAX] < position[TOTAL_PAYABLE]
    assert position[TOTAL_PAYABLE] < position[REFUND_OR_BALANCE_OWING]
    assert position[TOTAL_CREDITS] < position[REFUND_OR_BALANCE_OWING]
    assert position[WORKING_INCOME] < position[CWB_BEFORE_REDUCTION]
    assert position[NET_INCOME] < position[ADJUSTED_FAMILY_NET_INCOME] < position[CWB_REDUCTION]
    assert position[CWB_BEFORE_REDUCTION] < position[CANADA_WORKERS_BENEFIT]
    assert position[CWB_REDUCTION] < position[CANADA_WORKERS_BENEFIT] < position[TOTAL_CREDITS]


def test_a_credit_larger_than_the_tax_leaves_zero_not_a_refund() -> None:
    # Employment income of 10000, with the CPP contributions computed by Schedule 8's tiers:
    # base 4.95% x (10000 - 3500) = 321.75, first additional 1% x 6500 = 65.00, no second
    # additional, so enhanced 65.00; the EI premiums computed from employment income, 1.64% x
    # 10000 = 164.00; no unused or new RRSP contributions, so the most that may be deducted is
    # the lesser of 0 and the deduction limit of 1800, and the amount deducted is 0; the Canada
    # employment amount is the lesser of 10000 and 1471.
    worksheet = compute("10000", "0", "0", "0", "1800", "0", "0")

    assert worksheet.get(TOTAL_INCOME).value == D("10000")
    assert worksheet.get(CPP_BASE_CONTRIBUTIONS).value == D("321.75")
    assert worksheet.get(CPP_FIRST_ADDITIONAL_CONTRIBUTIONS).value == D("65.00")
    assert worksheet.get(CPP_SECOND_ADDITIONAL_CONTRIBUTIONS).value == D("0")
    assert worksheet.get(CPP_ENHANCED_CONTRIBUTIONS).value == D("65.00")
    assert worksheet.get(EI_PREMIUMS).value == D("164.00")
    assert worksheet.get(RRSP_CONTRIBUTIONS_AVAILABLE).value == D("0")
    assert worksheet.get(RRSP_DEDUCTION_MAXIMUM).value == D("0")
    assert worksheet.get(RRSP_DEDUCTION).value == D("0")
    assert worksheet.get(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD).value == D("0")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("65.00")
    assert worksheet.get(NET_INCOME).value == D("9935.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("9935.00")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("1440.575")
    assert worksheet.get(CANADA_EMPLOYMENT_AMOUNT).value == D("1471")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("18085.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("13232.75")
    # 14.5% of 18085.75 and 5.05% of 13232.75: each larger than its basic tax.
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("2622.43375")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("668.253875")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("0")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("0")
    # A zero Ontario tax is below the first surtax threshold: no surtax.
    assert worksheet.get(ONTARIO_SURTAX).value == D("0")
    assert worksheet.get(ONTARIO_TAX_WITH_SURTAX).value == D("0")
    # ON428 line 80: twice the basic reduction of 294.00, less a tax of zero, is 588.00, all of
    # it unused; line 81 leaves zero, not a refund.
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("294.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("588.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("0")
    # Schedule ON428-A: line 5 is 5.05% x 10000 = 505.0000, below the $875 maximum, and net
    # income of 9935.00 is below the 32,500.00 threshold, so no reduction: the credit (ON428 line
    # 85) is 505.0000, more than the Ontario tax after the reduction of zero, so line 86 is zero.
    assert worksheet.get(LIFT_CREDIT_BEFORE_MAXIMUM).value == D("505.0000")
    assert worksheet.get(LIFT_MAXIMUM_CREDIT).value == D("505.0000")
    assert worksheet.get(LIFT_REDUCTION).value == D("0")
    assert worksheet.get(LIFT_CREDIT).value == D("505.0000")
    assert worksheet.get(ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("0")
    # A taxable income of 9935.00 is "$20,000 or less" on the health premium chart: no premium.
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("0")
    assert worksheet.get(ONTARIO_TAX).value == D("0")
    # Schedule 6: the working income is the employment income of 10000, and line 20 is (10000 -
    # 3000) x 27% = 1890.00, more than the $1,633 of line 21, so line 22 is 1633; the adjusted
    # family net income of 9935.00 is below the $26,855 of line 24, so no reduction: the benefit
    # (line 28, T1 line 45300) is 1633.
    assert worksheet.get(WORKING_INCOME).value == D("10000")
    assert worksheet.get(ADJUSTED_FAMILY_NET_INCOME).value == D("9935.00")
    assert worksheet.get(CWB_BEFORE_REDUCTION).value == D("1633")
    assert worksheet.get(CWB_REDUCTION).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("1633")
    # With no tax deducted, nothing is payable and the benefit is the only credit: line 167 is
    # 0 - 1633 = -1633, a refund.
    assert worksheet.get(NET_FEDERAL_TAX).value == D("0")
    assert worksheet.get(TOTAL_PAYABLE).value == D("0")
    assert worksheet.get(TOTAL_CREDITS).value == D("1633")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-1633")


def test_the_tax_reduction_lowers_a_tax_below_twice_the_reduction_amounts() -> None:
    # Employment income of 24000, with no capital gain, no RRSP contributions and no union dues:
    # base CPP contributions 4.95% x (24000 - 3500) = 1014.75, first additional 1% x 20500 =
    # 205.00, EI premiums 1.64% x 24000 = 393.60; net and taxable income 23795.00; Ontario basic
    # tax 5.05% x 23795.00 = 1201.6475 less the Ontario credits 5.05% x (12747 + 1014.75 +
    # 393.60 = 14155.35) = 714.845175 is 486.802325, below the first surtax threshold, so the
    # Ontario tax with surtax (ON428 line 73) is 486.802325. With no dependent children and no
    # dependants, line 78 is 2 x 294.00 = 588.00, and line 80 is 588.00 - 486.802325 =
    # 101.197675; line 81 is 486.802325 - 101.197675 = 385.604650.
    worksheet = compute("24000", "0", "0", "0", "4320", "0", "0")

    assert worksheet.get(ONTARIO_TAX_WITH_SURTAX).value == D("486.802325")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("294.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("101.197675")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("385.604650")


def test_dependent_children_and_dependants_raise_the_tax_reduction() -> None:
    # Return A's amounts with five dependent children (ON428 line 75, line 60969) and three
    # dependants (line 76, line 60970): line 75 is 5 x 544 = 2720, line 76 is 3 x 544 = 1632,
    # line 77 is 294.00 + 2720 + 1632 = 4646.00 and line 78 is 9292.00; line 80 is 9292.00 -
    # 8195.7699076 = 1096.2300924, and line 81 is 8195.7699076 - 1096.2300924 = 7099.5398152.
    worksheet = compute(
        "110000", "20000", "0", "1926", "19800", "1926", "2000", dependent_children=5, dependants=3
    )

    assert worksheet.get(DEPENDENT_CHILDREN).value == 5
    assert worksheet.get(DEPENDANTS).value == 3
    assert worksheet.get(TAX_REDUCTION_FOR_CHILDREN).value == D("2720")
    assert worksheet.get(TAX_REDUCTION_FOR_DEPENDANTS).value == D("1632")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("4646.00")
    assert worksheet.get(ONTARIO_TAX_WITH_SURTAX).value == D("8195.7699076")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("1096.2300924")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("7099.5398152")


def test_the_health_premium_in_a_sloped_row_adds_the_rate_to_the_plateau() -> None:
    # A capital gain of 74000 alone, with no employment income, no RRSP contributions and no
    # union dues: taxable income is half the gain, 37000, and the Ontario credits are 5.05% x
    # 12747 = 643.7235. ON428 line 89's chart, "more than $36,000 but not more than $38,500":
    # (37000 - 36000) x 6% + 300 = 360.00; the Ontario basic tax 5.05% x 37000 = 1868.50 less
    # the credits is 1224.7765, above 588.00, so no reduction, and line 90 is 1224.7765 +
    # 360.00 = 1584.7765.
    worksheet = compute("0", "74000", "0", "0", "0", "0", "0")

    assert worksheet.get(TAXABLE_INCOME).value == D("37000")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("1224.7765")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("360.00")
    assert worksheet.get(ONTARIO_TAX).value == D("1584.7765")


def test_the_health_premium_at_the_top_of_a_sloped_row_is_the_plateau() -> None:
    # A capital gain of 50000 alone: taxable income 25000, "more than $20,000 but not more than
    # $25,000": (25000 - 20000) x 6% = 300.00, the plateau itself; the Ontario basic tax 5.05%
    # x 25000 = 1262.50 less the credits of 643.7235 is 618.7765, above 588.00, so no
    # reduction, and line 90 is 618.7765 + 300.00 = 918.7765.
    worksheet = compute("0", "50000", "0", "0", "0", "0", "0")

    assert worksheet.get(TAXABLE_INCOME).value == D("25000")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("618.7765")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("300.00")
    assert worksheet.get(ONTARIO_TAX).value == D("918.7765")


def test_no_health_premium_at_the_first_threshold() -> None:
    # A capital gain of 40000 alone: taxable income 20000, "$20,000 or less", so no premium;
    # the Ontario basic tax 5.05% x 20000 = 1010.00 less the credits of 643.7235 is 366.2765,
    # below 588.00, so the reduction is 221.7235 and line 81 is 144.5530, which is line 90.
    worksheet = compute("0", "40000", "0", "0", "0", "0", "0")

    assert worksheet.get(TAXABLE_INCOME).value == D("20000")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("144.5530")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("0")
    assert worksheet.get(ONTARIO_TAX).value == D("144.5530")


def test_the_lift_credit_between_the_thresholds_is_reduced_and_comes_off_the_tax() -> None:
    # Employment income of 40000, with no capital gain, no RRSP contributions and no union dues:
    # base CPP contributions 4.95% x (40000 - 3500) = 1806.75, first additional 1% x 36500 =
    # 365.00, EI premiums 1.64% x 40000 = 656.00; net and taxable income 39635.00. Ontario basic
    # tax 5.05% x 39635.00 = 2001.567500 less the Ontario credits 5.05% x (12747 + 1806.75 +
    # 656.00 = 15209.75) = 768.092375 is 1233.475125, below the first surtax threshold and above
    # 588.00, so line 81 is 1233.475125. Schedule ON428-A: line 5 is 5.05% x 40000 = 2020.0000,
    # at most 875 (line 14); line 17 is 39635.00 - 32500 = 7135.00 and line 19 7135.00 x 5% =
    # 356.75; line 20 is 875 - 356.75 = 518.25 (ON428 line 85). Line 86 is 1233.475125 - 518.25
    # = 715.225125; the health premium on 39635.00, "more than $38,500 but not more than
    # $48,000", is 450, so line 90 is 715.225125 + 450 = 1165.225125.
    worksheet = compute("40000", "0", "0", "0", "7200", "0", "0")

    assert worksheet.get(NET_INCOME).value == D("39635.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("1233.475125")
    assert worksheet.get(LIFT_CREDIT_BEFORE_MAXIMUM).value == D("2020.0000")
    assert worksheet.get(LIFT_MAXIMUM_CREDIT).value == D("875")
    assert worksheet.get(LIFT_REDUCTION).value == D("356.75")
    assert worksheet.get(LIFT_CREDIT).value == D("518.25")
    assert worksheet.get(ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("715.225125")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("450")
    assert worksheet.get(ONTARIO_TAX).value == D("1165.225125")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "lift_credit: lift_maximum_credit 875 less lift_reduction 356.75, not below 0 = 518.25"
    ) in rendered
    assert (
        "ontario_tax_after_lift_credit: ontario_tax_after_reduction 1233.475125 "
        "less lift_credit 518.25, not below 0 = 715.225125"
    ) in rendered


def test_the_canada_workers_benefit_below_its_maximum_is_27_percent_over_3000() -> None:
    # Employment income of 8000, with no capital gain, no RRSP contributions and no union dues:
    # base CPP contributions 4.95% x (8000 - 3500) = 222.75, first additional 1% x 4500 = 45.00,
    # EI premiums 1.64% x 8000 = 131.20; net income 8000 - 45.00 = 7955.00. Each form's credits
    # exceed its tax, so nothing is payable. Schedule 6: the working income (line 5) is 8000,
    # line 18 is 8000 - 3000 = 5000 and line 20 5000 x 27% = 1350.00, less than the $1,633 of
    # line 21, so line 22 is 1350.00; the adjusted family net income (line 15) of 7955.00 is
    # below the $26,855 of line 24, so line 27 is 0 and line 28 (T1 line 45300) is 1350.00. With
    # no tax deducted, the total credits are 0 + 1350.00 and line 167 is 0 - 1350.00 = -1350.00,
    # a refund.
    worksheet = compute("8000", "0", "0", "0", "1440", "0", "0")

    assert worksheet.get(NET_INCOME).value == D("7955.00")
    assert worksheet.get(TOTAL_PAYABLE).value == D("0")
    assert worksheet.get(WORKING_INCOME).value == D("8000")
    assert worksheet.get(ADJUSTED_FAMILY_NET_INCOME).value == D("7955.00")
    assert worksheet.get(CWB_BEFORE_REDUCTION).value == D("1350.00")
    assert worksheet.get(CWB_REDUCTION).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("1350.00")
    assert worksheet.get(TOTAL_CREDITS).value == D("1350.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-1350.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "cwb_before_reduction: 27% of working_income 8000 over 3000, at most 1633 (no rounding)"
    ) in rendered
    assert (
        "canada_workers_benefit: cwb_before_reduction 1350 less cwb_reduction 0, not below 0 = 1350"
    ) in rendered


def test_tax_deducted_above_the_total_payable_is_a_refund() -> None:
    # Return A's amounts with 30000 of income tax deducted (T1 line 43700): line 167 is the total
    # payable of 25897.1508076 less the total credits of 30000, -4102.8491924, negative, so a
    # refund (line 48400), exact as the T1 states no rounding.
    worksheet = compute(
        "110000", "20000", "0", "1926", "19800", "1926", "2000", income_tax_deducted="30000"
    )

    assert worksheet.get(TOTAL_PAYABLE).value == D("25897.1508076")
    assert worksheet.get(TOTAL_CREDITS).value == D("30000")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-4102.8491924")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "refund_or_balance_owing: total_payable 25897.1508076 "
        "less total_credits 30000 = -4102.8491924"
    ) in rendered


def test_tax_deducted_equal_to_the_total_payable_leaves_no_balance() -> None:
    worksheet = compute(
        "110000", "20000", "0", "1926", "19800", "1926", "2000", income_tax_deducted="25897.1508076"
    )

    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("0")


def test_with_no_tax_payable_all_the_tax_deducted_is_refunded() -> None:
    # Employment income of 10000 leaves no federal and no Ontario tax and a Canada workers
    # benefit of 1633 (see the test of a credit larger than the tax), so the total payable is 0;
    # with 500 deducted, the total credits are 500 + 1633 = 2133 and line 167 is 0 - 2133 =
    # -2133, a refund of everything deducted and the benefit, not floored at zero.
    worksheet = compute("10000", "0", "0", "0", "1800", "0", "0", income_tax_deducted="500")

    assert worksheet.get(TOTAL_PAYABLE).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("1633")
    assert worksheet.get(TOTAL_CREDITS).value == D("2133")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-2133")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "total_credits: income_tax_deducted 500 + canada_workers_benefit 1633 = 2133"
    ) in rendered


def test_contributions_above_the_deduction_limit_deduct_the_limit() -> None:
    # Schedule 7 line 17 "Enter whichever is less: amount from line 13 or line 16.": Return A's
    # amounts with contributions of 25000, above the deduction limit of 19800, so the most that
    # may be deducted is the limit, and deducting all of it (line 18) makes it the deduction;
    # total deductions are 19800 + 2000 + 1074.00 = 22874.00. Line 23 carries 25000 - 19800 =
    # 5200 forward.
    worksheet = compute("110000", "20000", "0", "25000", "19800", "19800", "2000")

    assert worksheet.get(RRSP_DEDUCTION_MAXIMUM).value == D("19800")
    assert worksheet.get(RRSP_DEDUCTION).value == D("19800")
    assert worksheet.get(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD).value == D("5200")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("22874.00")
    assert worksheet.get(NET_INCOME).value == D("97126.00")


def test_unused_contributions_and_no_new_ones_still_deduct() -> None:
    # Schedule 7 line 5 "Line 1 plus line 4 ... Total contributions" and line 17 "Enter
    # whichever is less: amount from line 13 or line 16.": Return A's amounts with unused
    # contributions of 5000 from earlier years (line 1) and no new contributions (line 4), so
    # the contributions available to deduct (line 10) are 5000 + 0 = 5000, below the deduction
    # limit of 19800; all 5000 is deducted (line 18); total deductions are 5000 + 2000 + 1074.00
    # = 8074.00.
    worksheet = compute("110000", "20000", "5000", "0", "19800", "5000", "2000")

    assert worksheet.get(RRSP_CONTRIBUTIONS_AVAILABLE).value == D("5000")
    assert worksheet.get(RRSP_DEDUCTION_MAXIMUM).value == D("5000")
    assert worksheet.get(RRSP_DEDUCTION).value == D("5000")
    assert worksheet.get(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD).value == D("0")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("8074.00")
    assert worksheet.get(NET_INCOME).value == D("111926.00")


def test_a_claim_below_the_maximum_deducts_the_claim_and_carries_the_rest_forward() -> None:
    # Schedule 7 line 18 "Enter your RRSP, PRPP, or SPP contributions you are deducting for 2025
    # (cannot be more than the amount on line 17).": Return A's amounts deducting 1000 of the
    # 1926 that line 17 allows, so the deduction (line 20) is 1000, and line 23 "Line 21 minus
    # line 22 Your unused contributions available to carry forward to a future year" is 1926 -
    # 1000 = 926. Total deductions are 1000 + 2000 + 1074.00 = 4074.00, and net income
    # 120000 - 4074.00 = 115926.00.
    worksheet = compute("110000", "20000", "0", "1926", "19800", "1000", "2000")

    assert worksheet.get(RRSP_DEDUCTION_MAXIMUM).value == D("1926")
    assert worksheet.get(RRSP_DEDUCTION).value == D("1000")
    assert worksheet.get(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD).value == D("926")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("4074.00")
    assert worksheet.get(NET_INCOME).value == D("115926.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert "rrsp_deduction: rrsp_amount_deducted 1000, at most rrsp_deduction_maximum 1926" in (
        rendered
    )
    assert (
        "unused_rrsp_contributions_carried_forward: rrsp_contributions_available 1926 "
        "less rrsp_deduction 1000 = 926"
    ) in rendered


def test_a_claim_above_the_maximum_is_refused_naming_both_kinds() -> None:
    # Line 18 "cannot be more than the amount on line 17": Return A's amounts claiming 3000
    # against a line 17 of 1926 is an input error, not capped to 1926.
    with pytest.raises(InputAboveBoundError) as raised:
        compute("110000", "20000", "0", "1926", "19800", "3000", "2000")

    assert str(raised.value) == (
        "ca/rrsp_amount_deducted 3000 is above ca/rrsp_deduction_maximum 1926"
    )


def test_an_eligible_dependant_with_no_income_adds_the_basic_personal_amount_and_10823() -> None:
    # Return F: employment income of 60000, one dependent child who is an eligible dependant with
    # no net income. Schedule 5 line 5 is its line 30000 of 16129.00 less 0, claimed for 1
    # eligible dependant: line 30400 is 16129.00. ON428 line 16 is 11905.00 less 0, at most
    # 10823: line 58160 is 10823. Line 33500 is 16129 + 16129.00 + 0 + 2796.75 + 984.00 + 1471 =
    # 37509.75, and line 35000 37509.75 x 14.5% = 5438.91375, so the federal tax after credits
    # is 8741.68 - 5438.91375 = 3302.76625. ON428 line 58800 is 12747 + 10823 + 2796.75 + 984.00
    # = 27350.75, and line 61500 27350.75 x 5.05% = 1381.212875, so the Ontario tax after
    # credits is 3269.9735 - 1381.212875 = 1888.760625. The child is a dependent child for the
    # Ontario tax reduction: 294.00 + 544 = 838.00, twice it 1676.00, below 1888.760625, so no
    # reduction. With the health premium of 600 the Ontario tax is 2488.760625, the total
    # payable 3302.76625 + 2488.760625 = 5791.526875, and line 167 5791.526875 - 8000 =
    # -2208.473125, a refund.
    worksheet = return_f()

    assert worksheet.get(NET_INCOME).value == D("59435.00")
    assert worksheet.get(BASIC_PERSONAL_AMOUNT).value == D("16129.00")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("16129.00")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT).value == D("16129.00")
    assert worksheet.get(INFIRM_CHILDREN_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("37509.75")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("5438.91375")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("3302.76625")
    assert worksheet.get(ELIGIBLE_DEPENDANT_BASE).value == D("11905.00")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM).value == D("11905.00")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("10823")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("10823")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("27350.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("1381.212875")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("1888.760625")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("838.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("0")
    assert worksheet.get(ONTARIO_TAX).value == D("2488.760625")
    assert worksheet.get(TOTAL_PAYABLE).value == D("5791.526875")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-2208.473125")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "eligible_dependant_amount: eligible_dependant_amount_before_count 16129 "
        "for each of 1 eligible_dependants = 16129"
    ) in rendered
    assert (
        "eligible_dependant_amount: eligible_dependant_amount_before_count 10823 "
        "for each of 1 eligible_dependants = 10823"
    ) in rendered
    assert (
        "non_refundable_credit_amounts: basic_personal_amount 16129 "
        "+ eligible_dependant_amount 16129 + infirm_children_amount 0 "
        "+ cpp_base_contributions 2796.75 + ei_premiums 984 "
        "+ canada_employment_amount 1471 = 37509.75"
    ) in rendered
    assert (
        "non_refundable_credit_amounts: basic_personal_amount 12747 "
        "+ eligible_dependant_amount 10823 "
        "+ cpp_base_contributions 2796.75 + ei_premiums 984 = 27350.75"
    ) in rendered


def test_the_dependants_net_income_comes_off_both_amounts() -> None:
    # Return F's amounts with a dependant's net income of 1500 (Schedule 5 line 4, ON428 line
    # 15): line 5 is 16129.00 - 1500 = 14629.00, and ON428 line 16 is 11905.00 - 1500 =
    # 10405.00, below the $10,823 maximum, so kept. Line 33500 is 16129 + 14629.00 + 0 +
    # 2796.75 + 984.00 + 1471 = 36009.75; ON428 line 58800 is 12747 + 10405.00 + 2796.75 +
    # 984.00 = 26932.75.
    worksheet = return_f(dependant_net_income="1500")

    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT).value == D("14629.00")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("10405.00")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("10405.00")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("36009.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("26932.75")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "eligible_dependant_amount_before_count: basic_personal_amount 16129 "
        "less dependant_net_income 1500, not below 0 = 14629"
    ) in rendered
    assert (
        "eligible_dependant_amount_before_count: lesser of "
        "eligible_dependant_amount_before_maximum 10405 and 10823 (no rounding)"
    ) in rendered


def test_a_dependant_with_more_income_than_the_amounts_adds_nothing() -> None:
    # Schedule 5 line 5 and ON428 line 16 "(if negative, enter "0")": a dependant's net income
    # of 20000 is above both 16129.00 and 11905.00, so each amount is 0 and the totals are those
    # without a dependant: 16129 + 0 + 0 + 2796.75 + 984.00 + 1471 = 21380.75 and 12747 + 0 +
    # 2796.75 + 984.00 = 16527.75.
    worksheet = return_f(dependant_net_income="20000")

    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("0")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT).value == D("0")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM).value == D("0")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("21380.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("16527.75")


def test_no_eligible_dependant_claims_nothing_whatever_the_dependants_income() -> None:
    # Return F's amounts with no eligible dependant claimed for but a dependant's net income of
    # 1500 entered: Schedule 5 line 5 is still 14629.00, but line 30400 claims it for 0
    # eligible dependants, so it is 0, and so is line 58160.
    worksheet = return_f(dependant_net_income="1500", eligible_dependants=0)

    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("14629.00")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT).value == D("0")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("10405.00")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("21380.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("16527.75")


def test_infirm_children_add_2687_each_to_the_federal_amounts_only() -> None:
    # Return A's amounts with two infirm children (T1 line 30499): line 30500 is 2 x 2687 =
    # 5374, so line 33500 is 22033.58 + 5374 = 27407.58, line 35000 27407.58 x 14.5% =
    # 3974.0991, and the federal tax after credits 20146.25 - 3974.0991 = 16172.1509. ON428 has
    # no such line here (its caregiver amount, line 58185, is not triggered), so its total is
    # unchanged at 17180.58.
    worksheet = compute("110000", "20000", "0", "1926", "19800", "1926", "2000", infirm_children=2)

    assert worksheet.get(INFIRM_CHILDREN).value == 2
    assert worksheet.get(INFIRM_CHILDREN_AMOUNT).value == D("5374")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("27407.58")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("3974.0991")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("16172.1509")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("17180.58")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert "infirm_children_amount: 2687 for each of 2 infirm_children = 5374 (no rounding)" in (
        rendered
    )
