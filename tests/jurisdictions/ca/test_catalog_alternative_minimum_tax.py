"""Registered and money kinds of the federal catalog family `alternative_minimum_tax`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactKind, ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    AMT_CAPITAL_GAINS_ADJUSTMENTS,
    AMT_CLASS_43_1_INCOME,
    AMT_FILM_PROPERTY_ADJUSTMENT,
    AMT_FILM_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_FILM_PROPERTY_INCOME_BEFORE_CCA,
    AMT_GRADUATED_RATE_ESTATE_CAPITAL_GAINS,
    AMT_LIMITED_PARTNER_CARRYING_CHARGES,
    AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS,
    AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
    AMT_PART_1_SUBTOTAL,
    AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
    AMT_PUBLICLY_LISTED_GIFTS_NET,
    AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231,
    AMT_PUBLICLY_LISTED_GIFTS_TOTAL,
    AMT_RENTAL_PROPERTY_ADJUSTMENT,
    AMT_RENTAL_PROPERTY_CCA_AND_CARRYING_CHARGES,
    AMT_RENTAL_PROPERTY_INCOME_BEFORE_CCA,
    AMT_RESOURCE_EXPENDITURES,
    AMT_RESOURCE_FOREIGN_PROPERTY_INCOME,
    AMT_RESOURCE_INCOME_TOTAL,
    AMT_RESOURCE_PRODUCTION_INCOME,
    AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES,
    AMT_TAX_SHELTER_ADJUSTMENTS,
    AMT_TAX_SHELTER_DEDUCTIBLE_AMOUNTS,
    AMT_TAX_SHELTER_LOSSES,
    AMT_TREATY_EXEMPT_CAPITAL_GAINS,
)
from tests.jurisdictions.ca.catalog_snapshot import SIGNED

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
    AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS,
    AMT_TREATY_EXEMPT_CAPITAL_GAINS,
    AMT_GRADUATED_RATE_ESTATE_CAPITAL_GAINS,
    AMT_CAPITAL_GAINS_ADJUSTMENTS,
    AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS,
    AMT_PUBLICLY_LISTED_GIFTS_TOTAL,
    AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231,
    AMT_PUBLICLY_LISTED_GIFTS_NET,
    AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT,
)

PART_9_KINDS: tuple[ArtifactKind[Decimal], ...] = (
    AMT_RESOURCE_EXPENDITURES,
    AMT_RESOURCE_PRODUCTION_INCOME,
    AMT_RESOURCE_FOREIGN_PROPERTY_INCOME,
    AMT_CLASS_43_1_INCOME,
    AMT_RESOURCE_INCOME_TOTAL,
    AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES,
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


def test_the_part_9_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/amt_resource_expenditures") is AMT_RESOURCE_EXPENDITURES
    assert registry.get("ca/amt_resource_production_income") is AMT_RESOURCE_PRODUCTION_INCOME
    assert (
        registry.get("ca/amt_resource_foreign_property_income")
        is AMT_RESOURCE_FOREIGN_PROPERTY_INCOME
    )
    assert registry.get("ca/amt_class_43_1_income") is AMT_CLASS_43_1_INCOME
    assert registry.get("ca/amt_resource_income_total") is AMT_RESOURCE_INCOME_TOTAL
    assert (
        registry.get("ca/amt_resource_property_and_flow_through_shares")
        is AMT_RESOURCE_PROPERTY_AND_FLOW_THROUGH_SHARES
    )


def test_the_part_1_capital_gains_and_gifts_kinds_are_the_registered_ones(
    registry: ArtifactRegistry,
) -> None:
    assert (
        registry.get("ca/amt_mortgage_foreclosure_capital_gains")
        is AMT_MORTGAGE_FORECLOSURE_CAPITAL_GAINS
    )
    assert registry.get("ca/amt_treaty_exempt_capital_gains") is AMT_TREATY_EXEMPT_CAPITAL_GAINS
    assert (
        registry.get("ca/amt_graduated_rate_estate_capital_gains")
        is AMT_GRADUATED_RATE_ESTATE_CAPITAL_GAINS
    )
    assert registry.get("ca/amt_capital_gains_adjustments") is AMT_CAPITAL_GAINS_ADJUSTMENTS
    assert (
        registry.get("ca/amt_net_capital_gains_after_adjustments")
        is AMT_NET_CAPITAL_GAINS_AFTER_ADJUSTMENTS
    )
    assert registry.get("ca/amt_publicly_listed_gifts_total") is AMT_PUBLICLY_LISTED_GIFTS_TOTAL
    assert (
        registry.get("ca/amt_publicly_listed_gifts_t1170_line_68231")
        is AMT_PUBLICLY_LISTED_GIFTS_T1170_LINE_68231
    )
    assert registry.get("ca/amt_publicly_listed_gifts_net") is AMT_PUBLICLY_LISTED_GIFTS_NET
    assert (
        registry.get("ca/amt_publicly_listed_gifts_adjustment")
        is AMT_PUBLICLY_LISTED_GIFTS_ADJUSTMENT
    )


def test_the_alternative_minimum_tax_kinds_are_money() -> None:
    for kind in PART_1_KINDS + PART_9_KINDS:
        assert kind.value_type is Decimal, kind.identifier


def test_the_bracketed_lines_are_signed_and_the_rest_are_not_below_zero() -> None:
    for kind in PART_1_KINDS + PART_9_KINDS:
        assert kind.non_negative is (kind.identifier not in SIGNED), kind.identifier
