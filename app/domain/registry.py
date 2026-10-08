"""Registries: where packages register the pieces they contribute (capabilities, parsers, ...).

The core never lists contributed pieces. A package declares its namespace once, as
`NAMESPACE = "..."` in its `__init__.py`, and registers each piece under a local id; the full
identifier is `<namespace>/<local id>`. The registry never discovers or imports anything: a
registration happens when the registering module is imported. A registration made while a
package without `NAMESPACE` is still being imported fails: declare `NAMESPACE` at the top of its
`__init__.py` (repeat the parent's to inherit it), or do not import registering modules from
that `__init__.py`.
"""

from __future__ import annotations

import re
import sys
from typing import ClassVar, Self

from app.domain.errors import (
    DuplicateRegistrationError,
    InvalidRegistrationError,
    UnknownRegistrationError,
)

_NAMESPACE = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
_LOCAL_ID = re.compile(r"[a-z][a-z0-9]*(_[a-z0-9]+)*")


class Registry[T]:
    """A store of items of one kind under unique keys; subclasses decide how items are keyed.

    Construct one directly for a private registry, or use `shared()` for the application-wide one.
    """

    _shared: ClassVar[dict[type[object], object]] = {}

    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    @classmethod
    def shared(cls) -> Self:
        """The application-wide instance of this registry class, created on first use."""
        instance = Registry._shared.get(cls)
        if not isinstance(instance, cls):
            instance = cls()
            Registry._shared[cls] = instance
        return instance

    def _add(self, key: str, item: T) -> None:
        if key in self._items:
            raise DuplicateRegistrationError(f"{key!r} is already registered")
        self._items[key] = item

    def _find(self, key: str) -> T:
        try:
            return self._items[key]
        except KeyError:
            raise UnknownRegistrationError(f"nothing is registered as {key!r}") from None


class NamespacedRegistry[T](Registry[T]):
    """A registry keyed by namespaced identifiers such as `core/progressive_tax`.

    The namespace is the one declared by the nearest package above the registered item's module.
    """

    def register(self, local_id: str, item: T) -> str:
        """Register `item` under `<namespace>/<local_id>` and return that full identifier."""
        if not _LOCAL_ID.fullmatch(local_id):
            raise InvalidRegistrationError(
                f"invalid local id {local_id!r}: expected snake_case, e.g. 'progressive_tax'"
            )
        identifier = f"{self._namespace_of(item)}/{local_id}"
        self._add(identifier, item)
        return identifier

    def get(self, identifier: str) -> T:
        """The item registered under the full identifier `identifier`."""
        return self._find(identifier)

    @staticmethod
    def _namespace_of(item: object) -> str:
        module = getattr(item, "__module__", None)
        if not isinstance(module, str):
            raise InvalidRegistrationError(f"cannot tell which module {item!r} comes from")
        parts = module.split(".")
        for end in range(len(parts), 0, -1):
            name = ".".join(parts[:end])
            package = sys.modules.get(name)
            is_package = package is not None and hasattr(package, "__path__")
            namespace = getattr(package, "NAMESPACE", None) if is_package else None
            if namespace is None and is_package and NamespacedRegistry._initializing(package):
                raise InvalidRegistrationError(
                    f"package {name} is still being imported and has no NAMESPACE: declare "
                    "NAMESPACE at the top of its __init__.py (repeat the parent's to inherit it), "
                    "or do not import registering modules from that __init__.py"
                )
            if namespace is not None:
                if not isinstance(namespace, str) or not _NAMESPACE.fullmatch(namespace):
                    raise InvalidRegistrationError(
                        f"invalid NAMESPACE {namespace!r} in {name}: expected lowercase letters "
                        "and digits with single hyphens, e.g. 'ca-on'"
                    )
                return namespace
        raise InvalidRegistrationError(
            f"no package above {module} declares a NAMESPACE; "
            "declare one as NAMESPACE = '...' in the package's __init__.py"
        )

    @staticmethod
    def _initializing(package: object) -> bool:
        # `__spec__._initializing` is a private CPython attribute, set while a module's code
        # runs; where it is absent the check is skipped.
        return bool(getattr(getattr(package, "__spec__", None), "_initializing", False))
