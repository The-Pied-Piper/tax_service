"""Registered and money kinds of the federal catalog family `refundable_credits`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    EDUCATOR_SCHOOL_SUPPLY_CREDIT,
    EDUCATOR_SUPPLIES_EXPENSES,
    EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
    EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
    JOURNALISM_LABOUR_TAX_CREDIT,
    MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3,
    MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5,
    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2,
    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3,
    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4,
    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5,
    MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS,
    MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME,
    MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS,
    MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME,
    MEDICAL_SUPPLEMENT_IF_RESIDENT,
    MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET,
    MEDICAL_SUPPLEMENT_INCOME_THRESHOLD,
    MEDICAL_SUPPLEMENT_LINE_6,
    MEDICAL_SUPPLEMENT_LINE_8,
    MEDICAL_SUPPLEMENT_LINE_11,
    MEDICAL_SUPPLEMENT_LINE_13,
    MEDICAL_SUPPLEMENT_LINE_14,
    MEDICAL_SUPPLEMENT_LINE_15,
    MEDICAL_SUPPLEMENT_LINE_16,
    MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME,
    MEDICAL_SUPPLEMENT_WORKING_INCOME,
    PART_XII_2_TAX_CREDIT,
    PROVINCIAL_CREDITS,
    REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT,
    TAX_PAID_BY_INSTALMENTS,
)


def test_the_refundable_credits_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/provincial_credits") is PROVINCIAL_CREDITS
    assert registry.get("ca/part_xii_2_tax_credit") is PART_XII_2_TAX_CREDIT
    assert (
        registry.get("ca/employee_and_partner_gst_hst_rebate")
        is EMPLOYEE_AND_PARTNER_GST_HST_REBATE
    )
    assert registry.get("ca/educator_supplies_expenses") is EDUCATOR_SUPPLIES_EXPENSES
    assert (
        registry.get("ca/educator_supplies_expenses_at_most_maximum")
        is EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM
    )
    assert registry.get("ca/educator_school_supply_credit") is EDUCATOR_SCHOOL_SUPPLY_CREDIT
    assert registry.get("ca/journalism_labour_tax_credit") is JOURNALISM_LABOUR_TAX_CREDIT
    assert registry.get("ca/tax_paid_by_instalments") is TAX_PAID_BY_INSTALMENTS
    assert (
        registry.get("ca/medical_supplement_employment_income")
        is MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME
    )
    assert (
        registry.get("ca/medical_supplement_employment_income_less_wage_loss")
        is MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS
    )
    assert (
        registry.get("ca/medical_supplement_employment_deductions")
        is MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS
    )
    assert (
        registry.get("ca/medical_supplement_employment_working_income")
        is MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME
    )
    assert (
        registry.get("ca/medical_supplement_self_employment_income")
        is MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME
    )
    assert registry.get("ca/medical_supplement_working_income") is MEDICAL_SUPPLEMENT_WORKING_INCOME
    assert (
        registry.get("ca/medical_supplement_column_1_line_3") is MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3
    )
    assert (
        registry.get("ca/medical_supplement_column_1_line_5") is MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5
    )
    assert (
        registry.get("ca/medical_supplement_column_2_line_2") is MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2
    )
    assert (
        registry.get("ca/medical_supplement_column_2_line_3") is MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3
    )
    assert (
        registry.get("ca/medical_supplement_column_2_line_4") is MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4
    )
    assert (
        registry.get("ca/medical_supplement_column_2_line_5") is MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5
    )
    assert registry.get("ca/medical_supplement_line_6") is MEDICAL_SUPPLEMENT_LINE_6
    assert (
        registry.get("ca/medical_supplement_income_threshold")
        is MEDICAL_SUPPLEMENT_INCOME_THRESHOLD
    )
    assert registry.get("ca/medical_supplement_line_8") is MEDICAL_SUPPLEMENT_LINE_8
    assert registry.get("ca/medical_supplement_line_11") is MEDICAL_SUPPLEMENT_LINE_11
    assert registry.get("ca/medical_supplement_line_13") is MEDICAL_SUPPLEMENT_LINE_13
    assert registry.get("ca/medical_supplement_line_14") is MEDICAL_SUPPLEMENT_LINE_14
    assert registry.get("ca/medical_supplement_line_15") is MEDICAL_SUPPLEMENT_LINE_15
    assert registry.get("ca/medical_supplement_line_16") is MEDICAL_SUPPLEMENT_LINE_16
    assert (
        registry.get("ca/medical_supplement_if_working_income_met")
        is MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET
    )
    assert registry.get("ca/medical_supplement_if_resident") is MEDICAL_SUPPLEMENT_IF_RESIDENT
    assert (
        registry.get("ca/refundable_medical_expense_supplement")
        is REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT
    )


def test_the_refundable_credits_kinds_are_money() -> None:
    for kind in (
        PROVINCIAL_CREDITS,
        PART_XII_2_TAX_CREDIT,
        EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
        EDUCATOR_SUPPLIES_EXPENSES,
        EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
        EDUCATOR_SCHOOL_SUPPLY_CREDIT,
        JOURNALISM_LABOUR_TAX_CREDIT,
        TAX_PAID_BY_INSTALMENTS,
        MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME,
        MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS,
        MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS,
        MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME,
        MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME,
        MEDICAL_SUPPLEMENT_WORKING_INCOME,
        MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3,
        MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5,
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2,
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3,
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4,
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5,
        MEDICAL_SUPPLEMENT_LINE_6,
        MEDICAL_SUPPLEMENT_INCOME_THRESHOLD,
        MEDICAL_SUPPLEMENT_LINE_8,
        MEDICAL_SUPPLEMENT_LINE_11,
        MEDICAL_SUPPLEMENT_LINE_13,
        MEDICAL_SUPPLEMENT_LINE_14,
        MEDICAL_SUPPLEMENT_LINE_15,
        MEDICAL_SUPPLEMENT_LINE_16,
        MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET,
        MEDICAL_SUPPLEMENT_IF_RESIDENT,
        REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT,
    ):
        assert kind.value_type is Decimal, kind.identifier
