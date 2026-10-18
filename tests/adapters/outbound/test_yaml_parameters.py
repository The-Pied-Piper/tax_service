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
from app.adapters.outbound.parameter_parsers.factor import FactorParser
from app.adapters.outbound.parameter_parsers.fraction import FractionParser
from app.adapters.outbound.parameter_parsers.rate import RateParser
from app.adapters.outbound.parameter_parsers.registry import ParameterParserRegistry
from app.adapters.outbound.parameter_parsers.surcharge_tiers import SurchargeTiersParser
from app.adapters.outbound.parameter_parsers.taper import TaperParser
from app.adapters.outbound.yaml_parameters import YamlParameterSource
from app.adapters.outbound.yaml_support import YamlNode
from app.domain.errors import (
    DomainError,
    InvalidAmountError,
    InvalidBracketScheduleError,
    InvalidContributionTierError,
    InvalidCreditError,
    InvalidFactorError,
    InvalidFractionError,
    InvalidParameterDataError,
    InvalidRateError,
    InvalidSurchargeTiersError,
    InvalidTaperError,
    NotFoundError,
    UnknownRegistrationError,
)
from app.domain.parameters.amount import AMOUNT, Amount
from app.domain.parameters.brackets import BRACKETS, Bracket, BracketSchedule
from app.domain.parameters.contribution_tier import CONTRIBUTION_TIER, ContributionTier
from app.domain.parameters.credit import CREDIT, Credit
from app.domain.parameters.datasets import ParameterDataset
from app.domain.parameters.factor import FACTOR, Factor
from app.domain.parameters.fraction import FRACTION, Fraction
from app.domain.parameters.kind import ParameterKind
from app.domain.parameters.rate import RATE, Rate
from app.domain.parameters.rounding import NO_ROUNDING, RoundingMode, RoundTo
from app.domain.parameters.surcharge_tiers import (
    SURCHARGE_TIERS,
    SurchargeTier,
    SurchargeTiers,
)
from app.domain.parameters.taper import TAPER, Taper
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
  - {from: "0", rate: "0.10", tax_at_start: "0.00"}
  - {from: "100", rate: "0.20", tax_at_start: "10.00"}
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

SURCHARGE_TIERS_2025 = """\
family: ex/surcharge_tiers
tax_year: 2025
kind: surcharge_tiers
sources:
  - https://example.org/surcharge-2025
rounding: none
tiers:
  - {threshold: "100", rate: "0.10"}
  - {threshold: "300.50", rate: "0.25"}
"""

CAPPED_SURCHARGE_TIERS_2025 = """\
family: ex/surcharge_tiers
tax_year: 2025
kind: surcharge_tiers
sources:
  - https://example.org/surcharge-2025
rounding: none
tiers:
  - {threshold: "100", rate: "0.10"}
  - {threshold: "300.50", rate: "0.25", maximum: "150.50"}
"""

TAPER_2025 = """\
family: ex/taper
tax_year: 2025
kind: taper
sources:
  - https://example.org/taper-2025
rounding: none
base: "1000"
supplement: "500"
threshold: "20000"
range: "10000"
"""

FACTOR_2025 = """\
family: ex/factor
tax_year: 2025
kind: factor
sources:
  - https://example.org/factor-2025
rounding: none
value: "2"
"""

FRACTION_2025 = """\
family: ex/fraction
tax_year: 2025
kind: fraction
sources:
  - https://example.org/fraction-2025
rounding: none
numerator: "2"
denominator: "3"
"""


def built_in_parsers() -> ParameterParserRegistry:
    """A fresh registry holding the built-in parsers, never the shared one."""
    registry = ParameterParserRegistry()
    registry.register_class(BracketsParser)
    registry.register_class(CreditParser)
    registry.register_class(RateParser)
    registry.register_class(AmountParser)
    registry.register_class(ContributionTierParser)
    registry.register_class(SurchargeTiersParser)
    registry.register_class(TaperParser)
    registry.register_class(FactorParser)
    registry.register_class(FractionParser)
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
        values=BracketSchedule(
            (Bracket(D("0"), D("0.10"), D("0.00")), Bracket(D("100"), D("0.20"), D("10.00")))
        ),
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


def test_reads_a_surcharge_tiers_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/surcharge_tiers/2025.yaml", SURCHARGE_TIERS_2025)

    result = source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS)

    assert result == ParameterDataset(
        family="ex/surcharge_tiers",
        tax_year=2025,
        kind=SURCHARGE_TIERS,
        values=SurchargeTiers(
            (
                SurchargeTier(D("100"), Rate(D("0.10"))),
                SurchargeTier(D("300.50"), Rate(D("0.25"))),
            )
        ),
        rounding=NO_ROUNDING,
        sources=("https://example.org/surcharge-2025",),
    )


def test_reads_surcharge_tiers_exactly(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/surcharge_tiers/2025.yaml", SURCHARGE_TIERS_2025)

    tiers = source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS).values.tiers

    assert [str(tier.threshold) for tier in tiers] == ["100", "300.50"]  # exact, scale kept
    assert [str(tier.rate.value) for tier in tiers] == ["0.10", "0.25"]


def test_reads_a_single_surcharge_tier(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/surcharge_tiers/2025.yaml",
        SURCHARGE_TIERS_2025.replace('  - {threshold: "300.50", rate: "0.25"}\n', ""),
    )

    result = source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS)

    assert result.values == SurchargeTiers((SurchargeTier(D("100"), Rate(D("0.10"))),))


def test_reads_a_surcharge_tiers_rounding_rule(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/surcharge_tiers/2025.yaml",
        SURCHARGE_TIERS_2025.replace(
            "rounding: none", 'rounding: {increment: "0.01", mode: half_up}'
        ),
    )

    result = source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS)

    assert result.rounding == RoundTo(D("0.01"), RoundingMode.HALF_UP)


def test_by_default_the_surcharge_tiers_parser_comes_from_the_shared_registry(
    tmp_path: Path,
) -> None:
    write(tmp_path, "ex/parameters/surcharge_tiers/2025.yaml", SURCHARGE_TIERS_2025)

    result = YamlParameterSource(roots(tmp_path)).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS)

    assert result.values.tiers[0] == SurchargeTier(D("100"), Rate(D("0.10")))


def test_reads_a_taper_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/taper/2025.yaml", TAPER_2025)

    result = source(tmp_path).get("ex/taper", 2025, TAPER)

    assert result == ParameterDataset(
        family="ex/taper",
        tax_year=2025,
        kind=TAPER,
        values=Taper(base=D("1000"), supplement=D("500"), threshold=D("20000"), range=D("10000")),
        rounding=NO_ROUNDING,
        sources=("https://example.org/taper-2025",),
    )


def test_reads_a_tapers_figures_exactly(tmp_path: Path) -> None:
    content = (
        TAPER_2025.replace('base: "1000"', 'base: "1000.50"')
        .replace('supplement: "500"', 'supplement: "500.00"')
        .replace('threshold: "20000"', 'threshold: "20000.10"')
        .replace('range: "10000"', 'range: "10000.0"')
    )
    write(tmp_path, "ex/parameters/taper/2025.yaml", content)

    taper = source(tmp_path).get("ex/taper", 2025, TAPER).values

    assert (str(taper.base), str(taper.supplement), str(taper.threshold), str(taper.range)) == (
        "1000.50",
        "500.00",
        "20000.10",
        "10000.0",
    )


def test_reads_a_taper_with_a_zero_base_supplement_and_threshold(tmp_path: Path) -> None:
    content = (
        TAPER_2025.replace('base: "1000"', 'base: "0"')
        .replace('supplement: "500"', 'supplement: "0"')
        .replace('threshold: "20000"', 'threshold: "0"')
    )
    write(tmp_path, "ex/parameters/taper/2025.yaml", content)

    taper = source(tmp_path).get("ex/taper", 2025, TAPER).values

    assert (taper.base, taper.supplement, taper.threshold) == (D("0"), D("0"), D("0"))


def test_reads_a_taper_datasets_rounding_rule(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/taper/2025.yaml",
        TAPER_2025.replace("rounding: none", 'rounding: {increment: "0.01", mode: half_up}'),
    )

    result = source(tmp_path).get("ex/taper", 2025, TAPER)

    assert result.rounding == RoundTo(D("0.01"), RoundingMode.HALF_UP)


def test_by_default_the_taper_parser_comes_from_the_shared_registry(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/taper/2025.yaml", TAPER_2025)

    result = YamlParameterSource(roots(tmp_path)).get("ex/taper", 2025, TAPER)

    assert result.values == Taper(D("1000"), D("500"), D("20000"), D("10000"))


def test_reads_a_factor_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/factor/2025.yaml", FACTOR_2025)

    result = source(tmp_path).get("ex/factor", 2025, FACTOR)

    assert result == ParameterDataset(
        family="ex/factor",
        tax_year=2025,
        kind=FACTOR,
        values=Factor(D("2")),
        rounding=NO_ROUNDING,
        sources=("https://example.org/factor-2025",),
    )


@pytest.mark.parametrize("value", ["0", "1", "2", "2.50", "1000000"])
def test_reads_factors_exactly(tmp_path: Path, value: str) -> None:
    write(
        tmp_path,
        "ex/parameters/factor/2025.yaml",
        FACTOR_2025.replace('value: "2"', f'value: "{value}"'),
    )

    factor = source(tmp_path).get("ex/factor", 2025, FACTOR).values.value

    assert str(factor) == value  # exact, scale kept, no upper bound


def test_reads_a_factor_datasets_rounding_rule(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/factor/2025.yaml",
        FACTOR_2025.replace("rounding: none", 'rounding: {increment: "0.01", mode: half_up}'),
    )

    result = source(tmp_path).get("ex/factor", 2025, FACTOR)

    assert result.rounding == RoundTo(D("0.01"), RoundingMode.HALF_UP)


def test_by_default_the_factor_parser_comes_from_the_shared_registry(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/factor/2025.yaml", FACTOR_2025)

    result = YamlParameterSource(roots(tmp_path)).get("ex/factor", 2025, FACTOR)

    assert result.values == Factor(D("2"))


def test_reads_a_fraction_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/fraction/2025.yaml", FRACTION_2025)

    result = source(tmp_path).get("ex/fraction", 2025, FRACTION)

    assert result == ParameterDataset(
        family="ex/fraction",
        tax_year=2025,
        kind=FRACTION,
        values=Fraction(numerator=2, denominator=3),
        rounding=NO_ROUNDING,
        sources=("https://example.org/fraction-2025",),
    )


@pytest.mark.parametrize(
    ("numerator", "denominator"), [("1", "1"), ("2", "3"), ("3", "2"), ("4", "6"), ("7", "1000000")]
)
def test_reads_a_fractions_parts_as_whole_numbers(
    tmp_path: Path, numerator: str, denominator: str
) -> None:
    content = FRACTION_2025.replace('numerator: "2"', f'numerator: "{numerator}"').replace(
        'denominator: "3"', f'denominator: "{denominator}"'
    )
    write(tmp_path, "ex/parameters/fraction/2025.yaml", content)

    fraction = source(tmp_path).get("ex/fraction", 2025, FRACTION).values

    assert (fraction.numerator, fraction.denominator) == (int(numerator), int(denominator))
    assert type(fraction.numerator) is int
    assert type(fraction.denominator) is int


def test_reads_a_fraction_datasets_rounding_rule(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/fraction/2025.yaml",
        FRACTION_2025.replace("rounding: none", 'rounding: {increment: "0.01", mode: half_up}'),
    )

    result = source(tmp_path).get("ex/fraction", 2025, FRACTION)

    assert result.rounding == RoundTo(D("0.01"), RoundingMode.HALF_UP)


def test_by_default_the_fraction_parser_comes_from_the_shared_registry(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/fraction/2025.yaml", FRACTION_2025)

    result = YamlParameterSource(roots(tmp_path)).get("ex/fraction", 2025, FRACTION)

    assert result.values == Fraction(2, 3)


def test_reads_each_brackets_printed_constant_exactly(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/brackets/2025.yaml", BRACKETS_2025)

    schedule = source(tmp_path).get("ex/brackets", 2025, BRACKETS).values

    assert [str(b.tax_at_start) for b in schedule.brackets] == ["0.00", "10.00"]


def test_reads_a_constant_the_form_rounds_to_the_cent(tmp_path: Path) -> None:
    # 10.5% of 105 is 11.025; the form prints 11.03.
    content = (
        BRACKETS_2025.replace('rate: "0.10"', 'rate: "0.105"')
        .replace('from: "100"', 'from: "105"')
        .replace('tax_at_start: "10.00"', 'tax_at_start: "11.03"')
    )
    write(tmp_path, "ex/parameters/brackets/2025.yaml", content)

    schedule = source(tmp_path).get("ex/brackets", 2025, BRACKETS).values

    assert schedule.brackets[1] == Bracket(D("105"), D("0.20"), D("11.03"))


@pytest.mark.parametrize("constant", ["11.025", "11.02", "11.04"])
def test_refuses_a_constant_that_is_not_the_rounded_tax_below_naming_the_bracket(
    tmp_path: Path, constant: str
) -> None:
    content = (
        BRACKETS_2025.replace('rate: "0.10"', 'rate: "0.105"')
        .replace('from: "100"', 'from: "105"')
        .replace('tax_at_start: "10.00"', f'tax_at_start: "{constant}"')
    )
    write(tmp_path, "ex/parameters/brackets/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match="from 105") as excinfo:
        source(tmp_path).get("ex/brackets", 2025, BRACKETS)

    assert isinstance(excinfo.value.__cause__, InvalidBracketScheduleError)
    assert "2025.yaml" in str(excinfo.value)
    assert constant in str(excinfo.value)
    assert "11.03" in str(excinfo.value)


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
        (Bracket(D("0"), D("0.10"), D("0.00")), Bracket(D("100"), D("0.20"), D("10.00")))
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
        BRACKETS_2025.replace("family: ex/brackets", "family: ex-two/brackets")
        .replace('"0.10"', '"0.15"')
        .replace('"10.00"', '"15.00"'),
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
            BRACKETS_2025.replace(', tax_at_start: "10.00"}', "}"),
            r"brackets\[1\]: missing keys \['tax_at_start'\]",
            id="constant-missing",
        ),
        pytest.param(
            BRACKETS_2025.replace(', tax_at_start: "0.00"}', "}"),
            r"brackets\[0\]: missing keys \['tax_at_start'\]",
            id="first-constant-missing",
        ),
        pytest.param(
            BRACKETS_2025.replace('tax_at_start: "10.00"', "tax_at_start: 10.00"),
            r"brackets\[1\].tax_at_start must be a string, got float",
            id="constant-as-yaml-number",
        ),
        pytest.param(
            BRACKETS_2025.replace('tax_at_start: "10.00"', 'tax_at_start: "ten"'),
            r"brackets\[1\].tax_at_start is not a decimal: 'ten'",
            id="constant-not-decimal",
        ),
        pytest.param(
            BRACKETS_2025.replace('tax_at_start: "10.00"', 'tax_at_start: "10.01"'),
            "from 100",
            id="constant-mistyped",
        ),
        pytest.param(
            BRACKETS_2025.replace('tax_at_start: "0.00"', 'tax_at_start: "1.00"'),
            "first bracket",
            id="first-constant-not-zero",
        ),
        pytest.param(
            BRACKETS_2025.replace('tax_at_start: "10.00"', 'tax_at_start: "-10.00"'),
            "tax_at_start must not be negative",
            id="constant-negative",
        ),
        pytest.param(
            BRACKETS_2025.replace('tax_at_start: "10.00"}', 'tax_at_start: "10.00", to: "300"}'),
            r"brackets\[1\]: unknown keys \['to'\]",
            id="no-upper-bound-key",
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


def test_reads_a_surcharge_tiers_maximum(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/surcharge_tiers/2025.yaml", CAPPED_SURCHARGE_TIERS_2025)

    result = source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS)

    assert result.values == SurchargeTiers(
        (
            SurchargeTier(D("100"), Rate(D("0.10"))),
            SurchargeTier(D("300.50"), Rate(D("0.25")), D("150.50")),
        )
    )


def test_reads_a_surcharge_tiers_maximum_exactly(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/surcharge_tiers/2025.yaml", CAPPED_SURCHARGE_TIERS_2025)

    tiers = source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS).values.tiers

    assert str(tiers[1].maximum) == "150.50"  # exact, scale kept


def test_a_surcharge_tier_without_a_maximum_reads_as_none(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/surcharge_tiers/2025.yaml", CAPPED_SURCHARGE_TIERS_2025)

    tiers = source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS).values.tiers

    assert tiers[0].maximum is None


def test_reads_a_maximum_on_every_surcharge_tier(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/surcharge_tiers/2025.yaml",
        SURCHARGE_TIERS_2025.replace('rate: "0.10"}', 'rate: "0.10", maximum: "20"}').replace(
            'rate: "0.25"}', 'rate: "0.25", maximum: "15"}'
        ),
    )

    tiers = source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS).values.tiers

    assert [tier.maximum for tier in tiers] == [D("20"), D("15")]


def test_reads_a_zero_surcharge_tier_maximum(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/surcharge_tiers/2025.yaml",
        SURCHARGE_TIERS_2025.replace('rate: "0.10"}', 'rate: "0.10", maximum: "0"}'),
    )

    tiers = source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS).values.tiers

    assert tiers[0].maximum == D("0")


def test_reads_a_surcharge_tiers_maximum_written_as_a_block_mapping(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/surcharge_tiers/2025.yaml",
        SURCHARGE_TIERS_2025.replace(
            '  - {threshold: "300.50", rate: "0.25"}\n',
            '  - threshold: "300.50"\n    rate: "0.25"\n    maximum: "150"\n',
        ),
    )

    tiers = source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS).values.tiers

    assert tiers[1] == SurchargeTier(D("300.50"), Rate(D("0.25")), D("150"))


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param(
            CAPPED_SURCHARGE_TIERS_2025.replace('maximum: "150.50"', "maximum: 150"),
            r"tiers\[1\].maximum must be a string, got int",
            id="maximum-as-yaml-number",
        ),
        pytest.param(
            CAPPED_SURCHARGE_TIERS_2025.replace('maximum: "150.50"', "maximum: null"),
            r"tiers\[1\].maximum must be a string",
            id="maximum-null",
        ),
        pytest.param(
            CAPPED_SURCHARGE_TIERS_2025.replace('maximum: "150.50"', 'maximum: "lots"'),
            r"tiers\[1\].maximum is not a decimal: 'lots'",
            id="maximum-not-decimal",
        ),
        pytest.param(
            CAPPED_SURCHARGE_TIERS_2025.replace('maximum: "150.50"', 'maximum: "NaN"'),
            r"tiers\[1\].maximum is not a decimal",
            id="maximum-nan",
        ),
        pytest.param(
            CAPPED_SURCHARGE_TIERS_2025.replace('maximum: "150.50"', 'maximum: "Infinity"'),
            r"tiers\[1\].maximum is not a decimal",
            id="maximum-infinite",
        ),
        pytest.param(
            CAPPED_SURCHARGE_TIERS_2025.replace('maximum: "150.50"', 'maximum: "-0.01"'),
            r"tiers\[1\].*maximum must not be negative",
            id="maximum-negative",
        ),
        pytest.param(
            CAPPED_SURCHARGE_TIERS_2025.replace(
                'maximum: "150.50"}', 'maximum: "150.50", cap: "1"}'
            ),
            r"tiers\[1\]: unknown keys \['cap'\]",
            id="unknown-key-beside-maximum",
        ),
        pytest.param(
            CAPPED_SURCHARGE_TIERS_2025.replace('{threshold: "300.50", ', "{"),
            r"tiers\[1\]: missing keys \['threshold'\]",
            id="maximum-does-not-replace-the-threshold",
        ),
    ],
)
def test_rejects_a_malformed_surcharge_tier_maximum(
    tmp_path: Path, content: str, message: str
) -> None:
    write(tmp_path, "ex/parameters/surcharge_tiers/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS)

    assert "2025.yaml" in str(excinfo.value)


def test_a_negative_surcharge_tier_maximum_is_reported_as_a_surcharge_tiers_error(
    tmp_path: Path,
) -> None:
    write(
        tmp_path,
        "ex/parameters/surcharge_tiers/2025.yaml",
        CAPPED_SURCHARGE_TIERS_2025.replace('maximum: "150.50"', 'maximum: "-1"'),
    )

    with pytest.raises(InvalidParameterDataError) as excinfo:
        source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS)

    assert isinstance(excinfo.value.__cause__, InvalidSurchargeTiersError)


def test_a_rate_dataset_is_not_a_contribution_tier_dataset(tmp_path: Path) -> None:
    # Both kinds read a `rate` key; the declared kind alone tells them apart.
    write(tmp_path, "ex/parameters/credit_rate/2025.yaml", RATE_2025)

    with pytest.raises(InvalidParameterDataError, match="kind 'rate' does not match"):
        source(tmp_path).get("ex/credit_rate", 2025, CONTRIBUTION_TIER)


def test_a_contribution_tier_dataset_is_not_a_rate_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/contribution_tier/2025.yaml", CONTRIBUTION_TIER_2025)

    with pytest.raises(InvalidParameterDataError, match="kind 'contribution_tier' does not match"):
        source(tmp_path).get("ex/contribution_tier", 2025, RATE)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param(
            SURCHARGE_TIERS_2025.replace(
                '  - {threshold: "100", rate: "0.10"}\n  - {threshold: "300.50", rate: "0.25"}\n',
                "  []\n",
            ),
            "at least one tier",
            id="no-tiers",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace('{threshold: "300.50"', '{threshold: "100"'),
            "strictly increasing",
            id="thresholds-equal",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace('{threshold: "300.50"', '{threshold: "50"'),
            "strictly increasing",
            id="thresholds-descending",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace('{threshold: "100"', '{threshold: "-1"'),
            r"tiers\[0\].*threshold must not be negative",
            id="threshold-negative",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace('rate: "0.25"', 'rate: "1.5"'),
            r"tiers\[1\].*rate must be between 0 and 1",
            id="rate-above-one",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace('rate: "0.25"', 'rate: "-0.1"'),
            r"tiers\[1\].*rate must be between 0 and 1",
            id="rate-negative",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace('rate: "0.25"', "rate: 0.25"),
            r"tiers\[1\].rate must be a string, got float",
            id="rate-as-yaml-number",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace('{threshold: "300.50"', "{threshold: 300"),
            r"tiers\[1\].threshold must be a string, got int",
            id="threshold-as-yaml-number",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace('{threshold: "100"', '{threshold: "lots"'),
            r"tiers\[0\].threshold is not a decimal: 'lots'",
            id="threshold-not-decimal",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace('rate: "0.10"', 'rate: "Infinity"'),
            r"tiers\[0\].rate is not a decimal",
            id="rate-infinite",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace('{threshold: "100", rate: "0.10"}', '{rate: "0.10"}'),
            r"tiers\[0\]: missing keys \['threshold'\]",
            id="threshold-missing",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace('rate: "0.25"}', 'rate: "0.25", from: "0"}'),
            r"tiers\[1\]: unknown keys \['from'\]",
            id="unknown-tier-key",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace('  - {threshold: "100", rate: "0.10"}', '  - "100"'),
            r"tiers\[0\] must be a mapping",
            id="tier-not-a-mapping",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace(
                '  - {threshold: "100", rate: "0.10"}\n  - {threshold: "300.50", rate: "0.25"}\n',
                '  {threshold: "100", rate: "0.10"}\n',
            ),
            "tiers must be a list",
            id="tiers-not-a-list",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace("tiers:", "brackets:"),
            r"unknown keys \['brackets'\]",
            id="brackets-are-not-tiers",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025 + 'rate: "0.125"\n',
            r"unknown keys \['rate'\]",
            id="rate-is-not-a-surcharge-tiers-key",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace("kind: surcharge_tiers", "kind: brackets"),
            "kind 'brackets' does not match the requested 'surcharge_tiers'",
            id="kind-mismatch",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace("rounding: none\n", ""),
            r"missing keys \['rounding'\]",
            id="rounding-missing",
        ),
        pytest.param(
            SURCHARGE_TIERS_2025.replace(
                "sources:\n  - https://example.org/surcharge-2025", "sources: []"
            ),
            "sources must list at least one",
            id="sources-empty",
        ),
    ],
)
def test_rejects_malformed_surcharge_tiers_dataset(
    tmp_path: Path, content: str, message: str
) -> None:
    write(tmp_path, "ex/parameters/surcharge_tiers/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS)

    assert "2025.yaml" in str(excinfo.value)


def test_invalid_tiers_are_reported_as_a_surcharge_tiers_error(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/surcharge_tiers/2025.yaml",
        SURCHARGE_TIERS_2025.replace('{threshold: "300.50"', '{threshold: "50"'),
    )

    with pytest.raises(InvalidParameterDataError) as excinfo:
        source(tmp_path).get("ex/surcharge_tiers", 2025, SURCHARGE_TIERS)

    assert isinstance(excinfo.value.__cause__, InvalidSurchargeTiersError)


def test_a_surcharge_tiers_dataset_is_not_a_bracket_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/surcharge_tiers/2025.yaml", SURCHARGE_TIERS_2025)

    with pytest.raises(InvalidParameterDataError, match="kind 'surcharge_tiers' does not match"):
        source(tmp_path).get("ex/surcharge_tiers", 2025, BRACKETS)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param(
            TAPER_2025.replace('base: "1000"', "base: 1000"),
            "base must be a string, got int",
            id="base-as-yaml-number",
        ),
        pytest.param(
            TAPER_2025.replace('supplement: "500"', "supplement: 500.5"),
            "supplement must be a string, got float",
            id="supplement-as-yaml-float",
        ),
        pytest.param(
            TAPER_2025.replace('threshold: "20000"', "threshold: 20000"),
            "threshold must be a string, got int",
            id="threshold-as-yaml-number",
        ),
        pytest.param(
            TAPER_2025.replace('range: "10000"', "range: 10000"),
            "range must be a string, got int",
            id="range-as-yaml-number",
        ),
        pytest.param(
            TAPER_2025.replace('base: "1000"', 'base: "lots"'),
            "base is not a decimal: 'lots'",
            id="base-not-decimal",
        ),
        pytest.param(
            TAPER_2025.replace('threshold: "20000"', 'threshold: "Infinity"'),
            "threshold is not a decimal",
            id="threshold-infinite",
        ),
        pytest.param(
            TAPER_2025.replace('range: "10000"', 'range: "NaN"'),
            "range is not a decimal",
            id="range-nan",
        ),
        pytest.param(
            TAPER_2025.replace('base: "1000"', 'base: "-1"'),
            "base must not be negative",
            id="base-negative",
        ),
        pytest.param(
            TAPER_2025.replace('supplement: "500"', 'supplement: "-0.01"'),
            "supplement must not be negative",
            id="supplement-negative",
        ),
        pytest.param(
            TAPER_2025.replace('threshold: "20000"', 'threshold: "-1"'),
            "threshold must not be negative",
            id="threshold-negative",
        ),
        pytest.param(
            TAPER_2025.replace('range: "10000"', 'range: "0"'),
            "range must be positive",
            id="range-zero",
        ),
        pytest.param(
            TAPER_2025.replace('range: "10000"', 'range: "-10000"'),
            "range must be positive",
            id="range-negative",
        ),
        pytest.param(
            TAPER_2025.replace('range: "10000"\n', ""),
            r"missing keys \['range'\]",
            id="range-missing",
        ),
        pytest.param(
            TAPER_2025.replace('base: "1000"\n', "").replace('supplement: "500"\n', ""),
            r"missing keys \['base', 'supplement'\]",
            id="base-and-supplement-missing",
        ),
        pytest.param(
            TAPER_2025 + 'maximum: "1500"\n',
            r"unknown keys \['maximum'\]",
            id="maximum-is-not-a-taper-key",
        ),
        pytest.param(
            TAPER_2025.replace('range: "10000"', 'upper: "30000"'),
            r"unknown keys \['upper'\]",
            id="upper-instead-of-range",
        ),
        pytest.param(
            TAPER_2025.replace("kind: taper", "kind: amount"),
            "kind 'amount' does not match the requested 'taper'",
            id="kind-mismatch",
        ),
        pytest.param(
            TAPER_2025.replace("rounding: none\n", ""),
            r"missing keys \['rounding'\]",
            id="rounding-missing",
        ),
        pytest.param(
            TAPER_2025.replace("sources:\n  - https://example.org/taper-2025", "sources: []"),
            "sources must list at least one",
            id="sources-empty",
        ),
    ],
)
def test_rejects_malformed_taper_dataset(tmp_path: Path, content: str, message: str) -> None:
    write(tmp_path, "ex/parameters/taper/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        source(tmp_path).get("ex/taper", 2025, TAPER)

    assert "2025.yaml" in str(excinfo.value)


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ('base: "1000"', 'base: "-1"'),
        ('supplement: "500"', 'supplement: "-1"'),
        ('threshold: "20000"', 'threshold: "-1"'),
        ('range: "10000"', 'range: "0"'),
    ],
)
def test_an_invalid_taper_is_reported_as_a_taper_error(tmp_path: Path, old: str, new: str) -> None:
    write(tmp_path, "ex/parameters/taper/2025.yaml", TAPER_2025.replace(old, new))

    with pytest.raises(InvalidParameterDataError) as excinfo:
        source(tmp_path).get("ex/taper", 2025, TAPER)

    assert isinstance(excinfo.value.__cause__, InvalidTaperError)


def test_an_amount_dataset_is_not_a_taper_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/amount_cap/2025.yaml", AMOUNT_2025)

    with pytest.raises(InvalidParameterDataError, match="kind 'amount' does not match"):
        source(tmp_path).get("ex/amount_cap", 2025, TAPER)


def test_a_taper_dataset_is_not_a_credit_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/taper/2025.yaml", TAPER_2025)

    with pytest.raises(InvalidParameterDataError, match="kind 'taper' does not match"):
        source(tmp_path).get("ex/taper", 2025, CREDIT)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param(
            FACTOR_2025.replace('value: "2"', 'value: "-1"'),
            "factor must not be negative",
            id="value-negative",
        ),
        pytest.param(
            FACTOR_2025.replace('value: "2"', 'value: "-0.01"'),
            "factor must not be negative",
            id="value-slightly-negative",
        ),
        pytest.param(
            FACTOR_2025.replace('value: "2"', 'value: "Infinity"'),
            "value is not a decimal",
            id="value-infinite",
        ),
        pytest.param(
            FACTOR_2025.replace('value: "2"', 'value: "NaN"'),
            "value is not a decimal",
            id="value-nan",
        ),
        pytest.param(
            FACTOR_2025.replace('value: "2"', 'value: "twice"'),
            "value is not a decimal: 'twice'",
            id="value-not-decimal",
        ),
        pytest.param(
            FACTOR_2025.replace('value: "2"', "value: 2"),
            "value must be a string, got int",
            id="value-as-yaml-number",
        ),
        pytest.param(
            FACTOR_2025.replace('value: "2"', "value: 2.5"),
            "value must be a string, got float",
            id="value-as-yaml-float",
        ),
        pytest.param(
            FACTOR_2025.replace('value: "2"\n', ""),
            r"missing keys \['value'\]",
            id="value-missing",
        ),
        pytest.param(
            FACTOR_2025.replace('value: "2"', 'factor: "2"'),
            r"unknown keys \['factor'\]",
            id="factor-instead-of-value",
        ),
        pytest.param(
            FACTOR_2025 + 'rate: "0.5"\n',
            r"unknown keys \['rate'\]",
            id="rate-is-not-a-factor-key",
        ),
        pytest.param(
            FACTOR_2025.replace("kind: factor", "kind: rate"),
            "kind 'rate' does not match the requested 'factor'",
            id="kind-mismatch",
        ),
        pytest.param(
            FACTOR_2025.replace("rounding: none\n", ""),
            r"missing keys \['rounding'\]",
            id="rounding-missing",
        ),
        pytest.param(
            FACTOR_2025.replace("sources:\n  - https://example.org/factor-2025", "sources: []"),
            "sources must list at least one",
            id="sources-empty",
        ),
    ],
)
def test_rejects_malformed_factor_dataset(tmp_path: Path, content: str, message: str) -> None:
    write(tmp_path, "ex/parameters/factor/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        source(tmp_path).get("ex/factor", 2025, FACTOR)

    assert "2025.yaml" in str(excinfo.value)


def test_a_negative_factor_is_reported_as_a_factor_error(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex/parameters/factor/2025.yaml",
        FACTOR_2025.replace('value: "2"', 'value: "-1"'),
    )

    with pytest.raises(InvalidParameterDataError) as excinfo:
        source(tmp_path).get("ex/factor", 2025, FACTOR)

    assert isinstance(excinfo.value.__cause__, InvalidFactorError)


def test_a_rate_dataset_is_not_a_factor_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/credit_rate/2025.yaml", RATE_2025)

    with pytest.raises(InvalidParameterDataError, match="kind 'rate' does not match"):
        source(tmp_path).get("ex/credit_rate", 2025, FACTOR)


def test_a_factor_dataset_is_not_an_amount_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/factor/2025.yaml", FACTOR_2025)

    with pytest.raises(InvalidParameterDataError, match="kind 'factor' does not match"):
        source(tmp_path).get("ex/factor", 2025, AMOUNT)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param(
            FRACTION_2025.replace('numerator: "2"', 'numerator: "0"'),
            "fraction numerator must be positive",
            id="numerator-zero",
        ),
        pytest.param(
            FRACTION_2025.replace('denominator: "3"', 'denominator: "0"'),
            "fraction denominator must be positive",
            id="denominator-zero",
        ),
        pytest.param(
            FRACTION_2025.replace('numerator: "2"', 'numerator: "-2"'),
            "numerator is not a whole number: '-2'",
            id="numerator-negative",
        ),
        pytest.param(
            FRACTION_2025.replace('denominator: "3"', 'denominator: "-3"'),
            "denominator is not a whole number: '-3'",
            id="denominator-negative",
        ),
        pytest.param(
            FRACTION_2025.replace('numerator: "2"', 'numerator: "2.5"'),
            "numerator is not a whole number: '2.5'",
            id="numerator-not-whole",
        ),
        pytest.param(
            FRACTION_2025.replace('denominator: "3"', 'denominator: "3.0"'),
            "denominator is not a whole number: '3.0'",
            id="denominator-with-a-decimal-point",
        ),
        pytest.param(
            FRACTION_2025.replace('numerator: "2"', 'numerator: "NaN"'),
            "numerator is not a whole number: 'NaN'",
            id="numerator-nan",
        ),
        pytest.param(
            FRACTION_2025.replace('denominator: "3"', 'denominator: "Infinity"'),
            "denominator is not a whole number: 'Infinity'",
            id="denominator-infinite",
        ),
        pytest.param(
            FRACTION_2025.replace('numerator: "2"', 'numerator: "two"'),
            "numerator is not a whole number: 'two'",
            id="numerator-words",
        ),
        pytest.param(
            FRACTION_2025.replace('numerator: "2"', 'numerator: "+2"'),
            r"numerator is not a whole number: '\+2'",
            id="numerator-signed",
        ),
        pytest.param(
            FRACTION_2025.replace('denominator: "3"', 'denominator: "03"'),
            "denominator is not a whole number: '03'",
            id="denominator-leading-zero",
        ),
        pytest.param(
            FRACTION_2025.replace('denominator: "3"', 'denominator: " 3"'),
            "denominator is not a whole number: ' 3'",
            id="denominator-padded",
        ),
        pytest.param(
            FRACTION_2025.replace('denominator: "3"', 'denominator: "1_000"'),
            "denominator is not a whole number: '1_000'",
            id="denominator-underscored",
        ),
        pytest.param(
            FRACTION_2025.replace('numerator: "2"', 'numerator: "\u0662"'),
            "numerator is not a whole number",
            id="numerator-non-ascii-digit",
        ),
        pytest.param(
            FRACTION_2025.replace('numerator: "2"', 'numerator: ""'),
            "numerator is not a whole number: ''",
            id="numerator-empty",
        ),
        pytest.param(
            FRACTION_2025.replace('numerator: "2"', "numerator: 2"),
            "numerator must be a string, got int",
            id="numerator-as-yaml-number",
        ),
        pytest.param(
            FRACTION_2025.replace('denominator: "3"', "denominator: 3"),
            "denominator must be a string, got int",
            id="denominator-as-yaml-number",
        ),
        pytest.param(
            FRACTION_2025.replace('numerator: "2"', "numerator: 2.5"),
            "numerator must be a string, got float",
            id="numerator-as-yaml-float",
        ),
        pytest.param(
            FRACTION_2025.replace('denominator: "3"\n', ""),
            r"missing keys \['denominator'\]",
            id="denominator-missing",
        ),
        pytest.param(
            FRACTION_2025.replace('numerator: "2"\n', "").replace('denominator: "3"\n', ""),
            r"missing keys \['denominator', 'numerator'\]",
            id="both-parts-missing",
        ),
        pytest.param(
            FRACTION_2025.replace('numerator: "2"\ndenominator: "3"', 'value: "2/3"'),
            r"unknown keys \['value'\]",
            id="value-instead-of-parts",
        ),
        pytest.param(
            FRACTION_2025 + 'rate: "0.5"\n',
            r"unknown keys \['rate'\]",
            id="rate-is-not-a-fraction-key",
        ),
        pytest.param(
            FRACTION_2025.replace("kind: fraction", "kind: rate"),
            "kind 'rate' does not match the requested 'fraction'",
            id="kind-mismatch",
        ),
        pytest.param(
            FRACTION_2025.replace("rounding: none\n", ""),
            r"missing keys \['rounding'\]",
            id="rounding-missing",
        ),
        pytest.param(
            FRACTION_2025.replace("sources:\n  - https://example.org/fraction-2025", "sources: []"),
            "sources must list at least one",
            id="sources-empty",
        ),
    ],
)
def test_rejects_malformed_fraction_dataset(tmp_path: Path, content: str, message: str) -> None:
    write(tmp_path, "ex/parameters/fraction/2025.yaml", content)

    with pytest.raises(InvalidParameterDataError, match=message) as excinfo:
        source(tmp_path).get("ex/fraction", 2025, FRACTION)

    assert "2025.yaml" in str(excinfo.value)


def test_rejects_a_part_too_long_for_a_whole_number(tmp_path: Path) -> None:
    # 4,301 digits: one more than `int()` converts from text by default.
    part = "1" + "0" * 4300
    write(
        tmp_path,
        "ex/parameters/fraction/2025.yaml",
        FRACTION_2025.replace('numerator: "2"', f'numerator: "{part}"'),
    )

    with pytest.raises(
        InvalidParameterDataError, match="numerator is not a whole number"
    ) as excinfo:
        source(tmp_path).get("ex/fraction", 2025, FRACTION)

    assert "2025.yaml" in str(excinfo.value)


@pytest.mark.parametrize(
    ("old", "new"),
    [('numerator: "2"', 'numerator: "0"'), ('denominator: "3"', 'denominator: "0"')],
)
def test_a_zero_part_is_reported_as_a_fraction_error(tmp_path: Path, old: str, new: str) -> None:
    write(tmp_path, "ex/parameters/fraction/2025.yaml", FRACTION_2025.replace(old, new))

    with pytest.raises(InvalidParameterDataError) as excinfo:
        source(tmp_path).get("ex/fraction", 2025, FRACTION)

    assert isinstance(excinfo.value.__cause__, InvalidFractionError)


def test_a_rate_dataset_is_not_a_fraction_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/credit_rate/2025.yaml", RATE_2025)

    with pytest.raises(InvalidParameterDataError, match="kind 'rate' does not match"):
        source(tmp_path).get("ex/credit_rate", 2025, FRACTION)


def test_a_fraction_dataset_is_not_a_rate_dataset(tmp_path: Path) -> None:
    write(tmp_path, "ex/parameters/fraction/2025.yaml", FRACTION_2025)

    with pytest.raises(InvalidParameterDataError, match="kind 'fraction' does not match"):
        source(tmp_path).get("ex/fraction", 2025, RATE)
