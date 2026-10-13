"""Artifacts: the named intermediate values that capabilities consume and produce.

Ordering in the engine is expressed through artifacts, never through direct
capability-to-capability dependencies (design.md §2). An `ArtifactKind[V]` names a kind of
artifact by a namespaced identifier such as `ca/taxable_income` and states the type of its
values; an `Artifact[V]` is one value of a kind, produced in one computation. Each package
declares its kinds through one `ArtifactCatalog`, which registers them; names come from the
jurisdiction's own law or return, never from another system's.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Generic, TypeVar

from app.domain.errors import InvalidRegistrationError
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
    """The registry of artifact kinds packages declare, by full identifier (`ca/taxable_income`).

    Register through an `ArtifactCatalog`. Items are stored as `object` because `ArtifactKind` is
    invariant: an `ArtifactKind[Decimal]` is not an `ArtifactKind[object]`.
    """


class ArtifactCatalog:
    """One package's artifact kinds: builds each kind in the package's namespace and registers it.

    Each package creates one, e.g. `ArtifactCatalog(Namespace("ca"))`.
    """

    def __init__(self, namespace: Namespace) -> None:
        self._namespace = namespace

    def declare[T](self, local_id: str, value_type: type[T]) -> ArtifactKind[T]:
        """Declare the kind `<namespace>/<local_id>` with values of `value_type` and register it.

        It goes in the shared ArtifactRegistry; an identifier already taken is an error.
        """
        kind = ArtifactKind(self._namespace.identifier(local_id), value_type)
        ArtifactRegistry.shared().register(kind.identifier, kind)
        return kind
