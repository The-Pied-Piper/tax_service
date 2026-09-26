"""A jurisdiction and every manifest version stored for it (design.md §4).

Plain attributes for now; resolution and the version-history rules come later.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.manifest import Manifest


@dataclass(frozen=True, slots=True)
class Jurisdiction:
    code: str
    manifests: tuple[Manifest, ...]
