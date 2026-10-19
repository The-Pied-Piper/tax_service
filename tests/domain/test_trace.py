"""Unit tests for the structured trace: one frozen line class per fact, with made-up values.

Each line records what happened with the domain objects involved (`ArtifactKind`, `Rate`,
`Credit`, `Amount`, `ContributionTier`, `Taper`, `Factor`, `Fraction`, `RoundingRule`), never
text; its `amount` is the figure the line is about. A count is an `int` artifact kind and its
`int` value.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields
from decimal import Decimal
from fractions import Fraction as ExactFraction
from typing import Any, cast

import pytest

from app.domain.artifact import ArtifactKind
from app.domain.parameters.amount import Amount
from app.domain.parameters.contribution_tier import ContributionTier
from app.domain.parameters.credit import Credit
from app.domain.parameters.factor import Factor
from app.domain.parameters.fraction import Fraction
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundTo
from app.domain.parameters.taper import Taper
from app.domain.trace import (
    AtMostLine,
    BracketColumnLine,
    CappedAmountLine,
    ChosenByCountLine,
    ChosenByRangeLine,
    ContributionTierLine,
    CreditAmountLine,
    FractionAppliedLine,
    LesserOfLine,
    MultipleOverLine,
    PerUnitAmountLine,
    RateAppliedLine,
    RecordTotalLine,
    RoundedTotalLine,
    SubtractedLine,
    SubtractedNotBelowZeroLine,
    SumLine,
    SurchargeTierLine,
    TaperedAmountLine,
    TimesCountLine,
    TraceLine,
)

D = Decimal
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)
BASE = ArtifactKind("ex/base", Decimal)
TAX = ArtifactKind("ex/tax", Decimal)
PART_ONE = ArtifactKind("ex/part_one", Decimal)
PART_TWO = ArtifactKind("ex/part_two", Decimal)
TOTAL = ArtifactKind("ex/total", Decimal)
RATED = ArtifactKind("ex/rated", Decimal)
GROSS = ArtifactKind("ex/gross", Decimal)
REDUCTION = ArtifactKind("ex/reduction", Decimal)
NET = ArtifactKind("ex/net", Decimal)
PERSONAL = ArtifactKind("ex/personal_amount", Decimal)
CAPPED = ArtifactKind("ex/capped", Decimal)
LESSER = ArtifactKind("ex/lesser", Decimal)
EARNINGS = ArtifactKind("ex/earnings", Decimal)
CONTRIBUTION = ArtifactKind("ex/contribution", Decimal)
TIER = ContributionTier(Rate(D("0.05")), D(3000), D(50000), D(2350))
SURCHARGE = ArtifactKind("ex/surcharge", Decimal)
INCOME = ArtifactKind("ex/income", Decimal)
TAPER = Taper(D(1000), D(500), D(20000), D(10000))
CHILDREN = ArtifactKind("ex/child_count", int)
CHILD_AMOUNT = ArtifactKind("ex/child_amount", Decimal)
CLAIMED = ArtifactKind("ex/claimed_amount", Decimal)
LIMIT = ArtifactKind("ex/claim_limit", Decimal)
ALLOWED = ArtifactKind("ex/allowed_amount", Decimal)
EARNED = ArtifactKind("ex/earned_income", Decimal)
PORTION = ArtifactKind("ex/earned_portion", Decimal)
EACH = ArtifactKind("ex/amount_each", Decimal)
PERSONS = ArtifactKind("ex/person_count", int)
CLAIMED_FOR_ALL = ArtifactKind("ex/amount_claimed", Decimal)
DEPENDANTS = ArtifactKind("ex/dependant_count", int)
ALONE = ArtifactKind("ex/amount_alone", Decimal)
WITH_FAMILY = ArtifactKind("ex/amount_with_family", Decimal)
CHOSEN = ArtifactKind("ex/amount_chosen", Decimal)
ITEM_AMOUNT = ArtifactKind("ex/item_amount", Decimal)
TESTED = ArtifactKind("ex/amount_tested", Decimal)
IN_THE_FIRST_RANGE = ArtifactKind("ex/amount_in_the_first_range", Decimal)
IN_THE_SECOND_RANGE = ArtifactKind("ex/amount_in_the_second_range", Decimal)


def column_line() -> BracketColumnLine:
    return BracketColumnLine(D(100), D("0.20"), D(150), D("10.00"), D("40.00"))


def total_line() -> RoundedTotalLine:
    return RoundedTotalLine(TAX, BASE, D(250), CENT, D("40.00"))


def sum_line() -> SumLine:
    return SumLine(TOTAL, ((PART_ONE, D("1.25")), (PART_TWO, D(2))), D("3.25"))


def rate_applied_line() -> RateAppliedLine:
    return RateAppliedLine(RATED, BASE, D("200.01"), Rate(D("0.5")), CENT, D("100.01"))


def subtracted_line() -> SubtractedLine:
    return SubtractedLine(NET, GROSS, D("100.25"), REDUCTION, D(40), D("60.25"))


def subtracted_not_below_zero_line() -> SubtractedNotBelowZeroLine:
    return SubtractedNotBelowZeroLine(NET, GROSS, D(10), REDUCTION, D("25.5"), D(0))


def credit_amount_line() -> CreditAmountLine:
    return CreditAmountLine(PERSONAL, Credit(D("1000.005")), CENT, D("1000.01"))


def capped_amount_line() -> CappedAmountLine:
    return CappedAmountLine(CAPPED, GROSS, D("1500.25"), Amount(D(1000)), CENT, D("1000.00"))


def lesser_of_line() -> LesserOfLine:
    return LesserOfLine(LESSER, ((PART_ONE, D("100.25")), (PART_TWO, D(40))), D(40))


def contribution_tier_line() -> ContributionTierLine:
    return ContributionTierLine(
        CONTRIBUTION, EARNINGS, D("23000.10"), TIER, CENT, D("20000.10"), D("1000.01")
    )


def surcharge_tier_line() -> SurchargeTierLine:
    return SurchargeTierLine(SURCHARGE, TAX, D("400.25"), D(300), Rate(D("0.25")), CENT, D("25.06"))


def capped_surcharge_tier_line() -> SurchargeTierLine:
    return SurchargeTierLine(
        SURCHARGE, TAX, D("400.25"), D(300), Rate(D("0.25")), CENT, D("25.06"), D(30)
    )


def tapered_amount_line() -> TaperedAmountLine:
    return TaperedAmountLine(
        PERSONAL, INCOME, D("22000.5"), TAPER, CENT, ExactFraction("100.025"), D("1399.98")
    )


def per_unit_amount_line() -> PerUnitAmountLine:
    return PerUnitAmountLine(CHILD_AMOUNT, CHILDREN, 2, Amount(D(544)), CENT, D(1088))


def multiple_over_line() -> MultipleOverLine:
    return MultipleOverLine(
        REDUCTION, TOTAL, D(294), Factor(D(2)), TAX, D("100.25"), CENT, D("487.75")
    )


def at_most_line() -> AtMostLine:
    return AtMostLine(ALLOWED, CLAIMED, D("1500.25"), LIMIT, D(1926))


def fraction_applied_line() -> FractionAppliedLine:
    return FractionAppliedLine(PORTION, EARNED, D(50000), Fraction(2, 3), CENT, D("33333.33"))


def times_count_line() -> TimesCountLine:
    return TimesCountLine(CLAIMED_FOR_ALL, EACH, D("16129.50"), PERSONS, 2, D("32259.00"))


def chosen_by_count_line() -> ChosenByCountLine:
    return ChosenByCountLine(CHOSEN, DEPENDANTS, 1, WITH_FAMILY, D("2813.00"))


def record_total_line() -> RecordTotalLine:
    return RecordTotalLine(TOTAL, ITEM_AMOUNT, (D("6000"), D("4000.50")), D("10000.50"))


def chosen_by_range_line() -> ChosenByRangeLine:
    return ChosenByRangeLine(CHOSEN, TESTED, D("1000.00"), IN_THE_SECOND_RANGE, D("625.01"))


ALL_LINES = [
    column_line,
    total_line,
    sum_line,
    rate_applied_line,
    subtracted_line,
    subtracted_not_below_zero_line,
    credit_amount_line,
    capped_amount_line,
    lesser_of_line,
    contribution_tier_line,
    surcharge_tier_line,
    tapered_amount_line,
    per_unit_amount_line,
    multiple_over_line,
    at_most_line,
    fraction_applied_line,
    times_count_line,
    chosen_by_count_line,
    record_total_line,
    chosen_by_range_line,
]


def test_the_base_line_cannot_be_built() -> None:
    with pytest.raises(TypeError):
        cast(Any, TraceLine)()


@pytest.mark.parametrize("make", ALL_LINES)
def test_every_line_is_a_trace_line(make: Any) -> None:
    assert isinstance(make(), TraceLine)


@pytest.mark.parametrize("make", ALL_LINES)
def test_lines_are_equal_by_value(make: Any) -> None:
    assert make() == make()
    assert make() is not make()


@pytest.mark.parametrize("make", ALL_LINES)
def test_lines_are_frozen(make: Any) -> None:
    line = make()
    with pytest.raises(FrozenInstanceError):
        setattr(line, fields(line)[0].name, D(1))


def test_bracket_column_line_fields_in_order() -> None:
    line = column_line()

    assert line == BracketColumnLine(
        lower=D(100), rate=D("0.20"), excess=D(150), tax_at_start=D("10.00"), tax=D("40.00")
    )
    assert [f.name for f in fields(line)] == ["lower", "rate", "excess", "tax_at_start", "tax"]
    assert (line.lower, line.rate, line.excess, line.tax_at_start, line.tax) == (
        D(100),
        D("0.20"),
        D(150),
        D("10.00"),
        D("40.00"),
    )
    assert line.amount == D("40.00")


def test_bracket_column_line_has_no_upper_bound() -> None:
    assert "upper" not in [f.name for f in fields(BracketColumnLine)]


def test_bracket_column_lines_differ_by_any_field() -> None:
    line = column_line()

    assert line != BracketColumnLine(D(0), D("0.20"), D(150), D("10.00"), D("40.00"))
    assert line != BracketColumnLine(D(100), D("0.25"), D(150), D("10.00"), D("40.00"))
    assert line != BracketColumnLine(D(100), D("0.20"), D(140), D("10.00"), D("40.00"))
    assert line != BracketColumnLine(D(100), D("0.20"), D(150), D("10.01"), D("40.00"))
    assert line != BracketColumnLine(D(100), D("0.20"), D(150), D("10.00"), D("40.01"))


def test_rounded_total_line_fields_in_order() -> None:
    line = total_line()

    assert line == RoundedTotalLine(
        output=TAX, base=BASE, base_amount=D(250), rounding=CENT, total=D("40.00")
    )
    assert line.output is TAX
    assert line.base is BASE
    assert line.base_amount == D(250)
    assert line.rounding == CENT
    assert line.total == D("40.00")
    assert line.amount == D("40.00")


def test_rounded_total_lines_differ_by_rounding() -> None:
    assert total_line() != RoundedTotalLine(TAX, BASE, D(250), NO_ROUNDING, D("40.00"))


def test_sum_line_fields_in_order() -> None:
    line = sum_line()

    assert line == SumLine(
        output=TOTAL, parts=((PART_ONE, D("1.25")), (PART_TWO, D(2))), total=D("3.25")
    )
    assert [f.name for f in fields(line)] == ["output", "parts", "total"]
    assert line.output is TOTAL
    assert line.parts == ((PART_ONE, D("1.25")), (PART_TWO, D(2)))
    assert line.total == D("3.25")
    assert line.amount == D("3.25")


def test_sum_line_may_have_no_parts() -> None:
    line = SumLine(TOTAL, (), D(0))

    assert line.parts == ()
    assert line.amount == D(0)


def test_sum_lines_differ_by_the_order_of_their_parts() -> None:
    assert sum_line() != SumLine(TOTAL, ((PART_TWO, D(2)), (PART_ONE, D("1.25"))), D("3.25"))


def test_sum_lines_are_hashable() -> None:
    assert hash(sum_line()) == hash(sum_line())


def test_rate_applied_line_fields_in_order() -> None:
    line = rate_applied_line()

    assert line == RateAppliedLine(
        output=RATED,
        base=BASE,
        base_amount=D("200.01"),
        rate=Rate(D("0.5")),
        rounding=CENT,
        result=D("100.01"),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "base",
        "base_amount",
        "rate",
        "rounding",
        "result",
    ]
    assert line.output is RATED
    assert line.base is BASE
    assert line.base_amount == D("200.01")
    assert line.rate == Rate(D("0.5"))
    assert line.rounding == CENT
    assert line.result == D("100.01")
    assert line.amount == D("100.01")


def test_rate_applied_lines_differ_by_rounding() -> None:
    assert rate_applied_line() != RateAppliedLine(
        RATED, BASE, D("200.01"), Rate(D("0.5")), NO_ROUNDING, D("100.01")
    )


def test_rate_applied_lines_are_hashable() -> None:
    assert hash(rate_applied_line()) == hash(rate_applied_line())


def test_subtracted_line_fields_in_order() -> None:
    line = subtracted_line()

    assert line == SubtractedLine(
        output=NET,
        minuend=GROSS,
        minuend_amount=D("100.25"),
        subtrahend=REDUCTION,
        subtrahend_amount=D(40),
        result=D("60.25"),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "minuend",
        "minuend_amount",
        "subtrahend",
        "subtrahend_amount",
        "result",
    ]
    assert line.output is NET
    assert line.minuend is GROSS
    assert line.minuend_amount == D("100.25")
    assert line.subtrahend is REDUCTION
    assert line.subtrahend_amount == D(40)
    assert line.result == D("60.25")
    assert line.amount == D("60.25")


def test_subtracted_line_may_hold_a_negative_result() -> None:
    line = SubtractedLine(NET, GROSS, D(10), REDUCTION, D("25.5"), D("-15.5"))

    assert line.result == D("-15.5")
    assert line.amount == D("-15.5")


def test_subtracted_lines_differ_by_which_kind_is_taken_off() -> None:
    assert subtracted_line() != SubtractedLine(
        NET, REDUCTION, D("100.25"), GROSS, D(40), D("60.25")
    )


def test_subtracted_lines_are_hashable() -> None:
    assert hash(subtracted_line()) == hash(subtracted_line())


def test_subtracted_not_below_zero_line_fields_in_order() -> None:
    line = subtracted_not_below_zero_line()

    assert line == SubtractedNotBelowZeroLine(
        output=NET,
        minuend=GROSS,
        minuend_amount=D(10),
        subtrahend=REDUCTION,
        subtrahend_amount=D("25.5"),
        result=D(0),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "minuend",
        "minuend_amount",
        "subtrahend",
        "subtrahend_amount",
        "result",
    ]
    assert line.output is NET
    assert line.minuend is GROSS
    assert line.minuend_amount == D(10)
    assert line.subtrahend is REDUCTION
    assert line.subtrahend_amount == D("25.5")
    assert line.result == D(0)
    assert line.amount == D(0)


def test_subtracted_not_below_zero_line_may_hold_a_positive_result() -> None:
    line = SubtractedNotBelowZeroLine(NET, GROSS, D("100.25"), REDUCTION, D(40), D("60.25"))

    assert line.result == D("60.25")
    assert line.amount == D("60.25")


def test_subtracted_not_below_zero_lines_differ_by_which_kind_is_taken_off() -> None:
    assert subtracted_not_below_zero_line() != SubtractedNotBelowZeroLine(
        NET, REDUCTION, D(10), GROSS, D("25.5"), D(0)
    )


def test_subtracted_not_below_zero_lines_are_hashable() -> None:
    assert hash(subtracted_not_below_zero_line()) == hash(subtracted_not_below_zero_line())


def test_a_floored_subtraction_is_not_a_plain_subtracted_line() -> None:
    # The class says the floor applied, so the same fields in the two classes are not equal.
    floored = SubtractedNotBelowZeroLine(NET, GROSS, D("100.25"), REDUCTION, D(40), D("60.25"))

    assert cast(Any, floored) != subtracted_line()


def test_credit_amount_line_fields_in_order() -> None:
    line = credit_amount_line()

    assert line == CreditAmountLine(
        output=PERSONAL, basis=Credit(D("1000.005")), rounding=CENT, value=D("1000.01")
    )
    assert [f.name for f in fields(line)] == ["output", "basis", "rounding", "value"]
    assert line.output is PERSONAL
    assert line.basis == Credit(D("1000.005"))
    assert line.rounding == CENT
    # Settled: `value` is the rounded amount, not the dataset's; the inherited `amount` returns it.
    assert line.value == D("1000.01")
    assert line.amount == line.value


def test_credit_amount_line_may_hold_an_unrounded_amount() -> None:
    line = CreditAmountLine(PERSONAL, Credit(D("1000.005")), NO_ROUNDING, D("1000.005"))

    assert line.rounding == NO_ROUNDING
    assert line.value == D("1000.005")
    assert line.amount == line.value


def test_credit_amount_lines_differ_by_rounding() -> None:
    assert credit_amount_line() != CreditAmountLine(
        PERSONAL, Credit(D("1000.005")), NO_ROUNDING, D("1000.01")
    )


def test_credit_amount_lines_differ_by_value() -> None:
    assert credit_amount_line() != CreditAmountLine(
        PERSONAL, Credit(D("1000.005")), CENT, D("1000.00")
    )


def test_credit_amount_lines_are_hashable() -> None:
    assert hash(credit_amount_line()) == hash(credit_amount_line())


def test_a_credit_amount_lines_amount_is_not_one_of_its_fields() -> None:
    assert "amount" not in [f.name for f in fields(credit_amount_line())]


def test_capped_amount_line_fields_in_order() -> None:
    line = capped_amount_line()

    assert line == CappedAmountLine(
        output=CAPPED,
        base=GROSS,
        base_amount=D("1500.25"),
        cap=Amount(D(1000)),
        rounding=CENT,
        result=D("1000.00"),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "base",
        "base_amount",
        "cap",
        "rounding",
        "result",
    ]
    assert line.output is CAPPED
    assert line.base is GROSS
    assert line.base_amount == D("1500.25")
    assert line.cap == Amount(D(1000))
    assert line.rounding == CENT
    assert line.result == D("1000.00")
    assert line.amount == D("1000.00")


def test_capped_amount_line_may_hold_a_base_below_the_cap() -> None:
    line = CappedAmountLine(CAPPED, GROSS, D("400.25"), Amount(D(1000)), NO_ROUNDING, D("400.25"))

    assert line.result == D("400.25")
    assert line.amount == D("400.25")


def test_capped_amount_lines_differ_by_cap() -> None:
    assert capped_amount_line() != CappedAmountLine(
        CAPPED, GROSS, D("1500.25"), Amount(D(1200)), CENT, D("1000.00")
    )


def test_capped_amount_lines_differ_by_rounding() -> None:
    assert capped_amount_line() != CappedAmountLine(
        CAPPED, GROSS, D("1500.25"), Amount(D(1000)), NO_ROUNDING, D("1000.00")
    )


def test_capped_amount_lines_are_hashable() -> None:
    assert hash(capped_amount_line()) == hash(capped_amount_line())


def test_lesser_of_line_fields_in_order() -> None:
    line = lesser_of_line()

    assert line == LesserOfLine(
        output=LESSER, parts=((PART_ONE, D("100.25")), (PART_TWO, D(40))), result=D(40)
    )
    assert [f.name for f in fields(line)] == ["output", "parts", "result"]
    assert line.output is LESSER
    assert line.parts == ((PART_ONE, D("100.25")), (PART_TWO, D(40)))
    assert line.result == D(40)
    assert line.amount == D(40)


def test_lesser_of_line_may_have_one_part() -> None:
    line = LesserOfLine(LESSER, ((PART_ONE, D("1.25")),), D("1.25"))

    assert line.parts == ((PART_ONE, D("1.25")),)
    assert line.amount == D("1.25")


def test_lesser_of_lines_differ_by_the_order_of_their_parts() -> None:
    assert lesser_of_line() != LesserOfLine(
        LESSER, ((PART_TWO, D(40)), (PART_ONE, D("100.25"))), D(40)
    )


def test_lesser_of_lines_differ_by_result() -> None:
    assert lesser_of_line() != LesserOfLine(
        LESSER, ((PART_ONE, D("100.25")), (PART_TWO, D(40))), D("100.25")
    )


def test_lesser_of_lines_are_hashable() -> None:
    assert hash(lesser_of_line()) == hash(lesser_of_line())


def test_a_lesser_of_line_is_not_a_sum_line_nor_a_capped_amount_line() -> None:
    assert not isinstance(lesser_of_line(), SumLine)
    assert not isinstance(lesser_of_line(), CappedAmountLine)
    assert cast(Any, lesser_of_line()) != SumLine(
        LESSER, ((PART_ONE, D("100.25")), (PART_TWO, D(40))), D(40)
    )


def test_contribution_tier_line_fields_in_order() -> None:
    line = contribution_tier_line()

    assert line == ContributionTierLine(
        output=CONTRIBUTION,
        earnings=EARNINGS,
        earnings_amount=D("23000.10"),
        tier=TIER,
        rounding=CENT,
        contributory=D("20000.10"),
        result=D("1000.01"),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "earnings",
        "earnings_amount",
        "tier",
        "rounding",
        "contributory",
        "result",
    ]
    assert line.output is CONTRIBUTION
    assert line.earnings is EARNINGS
    assert line.earnings_amount == D("23000.10")
    assert line.tier == TIER
    assert line.rounding == CENT
    assert line.contributory == D("20000.10")
    assert line.result == D("1000.01")
    assert line.amount == D("1000.01")


def test_contribution_tier_line_may_hold_zero_contributory_earnings() -> None:
    line = ContributionTierLine(CONTRIBUTION, EARNINGS, D("-500"), TIER, NO_ROUNDING, D(0), D(0))

    assert line.earnings_amount == D("-500")
    assert line.contributory == D(0)
    assert line.amount == D(0)


def test_contribution_tier_lines_differ_by_tier() -> None:
    other = ContributionTier(Rate(D("0.05")), D(3000), D(50000), D(2000))

    assert contribution_tier_line() != ContributionTierLine(
        CONTRIBUTION, EARNINGS, D("23000.10"), other, CENT, D("20000.10"), D("1000.01")
    )


def test_contribution_tier_lines_differ_by_rounding() -> None:
    assert contribution_tier_line() != ContributionTierLine(
        CONTRIBUTION, EARNINGS, D("23000.10"), TIER, NO_ROUNDING, D("20000.10"), D("1000.01")
    )


def test_contribution_tier_lines_differ_by_contributory_earnings() -> None:
    assert contribution_tier_line() != ContributionTierLine(
        CONTRIBUTION, EARNINGS, D("23000.10"), TIER, CENT, D("20000"), D("1000.01")
    )


def test_contribution_tier_lines_are_hashable() -> None:
    assert hash(contribution_tier_line()) == hash(contribution_tier_line())


def test_a_contribution_tier_lines_amount_is_not_one_of_its_fields() -> None:
    assert "amount" not in [f.name for f in fields(contribution_tier_line())]


def test_a_contribution_tier_line_is_not_a_rate_applied_or_capped_amount_line() -> None:
    line = contribution_tier_line()

    assert not isinstance(line, RateAppliedLine)
    assert not isinstance(line, CappedAmountLine)


def test_surcharge_tier_line_fields_in_order() -> None:
    line = surcharge_tier_line()

    assert line == SurchargeTierLine(
        output=SURCHARGE,
        base=TAX,
        base_amount=D("400.25"),
        threshold=D(300),
        rate=Rate(D("0.25")),
        rounding=CENT,
        part=D("25.06"),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "base",
        "base_amount",
        "threshold",
        "rate",
        "rounding",
        "part",
        "maximum",
    ]
    assert line.output is SURCHARGE
    assert line.base is TAX
    # `base_amount` is the whole base, not the part of it over the threshold.
    assert line.base_amount == D("400.25")
    assert line.threshold == D(300)
    assert line.rate == Rate(D("0.25"))
    assert line.rounding == CENT
    assert line.part == D("25.06")
    assert line.amount == D("25.06")


def test_surcharge_tier_line_may_hold_a_zero_part() -> None:
    # A base that does not reach the threshold still gets its tier's line, with nothing charged.
    line = SurchargeTierLine(SURCHARGE, TAX, D(200), D(300), Rate(D("0.25")), NO_ROUNDING, D(0))

    assert line.part == D(0)
    assert line.amount == D(0)


def test_surcharge_tier_line_has_no_maximum_by_default() -> None:
    assert surcharge_tier_line().maximum is None


def test_surcharge_tier_line_holds_its_tiers_maximum() -> None:
    line = SurchargeTierLine(
        SURCHARGE, TAX, D("400.25"), D(300), Rate(D("0.25")), CENT, D("20"), D("20")
    )

    assert line.maximum == D("20")
    # The capped part is still the line's amount.
    assert line.amount == D("20")


def test_surcharge_tier_line_takes_its_maximum_by_keyword() -> None:
    line = SurchargeTierLine(
        output=SURCHARGE,
        base=TAX,
        base_amount=D("400.25"),
        threshold=D(300),
        rate=Rate(D("0.25")),
        rounding=CENT,
        part=D("0"),
        maximum=D(0),
    )

    assert line.maximum == D(0)


def test_surcharge_tier_lines_differ_by_maximum() -> None:
    assert surcharge_tier_line() != capped_surcharge_tier_line()
    assert capped_surcharge_tier_line() != SurchargeTierLine(
        SURCHARGE, TAX, D("400.25"), D(300), Rate(D("0.25")), CENT, D("25.06"), D(40)
    )


def test_surcharge_tier_lines_with_a_maximum_are_hashable() -> None:
    assert hash(capped_surcharge_tier_line()) == hash(capped_surcharge_tier_line())


def test_surcharge_tier_lines_differ_by_threshold() -> None:
    assert surcharge_tier_line() != SurchargeTierLine(
        SURCHARGE, TAX, D("400.25"), D(100), Rate(D("0.25")), CENT, D("25.06")
    )


def test_surcharge_tier_lines_differ_by_rounding() -> None:
    assert surcharge_tier_line() != SurchargeTierLine(
        SURCHARGE, TAX, D("400.25"), D(300), Rate(D("0.25")), NO_ROUNDING, D("25.06")
    )


def test_surcharge_tier_lines_are_hashable() -> None:
    assert hash(surcharge_tier_line()) == hash(surcharge_tier_line())


def test_a_surcharge_tier_line_is_not_a_rate_applied_line() -> None:
    assert not isinstance(surcharge_tier_line(), RateAppliedLine)


def test_tapered_amount_line_fields_in_order() -> None:
    line = tapered_amount_line()

    assert line == TaperedAmountLine(
        output=PERSONAL,
        base=INCOME,
        base_amount=D("22000.5"),
        taper=TAPER,
        rounding=CENT,
        reduction=ExactFraction("100.025"),
        result=D("1399.98"),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "base",
        "base_amount",
        "taper",
        "rounding",
        "reduction",
        "result",
    ]
    assert line.output is PERSONAL
    assert line.base is INCOME
    assert line.base_amount == D("22000.5")
    assert line.taper == TAPER
    assert line.rounding == CENT
    assert line.reduction == ExactFraction(4001, 40)
    assert isinstance(line.reduction, ExactFraction)
    assert line.result == D("1399.98")
    assert line.amount == D("1399.98")


def test_tapered_amount_line_may_hold_a_zero_reduction() -> None:
    # A base at or below the threshold reduces nothing: the full amount.
    line = TaperedAmountLine(
        PERSONAL, INCOME, D(15000), TAPER, NO_ROUNDING, ExactFraction(0), D(1500)
    )

    assert line.reduction == ExactFraction(0)
    assert line.amount == D(1500)


def test_tapered_amount_line_may_hold_a_reduction_above_the_supplement() -> None:
    # The reduction is recorded before the floor at zero; the result is the base amount.
    line = TaperedAmountLine(
        PERSONAL, INCOME, D(80000), TAPER, NO_ROUNDING, ExactFraction(3000), D(1000)
    )

    assert line.reduction == ExactFraction(3000)
    assert line.amount == D(1000)


def test_tapered_amount_lines_differ_by_taper() -> None:
    other = Taper(D(1000), D(500), D(20000), D(5000))

    assert tapered_amount_line() != TaperedAmountLine(
        PERSONAL, INCOME, D("22000.5"), other, CENT, ExactFraction("100.025"), D("1399.98")
    )


def test_tapered_amount_lines_differ_by_rounding() -> None:
    assert tapered_amount_line() != TaperedAmountLine(
        PERSONAL, INCOME, D("22000.5"), TAPER, NO_ROUNDING, ExactFraction("100.025"), D("1399.98")
    )


def test_tapered_amount_lines_differ_by_reduction() -> None:
    assert tapered_amount_line() != TaperedAmountLine(
        PERSONAL, INCOME, D("22000.5"), TAPER, CENT, ExactFraction(100), D("1399.98")
    )


def test_tapered_amount_lines_are_hashable() -> None:
    assert hash(tapered_amount_line()) == hash(tapered_amount_line())


def test_a_tapered_amount_lines_amount_is_not_one_of_its_fields() -> None:
    assert "amount" not in [f.name for f in fields(tapered_amount_line())]


def test_a_tapered_amount_line_is_not_a_contribution_tier_or_subtracted_line() -> None:
    line = tapered_amount_line()

    assert not isinstance(line, ContributionTierLine)
    assert not isinstance(line, SubtractedNotBelowZeroLine)


def test_per_unit_amount_line_fields_in_order() -> None:
    line = per_unit_amount_line()

    assert line == PerUnitAmountLine(
        output=CHILD_AMOUNT,
        count_kind=CHILDREN,
        count=2,
        per_unit=Amount(D(544)),
        rounding=CENT,
        result=D(1088),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "count_kind",
        "count",
        "per_unit",
        "rounding",
        "result",
    ]
    assert line.output is CHILD_AMOUNT
    assert line.count_kind is CHILDREN
    assert line.count == 2
    assert type(line.count) is int
    assert line.per_unit == Amount(D(544))
    assert line.rounding == CENT
    assert line.result == D(1088)
    assert line.amount == D(1088)


def test_per_unit_amount_line_may_hold_a_count_of_zero() -> None:
    line = PerUnitAmountLine(CHILD_AMOUNT, CHILDREN, 0, Amount(D(544)), NO_ROUNDING, D(0))

    assert line.count == 0
    assert line.amount == D(0)


def test_per_unit_amount_lines_differ_by_count() -> None:
    assert per_unit_amount_line() != PerUnitAmountLine(
        CHILD_AMOUNT, CHILDREN, 3, Amount(D(544)), CENT, D(1088)
    )


def test_per_unit_amount_lines_differ_by_per_unit_amount() -> None:
    assert per_unit_amount_line() != PerUnitAmountLine(
        CHILD_AMOUNT, CHILDREN, 2, Amount(D(545)), CENT, D(1088)
    )


def test_per_unit_amount_lines_differ_by_rounding() -> None:
    assert per_unit_amount_line() != PerUnitAmountLine(
        CHILD_AMOUNT, CHILDREN, 2, Amount(D(544)), NO_ROUNDING, D(1088)
    )


def test_per_unit_amount_lines_differ_by_count_kind() -> None:
    other = ArtifactKind("ex/dependant_count", int)

    assert per_unit_amount_line() != PerUnitAmountLine(
        CHILD_AMOUNT, other, 2, Amount(D(544)), CENT, D(1088)
    )


def test_per_unit_amount_lines_are_hashable() -> None:
    assert hash(per_unit_amount_line()) == hash(per_unit_amount_line())


def test_a_per_unit_amount_lines_amount_is_not_one_of_its_fields() -> None:
    assert "amount" not in [f.name for f in fields(per_unit_amount_line())]


def test_a_per_unit_amount_line_is_not_a_credit_amount_or_capped_amount_line() -> None:
    line = per_unit_amount_line()

    assert not isinstance(line, CreditAmountLine)
    assert not isinstance(line, CappedAmountLine)


def test_multiple_over_line_fields_in_order() -> None:
    line = multiple_over_line()

    assert line == MultipleOverLine(
        output=REDUCTION,
        base=TOTAL,
        base_amount=D(294),
        factor=Factor(D(2)),
        less=TAX,
        less_amount=D("100.25"),
        rounding=CENT,
        result=D("487.75"),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "base",
        "base_amount",
        "factor",
        "less",
        "less_amount",
        "rounding",
        "result",
    ]
    assert line.output is REDUCTION
    assert line.base is TOTAL
    assert line.base_amount == D(294)
    assert line.factor == Factor(D(2))
    assert line.less is TAX
    assert line.less_amount == D("100.25")
    assert line.rounding == CENT
    assert line.result == D("487.75")
    assert line.amount == D("487.75")


def test_multiple_over_line_may_hold_a_floored_zero() -> None:
    # The multiple is below the figure taken off: the result is 0.
    line = MultipleOverLine(
        REDUCTION, TOTAL, D(294), Factor(D(2)), TAX, D("8195.7644476"), NO_ROUNDING, D(0)
    )

    assert line.result == D(0)
    assert line.amount == D(0)


def test_multiple_over_lines_differ_by_factor() -> None:
    assert multiple_over_line() != MultipleOverLine(
        REDUCTION, TOTAL, D(294), Factor(D(3)), TAX, D("100.25"), CENT, D("487.75")
    )


def test_multiple_over_lines_differ_by_rounding() -> None:
    assert multiple_over_line() != MultipleOverLine(
        REDUCTION, TOTAL, D(294), Factor(D(2)), TAX, D("100.25"), NO_ROUNDING, D("487.75")
    )


def test_multiple_over_lines_differ_by_the_figure_taken_off() -> None:
    assert multiple_over_line() != MultipleOverLine(
        REDUCTION, TOTAL, D(294), Factor(D(2)), TAX, D("100.5"), CENT, D("487.75")
    )


def test_multiple_over_lines_are_hashable() -> None:
    assert hash(multiple_over_line()) == hash(multiple_over_line())


def test_a_multiple_over_lines_amount_is_not_one_of_its_fields() -> None:
    assert "amount" not in [f.name for f in fields(multiple_over_line())]


def test_a_multiple_over_line_is_not_a_subtracted_or_rate_applied_line() -> None:
    line = multiple_over_line()

    assert not isinstance(line, SubtractedNotBelowZeroLine)
    assert not isinstance(line, SubtractedLine)
    assert not isinstance(line, RateAppliedLine)


def test_at_most_line_fields_in_order() -> None:
    line = at_most_line()

    assert line == AtMostLine(
        output=ALLOWED,
        amount_kind=CLAIMED,
        amount_value=D("1500.25"),
        bound=LIMIT,
        bound_value=D(1926),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "amount_kind",
        "amount_value",
        "bound",
        "bound_value",
    ]
    assert line.output is ALLOWED
    assert line.amount_kind is CLAIMED
    assert line.amount_value == D("1500.25")
    assert line.bound is LIMIT
    assert line.bound_value == D(1926)
    assert line.amount == D("1500.25")


def test_at_most_line_may_hold_an_amount_equal_to_its_bound() -> None:
    line = AtMostLine(ALLOWED, CLAIMED, D(1926), LIMIT, D(1926))

    assert line.amount == D(1926)


def test_at_most_line_may_hold_a_zero_amount() -> None:
    line = AtMostLine(ALLOWED, CLAIMED, D(0), LIMIT, D(0))

    assert line.amount == D(0)


def test_at_most_lines_differ_by_amount() -> None:
    assert at_most_line() != AtMostLine(ALLOWED, CLAIMED, D("1500.5"), LIMIT, D(1926))


def test_at_most_lines_differ_by_bound() -> None:
    assert at_most_line() != AtMostLine(ALLOWED, CLAIMED, D("1500.25"), LIMIT, D(2000))


def test_at_most_lines_differ_by_the_bounds_kind() -> None:
    other = ArtifactKind("ex/other_limit", Decimal)

    assert at_most_line() != AtMostLine(ALLOWED, CLAIMED, D("1500.25"), other, D(1926))


def test_at_most_lines_are_hashable() -> None:
    assert hash(at_most_line()) == hash(at_most_line())


def test_an_at_most_lines_amount_is_not_one_of_its_fields() -> None:
    assert "amount" not in [f.name for f in fields(at_most_line())]


def test_an_at_most_line_is_not_a_lesser_of_or_capped_amount_line() -> None:
    line = at_most_line()

    assert not isinstance(line, LesserOfLine)
    assert not isinstance(line, CappedAmountLine)


def test_fraction_applied_line_fields_in_order() -> None:
    line = fraction_applied_line()

    assert line == FractionAppliedLine(
        output=PORTION,
        base=EARNED,
        base_amount=D(50000),
        fraction=Fraction(2, 3),
        rounding=CENT,
        result=D("33333.33"),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "base",
        "base_amount",
        "fraction",
        "rounding",
        "result",
    ]
    assert line.output is PORTION
    assert line.base is EARNED
    assert line.base_amount == D(50000)
    assert line.fraction == Fraction(2, 3)
    assert line.rounding == CENT
    assert line.result == D("33333.33")
    assert line.amount == D("33333.33")


def test_fraction_applied_line_may_hold_an_unrounded_exact_amount() -> None:
    line = FractionAppliedLine(PORTION, EARNED, D(60000), Fraction(2, 3), NO_ROUNDING, D("40000"))

    assert line.amount == D("40000")


def test_fraction_applied_lines_differ_by_fraction() -> None:
    assert fraction_applied_line() != FractionAppliedLine(
        PORTION, EARNED, D(50000), Fraction(1, 3), CENT, D("33333.33")
    )


def test_fraction_applied_lines_differ_by_rounding() -> None:
    assert fraction_applied_line() != FractionAppliedLine(
        PORTION, EARNED, D(50000), Fraction(2, 3), NO_ROUNDING, D("33333.33")
    )


def test_fraction_applied_lines_are_hashable() -> None:
    assert hash(fraction_applied_line()) == hash(fraction_applied_line())


def test_a_fraction_applied_lines_amount_is_not_one_of_its_fields() -> None:
    assert "amount" not in [f.name for f in fields(fraction_applied_line())]


def test_a_fraction_applied_line_is_not_a_rate_applied_line() -> None:
    assert not isinstance(fraction_applied_line(), RateAppliedLine)


def test_times_count_line_fields_in_order() -> None:
    line = times_count_line()

    assert line == TimesCountLine(
        output=CLAIMED_FOR_ALL,
        amount_kind=EACH,
        amount_value=D("16129.50"),
        count_kind=PERSONS,
        count=2,
        result=D("32259.00"),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "amount_kind",
        "amount_value",
        "count_kind",
        "count",
        "result",
    ]
    assert line.output is CLAIMED_FOR_ALL
    assert line.amount_kind is EACH
    assert line.amount_value == D("16129.50")
    assert line.count_kind is PERSONS
    assert line.count == 2
    assert type(line.count) is int
    assert line.result == D("32259.00")
    assert line.amount == D("32259.00")


def test_times_count_line_may_hold_a_count_of_zero() -> None:
    line = TimesCountLine(CLAIMED_FOR_ALL, EACH, D("16129.50"), PERSONS, 0, D(0))

    assert line.count == 0
    assert line.amount == D(0)


def test_times_count_lines_differ_by_count() -> None:
    assert times_count_line() != TimesCountLine(
        CLAIMED_FOR_ALL, EACH, D("16129.50"), PERSONS, 3, D("32259.00")
    )


def test_times_count_lines_differ_by_amount() -> None:
    assert times_count_line() != TimesCountLine(
        CLAIMED_FOR_ALL, EACH, D("16129.75"), PERSONS, 2, D("32259.00")
    )


def test_times_count_lines_differ_by_the_amounts_kind() -> None:
    other = ArtifactKind("ex/other_amount", Decimal)

    assert times_count_line() != TimesCountLine(
        CLAIMED_FOR_ALL, other, D("16129.50"), PERSONS, 2, D("32259.00")
    )


def test_times_count_lines_differ_by_count_kind() -> None:
    other = ArtifactKind("ex/dependant_count", int)

    assert times_count_line() != TimesCountLine(
        CLAIMED_FOR_ALL, EACH, D("16129.50"), other, 2, D("32259.00")
    )


def test_times_count_lines_are_hashable() -> None:
    assert hash(times_count_line()) == hash(times_count_line())


def test_a_times_count_lines_amount_is_not_one_of_its_fields() -> None:
    assert "amount" not in [f.name for f in fields(times_count_line())]


def test_a_times_count_line_is_not_a_per_unit_amount_line() -> None:
    assert not isinstance(times_count_line(), PerUnitAmountLine)


def test_chosen_by_count_line_fields_in_order() -> None:
    line = chosen_by_count_line()

    assert line == ChosenByCountLine(
        output=CHOSEN,
        count_kind=DEPENDANTS,
        count=1,
        chosen_kind=WITH_FAMILY,
        chosen_value=D("2813.00"),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "count_kind",
        "count",
        "chosen_kind",
        "chosen_value",
    ]
    assert line.output is CHOSEN
    assert line.count_kind is DEPENDANTS
    assert line.count == 1
    assert type(line.count) is int
    assert line.chosen_kind is WITH_FAMILY
    assert line.chosen_value == D("2813.00")
    assert line.amount == D("2813.00")
    assert str(line.amount) == "2813.00"


def test_chosen_by_count_line_may_hold_a_count_of_zero() -> None:
    line = ChosenByCountLine(CHOSEN, DEPENDANTS, 0, ALONE, D("1633"))

    assert line.count == 0
    assert line.chosen_kind is ALONE
    assert line.amount == D("1633")


def test_chosen_by_count_lines_differ_by_count() -> None:
    assert chosen_by_count_line() != ChosenByCountLine(
        CHOSEN, DEPENDANTS, 2, WITH_FAMILY, D("2813.00")
    )


def test_chosen_by_count_lines_differ_by_the_chosen_kind() -> None:
    assert chosen_by_count_line() != ChosenByCountLine(CHOSEN, DEPENDANTS, 1, ALONE, D("2813.00"))


def test_chosen_by_count_lines_differ_by_the_chosen_value() -> None:
    assert chosen_by_count_line() != ChosenByCountLine(
        CHOSEN, DEPENDANTS, 1, WITH_FAMILY, D("2813.01")
    )


def test_chosen_by_count_lines_differ_by_count_kind() -> None:
    other = ArtifactKind("ex/spouse_count", int)

    assert chosen_by_count_line() != ChosenByCountLine(CHOSEN, other, 1, WITH_FAMILY, D("2813.00"))


def test_chosen_by_count_lines_differ_by_output() -> None:
    other = ArtifactKind("ex/other_amount", Decimal)

    assert chosen_by_count_line() != ChosenByCountLine(
        other, DEPENDANTS, 1, WITH_FAMILY, D("2813.00")
    )


def test_chosen_by_count_lines_are_hashable() -> None:
    assert hash(chosen_by_count_line()) == hash(chosen_by_count_line())


def test_a_chosen_by_count_lines_amount_is_not_one_of_its_fields() -> None:
    assert "amount" not in [f.name for f in fields(chosen_by_count_line())]


def test_a_chosen_by_count_line_is_not_a_times_count_line() -> None:
    assert not isinstance(chosen_by_count_line(), TimesCountLine)


def test_record_total_line_fields_in_order() -> None:
    line = record_total_line()

    assert line == RecordTotalLine(
        output=TOTAL, field=ITEM_AMOUNT, amounts=(D("6000"), D("4000.50")), total=D("10000.50")
    )
    assert [f.name for f in fields(line)] == ["output", "field", "amounts", "total"]
    assert line.output is TOTAL
    assert line.field is ITEM_AMOUNT
    assert line.amounts == (D("6000"), D("4000.50"))
    assert isinstance(line.amounts, tuple)
    assert line.total == D("10000.50")
    assert line.amount == D("10000.50")
    assert str(line.amount) == "10000.50"


def test_record_total_line_may_have_no_amounts() -> None:
    line = RecordTotalLine(TOTAL, ITEM_AMOUNT, (), D(0))

    assert line.amounts == ()
    assert line.amount == D(0)


def test_record_total_lines_differ_by_the_order_of_their_amounts() -> None:
    assert record_total_line() != RecordTotalLine(
        TOTAL, ITEM_AMOUNT, (D("4000.50"), D("6000")), D("10000.50")
    )


def test_record_total_lines_differ_by_the_amounts() -> None:
    assert record_total_line() != RecordTotalLine(
        TOTAL, ITEM_AMOUNT, (D("6000"), D("4000.51")), D("10000.50")
    )


def test_record_total_lines_differ_by_the_total() -> None:
    assert record_total_line() != RecordTotalLine(
        TOTAL, ITEM_AMOUNT, (D("6000"), D("4000.50")), D("10000.51")
    )


def test_record_total_lines_differ_by_the_field() -> None:
    other = ArtifactKind("ex/other_item_amount", Decimal)

    assert record_total_line() != RecordTotalLine(
        TOTAL, other, (D("6000"), D("4000.50")), D("10000.50")
    )


def test_record_total_lines_differ_by_the_output() -> None:
    other = ArtifactKind("ex/other_total", Decimal)

    assert record_total_line() != RecordTotalLine(
        other, ITEM_AMOUNT, (D("6000"), D("4000.50")), D("10000.50")
    )


def test_record_total_lines_are_hashable() -> None:
    assert hash(record_total_line()) == hash(record_total_line())


def test_a_record_total_lines_amount_is_not_one_of_its_fields() -> None:
    assert "amount" not in [f.name for f in fields(record_total_line())]


def test_a_record_total_line_is_not_a_sum_line() -> None:
    assert not isinstance(record_total_line(), SumLine)
    assert cast(Any, record_total_line()) != SumLine(
        TOTAL, ((ITEM_AMOUNT, D("6000")), (ITEM_AMOUNT, D("4000.50"))), D("10000.50")
    )


def test_chosen_by_range_line_fields_in_order() -> None:
    line = chosen_by_range_line()

    assert line == ChosenByRangeLine(
        output=CHOSEN,
        tested_kind=TESTED,
        tested_value=D("1000.00"),
        chosen_kind=IN_THE_SECOND_RANGE,
        chosen_value=D("625.01"),
    )
    assert [f.name for f in fields(line)] == [
        "output",
        "tested_kind",
        "tested_value",
        "chosen_kind",
        "chosen_value",
    ]
    assert line.output is CHOSEN
    assert line.tested_kind is TESTED
    assert line.tested_value == D("1000.00")
    assert str(line.tested_value) == "1000.00"
    assert line.chosen_kind is IN_THE_SECOND_RANGE
    assert line.chosen_value == D("625.01")
    assert line.amount == D("625.01")
    assert str(line.amount) == "625.01"


def test_chosen_by_range_lines_differ_by_the_tested_value() -> None:
    assert chosen_by_range_line() != ChosenByRangeLine(
        CHOSEN, TESTED, D("1000.01"), IN_THE_SECOND_RANGE, D("625.01")
    )


def test_chosen_by_range_lines_differ_by_the_tested_kind() -> None:
    other = ArtifactKind("ex/other_tested", Decimal)

    assert chosen_by_range_line() != ChosenByRangeLine(
        CHOSEN, other, D("1000.00"), IN_THE_SECOND_RANGE, D("625.01")
    )


def test_chosen_by_range_lines_differ_by_the_chosen_kind() -> None:
    assert chosen_by_range_line() != ChosenByRangeLine(
        CHOSEN, TESTED, D("1000.00"), IN_THE_FIRST_RANGE, D("625.01")
    )


def test_chosen_by_range_lines_differ_by_the_chosen_value() -> None:
    assert chosen_by_range_line() != ChosenByRangeLine(
        CHOSEN, TESTED, D("1000.00"), IN_THE_SECOND_RANGE, D("625.02")
    )


def test_chosen_by_range_lines_differ_by_output() -> None:
    other = ArtifactKind("ex/other_amount", Decimal)

    assert chosen_by_range_line() != ChosenByRangeLine(
        other, TESTED, D("1000.00"), IN_THE_SECOND_RANGE, D("625.01")
    )


def test_chosen_by_range_lines_are_hashable() -> None:
    assert hash(chosen_by_range_line()) == hash(chosen_by_range_line())


def test_a_chosen_by_range_lines_amount_is_not_one_of_its_fields() -> None:
    assert "amount" not in [f.name for f in fields(chosen_by_range_line())]


def test_a_chosen_by_range_line_is_not_a_chosen_by_count_line() -> None:
    assert not isinstance(chosen_by_range_line(), ChosenByCountLine)


def test_lines_of_different_classes_are_not_equal() -> None:
    assert cast(Any, SumLine(TOTAL, (), D(10))) != BracketColumnLine(
        D(0), D("0.10"), D(100), D(0), D(10)
    )
