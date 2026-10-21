"""Registered and money kinds of the federal catalog family `alternative_minimum_tax`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactKind, ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_FILM_PROPERTY_INCOME_BEFORE_CCA,
    AMT_LIMITED_PARTNER_CARRYING_CHARGES,
    AMT_PART_1_SUBTOTAL,
    AMT_RENTAL_PROPERTY_ADJUSTMENT,
    AMT_RENTAL_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_RENTAL_PROPERTY_INCOME_BEFORE_CCA,
    AMT_TAX_SHELTER_ADJUSTMENTS,
    AMT_TAX_SHELTER_DEDUCTIBLE_AMOUNTS,
    AMT_TAX_SHELTER_LOSSES,
)

PART_1_KINDS: tuple[ArtifactKind[Decimal], ...] = (
    AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_FILM_PROPERTY_INCOME_BEFORE_CCA,
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_RENTAL_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_RENTAL_PROPERTY_INCOME_BEFORE_CCA,
    AMT_RENTAL_PROPERTY_ADJUSTMENT,
    AMT_TAX_SHELTER_LOSSES,
    AMT_TAX_SHELTER_DEDUCTIBLE_AMOUNTS,
    AMT_LIMITED_PARTNER_CARRYING_CHARGES,
    AMT_TAX_SHELTER_ADJUSTMENTS,
    AMT_PART_1_SUBTOTAL,
)


def test_the_alternative_minimum_tax_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert (
        registry.get("ca/amt_film_property_cca_and_carrying_charges")
        is AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES
    )
    assert (
        registry.get("ca/amt_film_property_income_before_cca")
        is AMT_FILM_PROPERTY_INCOME_BEFORE_CCA
    )
    assert registry.get("ca/amt_film_property_adjustment") is AMT_FILM_PROPERTY_ADJUSTMENT
    assert (
        registry.get("ca/amt_rental_property_cca_and_carrying_charges")
        is AMT_RENTAL_PROPERTY_CCA_AND_CARRYING_CHARGES
    )
    assert (
        registry.get("ca/amt_rental_property_income_before_cca")
        is AMT_RENTAL_PROPERTY_INCOME_BEFORE_CCA
    )
    assert registry.get("ca/amt_rental_property_adjustment") is AMT_RENTAL_PROPERTY_ADJUSTMENT
    assert registry.get("ca/amt_tax_shelter_losses") is AMT_TAX_SHELTER_LOSSES
    assert (
        registry.get("ca/amt_tax_shelter_deductible_amounts") is AMT_TAX_SHELTER_DEDUCTIBLE_AMOUNTS
    )
    assert (
        registry.get("ca/amt_limited_partner_carrying_charges")
        is AMT_LIMITED_PARTNER_CARRYING_CHARGES
    )
    assert registry.get("ca/amt_tax_shelter_adjustments") is AMT_TAX_SHELTER_ADJUSTMENTS
    assert registry.get("ca/amt_part_1_subtotal") is AMT_PART_1_SUBTOTAL


def test_the_alternative_minimum_tax_kinds_are_money() -> None:
    for kind in PART_1_KINDS:
        assert kind.value_type is Decimal, kind.identifier
