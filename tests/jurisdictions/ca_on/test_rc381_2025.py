"""The 2025 datasets of Form RC381, checked against CRA's form.

Form RC381 (2025), "Inter-Provincial Calculation for CPP and QPP Contributions and
Overpayments" (`docs/cra-forms-2025/rc381-25e.pdf`; no .txt is published). Part 2: the "Monthly
proration for 2025" table, "Enter the corresponding amounts from the monthly proration table
above using the number of months from lines A and B.", lines G to J for the QPP. Part 3: "Line
4 divided by line 5 (calculated to the fifth decimal place without rounding)" (line 6); "Amount
from line E of Part 2 multiplied by the rate at line 6" (lines 7 to 10); "amount from line 19 x
83.1933%" (line 20); "amount from line 18 x 4.95% = (maximum $3,356.10)" (line 22), "amount from
line 18 x 1% = (maximum $678.00)" (line 23) and "amount from line 15 x 4% = (maximum
$396.00)" (line 26).

The form prints no "upper" of its own for lines 22, 23 and 26: the tiers run from 0 to the
maximum the printed maximum implies (67,800.00 at 4.95% and 1% and 9,900.00 at 4%).

The dataset of each line is checked with the rounding rule or the capability that reads it, on
made-up kinds; the lines together are in the `end_to_end` tests and
`returns/2025_return_bo.yaml`.
"""

from __future__ import annotations

import re
from decimal import Decimal
from fractions import Fraction as ExactFraction
from typing import Any

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.parameters.amount_by_count import AMOUNT_BY_COUNT
from app.domain.parameters.contribution_tier import CONTRIBUTION_TIER, ContributionTier
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import RoundingMode, RoundTo
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.domain.registry import Namespace

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)
FIVE_DECIMALS_DOWN = RoundTo(D("0.00001"), RoundingMode.DOWN)
RC381_PDF = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/rc381/rc381-25e.pdf"

RATIO_TRUNCATION = "ca/rc381_ratio_truncation"
CENTS_ROUNDING = "ca/rc381_cents_rounding"
CPP_BASE_SHARE_RATE = "ca/rc381_cpp_base_share_rate"
REQUIRED_CPP_BASE = "ca/rc381_required_cpp_base"
REQUIRED_FIRST_ADDITIONAL = "ca/rc381_required_first_additional"
REQUIRED_SECOND_ADDITIONAL = "ca/rc381_required_second_additional"

# Made up for this test and not registered.
EARNINGS = ArtifactKind("ex/earnings", Decimal)
CONTRIBUTION = ArtifactKind("ex/contribution", Decimal)

# Part 2's "Monthly proration for 2025" table as printed, by number of months: maximum
# pensionable earnings, maximum amount subject to second additional contributions, additional
# maximum pensionable earnings and maximum basic exemption.
PRORATION_TABLE = {
    1: ("5941.67", "825.00", "6766.67", "291.67"),
    2: ("11883.33", "1650.00", "13533.33", "583.33"),
    3: ("17825.00", "2475.00", "20300.00", "875.00"),
    4: ("23766.67", "3300.00", "27066.67", "1166.67"),
    5: ("29708.33", "4125.00", "33833.33", "1458.33"),
    6: ("35650.00", "4950.00", "40600.00", "1750.00"),
    7: ("41591.67", "5775.00", "47366.67", "2041.67"),
    8: ("47533.33", "6600.00", "54133.33", "2333.33"),
    9: ("53475.00", "7425.00", "60900.00", "2625.00"),
    10: ("59416.67", "8250.00", "67666.67", "2916.67"),
    11: ("65358.33", "9075.00", "74433.33", "3208.33"),
    12: ("71300.00", "9900.00", "81200.00", "3500.00"),
}
PRORATION_FAMILIES = (
    "ca/cpp_maximum_pensionable_earnings",
    "ca/cpp_second_additional_earnings_maximum",
    "ca/cpp_additional_maximum_pensionable_earnings",
    "ca/cpp_basic_exemption",
)


def squashed(text: str) -> str:
    """`text` with the comment markers and line breaks gone and runs of blanks made one."""
    return re.sub(r"\s+", " ", text.replace("#", " ")).strip()


def dataset_header(family: str) -> str:
    """The comment lines above the dataset's first key, squashed."""
    root = app.registrations.JURISDICTIONS.roots()[Namespace("ca")]
    name = family.removeprefix("ca/")
    lines = (root / "parameters" / name / "2025.yaml").read_text().splitlines()
    first_key = next(i for i, line in enumerate(lines) if line[:1] != "#")
    return squashed("\n".join(lines[:first_key]))


# Line 6.


def test_2025_line_6_is_cut_at_the_fifth_decimal_place_without_rounding() -> None:
    data = SOURCE.get(RATIO_TRUNCATION, 2025, ROUNDING_ONLY)

    assert data.values == RoundingOnly()
    # "calculated to the fifth decimal place without rounding": increment 0.00001, mode down.
    assert data.rounding == FIVE_DECIMALS_DOWN


@pytest.mark.parametrize(
    ("dividend", "divisor", "line_6"),
    [
        # The ticket's example: 30,000 / 70,000 = 0.4285714..., cut, not rounded up to 0.42857.
        ("30000", "70000", "0.42857"),
        # 2 / 3 = 0.66666..., which rounding would make 0.66667.
        ("2", "3", "0.66666"),
        ("1", "1", "1.00000"),
        ("0", "5", "0.00000"),
    ],
)
def test_line_6_truncates_the_quotient(dividend: str, divisor: str, line_6: str) -> None:
    rule = SOURCE.get(RATIO_TRUNCATION, 2025, ROUNDING_ONLY).rounding

    assert rule.apply(ExactFraction(D(dividend)) / ExactFraction(D(divisor))) == D(line_6)


# Lines 7 to 10.


def test_2025_lines_7_to_10_round_half_up_to_the_cent() -> None:
    data = SOURCE.get(CENTS_ROUNDING, 2025, ROUNDING_ONLY)

    assert data.values == RoundingOnly()
    assert data.rounding == CENT


@pytest.mark.parametrize(
    ("base", "line_6", "line"),
    [
        # The ticket's example, line 6 = 0.42857: line 7 = 81,200.00 x 0.42857 = 34,799.884.
        ("81200.00", "0.42857", "34799.88"),
        # Line 8 = 71,300.00 x 0.42857 = 30,557.0410.
        ("71300.00", "0.42857", "30557.04"),
        # Line 9 = 3,500.00 x 0.42857 = 1,499.995, a tie that goes up: 1,500.00.
        ("3500.00", "0.42857", "1500.00"),
        # Line 10 = 9,900.00 x 0.42857 = 4,242.843.
        ("9900.00", "0.42857", "4242.84"),
    ],
)
def test_lines_7_to_10_multiply_by_line_6_and_round_half_up(
    base: str, line_6: str, line: str
) -> None:
    rule = SOURCE.get(CENTS_ROUNDING, 2025, ROUNDING_ONLY).rounding

    assert rule.apply(ExactFraction(D(base)) * ExactFraction(D(line_6))) == D(line)


# Line 20.


def test_2025_line_20_is_83_1933_percent_to_the_cent() -> None:
    data = SOURCE.get(CPP_BASE_SHARE_RATE, 2025, RATE)

    assert data.values == Rate(D("0.831933"))
    assert data.rounding == CENT


@pytest.mark.parametrize(
    ("line_19", "line_20"),
    [
        # The ticket's example: 1,800.00 x 83.1933% = 1,497.4794.
        ("1800.00", "1497.48"),
        ("0", "0.00"),
        # The maximum base and first additional contributions on 67,800.00 x 5.95%.
        ("4034.10", "3356.10"),
    ],
)
def test_line_20_is_83_1933_percent_of_line_19(line_19: str, line_20: str) -> None:
    capability = ApplyRate(SOURCE.get(CPP_BASE_SHARE_RATE, 2025, RATE), EARNINGS, CONTRIBUTION)

    result = capability.compute((Artifact(EARNINGS, D(line_19)),))

    assert result.outputs == (Artifact(CONTRIBUTION, D(line_20)),)


# Lines 22, 23 and 26.


@pytest.mark.parametrize(
    ("family", "tier"),
    [
        # Line 22: "x 4.95% = (maximum $3,356.10)"; 67,800.00 x 4.95% is 3,356.10.
        (REQUIRED_CPP_BASE, ContributionTier(Rate(D("0.0495")), D("0"), D("67800"), D("3356.10"))),
        # Line 23: "x 1% = (maximum $678.00)"; 67,800.00 x 1% is 678.00.
        (
            REQUIRED_FIRST_ADDITIONAL,
            ContributionTier(Rate(D("0.01")), D("0"), D("67800"), D("678.00")),
        ),
        # Line 26: "x 4% = (maximum $396.00)"; 9,900.00 x 4% is 396.00.
        (
            REQUIRED_SECOND_ADDITIONAL,
            ContributionTier(Rate(D("0.04")), D("0"), D("9900"), D("396.00")),
        ),
    ],
)
def test_2025_required_contribution_tiers_are_the_printed_rate_and_maximum(
    family: str, tier: ContributionTier
) -> None:
    data = SOURCE.get(family, 2025, CONTRIBUTION_TIER)

    assert data.values == tier
    # The earnings on lines 18 and 15 are already net of the exemption, so the band starts at 0,
    # and the printed maximum is the whole band at the rate.
    assert (tier.upper - tier.lower) * tier.rate.value == tier.maximum
    # Lines 22, 23 and 26 are dollars-and-cents boxes.
    assert data.rounding == CENT


@pytest.mark.parametrize(
    ("family", "earnings", "contribution"),
    [
        # The ticket's example: line 18 = 28,500.00, so line 22 = 1,410.75, line 23 = 285.00.
        (REQUIRED_CPP_BASE, "28500.00", "1410.75"),
        (REQUIRED_FIRST_ADDITIONAL, "28500.00", "285.00"),
        # No earnings, and earnings at and above the band's top.
        (REQUIRED_CPP_BASE, "0", "0.00"),
        (REQUIRED_CPP_BASE, "67800.00", "3356.10"),
        (REQUIRED_CPP_BASE, "80000.00", "3356.10"),
        (REQUIRED_FIRST_ADDITIONAL, "67800.00", "678.00"),
        (REQUIRED_FIRST_ADDITIONAL, "80000.00", "678.00"),
        # Line 26: 4% of the earnings subject to second additional contributions, at most 396.00.
        (REQUIRED_SECOND_ADDITIONAL, "0", "0.00"),
        (REQUIRED_SECOND_ADDITIONAL, "1000.00", "40.00"),
        (REQUIRED_SECOND_ADDITIONAL, "9900.00", "396.00"),
        (REQUIRED_SECOND_ADDITIONAL, "12000.00", "396.00"),
        # Rounded half up to the cent: 4.95% of 0.10 is 0.00495, of 0.11 is 0.005445; 1% of
        # 0.50 is 0.005, a tie that goes up.
        (REQUIRED_CPP_BASE, "0.10", "0.00"),
        (REQUIRED_CPP_BASE, "0.11", "0.01"),
        (REQUIRED_FIRST_ADDITIONAL, "0.50", "0.01"),
    ],
)
def test_the_required_contributions_are_the_rate_of_the_earnings_up_to_the_maximum(
    family: str, earnings: str, contribution: str
) -> None:
    capability = TieredContribution(
        SOURCE.get(family, 2025, CONTRIBUTION_TIER), EARNINGS, CONTRIBUTION
    )

    result = capability.compute((Artifact(EARNINGS, D(earnings)),))

    assert result.outputs == (Artifact(CONTRIBUTION, D(contribution)),)


# Part 2 lines G to J read the four existing Schedule 8 tables.


@pytest.mark.parametrize("column", range(4), ids=lambda column: PRORATION_FAMILIES[column])
def test_the_monthly_proration_table_is_the_one_rc381_prints(column: int) -> None:
    data = SOURCE.get(PRORATION_FAMILIES[column], 2025, AMOUNT_BY_COUNT)

    assert dict(data.values.rows) == {
        months: D(row[column]) for months, row in PRORATION_TABLE.items()
    }


@pytest.mark.parametrize("family", PRORATION_FAMILIES)
def test_the_monthly_proration_tables_cite_rc381_beside_schedule_8(family: str) -> None:
    data = SOURCE.get(family, 2025, AMOUNT_BY_COUNT)

    assert RC381_PDF in data.sources
    assert "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/5000-s8/5000-s8-25e.txt" in (
        data.sources
    )


# Sources and headers.


@pytest.mark.parametrize(
    ("family", "kind"),
    [
        (RATIO_TRUNCATION, ROUNDING_ONLY),
        (CENTS_ROUNDING, ROUNDING_ONLY),
        (CPP_BASE_SHARE_RATE, RATE),
        (REQUIRED_CPP_BASE, CONTRIBUTION_TIER),
        (REQUIRED_FIRST_ADDITIONAL, CONTRIBUTION_TIER),
        (REQUIRED_SECOND_ADDITIONAL, CONTRIBUTION_TIER),
    ],
)
def test_2025_rc381_datasets_cite_only_the_rc381_pdf(family: str, kind: ParameterKind[Any]) -> None:
    assert SOURCE.get(family, 2025, kind).sources == (RC381_PDF,)


@pytest.mark.parametrize(
    ("family", "quotes"),
    [
        (
            RATIO_TRUNCATION,
            ("Line 4 divided by line 5 (calculated to the fifth decimal place without rounding)",),
        ),
        (
            CENTS_ROUNDING,
            ("Amount from line E of Part 2 multiplied by the rate at line 6",),
        ),
        (CPP_BASE_SHARE_RATE, ("amount from line 19", "83.1933%")),
        (REQUIRED_CPP_BASE, ("amount from line 18", "4.95%", "(maximum $3,356.10)")),
        (REQUIRED_FIRST_ADDITIONAL, ("amount from line 18", "1%", "(maximum $678.00)")),
        (REQUIRED_SECOND_ADDITIONAL, ("amount from line 15", "4%", "(maximum $396.00)")),
    ],
)
def test_the_dataset_header_quotes_rc381_as_the_form_prints_it(
    family: str, quotes: tuple[str, ...]
) -> None:
    header = dataset_header(family)

    assert "RC381" in header
    for quote in quotes:
        assert quote in header, quote


@pytest.mark.parametrize(
    "family",
    [
        RATIO_TRUNCATION,
        CENTS_ROUNDING,
        CPP_BASE_SHARE_RATE,
        REQUIRED_CPP_BASE,
        REQUIRED_FIRST_ADDITIONAL,
        REQUIRED_SECOND_ADDITIONAL,
    ],
)
def test_the_dataset_header_states_its_rounding_decision(family: str) -> None:
    assert "round" in dataset_header(family).lower()
