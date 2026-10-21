"""The 2025 datasets of Form T657, checked against CRA's form.

Form T657 (Calculation of Capital Gains Deduction, 2025 edition, confirmed 2026-10-19 from the PDF;
no .txt is published):

- Step 1 line 4 "Inclusion rate × 1/2", then line 5 "Line 3 multiplied by the inclusion rate on
  line 4 (if negative, enter "0")", and line 9 "Amount from line 17600 of Schedule 3 (if negative,
  enter "0") × 1/2";
- Chart 2 line 4 "Amount from line 2 × 1/4", line 8 "Amount from line 6 × 1/3", line 12 "Amount
  from line 10 × 1/3" and line 16 "Amount from line 14 × [ 1 – ( 2 × IR )]", the 2 of "2 × IR", the
  1 over "( 2 × IR )" and the quotient, which prints no figure of its own;
- Chart 2025 Part 1 and Part 2 "Add amounts F to J (if negative, enter "0") = × 1/2 = K";
- Chart 2025 Part 1 amount A 522,145.00 and Part 2 amount A 625,000.00;
- Chart 2024 Period 1 amount A 508,418.00 and Period 2 amount A 625,000.00, and each period's
  "Add amounts F to H (if negative, enter "0") = × 1/2 = I".

Every product or quotient is a dollars-and-cents box, so each rounds half-up to the cent, the
owner's decision, as the form states no rounding rule. Each printed 1/2, 1/4 and 1/3 is one dataset,
because each is a printed figure of its own line.
"""

from __future__ import annotations

import re
from decimal import Decimal

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.fraction import FRACTION, Fraction
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundTo
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.domain.registry import Namespace
from app.jurisdictions.ca.capabilities.apply_ratio_or_zero import ApplyRatioOrZero

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)
T657_PDF = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/t657/t657-25e.pdf"

# The form lines each dataset header quotes, lowercased as the header is compared. CRA publishes
# no .txt of T657, so the quotes are checked against the form lines as copied from the PDF.
HEADER_QUOTES = {
    "ca/t657_annual_gains_inclusion_rate": (
        "inclusion rate × 1/2",
        'line 3 multiplied by the inclusion rate on line 4 (if negative, enter "0")',
    ),
    "ca/t657_schedule_3_line_17600_fraction": (
        'amount from line 17600 of schedule 3 (if negative, enter "0") × 1/2',
    ),
    "ca/t657_chart_2_line_4_fraction": (
        "adjustment of 1988 and 1989 capital gains deductions excluding eligible capital property",
        "amount from line 2 × 1/4",
    ),
    "ca/t657_chart_2_line_8_fraction": (
        "adjustment of 1988 and 1989 capital gains deductions for eligible capital property",
        "amount from line 6 × 1/3",
    ),
    "ca/t657_chart_2_line_12_fraction": (
        "adjustment of 1990 to 1999 capital gains deductions",
        "amount from line 10 × 1/3",
    ),
    "ca/t657_chart_2_twice_ir_fraction": (
        "adjustment of 2000 capital gains deduction",
        "amount from line 14 × [ 1 – ( 2 × ir )]",
    ),
    "ca/t657_part_1_k_fraction": ('add amounts f to j (if negative, enter "0")', "× 1/2"),
    "ca/t657_part_2_k_fraction": ('add amounts f to j (if negative, enter "0")', "× 1/2"),
    "ca/chart_2025_part_1_amount_a": (
        "maximum capital gains deduction for qffp and/or qsbcs reported in 2025 but disposed of in "
        "period 1 of 2024",
        "522,145.00",
    ),
    "ca/chart_2025_part_2_amount_a": (
        "maximum capital gains deduction for qffp and/or qsbcs disposed of in 2025 or disposed of "
        "after june 24, 2024 and reported in 2025",
        "625,000.00",
    ),
    "ca/chart_2024_period_1_amount_a": (
        "maximum capital gains deduction for qffp and/or qsbcs disposed of in 2024 for period 1",
        "508,418.00",
    ),
    "ca/chart_2024_period_2_amount_a": (
        "maximum capital gains deduction for qffp and/or qsbcs disposed of in 2024 for period 2",
        "625,000.00",
    ),
    "ca/t657_chart_2024_period_1_i_fraction": (
        'add amounts f to h (if negative, enter "0")',
        "× 1/2",
    ),
    "ca/t657_chart_2024_period_2_i_fraction": (
        'add amounts f to h (if negative, enter "0")',
        "× 1/2",
    ),
    "ca/chart_2_numerator_one": (
        "adjustment of 2000 capital gains deduction",
        "amount from line 14 × [ 1 – ( 2 × ir )]",
    ),
    "ca/t657_chart_2_line_16_rounding": (
        "adjustment of 2000 capital gains deduction",
        "amount from line 14 × [ 1 – ( 2 × ir )]",
    ),
}

FRACTIONS = {
    "ca/t657_annual_gains_inclusion_rate": Fraction(1, 2),
    "ca/t657_schedule_3_line_17600_fraction": Fraction(1, 2),
    "ca/t657_chart_2_line_4_fraction": Fraction(1, 4),
    "ca/t657_chart_2_line_8_fraction": Fraction(1, 3),
    "ca/t657_chart_2_line_12_fraction": Fraction(1, 3),
    "ca/t657_part_1_k_fraction": Fraction(1, 2),
    "ca/t657_part_2_k_fraction": Fraction(1, 2),
    "ca/t657_chart_2024_period_1_i_fraction": Fraction(1, 2),
    "ca/t657_chart_2024_period_2_i_fraction": Fraction(1, 2),
}
CREDITS = {
    "ca/chart_2025_part_1_amount_a": D("522145"),
    "ca/chart_2025_part_2_amount_a": D("625000"),
    "ca/chart_2024_period_1_amount_a": D("508418"),
    "ca/chart_2024_period_2_amount_a": D("625000"),
    "ca/chart_2_numerator_one": D("1"),
}
ROUNDING_FAMILIES = ("ca/t657_chart_2_line_16_rounding",)

# Made up for this test and not registered.
BASE = ArtifactKind("ex/base", Decimal)
PRODUCT = ArtifactKind("ex/product", Decimal)
NUMERATOR = ArtifactKind("ex/numerator", Decimal)
DENOMINATOR = ArtifactKind("ex/denominator", Decimal)


def test_2025_the_2_of_2_x_ir_is_an_exact_fraction_of_2_over_1_with_no_rounding() -> None:
    data = SOURCE.get("ca/t657_chart_2_twice_ir_fraction", 2025, FRACTION)

    assert data.values == Fraction(2, 1)
    assert data.rounding == NO_ROUNDING
    assert T657_PDF in data.sources


@pytest.mark.parametrize(("family", "fraction"), FRACTIONS.items())
def test_2025_each_t657_printed_fraction_is_a_fraction_dataset(
    family: str, fraction: Fraction
) -> None:
    data = SOURCE.get(family, 2025, FRACTION)

    assert data.values == fraction
    assert data.rounding == CENT
    assert T657_PDF in data.sources


@pytest.mark.parametrize(("family", "amount"), CREDITS.items())
def test_2025_each_t657_printed_amount_is_a_credit_dataset(family: str, amount: Decimal) -> None:
    data = SOURCE.get(family, 2025, CREDIT)

    assert data.values == Credit(amount=amount)
    assert data.rounding == CENT
    assert T657_PDF in data.sources


@pytest.mark.parametrize("family", ROUNDING_FAMILIES)
def test_2025_each_t657_rounding_is_half_up_to_the_cent_with_no_values(family: str) -> None:
    data = SOURCE.get(family, 2025, ROUNDING_ONLY)

    assert data.values == RoundingOnly()
    assert data.rounding == CENT
    assert T657_PDF in data.sources


@pytest.mark.parametrize(
    ("line_3", "line_4_product"),
    [
        # Step 1 line 3 of 350000, line 3 multiplied by 1/2 is 175000.
        ("350000", "175000.00"),
        # Rounded half-up to the cent: 0.03 x 1/2 is 0.015, a tie, up to 0.02.
        ("0.03", "0.02"),
        # A loss is multiplied too: line 5 floors the product at 0, not this step.
        ("-1000", "-500.00"),
    ],
)
def test_the_line_4_fraction_halves_line_3(line_3: str, line_4_product: str) -> None:
    capability = ApplyFraction(
        SOURCE.get("ca/t657_annual_gains_inclusion_rate", 2025, FRACTION), BASE, PRODUCT
    )

    result = capability.compute((Artifact(BASE, D(line_3)),))

    assert result.outputs == (Artifact(PRODUCT, D(line_4_product)),)


@pytest.mark.parametrize(
    ("family", "amount", "adjustment"),
    [
        # Chart 2 line 4: line 2 x 1/4.
        ("ca/t657_chart_2_line_4_fraction", "40000", "10000.00"),
        # A tie rounds up: 0.02 x 1/4 is 0.005, up to 0.01.
        ("ca/t657_chart_2_line_4_fraction", "0.02", "0.01"),
        # Chart 2 line 8 and line 12: x 1/3, 6000 gives exactly 2000, 100 gives 33.33...
        ("ca/t657_chart_2_line_8_fraction", "6000", "2000.00"),
        ("ca/t657_chart_2_line_8_fraction", "100", "33.33"),
        ("ca/t657_chart_2_line_12_fraction", "9000", "3000.00"),
        ("ca/t657_chart_2_line_12_fraction", "0.05", "0.02"),
        # Chart 2 line 16's 2 of "2 x IR", as 2/1 on IR, exact and not rounded.
        ("ca/t657_chart_2_twice_ir_fraction", "0.6", "1.2"),
        ("ca/t657_chart_2_twice_ir_fraction", "0.6667", "1.3334"),
        # Step 1 line 9 and the K amounts of Chart 2025: x 1/2.
        ("ca/t657_schedule_3_line_17600_fraction", "20000", "10000.00"),
        ("ca/t657_part_1_k_fraction", "350000", "175000.00"),
        ("ca/t657_part_2_k_fraction", "350000.01", "175000.01"),
    ],
)
def test_each_printed_fraction_gives_its_line(family: str, amount: str, adjustment: str) -> None:
    capability = ApplyFraction(SOURCE.get(family, 2025, FRACTION), BASE, PRODUCT)

    result = capability.compute((Artifact(BASE, D(amount)),))

    assert result.outputs == (Artifact(PRODUCT, D(adjustment)),)


@pytest.mark.parametrize(
    ("family", "maximum"),
    [
        ("ca/chart_2025_part_1_amount_a", "522145.00"),
        ("ca/chart_2025_part_2_amount_a", "625000.00"),
        ("ca/chart_2_numerator_one", "1.00"),
    ],
)
def test_each_printed_amount_becomes_an_artifact_of_the_same_name(
    family: str, maximum: str
) -> None:
    capability = CreditAmount(SOURCE.get(family, 2025, CREDIT), PRODUCT)

    result = capability.compute(())

    assert result.outputs == (Artifact(PRODUCT, D(maximum)),)


@pytest.mark.parametrize(
    ("line_14", "twice_ir", "quotient"),
    [
        # IR 0.6: 2 x IR is 1.2, so 12000 x 1/1.2 is 10000.
        ("12000.00", "1.2", "10000.00"),
        # IR 0.5: 2 x IR is 1, so the quotient is the whole of line 14.
        ("12000.00", "1.0", "12000.00"),
        # One rounding, half-up to the cent: 1000.01 / 1 is exact, 1000 / 1.4 = 714.2857...
        ("1000.01", "1.0", "1000.01"),
        ("1000.00", "1.4", "714.29"),
        # IR left blank (0) gives 0, not an error, so a return with nothing on Chart 2 computes.
        ("0.00", "0", "0.00"),
        ("12000.00", "0", "0.00"),
    ],
)
def test_the_chart_2_line_16_quotient_is_line_14_over_twice_ir(
    line_14: str, twice_ir: str, quotient: str
) -> None:
    capability = ApplyRatioOrZero(
        SOURCE.get("ca/t657_chart_2_line_16_rounding", 2025, ROUNDING_ONLY),
        BASE,
        NUMERATOR,
        DENOMINATOR,
        PRODUCT,
    )

    result = capability.compute(
        (
            Artifact(BASE, D(line_14)),
            Artifact(NUMERATOR, D("1")),
            Artifact(DENOMINATOR, D(twice_ir)),
        )
    )

    assert result.outputs == (Artifact(PRODUCT, D(quotient)),)


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


@pytest.mark.parametrize(("family", "quotes"), HEADER_QUOTES.items())
def test_the_dataset_header_quotes_t657_as_the_form_prints_it(
    family: str, quotes: tuple[str, ...]
) -> None:
    header = dataset_header(family).lower()

    for quoted in quotes:
        assert quoted in header, quoted


@pytest.mark.parametrize(
    "family", [family for family in HEADER_QUOTES if family != "ca/t657_chart_2_twice_ir_fraction"]
)
def test_the_dataset_header_states_the_half_up_cent_rule(family: str) -> None:
    assert "half-up to the cent" in dataset_header(family)
