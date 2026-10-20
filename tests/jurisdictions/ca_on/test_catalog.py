"""Snapshot of the `ca-on/` artifact kind identifiers, as the application registers them.

Identifiers are stored with results and exposed by the API, so changing or removing one is a
breaking change: update this snapshot only on purpose. Declaring a kind in this package's catalog
adds it here; federal kinds are snapshotted in `tests/jurisdictions/ca/`. The kinds are
registered explicitly, as the composition root does, into a fresh registry.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import app.jurisdictions.ca_on
import app.jurisdictions.ca_on.catalog
from app.domain.artifact import ArtifactCatalog, ArtifactKind, ArtifactRegistry
from app.domain.record_list import RecordListKind
from app.jurisdictions.ca_on.catalog import (
    AGE_AMOUNT,
    AGE_AMOUNT_BEFORE_COUNT,
    AGE_INCOME_OVER_THRESHOLD,
    AGE_INCOME_THRESHOLD,
    AGE_MAXIMUM,
    AGE_REDUCTION,
    BASIC_PERSONAL_AMOUNT,
    CATALOG,
    COMMUNITY_FOOD_PROGRAM_CREDIT,
    COMMUNITY_FOOD_PROGRAM_DONATIONS,
    CREDIT_AMOUNTS_AT_CREDIT_RATE,
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    DIVIDEND_CREDIT_FROM_LINE_57,
    DIVIDEND_TAX_CREDIT,
    DIVIDENDS_AMOUNT_A,
    DIVIDENDS_AMOUNT_A_LESS_B,
    DIVIDENDS_AMOUNT_B,
    DONATIONS_AND_GIFTS_CREDIT,
    DONATIONS_FIRST_TIER_CREDIT,
    DONATIONS_OVER_FIRST_TIER_CREDIT,
    ELIGIBLE_DEPENDANT_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
    ELIGIBLE_DEPENDANT_BASE,
    ELIGIBLE_DIVIDENDS_CREDIT,
    FERTILITY_CREDIT,
    FERTILITY_CREDIT_BEFORE_MAXIMUM,
    FERTILITY_EXPENSES,
    FLOW_THROUGH_SHARE_CREDIT,
    FLOW_THROUGH_SHARE_EXPENSES,
    FLOW_THROUGH_SHARE_SLIP_EXPENSES,
    FLOW_THROUGH_SHARE_SLIPS,
    LIFT_CREDIT,
    LIFT_CREDIT_BEFORE_MAXIMUM,
    LIFT_MAXIMUM_CREDIT,
    LIFT_REDUCTION,
    NET_REFUND,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    ONTARIO_BASIC_TAX,
    ONTARIO_CREDITS,
    ONTARIO_CREDITS_SUBTOTAL,
    ONTARIO_HEALTH_PREMIUM,
    ONTARIO_SURTAX,
    ONTARIO_TAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_AFTER_DIVIDEND_CREDIT,
    ONTARIO_TAX_AFTER_FOOD_CREDIT,
    ONTARIO_TAX_AFTER_LIFT_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
    ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT,
    ONTARIO_TAX_LESS_DIVIDEND_CREDIT,
    ONTARIO_TAX_REDUCTION,
    ONTARIO_TAX_WITH_SURTAX,
    OPPORTUNITIES_FUND_DONATION,
    OTHER_DIVIDENDS_CREDIT,
    POLITICAL_CONTRIBUTIONS,
    POLITICAL_CREDIT,
    POLITICAL_CREDIT_BEFORE_MAXIMUM,
    POLITICAL_CREDIT_COLUMN_1_LINE_2,
    POLITICAL_CREDIT_COLUMN_1_LINE_3,
    POLITICAL_CREDIT_COLUMN_1_LINE_5,
    POLITICAL_CREDIT_COLUMN_1_LINE_6,
    POLITICAL_CREDIT_COLUMN_1_LINE_7,
    POLITICAL_CREDIT_COLUMN_2_LINE_2,
    POLITICAL_CREDIT_COLUMN_2_LINE_3,
    POLITICAL_CREDIT_COLUMN_2_LINE_5,
    POLITICAL_CREDIT_COLUMN_2_LINE_6,
    POLITICAL_CREDIT_COLUMN_2_LINE_7,
    POLITICAL_CREDIT_COLUMN_3_LINE_2,
    POLITICAL_CREDIT_COLUMN_3_LINE_3,
    POLITICAL_CREDIT_COLUMN_3_LINE_5,
    POLITICAL_CREDIT_COLUMN_3_LINE_6,
    POLITICAL_CREDIT_COLUMN_3_LINE_7,
    REFUND_BEFORE_DONATION,
    SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
    SENIORS_TRANSIT_CREDIT,
    SENIORS_TRANSIT_PAID,
    SPOUSE_AMOUNT,
    SPOUSE_AMOUNT_BEFORE_COUNT,
    SPOUSE_AMOUNT_BEFORE_MAXIMUM,
    SPOUSE_BASE,
    TAX_REDUCTION_AMOUNTS,
    TAX_REDUCTION_BASIC,
    TAX_REDUCTION_FOR_CHILDREN,
    TAX_REDUCTION_FOR_DEPENDANTS,
)
from app.registrations import JURISDICTIONS

REGISTERED = frozenset(
    {
        "ca-on/ontario_basic_tax",
        "ca-on/basic_personal_amount",
        "ca-on/age_maximum",
        "ca-on/age_income_threshold",
        "ca-on/age_income_over_threshold",
        "ca-on/age_reduction",
        "ca-on/age_amount_before_count",
        "ca-on/age_amount",
        "ca-on/spouse_base",
        "ca-on/spouse_amount_before_maximum",
        "ca-on/spouse_amount_before_count",
        "ca-on/spouse_amount",
        "ca-on/eligible_dependant_base",
        "ca-on/eligible_dependant_amount_before_maximum",
        "ca-on/eligible_dependant_amount_before_count",
        "ca-on/eligible_dependant_amount",
        "ca-on/non_refundable_credit_amounts",
        "ca-on/credit_amounts_at_credit_rate",
        "ca-on/donations_first_tier_credit",
        "ca-on/donations_over_first_tier_credit",
        "ca-on/donations_and_gifts_credit",
        "ca-on/non_refundable_tax_credits",
        "ca-on/ontario_tax_after_credits",
        "ca-on/ontario_surtax",
        "ca-on/ontario_tax_with_surtax",
        "ca-on/dividends_amount_a",
        "ca-on/dividends_amount_b",
        "ca-on/other_dividends_credit",
        "ca-on/dividends_amount_a_less_b",
        "ca-on/eligible_dividends_credit",
        "ca-on/dividend_tax_credit",
        "ca-on/ontario_tax_before_dividend_credit",
        "ca-on/ontario_tax_less_dividend_credit",
        "ca-on/dividend_credit_from_line_57",
        "ca-on/ontario_tax_after_dividend_credit",
        "ca-on/tax_reduction_basic",
        "ca-on/dependent_children",
        "ca-on/tax_reduction_for_children",
        "ca-on/dependants",
        "ca-on/tax_reduction_for_dependants",
        "ca-on/tax_reduction_amounts",
        "ca-on/ontario_tax_reduction",
        "ca-on/ontario_tax_after_reduction",
        "ca-on/lift_credit_before_maximum",
        "ca-on/lift_maximum_credit",
        "ca-on/lift_reduction",
        "ca-on/lift_credit",
        "ca-on/ontario_tax_after_lift_credit",
        "ca-on/community_food_program_donations",
        "ca-on/community_food_program_credit",
        "ca-on/ontario_tax_after_food_credit",
        "ca-on/ontario_health_premium",
        "ca-on/ontario_tax",
        "ca-on/fertility_expenses",
        "ca-on/fertility_credit_before_maximum",
        "ca-on/fertility_credit",
        "ca-on/seniors_transit_paid",
        "ca-on/seniors_transit_amount_paid_at_most_maximum",
        "ca-on/seniors_transit_credit",
        "ca-on/political_contributions",
        "ca-on/political_credit_column_1_line_2",
        "ca-on/political_credit_column_1_line_3",
        "ca-on/political_credit_column_1_line_5",
        "ca-on/political_credit_column_1_line_6",
        "ca-on/political_credit_column_1_line_7",
        "ca-on/political_credit_column_2_line_2",
        "ca-on/political_credit_column_2_line_3",
        "ca-on/political_credit_column_2_line_5",
        "ca-on/political_credit_column_2_line_6",
        "ca-on/political_credit_column_2_line_7",
        "ca-on/political_credit_column_3_line_2",
        "ca-on/political_credit_column_3_line_3",
        "ca-on/political_credit_column_3_line_5",
        "ca-on/political_credit_column_3_line_6",
        "ca-on/political_credit_column_3_line_7",
        "ca-on/political_credit_before_maximum",
        "ca-on/political_credit",
        "ca-on/flow_through_share_slip_expenses",
        "ca-on/flow_through_share_slips",
        "ca-on/flow_through_share_expenses",
        "ca-on/flow_through_share_credit",
        "ca-on/ontario_credits_subtotal",
        "ca-on/ontario_credits",
        "ca-on/refund_before_donation",
        "ca-on/opportunities_fund_donation",
        "ca-on/net_refund",
    }
)
# ON428 lines 75 (line 60969) and 76 (line 60970): the numbers of dependent children and of
# dependants, counted, not money.
COUNTS = frozenset({"ca-on/dependent_children", "ca-on/dependants"})
# Form T1221 lines 1 to 3, one line per corporation or slip: the record list of the slips.
RECORD_LISTS = frozenset({"ca-on/flow_through_share_slips"})


@pytest.fixture
def registry() -> ArtifactRegistry:
    registry = ArtifactRegistry()
    JURISDICTIONS.register(registry)
    return registry


def test_registered_identifiers_snapshot(registry: ArtifactRegistry) -> None:
    identifiers = registry.identifiers()

    assert {i for i in identifiers if i.startswith("ca-on/")} == REGISTERED


def test_the_package_exposes_its_catalog() -> None:
    assert isinstance(app.jurisdictions.ca_on.catalog.CATALOG, ArtifactCatalog)
    assert app.jurisdictions.ca_on.catalog.CATALOG is CATALOG
    assert {kind.identifier for kind in CATALOG.kinds} == REGISTERED


def test_catalog_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca-on/ontario_basic_tax") is ONTARIO_BASIC_TAX
    assert registry.get("ca-on/ontario_tax_after_credits") is ONTARIO_TAX_AFTER_CREDITS
    assert registry.get("ca-on/basic_personal_amount") is BASIC_PERSONAL_AMOUNT
    assert registry.get("ca-on/age_maximum") is AGE_MAXIMUM
    assert registry.get("ca-on/age_income_threshold") is AGE_INCOME_THRESHOLD
    assert registry.get("ca-on/age_income_over_threshold") is AGE_INCOME_OVER_THRESHOLD
    assert registry.get("ca-on/age_reduction") is AGE_REDUCTION
    assert registry.get("ca-on/age_amount_before_count") is AGE_AMOUNT_BEFORE_COUNT
    assert registry.get("ca-on/age_amount") is AGE_AMOUNT
    assert registry.get("ca-on/spouse_base") is SPOUSE_BASE
    assert registry.get("ca-on/spouse_amount_before_maximum") is SPOUSE_AMOUNT_BEFORE_MAXIMUM
    assert registry.get("ca-on/spouse_amount_before_count") is SPOUSE_AMOUNT_BEFORE_COUNT
    assert registry.get("ca-on/spouse_amount") is SPOUSE_AMOUNT
    assert registry.get("ca-on/eligible_dependant_base") is ELIGIBLE_DEPENDANT_BASE
    assert (
        registry.get("ca-on/eligible_dependant_amount_before_maximum")
        is ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM
    )
    assert (
        registry.get("ca-on/eligible_dependant_amount_before_count")
        is ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT
    )
    assert registry.get("ca-on/eligible_dependant_amount") is ELIGIBLE_DEPENDANT_AMOUNT
    assert registry.get("ca-on/non_refundable_credit_amounts") is NON_REFUNDABLE_CREDIT_AMOUNTS
    assert registry.get("ca-on/credit_amounts_at_credit_rate") is CREDIT_AMOUNTS_AT_CREDIT_RATE
    assert registry.get("ca-on/donations_first_tier_credit") is DONATIONS_FIRST_TIER_CREDIT
    assert (
        registry.get("ca-on/donations_over_first_tier_credit") is DONATIONS_OVER_FIRST_TIER_CREDIT
    )
    assert registry.get("ca-on/donations_and_gifts_credit") is DONATIONS_AND_GIFTS_CREDIT
    assert registry.get("ca-on/non_refundable_tax_credits") is NON_REFUNDABLE_TAX_CREDITS
    assert registry.get("ca-on/ontario_surtax") is ONTARIO_SURTAX
    assert registry.get("ca-on/ontario_tax_with_surtax") is ONTARIO_TAX_WITH_SURTAX
    assert registry.get("ca-on/dividends_amount_a") is DIVIDENDS_AMOUNT_A
    assert registry.get("ca-on/dividends_amount_b") is DIVIDENDS_AMOUNT_B
    assert registry.get("ca-on/other_dividends_credit") is OTHER_DIVIDENDS_CREDIT
    assert registry.get("ca-on/dividends_amount_a_less_b") is DIVIDENDS_AMOUNT_A_LESS_B
    assert registry.get("ca-on/eligible_dividends_credit") is ELIGIBLE_DIVIDENDS_CREDIT
    assert registry.get("ca-on/dividend_tax_credit") is DIVIDEND_TAX_CREDIT
    assert (
        registry.get("ca-on/ontario_tax_before_dividend_credit")
        is ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT
    )
    assert (
        registry.get("ca-on/ontario_tax_less_dividend_credit") is ONTARIO_TAX_LESS_DIVIDEND_CREDIT
    )
    assert registry.get("ca-on/dividend_credit_from_line_57") is DIVIDEND_CREDIT_FROM_LINE_57
    assert (
        registry.get("ca-on/ontario_tax_after_dividend_credit") is ONTARIO_TAX_AFTER_DIVIDEND_CREDIT
    )
    assert registry.get("ca-on/tax_reduction_basic") is TAX_REDUCTION_BASIC
    assert registry.get("ca-on/dependent_children") is DEPENDENT_CHILDREN
    assert registry.get("ca-on/tax_reduction_for_children") is TAX_REDUCTION_FOR_CHILDREN
    assert registry.get("ca-on/dependants") is DEPENDANTS
    assert registry.get("ca-on/tax_reduction_for_dependants") is TAX_REDUCTION_FOR_DEPENDANTS
    assert registry.get("ca-on/tax_reduction_amounts") is TAX_REDUCTION_AMOUNTS
    assert registry.get("ca-on/ontario_tax_reduction") is ONTARIO_TAX_REDUCTION
    assert registry.get("ca-on/ontario_tax_after_reduction") is ONTARIO_TAX_AFTER_REDUCTION
    assert registry.get("ca-on/lift_credit_before_maximum") is LIFT_CREDIT_BEFORE_MAXIMUM
    assert registry.get("ca-on/lift_maximum_credit") is LIFT_MAXIMUM_CREDIT
    assert registry.get("ca-on/lift_reduction") is LIFT_REDUCTION
    assert registry.get("ca-on/lift_credit") is LIFT_CREDIT
    assert registry.get("ca-on/ontario_tax_after_lift_credit") is ONTARIO_TAX_AFTER_LIFT_CREDIT
    assert (
        registry.get("ca-on/community_food_program_donations") is COMMUNITY_FOOD_PROGRAM_DONATIONS
    )
    assert registry.get("ca-on/community_food_program_credit") is COMMUNITY_FOOD_PROGRAM_CREDIT
    assert registry.get("ca-on/ontario_tax_after_food_credit") is ONTARIO_TAX_AFTER_FOOD_CREDIT
    assert registry.get("ca-on/ontario_health_premium") is ONTARIO_HEALTH_PREMIUM
    assert registry.get("ca-on/ontario_tax") is ONTARIO_TAX
    assert registry.get("ca-on/fertility_expenses") is FERTILITY_EXPENSES
    assert registry.get("ca-on/fertility_credit_before_maximum") is FERTILITY_CREDIT_BEFORE_MAXIMUM
    assert registry.get("ca-on/fertility_credit") is FERTILITY_CREDIT
    assert registry.get("ca-on/seniors_transit_paid") is SENIORS_TRANSIT_PAID
    assert (
        registry.get("ca-on/seniors_transit_amount_paid_at_most_maximum")
        is SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM
    )
    assert registry.get("ca-on/seniors_transit_credit") is SENIORS_TRANSIT_CREDIT
    assert registry.get("ca-on/political_contributions") is POLITICAL_CONTRIBUTIONS
    assert (
        registry.get("ca-on/political_credit_column_1_line_2") is POLITICAL_CREDIT_COLUMN_1_LINE_2
    )
    assert (
        registry.get("ca-on/political_credit_column_1_line_3") is POLITICAL_CREDIT_COLUMN_1_LINE_3
    )
    assert (
        registry.get("ca-on/political_credit_column_1_line_5") is POLITICAL_CREDIT_COLUMN_1_LINE_5
    )
    assert (
        registry.get("ca-on/political_credit_column_1_line_6") is POLITICAL_CREDIT_COLUMN_1_LINE_6
    )
    assert (
        registry.get("ca-on/political_credit_column_1_line_7") is POLITICAL_CREDIT_COLUMN_1_LINE_7
    )
    assert (
        registry.get("ca-on/political_credit_column_2_line_2") is POLITICAL_CREDIT_COLUMN_2_LINE_2
    )
    assert (
        registry.get("ca-on/political_credit_column_2_line_3") is POLITICAL_CREDIT_COLUMN_2_LINE_3
    )
    assert (
        registry.get("ca-on/political_credit_column_2_line_5") is POLITICAL_CREDIT_COLUMN_2_LINE_5
    )
    assert (
        registry.get("ca-on/political_credit_column_2_line_6") is POLITICAL_CREDIT_COLUMN_2_LINE_6
    )
    assert (
        registry.get("ca-on/political_credit_column_2_line_7") is POLITICAL_CREDIT_COLUMN_2_LINE_7
    )
    assert (
        registry.get("ca-on/political_credit_column_3_line_2") is POLITICAL_CREDIT_COLUMN_3_LINE_2
    )
    assert (
        registry.get("ca-on/political_credit_column_3_line_3") is POLITICAL_CREDIT_COLUMN_3_LINE_3
    )
    assert (
        registry.get("ca-on/political_credit_column_3_line_5") is POLITICAL_CREDIT_COLUMN_3_LINE_5
    )
    assert (
        registry.get("ca-on/political_credit_column_3_line_6") is POLITICAL_CREDIT_COLUMN_3_LINE_6
    )
    assert (
        registry.get("ca-on/political_credit_column_3_line_7") is POLITICAL_CREDIT_COLUMN_3_LINE_7
    )
    assert registry.get("ca-on/political_credit_before_maximum") is POLITICAL_CREDIT_BEFORE_MAXIMUM
    assert registry.get("ca-on/political_credit") is POLITICAL_CREDIT
    assert (
        registry.get("ca-on/flow_through_share_slip_expenses") is FLOW_THROUGH_SHARE_SLIP_EXPENSES
    )
    assert registry.get("ca-on/flow_through_share_slips") is FLOW_THROUGH_SHARE_SLIPS
    assert registry.get("ca-on/flow_through_share_expenses") is FLOW_THROUGH_SHARE_EXPENSES
    assert registry.get("ca-on/flow_through_share_credit") is FLOW_THROUGH_SHARE_CREDIT
    assert registry.get("ca-on/ontario_credits_subtotal") is ONTARIO_CREDITS_SUBTOTAL
    assert registry.get("ca-on/ontario_credits") is ONTARIO_CREDITS
    assert registry.get("ca-on/refund_before_donation") is REFUND_BEFORE_DONATION
    assert registry.get("ca-on/opportunities_fund_donation") is OPPORTUNITIES_FUND_DONATION
    assert registry.get("ca-on/net_refund") is NET_REFUND


def test_every_registered_kind_but_the_counts_and_record_lists_is_money_in_the_package_namespace(
    registry: ArtifactRegistry,
) -> None:
    for identifier in REGISTERED - COUNTS - RECORD_LISTS:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.identifier.startswith(f"{app.jurisdictions.ca_on.NAMESPACE}/")
        assert kind.value_type is Decimal, identifier


def test_the_counts_are_int_kinds_in_the_package_namespace(registry: ArtifactRegistry) -> None:
    assert COUNTS <= REGISTERED
    for identifier in COUNTS:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.identifier.startswith(f"{app.jurisdictions.ca_on.NAMESPACE}/")
        assert kind.value_type is int, identifier


def test_the_flow_through_share_slips_are_a_record_list_of_the_slip_expenses(
    registry: ArtifactRegistry,
) -> None:
    assert RECORD_LISTS <= REGISTERED
    for identifier in RECORD_LISTS:
        kind = registry.get(identifier)
        assert isinstance(kind, RecordListKind)
        assert kind.identifier.startswith(f"{app.jurisdictions.ca_on.NAMESPACE}/")
    assert FLOW_THROUGH_SHARE_SLIPS.fields == (FLOW_THROUGH_SHARE_SLIP_EXPENSES,)
    assert FLOW_THROUGH_SHARE_SLIP_EXPENSES.value_type is Decimal


def test_every_kind_but_the_record_lists_is_declared_non_negative(
    registry: ArtifactRegistry,
) -> None:
    for kind in CATALOG.kinds:
        if kind.identifier not in RECORD_LISTS:
            assert kind.non_negative is True, kind.identifier
    for identifier in REGISTERED - RECORD_LISTS:
        assert registry.kind(identifier).non_negative is True, identifier
