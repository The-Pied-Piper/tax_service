"""Unit tests for YamlNode: a parsed YAML value plus its location, for strict reading."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest
import yaml

from app.adapters.outbound.yaml_support import YamlNode, YamlShapeError


def node(value: object) -> YamlNode:
    return YamlNode.root(value, "document")


# --- loading -------------------------------------------------------------------


def test_load_parses_a_file(tmp_path: Path) -> None:
    path = tmp_path / "x.yaml"
    path.write_text("a: 1\n", encoding="utf-8")

    assert YamlNode.load(path, "document").value == {"a": 1}


def test_load_rejects_duplicate_keys(tmp_path: Path) -> None:
    path = tmp_path / "x.yaml"
    path.write_text("a: 1\na: 2\n", encoding="utf-8")

    with pytest.raises(yaml.YAMLError, match="duplicate key 'a'"):
        YamlNode.load(path, "document")


# --- mappings and locations ------------------------------------------------------


def test_require_mapping_accepts_exact_keys() -> None:
    doc = node({"a": 1, "b": 2}).require_mapping(frozenset({"a", "b"}))

    assert doc.field("a").value == 1


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ([1], "document must be a mapping"),
        (None, "document must be a mapping"),
        ({"a": 1, "x": 2}, r"document: unknown keys \['x'\]"),
        ({}, r"document: missing keys \['a'\]"),
    ],
)
def test_require_mapping_rejects(value: object, message: str) -> None:
    with pytest.raises(YamlShapeError, match=message):
        node(value).require_mapping(frozenset({"a"}))


def test_require_mapping_accepts_optional_keys_present_or_absent() -> None:
    keys, optional = frozenset({"a"}), frozenset({"b"})

    assert node({"a": 1, "b": 2}).require_mapping(keys, optional=optional).field("b").value == 2
    assert node({"a": 1}).require_mapping(keys, optional=optional).optional_field("b") is None


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ({"a": 1, "x": 2}, r"document: unknown keys \['x'\]"),
        ({"b": 2}, r"document: missing keys \['a'\]"),
    ],
)
def test_require_mapping_with_optional_keys_rejects(value: object, message: str) -> None:
    with pytest.raises(YamlShapeError, match=message):
        node(value).require_mapping(frozenset({"a"}), optional=frozenset({"b"}))


def test_optional_field_is_the_value_under_a_present_key() -> None:
    found = node({"params": {"a": "x"}}).optional_field("params")

    assert found is not None
    assert found.where == "params"
    assert found.value == {"a": "x"}


def test_optional_field_requires_a_mapping() -> None:
    with pytest.raises(YamlShapeError, match="^document must be a mapping"):
        node([1]).optional_field("a")


def test_string_mapping_reads_strings_to_strings() -> None:
    assert node({"m": {"a": "x", "b": "y"}}).field("m").string_mapping() == {"a": "x", "b": "y"}
    assert node({"m": {}}).field("m").string_mapping() == {}


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ({"a": 7}, r"^m\.a must be a string, got int"),
        ({"a": None}, r"^m\.a must be a string, got NoneType"),
        ({7: "x"}, r"^m: key 7 must be a string, got int"),
        ({"": "x"}, r"^m: keys must not be empty"),
        ({"a": ""}, r"^m\.a must not be empty"),
        (["x"], "^m must be a mapping"),
        (None, "^m must be a mapping"),
    ],
)
def test_string_mapping_rejects(value: object, message: str) -> None:
    with pytest.raises(YamlShapeError, match=message):
        node({"m": value}).field("m").string_mapping()


def test_top_level_fields_are_named_without_the_root_label() -> None:
    with pytest.raises(YamlShapeError, match="^version must be an integer"):
        node({"version": "1"}).field("version").require_integer()


def test_locations_follow_fields_and_items() -> None:
    doc = node({"brackets": [{"rate": "ten"}]})
    rate = doc.field("brackets").items()[0].field("rate")

    assert rate.where == "brackets[0].rate"
    with pytest.raises(YamlShapeError, match=r"^brackets\[0\].rate is not a decimal: 'ten'"):
        rate.parse_decimal()


def test_items_rejects_non_list() -> None:
    with pytest.raises(YamlShapeError, match="^sources must be a list"):
        node({"sources": "x"}).field("sources").items()


def test_field_of_a_missing_key_is_a_shape_error() -> None:
    with pytest.raises(YamlShapeError, match="missing key 'a'"):
        node({}).field("a")


# --- scalars ---------------------------------------------------------------------


def test_require_string() -> None:
    assert node({"a": "x"}).field("a").require_string() == "x"
    with pytest.raises(YamlShapeError, match="^a must be a string, got int"):
        node({"a": 1}).field("a").require_string()


@pytest.mark.parametrize(("value", "got"), [(True, "bool"), ("1", "str"), (1.0, "float")])
def test_require_integer_rejects(value: object, got: str) -> None:
    with pytest.raises(YamlShapeError, match=f"^a must be an integer, got {got}"):
        node({"a": value}).field("a").require_integer()


def test_require_integer_accepts_int() -> None:
    assert node({"a": 7}).field("a").require_integer() == 7


def test_parse_decimal_reads_strings_exactly() -> None:
    assert node({"a": "0.145"}).field("a").parse_decimal() == Decimal("0.145")


@pytest.mark.parametrize(
    ("value", "message"),
    [
        (0.145, "a must be a string, got float"),
        ("abc", "a is not a decimal: 'abc'"),
        ("NaN", "a is not a decimal: 'NaN'"),
        ("Infinity", "a is not a decimal: 'Infinity'"),
    ],
)
def test_parse_decimal_rejects(value: object, message: str) -> None:
    with pytest.raises(YamlShapeError, match=f"^{message}"):
        node({"a": value}).field("a").parse_decimal()


@pytest.mark.parametrize(
    ("value", "number"), [("0", 0), ("3", 3), ("10", 10), ("1000000", 1000000)]
)
def test_parse_whole_number_reads_digit_strings_as_ints(value: str, number: int) -> None:
    parsed = node({"a": value}).field("a").parse_whole_number()

    assert parsed == number
    assert type(parsed) is int


def test_parse_whole_number_reads_more_digits_than_a_machine_word() -> None:
    assert node({"a": "1" + "0" * 30}).field("a").parse_whole_number() == 10**30


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ("-3", r"a is not a whole number: '-3'"),
        ("+3", r"a is not a whole number: '\+3'"),
        ("03", r"a is not a whole number: '03'"),
        ("00", r"a is not a whole number: '00'"),
        (" 3", r"a is not a whole number: ' 3'"),
        ("3 ", r"a is not a whole number: '3 '"),
        ("1_000", r"a is not a whole number: '1_000'"),
        ("3.0", r"a is not a whole number: '3\.0'"),
        ("٣", r"a is not a whole number: '٣'"),  # ARABIC-INDIC DIGIT THREE
        ("３", r"a is not a whole number: '３'"),  # FULLWIDTH DIGIT THREE
        ("", r"a is not a whole number: ''"),
        ("three", r"a is not a whole number: 'three'"),
        (3, "a must be a string, got int"),
        (3.0, "a must be a string, got float"),
        (True, "a must be a string, got bool"),
    ],
)
def test_parse_whole_number_rejects(value: object, message: str) -> None:
    with pytest.raises(YamlShapeError, match=f"^{message}"):
        node({"a": value}).field("a").parse_whole_number()


def test_parse_whole_number_rejects_more_digits_than_int_converts() -> None:
    # 4,301 digits: one more than `int()` converts from text by default.
    with pytest.raises(YamlShapeError, match="^a is not a whole number: '1000"):
        node({"a": "1" + "0" * 4300}).field("a").parse_whole_number()


def test_parse_whole_number_names_the_nodes_location() -> None:
    part = node({"parts": [{"numerator": "-2"}]}).field("parts").items()[0].field("numerator")

    with pytest.raises(YamlShapeError, match=r"^parts\[0\]\.numerator is not a whole number"):
        part.parse_whole_number()
