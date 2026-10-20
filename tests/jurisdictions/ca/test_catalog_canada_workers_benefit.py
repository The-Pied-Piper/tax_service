"""Registered and money kinds of the federal catalog family `canada_workers_benefit`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    ADJUSTED_FAMILY_NET_INCOME,
    CANADA_WORKERS_BENEFIT,
    CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
    CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
    CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
    CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
    CWB_ELIGIBLE_DEPENDANTS,
    CWB_REDUCTION_WITH_DEPENDANT,
    CWB_REDUCTION_WITHOUT_DEPENDANT,
    WORKING_INCOME,
)


def test_the_canada_workers_benefit_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert registry.get("ca/cwb_eligible_dependants") is CWB_ELIGIBLE_DEPENDANTS
    assert registry.get("ca/working_income") is WORKING_INCOME
    assert registry.get("ca/adjusted_family_net_income") is ADJUSTED_FAMILY_NET_INCOME
    assert (
        registry.get("ca/cwb_before_reduction_without_dependant")
        is CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT
    )
    assert registry.get("ca/cwb_reduction_without_dependant") is CWB_REDUCTION_WITHOUT_DEPENDANT
    assert (
        registry.get("ca/canada_workers_benefit_without_dependant")
        is CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT
    )
    assert (
        registry.get("ca/cwb_before_reduction_with_dependant")
        is CWB_BEFORE_REDUCTION_WITH_DEPENDANT
    )
    assert registry.get("ca/cwb_reduction_with_dependant") is CWB_REDUCTION_WITH_DEPENDANT
    assert (
        registry.get("ca/canada_workers_benefit_with_dependant")
        is CANADA_WORKERS_BENEFIT_WITH_DEPENDANT
    )
    assert registry.get("ca/canada_workers_benefit") is CANADA_WORKERS_BENEFIT


def test_the_canada_workers_benefit_kinds_are_money() -> None:
    for kind in (
        WORKING_INCOME,
        ADJUSTED_FAMILY_NET_INCOME,
        CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
        CWB_REDUCTION_WITHOUT_DEPENDANT,
        CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
        CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
        CWB_REDUCTION_WITH_DEPENDANT,
        CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
        CANADA_WORKERS_BENEFIT,
    ):
        assert kind.value_type is Decimal, kind.identifier
