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
