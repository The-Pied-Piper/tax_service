"""Fixtures for the federal Canada tests."""

from __future__ import annotations

import pytest

from app.domain.artifact import ArtifactRegistry
from app.registrations import JURISDICTIONS


@pytest.fixture
def registry() -> ArtifactRegistry:
    registry = ArtifactRegistry()
    JURISDICTIONS.register(registry)
    return registry
