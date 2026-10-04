"""Strict YAML reading shared by the YAML adapters.

`YamlNode` wraps a parsed value with its location in the document, so every
check names exactly where it failed ("brackets[0].rate is not a decimal").
Unknown, missing and duplicate keys and wrongly typed values are rejected,
never coerced or ignored. Shape problems raise YamlShapeError; each adapter
re-raises them as its own domain error with the file named.
"""

from __future__ import annotations

from collections.abc import Hashable
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

import yaml
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode


class YamlShapeError(ValueError):
    """A YAML document does not have the expected shape."""


class _StrictLoader(yaml.SafeLoader):
    """SafeLoader that rejects duplicate mapping keys instead of keeping the last one."""

    def construct_mapping(self, node: MappingNode, deep: bool = False) -> dict[Hashable, Any]:
        seen: set[Any] = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in seen:
                raise ConstructorError(None, None, f"duplicate key {key!r}", key_node.start_mark)
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


class YamlNode:
    """A parsed YAML value and where it sits in its document.

    The root is labelled (e.g. "manifest") for its own errors; locations below
    it start fresh, so a top-level field is "version", not "manifest.version".
    """

    def __init__(self, value: object, where: str, *, is_root: bool = False) -> None:
        self._value = value
        self._where = where
        self._is_root = is_root

    @classmethod
    def root(cls, value: object, label: str) -> YamlNode:
        return cls(value, label, is_root=True)

    @classmethod
    def load(cls, path: Path, label: str) -> YamlNode:
        """Parse `path` strictly; raises OSError or yaml.YAMLError."""
        return cls.root(yaml.load(path.read_text(encoding="utf-8"), Loader=_StrictLoader), label)

    @property
    def value(self) -> object:
        return self._value

    @property
    def where(self) -> str:
        return self._where

    def require_mapping(self, keys: frozenset[str]) -> YamlNode:
        """This node, checked to be a mapping with exactly `keys`."""
        mapping = self._mapping()
        unknown = set(mapping) - keys
        if unknown:
            raise YamlShapeError(f"{self._where}: unknown keys {sorted(map(str, unknown))}")
        missing = keys - set(mapping)
        if missing:
            raise YamlShapeError(f"{self._where}: missing keys {sorted(missing)}")
        return self

    def field(self, key: str) -> YamlNode:
        mapping = self._mapping()
        if key not in mapping:
            raise YamlShapeError(f"{self._where}: missing key {key!r}")
        where = key if self._is_root else f"{self._where}.{key}"
        return YamlNode(mapping[key], where)

    def items(self) -> list[YamlNode]:
        if not isinstance(self._value, list):
            raise YamlShapeError(f"{self._where} must be a list")
        return [YamlNode(item, f"{self._where}[{i}]") for i, item in enumerate(self._value)]

    def require_string(self) -> str:
        if not isinstance(self._value, str):
            raise YamlShapeError(f"{self._where} must be a string, got {self._type_name()}")
        return self._value

    def require_integer(self) -> int:
        # bool is an int subclass; `version: yes` must not become 1.
        if not isinstance(self._value, int) or isinstance(self._value, bool):
            raise YamlShapeError(f"{self._where} must be an integer, got {self._type_name()}")
        return self._value

    def parse_decimal(self) -> Decimal:
        """A decimal written as a YAML string, so it never passes through float."""
        text = self.require_string()
        try:
            result = Decimal(text)
        except InvalidOperation:
            raise YamlShapeError(f"{self._where} is not a decimal: {text!r}") from None
        if not result.is_finite():
            raise YamlShapeError(f"{self._where} is not a decimal: {text!r}")
        return result

    def _mapping(self) -> dict[object, object]:
        if not isinstance(self._value, dict):
            raise YamlShapeError(f"{self._where} must be a mapping")
        return self._value

    def _type_name(self) -> str:
        return type(self._value).__name__
