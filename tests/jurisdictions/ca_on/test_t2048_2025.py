"""The 2025 datasets of Form T2048, checked against CRA's form.

Form T2048 (Capital Gains Deduction for Qualifying Business Transfers or Qualifying Cooperative
Conversions, 2025 edition, confirmed 2026-10-19 from the PDF; no .txt is published):

- Part 2 line 4 "Inclusion rate × 50%", then line 5 "Line 3 multiplied by the percentage from
  line 4";
- Part 3 line 15 "Inclusion rate × 50%", then line 16 "Taxable capital gains for the QBT or QCC
  only: line 14 multiplied by the inclusion rate on line 15";
- Chart A line 5 "50% of exploration and development expenses (line 22400)" and line 15 "50% of
  income from the recovery of exploration and development expenses (line 13000)";
- Part 2 line 3 "Line 1 multiplied by the percentage from line 2" and Part 4 line 41 "Line 39
  multiplied by line 40" (line 39 being "Line 37 divided by line 38"), which print no figure of
  their own.

Every one of these is a dollars-and-cents box, so each product rounds half-up to the cent, the
owner's decision, as the form states no rounding rule. The four 50% rates are one dataset each,
because each is a printed figure of its own line.
"""

from __future__ import annotations

import re
from decimal import Decimal

import pytest

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import RoundingMode, RoundTo
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.domain.registry import Namespace
from app.jurisdictions.ca.capabilities.apply_percentage import ApplyPercentage
from app.jurisdictions.ca.capabilities.apply_ratio_or_zero import ApplyRatioOrZero

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)
T2048_PDF = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/t2048/t2048-25e.pdf"

# The form lines each dataset header quotes, lowercased as the header is compared. CRA publishes
# no .txt of T2048, so the quotes are checked against the form lines as copied from the PDF.
HEADER_QUOTES = {
    "ca/qbt_abil_reduction_rounding": (
        "line 39 multiplied by line 40",
        "abil reduction",
        "line 37 divided by line 38",
    ),
    "ca/qbt_amount_allocated_rounding": (
        "line 1 multiplied by the percentage from line 2",
        "percentage allocated to you",
    ),
    "ca/qbt_election_inclusion_rate": (
        "inclusion rate × 50%",
        "line 3 multiplied by the percentage from line 4",
    ),
    "ca/qbt_exploration_expenses_rate": (
        "50% of exploration and development expenses (line 22400)",
    ),
    "ca/qbt_exploration_recovery_rate": (
        "50% of income from the recovery of exploration and development expenses (line 13000)",
    ),
    "ca/qbt_gains_inclusion_rate": (
        "inclusion rate × 50%",
        "taxable capital gains for the qbt or qcc only: line 14 multiplied by the inclusion rate "
        "on line 15",
    ),
}

RATE_FAMILIES = (
    "ca/qbt_election_inclusion_rate",
    "ca/qbt_gains_inclusion_rate",
    "ca/qbt_exploration_expenses_rate",
    "ca/qbt_exploration_recovery_rate",
)
ROUNDING_FAMILIES = (
    "ca/qbt_amount_allocated_rounding",
    "ca/qbt_abil_reduction_rounding",
)

# Made up for this test and not registered.
BASE = ArtifactKind("ex/base", Decimal)
PRODUCT = ArtifactKind("ex/product", Decimal)
NUMERATOR = ArtifactKind("ex/numerator", Decimal)
DENOMINATOR = ArtifactKind("ex/denominator", Decimal)
PERCENTAGE = ArtifactKind("ex/percentage", Decimal)


@pytest.mark.parametrize("family", RATE_FAMILIES)
def test_2025_each_t2048_inclusion_rate_is_half(family: str) -> None:
    data = SOURCE.get(family, 2025, RATE)

    assert data.values == Rate(D("0.5"))
    assert data.rounding == CENT


@pytest.mark.parametrize("family", RATE_FAMILIES)
def test_2025_each_t2048_inclusion_rate_cites_the_form(family: str) -> None:
    assert T2048_PDF in SOURCE.get(family, 2025, RATE).sources


@pytest.mark.parametrize("family", ROUNDING_FAMILIES)
def test_2025_each_t2048_rounding_is_half_up_to_the_cent_with_no_values(family: str) -> None:
    data = SOURCE.get(family, 2025, ROUNDING_ONLY)

    assert data.values == RoundingOnly()
    assert data.rounding == CENT
    assert T2048_PDF in data.sources


@pytest.mark.parametrize(
    ("gains", "taxable"),
    [
        # Part 3 line 14 of 160000, line 16 is half of it.
        ("160000", "80000"),
        # Rounded half-up to the cent: 1234.57 x 50% is 617.285, a tie, up to 617.29.
        ("1234.57", "617.29"),
        ("0", "0"),
    ],
)
def test_the_line_15_rate_gives_line_16(gains: str, taxable: str) -> None:
    capability = ApplyRate(SOURCE.get("ca/qbt_gains_inclusion_rate", 2025, RATE), BASE, PRODUCT)

    result = capability.compute((Artifact(BASE, D(gains)),))

    assert result.outputs == (Artifact(PRODUCT, D(taxable)),)


@pytest.mark.parametrize(
    ("line_1", "percentage", "line_3"),
    [
        # Return BE: 600000 allocated 50%.
        ("600000", "50", "300000"),
        # A tie rounds up: 1000.01 x 50% = 500.005, up to 500.01.
        ("1000.01", "50", "500.01"),
        ("600000", "0", "0"),
    ],
)
def test_line_3_is_line_1_at_the_percentage_from_line_2(
    line_1: str, percentage: str, line_3: str
) -> None:
    capability = ApplyPercentage(
        SOURCE.get("ca/qbt_amount_allocated_rounding", 2025, ROUNDING_ONLY),
        BASE,
        PERCENTAGE,
        PRODUCT,
    )

    result = capability.compute((Artifact(BASE, D(line_1)), Artifact(PERCENTAGE, D(percentage))))

    assert result.outputs == (Artifact(PRODUCT, D(line_3)),)


@pytest.mark.parametrize(
    ("line_33", "line_36", "line_35", "line_41"),
    [
        # Return BE: line 36 equals line 35, so the whole ABIL is the reduction.
        ("4000", "9500", "9500", "4000"),
        # 4000 x 5000 / 9500 = 2105.2631..., rounded half-up to the cent.
        ("4000", "5000", "9500", "2105.26"),
        ("4000", "0", "9500", "0"),
        # Line 36 is 0 when line 35 is 0 ("enter 0 on lines 41 and 42"), not an error.
        ("0", "0", "0", "0"),
    ],
)
def test_line_41_is_line_33_times_line_36_over_line_35(
    line_33: str, line_36: str, line_35: str, line_41: str
) -> None:
    capability = ApplyRatioOrZero(
        SOURCE.get("ca/qbt_abil_reduction_rounding", 2025, ROUNDING_ONLY),
        BASE,
        NUMERATOR,
        DENOMINATOR,
        PRODUCT,
    )

    result = capability.compute(
        (
            Artifact(BASE, D(line_33)),
            Artifact(NUMERATOR, D(line_36)),
            Artifact(DENOMINATOR, D(line_35)),
        )
    )

    assert result.outputs == (Artifact(PRODUCT, D(line_41)),)


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
def test_the_dataset_header_quotes_t2048_as_the_form_prints_it(
    family: str, quotes: tuple[str, ...]
) -> None:
    header = dataset_header(family).lower()

    for quoted in quotes:
        assert quoted in header, quoted


@pytest.mark.parametrize("family", HEADER_QUOTES)
def test_the_dataset_header_states_the_half_up_cent_rule(family: str) -> None:
    assert "half-up to the cent" in dataset_header(family)
