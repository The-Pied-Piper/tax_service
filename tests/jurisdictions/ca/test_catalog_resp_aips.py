"""Registered and money kinds of the federal catalog family `resp_aips`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    ADVANCED_CANADA_WORKERS_BENEFIT,
    RESP_AIPS_ADDITIONAL_TAX,
    RESP_AIPS_CONTRIBUTIONS_COUNTED,
    RESP_AIPS_LIFETIME_LIMIT,
    RESP_AIPS_LIMIT_REMAINING,
    RESP_AIPS_PART_A_APPLIES,
    RESP_AIPS_PART_A_TAX,
    RESP_AIPS_PART_B_TAX,
    RESP_AIPS_RECEIVED_PART_A,
    RESP_AIPS_RECEIVED_PART_B,
    RESP_AIPS_REDUCTION,
    RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS,
    RESP_AIPS_RRSP_CONTRIBUTIONS,
    RESP_AIPS_SUBJECT_TO_TAX,
)


def test_the_resp_aips_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/advanced_canada_workers_benefit") is ADVANCED_CANADA_WORKERS_BENEFIT
    assert registry.get("ca/resp_aips_received_part_a") is RESP_AIPS_RECEIVED_PART_A
    assert registry.get("ca/resp_aips_rrsp_contributions") is RESP_AIPS_RRSP_CONTRIBUTIONS
    assert (
        registry.get("ca/resp_aips_reduction_used_in_previous_years")
        is RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS
    )
    assert registry.get("ca/resp_aips_received_part_b") is RESP_AIPS_RECEIVED_PART_B
    assert registry.get("ca/resp_aips_part_a_applies") is RESP_AIPS_PART_A_APPLIES
    assert registry.get("ca/resp_aips_contributions_counted") is RESP_AIPS_CONTRIBUTIONS_COUNTED
    assert registry.get("ca/resp_aips_lifetime_limit") is RESP_AIPS_LIFETIME_LIMIT
    assert registry.get("ca/resp_aips_limit_remaining") is RESP_AIPS_LIMIT_REMAINING
    assert registry.get("ca/resp_aips_reduction") is RESP_AIPS_REDUCTION
    assert registry.get("ca/resp_aips_subject_to_tax") is RESP_AIPS_SUBJECT_TO_TAX
    assert registry.get("ca/resp_aips_part_a_tax") is RESP_AIPS_PART_A_TAX
    assert registry.get("ca/resp_aips_part_b_tax") is RESP_AIPS_PART_B_TAX
    assert registry.get("ca/resp_aips_additional_tax") is RESP_AIPS_ADDITIONAL_TAX


def test_the_resp_aips_kinds_are_money() -> None:
    for kind in (
        ADVANCED_CANADA_WORKERS_BENEFIT,
        RESP_AIPS_RECEIVED_PART_A,
        RESP_AIPS_RRSP_CONTRIBUTIONS,
        RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS,
        RESP_AIPS_RECEIVED_PART_B,
        RESP_AIPS_CONTRIBUTIONS_COUNTED,
        RESP_AIPS_LIFETIME_LIMIT,
        RESP_AIPS_LIMIT_REMAINING,
        RESP_AIPS_REDUCTION,
        RESP_AIPS_SUBJECT_TO_TAX,
        RESP_AIPS_PART_A_TAX,
        RESP_AIPS_PART_B_TAX,
        RESP_AIPS_ADDITIONAL_TAX,
    ):
        assert kind.value_type is Decimal, kind.identifier
