"""Shared helpers for the end-to-end tests of CA-ON 2025."""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any

from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.parameters.rounding import RoundingMode, RoundTo
from app.domain.record_list import RecordList, RecordListKind
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    ADDITIONAL_DEDUCTIONS,
    ADVANCED_CANADA_WORKERS_BENEFIT,
    AGED_18_OR_OLDER_AT_END_OF_2025,
    BOND_DISPOSITIONS,
    BORN_IN_1960_OR_EARLIER,
    BUSINESS_INCOME,
    BUSINESS_INVESTMENT_LOSS,
    CANADA_TRAINING_CREDIT_CLAIMED,
    CANADA_TRAINING_CREDIT_LIMIT,
    CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
    CANADIAN_TUITION_FEES,
    CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
    CAPITAL_GAINS_DEDUCTIONS_2000,
    CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
    CAPITAL_GAINS_DEFERRAL,
    CAPITAL_GAINS_RESERVES,
    CAPITAL_GIFT_GAINS_DEDUCTION,
    CAPITAL_GIFT_TAXABLE_GAINS,
    CCA_ADDITIONS,
    CCA_AIIP_ADDITIONS,
    CCA_CLAIMED,
    CCA_CLASS_NUMBER,
    CCA_NO_PROPERTY_LEFT,
    CCA_PROCEEDS,
    CCA_RIIP_ADDITIONS,
    CCA_UCC_AT_START,
    CHARITABLE_DONATIONS,
    CHILD_CARE_EXPENSES_PAID,
    CHILDREN_SEVEN_TO_SIXTEEN,
    CHILDREN_UNDER_SEVEN,
    CHILDREN_WITH_DISABILITY,
    CLERGY_RESIDENCE_DEDUCTION,
    COMMISSION_INCOME,
    CPP_MONTHS,
    CPP_OR_QPP_BENEFITS,
    CPP_PART_4_COMPLETED,
    CPT20_EARNINGS,
    CRYPTO_ASSET_DISPOSITIONS,
    CWB_ELIGIBLE_DEPENDANTS,
    DEPENDANT_CARE_EXPENSES,
    DEPENDANT_CREDIT_AMOUNTS,
    DEPENDANT_NET_INCOME,
    DEPENDANT_TAXABLE_INCOME,
    DEPENDANT_UNDER_18,
    DEPRECIABLE_GIFT_CAPITAL_COST,
    DEPRECIABLE_GIFT_NET_PROCEEDS,
    DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION,
    DISABILITY_AMOUNT_FOR_SELF,
    DISABILITY_DEPENDANTS,
    DISABILITY_SUPPORTS_DEDUCTION,
    DISPOSITION_ADJUSTED_COST_BASE,
    DISPOSITION_OUTLAYS,
    DISPOSITION_PROCEEDS,
    ECOLOGICAL_AND_CULTURAL_GIFTS,
    ECOLOGICAL_GIFTS_BEFORE_2016,
    EDUCATOR_SUPPLIES_EXPENSES,
    EI_AND_OTHER_BENEFITS,
    EI_BENEFITS_REPAYMENT,
    EI_CONTROLLED_CORPORATION_EARNINGS,
    EI_EXEMPT_SELF_EMPLOYMENT_INCOME,
    EI_INSURABLE_EARNINGS,
    EI_SPECIAL_BENEFITS_AGREEMENT,
    ELECTED_SPLIT_PENSION_AMOUNT,
    ELECTED_SPLIT_PENSION_DEDUCTION,
    ELIGIBLE_DEPENDANTS,
    ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
    EMPLOYMENT_INCOME,
    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
    FARMING_INCOME,
    FHSA_ANNUAL_LIMITS_FOR_2024_AND_PRIOR_YEARS,
    FHSA_CARRYFORWARD_FOR_2024,
    FHSA_CARRYFORWARD_FOR_2025,
    FHSA_CONTRIBUTIONS_DEDUCTED,
    FHSA_CONTRIBUTIONS_IN_2024,
    FHSA_CONTRIBUTIONS_IN_2024_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2025,
    FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS,
    FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
    FHSA_DESIGNATED_TRANSFERS_IN_2025,
    FHSA_DESIGNATED_WITHDRAWALS_IN_2025,
    FHSA_INCOME,
    FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED,
    FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
    FHSA_RRSP_TRANSFERS_IN_2025,
    FHSA_UNUSED_CONTRIBUTIONS_BROUGHT_FORWARD,
    FHSA_VARIABLE_B_AMOUNT,
    FHSA_VARIABLE_F_AMOUNT,
    FHSA_VARIABLE_H_AMOUNT,
    FISHING_INCOME,
    FOREIGN_CHARITY_DONATIONS,
    FOREIGN_INVESTMENT_INCOME,
    FOREIGN_TUITION_FEES,
    GOVERNMENT_DONATIONS,
    INCOME_TAX_DEDUCTED,
    INFIRM_CHILDREN,
    INFIRM_DEPENDANTS,
    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
    INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
    INVESTMENT_INCOME_WITHOUT_A_SLIP,
    INVESTMENT_ROYALTIES,
    ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT,
    ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT,
    JOURNALISM_LABOUR_TAX_CREDIT,
    LABOUR_SPONSORED_FUNDS_NET_COST,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    LISTED_PERSONAL_PROPERTY_DISPOSITIONS,
    MEDICAL_EXPENSES,
    NET_BUSINESS_INCOME,
    NET_CAPITAL_LOSSES_CLAIMED,
    NET_COMMISSION_INCOME,
    NET_FARMING_INCOME,
    NET_FEDERAL_SUPPLEMENTS,
    NET_FISHING_INCOME,
    NET_PARTNERSHIP_INCOME,
    NET_PROFESSIONAL_INCOME,
    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
    OAS_OVERPAYMENT_RECOVERED,
    OLD_AGE_SECURITY,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
    OTHER_DEDUCTIONS,
    OTHER_DEPENDANT_MEDICAL_EXPENSES,
    OTHER_DEPENDANTS,
    OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    OTHER_EMPLOYMENT_EXPENSES,
    OTHER_EMPLOYMENT_INCOME,
    OTHER_FHSA_INCOME,
    OTHER_FORECLOSURE_DISPOSITIONS,
    OTHER_INCOME,
    OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT,
    OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
    OTHER_PAYMENTS_WORKSHEET_REQUIRED,
    OTHER_PENSIONS_AND_SUPERANNUATION,
    OTHER_SPLIT_INCOME,
    PART_XII_2_TAX_CREDIT,
    PARTNERSHIP_GAINS_AT_FULL_INCLUSION,
    PERSONAL_USE_PROPERTY_DISPOSITIONS,
    POLITICAL_CONTRIBUTIONS,
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
    PRINCIPAL_RESIDENCE_PROPERTIES,
    PROFESSIONAL_INCOME,
    QFFP_DISPOSITIONS,
    QFFP_FORECLOSURE_DISPOSITIONS,
    QSBCS_DISPOSITIONS,
    RDSP_INCOME,
    RDSP_INCOME_REPAYMENT,
    REAL_ESTATE_DISPOSITIONS,
    RENTAL_ADVERTISING,
    RENTAL_ADVERTISING_PERSONAL_PORTION,
    RENTAL_ADVERTISING_SHORT_TERM_PORTION,
    RENTAL_CCA_BUSINESS_USE_OF_HOME,
    RENTAL_CCA_CLASSES,
    RENTAL_CCA_PERSONAL_PART,
    RENTAL_COOWNER,
    RENTAL_COOWNER_CCA_CLAIM,
    RENTAL_COOWNER_OTHER_EXPENSES,
    RENTAL_COOWNER_RECAPTURED_CCA,
    RENTAL_COOWNER_SHARE,
    RENTAL_COOWNER_TERMINAL_LOSS,
    RENTAL_INSURANCE,
    RENTAL_INSURANCE_PERSONAL_PORTION,
    RENTAL_INSURANCE_SHORT_TERM_PORTION,
    RENTAL_INTEREST_AND_BANK_CHARGES,
    RENTAL_INTEREST_AND_BANK_CHARGES_PERSONAL_PORTION,
    RENTAL_INTEREST_AND_BANK_CHARGES_SHORT_TERM_PORTION,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_PERSONAL_PORTION,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_SHORT_TERM_PORTION,
    RENTAL_MOTOR_VEHICLE_EXPENSES,
    RENTAL_MOTOR_VEHICLE_EXPENSES_PERSONAL_PORTION,
    RENTAL_MOTOR_VEHICLE_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_OFFICE_EXPENSES,
    RENTAL_OFFICE_EXPENSES_PERSONAL_PORTION,
    RENTAL_OFFICE_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_OTHER_EXPENSES,
    RENTAL_OTHER_EXPENSES_PERSONAL_PORTION,
    RENTAL_OTHER_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_OTHER_INCOME,
    RENTAL_PARTNER,
    RENTAL_PARTNER_GST_HST_REBATE,
    RENTAL_PARTNER_OTHER_EXPENSES,
    RENTAL_PARTNER_SHARE,
    RENTAL_PROFESSIONAL_FEES,
    RENTAL_PROFESSIONAL_FEES_PERSONAL_PORTION,
    RENTAL_PROFESSIONAL_FEES_SHORT_TERM_PORTION,
    RENTAL_PROPERTIES,
    RENTAL_PROPERTY_GROSS_RENTS,
    RENTAL_PROPERTY_SHORT_TERM_RENTS,
    RENTAL_PROPERTY_TAXES,
    RENTAL_PROPERTY_TAXES_PERSONAL_PORTION,
    RENTAL_PROPERTY_TAXES_SHORT_TERM_PORTION,
    RENTAL_PROPERTY_UNITS,
    RENTAL_REPAIRS_AND_MAINTENANCE,
    RENTAL_REPAIRS_AND_MAINTENANCE_PERSONAL_PORTION,
    RENTAL_REPAIRS_AND_MAINTENANCE_SHORT_TERM_PORTION,
    RENTAL_SALARIES_WAGES_AND_BENEFITS,
    RENTAL_SALARIES_WAGES_AND_BENEFITS_PERSONAL_PORTION,
    RENTAL_SALARIES_WAGES_AND_BENEFITS_SHORT_TERM_PORTION,
    RENTAL_TRAVEL,
    RENTAL_TRAVEL_PERSONAL_PORTION,
    RENTAL_TRAVEL_SHORT_TERM_PORTION,
    RENTAL_UTILITIES,
    RENTAL_UTILITIES_PERSONAL_PORTION,
    RENTAL_UTILITIES_SHORT_TERM_PORTION,
    RESIDENCE_ADJUSTED_COST_BASE,
    RESIDENCE_OUTLAYS,
    RESIDENCE_PLUS_ONE_YEAR,
    RESIDENCE_PROCEEDS,
    RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
    RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
    RESIDENCE_YEARS_OWNED_1972_TO_1981,
    RESIDENCE_YEARS_OWNED_AFTER_1981,
    RESIDENT_IN_CANADA_THROUGHOUT_2025,
    RESP_AIPS_PART_A_APPLIES,
    RESP_AIPS_RECEIVED_PART_A,
    RESP_AIPS_RECEIVED_PART_B,
    RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS,
    RESP_AIPS_RRSP_CONTRIBUTIONS,
    RL_10_LABOUR_SPONSORED_FUND_AMOUNT,
    RPP_DEDUCTION,
    RRSP_AMOUNT_DEDUCTED,
    RRSP_CONTRIBUTIONS,
    RRSP_DEDUCTION_LIMIT,
    RRSP_INCOME,
    SECURITY_OPTIONS_DEDUCTIONS,
    SHARE_DISPOSITIONS,
    SHORT_TERM_RENTAL_CCA_UNITS,
    SHORT_TERM_RENTAL_DAYS,
    SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS,
    SHORT_TERM_RENTAL_RELATED_CCA,
    SHORT_TERM_RENTAL_RELATED_EXPENSES,
    SHORT_TERM_RENTAL_UNITS,
    SLIP_CAPITAL_GAINS_OR_LOSSES,
    SOCIAL_ASSISTANCE_PAYMENTS,
    SPLIT_INCOME_DIVIDENDS,
    SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SPOUSE_CAREGIVER_ELIGIBLE,
    SPOUSE_DESIGNATED_TUITION,
    SPOUSE_NET_INCOME,
    SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS,
    SPOUSE_NOT_SEPARATED_90_DAYS,
    SPOUSE_OR_COMMON_LAW_PARTNER_ON_DECEMBER_31,
    SPOUSE_RDSP_INCOME,
    SPOUSE_RDSP_INCOME_REPAYMENT,
    SPOUSE_RETURN_AGE_AMOUNT,
    SPOUSE_RETURN_BASIC_PERSONAL_AMOUNT,
    SPOUSE_RETURN_DISABILITY_AMOUNT,
    SPOUSE_RETURN_FEDERAL_BASIC_TAX,
    SPOUSE_RETURN_FEDERAL_TUITION_AMOUNT,
    SPOUSE_RETURN_INFIRM_CHILDREN_AMOUNT,
    SPOUSE_RETURN_LINE_96,
    SPOUSE_RETURN_PENSION_INCOME_AMOUNT,
    SPOUSE_RETURN_TAXABLE_INCOME,
    SPOUSE_UCCB_REPAYMENT,
    SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT,
    SPOUSES_CLAIMED,
    STANDARD_AMOUNT_ALLOCATED_1,
    STANDARD_AMOUNT_ALLOCATED_2,
    STANDARD_AMOUNT_ALLOCATED_3,
    SUPPORT_PAYMENTS_DEDUCTION,
    T3_CAPITAL_GAINS_OR_LOSSES,
    T3_DIVIDEND_TAX_CREDIT,
    T3_INVESTMENT_INCOME,
    T3_TAXABLE_DIVIDENDS,
    T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    T4PS_DIVIDEND_TAX_CREDIT,
    T4PS_TAXABLE_DIVIDENDS,
    T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    T5_DIVIDEND_TAX_CREDIT,
    T5_INVESTMENT_INCOME,
    T5_TAXABLE_DIVIDENDS,
    T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    T5013_DIVIDEND_TAX_CREDIT,
    T5013_INVESTMENT_INCOME,
    T5013_TAXABLE_DIVIDENDS,
    T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TAX_PAID_BY_INSTALMENTS,
    TAX_REFUND_INTEREST,
    TAXABLE_SCHOLARSHIPS,
    TAXABLE_SUPPORT_PAYMENTS,
    TOTAL_CARRYING_CHARGES,
    TOTAL_INTEREST_EXPENSES,
    TOTAL_OTHER_EXPENSES,
    TRAVEL_INDIVIDUAL,
    TRAVEL_INDIVIDUALS,
    TRAVEL_TRIPS,
    TRIP_BENEFIT_OR_STANDARD_AMOUNT,
    TRIP_LOWEST_RETURN_AIRFARE,
    TRIP_TRAVEL_EXPENSES,
    TRIP_ZONE,
    TUITION_TRANSFER_ELECTED,
    TUITION_TRANSFERRED_FROM_CHILD,
    UCCB_REPAYMENT,
    UNAPPLIED_LISTED_PERSONAL_PROPERTY_LOSSES,
    UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
    UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
    UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
    UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
    UNION_DUES,
    UNIVERSAL_CHILD_CARE_BENEFIT,
    UNIVERSITY_DONATIONS_OUTSIDE_CANADA,
    UNUSED_RRSP_CONTRIBUTIONS,
    UNUSED_TUITION_FROM_2024,
    WAGE_LOSS_REPLACEMENT_PLAN_INCOME,
    WORKERS_COMPENSATION_BENEFITS,
    ZONE_A_ADDITIONAL_RESIDENCY_DAYS,
    ZONE_A_DAYS_LIVED,
    ZONE_A_SPECIAL_WORK_SITE_BENEFITS,
    ZONE_B_ADDITIONAL_RESIDENCY_DAYS,
    ZONE_B_DAYS_LIVED,
    ZONE_B_SPECIAL_WORK_SITE_BENEFITS,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    APPLIES_FOR_ENERGY_AND_PROPERTY_TAX_CREDIT,
    APPLIES_FOR_NORTHERN_ENERGY_CREDIT,
    APPLIES_FOR_SENIOR_HOMEOWNERS_GRANT,
    CARE_SUPPORTING_PERSONS_ADJUSTED_INCOME,
    CHOOSES_SINGLE_BENEFIT_PAYMENT,
    CLAIMS_SENIORS_CARE_CREDIT,
    COMMUNITY_FOOD_PROGRAM_DONATIONS,
    COOP_CLAIMED_AS_PARTNERSHIP_MEMBER,
    COOP_EDUCATION_PAYROLL,
    COOP_EDUCATION_PLACEMENT_EXPENDITURES,
    COOP_EDUCATION_PLACEMENTS,
    COOP_PARTNERSHIP_BUSINESS_NUMBER,
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    FERTILITY_EXPENSES,
    FLOW_THROUGH_SHARE_SLIP_EXPENSES,
    FLOW_THROUGH_SHARE_SLIPS,
    LIVED_IN_STUDENT_RESIDENCE,
    PROPERTY_TAX_PAID,
    PUBLIC_LONG_TERM_CARE_PAID,
    RENT_PAID,
    RESERVE_HOME_ENERGY_COSTS,
    SENIORS_TRANSIT_PAID,
    SEPARATE_RESIDENCES_FOR_MEDICAL_REASONS,
)
from app.main import build_tax_computation

D = Decimal


CA_ON = JurisdictionCode("CA-ON")


# Every amount computed from a rate, fraction, amount or chart on the forms is rounded half-up to
# the cent, each line being a dollars-and-cents box: Schedule 8 Part 3a lines 25 and 28 say "(in
# dollars and cents)", the EI premiums are in dollars and cents too, T4127's BPAF rounding footnote
# rounds the federal basic personal amount so, and every other line is so by the owner's decision.
CENT = RoundTo(D("0.01"), RoundingMode.HALF_UP)


FEDERAL_POLITICAL_COLUMN_LINES = {
    1: {
        2: POLITICAL_CREDIT_COLUMN_1_LINE_2,
        3: POLITICAL_CREDIT_COLUMN_1_LINE_3,
        5: POLITICAL_CREDIT_COLUMN_1_LINE_5,
        6: POLITICAL_CREDIT_COLUMN_1_LINE_6,
        7: POLITICAL_CREDIT_COLUMN_1_LINE_7,
    },
    2: {
        2: POLITICAL_CREDIT_COLUMN_2_LINE_2,
        3: POLITICAL_CREDIT_COLUMN_2_LINE_3,
        5: POLITICAL_CREDIT_COLUMN_2_LINE_5,
        6: POLITICAL_CREDIT_COLUMN_2_LINE_6,
        7: POLITICAL_CREDIT_COLUMN_2_LINE_7,
    },
    3: {
        2: POLITICAL_CREDIT_COLUMN_3_LINE_2,
        3: POLITICAL_CREDIT_COLUMN_3_LINE_3,
        5: POLITICAL_CREDIT_COLUMN_3_LINE_5,
        6: POLITICAL_CREDIT_COLUMN_3_LINE_6,
        7: POLITICAL_CREDIT_COLUMN_3_LINE_7,
    },
}


POLITICAL_COLUMN_LINES = {
    1: {
        2: ontario.POLITICAL_CREDIT_COLUMN_1_LINE_2,
        3: ontario.POLITICAL_CREDIT_COLUMN_1_LINE_3,
        5: ontario.POLITICAL_CREDIT_COLUMN_1_LINE_5,
        6: ontario.POLITICAL_CREDIT_COLUMN_1_LINE_6,
        7: ontario.POLITICAL_CREDIT_COLUMN_1_LINE_7,
    },
    2: {
        2: ontario.POLITICAL_CREDIT_COLUMN_2_LINE_2,
        3: ontario.POLITICAL_CREDIT_COLUMN_2_LINE_3,
        5: ontario.POLITICAL_CREDIT_COLUMN_2_LINE_5,
        6: ontario.POLITICAL_CREDIT_COLUMN_2_LINE_6,
        7: ontario.POLITICAL_CREDIT_COLUMN_2_LINE_7,
    },
    3: {
        2: ontario.POLITICAL_CREDIT_COLUMN_3_LINE_2,
        3: ontario.POLITICAL_CREDIT_COLUMN_3_LINE_3,
        5: ontario.POLITICAL_CREDIT_COLUMN_3_LINE_5,
        6: ontario.POLITICAL_CREDIT_COLUMN_3_LINE_6,
        7: ontario.POLITICAL_CREDIT_COLUMN_3_LINE_7,
    },
}


def service() -> TaxComputationService:
    return build_tax_computation()


def slips(*expenses: str) -> Artifact[RecordList]:
    """The Form T1221 slips, one record per amount of qualifying expenses, in the order given."""
    records = [{FLOW_THROUGH_SHARE_SLIP_EXPENSES: D(amount)} for amount in expenses]
    return Artifact(FLOW_THROUGH_SHARE_SLIPS, RecordList(FLOW_THROUGH_SHARE_SLIPS.fields, records))


def placement_list(*expenditures: str) -> Artifact[RecordList]:
    """The work placements, one record per amount of eligible expenditures, in the order given."""
    records = [{COOP_EDUCATION_PLACEMENT_EXPENDITURES: D(amount)} for amount in expenditures]
    return Artifact(
        COOP_EDUCATION_PLACEMENTS, RecordList(COOP_EDUCATION_PLACEMENTS.fields, records)
    )


def rental_properties_list(*rows: tuple[int, str, str]) -> Artifact[RecordList]:
    """The Form T776 Part 3 rows, one record per (units, short-term rents, all rents)."""
    records: list[dict[ArtifactKind[Any], object]] = [
        {
            RENTAL_PROPERTY_UNITS: units,
            RENTAL_PROPERTY_SHORT_TERM_RENTS: D(short_term),
            RENTAL_PROPERTY_GROSS_RENTS: D(gross),
        }
        for units, short_term, gross in rows
    ]
    return Artifact(RENTAL_PROPERTIES, RecordList(RENTAL_PROPERTIES.fields, records))


def rental_cca_classes(
    *rows: tuple[str, str, str, str, str, str, str, int],
) -> Artifact[RecordList]:
    """The Form T776 Area A rows, one record per class: column 1 (class number), column 2, column
    3, column 5, column 11, column 12, the CCA claimed (column 23) as decimal text, and 1 if no
    property is left in the class, else 0 (Note 3)."""
    records: list[dict[ArtifactKind[Any], object]] = [
        {
            CCA_CLASS_NUMBER: D(class_number),
            CCA_UCC_AT_START: D(ucc_at_start),
            CCA_ADDITIONS: D(additions),
            CCA_PROCEEDS: D(proceeds),
            CCA_AIIP_ADDITIONS: D(aiip_additions),
            CCA_RIIP_ADDITIONS: D(riip_additions),
            CCA_CLAIMED: D(claimed),
            CCA_NO_PROPERTY_LEFT: no_property_left,
        }
        for (
            class_number,
            ucc_at_start,
            additions,
            proceeds,
            aiip_additions,
            riip_additions,
            claimed,
            no_property_left,
        ) in rows
    ]
    return Artifact(RENTAL_CCA_CLASSES, RecordList(RENTAL_CCA_CLASSES.fields, records))


def short_term_rental_units(*rows: tuple[str, int, int]) -> Artifact[RecordList]:
    """The Form T776 Chart A rows, one record per (column 3, column 4, column 5)."""
    records: list[dict[ArtifactKind[Any], object]] = [
        {
            SHORT_TERM_RENTAL_RELATED_EXPENSES: D(expenses),
            SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS: non_compliant_days,
            SHORT_TERM_RENTAL_DAYS: days,
        }
        for expenses, non_compliant_days, days in rows
    ]
    return Artifact(SHORT_TERM_RENTAL_UNITS, RecordList(SHORT_TERM_RENTAL_UNITS.fields, records))


def short_term_rental_cca_units(*rows: tuple[str, str, int, int]) -> Artifact[RecordList]:
    """The Form T776 Chart B rows, one record per (column 1, column 4, column 5, column 6)."""
    records: list[dict[ArtifactKind[Any], object]] = [
        {
            CCA_CLASS_NUMBER: D(class_number),
            SHORT_TERM_RENTAL_RELATED_CCA: D(related_cca),
            SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS: non_compliant_days,
            SHORT_TERM_RENTAL_DAYS: days,
        }
        for class_number, related_cca, non_compliant_days, days in rows
    ]
    return Artifact(
        SHORT_TERM_RENTAL_CCA_UNITS, RecordList(SHORT_TERM_RENTAL_CCA_UNITS.fields, records)
    )


# The Form T776 Part 4 expense lines by name, each with the kinds of its three boxes: "Total
# expenses", "Personal portion of total expenses" and "Short-term rental portion of total
# expenses".
RENTAL_EXPENSE_KINDS: dict[str, tuple[ArtifactKind[Decimal], ...]] = {
    "advertising": (
        RENTAL_ADVERTISING,
        RENTAL_ADVERTISING_PERSONAL_PORTION,
        RENTAL_ADVERTISING_SHORT_TERM_PORTION,
    ),
    "insurance": (
        RENTAL_INSURANCE,
        RENTAL_INSURANCE_PERSONAL_PORTION,
        RENTAL_INSURANCE_SHORT_TERM_PORTION,
    ),
    "interest_and_bank_charges": (
        RENTAL_INTEREST_AND_BANK_CHARGES,
        RENTAL_INTEREST_AND_BANK_CHARGES_PERSONAL_PORTION,
        RENTAL_INTEREST_AND_BANK_CHARGES_SHORT_TERM_PORTION,
    ),
    "office_expenses": (
        RENTAL_OFFICE_EXPENSES,
        RENTAL_OFFICE_EXPENSES_PERSONAL_PORTION,
        RENTAL_OFFICE_EXPENSES_SHORT_TERM_PORTION,
    ),
    "professional_fees": (
        RENTAL_PROFESSIONAL_FEES,
        RENTAL_PROFESSIONAL_FEES_PERSONAL_PORTION,
        RENTAL_PROFESSIONAL_FEES_SHORT_TERM_PORTION,
    ),
    "management_and_administration_fees": (
        RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES,
        RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_PERSONAL_PORTION,
        RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_SHORT_TERM_PORTION,
    ),
    "repairs_and_maintenance": (
        RENTAL_REPAIRS_AND_MAINTENANCE,
        RENTAL_REPAIRS_AND_MAINTENANCE_PERSONAL_PORTION,
        RENTAL_REPAIRS_AND_MAINTENANCE_SHORT_TERM_PORTION,
    ),
    "salaries_wages_and_benefits": (
        RENTAL_SALARIES_WAGES_AND_BENEFITS,
        RENTAL_SALARIES_WAGES_AND_BENEFITS_PERSONAL_PORTION,
        RENTAL_SALARIES_WAGES_AND_BENEFITS_SHORT_TERM_PORTION,
    ),
    "property_taxes": (
        RENTAL_PROPERTY_TAXES,
        RENTAL_PROPERTY_TAXES_PERSONAL_PORTION,
        RENTAL_PROPERTY_TAXES_SHORT_TERM_PORTION,
    ),
    "travel": (RENTAL_TRAVEL, RENTAL_TRAVEL_PERSONAL_PORTION, RENTAL_TRAVEL_SHORT_TERM_PORTION),
    "utilities": (
        RENTAL_UTILITIES,
        RENTAL_UTILITIES_PERSONAL_PORTION,
        RENTAL_UTILITIES_SHORT_TERM_PORTION,
    ),
    "motor_vehicle_expenses": (
        RENTAL_MOTOR_VEHICLE_EXPENSES,
        RENTAL_MOTOR_VEHICLE_EXPENSES_PERSONAL_PORTION,
        RENTAL_MOTOR_VEHICLE_EXPENSES_SHORT_TERM_PORTION,
    ),
    "other_expenses": (
        RENTAL_OTHER_EXPENSES,
        RENTAL_OTHER_EXPENSES_PERSONAL_PORTION,
        RENTAL_OTHER_EXPENSES_SHORT_TERM_PORTION,
    ),
}


def rental_expense_artifacts(
    amounts: Mapping[str, tuple[str, str, str]],
) -> list[Artifact[Decimal]]:
    """The 39 expense boxes: each line's (total, personal portion, short-term portion), else 0."""
    assert set(amounts) <= set(RENTAL_EXPENSE_KINDS)
    artifacts: list[Artifact[Decimal]] = []
    for name, kinds in RENTAL_EXPENSE_KINDS.items():
        for kind, amount in zip(kinds, amounts.get(name, ("0", "0", "0")), strict=True):
            artifacts.append(Artifact(kind, D(amount)))
    return artifacts


def trip(individual: int, zone: int, column_3: str, column_4: str, column_5: str) -> dict[Any, Any]:
    """A Form T2222 Chart B record: the individual, the zone (1 for A, 2 for B), columns 3 to 5."""
    return {
        TRAVEL_INDIVIDUAL: individual,
        TRIP_ZONE: zone,
        TRIP_BENEFIT_OR_STANDARD_AMOUNT: D(column_3),
        TRIP_TRAVEL_EXPENSES: D(column_4),
        TRIP_LOWEST_RETURN_AIRFARE: D(column_5),
    }


def individual(
    number: int, first: str = "0", second: str = "0", third: str = "0"
) -> dict[Any, Any]:
    """A Form T2222 Chart A record: the individual and the three row B amounts."""
    return {
        TRAVEL_INDIVIDUAL: number,
        STANDARD_AMOUNT_ALLOCATED_1: D(first),
        STANDARD_AMOUNT_ALLOCATED_2: D(second),
        STANDARD_AMOUNT_ALLOCATED_3: D(third),
    }


Disposition = tuple[str, str, str]
"""One disposition row of Schedule 3 Part 3: proceeds (column 2), adjusted cost base (column 3)
and outlays and expenses (column 4)."""


def dispositions(kind: RecordListKind, *rows: Disposition) -> Artifact[RecordList]:
    """A Schedule 3 Part 3 record list of `kind` with one record per row, in the order given."""
    records: list[dict[ArtifactKind[Any], object]] = [
        {
            DISPOSITION_PROCEEDS: D(proceeds),
            DISPOSITION_ADJUSTED_COST_BASE: D(cost_base),
            DISPOSITION_OUTLAYS: D(outlays),
        }
        for proceeds, cost_base, outlays in rows
    ]
    return Artifact(kind, RecordList(kind.fields, records))


ResidenceProperty = tuple[int, int, int, int, str, str, str, int]
"""One Form T2091(IND) property: the years designated after 1981 and from 1972 to 1981 (lines 1
and 2), the years owned in the same periods (lines 5 and 6), the proceeds of disposition (line 8),
the outlays and expenses (line 9), the adjusted cost base (line 10) and 1 if the "plus one" rule
applies, else 0."""


def principal_residence_properties(*rows: ResidenceProperty) -> Artifact[RecordList]:
    """The Form T2091(IND) properties, one record per row, in the order given."""
    records: list[dict[ArtifactKind[Any], object]] = [
        {
            RESIDENCE_YEARS_DESIGNATED_AFTER_1981: designated_after,
            RESIDENCE_YEARS_DESIGNATED_1972_TO_1981: designated_before,
            RESIDENCE_YEARS_OWNED_AFTER_1981: owned_after,
            RESIDENCE_YEARS_OWNED_1972_TO_1981: owned_before,
            RESIDENCE_PROCEEDS: D(proceeds),
            RESIDENCE_OUTLAYS: D(outlays),
            RESIDENCE_ADJUSTED_COST_BASE: D(cost_base),
            RESIDENCE_PLUS_ONE_YEAR: plus_one,
        }
        for (
            designated_after,
            designated_before,
            owned_after,
            owned_before,
            proceeds,
            outlays,
            cost_base,
            plus_one,
        ) in rows
    ]
    return Artifact(
        PRINCIPAL_RESIDENCE_PROPERTIES, RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, records)
    )


def compute(
    employment_income: str,
    share_dispositions: tuple[Disposition, ...],
    unused_rrsp_contributions: str,
    rrsp_contributions: str,
    rrsp_deduction_limit: str,
    rrsp_amount_deducted: str,
    union_dues: str,
    *,
    qsbcs_dispositions: tuple[Disposition, ...] = (),
    qffp_dispositions: tuple[Disposition, ...] = (),
    qffp_foreclosure_dispositions: tuple[Disposition, ...] = (),
    real_estate_dispositions: tuple[Disposition, ...] = (),
    bond_dispositions: tuple[Disposition, ...] = (),
    crypto_asset_dispositions: tuple[Disposition, ...] = (),
    other_foreclosure_dispositions: tuple[Disposition, ...] = (),
    personal_use_property_dispositions: tuple[Disposition, ...] = (),
    listed_personal_property_dispositions: tuple[Disposition, ...] = (),
    principal_residence_properties_rows: tuple[ResidenceProperty, ...] = (),
    unapplied_listed_personal_property_losses: str = "0",
    capital_gains_deferral: str = "0",
    slip_capital_gains_or_losses: str = "0",
    t3_capital_gains_or_losses: str = "0",
    capital_gains_reserves: str = "0",
    partnership_gains_at_full_inclusion: str = "0",
    other_employment_income: str = "0",
    old_age_security: str = "0",
    cpp_or_qpp_benefits: str = "0",
    other_pensions_and_superannuation: str = "0",
    elected_split_pension_amount: str = "0",
    universal_child_care_benefit: str = "0",
    ei_and_other_benefits: str = "0",
    t3_taxable_dividends_other_than_eligible: str = "0",
    t4ps_taxable_dividends_other_than_eligible: str = "0",
    t5_taxable_dividends_other_than_eligible: str = "0",
    t5013_taxable_dividends_other_than_eligible: str = "0",
    t3_taxable_dividends: str = "0",
    t4ps_taxable_dividends: str = "0",
    t5_taxable_dividends: str = "0",
    t5013_taxable_dividends: str = "0",
    eligible_dividends_received_without_a_slip: str = "0",
    other_dividends_received_without_a_slip: str = "0",
    t3_dividend_tax_credit: str = "0",
    t4ps_dividend_tax_credit: str = "0",
    t5_dividend_tax_credit: str = "0",
    t5013_dividend_tax_credit: str = "0",
    t3_investment_income: str = "0",
    t5_investment_income: str = "0",
    t5013_investment_income: str = "0",
    investment_income_credited_not_received: str = "0",
    tax_refund_interest: str = "0",
    foreign_investment_income: str = "0",
    investment_income_without_a_slip: str = "0",
    investment_royalties: str = "0",
    investment_income_reported_in_previous_years: str = "0",
    net_partnership_income: str = "0",
    rdsp_income: str = "0",
    rental_properties: tuple[tuple[int, str, str], ...] = (),
    rental_other_income: str = "0",
    rental_expenses: Mapping[str, tuple[str, str, str]] | None = None,
    short_term_rental_units_rows: tuple[tuple[str, int, int], ...] = (),
    short_term_rental_cca_units_rows: tuple[tuple[str, str, int, int], ...] = (),
    rental_coowner: int = 0,
    rental_coowner_share: str = "0",
    rental_coowner_other_expenses: str = "0",
    rental_cca_classes_rows: tuple[tuple[str, str, str, str, str, str, str, int], ...] = (),
    rental_coowner_recaptured_cca: str = "0",
    rental_coowner_terminal_loss: str = "0",
    rental_coowner_cca_claim: str = "0",
    rental_cca_personal_part: str = "0",
    rental_cca_business_use_of_home: str = "0",
    rental_partner: int = 0,
    rental_partner_share: str = "0",
    rental_partner_gst_hst_rebate: str = "0",
    rental_partner_other_expenses: str = "0",
    taxable_support_payments: str = "0",
    rrsp_income: str = "0",
    fhsa_income: str = "0",
    other_fhsa_income: str = "0",
    other_income: str = "0",
    taxable_scholarships: str = "0",
    workers_compensation_benefits: str = "0",
    social_assistance_payments: str = "0",
    net_federal_supplements: str = "0",
    uccb_repayment: str = "0",
    rdsp_income_repayment: str = "0",
    oas_overpayment_recovered: str = "0",
    ei_benefits_repayment: str = "0",
    canadian_armed_forces_and_police_deduction: str = "0",
    security_options_deductions: str = "0",
    limited_partnership_losses_of_other_years: str = "0",
    non_capital_losses_of_other_years: str = "0",
    additional_deductions: str = "0",
    other_payments_deduction_above_limit: str = "0",
    other_payments_worksheet_required: int = 0,
    other_payments_worksheet_line_9_over_limit: int = 0,
    rpp_deduction: str = "0",
    elected_split_pension_deduction: str = "0",
    support_payments_deduction: str = "0",
    exploration_and_development_expenses: str = "0",
    other_deductions: str = "0",
    total_carrying_charges: str = "0",
    total_interest_expenses: str = "0",
    total_other_expenses: str = "0",
    capital_gains_deductions_1985_to_1987: str = "0",
    capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property: str = "0",
    capital_gains_deductions_1988_and_1989_eligible_capital_property: str = "0",
    capital_gains_deductions_1990_to_1999: str = "0",
    capital_gains_deductions_2000: str = "0",
    capital_gains_deductions_2001_to_2024: str = "0",
    other_business_investment_loss_reductions_1986_to_1994: str = "0",
    other_business_investment_loss_reductions_1994_to_1996: str = "0",
    other_business_investment_loss_reductions_1997_to_1999: str = "0",
    other_business_investment_loss_reductions_2000: str = "0",
    other_business_investment_loss_reductions_2001_to_2023: str = "0",
    other_business_investment_loss_reductions_2024: str = "0",
    business_investment_loss: str = "0",
    fhsa_contributions_in_2025: str = "0",
    fhsa_contributions_in_2025_after_first_qualifying_withdrawal: str = "0",
    fhsa_variable_b_amount: str = "0",
    fhsa_designated_withdrawals_in_2025: str = "0",
    fhsa_contributions_in_2024: str = "0",
    fhsa_contributions_in_2024_before_first_qualifying_withdrawal: str = "0",
    fhsa_carryforward_for_2025: str = "0",
    fhsa_rrsp_transfers_in_2024_and_prior_years: str = "0",
    fhsa_rrsp_transfers_in_2025: str = "0",
    fhsa_designated_transfers_in_2024_and_prior_years: str = "0",
    fhsa_designated_transfers_in_2025: str = "0",
    fhsa_variable_h_amount: str = "0",
    fhsa_carryforward_for_2024: str = "0",
    fhsa_variable_f_amount: str = "0",
    fhsa_annual_limits_for_2024_and_prior_years: str = "0",
    fhsa_deductions_for_2024_and_prior_years: str = "0",
    fhsa_unused_contributions_brought_forward: str = "0",
    fhsa_contributions_deducted: str = "0",
    fhsa_maximum_participation_period_ended: int = 0,
    zone_a_days_lived: int = 0,
    zone_a_additional_residency_days: int = 0,
    zone_a_special_work_site_benefits: str = "0",
    zone_b_days_lived: int = 0,
    zone_b_additional_residency_days: int = 0,
    zone_b_special_work_site_benefits: str = "0",
    travel_trips: tuple[dict[Any, Any], ...] = (),
    travel_individuals: tuple[dict[Any, Any], ...] = (),
    dependent_children: int = 0,
    dependants: int = 0,
    eligible_dependants: int = 0,
    dependant_net_income: str = "0",
    infirm_children: int = 0,
    born_in_1960_or_earlier: int = 0,
    spouse_net_income: str = "0",
    spouses_claimed: int = 0,
    spouse_caregiver_eligible: int = 0,
    infirm_dependants: tuple[str, ...] = (),
    medical_expenses: str = "0",
    other_dependants: tuple[tuple[str, str], ...] = (),
    caregiver_dependants: tuple[tuple[str, int], ...] = (),
    disability_dependants: tuple[tuple[int, str, str, str], ...] = (),
    ontario_disability_dependants: tuple[tuple[int, str, str, str], ...] = (),
    ontario_disability_amount_for_self: str = "0",
    child_care_expenses_paid: str = "0",
    children_under_seven: int = 0,
    children_with_disability: int = 0,
    children_seven_to_sixteen: int = 0,
    cwb_eligible_dependants: int = 0,
    income_tax_deducted: str = "0",
    part_xii_2_tax_credit: str = "0",
    employee_and_partner_gst_hst_rebate: str = "0",
    educator_supplies_expenses: str = "0",
    journalism_labour_tax_credit: str = "0",
    tax_paid_by_instalments: str = "0",
    itc_recapture_expenditure_at_15_percent: str = "0",
    itc_recapture_expenditure_at_20_percent: str = "0",
    labour_sponsored_funds_net_cost: str = "0",
    advanced_canada_workers_benefit: str = "0",
    resp_aips_received_part_a: str = "0",
    resp_aips_rrsp_contributions: str = "0",
    resp_aips_reduction_used_in_previous_years: str = "0",
    resp_aips_received_part_b: str = "0",
    resp_aips_part_a_applies: int = 0,
    rl_10_labour_sponsored_fund_amount: str = "0",
    opportunities_fund_donation: str = "0",
    fertility_expenses: str = "0",
    claims_seniors_care_credit: int = 0,
    applies_for_energy_and_property_tax_credit: int = 0,
    applies_for_northern_energy_credit: int = 0,
    chooses_single_benefit_payment: int = 0,
    applies_for_senior_homeowners_grant: int = 0,
    separate_residences_for_medical_reasons: int = 0,
    lived_in_student_residence: int = 0,
    rent_paid: str = "0",
    property_tax_paid: str = "0",
    reserve_home_energy_costs: str = "0",
    public_long_term_care_paid: str = "0",
    seniors_transit_paid: str = "0",
    flow_through_share_slips: tuple[str, ...] = (),
    coop_education_payroll: str = "0",
    coop_education_placements: tuple[str, ...] = (),
    coop_claimed_as_partnership_member: int = 0,
    coop_partnership_business_number: str = "",
    community_food_program_donations: str = "0",
    charitable_donations: str = "0",
    government_donations: str = "0",
    university_donations_outside_canada: str = "0",
    foreign_charity_donations: str = "0",
    ecological_and_cultural_gifts: str = "0",
    ecological_gifts_before_2016: str = "0",
    depreciable_gift_recaptured_depreciation: str = "0",
    depreciable_gift_net_proceeds: str = "0",
    depreciable_gift_capital_cost: str = "0",
    capital_gift_taxable_gains: str = "0",
    capital_gift_gains_deduction: str = "0",
    political_contributions: str = "0",
    care_supporting_persons_adjusted_income: str = "0",
    federal_political_contributions: str = "0",
    disability_supports_deduction: str = "0",
    other_employment_expenses: str = "0",
    clergy_residence_deduction: str = "0",
    net_business_income: str = "0",
    net_professional_income: str = "0",
    net_commission_income: str = "0",
    net_farming_income: str = "0",
    net_fishing_income: str = "0",
    wage_loss_replacement_plan_income: str = "0",
    resident_in_canada_throughout_2025: int = 1,
    aged_18_or_older_at_end_of_2025: int = 1,
    spouse_net_income_before_adjustments: str = "0",
    spouse_uccb_repayment: str = "0",
    spouse_rdsp_income_repayment: str = "0",
    spouse_universal_child_care_benefit: str = "0",
    spouse_rdsp_income: str = "0",
    split_income_dividends: str = "0",
    split_income_dividends_other_than_eligible: str = "0",
    other_split_income: str = "0",
    disability_amount_for_self: str = "0",
    unapplied_net_capital_losses_1985_to_1987: str = "0",
    unapplied_net_capital_losses_1988_and_1989: str = "0",
    unapplied_net_capital_losses_1990_to_1999: str = "0",
    unapplied_net_capital_losses_2001_to_2024: str = "0",
    net_capital_losses_claimed: str = "0",
    business_income: str = "0",
    professional_income: str = "0",
    commission_income: str = "0",
    farming_income: str = "0",
    fishing_income: str = "0",
    cpp_months: int = 12,
    cpt20_earnings: str = "0",
    cpp_part_4_completed: int = 0,
    ei_controlled_corporation_earnings: str = "0",
    ei_exempt_self_employment_income: str = "0",
    ei_insurable_earnings: str = "0",
    ei_special_benefits_agreement: int = 0,
    canadian_tuition_fees: str = "0",
    canada_training_credit_limit: str = "0",
    canada_training_credit_claimed: str = "0",
    foreign_tuition_fees: str = "0",
    unused_tuition_from_2024: str = "0",
    tuition_transfer_elected: str = "0",
    tuition_transferred_from_child: str = "0",
    spouse_return_age_amount: str = "0",
    spouse_return_infirm_children_amount: str = "0",
    spouse_return_pension_income_amount: str = "0",
    spouse_return_disability_amount: str = "0",
    spouse_designated_tuition: str = "0",
    spouse_return_taxable_income: str = "0",
    spouse_return_federal_basic_tax: str = "0",
    spouse_return_basic_personal_amount: str = "0",
    spouse_return_line_96: str = "0",
    spouse_return_federal_tuition_amount: str = "0",
    spouse_not_separated_90_days: int = 0,
    spouse_return_ontario_age_amount: str = "0",
    spouse_return_ontario_pension_income_amount: str = "0",
    spouse_return_ontario_disability_amount: str = "0",
    spouse_return_ontario_basic_tax: str = "0",
    spouse_return_ontario_basic_personal_amount: str = "0",
    spouse_return_ontario_line_24: str = "0",
    spouse_return_ontario_unused_tuition_amount: str = "0",
    lift_spouse_at_year_end: int = 0,
    ontario_minimum_tax: str = "0",
    not_resident_of_canada_at_start_of_year: int = 0,
    not_resident_of_ontario_at_year_end: int = 0,
    bankrupt_in_year: int = 0,
    return_filed_by_trustee_in_bankruptcy: int = 0,
    not_claiming_ontario_tax_reduction: int = 0,
    spouse_or_common_law_partner_on_december_31: int = 0,
    claims_tax_reduction_amounts_at_equal_net_income: int = 0,
    unused_tuition_amounts_brought_forward: str = "0",
) -> Worksheet:
    return service().compute(
        CA_ON,
        2025,
        Artifact(EMPLOYMENT_INCOME, D(employment_income)),
        dispositions(QSBCS_DISPOSITIONS, *qsbcs_dispositions),
        dispositions(QFFP_DISPOSITIONS, *qffp_dispositions),
        dispositions(QFFP_FORECLOSURE_DISPOSITIONS, *qffp_foreclosure_dispositions),
        dispositions(SHARE_DISPOSITIONS, *share_dispositions),
        dispositions(REAL_ESTATE_DISPOSITIONS, *real_estate_dispositions),
        dispositions(BOND_DISPOSITIONS, *bond_dispositions),
        dispositions(CRYPTO_ASSET_DISPOSITIONS, *crypto_asset_dispositions),
        dispositions(OTHER_FORECLOSURE_DISPOSITIONS, *other_foreclosure_dispositions),
        dispositions(PERSONAL_USE_PROPERTY_DISPOSITIONS, *personal_use_property_dispositions),
        dispositions(LISTED_PERSONAL_PROPERTY_DISPOSITIONS, *listed_personal_property_dispositions),
        principal_residence_properties(*principal_residence_properties_rows),
        Artifact(
            UNAPPLIED_LISTED_PERSONAL_PROPERTY_LOSSES, D(unapplied_listed_personal_property_losses)
        ),
        Artifact(CAPITAL_GAINS_DEFERRAL, D(capital_gains_deferral)),
        Artifact(SLIP_CAPITAL_GAINS_OR_LOSSES, D(slip_capital_gains_or_losses)),
        Artifact(T3_CAPITAL_GAINS_OR_LOSSES, D(t3_capital_gains_or_losses)),
        Artifact(CAPITAL_GAINS_RESERVES, D(capital_gains_reserves)),
        Artifact(PARTNERSHIP_GAINS_AT_FULL_INCLUSION, D(partnership_gains_at_full_inclusion)),
        Artifact(OTHER_EMPLOYMENT_INCOME, D(other_employment_income)),
        Artifact(OLD_AGE_SECURITY, D(old_age_security)),
        Artifact(CPP_OR_QPP_BENEFITS, D(cpp_or_qpp_benefits)),
        Artifact(OTHER_PENSIONS_AND_SUPERANNUATION, D(other_pensions_and_superannuation)),
        Artifact(ELECTED_SPLIT_PENSION_AMOUNT, D(elected_split_pension_amount)),
        Artifact(UNIVERSAL_CHILD_CARE_BENEFIT, D(universal_child_care_benefit)),
        Artifact(EI_AND_OTHER_BENEFITS, D(ei_and_other_benefits)),
        Artifact(
            T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D(t3_taxable_dividends_other_than_eligible)
        ),
        Artifact(
            T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            D(t4ps_taxable_dividends_other_than_eligible),
        ),
        Artifact(
            T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D(t5_taxable_dividends_other_than_eligible)
        ),
        Artifact(
            T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            D(t5013_taxable_dividends_other_than_eligible),
        ),
        Artifact(T3_TAXABLE_DIVIDENDS, D(t3_taxable_dividends)),
        Artifact(T4PS_TAXABLE_DIVIDENDS, D(t4ps_taxable_dividends)),
        Artifact(T5_TAXABLE_DIVIDENDS, D(t5_taxable_dividends)),
        Artifact(T5013_TAXABLE_DIVIDENDS, D(t5013_taxable_dividends)),
        Artifact(
            ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
            D(eligible_dividends_received_without_a_slip),
        ),
        Artifact(
            OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP, D(other_dividends_received_without_a_slip)
        ),
        Artifact(T3_DIVIDEND_TAX_CREDIT, D(t3_dividend_tax_credit)),
        Artifact(T4PS_DIVIDEND_TAX_CREDIT, D(t4ps_dividend_tax_credit)),
        Artifact(T5_DIVIDEND_TAX_CREDIT, D(t5_dividend_tax_credit)),
        Artifact(T5013_DIVIDEND_TAX_CREDIT, D(t5013_dividend_tax_credit)),
        Artifact(T3_INVESTMENT_INCOME, D(t3_investment_income)),
        Artifact(T5_INVESTMENT_INCOME, D(t5_investment_income)),
        Artifact(T5013_INVESTMENT_INCOME, D(t5013_investment_income)),
        Artifact(
            INVESTMENT_INCOME_CREDITED_NOT_RECEIVED, D(investment_income_credited_not_received)
        ),
        Artifact(TAX_REFUND_INTEREST, D(tax_refund_interest)),
        Artifact(FOREIGN_INVESTMENT_INCOME, D(foreign_investment_income)),
        Artifact(INVESTMENT_INCOME_WITHOUT_A_SLIP, D(investment_income_without_a_slip)),
        Artifact(INVESTMENT_ROYALTIES, D(investment_royalties)),
        Artifact(
            INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
            D(investment_income_reported_in_previous_years),
        ),
        Artifact(NET_PARTNERSHIP_INCOME, D(net_partnership_income)),
        Artifact(RDSP_INCOME, D(rdsp_income)),
        rental_properties_list(*rental_properties),
        Artifact(RENTAL_OTHER_INCOME, D(rental_other_income)),
        *rental_expense_artifacts(rental_expenses or {}),
        short_term_rental_units(*short_term_rental_units_rows),
        short_term_rental_cca_units(*short_term_rental_cca_units_rows),
        Artifact(RENTAL_COOWNER, rental_coowner),
        Artifact(RENTAL_COOWNER_SHARE, D(rental_coowner_share)),
        Artifact(RENTAL_COOWNER_OTHER_EXPENSES, D(rental_coowner_other_expenses)),
        rental_cca_classes(*rental_cca_classes_rows),
        Artifact(RENTAL_COOWNER_RECAPTURED_CCA, D(rental_coowner_recaptured_cca)),
        Artifact(RENTAL_COOWNER_TERMINAL_LOSS, D(rental_coowner_terminal_loss)),
        Artifact(RENTAL_COOWNER_CCA_CLAIM, D(rental_coowner_cca_claim)),
        Artifact(RENTAL_CCA_PERSONAL_PART, D(rental_cca_personal_part)),
        Artifact(RENTAL_CCA_BUSINESS_USE_OF_HOME, D(rental_cca_business_use_of_home)),
        Artifact(RENTAL_PARTNER, rental_partner),
        Artifact(RENTAL_PARTNER_SHARE, D(rental_partner_share)),
        Artifact(RENTAL_PARTNER_GST_HST_REBATE, D(rental_partner_gst_hst_rebate)),
        Artifact(RENTAL_PARTNER_OTHER_EXPENSES, D(rental_partner_other_expenses)),
        Artifact(TAXABLE_SUPPORT_PAYMENTS, D(taxable_support_payments)),
        Artifact(RRSP_INCOME, D(rrsp_income)),
        Artifact(FHSA_INCOME, D(fhsa_income)),
        Artifact(OTHER_FHSA_INCOME, D(other_fhsa_income)),
        Artifact(OTHER_INCOME, D(other_income)),
        Artifact(TAXABLE_SCHOLARSHIPS, D(taxable_scholarships)),
        Artifact(WORKERS_COMPENSATION_BENEFITS, D(workers_compensation_benefits)),
        Artifact(SOCIAL_ASSISTANCE_PAYMENTS, D(social_assistance_payments)),
        Artifact(NET_FEDERAL_SUPPLEMENTS, D(net_federal_supplements)),
        Artifact(UCCB_REPAYMENT, D(uccb_repayment)),
        Artifact(RDSP_INCOME_REPAYMENT, D(rdsp_income_repayment)),
        Artifact(OAS_OVERPAYMENT_RECOVERED, D(oas_overpayment_recovered)),
        Artifact(EI_BENEFITS_REPAYMENT, D(ei_benefits_repayment)),
        Artifact(
            CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
            D(canadian_armed_forces_and_police_deduction),
        ),
        Artifact(SECURITY_OPTIONS_DEDUCTIONS, D(security_options_deductions)),
        Artifact(
            LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS, D(limited_partnership_losses_of_other_years)
        ),
        Artifact(NON_CAPITAL_LOSSES_OF_OTHER_YEARS, D(non_capital_losses_of_other_years)),
        Artifact(ADDITIONAL_DEDUCTIONS, D(additional_deductions)),
        Artifact(OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT, D(other_payments_deduction_above_limit)),
        Artifact(OTHER_PAYMENTS_WORKSHEET_REQUIRED, other_payments_worksheet_required),
        Artifact(
            OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT, other_payments_worksheet_line_9_over_limit
        ),
        Artifact(RPP_DEDUCTION, D(rpp_deduction)),
        Artifact(ELECTED_SPLIT_PENSION_DEDUCTION, D(elected_split_pension_deduction)),
        Artifact(SUPPORT_PAYMENTS_DEDUCTION, D(support_payments_deduction)),
        Artifact(EXPLORATION_AND_DEVELOPMENT_EXPENSES, D(exploration_and_development_expenses)),
        Artifact(OTHER_DEDUCTIONS, D(other_deductions)),
        Artifact(TOTAL_CARRYING_CHARGES, D(total_carrying_charges)),
        Artifact(TOTAL_INTEREST_EXPENSES, D(total_interest_expenses)),
        Artifact(TOTAL_OTHER_EXPENSES, D(total_other_expenses)),
        Artifact(CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987, D(capital_gains_deductions_1985_to_1987)),
        Artifact(
            CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
            D(capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property),
        ),
        Artifact(
            CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
            D(capital_gains_deductions_1988_and_1989_eligible_capital_property),
        ),
        Artifact(CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999, D(capital_gains_deductions_1990_to_1999)),
        Artifact(CAPITAL_GAINS_DEDUCTIONS_2000, D(capital_gains_deductions_2000)),
        Artifact(CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024, D(capital_gains_deductions_2001_to_2024)),
        Artifact(
            OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
            D(other_business_investment_loss_reductions_1986_to_1994),
        ),
        Artifact(
            OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
            D(other_business_investment_loss_reductions_1994_to_1996),
        ),
        Artifact(
            OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
            D(other_business_investment_loss_reductions_1997_to_1999),
        ),
        Artifact(
            OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
            D(other_business_investment_loss_reductions_2000),
        ),
        Artifact(
            OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
            D(other_business_investment_loss_reductions_2001_to_2023),
        ),
        Artifact(
            OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
            D(other_business_investment_loss_reductions_2024),
        ),
        Artifact(BUSINESS_INVESTMENT_LOSS, D(business_investment_loss)),
        Artifact(FHSA_CONTRIBUTIONS_IN_2025, D(fhsa_contributions_in_2025)),
        Artifact(
            FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
            D(fhsa_contributions_in_2025_after_first_qualifying_withdrawal),
        ),
        Artifact(FHSA_VARIABLE_B_AMOUNT, D(fhsa_variable_b_amount)),
        Artifact(FHSA_DESIGNATED_WITHDRAWALS_IN_2025, D(fhsa_designated_withdrawals_in_2025)),
        Artifact(FHSA_CONTRIBUTIONS_IN_2024, D(fhsa_contributions_in_2024)),
        Artifact(
            FHSA_CONTRIBUTIONS_IN_2024_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
            D(fhsa_contributions_in_2024_before_first_qualifying_withdrawal),
        ),
        Artifact(FHSA_CARRYFORWARD_FOR_2025, D(fhsa_carryforward_for_2025)),
        Artifact(
            FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
            D(fhsa_rrsp_transfers_in_2024_and_prior_years),
        ),
        Artifact(FHSA_RRSP_TRANSFERS_IN_2025, D(fhsa_rrsp_transfers_in_2025)),
        Artifact(
            FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
            D(fhsa_designated_transfers_in_2024_and_prior_years),
        ),
        Artifact(FHSA_DESIGNATED_TRANSFERS_IN_2025, D(fhsa_designated_transfers_in_2025)),
        Artifact(FHSA_VARIABLE_H_AMOUNT, D(fhsa_variable_h_amount)),
        Artifact(FHSA_CARRYFORWARD_FOR_2024, D(fhsa_carryforward_for_2024)),
        Artifact(FHSA_VARIABLE_F_AMOUNT, D(fhsa_variable_f_amount)),
        Artifact(
            FHSA_ANNUAL_LIMITS_FOR_2024_AND_PRIOR_YEARS,
            D(fhsa_annual_limits_for_2024_and_prior_years),
        ),
        Artifact(
            FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS, D(fhsa_deductions_for_2024_and_prior_years)
        ),
        Artifact(
            FHSA_UNUSED_CONTRIBUTIONS_BROUGHT_FORWARD, D(fhsa_unused_contributions_brought_forward)
        ),
        Artifact(FHSA_CONTRIBUTIONS_DEDUCTED, D(fhsa_contributions_deducted)),
        Artifact(FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED, fhsa_maximum_participation_period_ended),
        Artifact(ZONE_A_DAYS_LIVED, zone_a_days_lived),
        Artifact(ZONE_A_ADDITIONAL_RESIDENCY_DAYS, zone_a_additional_residency_days),
        Artifact(ZONE_A_SPECIAL_WORK_SITE_BENEFITS, D(zone_a_special_work_site_benefits)),
        Artifact(ZONE_B_DAYS_LIVED, zone_b_days_lived),
        Artifact(ZONE_B_ADDITIONAL_RESIDENCY_DAYS, zone_b_additional_residency_days),
        Artifact(ZONE_B_SPECIAL_WORK_SITE_BENEFITS, D(zone_b_special_work_site_benefits)),
        Artifact(TRAVEL_TRIPS, RecordList(TRAVEL_TRIPS.fields, travel_trips)),
        Artifact(TRAVEL_INDIVIDUALS, RecordList(TRAVEL_INDIVIDUALS.fields, travel_individuals)),
        Artifact(UNUSED_RRSP_CONTRIBUTIONS, D(unused_rrsp_contributions)),
        Artifact(RRSP_CONTRIBUTIONS, D(rrsp_contributions)),
        Artifact(RRSP_DEDUCTION_LIMIT, D(rrsp_deduction_limit)),
        Artifact(RRSP_AMOUNT_DEDUCTED, D(rrsp_amount_deducted)),
        Artifact(UNION_DUES, D(union_dues)),
        Artifact(DEPENDENT_CHILDREN, dependent_children),
        Artifact(DEPENDANTS, dependants),
        Artifact(ELIGIBLE_DEPENDANTS, eligible_dependants),
        Artifact(DEPENDANT_NET_INCOME, D(dependant_net_income)),
        Artifact(
            INFIRM_DEPENDANTS,
            RecordList(
                INFIRM_DEPENDANTS.fields,
                [{DEPENDANT_NET_INCOME: D(income)} for income in infirm_dependants],
            ),
        ),
        Artifact(MEDICAL_EXPENSES, D(medical_expenses)),
        Artifact(
            OTHER_DEPENDANTS,
            RecordList(
                OTHER_DEPENDANTS.fields,
                [
                    {
                        OTHER_DEPENDANT_MEDICAL_EXPENSES: D(expenses),
                        DEPENDANT_NET_INCOME: D(income),
                    }
                    for expenses, income in other_dependants
                ],
            ),
        ),
        Artifact(
            ontario.CAREGIVER_DEPENDANTS,
            RecordList(
                ontario.CAREGIVER_DEPENDANTS.fields,
                [
                    {
                        DEPENDANT_NET_INCOME: D(income),
                        ontario.CLAIMED_AS_ELIGIBLE_DEPENDANT: claimed,
                    }
                    for income, claimed in caregiver_dependants
                ],
            ),
        ),
        Artifact(ontario.DISABILITY_AMOUNT_FOR_SELF, D(ontario_disability_amount_for_self)),
        Artifact(
            ontario.DISABILITY_DEPENDANTS,
            RecordList(
                ontario.DISABILITY_DEPENDANTS.fields,
                [
                    {
                        DEPENDANT_UNDER_18: under_18,
                        DEPENDANT_CARE_EXPENSES: D(care_expenses),
                        ontario.DEPENDANT_ON428_LINE_28: D(on428_line_28),
                        DEPENDANT_TAXABLE_INCOME: D(taxable_income),
                    }
                    for under_18, care_expenses, on428_line_28, taxable_income in (
                        ontario_disability_dependants
                    )
                ],
            ),
        ),
        Artifact(
            DISABILITY_DEPENDANTS,
            RecordList(
                DISABILITY_DEPENDANTS.fields,
                [
                    {
                        DEPENDANT_UNDER_18: under_18,
                        DEPENDANT_CARE_EXPENSES: D(care_expenses),
                        DEPENDANT_CREDIT_AMOUNTS: D(credit_amounts),
                        DEPENDANT_TAXABLE_INCOME: D(taxable_income),
                    }
                    for under_18, care_expenses, credit_amounts, taxable_income in (
                        disability_dependants
                    )
                ],
            ),
        ),
        Artifact(INFIRM_CHILDREN, infirm_children),
        Artifact(BORN_IN_1960_OR_EARLIER, born_in_1960_or_earlier),
        Artifact(SPOUSE_NET_INCOME, D(spouse_net_income)),
        Artifact(SPOUSES_CLAIMED, spouses_claimed),
        Artifact(SPOUSE_CAREGIVER_ELIGIBLE, spouse_caregiver_eligible),
        Artifact(CHILD_CARE_EXPENSES_PAID, D(child_care_expenses_paid)),
        Artifact(CHILDREN_UNDER_SEVEN, children_under_seven),
        Artifact(CHILDREN_WITH_DISABILITY, children_with_disability),
        Artifact(CHILDREN_SEVEN_TO_SIXTEEN, children_seven_to_sixteen),
        Artifact(CWB_ELIGIBLE_DEPENDANTS, cwb_eligible_dependants),
        Artifact(INCOME_TAX_DEDUCTED, D(income_tax_deducted)),
        Artifact(PART_XII_2_TAX_CREDIT, D(part_xii_2_tax_credit)),
        Artifact(EMPLOYEE_AND_PARTNER_GST_HST_REBATE, D(employee_and_partner_gst_hst_rebate)),
        Artifact(EDUCATOR_SUPPLIES_EXPENSES, D(educator_supplies_expenses)),
        Artifact(JOURNALISM_LABOUR_TAX_CREDIT, D(journalism_labour_tax_credit)),
        Artifact(TAX_PAID_BY_INSTALMENTS, D(tax_paid_by_instalments)),
        Artifact(
            ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT, D(itc_recapture_expenditure_at_15_percent)
        ),
        Artifact(
            ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT, D(itc_recapture_expenditure_at_20_percent)
        ),
        Artifact(LABOUR_SPONSORED_FUNDS_NET_COST, D(labour_sponsored_funds_net_cost)),
        Artifact(ADVANCED_CANADA_WORKERS_BENEFIT, D(advanced_canada_workers_benefit)),
        Artifact(RESP_AIPS_RECEIVED_PART_A, D(resp_aips_received_part_a)),
        Artifact(RESP_AIPS_RRSP_CONTRIBUTIONS, D(resp_aips_rrsp_contributions)),
        Artifact(
            RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS,
            D(resp_aips_reduction_used_in_previous_years),
        ),
        Artifact(RESP_AIPS_RECEIVED_PART_B, D(resp_aips_received_part_b)),
        Artifact(RESP_AIPS_PART_A_APPLIES, resp_aips_part_a_applies),
        Artifact(RL_10_LABOUR_SPONSORED_FUND_AMOUNT, D(rl_10_labour_sponsored_fund_amount)),
        Artifact(ontario.OPPORTUNITIES_FUND_DONATION, D(opportunities_fund_donation)),
        Artifact(FERTILITY_EXPENSES, D(fertility_expenses)),
        Artifact(CLAIMS_SENIORS_CARE_CREDIT, claims_seniors_care_credit),
        Artifact(
            APPLIES_FOR_ENERGY_AND_PROPERTY_TAX_CREDIT, applies_for_energy_and_property_tax_credit
        ),
        Artifact(APPLIES_FOR_NORTHERN_ENERGY_CREDIT, applies_for_northern_energy_credit),
        Artifact(CHOOSES_SINGLE_BENEFIT_PAYMENT, chooses_single_benefit_payment),
        Artifact(APPLIES_FOR_SENIOR_HOMEOWNERS_GRANT, applies_for_senior_homeowners_grant),
        Artifact(SEPARATE_RESIDENCES_FOR_MEDICAL_REASONS, separate_residences_for_medical_reasons),
        Artifact(LIVED_IN_STUDENT_RESIDENCE, lived_in_student_residence),
        Artifact(RENT_PAID, D(rent_paid)),
        Artifact(PROPERTY_TAX_PAID, D(property_tax_paid)),
        Artifact(RESERVE_HOME_ENERGY_COSTS, D(reserve_home_energy_costs)),
        Artifact(PUBLIC_LONG_TERM_CARE_PAID, D(public_long_term_care_paid)),
        Artifact(SENIORS_TRANSIT_PAID, D(seniors_transit_paid)),
        slips(*flow_through_share_slips),
        Artifact(COOP_EDUCATION_PAYROLL, D(coop_education_payroll)),
        placement_list(*coop_education_placements),
        Artifact(COOP_CLAIMED_AS_PARTNERSHIP_MEMBER, coop_claimed_as_partnership_member),
        Artifact(COOP_PARTNERSHIP_BUSINESS_NUMBER, coop_partnership_business_number),
        Artifact(COMMUNITY_FOOD_PROGRAM_DONATIONS, D(community_food_program_donations)),
        Artifact(CHARITABLE_DONATIONS, D(charitable_donations)),
        Artifact(GOVERNMENT_DONATIONS, D(government_donations)),
        Artifact(UNIVERSITY_DONATIONS_OUTSIDE_CANADA, D(university_donations_outside_canada)),
        Artifact(FOREIGN_CHARITY_DONATIONS, D(foreign_charity_donations)),
        Artifact(ECOLOGICAL_AND_CULTURAL_GIFTS, D(ecological_and_cultural_gifts)),
        Artifact(ECOLOGICAL_GIFTS_BEFORE_2016, D(ecological_gifts_before_2016)),
        Artifact(
            DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION, D(depreciable_gift_recaptured_depreciation)
        ),
        Artifact(DEPRECIABLE_GIFT_NET_PROCEEDS, D(depreciable_gift_net_proceeds)),
        Artifact(DEPRECIABLE_GIFT_CAPITAL_COST, D(depreciable_gift_capital_cost)),
        Artifact(CAPITAL_GIFT_TAXABLE_GAINS, D(capital_gift_taxable_gains)),
        Artifact(CAPITAL_GIFT_GAINS_DEDUCTION, D(capital_gift_gains_deduction)),
        Artifact(ontario.POLITICAL_CONTRIBUTIONS, D(political_contributions)),
        Artifact(
            CARE_SUPPORTING_PERSONS_ADJUSTED_INCOME, D(care_supporting_persons_adjusted_income)
        ),
        Artifact(POLITICAL_CONTRIBUTIONS, D(federal_political_contributions)),
        Artifact(DISABILITY_SUPPORTS_DEDUCTION, D(disability_supports_deduction)),
        Artifact(OTHER_EMPLOYMENT_EXPENSES, D(other_employment_expenses)),
        Artifact(CLERGY_RESIDENCE_DEDUCTION, D(clergy_residence_deduction)),
        Artifact(NET_BUSINESS_INCOME, D(net_business_income)),
        Artifact(NET_PROFESSIONAL_INCOME, D(net_professional_income)),
        Artifact(NET_COMMISSION_INCOME, D(net_commission_income)),
        Artifact(NET_FARMING_INCOME, D(net_farming_income)),
        Artifact(NET_FISHING_INCOME, D(net_fishing_income)),
        Artifact(WAGE_LOSS_REPLACEMENT_PLAN_INCOME, D(wage_loss_replacement_plan_income)),
        Artifact(RESIDENT_IN_CANADA_THROUGHOUT_2025, resident_in_canada_throughout_2025),
        Artifact(AGED_18_OR_OLDER_AT_END_OF_2025, aged_18_or_older_at_end_of_2025),
        Artifact(SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS, D(spouse_net_income_before_adjustments)),
        Artifact(SPOUSE_UCCB_REPAYMENT, D(spouse_uccb_repayment)),
        Artifact(SPOUSE_RDSP_INCOME_REPAYMENT, D(spouse_rdsp_income_repayment)),
        Artifact(SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT, D(spouse_universal_child_care_benefit)),
        Artifact(SPOUSE_RDSP_INCOME, D(spouse_rdsp_income)),
        Artifact(SPLIT_INCOME_DIVIDENDS, D(split_income_dividends)),
        Artifact(
            SPLIT_INCOME_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            D(split_income_dividends_other_than_eligible),
        ),
        Artifact(OTHER_SPLIT_INCOME, D(other_split_income)),
        Artifact(DISABILITY_AMOUNT_FOR_SELF, D(disability_amount_for_self)),
        Artifact(
            UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987, D(unapplied_net_capital_losses_1985_to_1987)
        ),
        Artifact(
            UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
            D(unapplied_net_capital_losses_1988_and_1989),
        ),
        Artifact(
            UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999, D(unapplied_net_capital_losses_1990_to_1999)
        ),
        Artifact(
            UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024, D(unapplied_net_capital_losses_2001_to_2024)
        ),
        Artifact(NET_CAPITAL_LOSSES_CLAIMED, D(net_capital_losses_claimed)),
        Artifact(BUSINESS_INCOME, D(business_income)),
        Artifact(PROFESSIONAL_INCOME, D(professional_income)),
        Artifact(COMMISSION_INCOME, D(commission_income)),
        Artifact(FARMING_INCOME, D(farming_income)),
        Artifact(FISHING_INCOME, D(fishing_income)),
        Artifact(CPP_MONTHS, cpp_months),
        Artifact(CPT20_EARNINGS, D(cpt20_earnings)),
        Artifact(CPP_PART_4_COMPLETED, cpp_part_4_completed),
        Artifact(EI_CONTROLLED_CORPORATION_EARNINGS, D(ei_controlled_corporation_earnings)),
        Artifact(EI_EXEMPT_SELF_EMPLOYMENT_INCOME, D(ei_exempt_self_employment_income)),
        Artifact(EI_INSURABLE_EARNINGS, D(ei_insurable_earnings)),
        Artifact(EI_SPECIAL_BENEFITS_AGREEMENT, ei_special_benefits_agreement),
        Artifact(CANADIAN_TUITION_FEES, D(canadian_tuition_fees)),
        Artifact(CANADA_TRAINING_CREDIT_LIMIT, D(canada_training_credit_limit)),
        Artifact(CANADA_TRAINING_CREDIT_CLAIMED, D(canada_training_credit_claimed)),
        Artifact(FOREIGN_TUITION_FEES, D(foreign_tuition_fees)),
        Artifact(UNUSED_TUITION_FROM_2024, D(unused_tuition_from_2024)),
        Artifact(TUITION_TRANSFER_ELECTED, D(tuition_transfer_elected)),
        Artifact(TUITION_TRANSFERRED_FROM_CHILD, D(tuition_transferred_from_child)),
        Artifact(SPOUSE_RETURN_AGE_AMOUNT, D(spouse_return_age_amount)),
        Artifact(SPOUSE_RETURN_INFIRM_CHILDREN_AMOUNT, D(spouse_return_infirm_children_amount)),
        Artifact(SPOUSE_RETURN_PENSION_INCOME_AMOUNT, D(spouse_return_pension_income_amount)),
        Artifact(SPOUSE_RETURN_DISABILITY_AMOUNT, D(spouse_return_disability_amount)),
        Artifact(SPOUSE_DESIGNATED_TUITION, D(spouse_designated_tuition)),
        Artifact(SPOUSE_RETURN_TAXABLE_INCOME, D(spouse_return_taxable_income)),
        Artifact(SPOUSE_RETURN_FEDERAL_BASIC_TAX, D(spouse_return_federal_basic_tax)),
        Artifact(SPOUSE_RETURN_BASIC_PERSONAL_AMOUNT, D(spouse_return_basic_personal_amount)),
        Artifact(SPOUSE_RETURN_LINE_96, D(spouse_return_line_96)),
        Artifact(SPOUSE_RETURN_FEDERAL_TUITION_AMOUNT, D(spouse_return_federal_tuition_amount)),
        Artifact(SPOUSE_NOT_SEPARATED_90_DAYS, spouse_not_separated_90_days),
        Artifact(ontario.SPOUSE_RETURN_ONTARIO_AGE_AMOUNT, D(spouse_return_ontario_age_amount)),
        Artifact(
            ontario.SPOUSE_RETURN_ONTARIO_PENSION_INCOME_AMOUNT,
            D(spouse_return_ontario_pension_income_amount),
        ),
        Artifact(
            ontario.SPOUSE_RETURN_ONTARIO_DISABILITY_AMOUNT,
            D(spouse_return_ontario_disability_amount),
        ),
        Artifact(ontario.SPOUSE_RETURN_ONTARIO_BASIC_TAX, D(spouse_return_ontario_basic_tax)),
        Artifact(
            ontario.SPOUSE_RETURN_ONTARIO_BASIC_PERSONAL_AMOUNT,
            D(spouse_return_ontario_basic_personal_amount),
        ),
        Artifact(ontario.SPOUSE_RETURN_ONTARIO_LINE_24, D(spouse_return_ontario_line_24)),
        Artifact(
            ontario.SPOUSE_RETURN_ONTARIO_UNUSED_TUITION_AMOUNT,
            D(spouse_return_ontario_unused_tuition_amount),
        ),
        Artifact(ontario.LIFT_SPOUSE_AT_YEAR_END, lift_spouse_at_year_end),
        Artifact(ontario.ONTARIO_MINIMUM_TAX, D(ontario_minimum_tax)),
        Artifact(
            ontario.NOT_RESIDENT_OF_CANADA_AT_START_OF_YEAR, not_resident_of_canada_at_start_of_year
        ),
        Artifact(ontario.NOT_RESIDENT_OF_ONTARIO_AT_YEAR_END, not_resident_of_ontario_at_year_end),
        Artifact(ontario.BANKRUPT_IN_YEAR, bankrupt_in_year),
        Artifact(
            ontario.RETURN_FILED_BY_TRUSTEE_IN_BANKRUPTCY, return_filed_by_trustee_in_bankruptcy
        ),
        Artifact(ontario.NOT_CLAIMING_ONTARIO_TAX_REDUCTION, not_claiming_ontario_tax_reduction),
        Artifact(
            SPOUSE_OR_COMMON_LAW_PARTNER_ON_DECEMBER_31, spouse_or_common_law_partner_on_december_31
        ),
        Artifact(
            ontario.CLAIMS_TAX_REDUCTION_AMOUNTS_AT_EQUAL_NET_INCOME,
            claims_tax_reduction_amounts_at_equal_net_income,
        ),
        Artifact(
            ontario.UNUSED_TUITION_AMOUNTS_BROUGHT_FORWARD,
            D(unused_tuition_amounts_brought_forward),
        ),
    )


def return_a() -> Worksheet:
    """Return A's inputs, as in `returns/2025_return_a.yaml`, with its chosen tax deducted."""
    return compute(
        "110000",
        (("20000", "0", "0"),),
        "0",
        "1926",
        "19800",
        "1926",
        "2000",
        income_tax_deducted="25000",
    )


def return_f_with_credits(
    fertility_expenses: str,
    seniors_transit_paid: str,
    flow_through_share_slips: tuple[str, ...] = (),
    coop_education_payroll: str = "0",
    coop_education_placements: tuple[str, ...] = (),
) -> Worksheet:
    """Return F's inputs, as in `returns/2025_return_f.yaml`, with the ON479 amounts given."""
    return compute(
        "60000",
        (),
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        child_care_expenses_paid="6000",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
        fertility_expenses=fertility_expenses,
        seniors_transit_paid=seniors_transit_paid,
        flow_through_share_slips=flow_through_share_slips,
        coop_education_payroll=coop_education_payroll,
        coop_education_placements=coop_education_placements,
    )


def return_r(payroll: str = "500000", placements: tuple[str, ...] = ("8000", "15000")) -> Worksheet:
    """Return R's inputs, as in `returns/2025_return_r.yaml`: Return M with work placements."""
    return return_f_with_credits(
        "24000",
        "1200",
        ("6000", "4000"),
        coop_education_payroll=payroll,
        coop_education_placements=placements,
    )


def return_k() -> Worksheet:
    """Return K's inputs, as in `returns/2025_return_k.yaml`: slip and no-slip dividends."""
    return compute(
        "50000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        t5_taxable_dividends_other_than_eligible="200",
        t5_taxable_dividends="500",
        t5_dividend_tax_credit="60.00",
        eligible_dividends_received_without_a_slip="1000",
        other_dividends_received_without_a_slip="500",
        income_tax_deducted="9000",
    )


def return_w(**overrides: Any) -> Worksheet:
    """Return W's inputs (`returns/2025_return_w.yaml`): Return Q's and two Ontario dependants.

    `overrides` replace any keyword of `compute`, for the variants below.
    """
    given: dict[str, Any] = {
        "income_tax_deducted": "4800",
        "community_food_program_donations": "1000",
        "infirm_dependants": ("5000", "25000"),
        "caregiver_dependants": (("5000", 0), ("25000", 0)),
    }
    return compute("48000", (), "0", "0", "8640", "0", "0", **{**given, **overrides})


def step_3(**amounts: Any) -> Worksheet:
    """A return with no income, no CPP, no RRSP and no deductions but the keyword `amounts`."""
    return compute("0", (), "0", "0", "0", "0", "0", **amounts)
