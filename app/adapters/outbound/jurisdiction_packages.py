"""Finds where each jurisdiction package keeps its data: namespace -> package directory.

A jurisdiction package declares only `NAMESPACE = "..."` in its `__init__.py`; its directory is
the one holding that file, with `manifests/` and `parameters/` inside. The YAML sources read
under these directories.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import Path
from types import MappingProxyType, ModuleType

from app.domain.errors import DuplicateRegistrationError, InvalidRegistrationError
from app.domain.registry import Namespace


class JurisdictionPackages:
    """The jurisdiction packages the application uses, keyed by the namespace each declares.

    A package without a valid `NAMESPACE`, or two packages declaring the same one, is rejected.
    """

    def __init__(self, packages: Iterable[ModuleType]) -> None:
        roots: dict[Namespace, Path] = {}
        owners: dict[Namespace, str] = {}
        for package in packages:
            namespace = self._namespace(package)
            if namespace in owners:
                raise DuplicateRegistrationError(
                    f"namespace {namespace.name!r} is declared by both {owners[namespace]} "
                    f"and {package.__name__}"
                )
            owners[namespace] = package.__name__
            roots[namespace] = self._directory(package)
        self._roots: Mapping[Namespace, Path] = MappingProxyType(roots)

    def roots(self) -> Mapping[Namespace, Path]:
        """Each package's namespace mapped to its package directory."""
        return self._roots

    @staticmethod
    def _namespace(package: ModuleType) -> Namespace:
        declared = getattr(package, "NAMESPACE", None)
        if not isinstance(declared, str):
            raise InvalidRegistrationError(
                f"jurisdiction package {package.__name__} must declare NAMESPACE = '...' as a "
                f"string in its __init__.py, got {declared!r}"
            )
        try:
            return Namespace(declared)
        except InvalidRegistrationError as exc:
            raise InvalidRegistrationError(f"{package.__name__}: {exc}") from None

    @staticmethod
    def _directory(package: ModuleType) -> Path:
        file = getattr(package, "__file__", None)
        if not isinstance(file, str):
            raise InvalidRegistrationError(
                f"jurisdiction package {package.__name__} has no __file__ to locate its data"
            )
        return Path(file).parent
