"""Snapshot of the registered `ca-on/` artifact kind identifiers, as the application registers them.

Identifiers are stored with results and exposed by the API, so changing or removing one is a
breaking change: update this snapshot only on purpose. Declaring a kind in this package's catalog
adds it here; federal kinds are snapshotted in `tests/jurisdictions/ca/`.
"""

from __future__ import annotations

import app.registrations  # noqa: F401  (fills the shared registries, as the app does)
from app.domain.artifact import ArtifactRegistry

REGISTERED: frozenset[str] = frozenset()


def test_registered_identifiers_snapshot() -> None:
    identifiers = ArtifactRegistry.shared().identifiers()

    assert {i for i in identifiers if i.startswith("ca-on/")} == REGISTERED
