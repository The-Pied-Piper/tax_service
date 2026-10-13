"""The Ontario artifact catalog. It declares nothing yet: Ontario kinds are added as capabilities
need them, and federal kinds come from `app.jurisdictions.ca.catalog`."""

from __future__ import annotations

from app.domain.artifact import ArtifactCatalog
from app.domain.registry import Namespace
from app.jurisdictions.ca_on import NAMESPACE

CATALOG = ArtifactCatalog(Namespace(NAMESPACE))
