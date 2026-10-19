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
that RRSP deduction, union dues of 2000, the child care expenses deduction of 0 (T1 line 21400, Form
T778 line 7, the least of the basic limit of line 4, 0 x 8000 + 0 x 11000 + 0 x 5000
= 0, the 0 paid of line 5 and two-thirds of the earned income of line 6, the employment
income of 110000, 73333.33..., rounded half-up to the cent, 73333.33: 0) and the enhanced
contributions to net income 115000, less no deductions from net income to taxable income
115000, and from each basic personal
amount (16129 federal, the Federal Worksheet's taper on net income, here at or below
the 177882 threshold so not reduced; 12747 Ontario) plus each amount for an eligible
dependant (T1 line 30400, Schedule 5 line 5, the federal basic personal amount less the
dependant's net income of 0; ON428 line 58160, the 11905.00 base less it, at most 10823), claimed
for 0 eligible dependants and so 0, the base CPP contributions and the EI premiums, and federally
the amount for infirm children of 0 x 2687 (line 30500) and the Canada employment amount of 1471
(the lesser of employment income and 1471), through each total of credit amounts and each form's
non-refundable tax credits (T1 line 35000, ON428 line 61500) to each tax after credits, the Ontario
surtax on the Ontario tax after credits (ON428 lines 66 to 68) to the Ontario tax with surtax of
line 69, and with no dependent children and no dependants the Ontario tax reduction amounts of
294.00 (lines 74 to 77), twice them less the tax with surtax (line 73), not below zero, the Ontario
tax reduction of 0 (line 80), to the Ontario tax after the reduction (line 81); Schedule ON428-A's
LIFT credit, 5.05% of employment income, 5555, at most 875 (lines 5 and 14), less 5% of net income
over 32500, 4125 (line 19), not below zero, 0 (line 20, ON428 line 85), taken off the Ontario tax
after the reduction, not below zero (line 86); and the Ontario health premium on taxable income by
the chart of line 89, 750, added to it to the Ontario tax of line 90; and on the T1, the federal tax
after credits carried to the net federal tax (line 42000), added to the Ontario tax (line 42800) to
the total payable (line 43500); Schedule 6's Canada workers benefit, computed for each family
status, from the working income of 110000 (line 5, employment income), 27% of it over 3000 at most
1633 (line 22), less 15% of the adjusted family net income (line 15, net income) of 115000 over
26855, 13221.75 (line 27), not below zero, 0 (line 28), and with an eligible dependant 27% of the
working income at most 2813, less 15% of the adjusted family net income over 30639, 12654.15, not
below zero, 0, the count of 0 Schedule 6 eligible dependants (line 38100) choosing the first (T1
line 45300); less the total credits (line 48200), here the chosen income tax
deducted of 25000 (line 43700) plus that benefit, to the refund or balance owing (line 167),
897.15, positive so a balance owing; every line computed from a dataset rounded half-up to the
cent) are checked from the files under `returns/` by `test_worked_returns.py`, as are Returns B,
C, D, E and F; this module pins which capability produces each line, the order, and the trace that
explains them.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import Artifact
from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.at_most import AtMost
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.choose_by_count import ChooseByCount
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
from app.domain.parameters.fraction import Fraction
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import RoundingMode, RoundTo
from app.domain.parameters.taper import Taper
from app.domain.trace import (
    AtMostLine,
    BracketColumnLine,
    CappedAmountLine,
    ChosenByCountLine,
    ContributionTierLine,
    CreditAmountLine,
    FractionAppliedLine,
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
    CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
    CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
    CAPITAL_GAIN,
    CHILD_CARE_BASIC_LIMIT,
    CHILD_CARE_EARNED_INCOME,
    CHILD_CARE_EARNED_INCOME_LIMIT,
    CHILD_CARE_EXPENSES,
    CHILD_CARE_EXPENSES_PAID,
    CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
    CHILDREN_SEVEN_TO_SIXTEEN,
    CHILDREN_UNDER_SEVEN,
    CHILDREN_WITH_DISABILITY,
    CPP_BASE_CONTRIBUTIONS,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
    CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
    CWB_ELIGIBLE_DEPENDANTS,
    CWB_REDUCTION_WITH_DEPENDANT,
    CWB_REDUCTION_WITHOUT_DEPENDANT,
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
    PROVINCIAL_CREDITS,
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
    FERTILITY_CREDIT,
    FERTILITY_CREDIT_BEFORE_MAXIMUM,
    FERTILITY_EXPENSES,
    LIFT_CREDIT,
    LIFT_CREDIT_BEFORE_MAXIMUM,
    LIFT_MAXIMUM_CREDIT,
    LIFT_REDUCTION,
    ONTARIO_BASIC_TAX,
    ONTARIO_CREDITS,
    ONTARIO_CREDITS_SUBTOTAL,
    ONTARIO_HEALTH_PREMIUM,
    ONTARIO_SURTAX,
    ONTARIO_TAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_AFTER_LIFT_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
    ONTARIO_TAX_REDUCTION,
    ONTARIO_TAX_WITH_SURTAX,
    SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
    SENIORS_TRANSIT_CREDIT,
    SENIORS_TRANSIT_PAID,
    TAX_REDUCTION_AMOUNTS,
    TAX_REDUCTION_BASIC,
    TAX_REDUCTION_FOR_CHILDREN,
    TAX_REDUCTION_FOR_DEPENDANTS,
)
from app.main import build_tax_computation

D = Decimal
CA_ON = JurisdictionCode("CA-ON")
# Every amount computed from a rate, fraction, amount or chart on the forms is rounded half-up to
# the cent, each line being a dollars-and-cents box: Schedule 8 Part 3a lines 25 and 28 say "(in
# dollars and cents)", the EI premiums are in dollars and cents too, T4127's BPAF rounding footnote
# rounds the federal basic personal amount so, and every other line is so by the owner's decision.
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
    child_care_expenses_paid: str = "0",
    children_under_seven: int = 0,
    children_with_disability: int = 0,
    children_seven_to_sixteen: int = 0,
    cwb_eligible_dependants: int = 0,
    income_tax_deducted: str = "0",
    fertility_expenses: str = "0",
    seniors_transit_paid: str = "0",
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
        Artifact(CHILD_CARE_EXPENSES_PAID, D(child_care_expenses_paid)),
        Artifact(CHILDREN_UNDER_SEVEN, children_under_seven),
        Artifact(CHILDREN_WITH_DISABILITY, children_with_disability),
        Artifact(CHILDREN_SEVEN_TO_SIXTEEN, children_seven_to_sixteen),
        Artifact(CWB_ELIGIBLE_DEPENDANTS, cwb_eligible_dependants),
        Artifact(INCOME_TAX_DEDUCTED, D(income_tax_deducted)),
        Artifact(FERTILITY_EXPENSES, D(fertility_expenses)),
        Artifact(SENIORS_TRANSIT_PAID, D(seniors_transit_paid)),
    )


def return_a() -> Worksheet:
    """Return A's inputs, as in `returns/2025_return_a.yaml`, with its chosen tax deducted."""
    return compute(
        "110000", "20000", "0", "1926", "19800", "1926", "2000", income_tax_deducted="25000"
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
    assert worksheet.producer_of(CHILD_CARE_EXPENSES_PAID) is None
    assert worksheet.producer_of(CHILDREN_UNDER_SEVEN) is None
    assert worksheet.producer_of(CHILDREN_WITH_DISABILITY) is None
    assert worksheet.producer_of(CHILDREN_SEVEN_TO_SIXTEEN) is None
    assert worksheet.producer_of(CWB_ELIGIBLE_DEPENDANTS) is None
    assert worksheet.producer_of(INCOME_TAX_DEDUCTED) is None
    assert worksheet.producer_of(FERTILITY_EXPENSES) is None
    assert worksheet.producer_of(SENIORS_TRANSIT_PAID) is None
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
    # Form T778 Part B lines 1 to 3, line 4, line 6 and line 7 (T1 line 21400).
    child_care_limits = {
        worksheet.producer_of(kind)
        for kind in (
            CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
            CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
            CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
        )
    }
    assert len(child_care_limits) == 3
    assert all(isinstance(producer, PerUnitAmount) for producer in child_care_limits)
    assert isinstance(worksheet.producer_of(CHILD_CARE_BASIC_LIMIT), Sum)
    assert isinstance(worksheet.producer_of(CHILD_CARE_EARNED_INCOME), Sum)
    assert worksheet.producer_of(CHILD_CARE_EARNED_INCOME) is not worksheet.producer_of(
        WORKING_INCOME
    )
    assert isinstance(worksheet.producer_of(CHILD_CARE_EARNED_INCOME_LIMIT), ApplyFraction)
    assert isinstance(worksheet.producer_of(CHILD_CARE_EXPENSES), LesserOf)
    assert worksheet.producer_of(CHILD_CARE_EXPENSES) is not worksheet.producer_of(
        RRSP_DEDUCTION_MAXIMUM
    )
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
    # Schedule 6 lines 22, 27 and 28, once for each family status, and the count's choice.
    cwb_lines = (
        CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
        CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
        CWB_REDUCTION_WITHOUT_DEPENDANT,
        CWB_REDUCTION_WITH_DEPENDANT,
    )
    for kind in cwb_lines:
        assert isinstance(worksheet.producer_of(kind), TieredSurcharge)
    assert len({id(worksheet.producer_of(kind)) for kind in cwb_lines}) == 4
    assert worksheet.producer_of(CWB_REDUCTION_WITHOUT_DEPENDANT) is not worksheet.producer_of(
        LIFT_REDUCTION
    )
    for kind in (CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT, CANADA_WORKERS_BENEFIT_WITH_DEPENDANT):
        assert isinstance(worksheet.producer_of(kind), SubtractNotBelowZero)
        assert worksheet.producer_of(kind) is not worksheet.producer_of(LIFT_CREDIT)
    assert worksheet.producer_of(
        CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT
    ) is not worksheet.producer_of(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT)
    assert isinstance(worksheet.producer_of(CANADA_WORKERS_BENEFIT), ChooseByCount)
    # ON479 line 1 (the rate, then the maximum on the credit), line 14 (the maximum on the amount
    # paid, then the rate), lines 18 and 21 and T1 line 47900.
    assert isinstance(worksheet.producer_of(FERTILITY_CREDIT_BEFORE_MAXIMUM), ApplyRate)
    assert isinstance(worksheet.producer_of(FERTILITY_CREDIT), CappedAmount)
    assert isinstance(
        worksheet.producer_of(SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM), CappedAmount
    )
    assert isinstance(worksheet.producer_of(SENIORS_TRANSIT_CREDIT), ApplyRate)
    assert worksheet.producer_of(FERTILITY_CREDIT_BEFORE_MAXIMUM) is not worksheet.producer_of(
        SENIORS_TRANSIT_CREDIT
    )
    assert worksheet.producer_of(FERTILITY_CREDIT) is not worksheet.producer_of(
        SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM
    )
    assert isinstance(worksheet.producer_of(ONTARIO_CREDITS_SUBTOTAL), Sum)
    assert isinstance(worksheet.producer_of(ONTARIO_CREDITS), Sum)
    assert isinstance(worksheet.producer_of(PROVINCIAL_CREDITS), Sum)
    assert (
        len(
            {
                id(worksheet.producer_of(kind))
                for kind in (
                    ONTARIO_CREDITS_SUBTOTAL,
                    ONTARIO_CREDITS,
                    PROVINCIAL_CREDITS,
                    TOTAL_CREDITS,
                )
            }
        )
        == 4
    )
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
        "taxable_capital_gains: 50% of capital_gain 20000 (half-up to 0.01)", "10000"
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
    # Form T778 Part B lines 1 to 3 for no eligible children, line 4, line 6 two-thirds of the
    # employment income, and line 7 the least of lines 4, 5 and 6.
    child_care_under_seven = position(
        "child_care_limit_for_children_under_seven: 8000 for each of 0 children_under_seven "
        "= 0 (half-up to 0.01)",
        "0",
    )
    child_care_disability = position(
        "child_care_limit_for_children_with_disability: 11000 for each of 0 "
        "children_with_disability = 0 (half-up to 0.01)",
        "0",
    )
    child_care_seven_to_sixteen = position(
        "child_care_limit_for_children_seven_to_sixteen: 5000 for each of 0 "
        "children_seven_to_sixteen = 0 (half-up to 0.01)",
        "0",
    )
    child_care_basic = position(
        "child_care_basic_limit: child_care_limit_for_children_under_seven 0 "
        "+ child_care_limit_for_children_with_disability 0 "
        "+ child_care_limit_for_children_seven_to_sixteen 0 = 0",
        "0",
    )
    child_care_earned = position(
        "child_care_earned_income: employment_income 110000 = 110000", "110000"
    )
    child_care_earned_limit = position(
        "child_care_earned_income_limit: 2/3 of child_care_earned_income 110000 (half-up to 0.01)",
        "73333.33",
    )
    child_care = position(
        "child_care_expenses: lesser of child_care_basic_limit 0 and child_care_expenses_paid 0 "
        "and child_care_earned_income_limit 73333.33 = 0",
        "0",
    )
    deductions = position(
        "deductions_from_total_income: rrsp_deduction 1926 + union_dues 2000 "
        "+ child_care_expenses 0 + cpp_enhanced_contributions 1074 = 5000",
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
    federal_basic = position(
        "federal_basic_tax on taxable_income 115000 (half-up to 0.01)", "20146.25"
    )
    federal_amount = position(
        "basic_personal_amount: 14538 plus 1591 less 0 for net_income 115000 over 177882 "
        "(range 75532), not below 14538 (half-up to 0.01)",
        "16129",
    )
    employment_amount = position(
        "canada_employment_amount: lesser of employment_income 110000 and 1471 (half-up to 0.01)",
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
        "infirm_children_amount: 2687 for each of 0 infirm_children = 0 (half-up to 0.01)", "0"
    )
    federal_amounts = position(
        "non_refundable_credit_amounts: basic_personal_amount 16129 "
        "+ eligible_dependant_amount 0 + infirm_children_amount 0 "
        "+ cpp_base_contributions 3356.1 + ei_premiums 1077.48 "
        "+ canada_employment_amount 1471 = 22033.58",
        "22033.58",
    )
    federal_credit = position(
        "non_refundable_tax_credits: 14.5% of non_refundable_credit_amounts 22033.58 "
        "(half-up to 0.01)",
        "3194.87",
    )
    federal_after = position(
        "federal_tax_after_credits: federal_basic_tax 20146.25 "
        "less non_refundable_tax_credits 3194.87, not below 0 = 16951.38",
        "16951.38",
    )
    # ON428 Part A, the column "more than $105,775 but not more than $150,000": line 4 is
    # 115000 - 105775 = 9225, line 6 is 11.16% of it, 1029.51, and line 8 adds line 7's 7,510.09.
    ontario_column = position("11.16% on 9225 over 105775 plus 7510.09", "8539.60")
    ontario_basic = position(
        "ontario_basic_tax on taxable_income 115000 (half-up to 0.01)", "8539.60"
    )
    ontario_amount = position(
        "basic_personal_amount: credit amount 12747 (half-up to 0.01)", "12747"
    )
    # ON428 lines 14 to 16 (line 58160), for 0 eligible dependants.
    ontario_base = position(
        "eligible_dependant_base: credit amount 11905 (half-up to 0.01)", "11905"
    )
    ontario_before_maximum = position(
        "eligible_dependant_amount_before_maximum: eligible_dependant_base 11905 "
        "less dependant_net_income 0, not below 0 = 11905",
        "11905",
    )
    ontario_dependant = position(
        "eligible_dependant_amount_before_count: lesser of "
        "eligible_dependant_amount_before_maximum 11905 and 10823 (half-up to 0.01)",
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
        "non_refundable_tax_credits: 5.05% of non_refundable_credit_amounts 17180.58 "
        "(half-up to 0.01)",
        "867.62",
    )
    ontario_after = position(
        "ontario_tax_after_credits: ontario_basic_tax 8539.6 "
        "less non_refundable_tax_credits 867.62, not below 0 = 7671.98",
        "7671.98",
    )
    surtax_first = position(
        "ontario_surtax: 20% of ontario_tax_after_credits 7671.98 over 5710 (half-up to 0.01)",
        "392.40",
    )
    surtax_second = position(
        "ontario_surtax: 36% of ontario_tax_after_credits 7671.98 over 7307 (half-up to 0.01)",
        "131.39",
    )
    with_surtax = position(
        "ontario_tax_with_surtax: ontario_tax_after_credits 7671.98 "
        "+ ontario_surtax 523.79 = 8195.77",
        "8195.77",
    )
    reduction_basic = position(
        "tax_reduction_basic: credit amount 294 (half-up to 0.01)",
        "294.00",
    )
    reduction_children = position(
        "tax_reduction_for_children: 544 for each of 0 dependent_children = 0 (half-up to 0.01)",
        "0",
    )
    reduction_dependants = position(
        "tax_reduction_for_dependants: 544 for each of 0 dependants = 0 (half-up to 0.01)",
        "0",
    )
    reduction_amounts = position(
        "tax_reduction_amounts: tax_reduction_basic 294 + tax_reduction_for_children 0 "
        "+ tax_reduction_for_dependants 0 = 294",
        "294.00",
    )
    reduction = position(
        "ontario_tax_reduction: 2 × tax_reduction_amounts 294 "
        "over ontario_tax_with_surtax 8195.77, not below 0 (half-up to 0.01)",
        "0",
    )
    after_reduction = position(
        "ontario_tax_after_reduction: ontario_tax_with_surtax 8195.77 "
        "less ontario_tax_reduction 0, not below 0 = 8195.77",
        "8195.77",
    )
    lift_before_maximum = position(
        "lift_credit_before_maximum: 5.05% of employment_income 110000 (half-up to 0.01)", "5555"
    )
    lift_maximum = position(
        "lift_maximum_credit: lesser of lift_credit_before_maximum 5555 and 875 (half-up to 0.01)",
        "875",
    )
    lift_reduction = position(
        "lift_reduction: 5% of net_income 115000 over 32500 (half-up to 0.01)", "4125"
    )
    lift = position(
        "lift_credit: lift_maximum_credit 875 less lift_reduction 4125, not below 0 = 0", "0"
    )
    after_lift = position(
        "ontario_tax_after_lift_credit: ontario_tax_after_reduction 8195.77 "
        "less lift_credit 0, not below 0 = 8195.77",
        "8195.77",
    )
    premium_first = position(
        "ontario_health_premium: 6% of taxable_income 115000 over 20000, at most 300 "
        "(half-up to 0.01)",
        "300",
    )
    premium_second = position(
        "ontario_health_premium: 6% of taxable_income 115000 over 36000, at most 150 "
        "(half-up to 0.01)",
        "150",
    )
    premium_third = position(
        "ontario_health_premium: 25% of taxable_income 115000 over 48000, at most 150 "
        "(half-up to 0.01)",
        "150",
    )
    premium_fourth = position(
        "ontario_health_premium: 25% of taxable_income 115000 over 72000, at most 150 "
        "(half-up to 0.01)",
        "150",
    )
    premium_fifth = position(
        "ontario_health_premium: 25% of taxable_income 115000 over 200000, at most 150 "
        "(half-up to 0.01)",
        "0",
    )
    ontario_tax = position(
        "ontario_tax: ontario_tax_after_lift_credit 8195.77 + ontario_health_premium 750 = 8945.77",
        "8945.77",
    )
    net_federal = position(
        "net_federal_tax: federal_tax_after_credits 16951.38 = 16951.38", "16951.38"
    )
    payable = position(
        "total_payable: net_federal_tax 16951.38 + ontario_tax 8945.77 = 25897.15",
        "25897.15",
    )
    working = position("working_income: employment_income 110000 = 110000", "110000")
    family_net = position("adjusted_family_net_income: net_income 115000 = 115000", "115000")
    cwb_before_reduction = position(
        "cwb_before_reduction_without_dependant: 27% of working_income 110000 over 3000, "
        "at most 1633 (half-up to 0.01)",
        "1633",
    )
    cwb_reduction = position(
        "cwb_reduction_without_dependant: 15% of adjusted_family_net_income 115000 over 26855 "
        "(half-up to 0.01)",
        "13221.75",
    )
    cwb_without = position(
        "canada_workers_benefit_without_dependant: cwb_before_reduction_without_dependant 1633 "
        "less cwb_reduction_without_dependant 13221.75, not below 0 = 0",
        "0",
    )
    cwb_before_reduction_dependant = position(
        "cwb_before_reduction_with_dependant: 27% of working_income 110000 over 3000, "
        "at most 2813 (half-up to 0.01)",
        "2813",
    )
    cwb_reduction_dependant = position(
        "cwb_reduction_with_dependant: 15% of adjusted_family_net_income 115000 over 30639 "
        "(half-up to 0.01)",
        "12654.15",
    )
    cwb_with = position(
        "canada_workers_benefit_with_dependant: cwb_before_reduction_with_dependant 2813 "
        "less cwb_reduction_with_dependant 12654.15, not below 0 = 0",
        "0",
    )
    cwb = position(
        "canada_workers_benefit: canada_workers_benefit_without_dependant 0, "
        "chosen as cwb_eligible_dependants is 0",
        "0",
    )
    fertility_before_maximum = position(
        "fertility_credit_before_maximum: 25% of fertility_expenses 0 (half-up to 0.01)", "0"
    )
    fertility = position(
        "fertility_credit: lesser of fertility_credit_before_maximum 0 and 5000 (half-up to 0.01)",
        "0",
    )
    transit_paid = position(
        "seniors_transit_amount_paid_at_most_maximum: lesser of seniors_transit_paid 0 and 3000 "
        "(half-up to 0.01)",
        "0",
    )
    transit = position(
        "seniors_transit_credit: 15% of seniors_transit_amount_paid_at_most_maximum 0 "
        "(half-up to 0.01)",
        "0",
    )
    ontario_credits_subtotal = position(
        "ontario_credits_subtotal: fertility_credit 0 + seniors_transit_credit 0 = 0", "0"
    )
    ontario_credits = position("ontario_credits: ontario_credits_subtotal 0 = 0", "0")
    provincial = position("provincial_credits: ontario_credits 0 = 0", "0")
    credits = position(
        "total_credits: income_tax_deducted 25000 + canada_workers_benefit 0 "
        "+ provincial_credits 0 = 25000",
        "25000",
    )
    balance = position(
        "refund_or_balance_owing: total_payable 25897.15 less total_credits 25000 = 897.15",
        "897.15",
    )
    assert taxable_gains < total < net
    assert cpp_first < cpp_enhanced < deductions < net
    assert rrsp_available < rrsp_maximum < rrsp < deductions
    assert rrsp < rrsp_carried
    assert child_care_under_seven < child_care_basic
    assert child_care_disability < child_care_basic
    assert child_care_seven_to_sixteen < child_care_basic < child_care
    assert child_care_earned < child_care_earned_limit < child_care < deductions
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
    assert working < cwb_before_reduction < cwb_without < cwb
    assert net < family_net < cwb_reduction < cwb_without
    assert working < cwb_before_reduction_dependant < cwb_with < cwb
    assert family_net < cwb_reduction_dependant < cwb_with
    assert fertility_before_maximum < fertility < ontario_credits_subtotal
    assert transit_paid < transit < ontario_credits_subtotal
    assert ontario_credits_subtotal < ontario_credits < provincial < credits
    assert cwb < credits
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
        if isinstance(line, SurchargeTierLine)
        and line.output
        in (CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT, CWB_BEFORE_REDUCTION_WITH_DEPENDANT)
    ]
    cwb_reduction_tiers = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine)
        and line.output in (CWB_REDUCTION_WITHOUT_DEPENDANT, CWB_REDUCTION_WITH_DEPENDANT)
    ]
    per_unit = {line.output: line for line in trace if isinstance(line, PerUnitAmountLine)}
    multiples = {line.output: line for line in trace if isinstance(line, MultipleOverLine)}
    times = {line.output: line for line in trace if isinstance(line, TimesCountLine)}
    fractions = {line.output: line for line in trace if isinstance(line, FractionAppliedLine)}
    chosen = {line.output: line for line in trace if isinstance(line, ChosenByCountLine)}

    # The rate is applied once, to each form's total of credit amounts (T1 line 33800, ON428
    # line 58840), giving its non-refundable tax credits (T1 line 35000, ON428 line 61500).
    assert rated == {
        TAXABLE_CAPITAL_GAINS: RateAppliedLine(
            TAXABLE_CAPITAL_GAINS, CAPITAL_GAIN, D("20000"), Rate(D("0.5")), CENT, D("10000")
        ),
        NON_REFUNDABLE_TAX_CREDITS: RateAppliedLine(
            NON_REFUNDABLE_TAX_CREDITS,
            NON_REFUNDABLE_CREDIT_AMOUNTS,
            D("22033.58"),
            Rate(D("0.145")),
            CENT,
            D("3194.87"),
        ),
        ontario.NON_REFUNDABLE_TAX_CREDITS: RateAppliedLine(
            ontario.NON_REFUNDABLE_TAX_CREDITS,
            ontario.NON_REFUNDABLE_CREDIT_AMOUNTS,
            D("17180.58"),
            Rate(D("0.0505")),
            CENT,
            D("867.62"),
        ),
        # ON479 line 1 "Eligible medical expenses for fertility treatment multiplied by 25%
        # (maximum $5,000)", before its maximum: no expenses.
        FERTILITY_CREDIT_BEFORE_MAXIMUM: RateAppliedLine(
            FERTILITY_CREDIT_BEFORE_MAXIMUM,
            FERTILITY_EXPENSES,
            D("0"),
            Rate(D("0.25")),
            CENT,
            D("0"),
        ),
        # ON479 line 14 "multiplied by 15%", on the amount paid after its maximum of $3,000.
        SENIORS_TRANSIT_CREDIT: RateAppliedLine(
            SENIORS_TRANSIT_CREDIT,
            SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
            D("0"),
            Rate(D("0.15")),
            CENT,
            D("0"),
        ),
        # Schedule ON428-A line 5 "Line 3 multiplied by the percentage from line 4 (maximum
        # $875)", before its maximum: line 3 is employment income (line 10100), as line 2 (line
        # 10400) is not triggered.
        LIFT_CREDIT_BEFORE_MAXIMUM: RateAppliedLine(
            LIFT_CREDIT_BEFORE_MAXIMUM,
            EMPLOYMENT_INCOME,
            D("110000"),
            Rate(D("0.0505")),
            CENT,
            D("5555.00"),
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
        # Form T778 line 4 "Add lines 1 to 3.", and line 6's earned income, the employment
        # income.
        CHILD_CARE_BASIC_LIMIT: SumLine(
            CHILD_CARE_BASIC_LIMIT,
            (
                (CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN, D("0")),
                (CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY, D("0")),
                (CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN, D("0")),
            ),
            D("0"),
        ),
        CHILD_CARE_EARNED_INCOME: SumLine(
            CHILD_CARE_EARNED_INCOME, ((EMPLOYMENT_INCOME, D("110000")),), D("110000")
        ),
        # T1 line 23300, in line order: 20800, 21200, 21400, 22215.
        DEDUCTIONS_FROM_TOTAL_INCOME: SumLine(
            DEDUCTIONS_FROM_TOTAL_INCOME,
            (
                (RRSP_DEDUCTION, D("1926")),
                (UNION_DUES, D("2000")),
                (CHILD_CARE_EXPENSES, D("0")),
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
            ((ONTARIO_TAX_AFTER_CREDITS, D("7671.98")), (ONTARIO_SURTAX, D("523.79"))),
            D("8195.77"),
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
                (ONTARIO_TAX_AFTER_LIFT_CREDIT, D("8195.77")),
                (ONTARIO_HEALTH_PREMIUM, D("750")),
            ),
            D("8945.77"),
        ),
        # T1 line 142 (line 42000) "Add lines 139 to 141. Net federal tax": line 139 carries the
        # federal tax after credits (line 126, 42900, through line 134, 40600), and lines 140
        # and 141 are not modelled.
        NET_FEDERAL_TAX: SumLine(
            NET_FEDERAL_TAX, ((FEDERAL_TAX_AFTER_CREDITS, D("16951.38")),), D("16951.38")
        ),
        # T1 line 148 (line 43500) "Add lines 143 to 147. Total payable", in line order: line
        # 143 "Amount from line 42000" and line 147 (42800), the Ontario tax.
        TOTAL_PAYABLE: SumLine(
            TOTAL_PAYABLE,
            ((NET_FEDERAL_TAX, D("16951.38")), (ONTARIO_TAX, D("8945.77"))),
            D("25897.15"),
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
        # ON479 line 18 "Add lines 1, 2, 13, 14, 16, and 17.": lines 1 and 14, in line order.
        ONTARIO_CREDITS_SUBTOTAL: SumLine(
            ONTARIO_CREDITS_SUBTOTAL,
            ((FERTILITY_CREDIT, D("0")), (SENIORS_TRANSIT_CREDIT, D("0"))),
            D("0"),
        ),
        # ON479 line 21 "Line 19 plus line 20": line 19 carries line 18, line 20 is not triggered.
        ONTARIO_CREDITS: SumLine(ONTARIO_CREDITS, ((ONTARIO_CREDITS_SUBTOTAL, D("0")),), D("0")),
        # T1 line 165 (line 47900) "Provincial or territorial credits": ON479 line 21.
        PROVINCIAL_CREDITS: SumLine(PROVINCIAL_CREDITS, ((ONTARIO_CREDITS, D("0")),), D("0")),
        # T1 line 166 (line 48200) "Add lines 150 to 165. Total credits": line 150 (43700), line
        # 155 (45300), the Canada workers benefit, and line 165 (47900), in line order.
        TOTAL_CREDITS: SumLine(
            TOTAL_CREDITS,
            (
                (INCOME_TAX_DEDUCTED, D("25000")),
                (CANADA_WORKERS_BENEFIT, D("0")),
                (PROVINCIAL_CREDITS, D("0")),
            ),
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
        # T1 line 167 "Line 149 minus line 166 ... Refund or balance owing": it takes amounts
        # already in cents, is not floored, and is positive here, so a balance owing (line 48500).
        REFUND_OR_BALANCE_OWING: SubtractedLine(
            output=REFUND_OR_BALANCE_OWING,
            minuend=TOTAL_PAYABLE,
            minuend_amount=D("25897.15"),
            subtrahend=TOTAL_CREDITS,
            subtrahend_amount=D("25000"),
            result=D("897.15"),
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
            ontario.BASIC_PERSONAL_AMOUNT, Credit(amount=D("12747")), CENT, D("12747")
        ),
        TAX_REDUCTION_BASIC: CreditAmountLine(
            TAX_REDUCTION_BASIC, Credit(amount=D("294.00")), CENT, D("294.00")
        ),
        # ON428 line 14 "Base amount 11,905.00".
        ELIGIBLE_DEPENDANT_BASE: CreditAmountLine(
            ELIGIBLE_DEPENDANT_BASE, Credit(amount=D("11905.00")), CENT, D("11905.00")
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
            rounding=CENT,
            result=D("0"),
        ),
        TAX_REDUCTION_FOR_DEPENDANTS: PerUnitAmountLine(
            output=TAX_REDUCTION_FOR_DEPENDANTS,
            count_kind=DEPENDANTS,
            count=0,
            per_unit=Amount(D("544")),
            rounding=CENT,
            result=D("0"),
        ),
        # T1 line 30500 "Number of children you are claiming this amount for Line 30499"
        # "multiplied by $2,687": Return A has no infirm child.
        INFIRM_CHILDREN_AMOUNT: PerUnitAmountLine(
            output=INFIRM_CHILDREN_AMOUNT,
            count_kind=INFIRM_CHILDREN,
            count=0,
            per_unit=Amount(D("2687")),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T778 Part B lines 1 to 3, "multiplied by $8,000", "$11,000" and "$5,000": Return A
        # has no eligible child.
        CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN: PerUnitAmountLine(
            output=CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
            count_kind=CHILDREN_UNDER_SEVEN,
            count=0,
            per_unit=Amount(D("8000")),
            rounding=CENT,
            result=D("0"),
        ),
        CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY: PerUnitAmountLine(
            output=CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
            count_kind=CHILDREN_WITH_DISABILITY,
            count=0,
            per_unit=Amount(D("11000")),
            rounding=CENT,
            result=D("0"),
        ),
        CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN: PerUnitAmountLine(
            output=CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
            count_kind=CHILDREN_SEVEN_TO_SIXTEEN,
            count=0,
            per_unit=Amount(D("5000")),
            rounding=CENT,
            result=D("0"),
        ),
    }
    # Form T778 line 6 "Enter your earned income." "multiplied by two-thirds": 220000 / 3,
    # rounded half-up to the cent.
    assert fractions == {
        CHILD_CARE_EARNED_INCOME_LIMIT: FractionAppliedLine(
            output=CHILD_CARE_EARNED_INCOME_LIMIT,
            base=CHILD_CARE_EARNED_INCOME,
            base_amount=D("110000"),
            fraction=Fraction(2, 3),
            rounding=CENT,
            result=D("73333.33"),
        )
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
    # 588.00 is below the tax with surtax of 8195.77, so the reduction is 0.
    assert multiples == {
        ONTARIO_TAX_REDUCTION: MultipleOverLine(
            output=ONTARIO_TAX_REDUCTION,
            base=TAX_REDUCTION_AMOUNTS,
            base_amount=D("294.00"),
            factor=Factor(D("2")),
            less=ONTARIO_TAX_WITH_SURTAX,
            less_amount=D("8195.77"),
            rounding=CENT,
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
            CENT,
            D("1471"),
        ),
        # Schedule ON428-A line 5's "(maximum $875)" and line 14 "Amount from line 5 above
        # (maximum $875)": 5555.00 is above it.
        LIFT_MAXIMUM_CREDIT: CappedAmountLine(
            LIFT_MAXIMUM_CREDIT,
            LIFT_CREDIT_BEFORE_MAXIMUM,
            D("5555.00"),
            Amount(D("875")),
            CENT,
            D("875"),
        ),
        # ON479 line 1's "(maximum $5,000)", printed after the percentage: it caps the credit.
        FERTILITY_CREDIT: CappedAmountLine(
            FERTILITY_CREDIT,
            FERTILITY_CREDIT_BEFORE_MAXIMUM,
            D("0"),
            Amount(D("5000")),
            CENT,
            D("0"),
        ),
        # ON479 line 14's "(maximum $3,000)", printed before the percentage: it caps the amount
        # paid.
        SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM: CappedAmountLine(
            SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
            SENIORS_TRANSIT_PAID,
            D("0"),
            Amount(D("3000")),
            CENT,
            D("0"),
        ),
        # ON428 line 16's "(maximum $10,823)": 11905.00 is above it.
        ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT: CappedAmountLine(
            ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
            ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
            D("11905.00"),
            Amount(D("10823")),
            CENT,
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
        ),
        # Form T778 line 7 "Enter whichever amount is the least: line 4, line 5 or line 6.", in
        # that order: lines 4 and 5 are both 0, and the first listed is produced.
        CHILD_CARE_EXPENSES: LesserOfLine(
            CHILD_CARE_EXPENSES,
            (
                (CHILD_CARE_BASIC_LIMIT, D("0")),
                (CHILD_CARE_EXPENSES_PAID, D("0")),
                (CHILD_CARE_EARNED_INCOME_LIMIT, D("73333.33")),
            ),
            D("0"),
        ),
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
    # the Ontario tax after credits (line 65, as line 64 is not modelled); each part rounded
    # half-up to the cent.
    assert surcharged == [
        SurchargeTierLine(
            output=ONTARIO_SURTAX,
            base=ONTARIO_TAX_AFTER_CREDITS,
            base_amount=D("7671.98"),
            threshold=D("5710"),
            rate=Rate(D("0.20")),
            rounding=CENT,
            part=D("392.40"),
        ),
        SurchargeTierLine(
            output=ONTARIO_SURTAX,
            base=ONTARIO_TAX_AFTER_CREDITS,
            base_amount=D("7671.98"),
            threshold=D("7307"),
            rate=Rate(D("0.36")),
            rounding=CENT,
            part=D("131.39"),
        ),
    ]
    # ON428 line 89 and its chart, on line 1 "Enter your taxable income from line 26000 of your
    # return", in threshold order: taxable income of 115000 is "more than $72,600 but not more
    # than $200,000", so the four lower tiers each charge their maximum, 300 + 150 + 150 + 150 =
    # 750, and the top tier nothing; each tier rounded half-up to the cent.
    assert premium_tiers == [
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("20000"),
            rate=Rate(D("0.06")),
            rounding=CENT,
            part=D("300"),
            maximum=D("300"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("36000"),
            rate=Rate(D("0.06")),
            rounding=CENT,
            part=D("150"),
            maximum=D("150"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("48000"),
            rate=Rate(D("0.25")),
            rounding=CENT,
            part=D("150"),
            maximum=D("150"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("72000"),
            rate=Rate(D("0.25")),
            rounding=CENT,
            part=D("150"),
            maximum=D("150"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("200000"),
            rate=Rate(D("0.25")),
            rounding=CENT,
            part=D("0"),
            maximum=D("150"),
        ),
    ]
    # Schedule ON428-A line 17 "Line 15 minus line 16 (if negative, enter "0")" and line 19 "Line
    # 17 multiplied by the percentage from line 18": net income (line 15, from line 13) of 115000
    # less the 32,500.00 threshold (line 16), times 5% (line 18), rounded half-up to the cent.
    assert lift_tiers == [
        SurchargeTierLine(
            output=LIFT_REDUCTION,
            base=NET_INCOME,
            base_amount=D("115000"),
            threshold=D("32500"),
            rate=Rate(D("0.05")),
            rounding=CENT,
            part=D("4125.00"),
        )
    ]
    # Schedule 6 line 18 "Line 16 minus line 17 (if negative, enter "0")", line 20 "Line 18
    # multiplied by the percentage from line 19" and line 22 "Enter whichever is less: amount from
    # line 20 or line 21.": (110000 - 3000) x 27% is above both of line 21's amounts, so line 22
    # is 1633 with no eligible spouse or dependant and 2813 with one, rounded half-up to the cent.
    assert set(cwb_basic_tiers) == {
        SurchargeTierLine(
            output=CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
            base=WORKING_INCOME,
            base_amount=D("110000"),
            threshold=D("3000"),
            rate=Rate(D("0.27")),
            rounding=CENT,
            part=D("1633"),
            maximum=D("1633"),
        ),
        SurchargeTierLine(
            output=CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
            base=WORKING_INCOME,
            base_amount=D("110000"),
            threshold=D("3000"),
            rate=Rate(D("0.27")),
            rounding=CENT,
            part=D("2813"),
            maximum=D("2813"),
        ),
    }
    assert len(cwb_basic_tiers) == 2
    # Schedule 6 line 25 "Line 23 minus line 24 (if negative, enter "0")" and line 27 "Line 25
    # multiplied by the percentage from line 26": (115000 - 26855) x 15% with no eligible spouse
    # or dependant and (115000 - 30639) x 15% with one, rounded half-up to the cent.
    assert set(cwb_reduction_tiers) == {
        SurchargeTierLine(
            output=CWB_REDUCTION_WITHOUT_DEPENDANT,
            base=ADJUSTED_FAMILY_NET_INCOME,
            base_amount=D("115000"),
            threshold=D("26855"),
            rate=Rate(D("0.15")),
            rounding=CENT,
            part=D("13221.75"),
        ),
        SurchargeTierLine(
            output=CWB_REDUCTION_WITH_DEPENDANT,
            base=ADJUSTED_FAMILY_NET_INCOME,
            base_amount=D("115000"),
            threshold=D("30639"),
            rate=Rate(D("0.15")),
            rounding=CENT,
            part=D("12654.15"),
        ),
    }
    assert len(cwb_reduction_tiers) == 2
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
            subtrahend_amount=D("3194.87"),
            result=D("16951.38"),
        ),
        ONTARIO_TAX_AFTER_CREDITS: SubtractedNotBelowZeroLine(
            output=ONTARIO_TAX_AFTER_CREDITS,
            minuend=ONTARIO_BASIC_TAX,
            minuend_amount=D("8539.60"),
            subtrahend=ontario.NON_REFUNDABLE_TAX_CREDITS,
            subtrahend_amount=D("867.62"),
            result=D("7671.98"),
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
            minuend_amount=D("8195.77"),
            subtrahend=ONTARIO_TAX_REDUCTION,
            subtrahend_amount=D("0"),
            result=D("8195.77"),
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
            minuend_amount=D("8195.77"),
            subtrahend=LIFT_CREDIT,
            subtrahend_amount=D("0"),
            result=D("8195.77"),
        ),
        # Schedule 6 line 28 "Line 22 minus line 27 (if negative, enter "0")": the reduction of
        # 13221.75 exceeds the 1633, and that of 12654.15 the 2813, so the benefit is 0 with or
        # without an eligible dependant.
        CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT: SubtractedNotBelowZeroLine(
            output=CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
            minuend=CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
            minuend_amount=D("1633"),
            subtrahend=CWB_REDUCTION_WITHOUT_DEPENDANT,
            subtrahend_amount=D("13221.75"),
            result=D("0"),
        ),
        CANADA_WORKERS_BENEFIT_WITH_DEPENDANT: SubtractedNotBelowZeroLine(
            output=CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
            minuend=CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
            minuend_amount=D("2813"),
            subtrahend=CWB_REDUCTION_WITH_DEPENDANT,
            subtrahend_amount=D("12654.15"),
            result=D("0"),
        ),
    }
    # T1 line 45300: Schedule 6 line 28 for Return A's family status, no eligible spouse and 0
    # Schedule 6 eligible dependants (line 38100), so the amounts with neither.
    assert chosen == {
        CANADA_WORKERS_BENEFIT: ChosenByCountLine(
            output=CANADA_WORKERS_BENEFIT,
            count_kind=CWB_ELIGIBLE_DEPENDANTS,
            count=0,
            chosen_kind=CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
            chosen_value=D("0"),
        )
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

    assert len(order) == 75
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
    for limit in (
        CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
        CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
        CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
    ):
        assert position[limit] < position[CHILD_CARE_BASIC_LIMIT]
    assert position[CHILD_CARE_BASIC_LIMIT] < position[CHILD_CARE_EXPENSES]
    assert (
        position[CHILD_CARE_EARNED_INCOME]
        < position[CHILD_CARE_EARNED_INCOME_LIMIT]
        < position[CHILD_CARE_EXPENSES]
        < position[DEDUCTIONS_FROM_TOTAL_INCOME]
    )
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
    for family_status in (
        (
            CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
            CWB_REDUCTION_WITHOUT_DEPENDANT,
            CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
        ),
        (
            CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
            CWB_REDUCTION_WITH_DEPENDANT,
            CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
        ),
    ):
        basic, reduction, benefit = family_status
        assert position[WORKING_INCOME] < position[basic] < position[benefit]
        assert position[NET_INCOME] < position[ADJUSTED_FAMILY_NET_INCOME] < position[reduction]
        assert position[reduction] < position[benefit] < position[CANADA_WORKERS_BENEFIT]
    assert position[CANADA_WORKERS_BENEFIT] < position[TOTAL_CREDITS]
    assert position[FERTILITY_CREDIT_BEFORE_MAXIMUM] < position[FERTILITY_CREDIT]
    assert position[SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM] < position[SENIORS_TRANSIT_CREDIT]
    assert position[FERTILITY_CREDIT] < position[ONTARIO_CREDITS_SUBTOTAL]
    assert position[SENIORS_TRANSIT_CREDIT] < position[ONTARIO_CREDITS_SUBTOTAL]
    assert (
        position[ONTARIO_CREDITS_SUBTOTAL]
        < position[ONTARIO_CREDITS]
        < position[PROVINCIAL_CREDITS]
        < position[TOTAL_CREDITS]
    )


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
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("1440.58")
    assert worksheet.get(CANADA_EMPLOYMENT_AMOUNT).value == D("1471")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("18085.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("13232.75")
    # 14.5% of 18085.75 = 2622.43375 and 5.05% of 13232.75 = 668.253875, each rounded half-up to
    # the cent: each larger than its basic tax (14.5% of 9935.00 = 1440.575, rounded half-up to
    # the cent: 1440.58).
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("2622.43")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("668.25")
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
    # Schedule ON428-A: line 5 is 5.05% x 10000 = 505.00, below the $875 maximum, and net
    # income of 9935.00 is below the 32,500.00 threshold, so no reduction: the credit (ON428 line
    # 85) is 505.00, more than the Ontario tax after the reduction of zero, so line 86 is zero.
    assert worksheet.get(LIFT_CREDIT_BEFORE_MAXIMUM).value == D("505.00")
    assert worksheet.get(LIFT_MAXIMUM_CREDIT).value == D("505.00")
    assert worksheet.get(LIFT_REDUCTION).value == D("0")
    assert worksheet.get(LIFT_CREDIT).value == D("505.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("0")
    # A taxable income of 9935.00 is "$20,000 or less" on the health premium chart: no premium.
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("0")
    assert worksheet.get(ONTARIO_TAX).value == D("0")
    # Schedule 6: the working income is the employment income of 10000, and line 20 is (10000 -
    # 3000) x 27% = 1890.00, more than the $1,633 of line 21, so line 22 is 1633; the adjusted
    # family net income of 9935.00 is below the $26,855 of line 24, so no reduction: the benefit
    # (line 28) is 1633. With an eligible dependant line 22 would be 1890.00, below the $2,813,
    # and line 24's $30,639 is above the income too, so its line 28 is 1890.00; with 0 eligible
    # dependants the amounts without one are the ones claimed (T1 line 45300): 1633.
    assert worksheet.get(WORKING_INCOME).value == D("10000")
    assert worksheet.get(ADJUSTED_FAMILY_NET_INCOME).value == D("9935.00")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT).value == D("1633")
    assert worksheet.get(CWB_REDUCTION_WITHOUT_DEPENDANT).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT).value == D("1633")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITH_DEPENDANT).value == D("1890.00")
    assert worksheet.get(CWB_REDUCTION_WITH_DEPENDANT).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT).value == D("1890.00")
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
    # tax 5.05% x 23795.00 = 1201.6475, rounded half-up to the cent: 1201.65, less the Ontario
    # credits 5.05% x (12747 + 1014.75 + 393.60 = 14155.35) = 714.845175, rounded half-up to the
    # cent: 714.85, is 486.80, below the first surtax threshold, so the Ontario tax with surtax
    # (ON428 line 73) is 486.80. With no dependent children and no dependants, line 78 is 2 x
    # 294.00 = 588.00, and line 80 is 588.00 - 486.80 = 101.20; line 81 is 486.80 - 101.20 =
    # 385.60.
    worksheet = compute("24000", "0", "0", "0", "4320", "0", "0")

    assert worksheet.get(ONTARIO_TAX_WITH_SURTAX).value == D("486.80")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("294.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("101.20")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("385.60")


def test_dependent_children_and_dependants_raise_the_tax_reduction() -> None:
    # Return A's amounts with five dependent children (ON428 line 75, line 60969) and three
    # dependants (line 76, line 60970): line 75 is 5 x 544 = 2720, line 76 is 3 x 544 = 1632,
    # line 77 is 294.00 + 2720 + 1632 = 4646.00 and line 78 is 9292.00; line 80 is 9292.00 -
    # 8195.77 = 1096.23, and line 81 is 8195.77 - 1096.23 = 7099.54.
    worksheet = compute(
        "110000", "20000", "0", "1926", "19800", "1926", "2000", dependent_children=5, dependants=3
    )

    assert worksheet.get(DEPENDENT_CHILDREN).value == 5
    assert worksheet.get(DEPENDANTS).value == 3
    assert worksheet.get(TAX_REDUCTION_FOR_CHILDREN).value == D("2720")
    assert worksheet.get(TAX_REDUCTION_FOR_DEPENDANTS).value == D("1632")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("4646.00")
    assert worksheet.get(ONTARIO_TAX_WITH_SURTAX).value == D("8195.77")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("1096.23")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("7099.54")


def test_the_health_premium_in_a_sloped_row_adds_the_rate_to_the_plateau() -> None:
    # A capital gain of 74000 alone, with no employment income, no RRSP contributions and no
    # union dues: taxable income is half the gain, 37000, and the Ontario credits are 5.05% x
    # 12747 = 643.7235, rounded half-up to the cent: 643.72. ON428 line 89's chart, "more than
    # $36,000 but not more than $38,500": (37000 - 36000) x 6% + 300 = 360.00; the Ontario basic
    # tax 5.05% x 37000 = 1868.50 less the credits is 1224.78, above 588.00, so no reduction,
    # and line 90 is 1224.78 + 360.00 = 1584.78.
    worksheet = compute("0", "74000", "0", "0", "0", "0", "0")

    assert worksheet.get(TAXABLE_INCOME).value == D("37000")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("1224.78")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("360.00")
    assert worksheet.get(ONTARIO_TAX).value == D("1584.78")


def test_the_health_premium_at_the_top_of_a_sloped_row_is_the_plateau() -> None:
    # A capital gain of 50000 alone: taxable income 25000, "more than $20,000 but not more than
    # $25,000": (25000 - 20000) x 6% = 300.00, the plateau itself; the Ontario basic tax 5.05%
    # x 25000 = 1262.50 less the credits of 643.72 is 618.78, above 588.00, so no reduction,
    # and line 90 is 618.78 + 300.00 = 918.78.
    worksheet = compute("0", "50000", "0", "0", "0", "0", "0")

    assert worksheet.get(TAXABLE_INCOME).value == D("25000")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("618.78")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("300.00")
    assert worksheet.get(ONTARIO_TAX).value == D("918.78")


def test_no_health_premium_at_the_first_threshold() -> None:
    # A capital gain of 40000 alone: taxable income 20000, "$20,000 or less", so no premium;
    # the Ontario basic tax 5.05% x 20000 = 1010.00 less the credits of 643.72 is 366.28, below
    # 588.00, so the reduction is 221.72 and line 81 is 144.56, which is line 90.
    worksheet = compute("0", "40000", "0", "0", "0", "0", "0")

    assert worksheet.get(TAXABLE_INCOME).value == D("20000")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("144.56")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("0")
    assert worksheet.get(ONTARIO_TAX).value == D("144.56")


def test_the_lift_credit_between_the_thresholds_is_reduced_and_comes_off_the_tax() -> None:
    # Employment income of 40000, with no capital gain, no RRSP contributions and no union dues:
    # base CPP contributions 4.95% x (40000 - 3500) = 1806.75, first additional 1% x 36500 =
    # 365.00, EI premiums 1.64% x 40000 = 656.00; net and taxable income 39635.00. Ontario basic
    # tax 5.05% x 39635.00 = 2001.5675, rounded half-up to the cent: 2001.57, less the Ontario
    # credits 5.05% x (12747 + 1806.75 + 656.00 = 15209.75) = 768.092375, rounded half-up to the
    # cent: 768.09, is 1233.48, below the first surtax threshold and above 588.00, so line 81 is
    # 1233.48.
    # Schedule ON428-A: line 5 is 5.05% x 40000 = 2020.00, at most 875 (line 14); line 17 is
    # 39635.00 - 32500 = 7135.00 and line 19 7135.00 x 5% = 356.75; line 20 is 875 - 356.75 =
    # 518.25 (ON428 line 85). Line 86 is 1233.48 - 518.25 = 715.23; the health premium on
    # 39635.00, "more than $38,500 but not more than $48,000", is 450, so line 90 is 715.23 + 450
    # = 1165.23.
    worksheet = compute("40000", "0", "0", "0", "7200", "0", "0")

    assert worksheet.get(NET_INCOME).value == D("39635.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("1233.48")
    assert worksheet.get(LIFT_CREDIT_BEFORE_MAXIMUM).value == D("2020.00")
    assert worksheet.get(LIFT_MAXIMUM_CREDIT).value == D("875")
    assert worksheet.get(LIFT_REDUCTION).value == D("356.75")
    assert worksheet.get(LIFT_CREDIT).value == D("518.25")
    assert worksheet.get(ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("715.23")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("450")
    assert worksheet.get(ONTARIO_TAX).value == D("1165.23")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "lift_credit: lift_maximum_credit 875 less lift_reduction 356.75, not below 0 = 518.25"
    ) in rendered
    assert (
        "ontario_tax_after_lift_credit: ontario_tax_after_reduction 1233.48 "
        "less lift_credit 518.25, not below 0 = 715.23"
    ) in rendered


def test_the_canada_workers_benefit_below_its_maximum_is_27_percent_over_3000() -> None:
    # Employment income of 8000, with no capital gain, no RRSP contributions and no union dues:
    # base CPP contributions 4.95% x (8000 - 3500) = 222.75, first additional 1% x 4500 = 45.00,
    # EI premiums 1.64% x 8000 = 131.20; net income 8000 - 45.00 = 7955.00. Each form's credits
    # exceed its tax, so nothing is payable. Schedule 6: the working income (line 5) is 8000,
    # line 18 is 8000 - 3000 = 5000 and line 20 5000 x 27% = 1350.00, less than the $1,633 of
    # line 21, so line 22 is 1350.00; the adjusted family net income (line 15) of 7955.00 is
    # below the $26,855 of line 24, so line 27 is 0 and line 28 (T1 line 45300) is 1350.00. With
    # an eligible dependant the same 1350.00, below its $2,813 and over nothing above its
    # $30,639. With no tax deducted, the total credits are 0 + 1350.00 and line 167 is
    # 0 - 1350.00 = -1350.00, a refund.
    worksheet = compute("8000", "0", "0", "0", "1440", "0", "0")

    assert worksheet.get(NET_INCOME).value == D("7955.00")
    assert worksheet.get(TOTAL_PAYABLE).value == D("0")
    assert worksheet.get(WORKING_INCOME).value == D("8000")
    assert worksheet.get(ADJUSTED_FAMILY_NET_INCOME).value == D("7955.00")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT).value == D("1350.00")
    assert worksheet.get(CWB_REDUCTION_WITHOUT_DEPENDANT).value == D("0")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITH_DEPENDANT).value == D("1350.00")
    assert worksheet.get(CWB_REDUCTION_WITH_DEPENDANT).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("1350.00")
    assert worksheet.get(TOTAL_CREDITS).value == D("1350.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-1350.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "cwb_before_reduction_without_dependant: 27% of working_income 8000 over 3000, "
        "at most 1633 (half-up to 0.01)"
    ) in rendered
    assert (
        "canada_workers_benefit_without_dependant: cwb_before_reduction_without_dependant 1350 "
        "less cwb_reduction_without_dependant 0, not below 0 = 1350"
    ) in rendered
    assert (
        "canada_workers_benefit: canada_workers_benefit_without_dependant 1350, "
        "chosen as cwb_eligible_dependants is 0"
    ) in rendered


def test_an_eligible_dependant_takes_the_schedule_6_amounts_of_2813_and_30639() -> None:
    # Employment income of 35000 and one eligible dependant, a dependent child: base CPP
    # contributions 4.95% x (35000 - 3500) = 1559.25, first additional 1% x 31500 = 315.00, so
    # net income is 35000 - 315.00 = 34685.00. Schedule 6 lines 21 and 24, "If you had an
    # eligible spouse or an eligible dependant, enter $2,813. If not, enter $1,633." and "...
    # enter $30,639. If not, enter $26,855.": with no eligible spouse or dependant, line 22 is
    # 1633 (32000 x 27% = 8640.00 is more), line 27 (34685.00 - 26855) x 15% = 1174.50 and
    # line 28 458.50; with one, line 22 is 2813, line 27 (34685.00 - 30639) x 15% = 606.90
    # and line 28 2206.10, each rounded half-up to the cent, which changes none of them. The
    # count of 1 Schedule 6 eligible dependant (line 38100) chooses the second for line 45300, so
    # with no tax deducted the total credits are 2206.10.
    worksheet = compute(
        "35000",
        "0",
        "0",
        "0",
        "6300",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
    )

    assert worksheet.get(NET_INCOME).value == D("34685.00")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT).value == D("1633")
    assert worksheet.get(CWB_REDUCTION_WITHOUT_DEPENDANT).value == D("1174.50")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT).value == D("458.50")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITH_DEPENDANT).value == D("2813")
    assert worksheet.get(CWB_REDUCTION_WITH_DEPENDANT).value == D("606.90")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT).value == D("2206.10")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("2206.10")
    assert worksheet.get(TOTAL_CREDITS).value == D("2206.10")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "cwb_before_reduction_with_dependant: 27% of working_income 35000 over 3000, "
        "at most 2813 (half-up to 0.01)"
    ) in rendered
    assert (
        "cwb_reduction_with_dependant: 15% of adjusted_family_net_income 34685 over 30639 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "canada_workers_benefit: canada_workers_benefit_with_dependant 2206.1, "
        "chosen as cwb_eligible_dependants is 1"
    ) in rendered


def test_with_no_eligible_dependant_the_same_income_takes_the_amounts_of_1633_and_26855() -> None:
    # The amounts of the test above with no eligible dependant claimed for, and no dependent
    # child: both family statuses are computed alike, and the count of 0 chooses the one
    # without an eligible dependant, 458.50.
    worksheet = compute("35000", "0", "0", "0", "6300", "0", "0")

    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT).value == D("458.50")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT).value == D("2206.10")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("458.50")
    assert worksheet.get(TOTAL_CREDITS).value == D("458.50")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "canada_workers_benefit: canada_workers_benefit_without_dependant 458.5, "
        "chosen as cwb_eligible_dependants is 0"
    ) in rendered


def test_a_line_30400_dependant_who_is_not_schedule_6s_leaves_the_amounts_without_one() -> None:
    # The amounts of the tests above with one eligible dependant claimed for on T1 line 30400, a
    # parent, say, who is not Schedule 6's eligible dependant ("They were your or your spouse's
    # or common-law partner's child"): the Schedule 6 count of 0 (line 38100), not the line
    # 30400 count of 1, chooses the amounts with no eligible dependant, 458.50.
    worksheet = compute("35000", "0", "0", "0", "6300", "0", "0", eligible_dependants=1)

    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT).value == D("458.50")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT).value == D("2206.10")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("458.50")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "canada_workers_benefit: canada_workers_benefit_without_dependant 458.5, "
        "chosen as cwb_eligible_dependants is 0"
    ) in rendered


def test_a_schedule_6_dependant_not_claimed_on_line_30400_takes_the_amounts_with_one() -> None:
    # The same income with a child under 19 who lived with the filer but is not claimed for on
    # T1 line 30400 (claimed by the other parent, say): the Schedule 6 count of 1 (line 38100)
    # chooses the amounts with an eligible dependant, 2206.10, though the line 30400 count is 0.
    worksheet = compute("35000", "0", "0", "0", "6300", "0", "0", cwb_eligible_dependants=1)

    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT).value == D("458.50")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT).value == D("2206.10")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("2206.10")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "canada_workers_benefit: canada_workers_benefit_with_dependant 2206.1, "
        "chosen as cwb_eligible_dependants is 1"
    ) in rendered


def test_tax_deducted_above_the_total_payable_is_a_refund() -> None:
    # Return A's amounts with 30000 of income tax deducted (T1 line 43700): line 167 is the total
    # payable of 25897.15 less the total credits of 30000, -4102.85, negative, so a refund (line
    # 48400), in cents as every line before it is.
    worksheet = compute(
        "110000", "20000", "0", "1926", "19800", "1926", "2000", income_tax_deducted="30000"
    )

    assert worksheet.get(TOTAL_PAYABLE).value == D("25897.15")
    assert worksheet.get(TOTAL_CREDITS).value == D("30000")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-4102.85")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "refund_or_balance_owing: total_payable 25897.15 less total_credits 30000 = -4102.85"
    ) in rendered


def test_tax_deducted_equal_to_the_total_payable_leaves_no_balance() -> None:
    worksheet = compute(
        "110000", "20000", "0", "1926", "19800", "1926", "2000", income_tax_deducted="25897.15"
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
        "total_credits: income_tax_deducted 500 + canada_workers_benefit 1633 "
        "+ provincial_credits 0 = 2133"
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
    # no net income, and the child care expenses deduction of 5000 (T1 line 21400), so net
    # income is 60000 - (5000 + 565.00) = 54435.00. Schedule 5 line 5 is its line 30000 of
    # 16129.00 less 0, claimed for 1 eligible dependant: line 30400 is 16129.00. ON428 line 16
    # is 11905.00 less 0, at most 10823: line 58160 is 10823. Line 33500 is 16129 + 16129.00 + 0
    # + 2796.75 + 984.00 + 1471 = 37509.75, and line 35000 37509.75 x 14.5% = 5438.91375,
    # rounded half-up to the cent: 5438.91, so the federal tax after credits is 14.5% x 54435.00
    # = 7893.075, rounded half-up to the cent: 7893.08, less it, 2454.17. ON428 line 58800 is
    # 12747 + 10823 + 2796.75 + 984.00 = 27350.75, and line 61500 27350.75 x 5.05% =
    # 1381.212875, rounded half-up to the cent: 1381.21, so the Ontario tax after credits is
    # 2670.74 + 9.15% x (54435.00 - 52886) = 2812.4735, rounded half-up to the cent: 2812.47,
    # less it, 1431.26. The child is a dependent child for the Ontario tax reduction: 294.00 +
    # 544 = 838.00, twice it 1676.00, less 1431.26 is a reduction of 244.74, leaving 1186.52.
    # With the health premium of 600 the Ontario tax is 1786.52, the total payable 2454.17 +
    # 1786.52 = 4240.69, and line 167 4240.69 - 8000 = -3759.31, a refund.
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        child_care_expenses_paid="6000",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
    )

    assert worksheet.get(NET_INCOME).value == D("54435.00")
    assert worksheet.get(BASIC_PERSONAL_AMOUNT).value == D("16129.00")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("16129.00")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT).value == D("16129.00")
    assert worksheet.get(INFIRM_CHILDREN_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("37509.75")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("5438.91")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("2454.17")
    assert worksheet.get(ELIGIBLE_DEPENDANT_BASE).value == D("11905.00")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM).value == D("11905.00")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("10823")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("10823")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("27350.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("1381.21")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("1431.26")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("838.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("244.74")
    assert worksheet.get(ONTARIO_TAX).value == D("1786.52")
    assert worksheet.get(TOTAL_PAYABLE).value == D("4240.69")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-3759.31")
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


def test_return_fs_canada_workers_benefit_is_zero_with_an_eligible_dependant() -> None:
    # Return F, Schedule 6: working income 60000 (line 5) and adjusted family net income
    # 54435.00 (line 15). With the eligible dependant, line 22 is the lesser of (60000 - 3000) x
    # 27% = 15390.00 and 2813: 2813; line 27 is (54435.00 - 30639) x 15% = 3569.40; line 28 is
    # 2813 - 3569.40, negative, so 0. Without an eligible dependant, line 22 1633 and line 27
    # (54435.00 - 26855) x 15% = 4137.00, is computed too and is also 0; the count of 1
    # Schedule 6 eligible dependant (line 38100) chooses the amounts with one for T1 line 45300.
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        child_care_expenses_paid="6000",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
    )

    assert worksheet.get(WORKING_INCOME).value == D("60000")
    assert worksheet.get(ADJUSTED_FAMILY_NET_INCOME).value == D("54435.00")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITH_DEPENDANT).value == D("2813")
    assert worksheet.get(CWB_REDUCTION_WITH_DEPENDANT).value == D("3569.40")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT).value == D("0")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT).value == D("1633")
    assert worksheet.get(CWB_REDUCTION_WITHOUT_DEPENDANT).value == D("4137.00")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("0")
    assert worksheet.get(TOTAL_CREDITS).value == D("8000")
    (chosen,) = [line for line in worksheet.trace if isinstance(line, ChosenByCountLine)]
    assert chosen == ChosenByCountLine(
        output=CANADA_WORKERS_BENEFIT,
        count_kind=CWB_ELIGIBLE_DEPENDANTS,
        count=1,
        chosen_kind=CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
        chosen_value=D("0"),
    )
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "canada_workers_benefit_with_dependant: cwb_before_reduction_with_dependant 2813 "
        "less cwb_reduction_with_dependant 3569.4, not below 0 = 0"
    ) in rendered
    assert (
        "canada_workers_benefit: canada_workers_benefit_with_dependant 0, "
        "chosen as cwb_eligible_dependants is 1"
    ) in rendered


def return_f_with_credits(fertility_expenses: str, seniors_transit_paid: str) -> Worksheet:
    """Return F's inputs, as in `returns/2025_return_f.yaml`, with the ON479 amounts given."""
    return compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        child_care_expenses_paid="6000",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
        fertility_expenses=fertility_expenses,
        seniors_transit_paid=seniors_transit_paid,
    )


def test_return_gs_ontario_credits_are_5180_and_lower_the_refund_by_that_much() -> None:
    # Return G is Return F with fertility expenses of 24000 and 1200 paid for seniors' transit.
    # ON479 line 1: 24000 x 25% = 6000.00, at most 5000: 5000. Line 14: 1200, at most 3000, x 15%
    # = 180.00. Line 18 is 5000 + 180.00 = 5180.00, line 19 carries it, line 21 and T1 line
    # 47900 are 5180.00; the total credits are 8000 + 0 + 5180.00 = 13180.00 and line 167 is
    # 4240.69 - 13180.00 = -8939.31, Return F's -3759.31 less 5180.00.
    without = return_f_with_credits("0", "0")
    worksheet = return_f_with_credits("24000", "1200")

    assert worksheet.get(FERTILITY_CREDIT_BEFORE_MAXIMUM).value == D("6000.00")
    assert worksheet.get(FERTILITY_CREDIT).value == D("5000")
    assert worksheet.get(SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM).value == D("1200")
    assert worksheet.get(SENIORS_TRANSIT_CREDIT).value == D("180.00")
    assert worksheet.get(ONTARIO_CREDITS_SUBTOTAL).value == D("5180.00")
    assert worksheet.get(ONTARIO_CREDITS).value == D("5180.00")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("5180.00")
    assert worksheet.get(TOTAL_PAYABLE).value == D("4240.69")
    assert worksheet.get(TOTAL_CREDITS).value == D("13180.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-8939.31")
    assert without.get(PROVINCIAL_CREDITS).value == D("0")
    assert without.get(REFUND_OR_BALANCE_OWING).value == D("-3759.31")
    assert without.get(REFUND_OR_BALANCE_OWING).value - worksheet.get(
        REFUND_OR_BALANCE_OWING
    ).value == D("5180.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "fertility_credit_before_maximum: 25% of fertility_expenses 24000 (half-up to 0.01)"
    ) in rendered
    assert (
        "fertility_credit: lesser of fertility_credit_before_maximum 6000 and 5000 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "seniors_transit_amount_paid_at_most_maximum: lesser of seniors_transit_paid 1200 and "
        "3000 (half-up to 0.01)"
    ) in rendered
    assert (
        "seniors_transit_credit: 15% of seniors_transit_amount_paid_at_most_maximum 1200 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "ontario_credits_subtotal: fertility_credit 5000 + seniors_transit_credit 180 = 5180"
    ) in rendered
    assert "ontario_credits: ontario_credits_subtotal 5180 = 5180" in rendered
    assert "provincial_credits: ontario_credits 5180 = 5180" in rendered
    assert (
        "total_credits: income_tax_deducted 8000 + canada_workers_benefit 0 "
        "+ provincial_credits 5180 = 13180"
    ) in rendered
    assert (
        "refund_or_balance_owing: total_payable 4240.69 less total_credits 13180 = -8939.31"
    ) in rendered


def test_the_fertility_credit_below_its_maximum_is_25_percent_of_the_expenses() -> None:
    # 12000 x 25% = 3000.00, below the maximum of 5000, so line 1 is 3000.00 and the credits are
    # 3000.00 with no transit amount.
    worksheet = return_f_with_credits("12000", "0")

    assert worksheet.get(FERTILITY_CREDIT_BEFORE_MAXIMUM).value == D("3000.00")
    assert worksheet.get(FERTILITY_CREDIT).value == D("3000.00")
    assert worksheet.get(SENIORS_TRANSIT_CREDIT).value == D("0")
    assert worksheet.get(ONTARIO_CREDITS).value == D("3000.00")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("3000.00")
    assert worksheet.get(TOTAL_CREDITS).value == D("11000.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-6759.31")


def test_the_transit_amount_paid_is_capped_before_the_rate() -> None:
    # 3500 paid is capped at 3000 (ON479 line 14, "(maximum $3,000)" before the percentage), and
    # 3000 x 15% = 450.00, not 3500 x 15% = 525.00.
    worksheet = return_f_with_credits("0", "3500")

    assert worksheet.get(SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM).value == D("3000")
    assert worksheet.get(SENIORS_TRANSIT_CREDIT).value == D("450.00")
    assert worksheet.get(FERTILITY_CREDIT).value == D("0")
    assert worksheet.get(ONTARIO_CREDITS).value == D("450.00")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("450.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-4209.31")
    (capped_paid,) = [
        line
        for line in worksheet.trace
        if isinstance(line, CappedAmountLine)
        and line.output == SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM
    ]
    assert capped_paid == CappedAmountLine(
        SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
        SENIORS_TRANSIT_PAID,
        D("3500"),
        Amount(D("3000")),
        CENT,
        D("3000"),
    )


def test_the_fertility_credit_is_capped_after_the_rate() -> None:
    # 24000 x 25% = 6000.00 is above 5000, so line 1 is the maximum, whereas capping the expenses
    # at 5000 first would give 1250.00.
    worksheet = return_f_with_credits("24000", "0")

    (capped,) = [
        line
        for line in worksheet.trace
        if isinstance(line, CappedAmountLine) and line.output == FERTILITY_CREDIT
    ]
    assert capped == CappedAmountLine(
        FERTILITY_CREDIT,
        FERTILITY_CREDIT_BEFORE_MAXIMUM,
        D("6000.00"),
        Amount(D("5000")),
        CENT,
        D("5000"),
    )


def test_the_dependants_net_income_comes_off_both_amounts() -> None:
    # Return F's amounts with a dependant's net income of 1500 (Schedule 5 line 4, ON428 line
    # 15): line 5 is 16129.00 - 1500 = 14629.00, and ON428 line 16 is 11905.00 - 1500 =
    # 10405.00, below the $10,823 maximum, so kept. Line 33500 is 16129 + 14629.00 + 0 +
    # 2796.75 + 984.00 + 1471 = 36009.75; ON428 line 58800 is 12747 + 10405.00 + 2796.75 +
    # 984.00 = 26932.75.
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        dependant_net_income="1500",
        child_care_expenses_paid="6000",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
    )

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
        "eligible_dependant_amount_before_maximum 10405 and 10823 (half-up to 0.01)"
    ) in rendered


def test_a_dependant_with_more_income_than_the_amounts_adds_nothing() -> None:
    # Schedule 5 line 5 and ON428 line 16 "(if negative, enter "0")": a dependant's net income
    # of 20000 is above both 16129.00 and 11905.00, so each amount is 0 and the totals are those
    # without a dependant: 16129 + 0 + 0 + 2796.75 + 984.00 + 1471 = 21380.75 and 12747 + 0 +
    # 2796.75 + 984.00 = 16527.75.
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        dependant_net_income="20000",
        child_care_expenses_paid="6000",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
    )

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
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        dependant_net_income="1500",
        child_care_expenses_paid="6000",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
    )

    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("14629.00")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT).value == D("0")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("10405.00")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("21380.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("16527.75")


def test_infirm_children_add_2687_each_to_the_federal_amounts_only() -> None:
    # Return A's amounts with two infirm children (T1 line 30499): line 30500 is 2 x 2687 =
    # 5374, so line 33500 is 22033.58 + 5374 = 27407.58, line 35000 27407.58 x 14.5% =
    # 3974.0991, rounded half-up to the cent: 3974.10, and the federal tax after credits
    # 20146.25 - 3974.10 = 16172.15. ON428 has
    # no such line here (its caregiver amount, line 58185, is not triggered), so its total is
    # unchanged at 17180.58.
    worksheet = compute("110000", "20000", "0", "1926", "19800", "1926", "2000", infirm_children=2)

    assert worksheet.get(INFIRM_CHILDREN).value == 2
    assert worksheet.get(INFIRM_CHILDREN_AMOUNT).value == D("5374")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("27407.58")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("3974.10")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("16172.15")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("17180.58")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "infirm_children_amount: 2687 for each of 2 infirm_children = 5374 (half-up to 0.01)"
        in (rendered)
    )


def test_the_child_care_expenses_deduction_is_5000_for_one_child_and_lowers_net_income() -> None:
    # Return F, Form T778: the child, born in 2015, is counted on Part B line 3, so line 1 is 0
    # x 8000 = 0, line 2 0 x 11000 = 0 and line 3 1 x 5000 = 5000; line 4 is 0 + 0 + 5000 =
    # 5000; line 5 is the 6000 paid; line 6 is two-thirds of the earned income, the employment
    # income of 60000: 40000. Line 7 is the least of 5000, 6000 and 40000: 5000, line 21400. T1
    # line 23300 is 0 + 0 + 5000 + 565.00 = 5565.00, and net income 60000 - 5565.00 =
    # 54435.00, which the LIFT reduction (5% of 54435.00 over 32500 = 1096.75) and Schedule 6
    # (15% of 54435.00 over 30639 = 3569.40, with the eligible dependant) read; the federal and
    # Ontario taxes on it are 7893.075 and 2812.4735, rounded half-up to the cent.
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        child_care_expenses_paid="6000",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
    )

    assert worksheet.get(CHILDREN_SEVEN_TO_SIXTEEN).value == 1
    assert worksheet.get(CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN).value == D("0")
    assert worksheet.get(CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY).value == D("0")
    assert worksheet.get(CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN).value == D("5000")
    assert worksheet.get(CHILD_CARE_BASIC_LIMIT).value == D("5000")
    assert worksheet.get(CHILD_CARE_EARNED_INCOME).value == D("60000")
    assert worksheet.get(CHILD_CARE_EARNED_INCOME_LIMIT).value == D("40000")
    assert worksheet.get(CHILD_CARE_EXPENSES).value == D("5000")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("5565.00")
    assert worksheet.get(NET_INCOME).value == D("54435.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("54435.00")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("7893.08")
    assert worksheet.get(ONTARIO_BASIC_TAX).value == D("2812.47")
    assert worksheet.get(LIFT_REDUCTION).value == D("1096.75")
    assert worksheet.get(LIFT_CREDIT).value == D("0")
    assert worksheet.get(ADJUSTED_FAMILY_NET_INCOME).value == D("54435.00")
    assert worksheet.get(CWB_REDUCTION_WITH_DEPENDANT).value == D("3569.40")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("0")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "child_care_limit_for_children_seven_to_sixteen: 5000 for each of 1 "
        "children_seven_to_sixteen = 5000 (half-up to 0.01)"
    ) in rendered
    assert (
        "child_care_earned_income_limit: 2/3 of child_care_earned_income 60000 (half-up to 0.01)"
    ) in rendered
    assert (
        "child_care_expenses: lesser of child_care_basic_limit 5000 and child_care_expenses_paid "
        "6000 and child_care_earned_income_limit 40000 = 5000"
    ) in rendered
    assert (
        "deductions_from_total_income: rrsp_deduction 0 + union_dues 0 "
        "+ child_care_expenses 5000 + cpp_enhanced_contributions 565 = 5565"
    ) in rendered


def test_expenses_paid_below_the_basic_limit_are_deducted_whole() -> None:
    # Return F with 3500 paid (T778 line 5): the least of 5000, 3500 and 40000 is 3500, so T1
    # line 23300 is 3500 + 565.00 = 4065.00 and net income 60000 - 4065.00 = 55935.00.
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        child_care_expenses_paid="3500",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
    )

    assert worksheet.get(CHILD_CARE_EXPENSES).value == D("3500")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("4065.00")
    assert worksheet.get(NET_INCOME).value == D("55935.00")


def test_the_limits_for_each_kind_of_eligible_child_add_up() -> None:
    # Return F with one child on each of T778 Part B lines 1, 2 and 3 and 30000 paid: line 4 is
    # 8000 + 11000 + 5000 = 24000, below the 30000 paid and the 40000 of line 6, so the
    # deduction is 24000, T1 line 23300 is 24000 + 565.00 = 24565.00 and net income 60000 -
    # 24565.00 = 35435.00.
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        child_care_expenses_paid="30000",
        children_under_seven=1,
        children_with_disability=1,
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
    )

    assert worksheet.get(CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN).value == D("8000")
    assert worksheet.get(CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY).value == D("11000")
    assert worksheet.get(CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN).value == D("5000")
    assert worksheet.get(CHILD_CARE_BASIC_LIMIT).value == D("24000")
    assert worksheet.get(CHILD_CARE_EXPENSES).value == D("24000")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("24565.00")
    assert worksheet.get(NET_INCOME).value == D("35435.00")


def test_two_thirds_of_a_low_earned_income_caps_the_deduction() -> None:
    # Employment income of 9000, two children born in 2019 or later and 12000 paid: line 4 is 2
    # x 8000 = 16000, line 5 12000, line 6 two-thirds of 9000 = 6000, the least, so the
    # deduction is 6000. The first additional CPP contribution is 1% x (9000 - 3500) = 55.00, so
    # T1 line 23300 is 6000 + 55.00 = 6055.00 and net income 9000 - 6055.00 = 2945.00.
    worksheet = compute(
        "9000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        child_care_expenses_paid="12000",
        children_under_seven=2,
    )

    assert worksheet.get(CHILD_CARE_BASIC_LIMIT).value == D("16000")
    assert worksheet.get(CHILD_CARE_EARNED_INCOME_LIMIT).value == D("6000")
    assert worksheet.get(CHILD_CARE_EXPENSES).value == D("6000")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("6055.00")
    assert worksheet.get(NET_INCOME).value == D("2945.00")
