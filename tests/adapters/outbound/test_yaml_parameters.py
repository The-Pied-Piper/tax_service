"""Unit tests for YamlParameterSource: parameter dataset files -> domain parameters.

Datasets live at <directory>/<family>/<tax_year>.yaml. Values are made up.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from textwrap import dedent

import pytest

from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.domain.errors import DomainError, InvalidParameterDataError, NotFoundError
from app.domain.parameters.brackets import Bracket, BracketSchedule
from app.domain.parameters.credit import Credit
from app.domain.parameters.datasets import BracketParameters, CreditParameters
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundTo

D = Decimal

BRACKETS_2025 = """\
family: ex/brackets
tax_year: 2025
sources:
  - https://example.org/rates-2025
rounding: none
brackets:
  - {from: "0", rate: "0.10"}
  - {from: "100", rate: "0.20"}
"""


def write(directory: Path, relative: str, content: str) -> None:
    path = directory / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content), encoding="utf-8")


def test_parses_a_bracket_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/brackets/2025.yaml", BRACKETS_2025)

    result = YamlParameterSource(tmp_path).get_brackets("ex/brackets", 2025)

    assert result == BracketParameters(
        family="ex/brackets",
        tax_year=2025,
        schedule=BracketSchedule((Bracket(D("0"), D("0.10")), Bracket(D("100"), D("0.20")))),
        rounding=NO_ROUNDING,
        sources=("https://example.org/rates-2025",),
    )


def test_parses_a_rounding_rule(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/brackets/2025.yaml",
        BRACKETS_2025.replace("rounding: none", 'rounding: {increment: "0.01", mode: half_up}'),
    )

    result = YamlParameterSource(tmp_path).get_brackets("ex/brackets", 2025)

    assert result.rounding == RoundTo(D("0.01"), RoundingMode.HALF_UP)


def test_absent_year_is_not_found_and_never_carried_forward(tmp_path: Path) -> None:
    write(tmp_path, "ex/brackets/2025.yaml", BRACKETS_2025)

    with pytest.raises(NotFoundError, match="ex/brackets.*2026"):
        YamlParameterSource(tmp_path).get_brackets("ex/brackets", 2026)


def test_absent_family_is_not_found(tmp_path: Path) -> None:
    with pytest.raises(NotFoundError, match="ex/other"):
        YamlParameterSource(tmp_path).get_brackets("ex/other", 2025)


@pytest.mark.parametrize("family", ["", "EX/brackets", "../brackets", "ex/../x", "/ex/b", "ex/"])
def test_rejects_malformed_family(tmp_path: Path, family: str) -> None:
    with pytest.raises(ValueError, match="parameter family"):
        YamlParameterSource(tmp_path).get_brackets(family, 2025)


def test_invalid_data_is_a_domain_error() -> None:
    assert issubclass(InvalidParameterDataError, DomainError)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param(
            BRACKETS_2025.replace("family: ex/brackets", "family: ex/other"),
            "family 'ex/other' does not match",
            id="family-mismatch",
        ),
        pytest.param(
            BRACKETS_2025.replace("tax_year: 2025", "tax_year: 2024"),
            "tax_year 2024 does not match",
            id="year-mismatch",
        ),
        pytest.param(BRACKETS_2025 + "extra: 1\n", r"unknown keys \['extra'\]", id="unknown-key"),
        pytest.param(
            BRACKETS_2025.replace("rounding: none\n", ""),
            r"missing keys \['rounding'\]",
            id="rounding-missing",
        ),
        pytest.param(
            BRACKETS_2025 + "tax_year: 2025\n", "duplicate key 'tax_year'", id="duplicate-key"
        ),
        pytest.param(
            BRACKETS_2025.replace('rate: "0.10"', "rate: 0.10"),
            r"brackets\[0\].rate must be a string, got float",
            id="rate-as-yaml-number",
        ),
        pytest.param(
            BRACKETS_2025.replace('rate: "0.10"', 'rate: "ten"'),
            r"brackets\[0\].rate is not a decimal: 'ten'",
            id="rate-not-decimal",
        ),
        pytest.param(
            BRACKETS_2025.replace('rate: "0.10"', 'rate: "NaN"'),
            r"brackets\[0\].rate is not a decimal: 'NaN'",
            id="rate-nan",
        ),
        pytest.param(
            BRACKETS_2025.replace('{from: "100"', '{from: "0"'),
            "strictly ascending",
            id="schedule-invalid",
        ),
        pytest.param(
            BRACKETS_2025.replace("rounding: none", "rounding: always"),
            "rounding must be 'none' or a mapping",
            id="rounding-unknown-word",
        ),
        pytest.param(
            BRACKETS_2025.replace(
                "rounding: none", 'rounding: {increment: "0.01", mode: sideways}'
            ),
            "rounding.mode 'sideways' is not one of",
            id="rounding-unknown-mode",
        ),
        pytest.param(
            BRACKETS_2025.replace("rounding: none", 'rounding: {increment: "0", mode: down}'),
            "increment must be a positive",
            id="rounding-zero-increment",
        ),
        pytest.param(
            BRACKETS_2025.replace("sources:\n  - https://example.org/rates-2025", "sources: []"),
            "sources must list at least one",
            id="sources-empty",
        ),
        pytest.param("", "dataset must be a mapping", id="empty-file"),
    ],
)
def test_rejects_malformed_dataset(tmp_path: Path, content: str, message: str) -> None:
    write(tmp_path, "ex/brackets/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        YamlParameterSource(tmp_path).get_brackets("ex/brackets", 2025)

    assert "2025.yaml" in str(excinfo.value)


CREDIT_2025 = """\
family: ex/personal_credit
tax_year: 2025
sources:
  - https://example.org/credits-2025
rounding: none
amount: "1000"
rate: "0.125"
"""


def test_parses_a_credit_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/personal_credit/2025.yaml", CREDIT_2025)

    result = YamlParameterSource(tmp_path).get_credit("ex/personal_credit", 2025)

    assert result == CreditParameters(
        family="ex/personal_credit",
        tax_year=2025,
        credit=Credit(amount=D("1000"), rate=D("0.125")),
        rounding=NO_ROUNDING,
        sources=("https://example.org/credits-2025",),
    )


def test_absent_credit_year_is_not_found(tmp_path: Path) -> None:
    with pytest.raises(NotFoundError, match="ex/personal_credit.*2025"):
        YamlParameterSource(tmp_path).get_credit("ex/personal_credit", 2025)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param(
            CREDIT_2025.replace('rate: "0.125"', 'rate: "1.5"'),
            "rate must be between 0 and 1",
            id="rate-out-of-range",
        ),
        pytest.param(
            CREDIT_2025.replace('amount: "1000"', "amount: 1000"),
            "amount must be a string, got int",
            id="amount-as-yaml-number",
        ),
        pytest.param(
            CREDIT_2025.replace('amount: "1000"\n', ""),
            r"missing keys \['amount'\]",
            id="amount-missing",
        ),
        pytest.param(
            CREDIT_2025 + "brackets: []\n",
            r"unknown keys \['brackets'\]",
            id="bracket-key-in-credit",
        ),
    ],
)
def test_rejects_malformed_credit_dataset(tmp_path: Path, content: str, message: str) -> None:
    write(tmp_path, "ex/personal_credit/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        YamlParameterSource(tmp_path).get_credit("ex/personal_credit", 2025)

    assert "2025.yaml" in str(excinfo.value)
