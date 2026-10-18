"""Unit tests for YamlParameterSource: parameter dataset files -> ParameterDataset.

The source takes a mapping of namespace -> package directory. Family `ex/brackets` for 2025 lives
at `roots[Namespace("ex")] / "parameters" / "brackets" / "2025.yaml"`; the namespace is the part of
the family before the first `/`. Datasets declare their kind.
Each kind is parsed by the parser registered for it, so new kinds need no change here.
Tests inject their own ParameterParserRegistry; by default the source reads the shared one.
Values are made up.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from pathlib import Path
from textwrap import dedent

import pytest

from app.adapters.outbound.parameter_parsers.amount import AmountParser
from app.adapters.outbound.parameter_parsers.brackets import BracketsParser
from app.adapters.outbound.parameter_parsers.contribution_tier import ContributionTierParser
from app.adapters.outbound.parameter_parsers.credit import CreditParser
from app.adapters.outbound.parameter_parsers.rate import RateParser
from app.adapters.outbound.parameter_parsers.registry import ParameterParserRegistry
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.adapters.outbound.yaml_support import YamlNode
from app.domain.errors import (
    DomainError,
    InvalidAmountError,
    InvalidContributionTierError,
    InvalidCreditError,
    InvalidParameterDataError,
    InvalidRateError,
    NotFoundError,
    UnknownRegistrationError,
)
from app.domain.parameters.amount import AMOUNT, Amount
from app.domain.parameters.brackets import BRACKETS, Bracket, BracketSchedule
from app.domain.parameters.contribution_tier import CONTRIBUTION_TIER, ContributionTier
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundTo
from app.domain.registry import Namespace

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
"""

RATE_2025 = """\
family: ex/credit_rate
tax_year: 2025
kind: rate
sources:
  - https://example.org/credit-rate-2025
rounding: none
rate: "0.125"
"""

AMOUNT_2025 = """\
family: ex/amount_cap
tax_year: 2025
kind: amount
sources:
  - https://example.org/amount-cap-2025
rounding: none
amount: "1471"
"""

CONTRIBUTION_TIER_2025 = """\
family: ex/contribution_tier
tax_year: 2025
kind: contribution_tier
sources:
  - https://example.org/contribution-tier-2025
rounding: none
rate: "0.05"
lower: "3000"
upper: "50000"
maximum: "2350"
"""


def built_in_parsers() -> ParameterParserRegistry:
    """A fresh registry holding the built-in parsers, never the shared one."""
    registry = ParameterParserRegistry()
    registry.register_class(BracketsParser)
    registry.register_class(CreditParser)
    registry.register_class(RateParser)
    registry.register_class(AmountParser)
    registry.register_class(ContributionTierParser)
    return registry


EX = Namespace("ex")


def roots(directory: Path) -> Mapping[Namespace, Path]:
    """One made-up package, namespace `ex`, whose directory is `<directory>/ex`."""
    return {EX: directory / "ex"}


def source(directory: Path) -> YamlParameterSource:
    return YamlParameterSource(roots(directory), parsers=built_in_parsers())


def write(directory: Path, relative: str, content: str) -> None:
    path = directory / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content), encoding="utf-8")


# --- reading each built-in kind ---------------------------------------------------


def test_reads_a_bracket_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/brackets/2025.yaml", BRACKETS_2025)

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
    write(tmp_path, "ex/parameters/personal_credit/2025.yaml", CREDIT_2025)

    result = source(tmp_path).get("ex/personal_credit", 2025, CREDIT)

    assert result == ParameterDataset(
        family="ex/personal_credit",
        tax_year=2025,
        kind=CREDIT,
        values=Credit(amount=D("1000")),
        rounding=NO_ROUNDING,
        sources=("https://example.org/credits-2025",),
    )


def test_reads_a_rate_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/credit_rate/2025.yaml", RATE_2025)

    result = source(tmp_path).get("ex/credit_rate", 2025, RATE)

    assert result == ParameterDataset(
        family="ex/credit_rate",
        tax_year=2025,
        kind=RATE,
        values=Rate(D("0.125")),
        rounding=NO_ROUNDING,
        sources=("https://example.org/credit-rate-2025",),
    )


@pytest.mark.parametrize("rate", ["0", "1", "0.0505"])
def test_reads_rates_from_zero_to_one_inclusive(tmp_path: Path, rate: str) -> None:
    write(
        tmp_path,
        "ex/parameters/credit_rate/2025.yaml",
        RATE_2025.replace('rate: "0.125"', f'rate: "{rate}"'),
    )

    assert source(tmp_path).get("ex/credit_rate", 2025, RATE).values == Rate(D(rate))


def test_reads_an_amount_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/amount_cap/2025.yaml", AMOUNT_2025)

    result = source(tmp_path).get("ex/amount_cap", 2025, AMOUNT)

    assert result == ParameterDataset(
        family="ex/amount_cap",
        tax_year=2025,
        kind=AMOUNT,
        values=Amount(D("1471")),
        rounding=NO_ROUNDING,
        sources=("https://example.org/amount-cap-2025",),
    )


@pytest.mark.parametrize("amount", ["0", "1471", "1234.56", "1000.50"])
def test_reads_amounts_exactly(tmp_path: Path, amount: str) -> None:
    write(
        tmp_path,
        "ex/parameters/amount_cap/2025.yaml",
        AMOUNT_2025.replace('amount: "1471"', f'amount: "{amount}"'),
    )

    value = source(tmp_path).get("ex/amount_cap", 2025, AMOUNT).values.value

    assert str(value) == amount  # exact, scale kept


def test_reads_an_amount_dataset_rounding_rule(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/amount_cap/2025.yaml",
        AMOUNT_2025.replace("rounding: none", 'rounding: {increment: "1", mode: down}'),
    )

    result = source(tmp_path).get("ex/amount_cap", 2025, AMOUNT)

    assert result.rounding == RoundTo(D("1"), RoundingMode.DOWN)


def test_by_default_the_amount_parser_comes_from_the_shared_registry(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/amount_cap/2025.yaml", AMOUNT_2025)

    result = YamlParameterSource(roots(tmp_path)).get("ex/amount_cap", 2025, AMOUNT)

    assert result.values == Amount(D("1471"))


def test_reads_a_contribution_tier_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/contribution_tier/2025.yaml", CONTRIBUTION_TIER_2025)

    result = source(tmp_path).get("ex/contribution_tier", 2025, CONTRIBUTION_TIER)

    assert result == ParameterDataset(
        family="ex/contribution_tier",
        tax_year=2025,
        kind=CONTRIBUTION_TIER,
        values=ContributionTier(
            rate=Rate(D("0.05")), lower=D("3000"), upper=D("50000"), maximum=D("2350")
        ),
        rounding=NO_ROUNDING,
        sources=("https://example.org/contribution-tier-2025",),
    )


def test_reads_a_contribution_tiers_figures_exactly(tmp_path: Path) -> None:
    content = (
        CONTRIBUTION_TIER_2025.replace('rate: "0.05"', 'rate: "0.0495"')
        .replace('lower: "3000"', 'lower: "3000.50"')
        .replace('upper: "50000"', 'upper: "50000.00"')
        .replace('maximum: "2350"', 'maximum: "2350.10"')
    )
    write(tmp_path, "ex/parameters/contribution_tier/2025.yaml", content)

    tier = source(tmp_path).get("ex/contribution_tier", 2025, CONTRIBUTION_TIER).values

    assert (str(tier.rate.value), str(tier.lower), str(tier.upper), str(tier.maximum)) == (
        "0.0495",
        "3000.50",
        "50000.00",
        "2350.10",
    )


def test_reads_a_contribution_tier_starting_at_zero_with_a_zero_maximum(tmp_path: Path) -> None:
    content = CONTRIBUTION_TIER_2025.replace('lower: "3000"', 'lower: "0"').replace(
        'maximum: "2350"', 'maximum: "0"'
    )
    write(tmp_path, "ex/parameters/contribution_tier/2025.yaml", content)

    tier = source(tmp_path).get("ex/contribution_tier", 2025, CONTRIBUTION_TIER).values

    assert (tier.lower, tier.maximum) == (D("0"), D("0"))


def test_reads_a_contribution_tier_datasets_rounding_rule(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/contribution_tier/2025.yaml",
        CONTRIBUTION_TIER_2025.replace(
            "rounding: none", 'rounding: {increment: "0.01", mode: half_up}'
        ),
    )

    result = source(tmp_path).get("ex/contribution_tier", 2025, CONTRIBUTION_TIER)

    assert result.rounding == RoundTo(D("0.01"), RoundingMode.HALF_UP)


def test_by_default_the_contribution_tier_parser_comes_from_the_shared_registry(
    tmp_path: Path,
) -> None:
    write(tmp_path, "ex/parameters/contribution_tier/2025.yaml", CONTRIBUTION_TIER_2025)

    result = YamlParameterSource(roots(tmp_path)).get(
        "ex/contribution_tier", 2025, CONTRIBUTION_TIER
    )

    assert result.values == ContributionTier(Rate(D("0.05")), D("3000"), D("50000"), D("2350"))


def test_reads_a_rounding_rule(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/brackets/2025.yaml",
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
        "ex/parameters/flat/2025.yaml",
        "family: ex/flat\ntax_year: 2025\nkind: flat_rate\n"
        'sources: [https://example.org]\nrounding: none\nrate: "0.2"\n',
    )
    parsers = built_in_parsers()
    parsers.register_class(FlatRateParser)

    values: Decimal = (
        YamlParameterSource(roots(tmp_path), parsers=parsers).get("ex/flat", 2025, FLAT_RATE).values
    )

    assert values == D("0.2")


def test_requesting_a_kind_without_a_parser_fails(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/brackets/2025.yaml", BRACKETS_2025)

    with pytest.raises(UnknownRegistrationError, match="'flat_rate'"):
        source(tmp_path).get("ex/brackets", 2025, FLAT_RATE)


def test_parsers_are_read_from_the_injected_registry(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/brackets/2025.yaml", BRACKETS_2025)
    parsers = ParameterParserRegistry()
    parsers.register_class(CreditParser)

    with pytest.raises(UnknownRegistrationError, match="'brackets'"):
        YamlParameterSource(roots(tmp_path), parsers=parsers).get("ex/brackets", 2025, BRACKETS)


def test_by_default_parsers_come_from_the_shared_registry(tmp_path: Path) -> None:
    # The built-in parsers registered themselves in the shared registry when imported.
    write(tmp_path, "ex/parameters/brackets/2025.yaml", BRACKETS_2025)

    result = YamlParameterSource(roots(tmp_path)).get("ex/brackets", 2025, BRACKETS)

    assert result.values == BracketSchedule(
        (Bracket(D("0"), D("0.10")), Bracket(D("100"), D("0.20")))
    )


# --- resolution -----------------------------------------------------------------------


def test_absent_year_is_not_found_and_never_carried_forward(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/brackets/2025.yaml", BRACKETS_2025)

    with pytest.raises(NotFoundError, match="ex/brackets.*2026"):
        source(tmp_path).get("ex/brackets", 2026, BRACKETS)


def test_absent_family_is_not_found(tmp_path: Path) -> None:
    with pytest.raises(NotFoundError, match="ex/other"):
        source(tmp_path).get("ex/other", 2025, BRACKETS)


def test_each_namespace_resolves_under_its_own_directory(tmp_path: Path) -> None:
    # Directory names need not match namespaces: the mapping decides.
    write(tmp_path, "pkg_one/parameters/brackets/2025.yaml", BRACKETS_2025)
    write(
        tmp_path,
        "pkg_two/parameters/brackets/2025.yaml",
        BRACKETS_2025.replace("family: ex/brackets", "family: ex-two/brackets").replace(
            '"0.10"', '"0.15"'
        ),
    )
    two_roots = {EX: tmp_path / "pkg_one", Namespace("ex-two"): tmp_path / "pkg_two"}
    parameters = YamlParameterSource(two_roots, parsers=built_in_parsers())

    one = parameters.get("ex/brackets", 2025, BRACKETS)
    two = parameters.get("ex-two/brackets", 2025, BRACKETS)

    assert one.values.brackets[0].rate == D("0.10")
    assert two.values.brackets[0].rate == D("0.15")


def test_family_may_nest_below_the_namespace(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/credits/personal/2025.yaml",
        CREDIT_2025.replace("family: ex/personal_credit", "family: ex/credits/personal"),
    )

    result = source(tmp_path).get("ex/credits/personal", 2025, CREDIT)

    assert result.family == "ex/credits/personal"


def test_files_outside_parameters_are_not_read(tmp_path: Path) -> None:
    write(tmp_path, "ex/brackets/2025.yaml", BRACKETS_2025)

    with pytest.raises(NotFoundError, match="ex/brackets"):
        source(tmp_path).get("ex/brackets", 2025, BRACKETS)


def test_unknown_namespace_is_not_found_and_named(tmp_path: Path) -> None:
    with pytest.raises(NotFoundError, match="namespace 'zz'"):
        source(tmp_path).get("zz/brackets", 2025, BRACKETS)


@pytest.mark.parametrize(
    "family", ["", "EX/brackets", "../brackets", "ex/../x", "/ex/b", "ex/", "ex_on/brackets"]
)
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
    write(tmp_path, "ex/parameters/brackets/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        source(tmp_path).get("ex/brackets", 2025, BRACKETS)

    assert "2025.yaml" in str(excinfo.value)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param(
            CREDIT_2025.replace('amount: "1000"', 'amount: "-1"'),
            "amount must not be negative",
            id="amount-negative",
        ),
        pytest.param(
            CREDIT_2025 + 'rate: "0.125"\n',
            r"unknown keys \['rate'\]",
            id="rate-is-not-a-credit-key",
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
    write(tmp_path, "ex/parameters/personal_credit/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        source(tmp_path).get("ex/personal_credit", 2025, CREDIT)

    assert "2025.yaml" in str(excinfo.value)


def test_an_invalid_credit_amount_is_reported_as_a_credit_error(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/personal_credit/2025.yaml",
        CREDIT_2025.replace('amount: "1000"', 'amount: "-1"'),
    )

    with pytest.raises(InvalidParameterDataError) as excinfo:
        source(tmp_path).get("ex/personal_credit", 2025, CREDIT)

    assert isinstance(excinfo.value.__cause__, InvalidCreditError)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param(
            RATE_2025.replace('rate: "0.125"', 'rate: "1.5"'),
            "rate must be between 0 and 1",
            id="rate-above-one",
        ),
        pytest.param(
            RATE_2025.replace('rate: "0.125"', 'rate: "-0.1"'),
            "rate must be between 0 and 1",
            id="rate-negative",
        ),
        pytest.param(
            RATE_2025.replace('rate: "0.125"', "rate: 0.125"),
            "rate must be a string, got float",
            id="rate-as-yaml-number",
        ),
        pytest.param(
            RATE_2025.replace('rate: "0.125"', 'rate: "Infinity"'),
            "rate is not a decimal",
            id="rate-infinite",
        ),
        pytest.param(
            RATE_2025.replace('rate: "0.125"\n', ""),
            r"missing keys \['rate'\]",
            id="rate-missing",
        ),
        pytest.param(
            RATE_2025 + 'amount: "1000"\n',
            r"unknown keys \['amount'\]",
            id="amount-is-not-a-rate-key",
        ),
        pytest.param(
            RATE_2025.replace("kind: rate", "kind: credit"),
            "kind 'credit' does not match the requested 'rate'",
            id="kind-mismatch",
        ),
    ],
)
def test_rejects_malformed_rate_dataset(tmp_path: Path, content: str, message: str) -> None:
    write(tmp_path, "ex/parameters/credit_rate/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        source(tmp_path).get("ex/credit_rate", 2025, RATE)

    assert "2025.yaml" in str(excinfo.value)


def test_a_rate_out_of_range_is_reported_as_a_rate_error(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/credit_rate/2025.yaml",
        RATE_2025.replace('rate: "0.125"', 'rate: "1.5"'),
    )

    with pytest.raises(InvalidParameterDataError) as excinfo:
        source(tmp_path).get("ex/credit_rate", 2025, RATE)

    assert isinstance(excinfo.value.__cause__, InvalidRateError)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param(
            AMOUNT_2025.replace('amount: "1471"', 'amount: "-1"'),
            "amount must not be negative",
            id="amount-negative",
        ),
        pytest.param(
            AMOUNT_2025.replace('amount: "1471"', 'amount: "-0.01"'),
            "amount must not be negative",
            id="amount-slightly-negative",
        ),
        pytest.param(
            AMOUNT_2025.replace('amount: "1471"', 'amount: "Infinity"'),
            "amount is not a decimal",
            id="amount-infinite",
        ),
        pytest.param(
            AMOUNT_2025.replace('amount: "1471"', 'amount: "NaN"'),
            "amount is not a decimal",
            id="amount-nan",
        ),
        pytest.param(
            AMOUNT_2025.replace('amount: "1471"', 'amount: "lots"'),
            "amount is not a decimal: 'lots'",
            id="amount-not-decimal",
        ),
        pytest.param(
            AMOUNT_2025.replace('amount: "1471"', "amount: 1471"),
            "amount must be a string, got int",
            id="amount-as-yaml-number",
        ),
        pytest.param(
            AMOUNT_2025.replace('amount: "1471"', "amount: 1471.5"),
            "amount must be a string, got float",
            id="amount-as-yaml-float",
        ),
        pytest.param(
            AMOUNT_2025.replace('amount: "1471"\n', ""),
            r"missing keys \['amount'\]",
            id="amount-missing",
        ),
        pytest.param(
            AMOUNT_2025 + 'rate: "0.125"\n',
            r"unknown keys \['rate'\]",
            id="rate-is-not-an-amount-key",
        ),
        pytest.param(
            AMOUNT_2025.replace("kind: amount", "kind: credit"),
            "kind 'credit' does not match the requested 'amount'",
            id="kind-mismatch",
        ),
        pytest.param(
            AMOUNT_2025.replace("kind: amount\n", ""),
            "missing key 'kind'",
            id="kind-missing",
        ),
        pytest.param(
            AMOUNT_2025.replace("rounding: none\n", ""),
            r"missing keys \['rounding'\]",
            id="rounding-missing",
        ),
        pytest.param(
            AMOUNT_2025.replace("sources:\n  - https://example.org/amount-cap-2025", "sources: []"),
            "sources must list at least one",
            id="sources-empty",
        ),
    ],
)
def test_rejects_malformed_amount_dataset(tmp_path: Path, content: str, message: str) -> None:
    write(tmp_path, "ex/parameters/amount_cap/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        source(tmp_path).get("ex/amount_cap", 2025, AMOUNT)

    assert "2025.yaml" in str(excinfo.value)


def test_a_negative_amount_is_reported_as_an_amount_error(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/amount_cap/2025.yaml",
        AMOUNT_2025.replace('amount: "1471"', 'amount: "-1"'),
    )

    with pytest.raises(InvalidParameterDataError) as excinfo:
        source(tmp_path).get("ex/amount_cap", 2025, AMOUNT)

    assert isinstance(excinfo.value.__cause__, InvalidAmountError)


def test_an_amount_dataset_is_not_a_credit_dataset(tmp_path: Path) -> None:
    # Both kinds read an `amount` key; the declared kind alone tells them apart.
    write(tmp_path, "ex/parameters/amount_cap/2025.yaml", AMOUNT_2025)

    with pytest.raises(InvalidParameterDataError, match="kind 'amount' does not match"):
        source(tmp_path).get("ex/amount_cap", 2025, CREDIT)


def test_a_credit_dataset_is_not_an_amount_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/personal_credit/2025.yaml", CREDIT_2025)

    with pytest.raises(InvalidParameterDataError, match="kind 'credit' does not match"):
        source(tmp_path).get("ex/personal_credit", 2025, AMOUNT)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('rate: "0.05"', 'rate: "1.5"'),
            "rate must be between 0 and 1",
            id="rate-above-one",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('rate: "0.05"', 'rate: "-0.05"'),
            "rate must be between 0 and 1",
            id="rate-negative",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('rate: "0.05"', "rate: 0.05"),
            "rate must be a string, got float",
            id="rate-as-yaml-number",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('lower: "3000"', "lower: 3000"),
            "lower must be a string, got int",
            id="lower-as-yaml-number",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('upper: "50000"', "upper: 50000.5"),
            "upper must be a string, got float",
            id="upper-as-yaml-float",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('maximum: "2350"', "maximum: 2350"),
            "maximum must be a string, got int",
            id="maximum-as-yaml-number",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('lower: "3000"', 'lower: "lots"'),
            "lower is not a decimal: 'lots'",
            id="lower-not-decimal",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('upper: "50000"', 'upper: "Infinity"'),
            "upper is not a decimal",
            id="upper-infinite",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('maximum: "2350"', 'maximum: "NaN"'),
            "maximum is not a decimal",
            id="maximum-nan",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('lower: "3000"', 'lower: "-1"'),
            "lower must not be negative",
            id="lower-negative",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('lower: "3000"', 'lower: "50000"'),
            "lower must be below upper",
            id="lower-at-upper",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('upper: "50000"', 'upper: "2999.99"'),
            "lower must be below upper",
            id="upper-below-lower",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('maximum: "2350"', 'maximum: "-0.01"'),
            "maximum must not be negative",
            id="maximum-negative",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('upper: "50000"\n', ""),
            r"missing keys \['upper'\]",
            id="upper-missing",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace('rate: "0.05"\n', "").replace('maximum: "2350"\n', ""),
            r"missing keys \['maximum', 'rate'\]",
            id="rate-and-maximum-missing",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025 + 'amount: "1000"\n',
            r"unknown keys \['amount'\]",
            id="amount-is-not-a-tier-key",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace("kind: contribution_tier", "kind: rate"),
            "kind 'rate' does not match the requested 'contribution_tier'",
            id="kind-mismatch",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace("rounding: none\n", ""),
            r"missing keys \['rounding'\]",
            id="rounding-missing",
        ),
        pytest.param(
            CONTRIBUTION_TIER_2025.replace(
                "sources:\n  - https://example.org/contribution-tier-2025", "sources: []"
            ),
            "sources must list at least one",
            id="sources-empty",
        ),
    ],
)
def test_rejects_malformed_contribution_tier_dataset(
    tmp_path: Path, content: str, message: str
) -> None:
    write(tmp_path, "ex/parameters/contribution_tier/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        source(tmp_path).get("ex/contribution_tier", 2025, CONTRIBUTION_TIER)

    assert "2025.yaml" in str(excinfo.value)


def test_an_invalid_tier_rate_is_reported_as_a_rate_error(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/contribution_tier/2025.yaml",
        CONTRIBUTION_TIER_2025.replace('rate: "0.05"', 'rate: "1.5"'),
    )

    with pytest.raises(InvalidParameterDataError) as excinfo:
        source(tmp_path).get("ex/contribution_tier", 2025, CONTRIBUTION_TIER)

    assert isinstance(excinfo.value.__cause__, InvalidRateError)


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ('lower: "3000"', 'lower: "-1"'),
        ('lower: "3000"', 'lower: "60000"'),
        ('maximum: "2350"', 'maximum: "-1"'),
    ],
)
def test_an_invalid_tier_is_reported_as_a_contribution_tier_error(
    tmp_path: Path, old: str, new: str
) -> None:
    write(
        tmp_path,
        "ex/parameters/contribution_tier/2025.yaml",
        CONTRIBUTION_TIER_2025.replace(old, new),
    )

    with pytest.raises(InvalidParameterDataError) as excinfo:
        source(tmp_path).get("ex/contribution_tier", 2025, CONTRIBUTION_TIER)

    assert isinstance(excinfo.value.__cause__, InvalidContributionTierError)


def test_a_rate_dataset_is_not_a_contribution_tier_dataset(tmp_path: Path) -> None:
    # Both kinds read a `rate` key; the declared kind alone tells them apart.
    write(tmp_path, "ex/parameters/credit_rate/2025.yaml", RATE_2025)

    with pytest.raises(InvalidParameterDataError, match="kind 'rate' does not match"):
        source(tmp_path).get("ex/credit_rate", 2025, CONTRIBUTION_TIER)


def test_a_contribution_tier_dataset_is_not_a_rate_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/contribution_tier/2025.yaml", CONTRIBUTION_TIER_2025)

    with pytest.raises(InvalidParameterDataError, match="kind 'contribution_tier' does not match"):
        source(tmp_path).get("ex/contribution_tier", 2025, RATE)
