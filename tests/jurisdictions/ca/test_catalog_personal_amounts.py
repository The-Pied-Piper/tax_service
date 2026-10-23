"""Registered and money kinds of the federal catalog family `personal_amounts`."""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    AGE_AMOUNT,
    AGE_AMOUNT_BEFORE_COUNT,
    AGE_INCOME_OVER_THRESHOLD,
    AGE_INCOME_THRESHOLD,
    AGE_MAXIMUM,
    AGE_REDUCTION,
    BASIC_PERSONAL_AMOUNT,
    BORN_IN_1960_OR_EARLIER,
    CAREGIVER_AMOUNT,
    CCA_ADDITIONS,
    CCA_AIIP_ADDITIONS,
    CCA_CLAIMED,
    CCA_CLASS_NUMBER,
    CCA_DIEP_ADDITIONS,
    CCA_DIEP_PROCEEDS,
    CCA_IMMEDIATE_EXPENSING,
    CCA_NO_PROPERTY_LEFT,
    CCA_PROCEEDS,
    CCA_RIIP_ADDITIONS,
    CCA_UCC_AT_END,
    CCA_UCC_AT_START,
    DEPENDANT_CARE_EXPENSES,
    DEPENDANT_CREDIT_AMOUNTS,
    DEPENDANT_NET_INCOME,
    DEPENDANT_TAXABLE_INCOME,
    DEPENDANT_UNDER_18,
    DISABILITY_AMOUNT_FOR_SELF,
    DISABILITY_AMOUNT_FOR_SELF_IF_ELIGIBLE,
    DISABILITY_DEPENDANTS,
    DISABILITY_SELF_BASE_AMOUNT,
    DISABILITY_SELF_CARE_EXPENSES,
    DISABILITY_SELF_CARE_OVER_THRESHOLD,
    DISABILITY_SELF_CARE_THRESHOLD,
    DISABILITY_SELF_SUPPLEMENT,
    DISABILITY_SELF_SUPPLEMENT_MAXIMUM,
    DISABILITY_SELF_WORKSHEET_AMOUNT,
    DISABILITY_TRANSFERRED_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
    ELIGIBLE_DEPENDANTS,
    ELIGIBLE_FOR_DISABILITY_AMOUNT,
    FEDERAL_BASIC_TAX,
    INFIRM_CHILDREN,
    INFIRM_CHILDREN_AMOUNT,
    INFIRM_DEPENDANTS,
    MEDICAL_CLAIM,
    MEDICAL_EXPENSES,
    MEDICAL_EXPENSES_OVER_THRESHOLD,
    MEDICAL_NET_INCOME_SHARE,
    MEDICAL_THRESHOLD,
    OTHER_DEPENDANT_MEDICAL_EXPENSES,
    OTHER_DEPENDANTS,
    OTHER_DEPENDANTS_MEDICAL,
    PRINCIPAL_RESIDENCE_GAIN,
    PRINCIPAL_RESIDENCE_PROPERTIES,
    RESIDENCE_ADJUSTED_COST_BASE,
    RESIDENCE_OUTLAYS,
    RESIDENCE_PLUS_ONE_YEAR,
    RESIDENCE_PROCEEDS,
    RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
    RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
    RESIDENCE_YEARS_OWNED_1972_TO_1981,
    RESIDENCE_YEARS_OWNED_AFTER_1981,
    SPOUSE_AMOUNT,
    SPOUSE_AMOUNT_BASIS,
    SPOUSE_AMOUNT_BEFORE_COUNT,
    SPOUSE_CAREGIVER_AMOUNT,
    SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT,
    SPOUSE_CAREGIVER_BASE,
    SPOUSE_CAREGIVER_BEFORE_MAXIMUM,
    SPOUSE_CAREGIVER_ELIGIBLE,
    SPOUSE_CAREGIVER_LIMIT,
    SPOUSE_INFIRMITY_SUPPLEMENT,
    SPOUSE_NET_INCOME,
    SPOUSES_CLAIMED,
    UNDER_18_ON_DECEMBER_31,
)


def test_the_personal_amounts_kinds_are_the_registered_ones(registry: ArtifactRegistry) -> None:
    assert registry.get("ca/federal_basic_tax") is FEDERAL_BASIC_TAX
    assert registry.get("ca/basic_personal_amount") is BASIC_PERSONAL_AMOUNT
    assert registry.get("ca/born_in_1960_or_earlier") is BORN_IN_1960_OR_EARLIER
    assert registry.get("ca/age_maximum") is AGE_MAXIMUM
    assert registry.get("ca/age_income_threshold") is AGE_INCOME_THRESHOLD
    assert registry.get("ca/age_income_over_threshold") is AGE_INCOME_OVER_THRESHOLD
    assert registry.get("ca/age_reduction") is AGE_REDUCTION
    assert registry.get("ca/age_amount_before_count") is AGE_AMOUNT_BEFORE_COUNT
    assert registry.get("ca/age_amount") is AGE_AMOUNT
    assert registry.get("ca/spouses_claimed") is SPOUSES_CLAIMED
    assert registry.get("ca/spouse_caregiver_eligible") is SPOUSE_CAREGIVER_ELIGIBLE
    assert registry.get("ca/spouse_net_income") is SPOUSE_NET_INCOME
    assert registry.get("ca/spouse_infirmity_supplement") is SPOUSE_INFIRMITY_SUPPLEMENT
    assert registry.get("ca/spouse_amount_basis") is SPOUSE_AMOUNT_BASIS
    assert registry.get("ca/spouse_amount_before_count") is SPOUSE_AMOUNT_BEFORE_COUNT
    assert registry.get("ca/spouse_amount") is SPOUSE_AMOUNT
    assert registry.get("ca/eligible_dependants") is ELIGIBLE_DEPENDANTS
    assert registry.get("ca/dependant_net_income") is DEPENDANT_NET_INCOME
    assert (
        registry.get("ca/eligible_dependant_amount_before_count")
        is ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT
    )
    assert registry.get("ca/eligible_dependant_amount") is ELIGIBLE_DEPENDANT_AMOUNT
    assert registry.get("ca/spouse_caregiver_base") is SPOUSE_CAREGIVER_BASE
    assert registry.get("ca/spouse_caregiver_before_maximum") is SPOUSE_CAREGIVER_BEFORE_MAXIMUM
    assert registry.get("ca/spouse_caregiver_limit") is SPOUSE_CAREGIVER_LIMIT
    assert (
        registry.get("ca/spouse_caregiver_amount_before_count")
        is SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT
    )
    assert registry.get("ca/spouse_caregiver_amount") is SPOUSE_CAREGIVER_AMOUNT
    assert registry.get("ca/infirm_dependants") is INFIRM_DEPENDANTS
    assert registry.get("ca/caregiver_amount") is CAREGIVER_AMOUNT
    assert registry.get("ca/other_dependant_medical_expenses") is OTHER_DEPENDANT_MEDICAL_EXPENSES
    assert registry.get("ca/other_dependants") is OTHER_DEPENDANTS
    assert registry.get("ca/other_dependants_medical") is OTHER_DEPENDANTS_MEDICAL
    assert registry.get("ca/medical_expenses") is MEDICAL_EXPENSES
    assert registry.get("ca/medical_net_income_share") is MEDICAL_NET_INCOME_SHARE
    assert registry.get("ca/medical_threshold") is MEDICAL_THRESHOLD
    assert registry.get("ca/medical_expenses_over_threshold") is MEDICAL_EXPENSES_OVER_THRESHOLD
    assert registry.get("ca/medical_claim") is MEDICAL_CLAIM
    assert registry.get("ca/dependant_under_18") is DEPENDANT_UNDER_18
    assert registry.get("ca/dependant_care_expenses") is DEPENDANT_CARE_EXPENSES
    assert registry.get("ca/dependant_credit_amounts") is DEPENDANT_CREDIT_AMOUNTS
    assert registry.get("ca/dependant_taxable_income") is DEPENDANT_TAXABLE_INCOME
    assert registry.get("ca/disability_dependants") is DISABILITY_DEPENDANTS
    assert registry.get("ca/disability_transferred_amount") is DISABILITY_TRANSFERRED_AMOUNT
    assert (
        registry.get("ca/residence_years_designated_after_1981")
        is RESIDENCE_YEARS_DESIGNATED_AFTER_1981
    )
    assert (
        registry.get("ca/residence_years_designated_1972_to_1981")
        is RESIDENCE_YEARS_DESIGNATED_1972_TO_1981
    )
    assert registry.get("ca/residence_years_owned_after_1981") is RESIDENCE_YEARS_OWNED_AFTER_1981
    assert (
        registry.get("ca/residence_years_owned_1972_to_1981") is RESIDENCE_YEARS_OWNED_1972_TO_1981
    )
    assert registry.get("ca/residence_proceeds") is RESIDENCE_PROCEEDS
    assert registry.get("ca/residence_outlays") is RESIDENCE_OUTLAYS
    assert registry.get("ca/residence_adjusted_cost_base") is RESIDENCE_ADJUSTED_COST_BASE
    assert registry.get("ca/residence_plus_one_year") is RESIDENCE_PLUS_ONE_YEAR
    assert registry.get("ca/principal_residence_properties") is PRINCIPAL_RESIDENCE_PROPERTIES
    assert registry.get("ca/principal_residence_gain") is PRINCIPAL_RESIDENCE_GAIN
    assert registry.get("ca/cca_class_number") is CCA_CLASS_NUMBER
    assert registry.get("ca/cca_ucc_at_start") is CCA_UCC_AT_START
    assert registry.get("ca/cca_additions") is CCA_ADDITIONS
    assert registry.get("ca/cca_proceeds") is CCA_PROCEEDS
    assert registry.get("ca/cca_aiip_additions") is CCA_AIIP_ADDITIONS
    assert registry.get("ca/cca_riip_additions") is CCA_RIIP_ADDITIONS
    assert registry.get("ca/cca_diep_additions") is CCA_DIEP_ADDITIONS
    assert registry.get("ca/cca_diep_proceeds") is CCA_DIEP_PROCEEDS
    assert registry.get("ca/cca_immediate_expensing") is CCA_IMMEDIATE_EXPENSING
    assert registry.get("ca/cca_claimed") is CCA_CLAIMED
    assert registry.get("ca/cca_no_property_left") is CCA_NO_PROPERTY_LEFT
    assert registry.get("ca/cca_ucc_at_end") is CCA_UCC_AT_END
    assert registry.get("ca/infirm_children") is INFIRM_CHILDREN
    assert registry.get("ca/infirm_children_amount") is INFIRM_CHILDREN_AMOUNT
    assert registry.get("ca/disability_amount_for_self") is DISABILITY_AMOUNT_FOR_SELF
    assert registry.get("ca/eligible_for_disability_amount") is ELIGIBLE_FOR_DISABILITY_AMOUNT
    assert registry.get("ca/under_18_on_december_31") is UNDER_18_ON_DECEMBER_31
    assert registry.get("ca/disability_self_care_expenses") is DISABILITY_SELF_CARE_EXPENSES
    assert registry.get("ca/disability_self_base_amount") is DISABILITY_SELF_BASE_AMOUNT
    assert (
        registry.get("ca/disability_self_supplement_maximum") is DISABILITY_SELF_SUPPLEMENT_MAXIMUM
    )
    assert registry.get("ca/disability_self_care_threshold") is DISABILITY_SELF_CARE_THRESHOLD
    assert (
        registry.get("ca/disability_self_care_over_threshold")
        is DISABILITY_SELF_CARE_OVER_THRESHOLD
    )
    assert registry.get("ca/disability_self_supplement") is DISABILITY_SELF_SUPPLEMENT
    assert registry.get("ca/disability_self_worksheet_amount") is DISABILITY_SELF_WORKSHEET_AMOUNT
    assert (
        registry.get("ca/disability_amount_for_self_if_eligible")
        is DISABILITY_AMOUNT_FOR_SELF_IF_ELIGIBLE
    )


def test_the_personal_amounts_kinds_are_money() -> None:
    for kind in (
        BASIC_PERSONAL_AMOUNT,
        AGE_MAXIMUM,
        AGE_INCOME_THRESHOLD,
        AGE_INCOME_OVER_THRESHOLD,
        AGE_REDUCTION,
        AGE_AMOUNT_BEFORE_COUNT,
        AGE_AMOUNT,
        SPOUSE_NET_INCOME,
        SPOUSE_INFIRMITY_SUPPLEMENT,
        SPOUSE_AMOUNT_BASIS,
        SPOUSE_AMOUNT_BEFORE_COUNT,
        SPOUSE_AMOUNT,
        DEPENDANT_NET_INCOME,
        ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
        ELIGIBLE_DEPENDANT_AMOUNT,
        SPOUSE_CAREGIVER_BASE,
        SPOUSE_CAREGIVER_BEFORE_MAXIMUM,
        SPOUSE_CAREGIVER_LIMIT,
        SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT,
        SPOUSE_CAREGIVER_AMOUNT,
        CAREGIVER_AMOUNT,
        OTHER_DEPENDANT_MEDICAL_EXPENSES,
        OTHER_DEPENDANTS_MEDICAL,
        MEDICAL_EXPENSES,
        MEDICAL_NET_INCOME_SHARE,
        MEDICAL_THRESHOLD,
        MEDICAL_EXPENSES_OVER_THRESHOLD,
        MEDICAL_CLAIM,
        DEPENDANT_CARE_EXPENSES,
        DEPENDANT_CREDIT_AMOUNTS,
        DEPENDANT_TAXABLE_INCOME,
        DISABILITY_TRANSFERRED_AMOUNT,
        RESIDENCE_PROCEEDS,
        RESIDENCE_OUTLAYS,
        RESIDENCE_ADJUSTED_COST_BASE,
        PRINCIPAL_RESIDENCE_GAIN,
        CCA_CLASS_NUMBER,
        CCA_UCC_AT_START,
        CCA_ADDITIONS,
        CCA_PROCEEDS,
        CCA_AIIP_ADDITIONS,
        CCA_RIIP_ADDITIONS,
        CCA_DIEP_ADDITIONS,
        CCA_DIEP_PROCEEDS,
        CCA_IMMEDIATE_EXPENSING,
        CCA_CLAIMED,
        CCA_UCC_AT_END,
        INFIRM_CHILDREN_AMOUNT,
        DISABILITY_AMOUNT_FOR_SELF,
        DISABILITY_SELF_CARE_EXPENSES,
        DISABILITY_SELF_BASE_AMOUNT,
        DISABILITY_SELF_SUPPLEMENT_MAXIMUM,
        DISABILITY_SELF_CARE_THRESHOLD,
        DISABILITY_SELF_CARE_OVER_THRESHOLD,
        DISABILITY_SELF_SUPPLEMENT,
        DISABILITY_SELF_WORKSHEET_AMOUNT,
        DISABILITY_AMOUNT_FOR_SELF_IF_ELIGIBLE,
    ):
        assert kind.value_type is Decimal, kind.identifier


def test_the_disability_amount_for_self_callers_are_counts_and_the_care_expenses_are_money() -> (
    None
):
    for count in (ELIGIBLE_FOR_DISABILITY_AMOUNT, UNDER_18_ON_DECEMBER_31):
        assert count.value_type is int, count.identifier
        assert count.non_negative is True, count.identifier
    assert DISABILITY_SELF_CARE_EXPENSES.value_type is Decimal
    assert DISABILITY_SELF_CARE_EXPENSES.non_negative is True
