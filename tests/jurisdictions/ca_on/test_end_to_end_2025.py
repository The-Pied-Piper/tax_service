"""CA-ON 2025, end to end: CRA's worked example computed from the manifest through the service.

The service is the one the composition root builds (`build_tax_computation`): the real YAML
sources over the jurisdiction packages and the shared registries. Return A's amounts (employment
income 110000 and a capital gain of 20000 to total income 120000; the CPP contributions computed
from employment income by Schedule 8's tiers, each at its maximum: base 3356.10, first additional
678.00 and second additional 396.00, the enhanced contributions 1074.00; the EI premiums computed
from employment income, at the maximum 1077.48; the RRSP deduction of 1926, the lesser of the
contributions of 1926 and the deduction limit of 19800 (Schedule 7 line 20); less that RRSP
deduction, union dues of 2000 and the enhanced contributions to net income 115000, less no
deductions from net income to taxable income 115000, and from each basic personal amount (16129
federal, 12747 Ontario) plus the base CPP contributions and the EI premiums, and federally the
Canada employment amount of 1471 (the lesser of employment income and 1471), through each total of
credit amounts and each form's non-refundable tax credits (T1 line 35000, ON428 line 61500) to each
tax after credits, and the Ontario surtax on the Ontario tax after credits (ON428 lines 66 to 68) to
the Ontario tax with surtax of line 69) are checked from the files under `returns/` by
`test_worked_returns.py`, as are Returns C and D; this module pins which capability produces each
line, the order, and the trace that explains them.
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
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.tiered_surcharge import TieredSurcharge
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.parameters.amount import Amount
from app.domain.parameters.contribution_tier import ContributionTier
from app.domain.parameters.credit import Credit
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundTo
from app.domain.trace import (
    CappedAmountLine,
    ContributionTierLine,
    CreditAmountLine,
    LesserOfLine,
    RateAppliedLine,
    RoundedTotalLine,
    SubtractedNotBelowZeroLine,
    SumLine,
    SurchargeTierLine,
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
    RRSP_DEDUCTION,
    RRSP_DEDUCTION_LIMIT,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    UNION_DUES,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    ONTARIO_BASIC_TAX,
    ONTARIO_SURTAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_WITH_SURTAX,
)
from app.main import build_tax_computation

D = Decimal
CA_ON = JurisdictionCode("CA-ON")
# Schedule 8 Part 3a lines 25 and 28: "(in dollars and cents)"; the EI premiums are in dollars and
# cents too.
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)


def service() -> TaxComputationService:
    return build_tax_computation()


def compute(
    employment_income: str,
    capital_gain: str,
    rrsp_contributions: str,
    rrsp_deduction_limit: str,
    union_dues: str,
) -> Worksheet:
    return service().compute(
        CA_ON,
        2025,
        Artifact(EMPLOYMENT_INCOME, D(employment_income)),
        Artifact(CAPITAL_GAIN, D(capital_gain)),
        Artifact(RRSP_CONTRIBUTIONS, D(rrsp_contributions)),
        Artifact(RRSP_DEDUCTION_LIMIT, D(rrsp_deduction_limit)),
        Artifact(UNION_DUES, D(union_dues)),
    )


def return_a() -> Worksheet:
    """Return A's inputs, as in `returns/2025_return_a.yaml`."""
    return compute("110000", "20000", "1926", "19800", "2000")


def test_each_amount_is_produced_by_its_capability() -> None:
    worksheet = return_a()

    assert worksheet.producer_of(EMPLOYMENT_INCOME) is None
    assert worksheet.producer_of(CAPITAL_GAIN) is None
    assert worksheet.producer_of(RRSP_CONTRIBUTIONS) is None
    assert worksheet.producer_of(RRSP_DEDUCTION_LIMIT) is None
    assert worksheet.producer_of(UNION_DUES) is None
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
    assert isinstance(worksheet.producer_of(BASIC_PERSONAL_AMOUNT), CreditAmount)
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
    rrsp = position(
        "rrsp_deduction: lesser of rrsp_contributions 1926 and rrsp_deduction_limit 19800 = 1926",
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
    federal_amount = position("basic_personal_amount: credit amount 16129 (no rounding)", "16129")
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
    assert taxable_gains < total < net
    assert cpp_first < cpp_enhanced < deductions < net
    assert rrsp < deductions
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
    assert federal_amount < federal_amounts < federal_credit < federal_after
    assert employment_amount < federal_amounts
    assert ontario_amount < ontario_amounts < ontario_credit < ontario_after
    assert ontario_after < surtax_first < surtax_second < with_surtax


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    trace = return_a().trace

    rated = {line.output: line for line in trace if isinstance(line, RateAppliedLine)}
    sums = {line.output: line for line in trace if isinstance(line, SumLine)}
    floored = {line.output: line for line in trace if isinstance(line, SubtractedNotBelowZeroLine)}
    totals = {line.output: line for line in trace if isinstance(line, RoundedTotalLine)}
    amounts = {line.output: line for line in trace if isinstance(line, CreditAmountLine)}
    capped = {line.output: line for line in trace if isinstance(line, CappedAmountLine)}
    tiers = {line.output: line for line in trace if isinstance(line, ContributionTierLine)}
    lesser = {line.output: line for line in trace if isinstance(line, LesserOfLine)}
    surcharged = [line for line in trace if isinstance(line, SurchargeTierLine)]

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
    }
    assert amounts == {
        BASIC_PERSONAL_AMOUNT: CreditAmountLine(
            BASIC_PERSONAL_AMOUNT, Credit(amount=D("16129")), NO_ROUNDING, D("16129")
        ),
        ontario.BASIC_PERSONAL_AMOUNT: CreditAmountLine(
            ontario.BASIC_PERSONAL_AMOUNT, Credit(amount=D("12747")), NO_ROUNDING, D("12747")
        ),
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
    # contributions of 1926 are below the deduction limit of 19800, so the deduction is the
    # contributions.
    assert lesser == {
        RRSP_DEDUCTION: LesserOfLine(
            RRSP_DEDUCTION,
            ((RRSP_CONTRIBUTIONS, D("1926")), (RRSP_DEDUCTION_LIMIT, D("19800"))),
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
    }

    assert totals[FEDERAL_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[FEDERAL_BASIC_TAX].base_amount == D("115000")
    assert totals[FEDERAL_BASIC_TAX].amount == D("20146.25")
    assert totals[ONTARIO_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[ONTARIO_BASIC_TAX].amount == D("8539.5965")


def test_each_capability_runs_after_what_it_consumes() -> None:
    order = service().compose(CA_ON, 2025).order

    assert len(order) == 25
    position = {kind: i for i, capability in enumerate(order) for kind in capability.produces}
    assert position[TAXABLE_CAPITAL_GAINS] < position[TOTAL_INCOME] < position[NET_INCOME]
    assert position[DEDUCTIONS_FROM_TOTAL_INCOME] < position[NET_INCOME]
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


def test_a_credit_larger_than_the_tax_leaves_zero_not_a_refund() -> None:
    # Employment income of 10000, with the CPP contributions computed by Schedule 8's tiers:
    # base 4.95% x (10000 - 3500) = 321.75, first additional 1% x 6500 = 65.00, no second
    # additional, so enhanced 65.00; the EI premiums computed from employment income, 1.64% x
    # 10000 = 164.00; no RRSP contributions, so the RRSP deduction is the lesser of 0 and the
    # deduction limit of 1800; the Canada employment amount is the lesser of 10000 and 1471.
    worksheet = compute("10000", "0", "0", "1800", "0")

    assert worksheet.get(TOTAL_INCOME).value == D("10000")
    assert worksheet.get(CPP_BASE_CONTRIBUTIONS).value == D("321.75")
    assert worksheet.get(CPP_FIRST_ADDITIONAL_CONTRIBUTIONS).value == D("65.00")
    assert worksheet.get(CPP_SECOND_ADDITIONAL_CONTRIBUTIONS).value == D("0")
    assert worksheet.get(CPP_ENHANCED_CONTRIBUTIONS).value == D("65.00")
    assert worksheet.get(EI_PREMIUMS).value == D("164.00")
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


def test_contributions_above_the_deduction_limit_deduct_the_limit() -> None:
    # Schedule 7 line 20 "Enter whichever is less: amount from line 10 or line 19.": Return A's
    # amounts with contributions of 25000, above the deduction limit of 19800, so the deduction
    # is the limit; total deductions are 19800 + 2000 + 1074.00 = 22874.00.
    worksheet = compute("110000", "20000", "25000", "19800", "2000")

    assert worksheet.get(RRSP_DEDUCTION).value == D("19800")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("22874.00")
    assert worksheet.get(NET_INCOME).value == D("97126.00")
