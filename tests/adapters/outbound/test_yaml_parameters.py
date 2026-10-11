"""Unit tests for YamlParameterSource: parameter dataset files -> ParameterDataset.

Datasets live at <directory>/<family>/<tax_year>.yaml and declare their kind.
Each kind is parsed by the parser registered for it, so new kinds need no change here.
Tests inject their own ParameterParserRegistry; by default the source reads the shared one.
Values are made up.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from textwrap import dedent

import pytest

from app.adapters.outbound.parameter_parsers.brackets import BracketsParser
from app.adapters.outbound.parameter_parsers.credit import CreditParser
from app.adapters.outbound.parameter_parsers.registry import ParameterParserRegistry
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.adapters.outbound.yaml_support import YamlNode
from app.domain.errors import (
    DomainError,
    InvalidParameterDataError,
    NotFoundError,
    UnknownRegistrationError,
)
from app.domain.parameters.brackets import BRACKETS, Bracket, BracketSchedule
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundTo

D = Decimal

BRACKETS_2025 = """\
family: ex/brackets
tax_year: 2025
kind: brackets
sources:
  - https://example.org/rates-2025
rounding: none
brackets:
  - {from: "0", rate: "0.10"}
  - {from: "100", rate: "0.20"}
"""

CREDIT_2025 = """\
family: ex/personal_credit
tax_year: 2025
kind: credit
sources:
  - https://example.org/credits-2025
rounding: none
amount: "1000"
rate: "0.125"
"""


def built_in_parsers() -> ParameterParserRegistry:
    """A fresh registry holding the built-in parsers, never the shared one."""
    registry = ParameterParserRegistry()
    registry.register_parser(BracketsParser())
    registry.register_parser(CreditParser())
    return registry


def source(directory: Path) -> YamlParameterSource:
    return YamlParameterSource(directory, parsers=built_in_parsers())


def write(directory: Path, relative: str, content: str) -> None:
    path = directory / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content), encoding="utf-8")


# --- reading each built-in kind ---------------------------------------------------


def test_reads_a_bracket_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/brackets/2025.yaml", BRACKETS_2025)

    result = source(tmp_path).get("ex/brackets", 2025, BRACKETS)

    assert result == ParameterDataset(
        family="ex/brackets",
        tax_year=2025,
        kind=BRACKETS,
        values=BracketSchedule((Bracket(D("0"), D("0.10")), Bracket(D("100"), D("0.20")))),
        rounding=NO_ROUNDING,
        sources=("https://example.org/rates-2025",),
    )


def test_reads_a_credit_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/personal_credit/2025.yaml", CREDIT_2025)

    result = source(tmp_path).get("ex/personal_credit", 2025, CREDIT)

    assert result == ParameterDataset(
        family="ex/personal_credit",
        tax_year=2025,
        kind=CREDIT,
        values=Credit(amount=D("1000"), rate=D("0.125")),
        rounding=NO_ROUNDING,
        sources=("https://example.org/credits-2025",),
    )


def test_reads_a_rounding_rule(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/brackets/2025.yaml",
        BRACKETS_2025.replace("rounding: none", 'rounding: {increment: "0.01", mode: half_up}'),
    )

    result = source(tmp_path).get("ex/brackets", 2025, BRACKETS)

    assert result.rounding == RoundTo(D("0.01"), RoundingMode.HALF_UP)


# --- open for extension -------------------------------------------------------------

FLAT_RATE = ParameterKind("flat_rate", Decimal)


class FlatRateParser:
    """A kind the adapter has never heard of, added purely by registering a parser."""

    kind = FLAT_RATE
    body_keys = frozenset({"rate"})

    def parse(self, document: YamlNode) -> Decimal:
        return document.field("rate").parse_decimal()


def test_new_kinds_need_only_a_registered_parser(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/flat/2025.yaml",
        "family: ex/flat\ntax_year: 2025\nkind: flat_rate\n"
        'sources: [https://example.org]\nrounding: none\nrate: "0.2"\n',
    )
    parsers = built_in_parsers()
    parsers.register_parser(FlatRateParser())

    values: Decimal = (
        YamlParameterSource(tmp_path, parsers=parsers).get("ex/flat", 2025, FLAT_RATE).values
    )

    assert values == D("0.2")


def test_requesting_a_kind_without_a_parser_fails(tmp_path: Path) -> None:
    write(tmp_path, "ex/brackets/2025.yaml", BRACKETS_2025)

    with pytest.raises(UnknownRegistrationError, match="'flat_rate'"):
        source(tmp_path).get("ex/brackets", 2025, FLAT_RATE)


def test_parsers_are_read_from_the_injected_registry(tmp_path: Path) -> None:
    write(tmp_path, "ex/brackets/2025.yaml", BRACKETS_2025)
    parsers = ParameterParserRegistry()
    parsers.register_parser(CreditParser())

    with pytest.raises(UnknownRegistrationError, match="'brackets'"):
        YamlParameterSource(tmp_path, parsers=parsers).get("ex/brackets", 2025, BRACKETS)


def test_by_default_parsers_come_from_the_shared_registry(tmp_path: Path) -> None:
    # The built-in parsers registered themselves in the shared registry when imported.
    write(tmp_path, "ex/brackets/2025.yaml", BRACKETS_2025)

    result = YamlParameterSource(tmp_path).get("ex/brackets", 2025, BRACKETS)

    assert result.values == BracketSchedule(
        (Bracket(D("0"), D("0.10")), Bracket(D("100"), D("0.20")))
    )


# --- resolution -----------------------------------------------------------------------


def test_absent_year_is_not_found_and_never_carried_forward(tmp_path: Path) -> None:
    write(tmp_path, "ex/brackets/2025.yaml", BRACKETS_2025)

    with pytest.raises(NotFoundError, match="ex/brackets.*2026"):
        source(tmp_path).get("ex/brackets", 2026, BRACKETS)


def test_absent_family_is_not_found(tmp_path: Path) -> None:
    with pytest.raises(NotFoundError, match="ex/other"):
        source(tmp_path).get("ex/other", 2025, BRACKETS)


@pytest.mark.parametrize("family", ["", "EX/brackets", "../brackets", "ex/../x", "/ex/b", "ex/"])
def test_rejects_malformed_family(tmp_path: Path, family: str) -> None:
    with pytest.raises(ValueError, match="parameter family"):
        source(tmp_path).get(family, 2025, BRACKETS)


def test_invalid_data_is_a_domain_error() -> None:
    assert issubclass(InvalidParameterDataError, DomainError)


# --- malformed files -------------------------------------------------------------------


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param(
            BRACKETS_2025.replace("kind: brackets", "kind: credit"),
            "kind 'credit' does not match the requested 'brackets'",
            id="kind-mismatch",
        ),
        pytest.param(
            BRACKETS_2025.replace("kind: brackets\n", ""), "missing key 'kind'", id="kind-missing"
        ),
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
            BRACKETS_2025 + "amount: '1'\n",
            r"unknown keys \['amount'\]",
            id="other-kinds-key",
        ),
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
def test_rejects_malformed_bracket_dataset(tmp_path: Path, content: str, message: str) -> None:
    write(tmp_path, "ex/brackets/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        source(tmp_path).get("ex/brackets", 2025, BRACKETS)

    assert "2025.yaml" in str(excinfo.value)


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
    ],
)
def test_rejects_malformed_credit_dataset(tmp_path: Path, content: str, message: str) -> None:
    write(tmp_path, "ex/personal_credit/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        source(tmp_path).get("ex/personal_credit", 2025, CREDIT)

    assert "2025.yaml" in str(excinfo.value)
