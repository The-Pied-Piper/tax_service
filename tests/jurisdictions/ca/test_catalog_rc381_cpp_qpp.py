"""Registered, money and count kinds of the federal catalog family `rc381_cpp_qpp`.

Form RC381 (2025), "Inter-Provincial Calculation for CPP and QPP Contributions and Overpayments"
(`docs/cra-forms-2025/rc381-25e.pdf`): Part 2 (the months and the monthly proration table) and
Part 3 lines 1, 2, 3, 6 to 11, 14 to 16, 18 to 24 and 26. The four kinds a caller enters carry a
docstring that quotes the form's own words.
"""

from __future__ import annotations

import ast
import re
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

import app.jurisdictions.ca.catalog
from app.domain.artifact import ArtifactKind, ArtifactRegistry
from app.domain.parameters.rate import Rate
from app.jurisdictions.ca.catalog import (
    QPP_MONTHS,
    RC381_PART_2_LINE_B,
    RC381_PART_2_LINE_G,
    RC381_PART_2_LINE_H,
    RC381_PART_2_LINE_I,
    RC381_PART_2_LINE_J,
    RC381_PART_3_LINE_3,
    RC381_PART_3_LINE_6,
    RC381_PART_3_LINE_7,
    RC381_PART_3_LINE_8,
    RC381_PART_3_LINE_9,
    RC381_PART_3_LINE_10,
    RC381_PART_3_LINE_11,
    RC381_PART_3_LINE_14,
    RC381_PART_3_LINE_15,
    RC381_PART_3_LINE_15_LESSER,
    RC381_PART_3_LINE_16,
    RC381_PART_3_LINE_18,
    RC381_PART_3_LINE_20,
    RC381_PART_3_LINE_21,
    RC381_PART_3_LINE_22,
    RC381_PART_3_LINE_23,
    RC381_PART_3_LINE_24,
    RC381_PART_3_LINE_26,
    T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC,
    T4_QPP_PENSIONABLE_EARNINGS_IN_QUEBEC,
)

INPUT_AMOUNTS: tuple[ArtifactKind[Decimal], ...] = (
    T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC,
    T4_QPP_PENSIONABLE_EARNINGS_IN_QUEBEC,
)

PART_2_AMOUNTS: tuple[ArtifactKind[Decimal], ...] = (
    RC381_PART_2_LINE_G,
    RC381_PART_2_LINE_H,
    RC381_PART_2_LINE_I,
    RC381_PART_2_LINE_J,
)

PART_3_AMOUNTS: tuple[ArtifactKind[Decimal], ...] = (
    RC381_PART_3_LINE_3,
    RC381_PART_3_LINE_7,
    RC381_PART_3_LINE_8,
    RC381_PART_3_LINE_9,
    RC381_PART_3_LINE_10,
    RC381_PART_3_LINE_11,
    RC381_PART_3_LINE_14,
    RC381_PART_3_LINE_15_LESSER,
    RC381_PART_3_LINE_15,
    RC381_PART_3_LINE_16,
    RC381_PART_3_LINE_18,
    RC381_PART_3_LINE_20,
    RC381_PART_3_LINE_21,
    RC381_PART_3_LINE_22,
    RC381_PART_3_LINE_23,
    RC381_PART_3_LINE_24,
    RC381_PART_3_LINE_26,
)


def test_the_rc381_part_2_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/qpp_months") is QPP_MONTHS
    assert registry.get("ca/rc381_part_2_line_b") is RC381_PART_2_LINE_B
    assert registry.get("ca/rc381_part_2_line_g") is RC381_PART_2_LINE_G
    assert registry.get("ca/rc381_part_2_line_h") is RC381_PART_2_LINE_H
    assert registry.get("ca/rc381_part_2_line_i") is RC381_PART_2_LINE_I
    assert registry.get("ca/rc381_part_2_line_j") is RC381_PART_2_LINE_J


def test_the_rc381_part_3_input_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert (
        registry.get("ca/t4_cpp_pensionable_earnings_outside_quebec")
        is T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC
    )
    assert (
        registry.get("ca/t4_qpp_pensionable_earnings_in_quebec")
        is T4_QPP_PENSIONABLE_EARNINGS_IN_QUEBEC
    )


def test_the_rc381_part_3_line_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/rc381_part_3_line_3") is RC381_PART_3_LINE_3
    assert registry.get("ca/rc381_part_3_line_6") is RC381_PART_3_LINE_6
    assert registry.get("ca/rc381_part_3_line_7") is RC381_PART_3_LINE_7
    assert registry.get("ca/rc381_part_3_line_8") is RC381_PART_3_LINE_8
    assert registry.get("ca/rc381_part_3_line_9") is RC381_PART_3_LINE_9
    assert registry.get("ca/rc381_part_3_line_10") is RC381_PART_3_LINE_10
    assert registry.get("ca/rc381_part_3_line_11") is RC381_PART_3_LINE_11
    assert registry.get("ca/rc381_part_3_line_14") is RC381_PART_3_LINE_14
    # Line 15's "Enter whichever is less: amount from line 10 or line 14.", before the gate on
    # line 3 against line C that decides whether line 15 takes it.
    assert registry.get("ca/rc381_part_3_line_15_lesser") is RC381_PART_3_LINE_15_LESSER
    assert registry.get("ca/rc381_part_3_line_15") is RC381_PART_3_LINE_15
    assert registry.get("ca/rc381_part_3_line_16") is RC381_PART_3_LINE_16
    assert registry.get("ca/rc381_part_3_line_18") is RC381_PART_3_LINE_18
    assert registry.get("ca/rc381_part_3_line_20") is RC381_PART_3_LINE_20
    assert registry.get("ca/rc381_part_3_line_21") is RC381_PART_3_LINE_21
    assert registry.get("ca/rc381_part_3_line_22") is RC381_PART_3_LINE_22
    assert registry.get("ca/rc381_part_3_line_23") is RC381_PART_3_LINE_23
    assert registry.get("ca/rc381_part_3_line_24") is RC381_PART_3_LINE_24
    assert registry.get("ca/rc381_part_3_line_26") is RC381_PART_3_LINE_26


def test_the_rc381_amounts_are_money() -> None:
    for kind in (*INPUT_AMOUNTS, *PART_2_AMOUNTS, *PART_3_AMOUNTS):
        assert kind.value_type is Decimal, kind.identifier


def test_line_6_is_a_rate_kind() -> None:
    # Line 6 "Line 4 divided by line 5 (calculated to the fifth decimal place without rounding)" is
    # "the rate at line 6" that lines 7 to 10 multiply by: a `Rate` (0 to 1), not money.
    assert RC381_PART_3_LINE_6.value_type is Rate


def test_the_rc381_months_are_counts() -> None:
    # Line B is a count of months the filer enters, and the line B the table is read with is the
    # same count after the check that line A "cannot be more than the number you enter on line B".
    assert QPP_MONTHS.value_type is int
    assert RC381_PART_2_LINE_B.value_type is int


def test_every_rc381_kind_is_non_negative() -> None:
    kinds: tuple[ArtifactKind[Any], ...] = (
        QPP_MONTHS,
        RC381_PART_2_LINE_B,
        *INPUT_AMOUNTS,
        *PART_2_AMOUNTS,
        *PART_3_AMOUNTS,
    )
    for kind in kinds:
        assert kind.non_negative is True, kind.identifier
    # A rate kind is bounded by `Rate` itself (0 to 1), as the Ontario CARE credit rate is.


# The words of the form each input's docstring quotes (`docs/cra-forms-2025/rc381-25e.pdf`), and
# the box number of the line, which the form prints beside it.
INPUT_QUOTES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("qpp_months", ("Enter the number of months that QPP applied in 2025.", "Part 2")),
    (
        "t4_cpp_pensionable_earnings_outside_quebec",
        (
            "Total CPP pensionable earnings from box 26 of all of your T4 slips where the "
            "province of employment is not Quebec",
            "50339",
            "Part 3",
        ),
    ),
    (
        "t4_qpp_pensionable_earnings_in_quebec",
        (
            "Total QPP pensionable earnings from box 26 of all of your T4 slips where the "
            "province of employment is Quebec",
            "50329",
            "Part 3",
        ),
    ),
)


def squashed(text: str) -> str:
    """`text` with every run of white space made one blank."""
    return re.sub(r"\s+", " ", text).strip()


def docstring_of(name: str) -> str:
    """The string right after `NAME = CATALOG.declare("<name>", ...)` in a catalog module."""
    folder = Path(app.jurisdictions.ca.catalog.__file__).parent
    for path in sorted(folder.glob("*.py")):
        body = ast.parse(path.read_text()).body
        for statement, following in zip(body, body[1:], strict=False):
            if not (isinstance(statement, ast.Assign) and isinstance(statement.value, ast.Call)):
                continue
            arguments = statement.value.args
            if not (
                arguments
                and isinstance(arguments[0], ast.Constant)
                and arguments[0].value == name
                and isinstance(following, ast.Expr)
                and isinstance(following.value, ast.Constant)
            ):
                continue
            return str(following.value.value)
    raise AssertionError(f"no declaration of {name!r} followed by a docstring")


@pytest.mark.parametrize(("name", "quotes"), INPUT_QUOTES, ids=[n for n, _ in INPUT_QUOTES])
def test_each_rc381_input_docstring_quotes_the_form(name: str, quotes: tuple[str, ...]) -> None:
    docstring = squashed(docstring_of(name))

    assert "RC381" in docstring
    for quote in quotes:
        assert squashed(quote) in docstring, quote
