"""Snapshot of the `ca/` artifact kind identifiers, as the application registers them.

Identifiers are stored with results and exposed by the API, so changing or removing one is a
breaking change: update this snapshot only on purpose. Each package snapshots its own namespace;
declaring a kind in this package's catalog adds it here. The kinds are registered explicitly,
as the composition root does, into a fresh registry. The snapshot itself is `REGISTERED` in
`catalog_snapshot.py`; the per-family checks are in `test_catalog_<family>.py`.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest

import app.jurisdictions.ca
import app.jurisdictions.ca.catalog
from app.domain.artifact import Artifact, ArtifactCatalog, ArtifactKind, ArtifactRegistry
from app.domain.errors import InvalidRecordError, NegativeArtifactError
from app.domain.record_list import RecordList, RecordListKind
from app.jurisdictions.ca.catalog import (
    ADVANCED_CANADA_WORKERS_BENEFIT,
    AGED_18_OR_OLDER_AT_END_OF_2025,
    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INCOME,
    BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
    CAPITAL_GAIN,
    CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
    CAREGIVER_AMOUNT,
    CATALOG,
    CCA_ADDITIONS,
    CCA_AIIP_ADDITIONS,
    CCA_CLAIMED,
    CCA_CLASS_NUMBER,
    CCA_NO_PROPERTY_LEFT,
    CCA_PROCEEDS,
    CCA_RIIP_ADDITIONS,
    CCA_UCC_AT_END,
    CCA_UCC_AT_START,
    CLERGY_RESIDENCE_DEDUCTION,
    COMMISSION_INCOME,
    CPP_EARNINGS_SUBJECT_TO_BASE_AND_FIRST_ADDITIONAL,
    CPP_EARNINGS_SUBJECT_TO_SECOND_ADDITIONAL,
    CPP_EARNINGS_UP_TO_MAXIMUM,
    CPP_PAYABLE_ON_SELF_EMPLOYMENT,
    CPP_PENSIONABLE_EARNINGS,
    CPT20_EARNINGS,
    CREDITS_AGAINST_FEDERAL_TAX,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    DEPENDANT_CARE_EXPENSES,
    DEPENDANT_CREDIT_AMOUNTS,
    DEPENDANT_NET_INCOME,
    DEPENDANT_TAXABLE_INCOME,
    DEPENDANT_UNDER_18,
    DISABILITY_DEPENDANTS,
    DISABILITY_SUPPORTS_DEDUCTION,
    DISABILITY_TRANSFERRED_AMOUNT,
    EDUCATOR_SCHOOL_SUPPLY_CREDIT,
    EDUCATOR_SUPPLIES_EXPENSES,
    EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
    EI_INSURABLE_EARNINGS_REMAINING,
    EI_PAYABLE_ON_SELF_EMPLOYMENT,
    EI_SELF_EMPLOYMENT_EARNINGS,
    EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
    FARMING_INCOME,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_LESS_CREDITS,
    FEDERAL_TAX_WITH_ITC_RECAPTURE,
    FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS,
    FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD,
    FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD,
    FHSA_ANNUAL_LIMIT,
    FHSA_ANNUAL_LIMIT_FROM_STEP_2,
    FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS,
    FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_AVAILABLE,
    FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_LIMIT,
    FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT,
    FHSA_DEDUCTION,
    FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
    FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS,
    FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS,
    FHSA_MAXIMUM_DEDUCTION,
    FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED,
    FHSA_NET_RRSP_TRANSFER_AMOUNT,
    FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS,
    FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS,
    FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT,
    FHSA_TOTAL_ANNUAL_LIMITS,
    FHSA_TOTAL_DESIGNATED_TRANSFERS,
    FHSA_TOTAL_RRSP_TRANSFERS,
    FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT,
    FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT,
    FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD,
    FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS,
    FISHING_INCOME,
    GROSS_RENTAL_INCOME,
    INCOME_TAX_DEDUCTED,
    INFIRM_DEPENDANTS,
    ITC_RECAPTURE,
    ITC_RECAPTURE_AT_15_PERCENT,
    ITC_RECAPTURE_AT_20_PERCENT,
    ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT,
    ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT,
    JOURNALISM_LABOUR_TAX_CREDIT,
    LABOUR_SPONSORED_FUNDS_CREDIT,
    LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
    LABOUR_SPONSORED_FUNDS_NET_COST,
    MEDICAL_CLAIM,
    MEDICAL_EXPENSES,
    MEDICAL_EXPENSES_OVER_THRESHOLD,
    MEDICAL_NET_INCOME_SHARE,
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
    MEDICAL_THRESHOLD,
    NET_BUSINESS_INCOME,
    NET_COMMISSION_INCOME,
    NET_FARMING_INCOME,
    NET_FISHING_INCOME,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
    NET_PROFESSIONAL_INCOME,
    NET_RENTAL_INCOME,
    NET_SELF_EMPLOYMENT_INCOME,
    NORTHERN_RESIDENTS_DEDUCTIONS,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
    OTHER_DEPENDANT_MEDICAL_EXPENSES,
    OTHER_DEPENDANTS,
    OTHER_DEPENDANTS_MEDICAL,
    OTHER_EMPLOYMENT_EXPENSES,
    OTHER_PAYMENTS_DEDUCTION,
    OTHER_PAYMENTS_LIMIT_INCOME,
    PART_XII_2_TAX_CREDIT,
    PENSIONABLE_NET_SELF_EMPLOYMENT_EARNINGS,
    POLITICAL_CONTRIBUTIONS,
    POLITICAL_CREDIT,
    POLITICAL_CREDIT_BEFORE_MAXIMUM,
    POLITICAL_CREDIT_CHOSEN_COLUMN,
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
    POLITICAL_CREDIT_SHORTCUT_AMOUNT,
    POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
    PRINCIPAL_RESIDENCE_GAIN,
    PRINCIPAL_RESIDENCE_PROPERTIES,
    PROFESSIONAL_INCOME,
    REFUND,
    REFUND_OR_BALANCE_OWING,
    REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT,
    RENTAL_ADVERTISING,
    RENTAL_ADVERTISING_PERSONAL_PORTION,
    RENTAL_ADVERTISING_SHORT_TERM_PORTION,
    RENTAL_CCA_CLAIM,
    RENTAL_COOWNER,
    RENTAL_COOWNER_OTHER_EXPENSES,
    RENTAL_COOWNER_SHARE,
    RENTAL_DEDUCTIBLE_EXPENSES,
    RENTAL_EXPENSES_LESS_PERSONAL_PORTION,
    RENTAL_GROSS_RENTS,
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
    RENTAL_NET_INCOME_AFTER_CCA,
    RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES,
    RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS,
    RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS,
    RENTAL_NET_INCOME_SHARE,
    RENTAL_NET_INCOME_WITH_RECAPTURE,
    RENTAL_NON_COMPLIANT_EXPENSES,
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
    RENTAL_PARTNER_SHARE_WITH_REBATE,
    RENTAL_PARTNERSHIP_NET_INCOME,
    RENTAL_PERSONAL_PORTION,
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
    RENTAL_RECAPTURED_CCA,
    RENTAL_REPAIRS_AND_MAINTENANCE,
    RENTAL_REPAIRS_AND_MAINTENANCE_PERSONAL_PORTION,
    RENTAL_REPAIRS_AND_MAINTENANCE_SHORT_TERM_PORTION,
    RENTAL_SALARIES_WAGES_AND_BENEFITS,
    RENTAL_SALARIES_WAGES_AND_BENEFITS_PERSONAL_PORTION,
    RENTAL_SALARIES_WAGES_AND_BENEFITS_SHORT_TERM_PORTION,
    RENTAL_SHORT_TERM_PORTION,
    RENTAL_TERMINAL_LOSS,
    RENTAL_TOTAL_EXPENSES,
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
    RESIDENCY_AMOUNT,
    RESIDENCY_DEDUCTION,
    RESIDENCY_NET_INCOME_LIMIT,
    RESIDENT_IN_CANADA_THROUGHOUT_2025,
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
    RL_10_LABOUR_SPONSORED_FUND_AMOUNT,
    RRSP_AMOUNT_DEDUCTED,
    SELF_EMPLOYED_CPP_DEDUCTION,
    SHORT_TERM_RENTAL_DAYS,
    SHORT_TERM_RENTAL_GROSS_RENTS,
    SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS,
    SHORT_TERM_RENTAL_RELATED_EXPENSES,
    SHORT_TERM_RENTAL_UNITS,
    SPECIAL_TAXES,
    SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS,
    SPOUSE_RDSP_INCOME,
    SPOUSE_RDSP_INCOME_REPAYMENT,
    SPOUSE_UCCB_REPAYMENT,
    SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT,
    STANDARD_AMOUNT_ALLOCATED_1,
    STANDARD_AMOUNT_ALLOCATED_2,
    STANDARD_AMOUNT_ALLOCATED_3,
    TAX_PAID_BY_INSTALMENTS,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    TRAVEL_DEDUCTION,
    TRAVEL_INDIVIDUAL,
    TRAVEL_INDIVIDUALS,
    TRAVEL_TRIPS,
    TRIP_BENEFIT_OR_STANDARD_AMOUNT,
    TRIP_LOWEST_RETURN_AIRFARE,
    TRIP_TRAVEL_EXPENSES,
    TRIP_ZONE,
    UCCB_AND_RDSP_INCOME,
    UCCB_AND_RDSP_INCOME_REPAYMENTS,
    WAGE_LOSS_REPLACEMENT_PLAN_INCOME,
    ZONE_A_RESIDENCY_AFTER_WORK_SITE,
    ZONE_B_RESIDENCY_AFTER_WORK_SITE,
)
from tests.jurisdictions.ca.catalog_snapshot import COUNTS, RECORD_LISTS, REGISTERED, SIGNED


def test_registered_identifiers_snapshot(registry: ArtifactRegistry) -> None:
    identifiers = registry.identifiers()

    assert {i for i in identifiers if i.startswith("ca/")} == REGISTERED


def test_the_package_exposes_its_catalog() -> None:
    assert isinstance(app.jurisdictions.ca.catalog.CATALOG, ArtifactCatalog)
    assert app.jurisdictions.ca.catalog.CATALOG is CATALOG
    assert {kind.identifier for kind in CATALOG.kinds} == REGISTERED


def test_catalog_kinds_are_in_the_package_namespace() -> None:
    for kind in CATALOG.kinds:
        assert kind.identifier.startswith(f"{app.jurisdictions.ca.NAMESPACE}/")


def test_the_catalog_kinds_named_by_the_package_are_money() -> None:
    assert TAXABLE_INCOME.value_type is Decimal
    assert FEDERAL_BASIC_TAX.value_type is Decimal


def test_every_registered_kind_but_the_counts_and_record_lists_is_money(
    registry: ArtifactRegistry,
) -> None:
    for identifier in REGISTERED - COUNTS - RECORD_LISTS:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.value_type is Decimal, identifier


def test_the_counts_are_int_kinds_in_the_package_namespace(registry: ArtifactRegistry) -> None:
    assert COUNTS <= REGISTERED
    for identifier in COUNTS:
        kind = registry.get(identifier)
        assert isinstance(kind, ArtifactKind)
        assert kind.identifier.startswith(f"{app.jurisdictions.ca.NAMESPACE}/")
        assert kind.value_type is int, identifier


def test_every_kind_but_the_balance_is_declared_non_negative(registry: ArtifactRegistry) -> None:
    # No other `ca/` line can be negative on the forms as modelled.
    # A record list is not an amount: it is never declared non-negative, its fields are.
    for kind in CATALOG.kinds:
        if kind.identifier not in SIGNED | RECORD_LISTS:
            assert kind.non_negative is True, kind.identifier
    for identifier in REGISTERED - SIGNED - RECORD_LISTS:
        assert registry.kind(identifier).non_negative is True, identifier


def test_the_refund_or_balance_owing_is_signed(registry: ArtifactRegistry) -> None:
    # T1 line 167 "Line 149 minus line 166 If the amount is negative, enter it on line 48400
    # below. If the amount is positive, enter it on line 48500 below. Refund or balance owing":
    # negative is a refund, so the kind is not declared non-negative.
    assert REFUND_OR_BALANCE_OWING.non_negative is False
    assert registry.kind("ca/refund_or_balance_owing").non_negative is False
    assert SIGNED <= REGISTERED


def test_the_other_payments_worksheets_lines_5_and_9_are_signed(registry: ArtifactRegistry) -> None:
    # Federal Worksheet "Line 25000 - Other payments deduction": line 5 "Line 1 minus line 4 =" and
    # line 9 "Line 5 plus line 8 =" print no floor, unlike line 1 ("if negative, enter "0"").
    assert NET_INCOME_LESS_UCCB_AND_RDSP_INCOME.non_negative is False
    assert OTHER_PAYMENTS_LIMIT_INCOME.non_negative is False
    assert registry.kind("ca/net_income_less_uccb_and_rdsp_income").non_negative is False
    assert registry.kind("ca/other_payments_limit_income").non_negative is False
    assert UCCB_AND_RDSP_INCOME.non_negative is True
    assert UCCB_AND_RDSP_INCOME_REPAYMENTS.non_negative is True
    assert OTHER_PAYMENTS_DEDUCTION.non_negative is True


def test_the_total_income_is_signed(registry: ArtifactRegistry) -> None:
    # T1 line 33 and line 15000 "Line 28 plus line 32 Total income" prints no floor, and the
    # General Guide for lines 13499 to 14300 says "If you have a loss, show it on the applicable
    # line using brackets": a loss larger than the other income is a negative total income. The
    # floor stays at line 23600 (`ca/net_income`).
    assert TOTAL_INCOME.non_negative is False
    assert registry.kind("ca/total_income").non_negative is False
    assert NET_INCOME.non_negative is True
    assert Artifact(TOTAL_INCOME, Decimal("-2000.00")).value == Decimal("-2000.00")


def test_the_net_income_before_adjustments_is_signed(registry: ArtifactRegistry) -> None:
    # T1 line 54 and line 23400 "Line 34 minus line 53 (if negative, show in brackets) Net income
    # before adjustments": the brackets are a negative figure, unlike line 56 (line 23600) "Line 54
    # minus line 55 (if negative, enter "0")", which stays the non-negative `ca/net_income`.
    assert NET_INCOME_BEFORE_ADJUSTMENTS.non_negative is False
    assert registry.kind("ca/net_income_before_adjustments").non_negative is False
    assert NET_INCOME.non_negative is True
    assert DEDUCTIONS_FROM_TOTAL_INCOME.non_negative is True


def test_the_t1436_lines_that_print_no_floor_are_signed(registry: ArtifactRegistry) -> None:
    # Form T1436 line 21700: line 15 "Line 7 minus line 14" and line 17 "Enter whichever is less:
    # amount from line 15 or line 16." print no "(if negative, enter "0")".
    assert BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE.non_negative is False
    assert BUSINESS_INVESTMENT_LOSS_REDUCTION.non_negative is False
    assert registry.kind("ca/business_investment_loss_reduction_available").non_negative is False
    assert registry.kind("ca/business_investment_loss_reduction").non_negative is False


def test_the_other_t1436_lines_are_non_negative(registry: ArtifactRegistry) -> None:
    # Lines 7 and 14 add non-negative figures; line 18 "Line 16 minus line 17" is never negative as
    # line 17 is at most line 16; line 20 "Line 18 multiplied by the percentage on line 19".
    for kind in (
        CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
        BUSINESS_INVESTMENT_LOSS,
        BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
        ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    ):
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier).non_negative is True, kind.identifier


def test_the_schedule_15_lines_that_print_no_floor_are_signed(registry: ArtifactRegistry) -> None:
    # Schedule 15 (FHSA) Steps 2 and 3: lines 3, 5, 9, 11, 23, 27, 36, 45, 48, 51, 54, 56 and 58
    # subtract (or add a line that subtracts, or take the lesser of such a line) with no "(if
    # negative, enter "0")".
    for kind in (
        FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT,
        FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_NET_RRSP_TRANSFER_AMOUNT,
        FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS,
        FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS,
        FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS,
        FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS,
        FHSA_MAXIMUM_DEDUCTION,
        FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS,
        FHSA_CONTRIBUTIONS_AVAILABLE,
        FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD,
    ):
        assert kind.non_negative is False, kind.identifier
        assert registry.kind(kind.identifier).non_negative is False, kind.identifier


def test_the_schedule_15_lines_that_print_a_floor_or_add_non_negative_figures_are_non_negative(
    registry: ArtifactRegistry,
) -> None:
    # Lines 12, 13, 29, 39 and 50 print "(if negative, enter "0")"; lines 16, 19, 22, 32, 33, 35,
    # 40 and 43 and the deduction (line 57, at most line 51) add or take the lesser of
    # non-negative lines.
    for kind in (
        FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
        FHSA_CONTRIBUTIONS_LIMIT,
        FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD,
        FHSA_TOTAL_RRSP_TRANSFERS,
        FHSA_TOTAL_DESIGNATED_TRANSFERS,
        FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT,
        FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD,
        FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT,
        FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT,
        FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS,
        FHSA_ANNUAL_LIMIT_FROM_STEP_2,
        FHSA_ANNUAL_LIMIT,
        FHSA_TOTAL_ANNUAL_LIMITS,
        FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS,
        FHSA_DEDUCTION,
    ):
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier).non_negative is True, kind.identifier


def test_the_fhsa_maximum_participation_period_count_is_a_non_negative_int() -> None:
    # Schedule 15 Step 2: "If your maximum participation period (MPP) ended in a prior year, ...
    # Enter "0" on line 40": a caller's 0 or 1 count.
    assert FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED.value_type is int
    assert FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED.non_negative is True


def test_the_income_tax_deducted_is_non_negative() -> None:
    # T1 line 150 (line 43700) "Total income tax deducted (amounts from all Canadian slips)".
    assert INCOME_TAX_DEDUCTED.non_negative is True


def test_the_rrsp_amount_deducted_is_non_negative() -> None:
    # Schedule 7 line 18 "Enter your RRSP, PRPP, or SPP contributions you are deducting for 2025
    # (cannot be more than the amount on line 17).": an amount the filer states.
    assert RRSP_AMOUNT_DEDUCTED.non_negative is True


def test_capital_gain_is_non_negative_while_losses_are_not_modelled() -> None:
    assert CAPITAL_GAIN.non_negative is True


def test_the_step_6_credit_lines_are_non_negative(registry: ArtifactRegistry) -> None:
    # T1 lines 45600, 45700, 46800, 46900, 47555 and 47600 are slip, receipt or form amounts of
    # money paid or credited to the filer, none of which prints a negative figure; line 48400
    # "Refund" is the negative of line 167 and is entered only when line 167 is negative, so it is
    # never below zero, unlike line 167 (`ca/refund_or_balance_owing`), which stays signed.
    for kind in (
        PART_XII_2_TAX_CREDIT,
        EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
        EDUCATOR_SUPPLIES_EXPENSES,
        EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
        EDUCATOR_SCHOOL_SUPPLY_CREDIT,
        JOURNALISM_LABOUR_TAX_CREDIT,
        TAX_PAID_BY_INSTALMENTS,
        REFUND,
    ):
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier).non_negative is True, kind.identifier
    assert REFUND_OR_BALANCE_OWING.non_negative is False


def test_the_infirm_dependants_are_a_record_list_of_their_net_incomes(
    registry: ArtifactRegistry,
) -> None:
    # Schedule 5 line 30450's chart, per dependant: line 2 "Infirm dependant's net income from
    # line 23600 of their return", the one field a record holds (the caller lists only the
    # dependants who are eligible, so there are no eligibility fields).
    assert RECORD_LISTS <= REGISTERED
    assert isinstance(INFIRM_DEPENDANTS, RecordListKind)
    assert INFIRM_DEPENDANTS.identifier == "ca/infirm_dependants"
    assert INFIRM_DEPENDANTS.value_type is RecordList
    assert INFIRM_DEPENDANTS.fields == (DEPENDANT_NET_INCOME,)
    assert registry.get("ca/infirm_dependants") is INFIRM_DEPENDANTS


def test_the_record_list_reuses_the_dependants_net_income_kind() -> None:
    # Schedule 5 line 4 and ON428 line 15 read the same kind; here it is the field of a record.
    assert INFIRM_DEPENDANTS.fields[0] is DEPENDANT_NET_INCOME
    assert DEPENDANT_NET_INCOME.identifier == "ca/dependant_net_income"
    assert DEPENDANT_NET_INCOME.non_negative is True


def test_the_infirm_dependants_hold_a_net_income_each_in_the_callers_order() -> None:
    dependants = RecordList(
        INFIRM_DEPENDANTS.fields,
        [{DEPENDANT_NET_INCOME: Decimal("5000")}, {DEPENDANT_NET_INCOME: Decimal("25000")}],
    )

    assert [record[DEPENDANT_NET_INCOME] for record in dependants.records] == [
        Decimal("5000"),
        Decimal("25000"),
    ]


def test_the_caregiver_amount_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # T1 line 82 (line 30450) "Canada caregiver amount for other infirm dependants age 18 or
    # older (complete Schedule 5)": the total of the allowable amounts, each at least "0".
    assert CAREGIVER_AMOUNT.identifier == "ca/caregiver_amount"
    assert CAREGIVER_AMOUNT.value_type is Decimal
    assert CAREGIVER_AMOUNT.non_negative is True
    assert registry.kind("ca/caregiver_amount") is CAREGIVER_AMOUNT


def test_the_other_dependants_are_a_record_list_of_expenses_and_net_income(
    registry: ArtifactRegistry,
) -> None:
    # Federal Worksheet, line 33199, "Complete one column for each dependant": line 1 "Medical
    # expenses for other dependant" and, for line 2, the dependant's net income. A list of its own:
    # the infirm dependants of line 30450 are a different set of people.
    assert isinstance(OTHER_DEPENDANTS, RecordListKind)
    assert OTHER_DEPENDANTS.identifier == "ca/other_dependants"
    assert OTHER_DEPENDANTS.value_type is RecordList
    assert OTHER_DEPENDANTS.fields == (OTHER_DEPENDANT_MEDICAL_EXPENSES, DEPENDANT_NET_INCOME)
    assert OTHER_DEPENDANTS is not INFIRM_DEPENDANTS
    assert registry.get("ca/other_dependants") is OTHER_DEPENDANTS


def test_the_other_dependants_list_reuses_the_dependants_net_income_kind() -> None:
    assert OTHER_DEPENDANTS.fields[1] is DEPENDANT_NET_INCOME


def test_the_other_dependants_hold_expenses_and_net_income_each_in_the_callers_order() -> None:
    dependants = RecordList(
        OTHER_DEPENDANTS.fields,
        [
            {
                OTHER_DEPENDANT_MEDICAL_EXPENSES: Decimal("3000"),
                DEPENDANT_NET_INCOME: Decimal("10000"),
            },
            {
                OTHER_DEPENDANT_MEDICAL_EXPENSES: Decimal("1000"),
                DEPENDANT_NET_INCOME: Decimal("40000"),
            },
        ],
    )

    assert [record[OTHER_DEPENDANT_MEDICAL_EXPENSES] for record in dependants.records] == [
        Decimal("3000"),
        Decimal("1000"),
    ]


def test_the_other_dependant_medical_expenses_are_a_non_negative_decimal(
    registry: ArtifactRegistry,
) -> None:
    # Federal Worksheet, line 33199, line 1 "Medical expenses for other dependant".
    assert OTHER_DEPENDANT_MEDICAL_EXPENSES.identifier == "ca/other_dependant_medical_expenses"
    assert OTHER_DEPENDANT_MEDICAL_EXPENSES.value_type is Decimal
    assert OTHER_DEPENDANT_MEDICAL_EXPENSES.non_negative is True
    assert registry.kind("ca/other_dependant_medical_expenses") is OTHER_DEPENDANT_MEDICAL_EXPENSES


def test_the_other_dependants_medical_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # T1 line 33199 "Allowable amount of medical expenses for other dependants": the total of
    # each dependant's line 3, which is "0" when negative.
    assert OTHER_DEPENDANTS_MEDICAL.identifier == "ca/other_dependants_medical"
    assert OTHER_DEPENDANTS_MEDICAL.value_type is Decimal
    assert OTHER_DEPENDANTS_MEDICAL.non_negative is True
    assert registry.kind("ca/other_dependants_medical") is OTHER_DEPENDANTS_MEDICAL


def test_the_short_term_rental_units_are_a_record_list_of_chart_a_columns_3_to_5(
    registry: ArtifactRegistry,
) -> None:
    # Form T776 Chart A, "Enter each short-term rental or mixed rental property on a separate
    # row": column 3 "Related portion of the total from line 9365 of Part 4", column 4 "Number
    # of days the residential property was a non compliant short-term rental" and column 5
    # "Number of days the residential property was a short-term rental" (columns 1 and 2 are
    # the address and unit number, labels the engine does not use).
    assert RECORD_LISTS <= REGISTERED
    assert isinstance(SHORT_TERM_RENTAL_UNITS, RecordListKind)
    assert SHORT_TERM_RENTAL_UNITS.identifier == "ca/short_term_rental_units"
    assert SHORT_TERM_RENTAL_UNITS.value_type is RecordList
    assert SHORT_TERM_RENTAL_UNITS.non_negative is False
    assert SHORT_TERM_RENTAL_UNITS.fields == (
        SHORT_TERM_RENTAL_RELATED_EXPENSES,
        SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS,
        SHORT_TERM_RENTAL_DAYS,
    )
    assert registry.get("ca/short_term_rental_units") is SHORT_TERM_RENTAL_UNITS


def test_the_short_term_rental_related_expenses_are_a_non_negative_decimal(
    registry: ArtifactRegistry,
) -> None:
    # Chart A, column 3 "Related portion of the total from line 9365 of Part 4".
    assert SHORT_TERM_RENTAL_RELATED_EXPENSES.identifier == "ca/short_term_rental_related_expenses"
    assert SHORT_TERM_RENTAL_RELATED_EXPENSES.value_type is Decimal
    assert SHORT_TERM_RENTAL_RELATED_EXPENSES.non_negative is True
    assert (
        registry.kind("ca/short_term_rental_related_expenses") is SHORT_TERM_RENTAL_RELATED_EXPENSES
    )


@pytest.mark.parametrize(
    ("kind", "identifier"),
    [
        (SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS, "ca/short_term_rental_non_compliant_days"),
        (SHORT_TERM_RENTAL_DAYS, "ca/short_term_rental_days"),
    ],
)
def test_the_short_term_rental_days_are_non_negative_int_counts(
    kind: ArtifactKind[int], identifier: str, registry: ArtifactRegistry
) -> None:
    # Chart A, columns 4 and 5: "Number of days ...", whole days.
    assert kind.identifier == identifier
    assert kind.value_type is int
    assert kind.non_negative is True
    assert registry.kind(identifier) is kind


def short_term_rental_record(**changes: object) -> dict[ArtifactKind[Any], object]:
    """One row of the ticket's example (900, 30 of 90 days) with `changes` by field name."""
    names: dict[str, ArtifactKind[Any]] = {
        "related_expenses": SHORT_TERM_RENTAL_RELATED_EXPENSES,
        "non_compliant_days": SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS,
        "days": SHORT_TERM_RENTAL_DAYS,
    }
    record: dict[ArtifactKind[Any], object] = {
        SHORT_TERM_RENTAL_RELATED_EXPENSES: Decimal("900"),
        SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS: 30,
        SHORT_TERM_RENTAL_DAYS: 90,
    }
    for name, value in changes.items():
        record[names[name]] = value
    return record


def test_the_short_term_rental_units_hold_each_rows_columns_in_the_callers_order() -> None:
    rows = RecordList(
        SHORT_TERM_RENTAL_UNITS.fields,
        [short_term_rental_record(), short_term_rental_record(related_expenses=Decimal("100"))],
    )

    assert [record[SHORT_TERM_RENTAL_RELATED_EXPENSES] for record in rows.records] == [
        Decimal("900"),
        Decimal("100"),
    ]
    assert rows.records[0][SHORT_TERM_RENTAL_NON_COMPLIANT_DAYS] == 30
    assert rows.records[0][SHORT_TERM_RENTAL_DAYS] == 90


def test_the_short_term_rental_units_may_be_empty() -> None:
    assert RecordList(SHORT_TERM_RENTAL_UNITS.fields, []).records == ()


@pytest.mark.parametrize("field", ["related_expenses", "non_compliant_days", "days"])
def test_a_short_term_rental_row_refuses_a_negative_column(field: str) -> None:
    value: object = Decimal("-1") if field == "related_expenses" else -1

    with pytest.raises(NegativeArtifactError, match="item 1"):
        RecordList(SHORT_TERM_RENTAL_UNITS.fields, [short_term_rental_record(**{field: value})])


def test_a_short_term_rental_row_refuses_a_fractional_number_of_days() -> None:
    with pytest.raises(TypeError, match="item 1.*short_term_rental_days"):
        RecordList(SHORT_TERM_RENTAL_UNITS.fields, [short_term_rental_record(days=Decimal("90"))])


def test_a_short_term_rental_row_missing_a_column_is_refused_naming_the_row() -> None:
    record = short_term_rental_record()
    del record[SHORT_TERM_RENTAL_DAYS]

    with pytest.raises(InvalidRecordError, match="item 1.*short_term_rental_days"):
        RecordList(SHORT_TERM_RENTAL_UNITS.fields, [record])


def rental_property_record(**changes: object) -> dict[ArtifactKind[Any], object]:
    """One row of Return AD (2 units, no short-term rents, 24000) with `changes` by field name."""
    names: dict[str, ArtifactKind[Any]] = {
        "units": RENTAL_PROPERTY_UNITS,
        "short_term_rents": RENTAL_PROPERTY_SHORT_TERM_RENTS,
        "gross_rents": RENTAL_PROPERTY_GROSS_RENTS,
    }
    record: dict[ArtifactKind[Any], object] = {
        RENTAL_PROPERTY_UNITS: 2,
        RENTAL_PROPERTY_SHORT_TERM_RENTS: Decimal("0"),
        RENTAL_PROPERTY_GROSS_RENTS: Decimal("24000"),
    }
    for name, value in changes.items():
        record[names[name]] = value
    return record


def test_the_rental_properties_are_a_record_list_of_the_part_3_columns(
    registry: ArtifactRegistry,
) -> None:
    # Form T776 Part 3, "List the addresses of your rental properties." with the headings
    # "Number of units", "Gross rents for short-term rentals" and "Gross rents for all units":
    # one row for each property (the address is a label the engine does not use).
    assert RECORD_LISTS <= REGISTERED
    assert isinstance(RENTAL_PROPERTIES, RecordListKind)
    assert RENTAL_PROPERTIES.identifier == "ca/rental_properties"
    assert RENTAL_PROPERTIES.value_type is RecordList
    assert RENTAL_PROPERTIES.non_negative is False
    assert RENTAL_PROPERTIES.fields == (
        RENTAL_PROPERTY_UNITS,
        RENTAL_PROPERTY_SHORT_TERM_RENTS,
        RENTAL_PROPERTY_GROSS_RENTS,
    )
    assert registry.get("ca/rental_properties") is RENTAL_PROPERTIES


def test_the_rental_property_units_are_a_non_negative_int_count(
    registry: ArtifactRegistry,
) -> None:
    # Part 3, "Number of units", whole units.
    assert RENTAL_PROPERTY_UNITS.identifier == "ca/rental_property_units"
    assert RENTAL_PROPERTY_UNITS.value_type is int
    assert RENTAL_PROPERTY_UNITS.non_negative is True
    assert registry.kind("ca/rental_property_units") is RENTAL_PROPERTY_UNITS


@pytest.mark.parametrize(
    ("kind", "identifier"),
    [
        (RENTAL_PROPERTY_SHORT_TERM_RENTS, "ca/rental_property_short_term_rents"),
        (RENTAL_PROPERTY_GROSS_RENTS, "ca/rental_property_gross_rents"),
    ],
)
def test_the_rental_property_rents_are_non_negative_decimals(
    kind: ArtifactKind[Decimal], identifier: str, registry: ArtifactRegistry
) -> None:
    # Part 3, "Gross rents for short-term rentals" and "Gross rents for all units".
    assert kind.identifier == identifier
    assert kind.value_type is Decimal
    assert kind.non_negative is True
    assert registry.kind(identifier) is kind


def test_the_rental_properties_hold_each_rows_columns_in_the_callers_order() -> None:
    rows = RecordList(
        RENTAL_PROPERTIES.fields,
        [rental_property_record(), rental_property_record(units=1, gross_rents=Decimal("500"))],
    )

    assert [record[RENTAL_PROPERTY_UNITS] for record in rows.records] == [2, 1]
    assert [record[RENTAL_PROPERTY_GROSS_RENTS] for record in rows.records] == [
        Decimal("24000"),
        Decimal("500"),
    ]
    assert rows.records[0][RENTAL_PROPERTY_SHORT_TERM_RENTS] == Decimal("0")


def test_the_rental_properties_may_be_empty() -> None:
    assert RecordList(RENTAL_PROPERTIES.fields, []).records == ()


@pytest.mark.parametrize("field", ["units", "short_term_rents", "gross_rents"])
def test_a_rental_property_row_refuses_a_negative_column(field: str) -> None:
    value: object = -1 if field == "units" else Decimal("-1")

    with pytest.raises(NegativeArtifactError, match="item 1"):
        RecordList(RENTAL_PROPERTIES.fields, [rental_property_record(**{field: value})])


def test_a_rental_property_row_refuses_a_fractional_number_of_units() -> None:
    with pytest.raises(TypeError, match="item 1.*rental_property_units"):
        RecordList(RENTAL_PROPERTIES.fields, [rental_property_record(units=Decimal("2"))])


def test_a_rental_property_row_missing_a_column_is_refused_naming_the_row() -> None:
    record = rental_property_record()
    del record[RENTAL_PROPERTY_GROSS_RENTS]

    with pytest.raises(InvalidRecordError, match="item 1.*rental_property_gross_rents"):
        RecordList(RENTAL_PROPERTIES.fields, [record])


# Form T776 Part 3 and Part 4 lines that are never below zero: the Part 3 totals and other income,
# every "Total expenses", "Personal portion of total expenses" and "Short-term rental portion of
# total expenses" box of the 13 expense lines and their totals (A, 9949, 9365, 9366), line 1
# "Deductible expenses (amount A minus line 9949 minus line 9366)", the co-owner's, partner's and
# CCA lines that print a positive figure (9945, 9947, 9948, 9936, 9974, 9943).
T776_NON_NEGATIVE_LINES = [
    ("ca/short_term_rental_gross_rents", SHORT_TERM_RENTAL_GROSS_RENTS),
    ("ca/rental_gross_rents", RENTAL_GROSS_RENTS),
    ("ca/rental_other_income", RENTAL_OTHER_INCOME),
    ("ca/gross_rental_income", GROSS_RENTAL_INCOME),
    ("ca/rental_advertising", RENTAL_ADVERTISING),
    ("ca/rental_advertising_personal_portion", RENTAL_ADVERTISING_PERSONAL_PORTION),
    ("ca/rental_advertising_short_term_portion", RENTAL_ADVERTISING_SHORT_TERM_PORTION),
    ("ca/rental_insurance", RENTAL_INSURANCE),
    ("ca/rental_insurance_personal_portion", RENTAL_INSURANCE_PERSONAL_PORTION),
    ("ca/rental_insurance_short_term_portion", RENTAL_INSURANCE_SHORT_TERM_PORTION),
    ("ca/rental_interest_and_bank_charges", RENTAL_INTEREST_AND_BANK_CHARGES),
    (
        "ca/rental_interest_and_bank_charges_personal_portion",
        RENTAL_INTEREST_AND_BANK_CHARGES_PERSONAL_PORTION,
    ),
    (
        "ca/rental_interest_and_bank_charges_short_term_portion",
        RENTAL_INTEREST_AND_BANK_CHARGES_SHORT_TERM_PORTION,
    ),
    ("ca/rental_office_expenses", RENTAL_OFFICE_EXPENSES),
    ("ca/rental_office_expenses_personal_portion", RENTAL_OFFICE_EXPENSES_PERSONAL_PORTION),
    ("ca/rental_office_expenses_short_term_portion", RENTAL_OFFICE_EXPENSES_SHORT_TERM_PORTION),
    ("ca/rental_professional_fees", RENTAL_PROFESSIONAL_FEES),
    ("ca/rental_professional_fees_personal_portion", RENTAL_PROFESSIONAL_FEES_PERSONAL_PORTION),
    ("ca/rental_professional_fees_short_term_portion", RENTAL_PROFESSIONAL_FEES_SHORT_TERM_PORTION),
    ("ca/rental_management_and_administration_fees", RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES),
    (
        "ca/rental_management_and_administration_fees_personal_portion",
        RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_PERSONAL_PORTION,
    ),
    (
        "ca/rental_management_and_administration_fees_short_term_portion",
        RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_SHORT_TERM_PORTION,
    ),
    ("ca/rental_repairs_and_maintenance", RENTAL_REPAIRS_AND_MAINTENANCE),
    (
        "ca/rental_repairs_and_maintenance_personal_portion",
        RENTAL_REPAIRS_AND_MAINTENANCE_PERSONAL_PORTION,
    ),
    (
        "ca/rental_repairs_and_maintenance_short_term_portion",
        RENTAL_REPAIRS_AND_MAINTENANCE_SHORT_TERM_PORTION,
    ),
    ("ca/rental_salaries_wages_and_benefits", RENTAL_SALARIES_WAGES_AND_BENEFITS),
    (
        "ca/rental_salaries_wages_and_benefits_personal_portion",
        RENTAL_SALARIES_WAGES_AND_BENEFITS_PERSONAL_PORTION,
    ),
    (
        "ca/rental_salaries_wages_and_benefits_short_term_portion",
        RENTAL_SALARIES_WAGES_AND_BENEFITS_SHORT_TERM_PORTION,
    ),
    ("ca/rental_property_taxes", RENTAL_PROPERTY_TAXES),
    ("ca/rental_property_taxes_personal_portion", RENTAL_PROPERTY_TAXES_PERSONAL_PORTION),
    ("ca/rental_property_taxes_short_term_portion", RENTAL_PROPERTY_TAXES_SHORT_TERM_PORTION),
    ("ca/rental_travel", RENTAL_TRAVEL),
    ("ca/rental_travel_personal_portion", RENTAL_TRAVEL_PERSONAL_PORTION),
    ("ca/rental_travel_short_term_portion", RENTAL_TRAVEL_SHORT_TERM_PORTION),
    ("ca/rental_utilities", RENTAL_UTILITIES),
    ("ca/rental_utilities_personal_portion", RENTAL_UTILITIES_PERSONAL_PORTION),
    ("ca/rental_utilities_short_term_portion", RENTAL_UTILITIES_SHORT_TERM_PORTION),
    ("ca/rental_motor_vehicle_expenses", RENTAL_MOTOR_VEHICLE_EXPENSES),
    (
        "ca/rental_motor_vehicle_expenses_personal_portion",
        RENTAL_MOTOR_VEHICLE_EXPENSES_PERSONAL_PORTION,
    ),
    (
        "ca/rental_motor_vehicle_expenses_short_term_portion",
        RENTAL_MOTOR_VEHICLE_EXPENSES_SHORT_TERM_PORTION,
    ),
    ("ca/rental_other_expenses", RENTAL_OTHER_EXPENSES),
    ("ca/rental_other_expenses_personal_portion", RENTAL_OTHER_EXPENSES_PERSONAL_PORTION),
    ("ca/rental_other_expenses_short_term_portion", RENTAL_OTHER_EXPENSES_SHORT_TERM_PORTION),
    ("ca/rental_total_expenses", RENTAL_TOTAL_EXPENSES),
    ("ca/rental_personal_portion", RENTAL_PERSONAL_PORTION),
    ("ca/rental_short_term_portion", RENTAL_SHORT_TERM_PORTION),
    ("ca/rental_non_compliant_expenses", RENTAL_NON_COMPLIANT_EXPENSES),
    ("ca/rental_expenses_less_personal_portion", RENTAL_EXPENSES_LESS_PERSONAL_PORTION),
    ("ca/rental_deductible_expenses", RENTAL_DEDUCTIBLE_EXPENSES),
    ("ca/rental_coowner_other_expenses", RENTAL_COOWNER_OTHER_EXPENSES),
    ("ca/rental_recaptured_cca", RENTAL_RECAPTURED_CCA),
    ("ca/rental_terminal_loss", RENTAL_TERMINAL_LOSS),
    ("ca/rental_cca_claim", RENTAL_CCA_CLAIM),
    ("ca/rental_partner_gst_hst_rebate", RENTAL_PARTNER_GST_HST_REBATE),
    ("ca/rental_partner_other_expenses", RENTAL_PARTNER_OTHER_EXPENSES),
]


@pytest.mark.parametrize(("identifier", "kind"), T776_NON_NEGATIVE_LINES)
def test_the_t776_lines_that_print_no_loss_are_non_negative_decimals(
    identifier: str, kind: ArtifactKind[Decimal], registry: ArtifactRegistry
) -> None:
    assert kind.identifier == identifier
    assert kind.value_type is Decimal
    assert kind.non_negative is True
    assert registry.kind(identifier) is kind


# Form T776 Part 4 lines that print "(loss)" or subtract with no floor, so may be below zero: line
# 9369 "Net income (loss) before adjustments", line 2 (the co-owner's share, entered as the form's
# amount 2), amounts 2 to 6, line 7 "Partners: your share of amount 6, or the amount from your T5013
# slip", the partnership's amount (line 7 plus line 9974 minus line 9943) and line 9946 "Your net
# income (loss)", which T1 line 12600 takes.
T776_SIGNED_LINES = [
    ("ca/rental_net_income_before_adjustments", RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS),
    ("ca/rental_coowner_share", RENTAL_COOWNER_SHARE),
    ("ca/rental_net_income_share", RENTAL_NET_INCOME_SHARE),
    ("ca/rental_net_income_after_coowner_expenses", RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES),
    ("ca/rental_net_income_with_recapture", RENTAL_NET_INCOME_WITH_RECAPTURE),
    ("ca/rental_net_income_after_terminal_loss", RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS),
    ("ca/rental_net_income_after_cca", RENTAL_NET_INCOME_AFTER_CCA),
    ("ca/rental_partner_share", RENTAL_PARTNER_SHARE),
    ("ca/rental_partner_share_with_rebate", RENTAL_PARTNER_SHARE_WITH_REBATE),
    ("ca/rental_partnership_net_income", RENTAL_PARTNERSHIP_NET_INCOME),
    ("ca/net_rental_income", NET_RENTAL_INCOME),
]


@pytest.mark.parametrize(("identifier", "kind"), T776_SIGNED_LINES)
def test_the_t776_lines_that_print_a_loss_are_signed_decimals(
    identifier: str, kind: ArtifactKind[Decimal], registry: ArtifactRegistry
) -> None:
    assert kind.identifier == identifier
    assert kind.value_type is Decimal
    assert kind.non_negative is False
    assert registry.kind(identifier) is kind
    assert identifier in SIGNED


@pytest.mark.parametrize(
    ("kind", "identifier"),
    [
        (RENTAL_COOWNER, "ca/rental_coowner"),
        (RENTAL_PARTNER, "ca/rental_partner"),
    ],
)
def test_the_co_owner_and_partner_counts_are_non_negative_int_counts(
    kind: ArtifactKind[int], identifier: str, registry: ArtifactRegistry
) -> None:
    # Part 4 line 2 "Co-owners: calculate your share of net income from line 9369" and line 7
    # "Partners: your share of amount 6": 1 if the filer is one, else 0, as the form takes it.
    assert kind.identifier == identifier
    assert kind.value_type is int
    assert kind.non_negative is True
    assert registry.kind(identifier) is kind


def test_each_expense_line_has_its_three_boxes() -> None:
    for _line, name in EXPENSE_LINE_NAMES:
        for suffix in ("", "_personal_portion", "_short_term_portion"):
            assert f"ca/rental_{name}{suffix}" in REGISTERED
    assert len(EXPENSE_LINE_NAMES) == 13


# Form T776 Part 4, each of the 13 expense lines (its line number and the name its three boxes
# share) with the boxes "Total expenses", "Personal portion of total expenses" and "Short-term
# rental portion of total expenses".
EXPENSE_LINE_NAMES = [
    (8521, "advertising"),
    (8690, "insurance"),
    (8710, "interest_and_bank_charges"),
    (8810, "office_expenses"),
    (8860, "professional_fees"),
    (8871, "management_and_administration_fees"),
    (8960, "repairs_and_maintenance"),
    (9060, "salaries_wages_and_benefits"),
    (9180, "property_taxes"),
    (9200, "travel"),
    (9220, "utilities"),
    (9281, "motor_vehicle_expenses"),
    (9270, "other_expenses"),
]


def test_medical_expenses_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # T1 line 107 and line 33099 "Medical expenses for self, spouse or common-law partner and
    # your dependent children under 18 years of age": a starting amount.
    assert MEDICAL_EXPENSES.identifier == "ca/medical_expenses"
    assert MEDICAL_EXPENSES.value_type is Decimal
    assert MEDICAL_EXPENSES.non_negative is True
    assert registry.kind("ca/medical_expenses") is MEDICAL_EXPENSES


def test_medical_net_income_share_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # T1 line 108 "Amount from line 23600" "multiplied by 3%".
    assert MEDICAL_NET_INCOME_SHARE.identifier == "ca/medical_net_income_share"
    assert MEDICAL_NET_INCOME_SHARE.value_type is Decimal
    assert MEDICAL_NET_INCOME_SHARE.non_negative is True
    assert registry.kind("ca/medical_net_income_share") is MEDICAL_NET_INCOME_SHARE


def test_medical_threshold_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # T1 line 109 "Enter whichever is less: $2,834 or the amount from line 108."
    assert MEDICAL_THRESHOLD.identifier == "ca/medical_threshold"
    assert MEDICAL_THRESHOLD.value_type is Decimal
    assert MEDICAL_THRESHOLD.non_negative is True
    assert registry.kind("ca/medical_threshold") is MEDICAL_THRESHOLD


def test_medical_expenses_over_threshold_is_a_non_negative_decimal(
    registry: ArtifactRegistry,
) -> None:
    # T1 line 110 "Line 107 minus line 109 (if negative, enter "0")".
    assert MEDICAL_EXPENSES_OVER_THRESHOLD.identifier == "ca/medical_expenses_over_threshold"
    assert MEDICAL_EXPENSES_OVER_THRESHOLD.value_type is Decimal
    assert MEDICAL_EXPENSES_OVER_THRESHOLD.non_negative is True
    assert registry.kind("ca/medical_expenses_over_threshold") is MEDICAL_EXPENSES_OVER_THRESHOLD


def test_medical_claim_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # T1 line 112 and line 33200 "Line 110 plus line 111".
    assert MEDICAL_CLAIM.identifier == "ca/medical_claim"
    assert MEDICAL_CLAIM.value_type is Decimal
    assert MEDICAL_CLAIM.non_negative is True
    assert registry.kind("ca/medical_claim") is MEDICAL_CLAIM


def test_the_disability_dependants_are_a_record_list_of_the_worksheets_figures(
    registry: ArtifactRegistry,
) -> None:
    # Federal Worksheet "Line 31800", per dependant: whether they were "under 18 years of age on
    # December 31, 2025", line 3 "Total of child care and attendant care expenses for your
    # dependant that you or another person claimed", line 9 "amount from line 98 of your
    # dependant's return" and line 11 "Dependant's taxable income from line 26000 of their
    # return": the four fields a record holds, in the worksheet's line order (the caller lists
    # only the dependants who qualify, so there are no eligibility fields).
    assert RECORD_LISTS <= REGISTERED
    assert isinstance(DISABILITY_DEPENDANTS, RecordListKind)
    assert DISABILITY_DEPENDANTS.identifier == "ca/disability_dependants"
    assert DISABILITY_DEPENDANTS.value_type is RecordList
    assert DISABILITY_DEPENDANTS.non_negative is False
    assert DISABILITY_DEPENDANTS.fields == (
        DEPENDANT_UNDER_18,
        DEPENDANT_CARE_EXPENSES,
        DEPENDANT_CREDIT_AMOUNTS,
        DEPENDANT_TAXABLE_INCOME,
    )
    assert registry.get("ca/disability_dependants") is DISABILITY_DEPENDANTS


def test_the_disability_dependants_fields_are_kinds_of_their_own() -> None:
    assert DEPENDANT_UNDER_18.identifier == "ca/dependant_under_18"
    assert DEPENDANT_CARE_EXPENSES.identifier == "ca/dependant_care_expenses"
    assert DEPENDANT_CREDIT_AMOUNTS.identifier == "ca/dependant_credit_amounts"
    assert DEPENDANT_TAXABLE_INCOME.identifier == "ca/dependant_taxable_income"
    # Not the net income of line 30400's dependant: another figure of another return.
    assert DEPENDANT_NET_INCOME not in DISABILITY_DEPENDANTS.fields
    for kind in DISABILITY_DEPENDANTS.fields:
        assert kind.non_negative is True, kind.identifier


def test_the_dependant_under_18_is_a_non_negative_int_count(registry: ArtifactRegistry) -> None:
    # "If the dependant was under 18 years of age on December 31, 2025, ...": a yes or no, taken
    # as a count of 0 or 1 like the forms' other yes or no questions.
    assert DEPENDANT_UNDER_18.value_type is int
    assert DEPENDANT_UNDER_18.non_negative is True
    assert registry.kind("ca/dependant_under_18") is DEPENDANT_UNDER_18


@pytest.mark.parametrize(
    "kind", [DEPENDANT_CARE_EXPENSES, DEPENDANT_CREDIT_AMOUNTS, DEPENDANT_TAXABLE_INCOME]
)
def test_the_disability_dependants_amounts_are_non_negative_decimals(
    kind: ArtifactKind[Decimal], registry: ArtifactRegistry
) -> None:
    assert kind.value_type is Decimal
    assert kind.non_negative is True
    assert registry.kind(kind.identifier) is kind


def disability_record(**changes: object) -> dict[ArtifactKind[Any], object]:
    """One dependant aged 20 with the ticket's chosen figures, with `changes` by field name."""
    record: dict[ArtifactKind[Any], object] = {
        DEPENDANT_UNDER_18: 0,
        DEPENDANT_CARE_EXPENSES: Decimal("0"),
        DEPENDANT_CREDIT_AMOUNTS: Decimal("16129"),
        DEPENDANT_TAXABLE_INCOME: Decimal("20000"),
    }
    names: dict[str, ArtifactKind[Any]] = {
        "under_18": DEPENDANT_UNDER_18,
        "care_expenses": DEPENDANT_CARE_EXPENSES,
        "credit_amounts": DEPENDANT_CREDIT_AMOUNTS,
        "taxable_income": DEPENDANT_TAXABLE_INCOME,
    }
    for name, value in changes.items():
        record[names[name]] = value
    return record


def test_the_disability_dependants_hold_the_four_figures_each_in_the_callers_order() -> None:
    dependants = RecordList(
        DISABILITY_DEPENDANTS.fields,
        [
            disability_record(),
            disability_record(under_18=1, care_expenses=Decimal("5000"), credit_amounts=Decimal(0)),
        ],
    )

    assert [record[DEPENDANT_UNDER_18] for record in dependants.records] == [0, 1]
    assert [record[DEPENDANT_CARE_EXPENSES] for record in dependants.records] == [
        Decimal("0"),
        Decimal("5000"),
    ]
    assert [record[DEPENDANT_CREDIT_AMOUNTS] for record in dependants.records] == [
        Decimal("16129"),
        Decimal("0"),
    ]
    assert [record[DEPENDANT_TAXABLE_INCOME] for record in dependants.records] == [
        Decimal("20000"),
        Decimal("20000"),
    ]


def test_there_may_be_no_disability_dependants() -> None:
    assert RecordList(DISABILITY_DEPENDANTS.fields, []).records == ()


@pytest.mark.parametrize(
    "missing",
    [
        DEPENDANT_UNDER_18,
        DEPENDANT_CARE_EXPENSES,
        DEPENDANT_CREDIT_AMOUNTS,
        DEPENDANT_TAXABLE_INCOME,
    ],
)
def test_a_disability_dependant_missing_a_figure_is_an_invalid_record(
    missing: ArtifactKind[Any],
) -> None:
    record = disability_record()
    del record[missing]

    with pytest.raises(InvalidRecordError, match=f"item 1: missing field {missing.identifier}"):
        RecordList(DISABILITY_DEPENDANTS.fields, [record])


def test_the_second_disability_dependant_is_named_by_its_position() -> None:
    record = disability_record()
    del record[DEPENDANT_TAXABLE_INCOME]

    with pytest.raises(
        InvalidRecordError, match="item 2: missing field ca/dependant_taxable_income"
    ):
        RecordList(DISABILITY_DEPENDANTS.fields, [disability_record(), record])


def test_a_disability_dependant_with_another_figure_is_an_invalid_record() -> None:
    record = disability_record()
    record[DEPENDANT_NET_INCOME] = Decimal("5000")

    with pytest.raises(InvalidRecordError, match="item 1: unknown field ca/dependant_net_income"):
        RecordList(DISABILITY_DEPENDANTS.fields, [record])


@pytest.mark.parametrize(
    ("change", "identifier"),
    [
        ({"under_18": -1}, "ca/dependant_under_18"),
        ({"care_expenses": Decimal("-0.01")}, "ca/dependant_care_expenses"),
        ({"credit_amounts": Decimal("-1")}, "ca/dependant_credit_amounts"),
        ({"taxable_income": Decimal("-1")}, "ca/dependant_taxable_income"),
    ],
)
def test_a_negative_disability_dependant_figure_is_refused(
    change: dict[str, object], identifier: str
) -> None:
    with pytest.raises(NegativeArtifactError, match=f"item 1: {identifier} cannot be negative"):
        RecordList(DISABILITY_DEPENDANTS.fields, [disability_record(**change)])


@pytest.mark.parametrize(
    "change",
    [
        {"under_18": Decimal("1")},
        {"under_18": True},
        {"care_expenses": 5000},
        {"credit_amounts": "16129"},
        {"taxable_income": 20000.0},
    ],
)
def test_a_disability_dependant_figure_of_the_wrong_type_is_refused(
    change: dict[str, object],
) -> None:
    with pytest.raises(TypeError):
        RecordList(DISABILITY_DEPENDANTS.fields, [disability_record(**change)])


def test_the_disability_transferred_amount_is_a_non_negative_decimal(
    registry: ArtifactRegistry,
) -> None:
    # T1 line 100 (line 31800) "Disability amount transferred from a dependant (use Federal
    # Worksheet)": the total of the worksheet's line 13 amounts, each the lesser of two amounts
    # that are at least "0".
    assert DISABILITY_TRANSFERRED_AMOUNT.identifier == "ca/disability_transferred_amount"
    assert DISABILITY_TRANSFERRED_AMOUNT.value_type is Decimal
    assert DISABILITY_TRANSFERRED_AMOUNT.non_negative is True
    assert registry.kind("ca/disability_transferred_amount") is DISABILITY_TRANSFERRED_AMOUNT


def test_the_principal_residence_properties_are_a_record_list_of_the_forms_input_lines(
    registry: ArtifactRegistry,
) -> None:
    # Form T2091(IND), per property ("Complete a separate form for each property you sold."):
    # line 1 and line 2 the years designated "After 1981" and "After 1971 and before 1982", line 5
    # and line 6 the years owned in the same periods, line 8 "Proceeds of disposition or deemed
    # disposition", line 9 "Outlays and expenses made or incurred related to the disposition",
    # line 10 "Adjusted cost base at the time of disposition", and whether the "plus one" rule
    # applies: the fields a record holds, in the form's line order (lines 3, 4, 7 and 14 onward
    # are worked out).
    assert RECORD_LISTS <= REGISTERED
    assert isinstance(PRINCIPAL_RESIDENCE_PROPERTIES, RecordListKind)
    assert PRINCIPAL_RESIDENCE_PROPERTIES.identifier == "ca/principal_residence_properties"
    assert PRINCIPAL_RESIDENCE_PROPERTIES.value_type is RecordList
    assert PRINCIPAL_RESIDENCE_PROPERTIES.non_negative is False
    assert PRINCIPAL_RESIDENCE_PROPERTIES.fields == (
        RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
        RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
        RESIDENCE_YEARS_OWNED_AFTER_1981,
        RESIDENCE_YEARS_OWNED_1972_TO_1981,
        RESIDENCE_PROCEEDS,
        RESIDENCE_OUTLAYS,
        RESIDENCE_ADJUSTED_COST_BASE,
        RESIDENCE_PLUS_ONE_YEAR,
    )
    assert registry.get("ca/principal_residence_properties") is PRINCIPAL_RESIDENCE_PROPERTIES


def test_the_principal_residence_properties_fields_are_kinds_of_their_own() -> None:
    assert RESIDENCE_YEARS_DESIGNATED_AFTER_1981.identifier == (
        "ca/residence_years_designated_after_1981"
    )
    assert RESIDENCE_YEARS_DESIGNATED_1972_TO_1981.identifier == (
        "ca/residence_years_designated_1972_to_1981"
    )
    assert RESIDENCE_YEARS_OWNED_AFTER_1981.identifier == "ca/residence_years_owned_after_1981"
    assert RESIDENCE_YEARS_OWNED_1972_TO_1981.identifier == (
        "ca/residence_years_owned_1972_to_1981"
    )
    assert RESIDENCE_PROCEEDS.identifier == "ca/residence_proceeds"
    assert RESIDENCE_OUTLAYS.identifier == "ca/residence_outlays"
    assert RESIDENCE_ADJUSTED_COST_BASE.identifier == "ca/residence_adjusted_cost_base"
    assert RESIDENCE_PLUS_ONE_YEAR.identifier == "ca/residence_plus_one_year"
    for kind in PRINCIPAL_RESIDENCE_PROPERTIES.fields:
        assert kind.non_negative is True, kind.identifier


@pytest.mark.parametrize(
    "kind",
    [
        RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
        RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
        RESIDENCE_YEARS_OWNED_AFTER_1981,
        RESIDENCE_YEARS_OWNED_1972_TO_1981,
        RESIDENCE_PLUS_ONE_YEAR,
    ],
)
def test_the_residence_years_and_the_plus_one_are_non_negative_int_counts(
    kind: ArtifactKind[int], registry: ArtifactRegistry
) -> None:
    # Lines 1, 2, 5 and 6 are numbers of tax years; the "plus one" is a yes or no, taken as a count
    # of 0 or 1 like the forms' other yes or no questions.
    assert kind.value_type is int
    assert kind.non_negative is True
    assert registry.kind(kind.identifier) is kind


@pytest.mark.parametrize(
    "kind", [RESIDENCE_PROCEEDS, RESIDENCE_OUTLAYS, RESIDENCE_ADJUSTED_COST_BASE]
)
def test_the_residence_amounts_are_non_negative_decimals(
    kind: ArtifactKind[Decimal], registry: ArtifactRegistry
) -> None:
    assert kind.value_type is Decimal
    assert kind.non_negative is True
    assert registry.kind(kind.identifier) is kind


def residence_record(**changes: object) -> dict[ArtifactKind[Any], object]:
    """One property with the ticket's example figures, with `changes` by field name."""
    record: dict[ArtifactKind[Any], object] = {
        RESIDENCE_YEARS_DESIGNATED_AFTER_1981: 6,
        RESIDENCE_YEARS_DESIGNATED_1972_TO_1981: 0,
        RESIDENCE_YEARS_OWNED_AFTER_1981: 10,
        RESIDENCE_YEARS_OWNED_1972_TO_1981: 0,
        RESIDENCE_PROCEEDS: Decimal("400000"),
        RESIDENCE_OUTLAYS: Decimal("5000"),
        RESIDENCE_ADJUSTED_COST_BASE: Decimal("95000"),
        RESIDENCE_PLUS_ONE_YEAR: 1,
    }
    names: dict[str, ArtifactKind[Any]] = {
        "designated_after_1981": RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
        "designated_1972_to_1981": RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
        "owned_after_1981": RESIDENCE_YEARS_OWNED_AFTER_1981,
        "owned_1972_to_1981": RESIDENCE_YEARS_OWNED_1972_TO_1981,
        "proceeds": RESIDENCE_PROCEEDS,
        "outlays": RESIDENCE_OUTLAYS,
        "adjusted_cost_base": RESIDENCE_ADJUSTED_COST_BASE,
        "plus_one": RESIDENCE_PLUS_ONE_YEAR,
    }
    for name, value in changes.items():
        record[names[name]] = value
    return record


def test_the_principal_residence_properties_hold_the_eight_figures_each_in_the_callers_order() -> (
    None
):
    properties = RecordList(
        PRINCIPAL_RESIDENCE_PROPERTIES.fields,
        [
            residence_record(),
            residence_record(
                designated_after_1981=2,
                designated_1972_to_1981=3,
                owned_after_1981=6,
                owned_1972_to_1981=4,
                proceeds=Decimal("500000"),
                outlays=Decimal("0"),
                plus_one=0,
            ),
        ],
    )

    assert [record[RESIDENCE_YEARS_DESIGNATED_AFTER_1981] for record in properties.records] == [
        6,
        2,
    ]
    assert [record[RESIDENCE_YEARS_DESIGNATED_1972_TO_1981] for record in properties.records] == [
        0,
        3,
    ]
    assert [record[RESIDENCE_YEARS_OWNED_AFTER_1981] for record in properties.records] == [10, 6]
    assert [record[RESIDENCE_YEARS_OWNED_1972_TO_1981] for record in properties.records] == [0, 4]
    assert [record[RESIDENCE_PROCEEDS] for record in properties.records] == [
        Decimal("400000"),
        Decimal("500000"),
    ]
    assert [record[RESIDENCE_OUTLAYS] for record in properties.records] == [
        Decimal("5000"),
        Decimal("0"),
    ]
    assert [record[RESIDENCE_ADJUSTED_COST_BASE] for record in properties.records] == [
        Decimal("95000"),
        Decimal("95000"),
    ]
    assert [record[RESIDENCE_PLUS_ONE_YEAR] for record in properties.records] == [1, 0]


def test_there_may_be_no_principal_residence_properties() -> None:
    assert RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, []).records == ()


@pytest.mark.parametrize("missing", PRINCIPAL_RESIDENCE_PROPERTIES.fields)
def test_a_property_missing_a_figure_is_an_invalid_record(missing: ArtifactKind[Any]) -> None:
    record = residence_record()
    del record[missing]

    with pytest.raises(InvalidRecordError, match=f"item 1: missing field {missing.identifier}"):
        RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, [record])


def test_the_second_property_is_named_by_its_position() -> None:
    record = residence_record()
    del record[RESIDENCE_PROCEEDS]

    with pytest.raises(InvalidRecordError, match="item 2: missing field ca/residence_proceeds"):
        RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, [residence_record(), record])


def test_a_property_with_another_figure_is_an_invalid_record() -> None:
    record = residence_record()
    record[CAPITAL_GAIN] = Decimal("300000")

    with pytest.raises(InvalidRecordError, match="item 1: unknown field ca/capital_gain"):
        RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, [record])


@pytest.mark.parametrize(
    ("change", "identifier"),
    [
        ({"designated_after_1981": -1}, "ca/residence_years_designated_after_1981"),
        ({"designated_1972_to_1981": -1}, "ca/residence_years_designated_1972_to_1981"),
        ({"owned_after_1981": -1}, "ca/residence_years_owned_after_1981"),
        ({"owned_1972_to_1981": -1}, "ca/residence_years_owned_1972_to_1981"),
        ({"proceeds": Decimal("-0.01")}, "ca/residence_proceeds"),
        ({"outlays": Decimal("-1")}, "ca/residence_outlays"),
        ({"adjusted_cost_base": Decimal("-1")}, "ca/residence_adjusted_cost_base"),
        ({"plus_one": -1}, "ca/residence_plus_one_year"),
    ],
)
def test_a_negative_property_figure_is_refused(change: dict[str, object], identifier: str) -> None:
    with pytest.raises(NegativeArtifactError, match=f"item 1: {identifier} cannot be negative"):
        RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, [residence_record(**change)])


@pytest.mark.parametrize(
    "change",
    [
        {"designated_after_1981": Decimal("6")},
        {"owned_after_1981": True},
        {"owned_1972_to_1981": 1.0},
        {"plus_one": Decimal("1")},
        {"proceeds": 400000},
        {"outlays": "5000"},
        {"adjusted_cost_base": 95000.0},
    ],
)
def test_a_property_figure_of_the_wrong_type_is_refused(change: dict[str, object]) -> None:
    with pytest.raises(TypeError):
        RecordList(PRINCIPAL_RESIDENCE_PROPERTIES.fields, [residence_record(**change)])


def test_the_principal_residence_gain_is_a_non_negative_decimal(registry: ArtifactRegistry) -> None:
    # Form T2091(IND) Part 3 line 54 "Total capital gain": line 24 "Line 18 minus line 23 (if
    # negative, enter "0")" for each property, totalled here.
    assert PRINCIPAL_RESIDENCE_GAIN.identifier == "ca/principal_residence_gain"
    assert PRINCIPAL_RESIDENCE_GAIN.value_type is Decimal
    assert PRINCIPAL_RESIDENCE_GAIN.non_negative is True
    assert registry.kind("ca/principal_residence_gain") is PRINCIPAL_RESIDENCE_GAIN


# --- the capital cost allowance table, one record per class -------------------------------------
#
# T776 Area A, "Calculation of capital cost allowance (CCA) claim", one row per class, and T2125
# Area A with the same columns: the fields each class's record holds, shared by the rental and the
# business lists (each list is declared when its form is wired). Columns 4, 6, 8 and 9 (DIEPs) are
# left out, so column 10 is column 3 and column 13 is column 7.


@pytest.mark.parametrize(
    ("kind", "identifier"),
    [
        # "Column 1: Class number": a number such as 10.1 or 43.1, so a Decimal.
        (CCA_CLASS_NUMBER, "ca/cca_class_number"),
        # "Column 2: Undepreciated capital cost (UCC) at the start of the year".
        (CCA_UCC_AT_START, "ca/cca_ucc_at_start"),
        # "Column 3: Cost of additions in the year".
        (CCA_ADDITIONS, "ca/cca_additions"),
        # "Column 5: Proceeds of dispositions in the year".
        (CCA_PROCEEDS, "ca/cca_proceeds"),
        # "Column 11: Cost of remaining additions from column 10 that are AIIPs or ZEVs acquired
        # before 2025".
        (CCA_AIIP_ADDITIONS, "ca/cca_aiip_additions"),
        # "Column 12: Cost of remaining additions from column 10 that are RIIPs or ZEVs acquired
        # after 2024".
        (CCA_RIIP_ADDITIONS, "ca/cca_riip_additions"),
        # T776 "Column 23: CCA claim for the year" (T2125 column 21): the amount claimed, an
        # election from 0 to the class's maximum.
        (CCA_CLAIMED, "ca/cca_claimed"),
        # T776 "Column 24: UCC at the end of the year (column 7 minus column 23)" (T2125 column
        # 22): a field of the closing list for next year.
        (CCA_UCC_AT_END, "ca/cca_ucc_at_end"),
    ],
)
def test_the_cca_table_fields_are_non_negative_decimals(
    registry: ArtifactRegistry, kind: ArtifactKind[Any], identifier: str
) -> None:
    assert kind.identifier == identifier
    assert kind.value_type is Decimal
    assert kind.non_negative is True
    assert registry.kind(identifier) is kind


def test_no_property_left_in_the_class_is_a_non_negative_int_count(
    registry: ArtifactRegistry,
) -> None:
    # Note 3: "If no property is left in the class and there is a positive amount in this column,
    # deduct the amount from your income as a terminal loss": a caller's 1 if no property is left
    # in the class at the end of the year, else 0, as the other 0 or 1 counts of the forms.
    assert CCA_NO_PROPERTY_LEFT.identifier == "ca/cca_no_property_left"
    assert CCA_NO_PROPERTY_LEFT.value_type is int
    assert CCA_NO_PROPERTY_LEFT.non_negative is True
    assert registry.kind("ca/cca_no_property_left") is CCA_NO_PROPERTY_LEFT


def test_the_cca_table_fields_are_kinds_of_their_own() -> None:
    kinds = (
        CCA_CLASS_NUMBER,
        CCA_UCC_AT_START,
        CCA_ADDITIONS,
        CCA_PROCEEDS,
        CCA_AIIP_ADDITIONS,
        CCA_RIIP_ADDITIONS,
        CCA_CLAIMED,
        CCA_NO_PROPERTY_LEFT,
        CCA_UCC_AT_END,
    )

    assert len({kind.identifier for kind in kinds}) == 9
    assert {kind.identifier for kind in kinds} <= REGISTERED
    assert not {kind.identifier for kind in kinds} & RECORD_LISTS


def test_the_cca_table_fields_hold_one_class_per_record() -> None:
    fields = (
        CCA_CLASS_NUMBER,
        CCA_UCC_AT_START,
        CCA_ADDITIONS,
        CCA_PROCEEDS,
        CCA_AIIP_ADDITIONS,
        CCA_RIIP_ADDITIONS,
        CCA_CLAIMED,
        CCA_NO_PROPERTY_LEFT,
    )
    classes = RecordList(
        fields,
        [
            {
                CCA_CLASS_NUMBER: Decimal("10.1"),
                CCA_UCC_AT_START: Decimal("20000"),
                CCA_ADDITIONS: Decimal("0"),
                CCA_PROCEEDS: Decimal("0"),
                CCA_AIIP_ADDITIONS: Decimal("0"),
                CCA_RIIP_ADDITIONS: Decimal("0"),
                CCA_CLAIMED: Decimal("6000"),
                CCA_NO_PROPERTY_LEFT: 0,
            }
        ],
    )

    (record,) = classes.records
    assert record[CCA_CLASS_NUMBER] == Decimal("10.1")
    assert record[CCA_NO_PROPERTY_LEFT] == 0


def test_a_negative_cca_claim_is_refused() -> None:
    # T4036: "You can claim any amount you like, from zero to the maximum allowed for the year."
    with pytest.raises(NegativeArtifactError, match="item 1: ca/cca_claimed cannot be negative"):
        RecordList(
            (CCA_CLASS_NUMBER, CCA_CLAIMED),
            [{CCA_CLASS_NUMBER: Decimal("8"), CCA_CLAIMED: Decimal("-1")}],
        )


def test_the_special_tax_and_credit_lines_are_non_negative(registry: ArtifactRegistry) -> None:
    # T1 lines 131, 41300, 41400, 41500 and 41800 and the forms behind them (T2038(IND) Part C,
    # T1172 Parts A and B, the RC210 box 10 and the RL-10 slip) print amounts of tax, credit or
    # expenditure with no negative figure; the lines that carry or subtract them print a floor
    # or cannot be negative: line 132 adds line 131 to line 126, line 139 is "if negative, enter
    # "0"" and T1172's line 3 is the lesser of two such amounts, line 8 is line 1 less a line 7
    # that is at most line 1.
    for kind in (
        ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT,
        ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT,
        LABOUR_SPONSORED_FUNDS_NET_COST,
        ADVANCED_CANADA_WORKERS_BENEFIT,
        RESP_AIPS_RECEIVED_PART_A,
        RESP_AIPS_RRSP_CONTRIBUTIONS,
        RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS,
        RESP_AIPS_RECEIVED_PART_B,
        RL_10_LABOUR_SPONSORED_FUND_AMOUNT,
        POLITICAL_CONTRIBUTIONS,
        ITC_RECAPTURE_AT_15_PERCENT,
        ITC_RECAPTURE_AT_20_PERCENT,
        ITC_RECAPTURE,
        FEDERAL_TAX_WITH_ITC_RECAPTURE,
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
        POLITICAL_CREDIT_CHOSEN_COLUMN,
        POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
        POLITICAL_CREDIT_SHORTCUT_AMOUNT,
        POLITICAL_CREDIT_BEFORE_MAXIMUM,
        POLITICAL_CREDIT,
        LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
        LABOUR_SPONSORED_FUNDS_CREDIT,
        CREDITS_AGAINST_FEDERAL_TAX,
        FEDERAL_TAX_LESS_CREDITS,
        RESP_AIPS_CONTRIBUTIONS_COUNTED,
        RESP_AIPS_LIFETIME_LIMIT,
        RESP_AIPS_SUBJECT_TO_TAX,
        RESP_AIPS_PART_A_TAX,
        RESP_AIPS_PART_B_TAX,
        RESP_AIPS_ADDITIONAL_TAX,
        SPECIAL_TAXES,
    ):
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier).non_negative is True, kind.identifier


def test_the_t1172_lines_that_print_no_floor_are_signed(registry: ArtifactRegistry) -> None:
    # Form T1172 Part A: line 6 "Line 4 minus line 5" and line 7 "Amount from line 3 or 6, whichever
    # is less" print no "(if negative, enter "0")", so line 5 above 50,000.00 would make them
    # negative, as the form prints; line 8 "line 1 minus line 7" is never negative as line 7 is at
    # most line 3, which is at most line 1.
    assert RESP_AIPS_LIMIT_REMAINING.non_negative is False
    assert RESP_AIPS_REDUCTION.non_negative is False
    assert registry.kind("ca/resp_aips_limit_remaining").non_negative is False
    assert registry.kind("ca/resp_aips_reduction").non_negative is False
    assert RESP_AIPS_CONTRIBUTIONS_COUNTED.non_negative is True
    assert RESP_AIPS_SUBJECT_TO_TAX.non_negative is True


def test_the_t1172_part_a_count_is_a_non_negative_int() -> None:
    # Form T1172 "Part B - Fill out this part only if Part A does not apply to you": a caller's 0
    # (Part B) or 1 (Part A) count, as the other 0 or 1 counts of the forms.
    assert RESP_AIPS_PART_A_APPLIES.value_type is int
    assert RESP_AIPS_PART_A_APPLIES.non_negative is True


def test_the_medical_supplement_counts_are_non_negative_int_counts(
    registry: ArtifactRegistry,
) -> None:
    # Federal Worksheet "Line 45200 - Refundable medical expense supplement": "You were resident
    # in Canada throughout 2025" and "You were 18 years of age or older at the end of 2025", each
    # a caller's 0 or 1 count as the other 0 or 1 counts of the forms.
    for kind in (RESIDENT_IN_CANADA_THROUGHOUT_2025, AGED_18_OR_OLDER_AT_END_OF_2025):
        assert kind.value_type is int, kind.identifier
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier) is kind
        assert kind.identifier in COUNTS


def test_the_medical_supplement_lines_that_print_no_floor_are_signed(
    registry: ArtifactRegistry,
) -> None:
    # Federal Worksheet "Line 45200 - Refundable medical expense supplement": column line 3 "Line 1
    # plus line 2" prints no "(if negative, enter "0")" and line 1 may be negative ("the amount you
    # would have entered if the instructions on line 23600 said "if negative, show in brackets""),
    # so the spouse's line 1 and each column's line 3 are signed; so is the employment income less
    # the wage-loss replacement plan amounts, which the worksheet floors only after the deductions
    # ("if the result is negative, consider it as "0"").
    for kind in (
        SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS,
        MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS,
        MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3,
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3,
    ):
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is False, kind.identifier
        assert registry.kind(kind.identifier) is kind
        assert kind.identifier in SIGNED


def test_the_other_medical_supplement_lines_are_non_negative_decimals(
    registry: ArtifactRegistry,
) -> None:
    # The lines that print "(if negative, enter "0")", add non-negative figures, take a lesser or
    # are caller amounts the forms never print as negative.
    signed = {
        "ca/spouse_net_income_before_adjustments",
        "ca/medical_supplement_employment_income_less_wage_loss",
        "ca/medical_supplement_column_1_line_3",
        "ca/medical_supplement_column_2_line_3",
    }
    kinds = (
        DISABILITY_SUPPORTS_DEDUCTION,
        OTHER_EMPLOYMENT_EXPENSES,
        CLERGY_RESIDENCE_DEDUCTION,
        NET_BUSINESS_INCOME,
        NET_PROFESSIONAL_INCOME,
        NET_COMMISSION_INCOME,
        NET_FARMING_INCOME,
        NET_FISHING_INCOME,
        WAGE_LOSS_REPLACEMENT_PLAN_INCOME,
        SPOUSE_UCCB_REPAYMENT,
        SPOUSE_RDSP_INCOME_REPAYMENT,
        SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT,
        SPOUSE_RDSP_INCOME,
        MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME,
        MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS,
        MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME,
        MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME,
        MEDICAL_SUPPLEMENT_WORKING_INCOME,
        MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5,
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2,
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
    )
    for kind in kinds:
        assert kind.identifier not in signed, kind.identifier
        assert kind.value_type is Decimal, kind.identifier
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier).non_negative is True, kind.identifier


# --- Form T2222, Northern Residents Deductions (T1 line 66 and line 25500) ---------------------


def test_the_record_lists_are_record_list_kinds_with_their_forms_fields(
    registry: ArtifactRegistry,
) -> None:
    # Step 3 Chart B: "Column 1: Enter the name of the person who took the trip", the zone the
    # trip's amount goes in (columns 6 and 7), and "Column 3", "Column 4" and "Column 5".
    assert RECORD_LISTS <= REGISTERED
    assert registry.get("ca/travel_trips") is TRAVEL_TRIPS
    assert registry.get("ca/travel_individuals") is TRAVEL_INDIVIDUALS
    assert isinstance(TRAVEL_TRIPS, RecordListKind)
    assert isinstance(TRAVEL_INDIVIDUALS, RecordListKind)
    assert TRAVEL_TRIPS.fields == (
        TRAVEL_INDIVIDUAL,
        TRIP_ZONE,
        TRIP_BENEFIT_OR_STANDARD_AMOUNT,
        TRIP_TRAVEL_EXPENSES,
        TRIP_LOWEST_RETURN_AIRFARE,
    )
    # Chart A: "Row A: Enter the name of each individual" and the three amounts of "Row B".
    assert TRAVEL_INDIVIDUALS.fields == (
        TRAVEL_INDIVIDUAL,
        STANDARD_AMOUNT_ALLOCATED_1,
        STANDARD_AMOUNT_ALLOCATED_2,
        STANDARD_AMOUNT_ALLOCATED_3,
    )


def test_the_chart_fields_are_non_negative_counts_and_amounts() -> None:
    for kind in (TRAVEL_INDIVIDUAL, TRIP_ZONE):
        assert kind.value_type is int, kind.identifier
        assert kind.non_negative is True, kind.identifier
    for amount_kind in (
        TRIP_BENEFIT_OR_STANDARD_AMOUNT,
        TRIP_TRAVEL_EXPENSES,
        TRIP_LOWEST_RETURN_AIRFARE,
        STANDARD_AMOUNT_ALLOCATED_1,
        STANDARD_AMOUNT_ALLOCATED_2,
        STANDARD_AMOUNT_ALLOCATED_3,
    ):
        assert amount_kind.value_type is Decimal, amount_kind.identifier
        assert amount_kind.non_negative is True, amount_kind.identifier


def test_the_step_2_residency_lines_are_non_negative() -> None:
    # Line 5 "Line 3 minus line 4 (if negative, enter "0")" and line 10 "Line 8 minus line 9 (if
    # negative, enter "0")" print a floor, and no other line of Steps 2 to 4 can be below zero.
    for kind in (
        ZONE_A_RESIDENCY_AFTER_WORK_SITE,
        ZONE_B_RESIDENCY_AFTER_WORK_SITE,
        RESIDENCY_AMOUNT,
        RESIDENCY_NET_INCOME_LIMIT,
        RESIDENCY_DEDUCTION,
        TRAVEL_DEDUCTION,
        NORTHERN_RESIDENTS_DEDUCTIONS,
    ):
        assert kind.non_negative is True, kind.identifier


def test_the_self_employment_incomes_and_the_pensionable_earnings_are_signed(
    registry: ArtifactRegistry,
) -> None:
    # T1 lines 13500, 13700, 13900, 14100 and 14300 "Net" (a loss when the expenses are larger),
    # line 27 "Add lines 22 to 26. Net self-employment income" and Schedule 8 Part 4 line 1
    # "amount from line 12200 of your return plus line 27 of your return" print no floor.
    for kind in (
        BUSINESS_INCOME,
        PROFESSIONAL_INCOME,
        COMMISSION_INCOME,
        FARMING_INCOME,
        FISHING_INCOME,
        NET_SELF_EMPLOYMENT_INCOME,
        PENSIONABLE_NET_SELF_EMPLOYMENT_EARNINGS,
    ):
        assert kind.non_negative is False, kind.identifier
        assert registry.kind(kind.identifier).non_negative is False, kind.identifier


def test_the_lines_after_a_floor_are_non_negative(registry: ArtifactRegistry) -> None:
    # Schedule 8 Part 4 line 3 "Line 1 plus line 2 (if negative, enter "0")", line 6 and line 7
    # "(if negative, enter "0")", line 9 "(if negative, enter "0")"; Schedule 13 line 1 "(if
    # negative, enter "0")" and line 7 "(if negative, enter "0")".
    for kind in (
        CPP_PENSIONABLE_EARNINGS,
        CPP_EARNINGS_SUBJECT_TO_SECOND_ADDITIONAL,
        CPP_EARNINGS_UP_TO_MAXIMUM,
        CPP_EARNINGS_SUBJECT_TO_BASE_AND_FIRST_ADDITIONAL,
        EI_SELF_EMPLOYMENT_EARNINGS,
        EI_INSURABLE_EARNINGS_REMAINING,
        CPT20_EARNINGS,
        SELF_EMPLOYED_CPP_DEDUCTION,
        CPP_PAYABLE_ON_SELF_EMPLOYMENT,
        EI_PAYABLE_ON_SELF_EMPLOYMENT,
    ):
        assert kind.non_negative is True, kind.identifier
        assert registry.kind(kind.identifier).non_negative is True, kind.identifier
