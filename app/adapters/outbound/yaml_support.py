"""Strict YAML reading shared by the YAML adapters.

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


def load(path: Path) -> object:
    """Parse `path`; raises OSError or yaml.YAMLError."""
    return yaml.load(path.read_text(encoding="utf-8"), Loader=_StrictLoader)


def mapping(value: object, where: str, keys: frozenset[str]) -> dict[str, object]:
    if not isinstance(value, dict):
        raise YamlShapeError(f"{where} must be a mapping")
    unknown = set(value) - keys
    if unknown:
        raise YamlShapeError(f"{where}: unknown keys {sorted(map(str, unknown))}")
    missing = keys - set(value)
    if missing:
        raise YamlShapeError(f"{where}: missing keys {sorted(missing)}")
    return value


def string(value: object, where: str) -> str:
    if not isinstance(value, str):
        raise YamlShapeError(f"{where} must be a string, got {type(value).__name__}")
    return value


def integer(value: object, where: str) -> int:
    # bool is an int subclass; `version: yes` must not become 1.
    if not isinstance(value, int) or isinstance(value, bool):
        raise YamlShapeError(f"{where} must be an integer, got {type(value).__name__}")
    return value


def decimal(value: object, where: str) -> Decimal:
    """A decimal written as a YAML string, so YAML never turns it into a float."""
    text = string(value, where)
    try:
        result = Decimal(text)
    except InvalidOperation:
        raise YamlShapeError(f"{where} is not a decimal: {text!r}") from None
    if not result.is_finite():
        raise YamlShapeError(f"{where} is not a decimal: {text!r}")
    return result


def sequence(value: object, where: str) -> list[object]:
    if not isinstance(value, list):
        raise YamlShapeError(f"{where} must be a list")
    return value
