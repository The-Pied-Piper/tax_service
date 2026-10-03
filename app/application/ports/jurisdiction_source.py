"""Outbound port: where jurisdictions and their manifests come from."""

from __future__ import annotations

from typing import Protocol

from app.domain.jurisdiction import Jurisdiction


class JurisdictionSource(Protocol):
    def get_jurisdiction(self, code: str) -> Jurisdiction:
        """The jurisdiction with every manifest stored for it.

        Raise NotFoundError if none are stored, InvalidManifestError if any cannot be read.
        """
        ...
