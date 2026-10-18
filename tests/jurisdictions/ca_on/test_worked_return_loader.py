"""The worked-return loader: a file's shape is checked and its identifiers resolved, or it fails.

Every failure names the file and the key that is wrong, so a reviewer editing a return sees where.
"""

from __future__ import annotations

import re
from decimal import Decimal
from pathlib import Path

import pytest

from app.domain.artifact import Artifact, ArtifactKind, ArtifactRegistry
from app.domain.errors import NegativeArtifactError
from app.domain.jurisdiction_code import JurisdictionCode
from app.jurisdictions.ca.catalog import (
    FEDERAL_BASIC_TAX,
    TAXABLE_INCOME,
)
from app.registrations import JURISDICTIONS
from tests.jurisdictions.ca_on.worked_return import WorkedReturn, WorkedReturnError

D = Decimal
RETURNS = Path(__file__).parent / "returns"
SECTIONS = {
    "jurisdiction": "jurisdiction: CA-ON\n",
    "tax_year": "tax_year: 2025\n",
    "description": "description: A return for the loader's tests.\n",
    "sources": "sources:\n  - T1 arithmetic.\n",
    "inputs": 'inputs:\n  ca/taxable_income: "115000"\n',
    "expected": 'expected:\n  ca/federal_basic_tax: "20146.25"\n',
}
VALID = "".join(SECTIONS.values())
# Made up for the count tests and not registered with the application: a non-negative count.
COUNT = ArtifactKind("ex/count", int, non_negative=True)


@pytest.fixture
def artifacts() -> ArtifactRegistry:
    JURISDICTIONS.register()
    return ArtifactRegistry.shared()


@pytest.fixture
def counts() -> ArtifactRegistry:
    """A registry of the made-up count and the federal basic tax `VALID` expects."""
    artifacts = ArtifactRegistry()
    artifacts.register(COUNT.identifier, COUNT)
    artifacts.register(FEDERAL_BASIC_TAX.identifier, FEDERAL_BASIC_TAX)
    return artifacts


def write(tmp_path: Path, text: str, name: str = "bad.yaml") -> Path:
    path = tmp_path / name
    path.write_text(text)
    return path


def with_section(section: str, text: str) -> str:
    """`VALID` with `section` replaced by `text` (which may be empty, removing it)."""
    return "".join(text if key == section else body for key, body in SECTIONS.items())


@pytest.mark.parametrize("path", WorkedReturn.discover(RETURNS), ids=lambda path: path.stem)
def test_loads_every_real_return(path: Path, artifacts: ArtifactRegistry) -> None:
    # Only what holds for every file in `returns/`; the figures themselves are checked by the
    # per-file computation test, never pinned here.
    worked = WorkedReturn.load(path, artifacts)

    assert worked.path == path
    assert worked.jurisdiction == JurisdictionCode("CA-ON")
    assert worked.tax_year == 2025
    assert worked.inputs and worked.expected and worked.sources


def test_loads_a_valid_file(tmp_path: Path, artifacts: ArtifactRegistry) -> None:
    worked = WorkedReturn.load(write(tmp_path, VALID, "ok.yaml"), artifacts)

    assert worked.description == "A return for the loader's tests."
    assert worked.sources == ("T1 arithmetic.",)
    assert worked.inputs == (Artifact(TAXABLE_INCOME, D("115000")),)
    assert worked.expected == (Artifact(FEDERAL_BASIC_TAX, D("20146.25")),)


@pytest.mark.parametrize("section", ["inputs", "expected"])
def test_an_unknown_identifier_names_the_file_and_key(
    tmp_path: Path, artifacts: ArtifactRegistry, section: str
) -> None:
    path = write(tmp_path, with_section(section, f'{section}:\n  ca/no_such_line: "1"\n'))

    with pytest.raises(
        WorkedReturnError,
        match=rf"bad\.yaml: {section}\.ca/no_such_line: unknown artifact identifier",
    ):
        WorkedReturn.load(path, artifacts)


@pytest.mark.parametrize(
    ("amount", "problem"),
    [
        ('"lots"', "is not a decimal"),
        ('"NaN"', "is not a decimal"),
        ("115000", "must be a string"),  # unquoted: YAML would make it a number
        ("115000.5", "must be a string"),
    ],
)
def test_a_non_decimal_amount_names_the_file_and_key(
    tmp_path: Path, artifacts: ArtifactRegistry, amount: str, problem: str
) -> None:
    path = write(tmp_path, VALID.replace('"115000"', amount))

    with pytest.raises(WorkedReturnError, match=rf"bad\.yaml: inputs\.ca/taxable_income {problem}"):
        WorkedReturn.load(path, artifacts)


@pytest.mark.parametrize("section", list(SECTIONS))
def test_a_missing_section_names_the_file_and_section(
    tmp_path: Path, artifacts: ArtifactRegistry, section: str
) -> None:
    path = write(tmp_path, with_section(section, ""))

    with pytest.raises(WorkedReturnError, match=rf"bad\.yaml: .*missing keys \['{section}'\]"):
        WorkedReturn.load(path, artifacts)


def test_an_unknown_section_names_the_file_and_section(
    tmp_path: Path, artifacts: ArtifactRegistry
) -> None:
    path = write(tmp_path, VALID + "notes: extra\n")

    with pytest.raises(WorkedReturnError, match=r"bad\.yaml: .*unknown keys \['notes'\]"):
        WorkedReturn.load(path, artifacts)


@pytest.mark.parametrize("section", ["inputs", "expected", "sources"])
def test_an_empty_section_names_the_file_and_section(
    tmp_path: Path, artifacts: ArtifactRegistry, section: str
) -> None:
    empty = f"{section}: []\n" if section == "sources" else f"{section}: {{}}\n"
    path = write(tmp_path, with_section(section, empty))

    with pytest.raises(WorkedReturnError, match=rf"bad\.yaml: {section} must not be empty"):
        WorkedReturn.load(path, artifacts)


@pytest.mark.parametrize(
    ("section", "text", "message"),
    [
        ("jurisdiction", "jurisdiction: ca-on\n", r"jurisdiction: invalid jurisdiction code"),
        ("tax_year", 'tax_year: "2025"\n', r"tax_year must be an integer"),
        ("description", 'description: ""\n', r"description must not be empty"),
        ("sources", "sources: T1 arithmetic.\n", r"sources must be a list"),
        ("sources", 'sources:\n  - ""\n', r"sources\[0\] must not be empty"),
        ("inputs", "inputs:\n  - ca/taxable_income\n", r"inputs must be a mapping"),
    ],
)
def test_a_malformed_section_names_the_file_and_section(
    tmp_path: Path, artifacts: ArtifactRegistry, section: str, text: str, message: str
) -> None:
    path = write(tmp_path, with_section(section, text))

    with pytest.raises(WorkedReturnError, match=rf"bad\.yaml: {message}"):
        WorkedReturn.load(path, artifacts)


def test_an_identifier_that_is_not_an_amount_names_the_file_and_key(tmp_path: Path) -> None:
    artifacts = ArtifactRegistry()
    artifacts.register("ex/flag", ArtifactKind("ex/flag", bool))
    artifacts.register(FEDERAL_BASIC_TAX.identifier, FEDERAL_BASIC_TAX)
    path = write(tmp_path, with_section("inputs", 'inputs:\n  ex/flag: "1"\n'))

    with pytest.raises(WorkedReturnError, match=r"bad\.yaml: inputs\.ex/flag: .*not an amount"):
        WorkedReturn.load(path, artifacts)


def test_an_int_kind_takes_a_digit_string(tmp_path: Path, counts: ArtifactRegistry) -> None:
    path = write(tmp_path, with_section("inputs", 'inputs:\n  ex/count: "3"\n'), "ok.yaml")

    worked = WorkedReturn.load(path, counts)

    assert worked.inputs == (Artifact(COUNT, 3),)
    assert type(worked.inputs[0].value) is int


def test_an_int_kind_takes_zero(tmp_path: Path, counts: ArtifactRegistry) -> None:
    path = write(tmp_path, with_section("inputs", 'inputs:\n  ex/count: "0"\n'), "ok.yaml")

    assert WorkedReturn.load(path, counts).inputs == (Artifact(COUNT, 0),)


def test_an_int_kind_takes_a_count_of_several_digits(
    tmp_path: Path, counts: ArtifactRegistry
) -> None:
    path = write(tmp_path, with_section("inputs", 'inputs:\n  ex/count: "120"\n'), "ok.yaml")

    assert WorkedReturn.load(path, counts).inputs == (Artifact(COUNT, 120),)


@pytest.mark.parametrize(
    ("count", "got"),
    [
        # Unquoted, YAML reads a count before the loader sees it, so it must be quoted.
        ("3", "int"),
        ("0", "int"),
        ("010", "int"),  # YAML 1.1 octal: 8
        ("0x10", "int"),  # hexadecimal: 16
        ("1_000", "int"),  # 1000
        ("1:30", "int"),  # sexagesimal: 90
        ("-1", "int"),
        ("true", "bool"),
        ("false", "bool"),
        ("yes", "bool"),
        ("3.0", "float"),
    ],
)
def test_an_int_kind_refuses_an_unquoted_value(
    tmp_path: Path, counts: ArtifactRegistry, count: str, got: str
) -> None:
    path = write(tmp_path, with_section("inputs", f"inputs:\n  ex/count: {count}\n"))

    with pytest.raises(
        WorkedReturnError, match=rf"bad\.yaml: inputs\.ex/count must be a string, got {got}"
    ):
        WorkedReturn.load(path, counts)


@pytest.mark.parametrize(
    "count",
    [
        "03",  # a leading zero is refused, so a count has one spelling
        "00",
        "+3",
        "-1",
        "3.0",
        "3e0",
        "three",
        "",
        " 3",
        "3 ",
        "1_000",
        "1,000",
        "0x10",
        "true",
        "\u0663",  # ARABIC-INDIC DIGIT THREE: a digit to str.isdigit, not a decimal digit here
        "\u00b3",  # SUPERSCRIPT THREE
    ],
)
def test_an_int_kind_refuses_a_string_that_is_not_decimal_digits(
    tmp_path: Path, counts: ArtifactRegistry, count: str
) -> None:
    path = write(tmp_path, with_section("inputs", f'inputs:\n  ex/count: "{count}"\n'))

    with pytest.raises(
        WorkedReturnError,
        match=rf"bad\.yaml: inputs\.ex/count is not a count: {re.escape(repr(count))}",
    ):
        WorkedReturn.load(path, counts)


def test_a_count_under_expected_names_the_file_and_key(
    tmp_path: Path, counts: ArtifactRegistry
) -> None:
    # Counts are what a return starts from, never a line it expects.
    text = with_section("inputs", 'inputs:\n  ex/count: "3"\n')
    path = write(
        tmp_path, text.replace('  ca/federal_basic_tax: "20146.25"\n', '  ex/count: "3"\n')
    )

    with pytest.raises(WorkedReturnError, match=r"bad\.yaml: expected\.ex/count: .*not an amount"):
        WorkedReturn.load(path, counts)


def test_loads_the_ontario_counts_as_integers(tmp_path: Path, artifacts: ArtifactRegistry) -> None:
    text = with_section(
        "inputs", 'inputs:\n  ca-on/dependent_children: "2"\n  ca-on/dependants: "1"\n'
    )

    worked = WorkedReturn.load(write(tmp_path, text, "ok.yaml"), artifacts)

    assert worked.inputs == (
        Artifact(artifacts.kind("ca-on/dependent_children"), 2),
        Artifact(artifacts.kind("ca-on/dependants"), 1),
    )
    assert all(type(artifact.value) is int for artifact in worked.inputs)


@pytest.mark.parametrize(("count", "got"), [("0", "int"), ("true", "bool")])
def test_an_unquoted_ontario_count_names_the_file_and_key(
    tmp_path: Path, artifacts: ArtifactRegistry, count: str, got: str
) -> None:
    path = write(tmp_path, with_section("inputs", f"inputs:\n  ca-on/dependants: {count}\n"))

    with pytest.raises(
        WorkedReturnError,
        match=rf"bad\.yaml: inputs\.ca-on/dependants must be a string, got {got}",
    ):
        WorkedReturn.load(path, artifacts)


def test_return_a_with_negative_union_dues_fails_at_load_naming_the_kind(
    tmp_path: Path, artifacts: ArtifactRegistry
) -> None:
    text = (RETURNS / "2025_return_a.yaml").read_text()
    assert 'ca/union_dues: "2000"' in text
    path = write(tmp_path, text.replace('ca/union_dues: "2000"', 'ca/union_dues: "-40000"'))

    with pytest.raises(NegativeArtifactError, match=r"ca/union_dues.*-40000"):
        WorkedReturn.load(path, artifacts)


def test_a_negative_expected_amount_for_a_non_negative_kind_fails_at_load_naming_the_kind(
    tmp_path: Path, artifacts: ArtifactRegistry
) -> None:
    path = write(tmp_path, VALID.replace('"20146.25"', '"-1"'))

    with pytest.raises(NegativeArtifactError, match="ca/federal_basic_tax"):
        WorkedReturn.load(path, artifacts)


def test_a_negative_expected_refund_loads_as_a_negative_amount(
    tmp_path: Path, artifacts: ArtifactRegistry
) -> None:
    # T1 line 167 is negative for a refund: the one signed `ca/` kind loads below zero.
    text = VALID.replace(
        'ca/federal_basic_tax: "20146.25"', 'ca/refund_or_balance_owing: "-4102.8546524"'
    )

    worked = WorkedReturn.load(write(tmp_path, text, "ok.yaml"), artifacts)

    assert worked.expected == (
        Artifact(artifacts.kind("ca/refund_or_balance_owing"), D("-4102.8546524")),
    )


def test_a_file_that_is_not_yaml_names_the_file(
    tmp_path: Path, artifacts: ArtifactRegistry
) -> None:
    path = write(tmp_path, "jurisdiction: [unclosed\n")

    with pytest.raises(WorkedReturnError, match=r"bad\.yaml: "):
        WorkedReturn.load(path, artifacts)


def test_requires_every_declared_output(tmp_path: Path, artifacts: ArtifactRegistry) -> None:
    worked = WorkedReturn.load(write(tmp_path, VALID, "valid.yaml"), artifacts)

    worked.require_outputs(frozenset({"ca/federal_basic_tax"}))
    with pytest.raises(
        WorkedReturnError,
        match=r"valid\.yaml: expected: missing declared outputs \['ca-on/other'\]",
    ):
        worked.require_outputs(frozenset({"ca/federal_basic_tax", "ca-on/other"}))


def test_discovers_every_yaml_file_in_name_order(tmp_path: Path) -> None:
    for name in ("b.yaml", "a.yaml", "notes.txt", "c.yml"):
        (tmp_path / name).write_text("")

    assert WorkedReturn.discover(tmp_path) == (tmp_path / "a.yaml", tmp_path / "b.yaml")
