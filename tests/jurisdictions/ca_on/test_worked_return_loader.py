"""The worked-return loader: a file's shape is checked and its identifiers resolved, or it fails.

Every failure names the file and the key that is wrong, so a reviewer editing a return sees where.
"""

from __future__ import annotations

import re
from decimal import Decimal
from pathlib import Path

import pytest

from app.domain.artifact import Artifact, ArtifactCatalog, ArtifactKind, ArtifactRegistry
from app.domain.digits import DigitsKind
from app.domain.errors import InvalidTextError, NegativeArtifactError
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.record_list import RecordList, RecordListKind
from app.domain.registry import Namespace
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
# Made up for the record-list tests: a YAML list of two records, each keyed by the identifiers
# of its fields, an amount and a count, both quoted.
DEPENDANTS = (
    "inputs:\n"
    "  ex/dependants:\n"
    '    - ex/dependant_net_income: "25000"\n'
    '      ex/months_resident: "12"\n'
    '    - ex/dependant_net_income: "5000.50"\n'
    '      ex/months_resident: "6"\n'
)


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


@pytest.fixture
def records() -> ArtifactRegistry:
    """A registry of made-up `ex/dependants` records (a non-negative amount and count) and the
    federal basic tax `VALID` expects."""
    catalog = ArtifactCatalog(Namespace("ex"))
    net_income = catalog.declare("dependant_net_income", Decimal, non_negative=True)
    months = catalog.declare("months_resident", int, non_negative=True)
    RecordListKind.declare(catalog, "dependants", fields=(net_income, months))
    artifacts = ArtifactRegistry()
    artifacts.register_catalog(catalog)
    artifacts.register(FEDERAL_BASIC_TAX.identifier, FEDERAL_BASIC_TAX)
    return artifacts


@pytest.fixture
def digits() -> ArtifactRegistry:
    """A registry of the made-up nine-digit `ex/business_number`, a count, and the federal basic
    tax `VALID` expects."""
    catalog = ArtifactCatalog(Namespace("ex"))
    DigitsKind.declare(catalog, "business_number", digits=9)
    catalog.declare("partnership_member", int, non_negative=True)
    artifacts = ArtifactRegistry()
    artifacts.register_catalog(catalog)
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


def with_expected_count(value: str) -> str:
    """`VALID` with a count input, also expecting the made-up count `ex/count` (a count output)."""
    return with_section("inputs", 'inputs:\n  ex/count: "3"\n').replace(
        'expected:\n  ca/federal_basic_tax: "20146.25"\n',
        f'expected:\n  ca/federal_basic_tax: "20146.25"\n  ex/count: {value}\n',
    )


def test_a_count_under_expected_loads_as_an_integer(
    tmp_path: Path, counts: ArtifactRegistry
) -> None:
    # A count a manifest declares as an output, such as a number of list items, is a line a return
    # expects, spelled like an input count.
    path = write(tmp_path, with_expected_count('"3"'), "ok.yaml")

    worked = WorkedReturn.load(path, counts)

    assert worked.expected == (Artifact(FEDERAL_BASIC_TAX, D("20146.25")), Artifact(COUNT, 3))
    assert type(worked.expected[1].value) is int


def test_a_zero_count_under_expected_loads(tmp_path: Path, counts: ArtifactRegistry) -> None:
    path = write(tmp_path, with_expected_count('"0"'), "ok.yaml")

    assert WorkedReturn.load(path, counts).expected[1] == Artifact(COUNT, 0)


@pytest.mark.parametrize(("count", "got"), [("3", "int"), ("true", "bool"), ("3.0", "float")])
def test_an_unquoted_count_under_expected_names_the_file_and_key(
    tmp_path: Path, counts: ArtifactRegistry, count: str, got: str
) -> None:
    path = write(tmp_path, with_expected_count(count))

    with pytest.raises(
        WorkedReturnError, match=rf"bad\.yaml: expected\.ex/count must be a string, got {got}"
    ):
        WorkedReturn.load(path, counts)


@pytest.mark.parametrize("count", ["03", "-1", "3.0", "three", ""])
def test_a_count_under_expected_that_is_not_decimal_digits_names_the_file_and_key(
    tmp_path: Path, counts: ArtifactRegistry, count: str
) -> None:
    path = write(tmp_path, with_expected_count(f'"{count}"'))

    with pytest.raises(
        WorkedReturnError,
        match=rf"bad\.yaml: expected\.ex/count is not a count: {re.escape(repr(count))}",
    ):
        WorkedReturn.load(path, counts)


def test_a_count_under_expected_is_kept_when_blanks_are_filled(
    tmp_path: Path, counts: ArtifactRegistry
) -> None:
    path = write(tmp_path, with_expected_count('"3"'), "ok.yaml")
    worked = WorkedReturn.load(path, counts)

    filled = worked.with_blanks(
        frozenset({"ex/count"}), frozenset({"ca/federal_basic_tax", "ex/count"}), counts
    )

    assert filled == worked


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


def test_loads_the_federal_counts_as_integers(tmp_path: Path, artifacts: ArtifactRegistry) -> None:
    # T1 line 30400 (Schedule 5) and line 30499: the eligible dependants claimed for and the
    # infirm children, counts read like the Ontario ones.
    text = with_section(
        "inputs", 'inputs:\n  ca/eligible_dependants: "1"\n  ca/infirm_children: "2"\n'
    )

    worked = WorkedReturn.load(write(tmp_path, text, "ok.yaml"), artifacts)

    assert worked.inputs == (
        Artifact(artifacts.kind("ca/eligible_dependants"), 1),
        Artifact(artifacts.kind("ca/infirm_children"), 2),
    )
    assert all(type(artifact.value) is int for artifact in worked.inputs)


def test_loads_the_age_and_spouse_inputs(tmp_path: Path, artifacts: ArtifactRegistry) -> None:
    # T1 line 30100 "(if you were born in 1960 or earlier)", Schedule 5 line 30300 (claimed) and
    # line 51090 (eligible for the Canada caregiver amount for the spouse): counts, read like the
    # others; the spouse's net income (Schedule 5 line 4) an amount.
    text = with_section(
        "inputs",
        "inputs:\n"
        '  ca/born_in_1960_or_earlier: "1"\n'
        '  ca/spouse_net_income: "12000.00"\n'
        '  ca/spouses_claimed: "1"\n'
        '  ca/spouse_caregiver_eligible: "1"\n',
    )

    worked = WorkedReturn.load(write(tmp_path, text, "ok.yaml"), artifacts)

    assert worked.inputs == (
        Artifact(artifacts.kind("ca/born_in_1960_or_earlier"), 1),
        Artifact(artifacts.kind("ca/spouse_net_income"), D("12000.00")),
        Artifact(artifacts.kind("ca/spouses_claimed"), 1),
        Artifact(artifacts.kind("ca/spouse_caregiver_eligible"), 1),
    )
    assert [type(artifact.value) for artifact in worked.inputs] == [int, D, int, int]


def test_loads_the_child_care_counts_as_integers(
    tmp_path: Path, artifacts: ArtifactRegistry
) -> None:
    # Form T778 Part B lines 1 to 3: the numbers of eligible children, counts read like the others.
    text = with_section(
        "inputs",
        "inputs:\n"
        '  ca/children_under_seven: "0"\n'
        '  ca/children_with_disability: "2"\n'
        '  ca/children_seven_to_sixteen: "1"\n',
    )

    worked = WorkedReturn.load(write(tmp_path, text, "ok.yaml"), artifacts)

    assert worked.inputs == (
        Artifact(artifacts.kind("ca/children_under_seven"), 0),
        Artifact(artifacts.kind("ca/children_with_disability"), 2),
        Artifact(artifacts.kind("ca/children_seven_to_sixteen"), 1),
    )
    assert all(type(artifact.value) is int for artifact in worked.inputs)


def test_loads_the_schedule_6_eligible_dependant_count_as_an_integer(
    tmp_path: Path, artifacts: ArtifactRegistry
) -> None:
    # Schedule 6 line 38100: the number of eligible dependants for the Canada workers benefit,
    # a count read like the others, apart from the T1 line 30400 count.
    text = with_section(
        "inputs", 'inputs:\n  ca/eligible_dependants: "0"\n  ca/cwb_eligible_dependants: "1"\n'
    )

    worked = WorkedReturn.load(write(tmp_path, text, "ok.yaml"), artifacts)

    assert worked.inputs == (
        Artifact(artifacts.kind("ca/eligible_dependants"), 0),
        Artifact(artifacts.kind("ca/cwb_eligible_dependants"), 1),
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


def test_an_expected_line_left_out_is_expected_to_be_zero(
    tmp_path: Path, artifacts: ArtifactRegistry
) -> None:
    worked = WorkedReturn.load(write(tmp_path, VALID, "valid.yaml"), artifacts)

    filled = worked.with_blanks(
        frozenset({"ca/taxable_income"}),
        frozenset({"ca/federal_basic_tax", "ca/taxable_capital_gains"}),
        artifacts,
    )

    assert filled.inputs == worked.inputs
    assert filled.expected == (
        *worked.expected,
        Artifact(artifacts.kind("ca/taxable_capital_gains"), D(0)),
    )


def test_an_input_left_out_is_blank_an_amount_a_count_or_no_records(
    tmp_path: Path, records: ArtifactRegistry
) -> None:
    records.register(COUNT.identifier, COUNT)
    text = with_section("inputs", 'inputs:\n  ex/count: "3"\n')
    worked = WorkedReturn.load(write(tmp_path, text, "valid.yaml"), records)

    filled = worked.with_blanks(
        frozenset({"ex/count", "ex/dependants", "ex/months_resident", "ex/dependant_net_income"}),
        frozenset(),
        records,
    )

    blanks = {artifact.kind.identifier: artifact.value for artifact in filled.inputs}
    assert blanks["ex/count"] == 3
    assert blanks["ex/months_resident"] == 0
    assert type(blanks["ex/months_resident"]) is int
    assert blanks["ex/dependant_net_income"] == D(0)
    kind = records.kind("ex/dependants")
    assert isinstance(kind, RecordListKind)
    assert blanks["ex/dependants"] == RecordList(kind.fields, [])
    assert filled.expected == worked.expected


def test_a_blank_never_replaces_a_line_the_file_gives(
    tmp_path: Path, artifacts: ArtifactRegistry
) -> None:
    worked = WorkedReturn.load(write(tmp_path, VALID, "valid.yaml"), artifacts)

    filled = worked.with_blanks(
        frozenset({"ca/taxable_income"}), frozenset({"ca/federal_basic_tax"}), artifacts
    )

    assert filled == worked


def test_a_declared_identifier_nothing_registers_fails_naming_the_file(
    tmp_path: Path, artifacts: ArtifactRegistry
) -> None:
    worked = WorkedReturn.load(write(tmp_path, VALID, "valid.yaml"), artifacts)

    with pytest.raises(
        WorkedReturnError, match=r"valid\.yaml: inputs: unknown artifact identifier 'ca/nothing'"
    ):
        worked.with_blanks(frozenset({"ca/nothing"}), frozenset(), artifacts)


def test_a_record_list_has_no_blank_as_an_expected_line(
    tmp_path: Path, records: ArtifactRegistry
) -> None:
    worked = WorkedReturn.load(
        write(tmp_path, with_section("inputs", DEPENDANTS), "valid.yaml"), records
    )

    with pytest.raises(
        WorkedReturnError, match=r"valid\.yaml: expected: 'ex/dependants' holds a RecordList"
    ):
        worked.with_blanks(frozenset(), frozenset({"ex/dependants"}), records)


def test_discovers_every_yaml_file_in_name_order(tmp_path: Path) -> None:
    for name in ("b.yaml", "a.yaml", "notes.txt", "c.yml"):
        (tmp_path / name).write_text("")

    assert WorkedReturn.discover(tmp_path) == (tmp_path / "a.yaml", tmp_path / "b.yaml")


def test_a_record_list_input_loads_its_records_in_order(
    tmp_path: Path, records: ArtifactRegistry
) -> None:
    path = write(tmp_path, with_section("inputs", DEPENDANTS), "ok.yaml")
    kind = records.kind("ex/dependants")
    net_income = records.kind("ex/dependant_net_income")
    months = records.kind("ex/months_resident")

    worked = WorkedReturn.load(path, records)

    expected = RecordList(
        (net_income, months),
        [{net_income: D("25000"), months: 12}, {net_income: D("5000.50"), months: 6}],
    )
    assert worked.inputs == (Artifact(kind, expected),)
    loaded = worked.inputs[0].value.records
    assert str(loaded[1][net_income]) == "5000.50"
    assert type(loaded[1][months]) is int


def test_an_empty_record_list_loads_as_no_records(
    tmp_path: Path, records: ArtifactRegistry
) -> None:
    path = write(tmp_path, with_section("inputs", "inputs:\n  ex/dependants: []\n"), "ok.yaml")
    kind = records.kind("ex/dependants")
    fields = (records.kind("ex/dependant_net_income"), records.kind("ex/months_resident"))

    worked = WorkedReturn.load(path, records)

    assert worked.inputs == (Artifact(kind, RecordList(fields, [])),)


def test_a_record_list_that_is_not_a_list_names_the_file_and_key(
    tmp_path: Path, records: ArtifactRegistry
) -> None:
    path = write(tmp_path, with_section("inputs", 'inputs:\n  ex/dependants: "2"\n'))

    with pytest.raises(WorkedReturnError, match=r"bad\.yaml: inputs\.ex/dependants must be a list"):
        WorkedReturn.load(path, records)


def test_a_record_that_is_not_a_mapping_names_the_file_and_item(
    tmp_path: Path, records: ArtifactRegistry
) -> None:
    path = write(tmp_path, with_section("inputs", 'inputs:\n  ex/dependants:\n    - "25000"\n'))

    with pytest.raises(
        WorkedReturnError, match=r"bad\.yaml: inputs\.ex/dependants\[0\] must be a mapping"
    ):
        WorkedReturn.load(path, records)


def test_a_record_missing_a_field_names_the_file_item_and_field(
    tmp_path: Path, records: ArtifactRegistry
) -> None:
    text = DEPENDANTS.replace('      ex/months_resident: "6"\n', "")
    path = write(tmp_path, with_section("inputs", text))

    with pytest.raises(
        WorkedReturnError,
        match=r"bad\.yaml: inputs\.ex/dependants\[1\]: missing keys \['ex/months_resident'\]",
    ):
        WorkedReturn.load(path, records)


@pytest.mark.parametrize("key", ["ex/other", "ca/federal_basic_tax", "months_resident"])
def test_a_record_with_an_unknown_field_names_the_file_item_and_field(
    tmp_path: Path, records: ArtifactRegistry, key: str
) -> None:
    # A field is one of the record list's own kinds: another registered kind is unknown here too.
    text = DEPENDANTS + f'      {key}: "1"\n'
    path = write(tmp_path, with_section("inputs", text))

    with pytest.raises(
        WorkedReturnError,
        match=rf"bad\.yaml: inputs\.ex/dependants\[1\]: unknown keys \['{key}'\]",
    ):
        WorkedReturn.load(path, records)


@pytest.mark.parametrize(
    ("amount", "problem"),
    [
        ('"lots"', "is not a decimal"),
        ('"NaN"', "is not a decimal"),
        ("5000.50", "must be a string"),  # unquoted: YAML would make it a float
    ],
)
def test_a_non_decimal_record_amount_names_the_file_item_and_field(
    tmp_path: Path, records: ArtifactRegistry, amount: str, problem: str
) -> None:
    path = write(tmp_path, with_section("inputs", DEPENDANTS.replace('"5000.50"', amount)))

    with pytest.raises(
        WorkedReturnError,
        match=rf"bad\.yaml: inputs\.ex/dependants\[1\]\.ex/dependant_net_income {problem}",
    ):
        WorkedReturn.load(path, records)


@pytest.mark.parametrize(
    ("count", "problem"),
    [
        ("6", "must be a string, got int"),  # unquoted: YAML would read it itself
        ('"06"', "is not a count: '06'"),
        ('"6.0"', "is not a count: '6.0'"),
        ('"-1"', "is not a count: '-1'"),
    ],
)
def test_a_record_count_that_is_not_a_digit_string_names_the_file_item_and_field(
    tmp_path: Path, records: ArtifactRegistry, count: str, problem: str
) -> None:
    path = write(tmp_path, with_section("inputs", DEPENDANTS.replace('"6"', count)))

    with pytest.raises(
        WorkedReturnError,
        match=rf"bad\.yaml: inputs\.ex/dependants\[1\]\.ex/months_resident {problem}",
    ):
        WorkedReturn.load(path, records)


def test_a_negative_record_amount_fails_at_load_naming_the_item_and_field(
    tmp_path: Path, records: ArtifactRegistry
) -> None:
    # Like a negative scalar input, the value type's own check refuses it, unwrapped.
    path = write(tmp_path, with_section("inputs", DEPENDANTS.replace('"5000.50"', '"-1"')))

    with pytest.raises(
        NegativeArtifactError, match=r"item 2: ex/dependant_net_income cannot be negative"
    ):
        WorkedReturn.load(path, records)


def test_a_record_list_under_expected_names_the_file_and_key(
    tmp_path: Path, records: ArtifactRegistry
) -> None:
    # Record lists are what a return starts from, never a line it expects (unlike counts).
    text = VALID.replace('  ca/federal_basic_tax: "20146.25"\n', "  ex/dependants: []\n").replace(
        'inputs:\n  ca/taxable_income: "115000"\n', DEPENDANTS
    )
    path = write(tmp_path, text)

    with pytest.raises(
        WorkedReturnError, match=r"bad\.yaml: expected\.ex/dependants: .*not an amount or a count"
    ):
        WorkedReturn.load(path, records)


# --- digits: a number the form asks for as a fixed count of digits, as quoted text -------------
#
# The made-up `ex/business_number` (the `digits` fixture) is a digits kind of nine digits, as a
# carried entry is listed under `inputs`.


def with_business_number(value: str) -> str:
    """`VALID` whose only input is the made-up business number spelled `value`."""
    return with_section("inputs", f"inputs:\n  ex/business_number: {value}\n")


@pytest.mark.parametrize("text", ["123456789", "012345678", "000000000"])
def test_a_digits_kind_takes_its_digits_as_quoted_text_as_entered(
    tmp_path: Path, digits: ArtifactRegistry, text: str
) -> None:
    path = write(tmp_path, with_business_number(f'"{text}"'), "ok.yaml")
    kind = digits.kind("ex/business_number")

    worked = WorkedReturn.load(path, digits)

    assert worked.inputs == (Artifact(kind, text),)
    assert type(worked.inputs[0].value) is str


def test_a_digits_kind_takes_the_empty_text_for_a_box_left_blank(
    tmp_path: Path, digits: ArtifactRegistry
) -> None:
    path = write(tmp_path, with_business_number('""'), "ok.yaml")

    worked = WorkedReturn.load(path, digits)

    assert worked.inputs == (Artifact(digits.kind("ex/business_number"), ""),)


def test_digits_load_beside_a_count_and_keep_the_files_order(
    tmp_path: Path, digits: ArtifactRegistry
) -> None:
    # A yes or no answer stays a count (0 or 1); only the number is text.
    text = with_section(
        "inputs",
        'inputs:\n  ex/partnership_member: "1"\n  ex/business_number: "123456789"\n',
    )

    worked = WorkedReturn.load(write(tmp_path, text, "ok.yaml"), digits)

    assert worked.inputs == (
        Artifact(digits.kind("ex/partnership_member"), 1),
        Artifact(digits.kind("ex/business_number"), "123456789"),
    )


@pytest.mark.parametrize(
    ("value", "got"),
    [
        # Unquoted, YAML reads these before the loader sees them, so digits must be quoted.
        ("123456789", "int"),
        ("1_234_567", "int"),
        ("12345.678", "float"),
        ("true", "bool"),
        ("", "NoneType"),  # an empty box is `""`, never a missing value
        ("[]", "list"),
    ],
)
def test_digits_that_are_not_quoted_text_name_the_file_and_key(
    tmp_path: Path, digits: ArtifactRegistry, value: str, got: str
) -> None:
    path = write(tmp_path, with_business_number(value))

    with pytest.raises(
        WorkedReturnError,
        match=rf"bad\.yaml: inputs\.ex/business_number must be a string, got {got}",
    ):
        WorkedReturn.load(path, digits)


@pytest.mark.parametrize("text", ["12345678", "1234567890", "123 456 789", "12345678a", " "])
def test_text_a_digits_kind_refuses_fails_at_load_naming_the_kind(
    tmp_path: Path, digits: ArtifactRegistry, text: str
) -> None:
    # Like a negative amount, the kind's own check refuses it, unwrapped.
    path = write(tmp_path, with_business_number(f'"{text}"'))

    with pytest.raises(
        InvalidTextError, match=rf"ex/business_number.*9 digits.*{re.escape(repr(text))}"
    ):
        WorkedReturn.load(path, digits)


def test_digits_under_expected_are_read_as_entered(
    tmp_path: Path, digits: ArtifactRegistry
) -> None:
    # A carried entry is listed as an input and as an output, so a return expects it back.
    text = with_business_number('"012345678"').replace(
        'expected:\n  ca/federal_basic_tax: "20146.25"\n',
        'expected:\n  ca/federal_basic_tax: "20146.25"\n  ex/business_number: "012345678"\n',
    )

    worked = WorkedReturn.load(write(tmp_path, text, "ok.yaml"), digits)

    assert worked.expected[1] == Artifact(digits.kind("ex/business_number"), "012345678")


def test_digits_under_expected_that_are_not_quoted_text_name_the_file_and_key(
    tmp_path: Path, digits: ArtifactRegistry
) -> None:
    text = with_business_number('"123456789"').replace(
        'expected:\n  ca/federal_basic_tax: "20146.25"\n',
        'expected:\n  ca/federal_basic_tax: "20146.25"\n  ex/business_number: 123456789\n',
    )

    with pytest.raises(
        WorkedReturnError,
        match=r"bad\.yaml: expected\.ex/business_number must be a string, got int",
    ):
        WorkedReturn.load(write(tmp_path, text), digits)
