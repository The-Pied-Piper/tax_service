"""Snapshot of the registered `ca-on/` artifact kind identifiers, as the application registers them.

Identifiers are stored with results and exposed by the API, so changing or removing one is a
breaking change: update this snapshot only on purpose. Declaring a kind in this package's catalog
adds it here; federal kinds are snapshotted in `tests/jurisdictions/ca/`.
"""

from __future__ import annotations

from decimal import Decimal

import app.jurisdictions.ca_on
import app.registrations  # noqa: F401  (fills the shared registries, as the app does)
from app.domain.artifact import ArtifactKind, ArtifactRegistry

REGISTERED = frozenset({"ca-on/ontario_basic_tax", "ca-on/ontario_tax_after_credits"})


def test_registered_identifiers_snapshot() -> None:
    identifiers = ArtifactRegistry.shared().identifiers()

    assert {i for i in identifiers if i.startswith("ca-on/")} == REGISTERED


def test_every_registered_kind_is_money_in_the_package_namespace() -> None:
    registry = ArtifactRegistry.shared()

    for identifier in REGISTERED:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.identifier.startswith(f"{app.jurisdictions.ca_on.NAMESPACE}/")
        assert kind.value_type is Decimal, identifier
