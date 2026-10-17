"""Artifacts: the named intermediate values that capabilities consume and produce.

Ordering in the engine is expressed through artifacts, never through direct
capability-to-capability dependencies (design.md §2). An `ArtifactKind[V]` names a kind of
artifact by a namespaced identifier such as `ex/taxable_income` and states the type of its
values; an `Artifact[V]` is one value of a kind, produced in one computation. Each package
declares its kinds through one `ArtifactCatalog`, which only records them; the composition root
registers each catalog explicitly with `ArtifactRegistry.register_catalog`. Names come from the
jurisdiction's own law or return, never from another system's.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Generic, TypeVar

from app.domain.errors import DuplicateRegistrationError, InvalidRegistrationError
from app.domain.registry import Namespace, Registry

# Invariant on purpose. PEP 695 syntax would infer covariance from `value_type: type[V]`, and
# mypy would then accept, say, an ArtifactKind[int] wired where an ArtifactKind[Decimal] is
# expected.
V = TypeVar("V")


@dataclass(frozen=True)
class ArtifactKind(Generic[V]):  # noqa: UP046  (invariant V, see above)
    """A kind of artifact, named by its identifier `<namespace>/<local id>`, and its value type.

    Built directly it is unregistered; packages declare theirs through an `ArtifactCatalog`.
    """

    identifier: str
    value_type: type[V]

    def __post_init__(self) -> None:
        namespace, _, local_id = self.identifier.partition("/")
        try:
            Namespace(namespace).identifier(local_id)
        except InvalidRegistrationError as exc:
            raise InvalidRegistrationError(
                f"invalid artifact kind identifier {self.identifier!r}: {exc}"
            ) from None
        if not isinstance(self.value_type, type):
            raise TypeError(f"value_type must be a type, got {self.value_type!r}")

    @property
    def label(self) -> str:
        """The local part of the identifier, for traces and messages."""
        return self.identifier.partition("/")[2]


type Money = ArtifactKind[Decimal]
"""A money kind: its artifacts are exact `Decimal`s in the jurisdiction's currency."""


@dataclass(frozen=True)
class Artifact[T]:
    """One value of an artifact kind in one computation, checked against the kind's value type."""

    kind: ArtifactKind[T]
    value: T

    def __post_init__(self) -> None:
        if not isinstance(self.value, self.kind.value_type):
            raise TypeError(
                f"{self.kind.label} must be a {self.kind.value_type.__name__}, "
                f"got {type(self.value).__name__}"
            )


class ArtifactRegistry(Registry[object]):
    """The registry of artifact kinds packages declare, by full identifier (`ex/taxable_income`).

    Register through `register_catalog`. Items are stored as `object` because `ArtifactKind` is
    invariant: an `ArtifactKind[Decimal]` is not an `ArtifactKind[object]`.
    """

    def register_catalog(self, catalog: ArtifactCatalog) -> None:
        """Register every kind `catalog` declared under its identifier.

        A kind already registered as that same object is skipped, so registering one catalog
        twice is idempotent; an identifier taken by anything else is an error, and then nothing
        from the catalog is registered.
        """
        pending = [kind for kind in catalog.kinds if self.identifier_of(kind) != kind.identifier]
        for kind in pending:
            if kind.identifier in self.identifiers():
                raise DuplicateRegistrationError(f"{kind.identifier!r} is already registered")
        for kind in pending:
            self.register(kind.identifier, kind)


class ArtifactCatalog:
    """One package's artifact kinds: builds each kind in the package's namespace and records it.

    Each package creates one, e.g. `ArtifactCatalog(Namespace("ca"))`. Declaring registers
    nothing; `ArtifactRegistry.register_catalog` does.
    """

    def __init__(self, namespace: Namespace) -> None:
        self._namespace = namespace
        self._kinds: dict[str, ArtifactKind[Any]] = {}

    @property
    def namespace(self) -> Namespace:
        """The namespace every kind of this catalog is declared in."""
        return self._namespace

    @property
    def kinds(self) -> tuple[ArtifactKind[Any], ...]:
        """Every kind declared so far, in declaration order."""
        return tuple(self._kinds.values())

    def declare[T](self, local_id: str, value_type: type[T]) -> ArtifactKind[T]:
        """Declare the kind `<namespace>/<local_id>` with values of `value_type` and record it.

        A local id this catalog already declared is an error.
        """
        kind = ArtifactKind(self._namespace.identifier(local_id), value_type)
        if kind.identifier in self._kinds:
            raise DuplicateRegistrationError(
                f"{kind.identifier!r} is already declared in this catalog"
            )
        self._kinds[kind.identifier] = kind
        return kind
