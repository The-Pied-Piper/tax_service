"""Unit tests for the composition root's wiring of services that have no HTTP route yet."""

from __future__ import annotations

from app.application.services.tax_computation import TaxComputationService
from app.domain.jurisdiction_code import JurisdictionCode
from app.main import build_tax_computation


def test_builds_a_tax_computation_over_the_jurisdiction_packages_and_shared_registries() -> None:
    computation = build_tax_computation()

    assert isinstance(computation, TaxComputationService)
    assert len(computation.compose(JurisdictionCode("CA-ON"), 2025).order) == 4
