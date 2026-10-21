"""Registered, money and count kinds of the federal catalog family `rc381_cpp_qpp`.

Form RC381 (2025), "Inter-Provincial Calculation for CPP and QPP Contributions and Overpayments"
(`docs/cra-forms-2025/rc381-25e.pdf`): Part 2 (the months and the monthly proration table) and
Part 3 lines 1 to 3, 6 to 11, 14 to 16, 18 to 24, 26 to 31, 34 to 36, 38, 40 to 44, 46, 49, 52, 53,
56, 59 to 61, 64 and 67 to 69, and the entries on lines 19, 25, 39 and 45, then Part 3a and Part 3b
(lines 73, 75 to 93, the helper under line 87 and the three results for lines 30800, 22215 and
44800). The seven kinds a caller enters and the three results carry a docstring that quotes the
form's own words. Lines 53, 60, 61, 68 and 69 are signed: "if negative, show in brackets". So is
the helper under line 87, "the result of line 68 minus line 80".
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
    RC381_CPP_OVERPAYMENT,
    RC381_EMPLOYMENT_CPP_BASE_CONTRIBUTIONS,
    RC381_EMPLOYMENT_CPP_ENHANCED_CONTRIBUTIONS,
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
    RC381_PART_3_LINE_27,
    RC381_PART_3_LINE_28,
    RC381_PART_3_LINE_29,
    RC381_PART_3_LINE_30,
    RC381_PART_3_LINE_31,
    RC381_PART_3_LINE_34,
    RC381_PART_3_LINE_35,
    RC381_PART_3_LINE_35_LESSER,
    RC381_PART_3_LINE_36,
    RC381_PART_3_LINE_38,
    RC381_PART_3_LINE_40,
    RC381_PART_3_LINE_41,
    RC381_PART_3_LINE_42,
    RC381_PART_3_LINE_43,
    RC381_PART_3_LINE_44,
    RC381_PART_3_LINE_46,
    RC381_PART_3_LINE_49,
    RC381_PART_3_LINE_52,
    RC381_PART_3_LINE_53,
    RC381_PART_3_LINE_56,
    RC381_PART_3_LINE_59,
    RC381_PART_3_LINE_60,
    RC381_PART_3_LINE_61,
    RC381_PART_3_LINE_64,
    RC381_PART_3_LINE_67,
    RC381_PART_3_LINE_68,
    RC381_PART_3_LINE_69,
    RC381_PART_3_LINE_73,
    RC381_PART_3_LINE_75,
    RC381_PART_3_LINE_76,
    RC381_PART_3_LINE_77,
    RC381_PART_3_LINE_78,
    RC381_PART_3_LINE_79,
    RC381_PART_3_LINE_80,
    RC381_PART_3_LINE_81,
    RC381_PART_3_LINE_82,
    RC381_PART_3_LINE_83,
    RC381_PART_3_LINE_84,
    RC381_PART_3_LINE_85,
    RC381_PART_3_LINE_86,
    RC381_PART_3_LINE_87,
    RC381_PART_3_LINE_87_DIFFERENCE,
    RC381_PART_3_LINE_88,
    RC381_PART_3_LINE_89,
    RC381_PART_3_LINE_90,
    RC381_PART_3_LINE_91,
    RC381_PART_3_LINE_92,
    RC381_PART_3_LINE_93,
    T4_CPP_CONTRIBUTIONS_BOX_16,
    T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC,
    T4_CPP_SECOND_ADDITIONAL_BOX_16A,
    T4_QPP_CONTRIBUTIONS_BOX_17,
    T4_QPP_PENSIONABLE_EARNINGS_IN_QUEBEC,
    T4_QPP_SECOND_ADDITIONAL_BOX_17A,
)

INPUT_AMOUNTS: tuple[ArtifactKind[Decimal], ...] = (
    T4_CPP_PENSIONABLE_EARNINGS_OUTSIDE_QUEBEC,
    T4_QPP_PENSIONABLE_EARNINGS_IN_QUEBEC,
    T4_CPP_CONTRIBUTIONS_BOX_16,
    T4_CPP_SECOND_ADDITIONAL_BOX_16A,
    T4_QPP_CONTRIBUTIONS_BOX_17,
    T4_QPP_SECOND_ADDITIONAL_BOX_17A,
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
    RC381_PART_3_LINE_27,
    RC381_PART_3_LINE_28,
    RC381_PART_3_LINE_29,
    RC381_PART_3_LINE_30,
    RC381_PART_3_LINE_31,
    RC381_PART_3_LINE_34,
    RC381_PART_3_LINE_35_LESSER,
    RC381_PART_3_LINE_35,
    RC381_PART_3_LINE_36,
    RC381_PART_3_LINE_38,
    RC381_PART_3_LINE_40,
    RC381_PART_3_LINE_41,
    RC381_PART_3_LINE_42,
    RC381_PART_3_LINE_43,
    RC381_PART_3_LINE_44,
    RC381_PART_3_LINE_46,
    RC381_PART_3_LINE_49,
    RC381_PART_3_LINE_52,
    RC381_PART_3_LINE_56,
    RC381_PART_3_LINE_59,
    RC381_PART_3_LINE_64,
    RC381_PART_3_LINE_67,
    RC381_PART_3_LINE_73,
    RC381_PART_3_LINE_75,
    RC381_PART_3_LINE_76,
    RC381_PART_3_LINE_77,
    RC381_PART_3_LINE_78,
    RC381_PART_3_LINE_79,
    RC381_PART_3_LINE_80,
    RC381_PART_3_LINE_81,
    RC381_PART_3_LINE_82,
    RC381_PART_3_LINE_83,
    RC381_PART_3_LINE_84,
    RC381_PART_3_LINE_85,
    RC381_PART_3_LINE_86,
    RC381_PART_3_LINE_87,
    RC381_PART_3_LINE_88,
    RC381_PART_3_LINE_89,
    RC381_PART_3_LINE_90,
    RC381_PART_3_LINE_91,
    RC381_PART_3_LINE_92,
    RC381_PART_3_LINE_93,
)

# The three results of Part 3a and Part 3b for "earnings subject to contributions ... from
# employment income only": lines 30800, 22215 and 44800 of the return.
RESULT_AMOUNTS: tuple[ArtifactKind[Decimal], ...] = (
    RC381_EMPLOYMENT_CPP_BASE_CONTRIBUTIONS,
    RC381_EMPLOYMENT_CPP_ENHANCED_CONTRIBUTIONS,
    RC381_CPP_OVERPAYMENT,
)

# Lines whose difference or sum can come out below zero: "if negative, show in brackets".
SIGNED_AMOUNTS: tuple[ArtifactKind[Decimal], ...] = (
    RC381_PART_3_LINE_53,
    RC381_PART_3_LINE_60,
    RC381_PART_3_LINE_61,
    RC381_PART_3_LINE_68,
    RC381_PART_3_LINE_69,
    RC381_PART_3_LINE_87_DIFFERENCE,
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
    assert registry.get("ca/t4_cpp_contributions_box_16") is T4_CPP_CONTRIBUTIONS_BOX_16
    assert registry.get("ca/t4_cpp_second_additional_box_16a") is T4_CPP_SECOND_ADDITIONAL_BOX_16A
    assert registry.get("ca/t4_qpp_contributions_box_17") is T4_QPP_CONTRIBUTIONS_BOX_17
    assert registry.get("ca/t4_qpp_second_additional_box_17a") is T4_QPP_SECOND_ADDITIONAL_BOX_17A


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
    assert registry.get("ca/rc381_part_3_line_27") is RC381_PART_3_LINE_27
    assert registry.get("ca/rc381_part_3_line_28") is RC381_PART_3_LINE_28
    assert registry.get("ca/rc381_part_3_line_29") is RC381_PART_3_LINE_29
    assert registry.get("ca/rc381_part_3_line_30") is RC381_PART_3_LINE_30
    assert registry.get("ca/rc381_part_3_line_31") is RC381_PART_3_LINE_31
    assert registry.get("ca/rc381_part_3_line_34") is RC381_PART_3_LINE_34
    # Line 35 "Enter whichever is less: amount from line 30 or line 34.", before the gate on
    # line 3 against line G that decides whether line 35 takes it.
    assert registry.get("ca/rc381_part_3_line_35_lesser") is RC381_PART_3_LINE_35_LESSER
    assert registry.get("ca/rc381_part_3_line_35") is RC381_PART_3_LINE_35
    assert registry.get("ca/rc381_part_3_line_36") is RC381_PART_3_LINE_36
    assert registry.get("ca/rc381_part_3_line_38") is RC381_PART_3_LINE_38
    assert registry.get("ca/rc381_part_3_line_40") is RC381_PART_3_LINE_40
    assert registry.get("ca/rc381_part_3_line_41") is RC381_PART_3_LINE_41
    assert registry.get("ca/rc381_part_3_line_42") is RC381_PART_3_LINE_42
    assert registry.get("ca/rc381_part_3_line_43") is RC381_PART_3_LINE_43
    assert registry.get("ca/rc381_part_3_line_44") is RC381_PART_3_LINE_44
    assert registry.get("ca/rc381_part_3_line_46") is RC381_PART_3_LINE_46
    assert registry.get("ca/rc381_part_3_line_49") is RC381_PART_3_LINE_49
    assert registry.get("ca/rc381_part_3_line_52") is RC381_PART_3_LINE_52
    assert registry.get("ca/rc381_part_3_line_53") is RC381_PART_3_LINE_53
    assert registry.get("ca/rc381_part_3_line_56") is RC381_PART_3_LINE_56
    assert registry.get("ca/rc381_part_3_line_59") is RC381_PART_3_LINE_59
    assert registry.get("ca/rc381_part_3_line_60") is RC381_PART_3_LINE_60
    assert registry.get("ca/rc381_part_3_line_61") is RC381_PART_3_LINE_61
    assert registry.get("ca/rc381_part_3_line_64") is RC381_PART_3_LINE_64
    assert registry.get("ca/rc381_part_3_line_67") is RC381_PART_3_LINE_67
    assert registry.get("ca/rc381_part_3_line_68") is RC381_PART_3_LINE_68
    assert registry.get("ca/rc381_part_3_line_69") is RC381_PART_3_LINE_69
    assert registry.get("ca/rc381_part_3_line_73") is RC381_PART_3_LINE_73
    assert registry.get("ca/rc381_part_3_line_75") is RC381_PART_3_LINE_75
    assert registry.get("ca/rc381_part_3_line_76") is RC381_PART_3_LINE_76
    assert registry.get("ca/rc381_part_3_line_77") is RC381_PART_3_LINE_77
    assert registry.get("ca/rc381_part_3_line_78") is RC381_PART_3_LINE_78
    assert registry.get("ca/rc381_part_3_line_79") is RC381_PART_3_LINE_79
    assert registry.get("ca/rc381_part_3_line_80") is RC381_PART_3_LINE_80
    assert registry.get("ca/rc381_part_3_line_81") is RC381_PART_3_LINE_81
    assert registry.get("ca/rc381_part_3_line_82") is RC381_PART_3_LINE_82
    assert registry.get("ca/rc381_part_3_line_83") is RC381_PART_3_LINE_83
    assert registry.get("ca/rc381_part_3_line_84") is RC381_PART_3_LINE_84
    assert registry.get("ca/rc381_part_3_line_85") is RC381_PART_3_LINE_85
    assert registry.get("ca/rc381_part_3_line_86") is RC381_PART_3_LINE_86
    assert registry.get("ca/rc381_part_3_line_87") is RC381_PART_3_LINE_87
    # Line 87 "the result of line 68 minus line 80", printed inside the line: a step of its own.
    assert registry.get("ca/rc381_part_3_line_87_difference") is RC381_PART_3_LINE_87_DIFFERENCE
    assert registry.get("ca/rc381_part_3_line_88") is RC381_PART_3_LINE_88
    assert registry.get("ca/rc381_part_3_line_89") is RC381_PART_3_LINE_89
    assert registry.get("ca/rc381_part_3_line_90") is RC381_PART_3_LINE_90
    assert registry.get("ca/rc381_part_3_line_91") is RC381_PART_3_LINE_91
    assert registry.get("ca/rc381_part_3_line_92") is RC381_PART_3_LINE_92
    assert registry.get("ca/rc381_part_3_line_93") is RC381_PART_3_LINE_93
    assert registry.get("ca/rc381_employment_cpp_base_contributions") is (
        RC381_EMPLOYMENT_CPP_BASE_CONTRIBUTIONS
    )
    assert registry.get("ca/rc381_employment_cpp_enhanced_contributions") is (
        RC381_EMPLOYMENT_CPP_ENHANCED_CONTRIBUTIONS
    )
    assert registry.get("ca/rc381_cpp_overpayment") is RC381_CPP_OVERPAYMENT


def test_the_rc381_amounts_are_money() -> None:
    for kind in (
        *INPUT_AMOUNTS,
        *PART_2_AMOUNTS,
        *PART_3_AMOUNTS,
        *RESULT_AMOUNTS,
        *SIGNED_AMOUNTS,
    ):
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
        *RESULT_AMOUNTS,
    )
    for kind in kinds:
        assert kind.non_negative is True, kind.identifier
    # A rate kind is bounded by `Rate` itself (0 to 1), as the Ontario CARE credit rate is.


def test_the_rc381_lines_that_may_be_negative_are_signed() -> None:
    # Line 53 "Line 49 minus line 52 (if negative, show in brackets)", line 60 "Line 56 minus line
    # 59 (if negative, show in brackets)", line 61 "Line 53 plus line 60 (if negative, show in
    # brackets)", line 68 "Line 64 minus line 67 (if negative, show in brackets)" and line 69
    # "Line 61 plus line 68 (if negative, show in brackets)": the actual contributions can be less
    # than the required ones, so these are not non-negative.
    # Line 87 helper "the result of line 68 minus line 80": line 68 may be negative while line
    # 80 is "0", so the difference can be below zero.
    for kind in SIGNED_AMOUNTS:
        assert kind.non_negative is False, kind.identifier


# The words of the form each result's docstring quotes.
RESULT_QUOTES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "rc381_employment_cpp_base_contributions",
        (
            "Enter this amount (in dollars and cents) on line 30800 of your return.",
            "Part 3a",
            "Part 3b",
            "line 69",
        ),
    ),
    (
        "rc381_employment_cpp_enhanced_contributions",
        (
            "Enter this amount (in dollars and cents) on line 22215 of your return.",
            "Part 3a",
            "Part 3b",
            "line 69",
        ),
    ),
    (
        "rc381_cpp_overpayment",
        (
            "Enter this amount (in dollars and cents) on line 44800 of your return.",
            "Part 3a",
            "line 69",
        ),
    ),
)

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
    (
        "t4_cpp_contributions_box_16",
        (
            "Total actual base and first additional contributions on CPP pensionable earnings "
            "from box 16 of all of your T4 slips",
            "50340",
            "Part 3",
        ),
    ),
    (
        "t4_cpp_second_additional_box_16a",
        (
            "Total actual second additional contributions on CPP pensionable earnings from box "
            "16A of all of your T4 slips",
            "50341",
            "Part 3",
        ),
    ),
    (
        "t4_qpp_contributions_box_17",
        (
            "Total actual base and first additional contributions on QPP pensionable earnings "
            "from box 17 of all of your T4 slips",
            "50330",
            "Part 3",
        ),
    ),
    (
        "t4_qpp_second_additional_box_17a",
        (
            "Total actual second additional contributions on QPP pensionable earnings from box "
            "17A of all of your T4 slips",
            "50331",
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


@pytest.mark.parametrize(("name", "quotes"), RESULT_QUOTES, ids=[n for n, _ in RESULT_QUOTES])
def test_each_rc381_result_docstring_quotes_the_form(name: str, quotes: tuple[str, ...]) -> None:
    docstring = squashed(docstring_of(name))

    assert "RC381" in docstring
    for quote in quotes:
        assert squashed(quote) in docstring, quote
