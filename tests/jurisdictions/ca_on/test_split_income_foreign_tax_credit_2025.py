"""The 2025 foreign tax credit on split income rounding datasets (Form T1206 line 23).

Form T1206 2025 (docs/cra-forms-2025/t1206-25e.pdf, confirmed 2026-10-19 from the PDF; no .txt
published), Part 2, "Federal foreign tax credit on split income": "Part of the amount on line 3 that
is from foreign sources" (68370) over "Total income from foreign sources" (68380), "× Amount from
line 40500 of your return" (line 23); "Line 22 minus line 23 (if negative, enter "0")" (line 24).

Line 23 multiplies and divides, so it has one `rounding_only` dataset,
`ca/split_income_line_23_rounding`: line 23 is a dollars-and-cents box, so the product over the
quotient rounds half-up to the cent once, the owner's decision, as the form states no rounding
rule. Line 24 takes amounts already in cents.

The dataset is tested with the capability that reads it, on made-up kinds.
"""

from __future__ import annotations

import re
from decimal import Decimal

import app.registrations
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.parameters.rounding import RoundingMode, RoundTo
from app.domain.parameters.rounding_only import ROUNDING_ONLY, RoundingOnly
from app.domain.registry import Namespace
from app.jurisdictions.ca.capabilities.apply_ratio_or_zero import ApplyRatioOrZero

D = Decimal
SOURCE = YamlParameterSource(app.registrations.JURISDICTIONS.roots())
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)
LINE_23_ROUNDING = "ca/split_income_line_23_rounding"
T1206_PDF = "https://www.canada.ca/content/dam/cra-arc/formspubs/pbg/t1206/t1206-25e.pdf"

# Made up for this test and not registered.
CREDIT = ArtifactKind("ex/credit", Decimal, non_negative=True)
FOREIGN_PART = ArtifactKind("ex/foreign_part", Decimal, non_negative=True)
FOREIGN_TOTAL = ArtifactKind("ex/foreign_total", Decimal, non_negative=True)
SHARE_OF_CREDIT = ArtifactKind("ex/share_of_credit", Decimal, non_negative=True)


def squashed(text: str) -> str:
    """`text` with the comment markers and line breaks gone and runs of blanks made one."""
    return re.sub(r"\s+", " ", text.replace("#", " ")).strip()


def dataset_header(family: str, namespace: str) -> str:
    """The comment lines above the dataset's first key, squashed."""
    root = app.registrations.JURISDICTIONS.roots()[Namespace(namespace)]
    name = family.removeprefix(f"{namespace}/")
    lines = (root / "parameters" / name / "2025.yaml").read_text().splitlines()
    first_key = next(i for i, line in enumerate(lines) if line[:1] != "#")
    return squashed("\n".join(lines[:first_key]))


def line_23(credit: str, foreign_part: str, foreign_total: str) -> Decimal:
    capability = ApplyRatioOrZero(
        SOURCE.get(LINE_23_ROUNDING, 2025, ROUNDING_ONLY),
        CREDIT,
        FOREIGN_PART,
        FOREIGN_TOTAL,
        SHARE_OF_CREDIT,
    )
    (output,) = capability.compute(
        (
            Artifact(CREDIT, D(credit)),
            Artifact(FOREIGN_PART, D(foreign_part)),
            Artifact(FOREIGN_TOTAL, D(foreign_total)),
        )
    ).outputs
    assert isinstance(output.value, Decimal)
    return output.value


def test_2025_line_23_rounding_is_half_up_to_the_cent_with_no_other_figure() -> None:
    data = SOURCE.get(LINE_23_ROUNDING, 2025, ROUNDING_ONLY)

    assert data.values == RoundingOnly()
    assert data.rounding == CENT


def test_2025_line_23_rounding_cites_only_the_t1206_pdf() -> None:
    assert SOURCE.get(LINE_23_ROUNDING, 2025, ROUNDING_ONLY).sources == (T1206_PDF,)


def test_the_line_23_header_quotes_t1206_as_the_form_prints_it() -> None:
    header = dataset_header(LINE_23_ROUNDING, "ca")

    for quoted in (
        "Part of the amount on line 3 that is from foreign sources",
        "Total income from foreign sources",
        "× Amount from line 40500 of your return",
    ):
        assert quoted in header, quoted


def test_the_line_23_header_states_the_half_up_cent_rule() -> None:
    header = dataset_header(LINE_23_ROUNDING, "ca").lower()

    assert "dollars-and-cents box" in header
    assert "half-up" in header
    assert "owner decided" in header or "owner's decision" in header


def test_line_23_is_the_credit_times_the_foreign_share_rounded_once() -> None:
    # 500.00 × 1000 / 3000 = 166.666..., rounded half-up to the cent once, not after the quotient.
    assert line_23("500.00", "1000", "3000") == D("166.67")
    assert line_23("500.00", "1500", "3000") == D("250.00")


def test_line_23_is_zero_when_there_is_no_income_from_foreign_sources() -> None:
    assert line_23("500.00", "0", "0") == D("0.00")
