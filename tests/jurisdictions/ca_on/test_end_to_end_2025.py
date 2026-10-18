"""CA-ON 2025, end to end: CRA's worked example computed from the manifest through the service.

The service is the one the composition root builds (`build_tax_computation`): the real YAML
sources over the jurisdiction packages and the shared registries. Return A's amounts (employment
income 110000 and a capital gain of 20000 to total income 120000; the CPP contributions computed
from employment income by Schedule 8's tiers, each at its maximum: base 3356.10, first additional
678.00 and second additional 396.00, the enhanced contributions 1074.00; the EI premiums computed
from employment income, at the maximum 1077.48; the RRSP contributions available to deduct of 1926,
no unused contributions plus the contributions of 1926 (Schedule 7 line 10), and the RRSP deduction
of 1926, the lesser of them and the deduction limit of 19800 (Schedule 7 line 20); less that RRSP
deduction, union dues of 2000 and the enhanced contributions to net income 115000, less no
deductions from net income to taxable income 115000, and from each basic personal amount (16129
federal, the Federal Worksheet's taper on net income, here at or below the 177882 threshold so not
reduced; 12747 Ontario) plus the base CPP contributions and the EI premiums, and federally the
Canada employment amount of 1471 (the lesser of employment income and 1471), through each total of
credit amounts and each form's non-refundable tax credits (T1 line 35000, ON428 line 61500) to each
tax after credits, the Ontario surtax on the Ontario tax after credits (ON428 lines 66 to 68) to
the Ontario tax with surtax of line 69, and with no dependent children and no dependants the
Ontario tax reduction amounts of 294.00 (lines 74 to 77), twice them less the tax with surtax (line
73), not below zero, the Ontario tax reduction of 0 (line 80), to the Ontario tax after the
reduction (line 81)) are checked from the files under `returns/` by `test_worked_returns.py`, as
are Returns C, D and E; this module pins which capability produces each line, the order, and the
trace that explains them.
"""

from __future__ import annotations

from decimal import Decimal

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import Artifact
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.multiple_over import MultipleOver
from app.domain.capabilities.per_unit_amount import PerUnitAmount
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.tapered_amount import TaperedAmount
from app.domain.capabilities.tiered_surcharge import TieredSurcharge
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.parameters.amount import Amount
from app.domain.parameters.contribution_tier import ContributionTier
from app.domain.parameters.credit import Credit
from app.domain.parameters.factor import Factor
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundTo
from app.domain.parameters.taper import Taper
from app.domain.trace import (
    CappedAmountLine,
    ContributionTierLine,
    CreditAmountLine,
    LesserOfLine,
    MultipleOverLine,
    PerUnitAmountLine,
    RateAppliedLine,
    RoundedTotalLine,
    SubtractedNotBelowZeroLine,
    SumLine,
    SurchargeTierLine,
    TaperedAmountLine,
)
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    BASIC_PERSONAL_AMOUNT,
    CANADA_EMPLOYMENT_AMOUNT,
    CAPITAL_GAIN,
    CPP_BASE_CONTRIBUTIONS,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    EI_PREMIUMS,
    EMPLOYMENT_INCOME,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    NET_INCOME,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    RRSP_CONTRIBUTIONS,
    RRSP_CONTRIBUTIONS_AVAILABLE,
    RRSP_DEDUCTION,
    RRSP_DEDUCTION_LIMIT,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    UNION_DUES,
    UNUSED_RRSP_CONTRIBUTIONS,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    ONTARIO_BASIC_TAX,
    ONTARIO_SURTAX,
    ONTARIO_TAX_AFTER_CREDITS,
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
    union_dues: str,
    *,
    dependent_children: int = 0,
    dependants: int = 0,
) -> Worksheet:
    return service().compute(
        CA_ON,
        2025,
        Artifact(EMPLOYMENT_INCOME, D(employment_income)),
        Artifact(CAPITAL_GAIN, D(capital_gain)),
        Artifact(UNUSED_RRSP_CONTRIBUTIONS, D(unused_rrsp_contributions)),
        Artifact(RRSP_CONTRIBUTIONS, D(rrsp_contributions)),
        Artifact(RRSP_DEDUCTION_LIMIT, D(rrsp_deduction_limit)),
        Artifact(UNION_DUES, D(union_dues)),
        Artifact(DEPENDENT_CHILDREN, dependent_children),
        Artifact(DEPENDANTS, dependants),
    )


def return_a() -> Worksheet:
    """Return A's inputs, as in `returns/2025_return_a.yaml`."""
    return compute("110000", "20000", "0", "1926", "19800", "2000")


def test_each_amount_is_produced_by_its_capability() -> None:
    worksheet = return_a()

    assert worksheet.producer_of(EMPLOYMENT_INCOME) is None
    assert worksheet.producer_of(CAPITAL_GAIN) is None
    assert worksheet.producer_of(UNUSED_RRSP_CONTRIBUTIONS) is None
    assert worksheet.producer_of(RRSP_CONTRIBUTIONS) is None
    assert worksheet.producer_of(RRSP_DEDUCTION_LIMIT) is None
    assert worksheet.producer_of(UNION_DUES) is None
    assert worksheet.producer_of(DEPENDENT_CHILDREN) is None
    assert worksheet.producer_of(DEPENDANTS) is None
    assert isinstance(worksheet.producer_of(RRSP_CONTRIBUTIONS_AVAILABLE), Sum)
    assert isinstance(worksheet.producer_of(RRSP_DEDUCTION), LesserOf)
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
    rrsp = position(
        "rrsp_deduction: lesser of rrsp_contributions_available 1926 "
        "and rrsp_deduction_limit 19800 = 1926",
        "1926",
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
    federal_amounts = position(
        "non_refundable_credit_amounts: basic_personal_amount 16129 "
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
    ontario_basic = position(
        "ontario_basic_tax on taxable_income 115000 (no rounding)", "8539.5965"
    )
    ontario_amount = position("basic_personal_amount: credit amount 12747 (no rounding)", "12747")
    ontario_amounts = position(
        "non_refundable_credit_amounts: basic_personal_amount 12747 "
        "+ cpp_base_contributions 3356.1 + ei_premiums 1077.48 = 17180.58",
        "17180.58",
    )
    ontario_credit = position(
        "non_refundable_tax_credits: 5.05% of non_refundable_credit_amounts 17180.58 (no rounding)",
        "867.61929",
    )
    ontario_after = position(
        "ontario_tax_after_credits: ontario_basic_tax 8539.5965 "
        "less non_refundable_tax_credits 867.61929, not below 0 = 7671.97721",
        "7671.97721",
    )
    surtax_first = position(
        "ontario_surtax: 20% of ontario_tax_after_credits 7671.97721 over 5710 (no rounding)",
        "392.395442",
    )
    surtax_second = position(
        "ontario_surtax: 36% of ontario_tax_after_credits 7671.97721 over 7307 (no rounding)",
        "131.3917956",
    )
    with_surtax = position(
        "ontario_tax_with_surtax: ontario_tax_after_credits 7671.97721 "
        "+ ontario_surtax 523.7872376 = 8195.7644476",
        "8195.7644476",
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
        "over ontario_tax_with_surtax 8195.7644476, not below 0 (no rounding)",
        "0",
    )
    after_reduction = position(
        "ontario_tax_after_reduction: ontario_tax_with_surtax 8195.7644476 "
        "less ontario_tax_reduction 0, not below 0 = 8195.7644476",
        "8195.7644476",
    )
    assert taxable_gains < total < net
    assert cpp_first < cpp_enhanced < deductions < net
    assert rrsp_available < rrsp < deductions
    assert cpp_second < cpp_enhanced
    assert cpp_base < federal_amounts
    assert cpp_base < ontario_amounts
    assert ei < federal_amounts
    assert ei < ontario_amounts
    assert net < taxable
    assert net_deductions < taxable
    assert taxable < federal_basic < federal_after
    assert taxable < ontario_basic
    assert ontario_basic < ontario_after
    assert net < federal_amount < federal_amounts < federal_credit < federal_after
    assert employment_amount < federal_amounts
    assert ontario_amount < ontario_amounts < ontario_credit < ontario_after
    assert ontario_after < surtax_first < surtax_second < with_surtax
    assert reduction_basic < reduction_amounts
    assert reduction_children < reduction_amounts
    assert reduction_dependants < reduction_amounts
    assert with_surtax < reduction < after_reduction
    assert reduction_amounts < reduction


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    trace = return_a().trace

    rated = {line.output: line for line in trace if isinstance(line, RateAppliedLine)}
    sums = {line.output: line for line in trace if isinstance(line, SumLine)}
    floored = {line.output: line for line in trace if isinstance(line, SubtractedNotBelowZeroLine)}
    totals = {line.output: line for line in trace if isinstance(line, RoundedTotalLine)}
    amounts = {line.output: line for line in trace if isinstance(line, CreditAmountLine)}
    tapered = {line.output: line for line in trace if isinstance(line, TaperedAmountLine)}
    capped = {line.output: line for line in trace if isinstance(line, CappedAmountLine)}
    tiers = {line.output: line for line in trace if isinstance(line, ContributionTierLine)}
    lesser = {line.output: line for line in trace if isinstance(line, LesserOfLine)}
    surcharged = [line for line in trace if isinstance(line, SurchargeTierLine)]
    per_unit = {line.output: line for line in trace if isinstance(line, PerUnitAmountLine)}
    multiples = {line.output: line for line in trace if isinstance(line, MultipleOverLine)}

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
                (CPP_BASE_CONTRIBUTIONS, D("3356.10")),
                (EI_PREMIUMS, D("1077.48")),
            ),
            D("17180.58"),
        ),
        # ON428 line 69 "Line 62 plus line 68": the Ontario tax after credits plus the surtax.
        ONTARIO_TAX_WITH_SURTAX: SumLine(
            ONTARIO_TAX_WITH_SURTAX,
            ((ONTARIO_TAX_AFTER_CREDITS, D("7671.97721")), (ONTARIO_SURTAX, D("523.7872376"))),
            D("8195.7644476"),
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
    }
    # ON428 line 78 "Amount from line 77 above multiplied by 2", line 79 "Amount from line 73
    # above" and line 80 "Line 78 minus line 79 (if negative, enter "0") Ontario tax reduction":
    # 588.00 is below the tax with surtax of 8195.7644476, so the reduction is 0.
    assert multiples == {
        ONTARIO_TAX_REDUCTION: MultipleOverLine(
            output=ONTARIO_TAX_REDUCTION,
            base=TAX_REDUCTION_AMOUNTS,
            base_amount=D("294.00"),
            factor=Factor(D("2")),
            less=ONTARIO_TAX_WITH_SURTAX,
            less_amount=D("8195.7644476"),
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
        )
    }
    # Schedule 7 line 20 "Enter whichever is less: amount from line 10 or line 19.": the
    # contributions available to deduct of 1926 are below the deduction limit of 19800, so the
    # deduction is the contributions available to deduct.
    assert lesser == {
        RRSP_DEDUCTION: LesserOfLine(
            RRSP_DEDUCTION,
            ((RRSP_CONTRIBUTIONS_AVAILABLE, D("1926")), (RRSP_DEDUCTION_LIMIT, D("19800"))),
            D("1926"),
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
            base_amount=D("7671.97721"),
            threshold=D("5710"),
            rate=Rate(D("0.20")),
            rounding=NO_ROUNDING,
            part=D("392.395442"),
        ),
        SurchargeTierLine(
            output=ONTARIO_SURTAX,
            base=ONTARIO_TAX_AFTER_CREDITS,
            base_amount=D("7671.97721"),
            threshold=D("7307"),
            rate=Rate(D("0.36")),
            rounding=NO_ROUNDING,
            part=D("131.3917956"),
        ),
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
            minuend_amount=D("8539.5965"),
            subtrahend=ontario.NON_REFUNDABLE_TAX_CREDITS,
            subtrahend_amount=D("867.61929"),
            result=D("7671.97721"),
        ),
        # ON428 line 81 "Line 73 minus line 80 (if negative, enter "0")".
        ONTARIO_TAX_AFTER_REDUCTION: SubtractedNotBelowZeroLine(
            output=ONTARIO_TAX_AFTER_REDUCTION,
            minuend=ONTARIO_TAX_WITH_SURTAX,
            minuend_amount=D("8195.7644476"),
            subtrahend=ONTARIO_TAX_REDUCTION,
            subtrahend_amount=D("0"),
            result=D("8195.7644476"),
        ),
    }

    assert totals[FEDERAL_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[FEDERAL_BASIC_TAX].base_amount == D("115000")
    assert totals[FEDERAL_BASIC_TAX].amount == D("20146.25")
    assert totals[ONTARIO_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[ONTARIO_BASIC_TAX].amount == D("8539.5965")


def test_each_capability_runs_after_what_it_consumes() -> None:
    order = service().compose(CA_ON, 2025).order

    assert len(order) == 32
    position = {kind: i for i, capability in enumerate(order) for kind in capability.produces}
    assert position[TAXABLE_CAPITAL_GAINS] < position[TOTAL_INCOME] < position[NET_INCOME]
    assert position[DEDUCTIONS_FROM_TOTAL_INCOME] < position[NET_INCOME]
    assert position[RRSP_CONTRIBUTIONS_AVAILABLE] < position[RRSP_DEDUCTION]
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
    )


def test_a_credit_larger_than_the_tax_leaves_zero_not_a_refund() -> None:
    # Employment income of 10000, with the CPP contributions computed by Schedule 8's tiers:
    # base 4.95% x (10000 - 3500) = 321.75, first additional 1% x 6500 = 65.00, no second
    # additional, so enhanced 65.00; the EI premiums computed from employment income, 1.64% x
    # 10000 = 164.00; no unused or new RRSP contributions, so the RRSP deduction is the lesser
    # of 0 and the deduction limit of 1800; the Canada employment amount is the lesser of 10000
    # and 1471.
    worksheet = compute("10000", "0", "0", "0", "1800", "0")

    assert worksheet.get(TOTAL_INCOME).value == D("10000")
    assert worksheet.get(CPP_BASE_CONTRIBUTIONS).value == D("321.75")
    assert worksheet.get(CPP_FIRST_ADDITIONAL_CONTRIBUTIONS).value == D("65.00")
    assert worksheet.get(CPP_SECOND_ADDITIONAL_CONTRIBUTIONS).value == D("0")
    assert worksheet.get(CPP_ENHANCED_CONTRIBUTIONS).value == D("65.00")
    assert worksheet.get(EI_PREMIUMS).value == D("164.00")
    assert worksheet.get(RRSP_CONTRIBUTIONS_AVAILABLE).value == D("0")
    assert worksheet.get(RRSP_DEDUCTION).value == D("0")
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


def test_the_tax_reduction_lowers_a_tax_below_twice_the_reduction_amounts() -> None:
    # Employment income of 24000, with no capital gain, no RRSP contributions and no union dues:
    # base CPP contributions 4.95% x (24000 - 3500) = 1014.75, first additional 1% x 20500 =
    # 205.00, EI premiums 1.64% x 24000 = 393.60; net and taxable income 23795.00; Ontario basic
    # tax 5.05% x 23795.00 = 1201.6475 less the Ontario credits 5.05% x (12747 + 1014.75 +
    # 393.60 = 14155.35) = 714.845175 is 486.802325, below the first surtax threshold, so the
    # Ontario tax with surtax (ON428 line 73) is 486.802325. With no dependent children and no
    # dependants, line 78 is 2 x 294.00 = 588.00, and line 80 is 588.00 - 486.802325 =
    # 101.197675; line 81 is 486.802325 - 101.197675 = 385.604650.
    worksheet = compute("24000", "0", "0", "0", "4320", "0")

    assert worksheet.get(ONTARIO_TAX_WITH_SURTAX).value == D("486.802325")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("294.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("101.197675")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("385.604650")


def test_dependent_children_and_dependants_raise_the_tax_reduction() -> None:
    # Return A's amounts with five dependent children (ON428 line 75, line 60969) and three
    # dependants (line 76, line 60970): line 75 is 5 x 544 = 2720, line 76 is 3 x 544 = 1632,
    # line 77 is 294.00 + 2720 + 1632 = 4646.00 and line 78 is 9292.00; line 80 is 9292.00 -
    # 8195.7644476 = 1096.2355524, and line 81 is 8195.7644476 - 1096.2355524 = 7099.5288952.
    worksheet = compute(
        "110000", "20000", "0", "1926", "19800", "2000", dependent_children=5, dependants=3
    )

    assert worksheet.get(DEPENDENT_CHILDREN).value == 5
    assert worksheet.get(DEPENDANTS).value == 3
    assert worksheet.get(TAX_REDUCTION_FOR_CHILDREN).value == D("2720")
    assert worksheet.get(TAX_REDUCTION_FOR_DEPENDANTS).value == D("1632")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("4646.00")
    assert worksheet.get(ONTARIO_TAX_WITH_SURTAX).value == D("8195.7644476")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("1096.2355524")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("7099.5288952")


def test_contributions_above_the_deduction_limit_deduct_the_limit() -> None:
    # Schedule 7 line 20 "Enter whichever is less: amount from line 10 or line 19.": Return A's
    # amounts with contributions of 25000, above the deduction limit of 19800, so the deduction
    # is the limit; total deductions are 19800 + 2000 + 1074.00 = 22874.00.
    worksheet = compute("110000", "20000", "0", "25000", "19800", "2000")

    assert worksheet.get(RRSP_DEDUCTION).value == D("19800")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("22874.00")
    assert worksheet.get(NET_INCOME).value == D("97126.00")


def test_unused_contributions_and_no_new_ones_still_deduct() -> None:
    # Schedule 7 line 5 "Line 1 plus line 4 ... Total contributions" and line 20 "Enter
    # whichever is less: amount from line 10 or line 19.": Return A's amounts with unused
    # contributions of 5000 from earlier years (line 1) and no new contributions (line 4), so
    # the contributions available to deduct (line 10) are 5000 + 0 = 5000, below the deduction
    # limit of 19800, and the deduction is 5000; total deductions are 5000 + 2000 + 1074.00 =
    # 8074.00.
    worksheet = compute("110000", "20000", "5000", "0", "19800", "2000")

    assert worksheet.get(RRSP_CONTRIBUTIONS_AVAILABLE).value == D("5000")
    assert worksheet.get(RRSP_DEDUCTION).value == D("5000")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("8074.00")
    assert worksheet.get(NET_INCOME).value == D("111926.00")
