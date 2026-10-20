"""CA-ON 2025, end to end: CRA's worked example computed from the manifest through the service.

The service is the one the composition root builds (`build_tax_computation`): the real YAML sources
over the jurisdiction packages and the shared registries. Return A's amounts (employment income
110000 and a capital gain of 20000 to total income 120000, the other Step 2 lines being 0 (the
Federal Worksheet's line 9, the eight sources of line 12100 added, less line 10, the part reported
in previous years, as line 11 and so the interest and other investment income, line 12100; lines
14400, 14500 and 14600 added to line 14700; and every income line, in line order, summed to line
15000); the CPP contributions computed from
employment income by Schedule 8's tiers, each at its maximum: base 3356.10, first additional 678.00
and second additional 396.00, the enhanced contributions 1074.00; the EI premiums computed from
employment income, at the maximum 1077.48; the RRSP contributions available to deduct of 1926, no
unused contributions plus the contributions of 1926 (Schedule 7 line 10), the most that may be
deducted, 1926, the lesser of them and the deduction limit of 19800 (Schedule 7 line 17), the amount
deducted of 1926 (line 18), at most that, as the RRSP deduction (line 20), and the unused
contributions carried forward of 0 (line 23), the contributions available less the deduction; less
that RRSP deduction, union dues of 2000, the child care expenses deduction of 0 (T1 line 21400, Form
T778 line 7, the least of the basic limit of line 4, 0 x 8000 + 0 x 11000 + 0 x 5000
= 0, the 0 paid of line 5 and two-thirds of the earned income of line 6, the employment
income of 110000, 73333.33..., rounded half-up to the cent, 73333.33: 0) and the enhanced
contributions to net income 115000, less no deductions from net income to taxable income
115000, and from each basic personal
amount (16129 federal, the Federal Worksheet's taper on net income, here at or below
the 177882 threshold so not reduced; 12747 Ontario) plus each amount for an eligible
dependant (T1 line 30400, Schedule 5 line 5, the federal basic personal amount less the
dependant's net income of 0; ON428 line 58160, the 11905.00 base less it, at most 10823), claimed
for 0 eligible dependants and so 0, the base CPP contributions and the EI premiums, and federally
the amount for infirm children of 0 x 2687 (line 30500) and the Canada employment amount of 1471
(the lesser of employment income and 1471), through each total of credit amounts and the credit rate
applied once to it (T1 line 33800, ON428 line 58840) to each form's non-refundable tax credits
(ON428 line 61500, which adds to line 46 the donations and gifts credit of lines 47 to 49 (line
58969), 5.05% of Schedule 9 line 13 and 11.16% of its line 14; T1 line 35000, which adds the
donations and gifts credit of Schedule 9 (line 34900) and the top-up tax credit of the Federal
Worksheet (line 34990); all 0 for donations of 0)
to each tax after credits, the Ontario
surtax on the Ontario tax after credits (ON428 lines 66 to 68) to the Ontario tax with surtax of
line 69, less the Ontario dividend tax credit of 0 (line 70, from line 57 and Worksheet ON428's
line 61520: no dividends), not below zero, to the Ontario tax after the dividend credit (line 71,
which is line 73 as line 72 is not triggered), and with no dependent children and no dependants
the Ontario tax reduction amounts of 294.00 (lines 74 to 77), twice them less line 73, not below
zero, the Ontario tax reduction of 0 (line 80), to the Ontario tax after the reduction (line 81);
Schedule ON428-A's
LIFT credit, 5.05% of employment income, 5555, at most 875 (lines 5 and 14), less 5% of net income
over 32500, 4125 (line 19), not below zero, 0 (line 20, ON428 line 85), taken off the Ontario tax
after the reduction, not below zero (line 86), less the community food program donation tax credit
for farmers, 25% of the qualifying donations (line 87), here 0 for donations of 0, not below zero
(line 88); and the Ontario health premium on taxable income by the chart of line 89, 750, added to
it to the Ontario tax of line 90; and on the T1, the federal tax after credits carried to the net
federal tax (line 42000), added to the Ontario tax (line 42800) to the total payable (line 43500);
Schedule 6's Canada workers benefit, computed for each family status, from the working income of
110000 (line 5, employment income), 27% of it over 3000 at most 1633 (line 22), less 15% of the
adjusted family net income (line 15, net income) of 115000 over 26855, 13221.75 (line 27), not below
zero, 0 (line 28), and with an eligible dependant 27% of the working income at most 2813, less 15%
of the adjusted family net income over 30639, 12654.15, not below zero, 0, the count of 0 Schedule 6
eligible dependants (line 38100) choosing the first (T1 line 45300); less the total credits (line
48200), here the chosen income tax deducted of 25000 (line 43700) plus that benefit, to the refund
or balance owing (line 167), 897.15, positive so a balance owing; every line computed from a dataset
rounded half-up to the cent) are checked from the files under `returns/` by
`test_worked_returns.py`, as are Returns B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, T, V, W and
X; this module pins which capability produces each line, the order, and the trace that
explains them.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction as ExactFraction
from typing import Any

import pytest

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.application.services.tax_computation import TaxComputationService
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.at_most import AtMost
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.choose_by_count import ChooseByCount
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.multiple_over import MultipleOver
from app.domain.capabilities.per_unit_amount import PerUnitAmount
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.tapered_amount import TaperedAmount
from app.domain.capabilities.tiered_surcharge import TieredSurcharge
from app.domain.capabilities.times_count import TimesCount
from app.domain.errors import CapabilityContractError, InputAboveBoundError, NegativeArtifactError
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.parameters.amount import Amount
from app.domain.parameters.claim_reduction import ClaimReduction
from app.domain.parameters.contribution_tier import ContributionTier
from app.domain.parameters.credit import Credit
from app.domain.parameters.factor import Factor
from app.domain.parameters.fraction import Fraction
from app.domain.parameters.rate import Rate
from app.domain.parameters.rounding import RoundingMode, RoundTo
from app.domain.parameters.taper import Taper
from app.domain.record_list import RecordList
from app.domain.trace import (
    AtMostLine,
    BracketColumnLine,
    CappedAmountLine,
    CaregiverClaimLessClaimedLine,
    CaregiverClaimLine,
    ChosenByCountLine,
    ChosenByRangeLine,
    ContributionTierLine,
    CreditAmountLine,
    DisabilityTransferLine,
    FractionAppliedLine,
    ItemsTotalLine,
    LesserOfLine,
    MultipleOverLine,
    OtherDependantMedicalLine,
    PerUnitAmountLine,
    PlacementCreditLine,
    QuotientLine,
    RateAppliedLine,
    RecordCountLine,
    RecordTotalLine,
    RoundedTotalLine,
    SubtractedLine,
    SubtractedNotBelowZeroLine,
    SumLine,
    SurchargeTierLine,
    TaperedAmountLine,
    ThresholdGateLine,
    TimesCountLine,
)
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.capabilities.caregiver_amount import CaregiverAmount
from app.jurisdictions.ca.capabilities.disability_transfer_amount import DisabilityTransferAmount
from app.jurisdictions.ca.capabilities.other_dependants_medical import OtherDependantsMedical
from app.jurisdictions.ca.capabilities.threshold_gate import ThresholdGate
from app.jurisdictions.ca.catalog import (
    ADDITIONAL_DEDUCTIONS,
    ADJUSTED_FAMILY_NET_INCOME,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
    ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
    ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
    ADJUSTED_LOSSES_APPLIED_1985_TO_1987,
    ADJUSTED_LOSSES_APPLIED_1988_AND_1989,
    ADJUSTED_LOSSES_APPLIED_1990_TO_1999,
    ADJUSTED_LOSSES_APPLIED_2001_TO_2024,
    ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987,
    ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989,
    ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999,
    ADVANCED_CANADA_WORKERS_BENEFIT,
    AGE_AMOUNT,
    AGE_AMOUNT_BEFORE_COUNT,
    AGE_INCOME_OVER_THRESHOLD,
    AGE_INCOME_THRESHOLD,
    AGE_MAXIMUM,
    AGE_REDUCTION,
    AGED_18_OR_OLDER_AT_END_OF_2025,
    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    BASIC_PERSONAL_AMOUNT,
    BORN_IN_1960_OR_EARLIER,
    BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
    CANADA_EMPLOYMENT_AMOUNT,
    CANADA_WORKERS_BENEFIT,
    CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
    CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
    CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
    CAPITAL_GAIN,
    CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
    CAPITAL_GAINS_DEDUCTIONS_2000,
    CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
    CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
    CAPITAL_GIFT_GAINS_DEDUCTION,
    CAPITAL_GIFT_TAXABLE_GAINS,
    CAPITAL_GIFTS_LIMIT_ADDITION,
    CAPITAL_GIFTS_TOTAL,
    CAPITAL_PROPERTY_GIFTS,
    CAREGIVER_AMOUNT,
    CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
    CHARITABLE_DONATIONS,
    CHARITABLE_DONATIONS_CLAIMED,
    CHARITABLE_DONATIONS_LIMIT,
    CHILD_CARE_BASIC_LIMIT,
    CHILD_CARE_EARNED_INCOME,
    CHILD_CARE_EARNED_INCOME_LIMIT,
    CHILD_CARE_EXPENSES,
    CHILD_CARE_EXPENSES_PAID,
    CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
    CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
    CHILDREN_SEVEN_TO_SIXTEEN,
    CHILDREN_UNDER_SEVEN,
    CHILDREN_WITH_DISABILITY,
    CLERGY_RESIDENCE_DEDUCTION,
    CPP_BASE_CONTRIBUTIONS,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_OR_QPP_BENEFITS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CREDIT_AMOUNTS_AT_CREDIT_RATE,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    CREDITS_AGAINST_FEDERAL_TAX,
    CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
    CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
    CWB_ELIGIBLE_DEPENDANTS,
    CWB_REDUCTION_WITH_DEPENDANT,
    CWB_REDUCTION_WITHOUT_DEPENDANT,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    DEPENDANT_CARE_EXPENSES,
    DEPENDANT_CREDIT_AMOUNTS,
    DEPENDANT_NET_INCOME,
    DEPENDANT_TAXABLE_INCOME,
    DEPENDANT_UNDER_18,
    DEPRECIABLE_GIFT_CAPITAL_COST,
    DEPRECIABLE_GIFT_NET_PROCEEDS,
    DEPRECIABLE_GIFT_PROCEEDS_OR_COST,
    DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION,
    DEPRECIABLE_GIFTS,
    DISABILITY_DEPENDANTS,
    DISABILITY_SUPPORTS_DEDUCTION,
    DISABILITY_TRANSFERRED_AMOUNT,
    DIVIDEND_TAX_CREDIT,
    DIVIDENDS_AMOUNT_A,
    DIVIDENDS_AMOUNT_A_LESS_B,
    DIVIDENDS_AMOUNT_B,
    DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
    DONATION_FIRST_TIER_MAXIMUM,
    DONATION_HIGH_INCOME_THRESHOLD,
    DONATION_LIMIT_ON_NET_INCOME,
    DONATION_LIMIT_WITH_CAPITAL_GIFTS,
    DONATIONS_AND_GIFTS_CREDIT,
    DONATIONS_AND_GIFTS_TOTAL,
    DONATIONS_FIRST_TIER,
    DONATIONS_OVER_FIRST_TIER,
    DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS,
    ECOLOGICAL_AND_CULTURAL_GIFTS,
    ECOLOGICAL_GIFTS_BEFORE_2016,
    EDUCATOR_SCHOOL_SUPPLY_CREDIT,
    EDUCATOR_SUPPLIES_EXPENSES,
    EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
    EI_AND_OTHER_BENEFITS,
    EI_PREMIUMS,
    ELECTED_SPLIT_PENSION_AMOUNT,
    ELECTED_SPLIT_PENSION_DEDUCTION,
    ELIGIBLE_DEPENDANT_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
    ELIGIBLE_DEPENDANTS,
    ELIGIBLE_DIVIDENDS_CREDIT,
    ELIGIBLE_DIVIDENDS_GROSSED_UP,
    ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
    EMPLOYMENT_INCOME,
    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    FEDERAL_TAX_LESS_CREDITS,
    FEDERAL_TAX_WITH_ITC_RECAPTURE,
    FHSA_ANNUAL_AMOUNT,
    FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS,
    FHSA_ANNUAL_AMOUNT_FOR_2024,
    FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD,
    FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD,
    FHSA_ANNUAL_LIMIT,
    FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD,
    FHSA_ANNUAL_LIMIT_FROM_STEP_2,
    FHSA_ANNUAL_LIMITS_FOR_2024_AND_PRIOR_YEARS,
    FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS,
    FHSA_CARRYFORWARD_FOR_2024,
    FHSA_CARRYFORWARD_FOR_2025,
    FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_AVAILABLE,
    FHSA_CONTRIBUTIONS_DEDUCTED,
    FHSA_CONTRIBUTIONS_IN_2024,
    FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2024_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2025,
    FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
    FHSA_CONTRIBUTIONS_LIMIT,
    FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT,
    FHSA_DEDUCTION,
    FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS,
    FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
    FHSA_DESIGNATED_TRANSFERS_IN_2025,
    FHSA_DESIGNATED_WITHDRAWALS_IN_2025,
    FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
    FHSA_INCOME,
    FHSA_LIFETIME_LIMIT,
    FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS,
    FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS,
    FHSA_MAXIMUM_DEDUCTION,
    FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED,
    FHSA_NET_RRSP_TRANSFER_AMOUNT,
    FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS,
    FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS,
    FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT,
    FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
    FHSA_RRSP_TRANSFERS_IN_2025,
    FHSA_TOTAL_ANNUAL_LIMITS,
    FHSA_TOTAL_DESIGNATED_TRANSFERS,
    FHSA_TOTAL_RRSP_TRANSFERS,
    FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT,
    FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT,
    FHSA_UNUSED_CONTRIBUTIONS_BROUGHT_FORWARD,
    FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD,
    FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS,
    FHSA_VARIABLE_B_AMOUNT,
    FHSA_VARIABLE_F_AMOUNT,
    FHSA_VARIABLE_H_AMOUNT,
    FIRST_TIER_DONATION_CREDIT,
    FOREIGN_CHARITY_DONATIONS,
    FOREIGN_INVESTMENT_INCOME,
    GOVERNMENT_DONATIONS,
    HIGH_INCOME_DONATION_CREDIT,
    HIGH_INCOME_DONATIONS,
    INCOME_SUPPORT_BENEFITS,
    INCOME_TAX_DEDUCTED,
    INFIRM_CHILDREN,
    INFIRM_CHILDREN_AMOUNT,
    INFIRM_DEPENDANTS,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
    INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
    INVESTMENT_INCOME_WITHOUT_A_SLIP,
    INVESTMENT_ROYALTIES,
    ITC_RECAPTURE,
    ITC_RECAPTURE_AT_15_PERCENT,
    ITC_RECAPTURE_AT_20_PERCENT,
    ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT,
    ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT,
    JOURNALISM_LABOUR_TAX_CREDIT,
    LABOUR_SPONSORED_FUNDS_CREDIT,
    LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
    LABOUR_SPONSORED_FUNDS_NET_COST,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
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
    NET_CAPITAL_LOSS_BALANCE_1985_TO_1987,
    NET_CAPITAL_LOSS_BALANCE_1988_AND_1989,
    NET_CAPITAL_LOSS_BALANCE_1990_TO_1999,
    NET_CAPITAL_LOSS_BALANCE_2001_TO_2024,
    NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
    NET_CAPITAL_LOSSES_CLAIMED,
    NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NET_COMMISSION_INCOME,
    NET_FARMING_INCOME,
    NET_FEDERAL_SUPPLEMENTS,
    NET_FEDERAL_TAX,
    NET_FISHING_INCOME,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
    NET_PARTNERSHIP_INCOME,
    NET_PROFESSIONAL_INCOME,
    NO_SLIP_DIVIDEND_TAX_CREDIT,
    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    OLD_AGE_SECURITY,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
    OTHER_DEDUCTIONS,
    OTHER_DEPENDANT_MEDICAL_EXPENSES,
    OTHER_DEPENDANTS,
    OTHER_DEPENDANTS_MEDICAL,
    OTHER_DIVIDENDS_CREDIT,
    OTHER_DIVIDENDS_GROSSED_UP,
    OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    OTHER_EMPLOYMENT_EXPENSES,
    OTHER_EMPLOYMENT_INCOME,
    OTHER_FHSA_INCOME,
    OTHER_INCOME,
    OTHER_PAYMENTS_DEDUCTION,
    OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT,
    OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
    OTHER_PAYMENTS_LIMIT_INCOME,
    OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
    OTHER_PAYMENTS_WORKSHEET_REQUIRED,
    OTHER_PENSIONS_AND_SUPERANNUATION,
    PART_XII_2_TAX_CREDIT,
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
    PROVINCIAL_CREDITS,
    RDSP_INCOME,
    RDSP_INCOME_REPAYMENT,
    REFUND,
    REFUND_OR_BALANCE_OWING,
    REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT,
    REGULAR_RATE_DONATION_CREDIT,
    REGULAR_RATE_DONATIONS,
    REMAINING_ADJUSTED_LOSSES_1985_TO_1987,
    REMAINING_ADJUSTED_LOSSES_1988_AND_1989,
    REMAINING_ADJUSTED_LOSSES_1990_TO_1999,
    REMAINING_ADJUSTED_LOSSES_2001_TO_2024,
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
    RPP_DEDUCTION,
    RRSP_AMOUNT_DEDUCTED,
    RRSP_CONTRIBUTIONS,
    RRSP_CONTRIBUTIONS_AVAILABLE,
    RRSP_DEDUCTION,
    RRSP_DEDUCTION_LIMIT,
    RRSP_DEDUCTION_MAXIMUM,
    RRSP_INCOME,
    SECURITY_OPTIONS_DEDUCTIONS,
    SLIP_DIVIDEND_TAX_CREDIT,
    SLIP_TAXABLE_DIVIDENDS,
    SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SOCIAL_ASSISTANCE_PAYMENTS,
    SPECIAL_TAXES,
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
    SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS,
    SPOUSE_RDSP_INCOME,
    SPOUSE_RDSP_INCOME_REPAYMENT,
    SPOUSE_UCCB_REPAYMENT,
    SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT,
    SPOUSES_CLAIMED,
    SUPPORT_PAYMENTS_DEDUCTION,
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
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_DIVIDENDS,
    TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TAXABLE_INCOME,
    TAXABLE_INCOME_OVER_DONATION_THRESHOLD,
    TAXABLE_SCHOLARSHIPS,
    TAXABLE_SUPPORT_PAYMENTS,
    TOP_UP_CREDITS_BASE,
    TOP_UP_EXCESS,
    TOP_UP_TAX_CREDIT,
    TOP_UP_THRESHOLD,
    TOTAL_ADJUSTED_NET_CAPITAL_LOSSES,
    TOTAL_CARRYING_CHARGES,
    TOTAL_CHARITABLE_DONATIONS,
    TOTAL_CREDITS,
    TOTAL_INCOME,
    TOTAL_INTEREST_EXPENSES,
    TOTAL_OTHER_EXPENSES,
    TOTAL_PAYABLE,
    UCCB_AND_RDSP_INCOME,
    UCCB_AND_RDSP_INCOME_REPAYMENTS,
    UCCB_REPAYMENT,
    UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
    UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
    UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
    UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
    UNION_DUES,
    UNIVERSAL_CHILD_CARE_BENEFIT,
    UNIVERSITY_DONATIONS_OUTSIDE_CANADA,
    UNUSED_RRSP_CONTRIBUTIONS,
    UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
    WAGE_LOSS_REPLACEMENT_PLAN_INCOME,
    WORKERS_COMPENSATION_BENEFITS,
    WORKING_INCOME,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.capabilities.caregiver_amount import OntarioCaregiverAmount
from app.jurisdictions.ca_on.capabilities.choose_by_range import ChooseByRange
from app.jurisdictions.ca_on.capabilities.coop_education_credit import CoopEducationCredit
from app.jurisdictions.ca_on.capabilities.flow_through_share_expenses import (
    FlowThroughShareExpenses,
)
from app.jurisdictions.ca_on.capabilities.quotient import Quotient
from app.jurisdictions.ca_on.capabilities.record_count import RecordCount
from app.jurisdictions.ca_on.catalog import (
    CLAIMS_SENIORS_CARE_CREDIT,
    COMMUNITY_FOOD_PROGRAM_CREDIT,
    COMMUNITY_FOOD_PROGRAM_DONATIONS,
    COOP_EDUCATION_CREDIT,
    COOP_EDUCATION_FULL_SHARE,
    COOP_EDUCATION_PAYROLL,
    COOP_EDUCATION_PAYROLL_OVER_THRESHOLD,
    COOP_EDUCATION_PAYROLL_RANGE,
    COOP_EDUCATION_PAYROLL_THRESHOLD,
    COOP_EDUCATION_PHASE_OUT_SHARE,
    COOP_EDUCATION_PLACEMENT_COUNT,
    COOP_EDUCATION_PLACEMENT_EXPENDITURES,
    COOP_EDUCATION_PLACEMENTS,
    COOP_EDUCATION_REMAINING_SHARE,
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
    ELIGIBLE_DEPENDANT_BASE,
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
    ONTARIO_BASIC_TAX,
    ONTARIO_CREDITS,
    ONTARIO_CREDITS_SUBTOTAL,
    ONTARIO_HEALTH_PREMIUM,
    ONTARIO_SURTAX,
    ONTARIO_TAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_AFTER_FOOD_CREDIT,
    ONTARIO_TAX_AFTER_LIFT_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
    ONTARIO_TAX_REDUCTION,
    ONTARIO_TAX_WITH_SURTAX,
    SENIORS_CARE_AMOUNT,
    SENIORS_CARE_BASE_AMOUNT,
    SENIORS_CARE_BEFORE_CLAIM,
    SENIORS_CARE_BEFORE_MAXIMUM,
    SENIORS_CARE_CREDIT,
    SENIORS_CARE_FAMILY_NET_INCOME,
    SENIORS_CARE_INCOME_OVER_BASE,
    SENIORS_CARE_REDUCTION,
    SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
    SENIORS_TRANSIT_CREDIT,
    SENIORS_TRANSIT_PAID,
    TAX_REDUCTION_AMOUNTS,
    TAX_REDUCTION_BASIC,
    TAX_REDUCTION_FOR_CHILDREN,
    TAX_REDUCTION_FOR_DEPENDANTS,
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


def compute(
    employment_income: str,
    capital_gain: str,
    unused_rrsp_contributions: str,
    rrsp_contributions: str,
    rrsp_deduction_limit: str,
    rrsp_amount_deducted: str,
    union_dues: str,
    *,
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
    seniors_transit_paid: str = "0",
    flow_through_share_slips: tuple[str, ...] = (),
    coop_education_payroll: str = "0",
    coop_education_placements: tuple[str, ...] = (),
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
    unapplied_net_capital_losses_1985_to_1987: str = "0",
    unapplied_net_capital_losses_1988_and_1989: str = "0",
    unapplied_net_capital_losses_1990_to_1999: str = "0",
    unapplied_net_capital_losses_2001_to_2024: str = "0",
    net_capital_losses_claimed: str = "0",
) -> Worksheet:
    return service().compute(
        CA_ON,
        2025,
        Artifact(EMPLOYMENT_INCOME, D(employment_income)),
        Artifact(CAPITAL_GAIN, D(capital_gain)),
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
        Artifact(SENIORS_TRANSIT_PAID, D(seniors_transit_paid)),
        slips(*flow_through_share_slips),
        Artifact(COOP_EDUCATION_PAYROLL, D(coop_education_payroll)),
        placement_list(*coop_education_placements),
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
    )


def return_a() -> Worksheet:
    """Return A's inputs, as in `returns/2025_return_a.yaml`, with its chosen tax deducted."""
    return compute(
        "110000", "20000", "0", "1926", "19800", "1926", "2000", income_tax_deducted="25000"
    )


def test_each_amount_is_produced_by_its_capability() -> None:
    worksheet = return_a()

    assert worksheet.producer_of(EMPLOYMENT_INCOME) is None
    assert worksheet.producer_of(CAPITAL_GAIN) is None
    assert worksheet.producer_of(UNUSED_RRSP_CONTRIBUTIONS) is None
    assert worksheet.producer_of(RRSP_CONTRIBUTIONS) is None
    assert worksheet.producer_of(RRSP_DEDUCTION_LIMIT) is None
    assert worksheet.producer_of(RRSP_AMOUNT_DEDUCTED) is None
    assert worksheet.producer_of(UNION_DUES) is None
    assert worksheet.producer_of(DEPENDENT_CHILDREN) is None
    assert worksheet.producer_of(DEPENDANTS) is None
    assert worksheet.producer_of(ELIGIBLE_DEPENDANTS) is None
    assert worksheet.producer_of(DEPENDANT_NET_INCOME) is None
    assert worksheet.producer_of(INFIRM_DEPENDANTS) is None
    assert worksheet.producer_of(MEDICAL_EXPENSES) is None
    assert worksheet.producer_of(OTHER_DEPENDANTS) is None
    assert worksheet.producer_of(ontario.CAREGIVER_DEPENDANTS) is None
    assert worksheet.producer_of(DISABILITY_DEPENDANTS) is None
    assert worksheet.producer_of(INFIRM_CHILDREN) is None
    assert worksheet.producer_of(BORN_IN_1960_OR_EARLIER) is None
    assert worksheet.producer_of(SPOUSE_NET_INCOME) is None
    assert worksheet.producer_of(SPOUSES_CLAIMED) is None
    assert worksheet.producer_of(SPOUSE_CAREGIVER_ELIGIBLE) is None
    assert worksheet.producer_of(CHILD_CARE_EXPENSES_PAID) is None
    assert worksheet.producer_of(CHILDREN_UNDER_SEVEN) is None
    assert worksheet.producer_of(CHILDREN_WITH_DISABILITY) is None
    assert worksheet.producer_of(CHILDREN_SEVEN_TO_SIXTEEN) is None
    assert worksheet.producer_of(CWB_ELIGIBLE_DEPENDANTS) is None
    assert worksheet.producer_of(INCOME_TAX_DEDUCTED) is None
    assert worksheet.producer_of(FERTILITY_EXPENSES) is None
    assert worksheet.producer_of(SENIORS_TRANSIT_PAID) is None
    assert worksheet.producer_of(FLOW_THROUGH_SHARE_SLIPS) is None
    assert worksheet.producer_of(COOP_EDUCATION_PAYROLL) is None
    assert worksheet.producer_of(COOP_EDUCATION_PLACEMENTS) is None
    assert worksheet.producer_of(COMMUNITY_FOOD_PROGRAM_DONATIONS) is None
    assert worksheet.producer_of(CHARITABLE_DONATIONS) is None
    assert worksheet.producer_of(GOVERNMENT_DONATIONS) is None
    assert worksheet.producer_of(UNIVERSITY_DONATIONS_OUTSIDE_CANADA) is None
    assert worksheet.producer_of(FOREIGN_CHARITY_DONATIONS) is None
    assert worksheet.producer_of(ECOLOGICAL_AND_CULTURAL_GIFTS) is None
    assert worksheet.producer_of(ECOLOGICAL_GIFTS_BEFORE_2016) is None
    assert worksheet.producer_of(DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION) is None
    assert worksheet.producer_of(DEPRECIABLE_GIFT_NET_PROCEEDS) is None
    assert worksheet.producer_of(DEPRECIABLE_GIFT_CAPITAL_COST) is None
    assert worksheet.producer_of(CAPITAL_GIFT_TAXABLE_GAINS) is None
    assert worksheet.producer_of(CAPITAL_GIFT_GAINS_DEDUCTION) is None
    assert worksheet.producer_of(ontario.POLITICAL_CONTRIBUTIONS) is None
    assert worksheet.producer_of(POLITICAL_CONTRIBUTIONS) is None
    assert worksheet.producer_of(DISABILITY_SUPPORTS_DEDUCTION) is None
    assert worksheet.producer_of(OTHER_EMPLOYMENT_EXPENSES) is None
    assert worksheet.producer_of(CLERGY_RESIDENCE_DEDUCTION) is None
    assert worksheet.producer_of(NET_BUSINESS_INCOME) is None
    assert worksheet.producer_of(NET_PROFESSIONAL_INCOME) is None
    assert worksheet.producer_of(NET_COMMISSION_INCOME) is None
    assert worksheet.producer_of(NET_FARMING_INCOME) is None
    assert worksheet.producer_of(NET_FISHING_INCOME) is None
    assert worksheet.producer_of(WAGE_LOSS_REPLACEMENT_PLAN_INCOME) is None
    assert worksheet.producer_of(RESIDENT_IN_CANADA_THROUGHOUT_2025) is None
    assert worksheet.producer_of(AGED_18_OR_OLDER_AT_END_OF_2025) is None
    assert worksheet.producer_of(SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS) is None
    assert worksheet.producer_of(SPOUSE_UCCB_REPAYMENT) is None
    assert worksheet.producer_of(SPOUSE_RDSP_INCOME_REPAYMENT) is None
    assert worksheet.producer_of(SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT) is None
    assert worksheet.producer_of(SPOUSE_RDSP_INCOME) is None
    assert worksheet.producer_of(OTHER_EMPLOYMENT_INCOME) is None
    assert worksheet.producer_of(OLD_AGE_SECURITY) is None
    assert worksheet.producer_of(CPP_OR_QPP_BENEFITS) is None
    assert worksheet.producer_of(OTHER_PENSIONS_AND_SUPERANNUATION) is None
    assert worksheet.producer_of(ELECTED_SPLIT_PENSION_AMOUNT) is None
    assert worksheet.producer_of(UNIVERSAL_CHILD_CARE_BENEFIT) is None
    assert worksheet.producer_of(EI_AND_OTHER_BENEFITS) is None
    assert worksheet.producer_of(T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE) is None
    assert worksheet.producer_of(T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE) is None
    assert worksheet.producer_of(T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE) is None
    assert worksheet.producer_of(T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE) is None
    assert worksheet.producer_of(T3_TAXABLE_DIVIDENDS) is None
    assert worksheet.producer_of(T4PS_TAXABLE_DIVIDENDS) is None
    assert worksheet.producer_of(T5_TAXABLE_DIVIDENDS) is None
    assert worksheet.producer_of(T5013_TAXABLE_DIVIDENDS) is None
    assert worksheet.producer_of(ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP) is None
    assert worksheet.producer_of(OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP) is None
    assert worksheet.producer_of(T3_DIVIDEND_TAX_CREDIT) is None
    assert worksheet.producer_of(T4PS_DIVIDEND_TAX_CREDIT) is None
    assert worksheet.producer_of(T5_DIVIDEND_TAX_CREDIT) is None
    assert worksheet.producer_of(T5013_DIVIDEND_TAX_CREDIT) is None
    assert worksheet.producer_of(T3_INVESTMENT_INCOME) is None
    assert worksheet.producer_of(T5_INVESTMENT_INCOME) is None
    assert worksheet.producer_of(T5013_INVESTMENT_INCOME) is None
    assert worksheet.producer_of(INVESTMENT_INCOME_CREDITED_NOT_RECEIVED) is None
    assert worksheet.producer_of(TAX_REFUND_INTEREST) is None
    assert worksheet.producer_of(FOREIGN_INVESTMENT_INCOME) is None
    assert worksheet.producer_of(INVESTMENT_INCOME_WITHOUT_A_SLIP) is None
    assert worksheet.producer_of(INVESTMENT_ROYALTIES) is None
    assert worksheet.producer_of(INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS) is None
    assert worksheet.producer_of(NET_PARTNERSHIP_INCOME) is None
    assert worksheet.producer_of(RDSP_INCOME) is None
    assert worksheet.producer_of(TAXABLE_SUPPORT_PAYMENTS) is None
    assert worksheet.producer_of(RRSP_INCOME) is None
    assert worksheet.producer_of(FHSA_INCOME) is None
    assert worksheet.producer_of(OTHER_FHSA_INCOME) is None
    assert worksheet.producer_of(OTHER_INCOME) is None
    assert worksheet.producer_of(TAXABLE_SCHOLARSHIPS) is None
    assert worksheet.producer_of(WORKERS_COMPENSATION_BENEFITS) is None
    assert worksheet.producer_of(SOCIAL_ASSISTANCE_PAYMENTS) is None
    assert worksheet.producer_of(NET_FEDERAL_SUPPLEMENTS) is None
    for starting_kind in (
        UCCB_REPAYMENT,
        RDSP_INCOME_REPAYMENT,
        CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
        SECURITY_OPTIONS_DEDUCTIONS,
        LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
        NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
        UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
        UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
        UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
        UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
        NET_CAPITAL_LOSSES_CLAIMED,
        ADDITIONAL_DEDUCTIONS,
        OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT,
        OTHER_PAYMENTS_WORKSHEET_REQUIRED,
        OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
    ):
        assert worksheet.producer_of(starting_kind) is None, starting_kind.identifier
    # The Federal Worksheet's "Line 25000 - Other payments deduction": lines 4, 8 and 9 add, line
    # 5 subtracts, and line 25000 is chosen twice by a count.
    assert isinstance(worksheet.producer_of(UCCB_AND_RDSP_INCOME), Sum)
    assert isinstance(worksheet.producer_of(NET_INCOME_LESS_UCCB_AND_RDSP_INCOME), Subtract)
    assert isinstance(worksheet.producer_of(UCCB_AND_RDSP_INCOME_REPAYMENTS), Sum)
    assert isinstance(worksheet.producer_of(OTHER_PAYMENTS_LIMIT_INCOME), Sum)
    assert isinstance(worksheet.producer_of(OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT), ChooseByCount)
    assert isinstance(worksheet.producer_of(OTHER_PAYMENTS_DEDUCTION), ChooseByCount)
    assert worksheet.producer_of(OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT) is not (
        worksheet.producer_of(OTHER_PAYMENTS_DEDUCTION)
    )
    assert worksheet.producer_of(OTHER_PAYMENTS_DEDUCTION) is not (
        worksheet.producer_of(CANADA_WORKERS_BENEFIT)
    )
    # T1 Step 2: the Federal Worksheet's line 9 and line 11 (line 12100), and line 14700.
    assert isinstance(worksheet.producer_of(INVESTMENT_INCOME_BEFORE_PRIOR_YEARS), Sum)
    assert isinstance(worksheet.producer_of(INTEREST_AND_OTHER_INVESTMENT_INCOME), Subtract)
    assert isinstance(worksheet.producer_of(INCOME_SUPPORT_BENEFITS), Sum)
    # The Federal Worksheet's dividend lines 5, 10, 13, 16, 17 (lines 12000 and 12010), and the
    # federal dividend tax credit's lines 5, A, B, 6, C, 7, 8 and 9 (line 40425).
    for kind in (
        SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
        SLIP_TAXABLE_DIVIDENDS,
        DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
        TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
        TAXABLE_DIVIDENDS,
        SLIP_DIVIDEND_TAX_CREDIT,
        DIVIDENDS_AMOUNT_A,
        DIVIDENDS_AMOUNT_B,
        NO_SLIP_DIVIDEND_TAX_CREDIT,
        DIVIDEND_TAX_CREDIT,
        CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    ):
        assert isinstance(worksheet.producer_of(kind), Sum), kind
    assert isinstance(worksheet.producer_of(ELIGIBLE_DIVIDENDS_GROSSED_UP), ApplyFraction)
    assert isinstance(worksheet.producer_of(OTHER_DIVIDENDS_GROSSED_UP), ApplyFraction)
    assert isinstance(worksheet.producer_of(OTHER_DIVIDENDS_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(ELIGIBLE_DIVIDENDS_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(DIVIDENDS_AMOUNT_A_LESS_B), Subtract)
    assert worksheet.producer_of(ELIGIBLE_DIVIDENDS_GROSSED_UP) is not (
        worksheet.producer_of(OTHER_DIVIDENDS_GROSSED_UP)
    )
    assert worksheet.producer_of(OTHER_DIVIDENDS_CREDIT) is not (
        worksheet.producer_of(ELIGIBLE_DIVIDENDS_CREDIT)
    )
    assert worksheet.producer_of(INTEREST_AND_OTHER_INVESTMENT_INCOME) is not (
        worksheet.producer_of(REFUND_OR_BALANCE_OWING)
    )
    assert worksheet.producer_of(INVESTMENT_INCOME_BEFORE_PRIOR_YEARS) is not (
        worksheet.producer_of(INCOME_SUPPORT_BENEFITS)
    )
    assert isinstance(worksheet.producer_of(RRSP_CONTRIBUTIONS_AVAILABLE), Sum)
    assert isinstance(worksheet.producer_of(RRSP_DEDUCTION_MAXIMUM), LesserOf)
    # Schedule 7 line 18 "cannot be more than the amount on line 17": checked, not capped.
    assert isinstance(worksheet.producer_of(RRSP_DEDUCTION), AtMost)
    assert isinstance(worksheet.producer_of(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD), Subtract)
    assert worksheet.producer_of(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD) is not (
        worksheet.producer_of(REFUND_OR_BALANCE_OWING)
    )
    assert isinstance(worksheet.producer_of(CPP_BASE_CONTRIBUTIONS), TieredContribution)
    assert isinstance(worksheet.producer_of(CPP_FIRST_ADDITIONAL_CONTRIBUTIONS), TieredContribution)
    assert isinstance(
        worksheet.producer_of(CPP_SECOND_ADDITIONAL_CONTRIBUTIONS), TieredContribution
    )
    tiers = {
        worksheet.producer_of(kind)
        for kind in (
            CPP_BASE_CONTRIBUTIONS,
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
        )
    }
    assert len(tiers) == 3
    assert isinstance(worksheet.producer_of(EI_PREMIUMS), TieredContribution)
    assert worksheet.producer_of(EI_PREMIUMS) not in tiers
    assert isinstance(worksheet.producer_of(CPP_ENHANCED_CONTRIBUTIONS), Sum)
    assert isinstance(worksheet.producer_of(TAXABLE_CAPITAL_GAINS), ApplyRate)
    assert isinstance(worksheet.producer_of(TOTAL_INCOME), Sum)
    # Form T778 Part B lines 1 to 3, line 4, line 6 and line 7 (T1 line 21400).
    child_care_limits = {
        worksheet.producer_of(kind)
        for kind in (
            CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
            CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
            CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
        )
    }
    assert len(child_care_limits) == 3
    assert all(isinstance(producer, PerUnitAmount) for producer in child_care_limits)
    assert isinstance(worksheet.producer_of(CHILD_CARE_BASIC_LIMIT), Sum)
    assert isinstance(worksheet.producer_of(CHILD_CARE_EARNED_INCOME), Sum)
    assert worksheet.producer_of(CHILD_CARE_EARNED_INCOME) is not worksheet.producer_of(
        WORKING_INCOME
    )
    assert isinstance(worksheet.producer_of(CHILD_CARE_EARNED_INCOME_LIMIT), ApplyFraction)
    assert isinstance(worksheet.producer_of(CHILD_CARE_EXPENSES), LesserOf)
    assert worksheet.producer_of(CHILD_CARE_EXPENSES) is not worksheet.producer_of(
        RRSP_DEDUCTION_MAXIMUM
    )
    assert isinstance(worksheet.producer_of(DEDUCTIONS_FROM_TOTAL_INCOME), Sum)
    assert isinstance(worksheet.producer_of(NET_INCOME), SubtractNotBelowZero)
    # T1 Step 3's new deduction lines, all starting amounts but the ones computed below: the
    # Federal Worksheet's line 22100, Form T1436's line 21700 and Schedule 15's line 20805.
    for starting_kind in (
        RPP_DEDUCTION,
        ELECTED_SPLIT_PENSION_DEDUCTION,
        SUPPORT_PAYMENTS_DEDUCTION,
        EXPLORATION_AND_DEVELOPMENT_EXPENSES,
        OTHER_DEDUCTIONS,
        TOTAL_CARRYING_CHARGES,
        TOTAL_INTEREST_EXPENSES,
        TOTAL_OTHER_EXPENSES,
        CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
        CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
        CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
        CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
        CAPITAL_GAINS_DEDUCTIONS_2000,
        CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
        BUSINESS_INVESTMENT_LOSS,
        FHSA_CONTRIBUTIONS_IN_2025,
        FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_VARIABLE_B_AMOUNT,
        FHSA_DESIGNATED_WITHDRAWALS_IN_2025,
        FHSA_CONTRIBUTIONS_IN_2024,
        FHSA_CONTRIBUTIONS_IN_2024_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_CARRYFORWARD_FOR_2025,
        FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
        FHSA_RRSP_TRANSFERS_IN_2025,
        FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
        FHSA_DESIGNATED_TRANSFERS_IN_2025,
        FHSA_VARIABLE_H_AMOUNT,
        FHSA_CARRYFORWARD_FOR_2024,
        FHSA_VARIABLE_F_AMOUNT,
        FHSA_ANNUAL_LIMITS_FOR_2024_AND_PRIOR_YEARS,
        FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS,
        FHSA_UNUSED_CONTRIBUTIONS_BROUGHT_FORWARD,
        FHSA_CONTRIBUTIONS_DEDUCTED,
        FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED,
    ):
        assert worksheet.producer_of(starting_kind) is None, starting_kind.identifier
    for kind in (
        CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
        CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
        FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT,
        FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD,
        FHSA_TOTAL_RRSP_TRANSFERS,
        FHSA_TOTAL_DESIGNATED_TRANSFERS,
        FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD,
        FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT,
        FHSA_TOTAL_ANNUAL_LIMITS,
        FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS,
    ):
        assert isinstance(worksheet.producer_of(kind), Sum), kind.identifier
    for kind in (
        BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
        BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
        FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
        FHSA_NET_RRSP_TRANSFER_AMOUNT,
        FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS,
        FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS,
        FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS,
        FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS,
        FHSA_CONTRIBUTIONS_AVAILABLE,
        FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD,
        NET_INCOME_BEFORE_ADJUSTMENTS,
    ):
        assert isinstance(worksheet.producer_of(kind), Subtract), kind.identifier
    for kind in (
        FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
        FHSA_CONTRIBUTIONS_LIMIT,
        FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT,
        FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS,
        FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS,
    ):
        assert isinstance(worksheet.producer_of(kind), SubtractNotBelowZero), kind.identifier
    for kind in (
        BUSINESS_INVESTMENT_LOSS_REDUCTION,
        FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT,
        FHSA_ANNUAL_LIMIT_FROM_STEP_2,
        FHSA_MAXIMUM_DEDUCTION,
    ):
        assert isinstance(worksheet.producer_of(kind), LesserOf), kind.identifier
    for kind in (ALLOWABLE_BUSINESS_INVESTMENT_LOSS,):
        assert isinstance(worksheet.producer_of(kind), ApplyRate), kind.identifier
    for kind in (
        FHSA_ANNUAL_AMOUNT,
        FHSA_ANNUAL_AMOUNT_FOR_2024,
        FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD,
        FHSA_LIFETIME_LIMIT,
    ):
        assert isinstance(worksheet.producer_of(kind), CreditAmount), kind.identifier
    for kind in (FHSA_ANNUAL_LIMIT,):
        assert isinstance(worksheet.producer_of(kind), ChooseByCount), kind.identifier
    for kind in (FHSA_DEDUCTION,):
        assert isinstance(worksheet.producer_of(kind), AtMost), kind.identifier
    # Lines 14 and 30 of Schedule 15 print the same 8,000.00: one dataset read by two steps, each
    # producing its own artifact.
    assert worksheet.producer_of(FHSA_ANNUAL_AMOUNT) is not (
        worksheet.producer_of(FHSA_ANNUAL_AMOUNT_FOR_2024)
    )
    # Line 40 is chosen by the count between Step 2's result and the printed "0".
    assert worksheet.producer_of(FHSA_ANNUAL_LIMIT) is not (
        worksheet.producer_of(FHSA_ANNUAL_LIMIT_FROM_STEP_2)
    )
    # T1 line 23400 is its own step, apart from the floored net income of line 23600.
    assert worksheet.producer_of(NET_INCOME_BEFORE_ADJUSTMENTS) is not (
        worksheet.producer_of(NET_INCOME)
    )
    assert worksheet.producer_of(TOTAL_INCOME) is not worksheet.producer_of(
        DEDUCTIONS_FROM_TOTAL_INCOME
    )
    assert isinstance(worksheet.producer_of(DEDUCTIONS_FROM_NET_INCOME), Sum)
    # Form T1436 Chart A, one step per cell of each printed row: column C (column A multiplied by
    # column B) and column G (column E multiplied by column F) by a fraction, column D the lesser of
    # column C and what is left of line 13, what is left the line 13 amount less the older rows'
    # column D, column E column C less column D; then lines 4, 6 and 7 (also T1 line 25300).
    assert isinstance(
        worksheet.producer_of(ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987), ApplyFraction
    )
    assert isinstance(
        worksheet.producer_of(ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989), ApplyFraction
    )
    assert isinstance(
        worksheet.producer_of(ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999), ApplyFraction
    )
    assert isinstance(
        worksheet.producer_of(ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024), ApplyFraction
    )
    assert isinstance(worksheet.producer_of(TOTAL_ADJUSTED_NET_CAPITAL_LOSSES), Sum)
    assert isinstance(worksheet.producer_of(NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM), LesserOf)
    assert isinstance(worksheet.producer_of(NET_CAPITAL_LOSSES_OF_OTHER_YEARS), AtMost)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_APPLIED_1985_TO_1987), LesserOf)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987), Subtract)
    assert isinstance(worksheet.producer_of(REMAINING_ADJUSTED_LOSSES_1985_TO_1987), Subtract)
    assert isinstance(worksheet.producer_of(NET_CAPITAL_LOSS_BALANCE_1985_TO_1987), ApplyFraction)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_APPLIED_1988_AND_1989), LesserOf)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989), Subtract)
    assert isinstance(worksheet.producer_of(REMAINING_ADJUSTED_LOSSES_1988_AND_1989), Subtract)
    assert isinstance(worksheet.producer_of(NET_CAPITAL_LOSS_BALANCE_1988_AND_1989), ApplyFraction)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_APPLIED_1990_TO_1999), LesserOf)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999), Subtract)
    assert isinstance(worksheet.producer_of(REMAINING_ADJUSTED_LOSSES_1990_TO_1999), Subtract)
    assert isinstance(worksheet.producer_of(NET_CAPITAL_LOSS_BALANCE_1990_TO_1999), ApplyFraction)
    assert isinstance(worksheet.producer_of(ADJUSTED_LOSSES_APPLIED_2001_TO_2024), LesserOf)
    assert isinstance(worksheet.producer_of(REMAINING_ADJUSTED_LOSSES_2001_TO_2024), Subtract)
    assert isinstance(worksheet.producer_of(NET_CAPITAL_LOSS_BALANCE_2001_TO_2024), ApplyFraction)
    assert worksheet.producer_of(NET_CAPITAL_LOSSES_OF_OTHER_YEARS) is not worksheet.producer_of(
        NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM
    )
    assert isinstance(worksheet.producer_of(TAXABLE_INCOME), SubtractNotBelowZero)
    assert worksheet.producer_of(TAXABLE_INCOME) is not worksheet.producer_of(NET_INCOME)
    assert worksheet.producer_of(DEDUCTIONS_FROM_NET_INCOME) is not worksheet.producer_of(
        TOTAL_INCOME
    )
    assert worksheet.producer_of(DEDUCTIONS_FROM_NET_INCOME) is not worksheet.producer_of(
        DEDUCTIONS_FROM_TOTAL_INCOME
    )
    assert isinstance(worksheet.producer_of(FEDERAL_BASIC_TAX), ProgressiveTax)
    assert isinstance(worksheet.producer_of(ONTARIO_BASIC_TAX), ProgressiveTax)
    assert worksheet.producer_of(FEDERAL_BASIC_TAX) is not worksheet.producer_of(ONTARIO_BASIC_TAX)
    assert isinstance(worksheet.producer_of(BASIC_PERSONAL_AMOUNT), TaperedAmount)
    assert isinstance(worksheet.producer_of(ontario.BASIC_PERSONAL_AMOUNT), CreditAmount)
    assert worksheet.producer_of(BASIC_PERSONAL_AMOUNT) is not worksheet.producer_of(
        ontario.BASIC_PERSONAL_AMOUNT
    )
    assert isinstance(worksheet.producer_of(CANADA_EMPLOYMENT_AMOUNT), CappedAmount)
    # Schedule 5 line 5 and T1 line 30400; T1 line 30500; ON428 lines 14 to 16 (line 58160).
    assert isinstance(
        worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT), TimesCount)
    # T1 line 30100 and the Federal Worksheet (5000-D1) lines 1 to 7; T1 line 30300 and Schedule 5
    # (5000-S5) lines 2 to 5; T1 line 30425 and Schedule 5 lines 1 to 5 of its line 30425 part.
    assert isinstance(worksheet.producer_of(AGE_MAXIMUM), CreditAmount)
    assert isinstance(worksheet.producer_of(AGE_INCOME_THRESHOLD), CreditAmount)
    assert isinstance(worksheet.producer_of(AGE_INCOME_OVER_THRESHOLD), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(AGE_REDUCTION), ApplyRate)
    assert isinstance(worksheet.producer_of(AGE_AMOUNT_BEFORE_COUNT), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(AGE_AMOUNT), TimesCount)
    assert isinstance(worksheet.producer_of(SPOUSE_INFIRMITY_SUPPLEMENT), PerUnitAmount)
    assert isinstance(worksheet.producer_of(SPOUSE_AMOUNT_BASIS), Sum)
    assert isinstance(worksheet.producer_of(SPOUSE_AMOUNT_BEFORE_COUNT), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(SPOUSE_AMOUNT), TimesCount)
    assert isinstance(worksheet.producer_of(SPOUSE_CAREGIVER_BASE), CreditAmount)
    assert isinstance(worksheet.producer_of(SPOUSE_CAREGIVER_BEFORE_MAXIMUM), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(SPOUSE_CAREGIVER_LIMIT), CappedAmount)
    assert isinstance(
        worksheet.producer_of(SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(SPOUSE_CAREGIVER_AMOUNT), TimesCount)
    assert worksheet.producer_of(AGE_AMOUNT) is not worksheet.producer_of(SPOUSE_AMOUNT)
    assert worksheet.producer_of(SPOUSE_AMOUNT) is not worksheet.producer_of(
        SPOUSE_CAREGIVER_AMOUNT
    )
    assert worksheet.producer_of(SPOUSE_AMOUNT) is not worksheet.producer_of(
        ELIGIBLE_DEPENDANT_AMOUNT
    )
    assert worksheet.producer_of(AGE_MAXIMUM) is not worksheet.producer_of(SPOUSE_CAREGIVER_BASE)
    assert worksheet.producer_of(SPOUSE_INFIRMITY_SUPPLEMENT) is not (
        worksheet.producer_of(INFIRM_CHILDREN_AMOUNT)
    )
    assert isinstance(worksheet.producer_of(INFIRM_CHILDREN_AMOUNT), PerUnitAmount)
    # T1 line 30450, over the record list of infirm dependants.
    assert isinstance(worksheet.producer_of(CAREGIVER_AMOUNT), CaregiverAmount)
    # T1 lines 107 to 112, one capability for each line: line 108 "Amount from line 23600
    # multiplied by 3%", line 109 "Enter whichever is less: $2,834 or the amount from line 108.",
    # line 110 "Line 107 minus line 109 (if negative, enter "0")", line 111 (line 33199) over the
    # record list of other dependants, and line 112 "Line 110 plus line 111".
    assert isinstance(worksheet.producer_of(MEDICAL_NET_INCOME_SHARE), ApplyRate)
    assert isinstance(worksheet.producer_of(MEDICAL_THRESHOLD), CappedAmount)
    assert isinstance(worksheet.producer_of(MEDICAL_EXPENSES_OVER_THRESHOLD), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(OTHER_DEPENDANTS_MEDICAL), OtherDependantsMedical)
    assert isinstance(worksheet.producer_of(MEDICAL_CLAIM), Sum)
    # T1 line 100 (line 31800), over the record list of dependants with a disability.
    assert isinstance(
        worksheet.producer_of(DISABILITY_TRANSFERRED_AMOUNT), DisabilityTransferAmount
    )
    assert worksheet.producer_of(INFIRM_CHILDREN_AMOUNT) is not worksheet.producer_of(
        TAX_REDUCTION_FOR_CHILDREN
    )
    assert isinstance(worksheet.producer_of(ELIGIBLE_DEPENDANT_BASE), CreditAmount)
    assert worksheet.producer_of(ELIGIBLE_DEPENDANT_BASE) is not worksheet.producer_of(
        ontario.BASIC_PERSONAL_AMOUNT
    )
    assert isinstance(
        worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM), SubtractNotBelowZero
    )
    assert worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM) is not (
        worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT)
    )
    assert isinstance(
        worksheet.producer_of(ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT), CappedAmount
    )
    assert isinstance(worksheet.producer_of(ontario.ELIGIBLE_DEPENDANT_AMOUNT), TimesCount)
    assert worksheet.producer_of(ontario.ELIGIBLE_DEPENDANT_AMOUNT) is not (
        worksheet.producer_of(ELIGIBLE_DEPENDANT_AMOUNT)
    )
    # ON428 line 17 (line 58185), over the record list of its dependants and line 58160.
    assert isinstance(worksheet.producer_of(ontario.CAREGIVER_AMOUNT), OntarioCaregiverAmount)
    assert worksheet.producer_of(ontario.CAREGIVER_AMOUNT) is not (
        worksheet.producer_of(CAREGIVER_AMOUNT)
    )
    # ON428 line 10 (line 58080) and Worksheet ON428 (5006-D) lines 1 to 7; ON428 lines 11 to 13
    # (line 58120).
    assert isinstance(worksheet.producer_of(ontario.AGE_MAXIMUM), CreditAmount)
    assert isinstance(worksheet.producer_of(ontario.AGE_INCOME_THRESHOLD), CreditAmount)
    assert isinstance(
        worksheet.producer_of(ontario.AGE_INCOME_OVER_THRESHOLD), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(ontario.AGE_REDUCTION), ApplyRate)
    assert isinstance(worksheet.producer_of(ontario.AGE_AMOUNT_BEFORE_COUNT), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(ontario.AGE_AMOUNT), TimesCount)
    assert worksheet.producer_of(ontario.AGE_AMOUNT) is not worksheet.producer_of(AGE_AMOUNT)
    assert isinstance(worksheet.producer_of(ontario.SPOUSE_BASE), CreditAmount)
    assert isinstance(
        worksheet.producer_of(ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(ontario.SPOUSE_AMOUNT_BEFORE_COUNT), CappedAmount)
    assert isinstance(worksheet.producer_of(ontario.SPOUSE_AMOUNT), TimesCount)
    assert worksheet.producer_of(ontario.SPOUSE_AMOUNT) is not worksheet.producer_of(SPOUSE_AMOUNT)
    assert isinstance(worksheet.producer_of(NON_REFUNDABLE_CREDIT_AMOUNTS), Sum)
    assert isinstance(worksheet.producer_of(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS), Sum)
    assert worksheet.producer_of(NON_REFUNDABLE_CREDIT_AMOUNTS) is not worksheet.producer_of(
        ontario.NON_REFUNDABLE_CREDIT_AMOUNTS
    )
    # T1 line 115 (line 33800) is the credit rate applied once; line 118 (line 35000) adds lines
    # 115 to 117, so it is a sum. ON428 line 46 (line 58840) is the Ontario credit rate applied
    # once; lines 47 and 48 are one rate each on Schedule 9 lines 13 and 14, line 49 (line 58969)
    # their sum and line 50 (line 61500) adds line 46 and line 49, so it is a sum too.
    assert isinstance(worksheet.producer_of(CREDIT_AMOUNTS_AT_CREDIT_RATE), ApplyRate)
    assert isinstance(worksheet.producer_of(NON_REFUNDABLE_TAX_CREDITS), Sum)
    assert isinstance(worksheet.producer_of(ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE), ApplyRate)
    assert isinstance(worksheet.producer_of(ontario.DONATIONS_FIRST_TIER_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(ontario.DONATIONS_OVER_FIRST_TIER_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(ontario.DONATIONS_AND_GIFTS_CREDIT), Sum)
    assert isinstance(worksheet.producer_of(ontario.NON_REFUNDABLE_TAX_CREDITS), Sum)
    assert worksheet.producer_of(ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE) is not (
        worksheet.producer_of(CREDIT_AMOUNTS_AT_CREDIT_RATE)
    )
    assert worksheet.producer_of(ontario.DONATIONS_AND_GIFTS_CREDIT) is not (
        worksheet.producer_of(DONATIONS_AND_GIFTS_CREDIT)
    )
    assert worksheet.producer_of(ontario.DONATIONS_FIRST_TIER_CREDIT) is not (
        worksheet.producer_of(ontario.DONATIONS_OVER_FIRST_TIER_CREDIT)
    )
    assert worksheet.producer_of(CREDIT_AMOUNTS_AT_CREDIT_RATE) is not worksheet.producer_of(
        ontario.NON_REFUNDABLE_TAX_CREDITS
    )
    assert worksheet.producer_of(CREDIT_AMOUNTS_AT_CREDIT_RATE) is not worksheet.producer_of(
        NON_REFUNDABLE_TAX_CREDITS
    )
    assert worksheet.producer_of(NON_REFUNDABLE_TAX_CREDITS) is not worksheet.producer_of(
        ontario.NON_REFUNDABLE_TAX_CREDITS
    )
    assert worksheet.producer_of(NON_REFUNDABLE_TAX_CREDITS) is not worksheet.producer_of(
        TAXABLE_CAPITAL_GAINS
    )
    assert isinstance(worksheet.producer_of(FEDERAL_TAX_AFTER_CREDITS), SubtractNotBelowZero)
    # Schedule 9: one capability for each line of the schedule and of its two charts.
    assert isinstance(worksheet.producer_of(DEPRECIABLE_GIFT_PROCEEDS_OR_COST), LesserOf)
    assert isinstance(worksheet.producer_of(DEPRECIABLE_GIFTS), LesserOf)
    assert isinstance(worksheet.producer_of(CAPITAL_PROPERTY_GIFTS), Subtract)
    assert isinstance(worksheet.producer_of(TOTAL_CHARITABLE_DONATIONS), Sum)
    assert isinstance(worksheet.producer_of(DONATION_LIMIT_ON_NET_INCOME), ApplyRate)
    assert isinstance(worksheet.producer_of(CAPITAL_GIFTS_TOTAL), Sum)
    assert isinstance(worksheet.producer_of(CAPITAL_GIFTS_LIMIT_ADDITION), ApplyRate)
    assert isinstance(worksheet.producer_of(DONATION_LIMIT_WITH_CAPITAL_GIFTS), Sum)
    assert isinstance(worksheet.producer_of(CHARITABLE_DONATIONS_LIMIT), LesserOf)
    assert isinstance(worksheet.producer_of(CHARITABLE_DONATIONS_CLAIMED), LesserOf)
    assert isinstance(worksheet.producer_of(DONATIONS_AND_GIFTS_TOTAL), Sum)
    assert isinstance(worksheet.producer_of(DONATION_FIRST_TIER_MAXIMUM), CreditAmount)
    assert isinstance(worksheet.producer_of(DONATIONS_FIRST_TIER), LesserOf)
    assert isinstance(worksheet.producer_of(DONATIONS_OVER_FIRST_TIER), Subtract)
    assert isinstance(
        worksheet.producer_of(DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(DONATION_HIGH_INCOME_THRESHOLD), CreditAmount)
    assert isinstance(
        worksheet.producer_of(TAXABLE_INCOME_OVER_DONATION_THRESHOLD), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(HIGH_INCOME_DONATIONS), LesserOf)
    assert isinstance(worksheet.producer_of(HIGH_INCOME_DONATION_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(REGULAR_RATE_DONATIONS), Subtract)
    assert isinstance(worksheet.producer_of(REGULAR_RATE_DONATION_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(FIRST_TIER_DONATION_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(DONATIONS_AND_GIFTS_CREDIT), Sum)
    # The Federal Worksheet's line 34990 calculation, lines 3, 4, 5 and 7.
    assert isinstance(worksheet.producer_of(TOP_UP_CREDITS_BASE), Sum)
    assert isinstance(worksheet.producer_of(TOP_UP_THRESHOLD), CreditAmount)
    assert isinstance(worksheet.producer_of(TOP_UP_EXCESS), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(TOP_UP_TAX_CREDIT), ApplyRate)
    schedule_9 = (
        DEPRECIABLE_GIFT_PROCEEDS_OR_COST,
        DEPRECIABLE_GIFTS,
        CAPITAL_PROPERTY_GIFTS,
        TOTAL_CHARITABLE_DONATIONS,
        DONATION_LIMIT_ON_NET_INCOME,
        CAPITAL_GIFTS_TOTAL,
        CAPITAL_GIFTS_LIMIT_ADDITION,
        DONATION_LIMIT_WITH_CAPITAL_GIFTS,
        CHARITABLE_DONATIONS_LIMIT,
        CHARITABLE_DONATIONS_CLAIMED,
        DONATIONS_AND_GIFTS_TOTAL,
        DONATION_FIRST_TIER_MAXIMUM,
        DONATIONS_FIRST_TIER,
        DONATIONS_OVER_FIRST_TIER,
        DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS,
        DONATION_HIGH_INCOME_THRESHOLD,
        TAXABLE_INCOME_OVER_DONATION_THRESHOLD,
        HIGH_INCOME_DONATIONS,
        HIGH_INCOME_DONATION_CREDIT,
        REGULAR_RATE_DONATIONS,
        REGULAR_RATE_DONATION_CREDIT,
        FIRST_TIER_DONATION_CREDIT,
        DONATIONS_AND_GIFTS_CREDIT,
        TOP_UP_CREDITS_BASE,
        TOP_UP_THRESHOLD,
        TOP_UP_EXCESS,
        TOP_UP_TAX_CREDIT,
    )
    # One line, one capability: no two lines share a producer.
    assert len({id(worksheet.producer_of(kind)) for kind in schedule_9}) == len(schedule_9)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_CREDITS), SubtractNotBelowZero)
    assert worksheet.producer_of(FEDERAL_TAX_AFTER_CREDITS) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_CREDITS
    )
    assert isinstance(worksheet.producer_of(ONTARIO_SURTAX), TieredSurcharge)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_WITH_SURTAX), Sum)
    assert worksheet.producer_of(ONTARIO_TAX_WITH_SURTAX) is not worksheet.producer_of(TOTAL_INCOME)
    # Worksheet ON428's lines A, 1, 2, 3 (line 61520) and ON428 lines 56, 58, 70 and 71, each
    # its own step.
    for kind in (
        ontario.DIVIDENDS_AMOUNT_A,
        ontario.DIVIDENDS_AMOUNT_B,
        ontario.DIVIDEND_TAX_CREDIT,
        ontario.ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT,
        ontario.DIVIDEND_CREDIT_FROM_LINE_57,
    ):
        assert isinstance(worksheet.producer_of(kind), Sum), kind
    assert isinstance(worksheet.producer_of(ontario.OTHER_DIVIDENDS_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(ontario.ELIGIBLE_DIVIDENDS_CREDIT), ApplyRate)
    assert isinstance(worksheet.producer_of(ontario.DIVIDENDS_AMOUNT_A_LESS_B), Subtract)
    assert isinstance(
        worksheet.producer_of(ontario.ONTARIO_TAX_LESS_DIVIDEND_CREDIT), SubtractNotBelowZero
    )
    assert isinstance(
        worksheet.producer_of(ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT), SubtractNotBelowZero
    )
    assert worksheet.producer_of(ontario.DIVIDENDS_AMOUNT_A) is not (
        worksheet.producer_of(DIVIDENDS_AMOUNT_A)
    )
    assert worksheet.producer_of(ontario.OTHER_DIVIDENDS_CREDIT) is not (
        worksheet.producer_of(OTHER_DIVIDENDS_CREDIT)
    )
    assert worksheet.producer_of(ontario.ELIGIBLE_DIVIDENDS_CREDIT) is not (
        worksheet.producer_of(ELIGIBLE_DIVIDENDS_CREDIT)
    )
    assert worksheet.producer_of(ontario.DIVIDENDS_AMOUNT_A_LESS_B) is not (
        worksheet.producer_of(DIVIDENDS_AMOUNT_A_LESS_B)
    )
    assert worksheet.producer_of(ontario.DIVIDEND_TAX_CREDIT) is not (
        worksheet.producer_of(DIVIDEND_TAX_CREDIT)
    )
    assert worksheet.producer_of(ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT) is not (
        worksheet.producer_of(ONTARIO_TAX_WITH_SURTAX)
    )
    assert isinstance(worksheet.producer_of(TAX_REDUCTION_BASIC), CreditAmount)
    assert worksheet.producer_of(TAX_REDUCTION_BASIC) is not worksheet.producer_of(
        ontario.BASIC_PERSONAL_AMOUNT
    )
    assert isinstance(worksheet.producer_of(TAX_REDUCTION_FOR_CHILDREN), PerUnitAmount)
    assert isinstance(worksheet.producer_of(TAX_REDUCTION_FOR_DEPENDANTS), PerUnitAmount)
    assert worksheet.producer_of(TAX_REDUCTION_FOR_CHILDREN) is not worksheet.producer_of(
        TAX_REDUCTION_FOR_DEPENDANTS
    )
    assert isinstance(worksheet.producer_of(TAX_REDUCTION_AMOUNTS), Sum)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_REDUCTION), MultipleOver)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_REDUCTION), SubtractNotBelowZero)
    assert worksheet.producer_of(ONTARIO_TAX_AFTER_REDUCTION) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_CREDITS
    )
    assert isinstance(worksheet.producer_of(LIFT_CREDIT_BEFORE_MAXIMUM), ApplyRate)
    assert worksheet.producer_of(LIFT_CREDIT_BEFORE_MAXIMUM) is not worksheet.producer_of(
        TAXABLE_CAPITAL_GAINS
    )
    assert isinstance(worksheet.producer_of(LIFT_MAXIMUM_CREDIT), CappedAmount)
    assert worksheet.producer_of(LIFT_MAXIMUM_CREDIT) is not worksheet.producer_of(
        CANADA_EMPLOYMENT_AMOUNT
    )
    assert isinstance(worksheet.producer_of(LIFT_REDUCTION), TieredSurcharge)
    assert worksheet.producer_of(LIFT_REDUCTION) is not worksheet.producer_of(ONTARIO_SURTAX)
    assert isinstance(worksheet.producer_of(LIFT_CREDIT), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_LIFT_CREDIT), SubtractNotBelowZero)
    assert worksheet.producer_of(LIFT_CREDIT) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_LIFT_CREDIT
    )
    assert worksheet.producer_of(ONTARIO_TAX_AFTER_LIFT_CREDIT) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_REDUCTION
    )
    assert isinstance(worksheet.producer_of(COMMUNITY_FOOD_PROGRAM_CREDIT), ApplyRate)
    assert worksheet.producer_of(COMMUNITY_FOOD_PROGRAM_CREDIT) is not worksheet.producer_of(
        LIFT_CREDIT_BEFORE_MAXIMUM
    )
    assert isinstance(worksheet.producer_of(ONTARIO_TAX_AFTER_FOOD_CREDIT), SubtractNotBelowZero)
    assert worksheet.producer_of(ONTARIO_TAX_AFTER_FOOD_CREDIT) is not worksheet.producer_of(
        ONTARIO_TAX_AFTER_LIFT_CREDIT
    )
    assert isinstance(worksheet.producer_of(ONTARIO_HEALTH_PREMIUM), TieredSurcharge)
    assert worksheet.producer_of(ONTARIO_HEALTH_PREMIUM) is not worksheet.producer_of(
        ONTARIO_SURTAX
    )
    assert worksheet.producer_of(ONTARIO_HEALTH_PREMIUM) is not worksheet.producer_of(
        LIFT_REDUCTION
    )
    assert isinstance(worksheet.producer_of(ONTARIO_TAX), Sum)
    assert worksheet.producer_of(ONTARIO_TAX) is not worksheet.producer_of(ONTARIO_TAX_WITH_SURTAX)
    assert isinstance(worksheet.producer_of(NET_FEDERAL_TAX), Sum)
    assert isinstance(worksheet.producer_of(TOTAL_PAYABLE), Sum)
    assert isinstance(worksheet.producer_of(WORKING_INCOME), Sum)
    assert isinstance(worksheet.producer_of(ADJUSTED_FAMILY_NET_INCOME), Sum)
    assert worksheet.producer_of(WORKING_INCOME) is not worksheet.producer_of(
        ADJUSTED_FAMILY_NET_INCOME
    )
    assert worksheet.producer_of(WORKING_INCOME) is not worksheet.producer_of(TOTAL_INCOME)
    # Schedule 6 lines 22, 27 and 28, once for each family status, and the count's choice.
    cwb_lines = (
        CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
        CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
        CWB_REDUCTION_WITHOUT_DEPENDANT,
        CWB_REDUCTION_WITH_DEPENDANT,
    )
    for kind in cwb_lines:
        assert isinstance(worksheet.producer_of(kind), TieredSurcharge)
    assert len({id(worksheet.producer_of(kind)) for kind in cwb_lines}) == 4
    assert worksheet.producer_of(CWB_REDUCTION_WITHOUT_DEPENDANT) is not worksheet.producer_of(
        LIFT_REDUCTION
    )
    for kind in (CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT, CANADA_WORKERS_BENEFIT_WITH_DEPENDANT):
        assert isinstance(worksheet.producer_of(kind), SubtractNotBelowZero)
        assert worksheet.producer_of(kind) is not worksheet.producer_of(LIFT_CREDIT)
    assert worksheet.producer_of(
        CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT
    ) is not worksheet.producer_of(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT)
    assert isinstance(worksheet.producer_of(CANADA_WORKERS_BENEFIT), ChooseByCount)
    # ON479 line 1 (the rate, then the maximum on the credit), line 14 (the maximum on the amount
    # paid, then the rate), lines 18 and 21 and T1 line 47900.
    assert isinstance(worksheet.producer_of(FERTILITY_CREDIT_BEFORE_MAXIMUM), ApplyRate)
    assert isinstance(worksheet.producer_of(FERTILITY_CREDIT), CappedAmount)
    assert isinstance(
        worksheet.producer_of(SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM), CappedAmount
    )
    assert isinstance(worksheet.producer_of(SENIORS_TRANSIT_CREDIT), ApplyRate)
    assert worksheet.producer_of(FERTILITY_CREDIT_BEFORE_MAXIMUM) is not worksheet.producer_of(
        SENIORS_TRANSIT_CREDIT
    )
    assert worksheet.producer_of(FERTILITY_CREDIT) is not worksheet.producer_of(
        SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM
    )
    # ON479 lines 3 to 13, one capability for each line: line 3 is the artifact ca-on/medical_claim
    # itself, lines 4 and 5 are the rate then the maximum, line 8 the sum of lines 6 and 7, line 9
    # the dataset as an artifact, line 10 a difference not below zero, line 12 the rate on it, line
    # 13 a difference not below zero, and the claim a count times line 13.
    assert isinstance(worksheet.producer_of(SENIORS_CARE_BEFORE_MAXIMUM), ApplyRate)
    assert isinstance(worksheet.producer_of(SENIORS_CARE_AMOUNT), CappedAmount)
    assert isinstance(worksheet.producer_of(SENIORS_CARE_FAMILY_NET_INCOME), Sum)
    assert isinstance(worksheet.producer_of(SENIORS_CARE_BASE_AMOUNT), CreditAmount)
    assert isinstance(worksheet.producer_of(SENIORS_CARE_INCOME_OVER_BASE), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(SENIORS_CARE_REDUCTION), ApplyRate)
    assert isinstance(worksheet.producer_of(SENIORS_CARE_BEFORE_CLAIM), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(SENIORS_CARE_CREDIT), TimesCount)
    assert worksheet.producer_of(SENIORS_CARE_BEFORE_MAXIMUM) is not worksheet.producer_of(
        SENIORS_CARE_REDUCTION
    )
    assert worksheet.producer_of(SENIORS_CARE_INCOME_OVER_BASE) is not worksheet.producer_of(
        SENIORS_CARE_BEFORE_CLAIM
    )
    assert worksheet.producer_of(SENIORS_CARE_BEFORE_MAXIMUM) is not worksheet.producer_of(
        FERTILITY_CREDIT_BEFORE_MAXIMUM
    )
    assert worksheet.producer_of(CLAIMS_SENIORS_CARE_CREDIT) is None
    for column in (1, 2, 3):
        assert isinstance(worksheet.producer_of(POLITICAL_COLUMN_LINES[column][2]), CreditAmount)
        assert isinstance(
            worksheet.producer_of(POLITICAL_COLUMN_LINES[column][3]), SubtractNotBelowZero
        )
        assert isinstance(worksheet.producer_of(POLITICAL_COLUMN_LINES[column][5]), ApplyRate)
        assert isinstance(worksheet.producer_of(POLITICAL_COLUMN_LINES[column][6]), CreditAmount)
        assert isinstance(worksheet.producer_of(POLITICAL_COLUMN_LINES[column][7]), Sum)
    assert isinstance(worksheet.producer_of(ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM), ChooseByRange)
    assert isinstance(worksheet.producer_of(ontario.POLITICAL_CREDIT), CappedAmount)
    assert worksheet.producer_of(ontario.POLITICAL_CREDIT) is not worksheet.producer_of(
        ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM
    )
    # Form T1221 line 4 (the slips added), then ON479 line 17 (the rate on it), which line 18 adds.
    assert isinstance(worksheet.producer_of(FLOW_THROUGH_SHARE_EXPENSES), FlowThroughShareExpenses)
    assert isinstance(worksheet.producer_of(FLOW_THROUGH_SHARE_CREDIT), ApplyRate)
    assert worksheet.producer_of(FLOW_THROUGH_SHARE_CREDIT) is not worksheet.producer_of(
        SENIORS_TRANSIT_CREDIT
    )
    assert isinstance(worksheet.producer_of(ONTARIO_CREDITS_SUBTOTAL), Sum)
    # Worksheet ON479 "Line 20": lines 5, 7 and 9 are the datasets as artifacts, lines 6 and 11
    # are differences not below zero, line 8 is the quotient, ON479 line 20 is the credit over the
    # placements, and line 63260 is their number; line 21 adds line 20 to line 19.
    assert isinstance(worksheet.producer_of(COOP_EDUCATION_PAYROLL_THRESHOLD), CreditAmount)
    assert isinstance(
        worksheet.producer_of(COOP_EDUCATION_PAYROLL_OVER_THRESHOLD), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(COOP_EDUCATION_PAYROLL_RANGE), CreditAmount)
    assert isinstance(worksheet.producer_of(COOP_EDUCATION_PHASE_OUT_SHARE), Quotient)
    assert isinstance(worksheet.producer_of(COOP_EDUCATION_FULL_SHARE), CreditAmount)
    assert isinstance(worksheet.producer_of(COOP_EDUCATION_REMAINING_SHARE), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(COOP_EDUCATION_CREDIT), CoopEducationCredit)
    assert isinstance(worksheet.producer_of(COOP_EDUCATION_PLACEMENT_COUNT), RecordCount)
    assert worksheet.producer_of(COOP_EDUCATION_PAYROLL_THRESHOLD) is not worksheet.producer_of(
        COOP_EDUCATION_PAYROLL_RANGE
    )
    assert worksheet.producer_of(COOP_EDUCATION_PAYROLL_OVER_THRESHOLD) is not (
        worksheet.producer_of(COOP_EDUCATION_REMAINING_SHARE)
    )
    assert isinstance(worksheet.producer_of(ONTARIO_CREDITS), Sum)
    assert isinstance(worksheet.producer_of(PROVINCIAL_CREDITS), Sum)
    assert (
        len(
            {
                id(worksheet.producer_of(kind))
                for kind in (
                    ONTARIO_CREDITS_SUBTOTAL,
                    ONTARIO_CREDITS,
                    PROVINCIAL_CREDITS,
                    TOTAL_CREDITS,
                )
            }
        )
        == 4
    )
    assert isinstance(worksheet.producer_of(TOTAL_CREDITS), Sum)
    assert worksheet.producer_of(NET_FEDERAL_TAX) is not worksheet.producer_of(TOTAL_PAYABLE)
    assert worksheet.producer_of(NET_FEDERAL_TAX) is not worksheet.producer_of(TOTAL_CREDITS)
    assert worksheet.producer_of(TOTAL_PAYABLE) is not worksheet.producer_of(TOTAL_CREDITS)
    assert worksheet.producer_of(TOTAL_PAYABLE) is not worksheet.producer_of(ONTARIO_TAX)
    # Not floored: T1 line 167 is negative for a refund.
    assert isinstance(worksheet.producer_of(REFUND_OR_BALANCE_OWING), Subtract)
    # Line 161 and line 46900: the "(maximum $1,000)" caps line 46800, then 25% of it.
    assert isinstance(
        worksheet.producer_of(EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM), CappedAmount
    )
    assert isinstance(worksheet.producer_of(EDUCATOR_SCHOOL_SUPPLY_CREDIT), ApplyRate)
    # Line 45200: the Federal Worksheet one step per printed line, then the working income
    # condition ("$4,390 or more"), then the residence and age counts.
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME), Sum)
    assert isinstance(
        worksheet.producer_of(MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS), Subtract
    )
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS), Sum)
    assert isinstance(
        worksheet.producer_of(MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME), Sum)
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_WORKING_INCOME), Sum)
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3), Sum)
    assert isinstance(
        worksheet.producer_of(MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2), Sum)
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3), Sum)
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4), Sum)
    assert isinstance(
        worksheet.producer_of(MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5), SubtractNotBelowZero
    )
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_LINE_6), Sum)
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_INCOME_THRESHOLD), CreditAmount)
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_LINE_8), SubtractNotBelowZero)
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_LINE_11), Sum)
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_LINE_13), ApplyRate)
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_LINE_14), CappedAmount)
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_LINE_15), ApplyRate)
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_LINE_16), SubtractNotBelowZero)
    assert isinstance(
        worksheet.producer_of(MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET), ThresholdGate
    )
    assert isinstance(worksheet.producer_of(MEDICAL_SUPPLEMENT_IF_RESIDENT), TimesCount)
    assert isinstance(worksheet.producer_of(REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT), TimesCount)
    assert worksheet.producer_of(MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET) is not (
        worksheet.producer_of(MEDICAL_SUPPLEMENT_LINE_16)
    )
    # Lines 45600, 45700, 46800, 47555 and 47600 are inputs the return takes, not computed.
    for kind in (
        PART_XII_2_TAX_CREDIT,
        EMPLOYEE_AND_PARTNER_GST_HST_REBATE,
        EDUCATOR_SUPPLIES_EXPENSES,
        JOURNALISM_LABOUR_TAX_CREDIT,
        TAX_PAID_BY_INSTALMENTS,
        ontario.OPPORTUNITIES_FUND_DONATION,
    ):
        assert worksheet.producer_of(kind) is None, kind
    # Line 48400 is floored, unlike line 167: a refund is never negative.
    assert isinstance(worksheet.producer_of(REFUND), SubtractNotBelowZero)
    assert worksheet.producer_of(REFUND) is not worksheet.producer_of(REFUND_OR_BALANCE_OWING)
    # The Ontario opportunities fund page: line 1 carries line 48400, line 3 is line 1 less line 2.
    assert isinstance(worksheet.producer_of(ontario.REFUND_BEFORE_DONATION), Sum)
    assert isinstance(worksheet.producer_of(ontario.NET_REFUND), Subtract)
    # Line 131 (T2038(IND) Part C): each expenditure at its own rate, then amount 3 adds them; line
    # 132 adds line 131 to line 126, a sum that is not the net federal tax's.
    assert isinstance(worksheet.producer_of(ITC_RECAPTURE_AT_15_PERCENT), ApplyRate)
    assert isinstance(worksheet.producer_of(ITC_RECAPTURE_AT_20_PERCENT), ApplyRate)
    assert worksheet.producer_of(ITC_RECAPTURE_AT_15_PERCENT) is not worksheet.producer_of(
        ITC_RECAPTURE_AT_20_PERCENT
    )
    assert isinstance(worksheet.producer_of(ITC_RECAPTURE), Sum)
    assert isinstance(worksheet.producer_of(FEDERAL_TAX_WITH_ITC_RECAPTURE), Sum)
    assert worksheet.producer_of(FEDERAL_TAX_WITH_ITC_RECAPTURE) is not worksheet.producer_of(
        NET_FEDERAL_TAX
    )
    # Line 41400: the percentage first, then the maximum of $750 on the credit.
    assert isinstance(
        worksheet.producer_of(LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM), ApplyRate
    )
    assert isinstance(worksheet.producer_of(LABOUR_SPONSORED_FUNDS_CREDIT), CappedAmount)
    # Line 41000: each Federal Worksheet column as printed, the column that applies, the shortcut's
    # $650 over it, then the maximum of $650.
    for column in (1, 2, 3):
        assert isinstance(
            worksheet.producer_of(FEDERAL_POLITICAL_COLUMN_LINES[column][2]), CreditAmount
        )
        assert isinstance(
            worksheet.producer_of(FEDERAL_POLITICAL_COLUMN_LINES[column][3]), SubtractNotBelowZero
        )
        assert isinstance(
            worksheet.producer_of(FEDERAL_POLITICAL_COLUMN_LINES[column][5]), ApplyRate
        )
        assert isinstance(
            worksheet.producer_of(FEDERAL_POLITICAL_COLUMN_LINES[column][6]), CreditAmount
        )
        assert isinstance(worksheet.producer_of(FEDERAL_POLITICAL_COLUMN_LINES[column][7]), Sum)
    assert isinstance(worksheet.producer_of(POLITICAL_CREDIT_CHOSEN_COLUMN), ChooseByRange)
    assert isinstance(worksheet.producer_of(POLITICAL_CREDIT_SHORTCUT_THRESHOLD), CreditAmount)
    assert isinstance(worksheet.producer_of(POLITICAL_CREDIT_SHORTCUT_AMOUNT), CreditAmount)
    assert isinstance(worksheet.producer_of(POLITICAL_CREDIT_BEFORE_MAXIMUM), ChooseByRange)
    assert worksheet.producer_of(POLITICAL_CREDIT_BEFORE_MAXIMUM) is not worksheet.producer_of(
        POLITICAL_CREDIT_CHOSEN_COLUMN
    )
    assert isinstance(worksheet.producer_of(POLITICAL_CREDIT), CappedAmount)
    # Line 138 adds lines 135 and 137; line 139 is floored, like line 126.
    assert isinstance(worksheet.producer_of(CREDITS_AGAINST_FEDERAL_TAX), Sum)
    assert isinstance(worksheet.producer_of(FEDERAL_TAX_LESS_CREDITS), SubtractNotBelowZero)
    assert worksheet.producer_of(FEDERAL_TAX_LESS_CREDITS) is not worksheet.producer_of(
        FEDERAL_TAX_AFTER_CREDITS
    )
    # Form T1172: line 3 and line 7 are the lesser of two lines, line 4 is the printed
    # $50,000.00, lines 6 and 8 subtract with no floor, lines 10 and 13 are 20% of line 8 and
    # line 11, and the count of Part A chooses between them.
    assert isinstance(worksheet.producer_of(RESP_AIPS_CONTRIBUTIONS_COUNTED), LesserOf)
    assert isinstance(worksheet.producer_of(RESP_AIPS_LIFETIME_LIMIT), CreditAmount)
    assert isinstance(worksheet.producer_of(RESP_AIPS_LIMIT_REMAINING), Subtract)
    assert isinstance(worksheet.producer_of(RESP_AIPS_REDUCTION), LesserOf)
    assert worksheet.producer_of(RESP_AIPS_REDUCTION) is not worksheet.producer_of(
        RESP_AIPS_CONTRIBUTIONS_COUNTED
    )
    assert isinstance(worksheet.producer_of(RESP_AIPS_SUBJECT_TO_TAX), Subtract)
    assert isinstance(worksheet.producer_of(RESP_AIPS_PART_A_TAX), ApplyRate)
    assert isinstance(worksheet.producer_of(RESP_AIPS_PART_B_TAX), ApplyRate)
    assert worksheet.producer_of(RESP_AIPS_PART_A_TAX) is not worksheet.producer_of(
        RESP_AIPS_PART_B_TAX
    )
    assert isinstance(worksheet.producer_of(RESP_AIPS_ADDITIONAL_TAX), ChooseByCount)
    # Line 41800 adds Form T1172's tax and the RL-10 amount.
    assert isinstance(worksheet.producer_of(SPECIAL_TAXES), Sum)
    # Lines 67193, 67195, 41300, 41500, Form T1172's lines 1, 2, 5 and 11, its count of Part A
    # and the RL-10 amount are inputs the return takes, not computed.
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
    ):
        assert worksheet.producer_of(kind) is None, kind
    assert worksheet.producer_of(RESP_AIPS_PART_A_APPLIES) is None


def test_the_trace_explains_the_computation() -> None:
    worksheet = return_a()
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)

    def position(
        expected: str,
        amount: str,
        claimed: ArtifactKind[Decimal] | None = None,
        output: ArtifactKind[Decimal] | None = None,
    ) -> int:
        """The index of the one rendered line reading `expected` whose line has `amount`.

        A claimed line (an amount times a count) reads the same federally and for Ontario when the
        amounts are alike, so it is told apart by the kind of the amount it claims. Any other line
        that reads the same federally and for Ontario, such as the medical lines and the totals of
        items, is told apart by the kind it produces, `output`.
        """
        (found,) = [
            i
            for i, (text, line) in enumerate(zip(rendered, worksheet.trace, strict=True))
            if text == expected
            and line.amount == D(amount)
            and (
                claimed is None
                or (isinstance(line, TimesCountLine) and line.amount_kind is claimed)
            )
            and (output is None or getattr(line, "output", None) is output)
        ]
        return found

    taxable_gains = position(
        "taxable_capital_gains: 50% of capital_gain 20000 (half-up to 0.01)", "10000"
    )
    investment_before = position(
        "investment_income_before_prior_years: t3_investment_income 0 + "
        "t5_investment_income 0 + t5013_investment_income 0 + "
        "investment_income_credited_not_received 0 + tax_refund_interest 0 + "
        "foreign_investment_income 0 + investment_income_without_a_slip 0 + "
        "investment_royalties 0 = 0",
        "0",
    )
    interest = position(
        "interest_and_other_investment_income: "
        "investment_income_before_prior_years 0 less "
        "investment_income_reported_in_previous_years 0 = 0",
        "0",
    )
    support = position(
        "income_support_benefits: workers_compensation_benefits 0 + "
        "social_assistance_payments 0 + net_federal_supplements 0 = 0",
        "0",
    )
    total = position(
        "total_income: employment_income 110000 + other_employment_income 0 + "
        "old_age_security 0 + cpp_or_qpp_benefits 0 + "
        "other_pensions_and_superannuation 0 + elected_split_pension_amount 0 + "
        "universal_child_care_benefit 0 + ei_and_other_benefits 0 + taxable_dividends 0 + "
        "interest_and_other_investment_income 0 + net_partnership_income 0 + "
        "rdsp_income 0 + taxable_capital_gains 10000 + taxable_support_payments 0 "
        "+ rrsp_income 0 + fhsa_income 0 + other_fhsa_income 0 + other_income 0 + "
        "taxable_scholarships 0 + income_support_benefits 0 = 120000",
        "120000",
    )
    cpp_base = position(
        "cpp_base_contributions: 4.95% of employment_income between 3500 and 71300 (67800), "
        "at most 3356.1 (half-up to 0.01)",
        "3356.10",
    )
    cpp_first = position(
        "cpp_first_additional_contributions: 1% of employment_income between 3500 and 71300 "
        "(67800), at most 678 (half-up to 0.01)",
        "678.00",
    )
    cpp_second = position(
        "cpp_second_additional_contributions: 4% of employment_income between 71300 and 81200 "
        "(9900), at most 396 (half-up to 0.01)",
        "396.00",
    )
    cpp_enhanced = position(
        "cpp_enhanced_contributions: cpp_first_additional_contributions 678 "
        "+ cpp_second_additional_contributions 396 = 1074",
        "1074.00",
    )
    ei = position(
        "ei_premiums: 1.64% of employment_income between 0 and 65700 (65700), "
        "at most 1077.48 (half-up to 0.01)",
        "1077.48",
    )
    rrsp_available = position(
        "rrsp_contributions_available: unused_rrsp_contributions 0 "
        "+ rrsp_contributions 1926 = 1926",
        "1926",
    )
    rrsp_maximum = position(
        "rrsp_deduction_maximum: lesser of rrsp_contributions_available 1926 "
        "and rrsp_deduction_limit 19800 = 1926",
        "1926",
    )
    rrsp = position(
        "rrsp_deduction: rrsp_amount_deducted 1926, at most rrsp_deduction_maximum 1926",
        "1926",
    )
    rrsp_carried = position(
        "unused_rrsp_contributions_carried_forward: rrsp_contributions_available 1926 "
        "less rrsp_deduction 1926 = 0",
        "0",
    )
    # Form T778 Part B lines 1 to 3 for no eligible children, line 4, line 6 two-thirds of the
    # employment income, and line 7 the least of lines 4, 5 and 6.
    child_care_under_seven = position(
        "child_care_limit_for_children_under_seven: 8000 for each of 0 children_under_seven "
        "= 0 (half-up to 0.01)",
        "0",
    )
    child_care_disability = position(
        "child_care_limit_for_children_with_disability: 11000 for each of 0 "
        "children_with_disability = 0 (half-up to 0.01)",
        "0",
    )
    child_care_seven_to_sixteen = position(
        "child_care_limit_for_children_seven_to_sixteen: 5000 for each of 0 "
        "children_seven_to_sixteen = 0 (half-up to 0.01)",
        "0",
    )
    child_care_basic = position(
        "child_care_basic_limit: child_care_limit_for_children_under_seven 0 "
        "+ child_care_limit_for_children_with_disability 0 "
        "+ child_care_limit_for_children_seven_to_sixteen 0 = 0",
        "0",
    )
    child_care_earned = position(
        "child_care_earned_income: employment_income 110000 = 110000", "110000"
    )
    child_care_earned_limit = position(
        "child_care_earned_income_limit: 2/3 of child_care_earned_income 110000 (half-up to 0.01)",
        "73333.33",
    )
    child_care = position(
        "child_care_expenses: lesser of child_care_basic_limit 0 and child_care_expenses_paid 0 "
        "and child_care_earned_income_limit 73333.33 = 0",
        "0",
    )
    deductions = position(
        "deductions_from_total_income: rpp_deduction 0 + rrsp_deduction 1926 + fhsa_deduction 0 "
        "+ elected_split_pension_deduction 0 + union_dues 2000 + uccb_repayment 0 "
        "+ child_care_expenses 0 + allowable_business_investment_loss 0 "
        "+ support_payments_deduction 0 "
        "+ carrying_charges_interest_expenses_and_other_expenses 0 "
        "+ cpp_enhanced_contributions 1074 + exploration_and_development_expenses 0 "
        "+ other_deductions 0 = 5000",
        "5000",
    )
    net = position(
        "net_income: total_income 120000 less deductions_from_total_income 5000, "
        "not below 0 = 115000",
        "115000",
    )
    uccb_and_rdsp = position(
        "uccb_and_rdsp_income: universal_child_care_benefit 0 + rdsp_income 0 = 0", "0"
    )
    line_5 = position(
        "net_income_less_uccb_and_rdsp_income: net_income 115000 less uccb_and_rdsp_income 0 "
        "= 115000",
        "115000",
    )
    repayments = position(
        "uccb_and_rdsp_income_repayments: uccb_repayment 0 + rdsp_income_repayment 0 = 0", "0"
    )
    line_9 = position(
        "other_payments_limit_income: net_income_less_uccb_and_rdsp_income 115000 "
        "+ uccb_and_rdsp_income_repayments 0 = 115000",
        "115000",
    )
    after_limit = position(
        "other_payments_deduction_after_limit: income_support_benefits 0, "
        "chosen as other_payments_worksheet_line_9_over_limit is 0",
        "0",
    )
    other_payments = position(
        "other_payments_deduction: income_support_benefits 0, "
        "chosen as other_payments_worksheet_required is 0",
        "0",
    )
    net_deductions = position(
        "deductions_from_net_income: canadian_armed_forces_and_police_deduction 0 "
        "+ security_options_deductions 0 + other_payments_deduction 0 "
        "+ limited_partnership_losses_of_other_years 0 + non_capital_losses_of_other_years 0 "
        "+ net_capital_losses_of_other_years 0 + additional_deductions 0 = 0",
        "0",
    )
    taxable = position(
        "taxable_income: net_income 115000 less deductions_from_net_income 0, not below 0 = 115000",
        "115000",
    )
    # T1 Part A, the column "more than $114,750 but not more than $177,882": line 72 is
    # 115000 - 114750 = 250, line 74 is 26% of it, 65.00, and line 76 adds line 75's 20,081.25.
    federal_column = position("26% on 250 over 114750 plus 20081.25", "20146.25")
    federal_basic = position(
        "federal_basic_tax on taxable_income 115000 (half-up to 0.01)", "20146.25"
    )
    federal_amount = position(
        "basic_personal_amount: 14538 plus 1591 less 0 for net_income 115000 over 177882 "
        "(range 75532), not below 14538 (half-up to 0.01)",
        "16129",
    )
    employment_amount = position(
        "canada_employment_amount: lesser of employment_income 110000 and 1471 (half-up to 0.01)",
        "1471",
    )
    # Schedule 5 line 5, then T1 line 30400 for 0 eligible dependants; line 30500.
    federal_dependant = position(
        "eligible_dependant_amount_before_count: basic_personal_amount 16129 "
        "less dependant_net_income 0, not below 0 = 16129",
        "16129",
    )
    federal_dependant_claimed = position(
        "eligible_dependant_amount: eligible_dependant_amount_before_count 16129 "
        "for each of 0 eligible_dependants = 0",
        "0",
    )
    # Schedule 5's chart for line 30450 and Worksheet ON428's for line 58185 read alike when
    # both lists are empty, so each total is told apart by the kind it produces.
    federal_caregiver = position("caregiver_amount: no items = 0", "0", output=CAREGIVER_AMOUNT)
    ontario_caregiver = position(
        "caregiver_amount: no items = 0", "0", output=ontario.CAREGIVER_AMOUNT
    )
    disability_transfer = position("disability_transferred_amount: no items = 0", "0")
    infirm_children = position(
        "infirm_children_amount: 2687 for each of 0 infirm_children = 0 (half-up to 0.01)", "0"
    )
    # T1 lines 108 to 112: 3% of the net income of 115000, at most 2834 (line 109), which the
    # medical expenses of 0 (line 107) do not reach (line 110), no other dependants (line 111).
    medical_share = position(
        "medical_net_income_share: 3% of net_income 115000 (half-up to 0.01)",
        "3450",
        output=MEDICAL_NET_INCOME_SHARE,
    )
    medical_threshold = position(
        "medical_threshold: lesser of medical_net_income_share 3450 and 2834 (half-up to 0.01)",
        "2834",
    )
    medical_over = position(
        "medical_expenses_over_threshold: medical_expenses 0 less medical_threshold 2834, "
        "not below 0 = 0",
        "0",
    )
    other_medical = position(
        "other_dependants_medical: no items = 0", "0", output=OTHER_DEPENDANTS_MEDICAL
    )
    medical_claim = position(
        "medical_claim: medical_expenses_over_threshold 0 + other_dependants_medical 0 = 0",
        "0",
        output=MEDICAL_CLAIM,
    )
    # ON428 lines 37 to 43: 3% of the same net income, at most 2885 (line 40), which the medical
    # expenses of 0 (line 36) do not reach (line 41), no other dependants (line 42, line 58729).
    ontario_medical_share = position(
        "medical_net_income_share: 3% of net_income 115000 (half-up to 0.01)",
        "3450",
        output=ontario.MEDICAL_NET_INCOME_SHARE,
    )
    ontario_medical_threshold = position(
        "medical_threshold: lesser of medical_net_income_share 3450 and 2885 (half-up to 0.01)",
        "2885",
    )
    ontario_medical_over = position(
        "medical_expenses_over_threshold: medical_expenses 0 less medical_threshold 2885, "
        "not below 0 = 0",
        "0",
    )
    ontario_other_medical = position(
        "other_dependants_medical: no items = 0", "0", output=ontario.OTHER_DEPENDANTS_MEDICAL
    )
    ontario_medical_claim = position(
        "medical_claim: medical_expenses_over_threshold 0 + other_dependants_medical 0 = 0",
        "0",
        output=ontario.MEDICAL_CLAIM,
    )
    # Federal Worksheet (5000-D1) lines 1 to 7 and T1 line 30100: 15% x (115000 - 45522) =
    # 10421.70 is more than the maximum 9028, so line 7 is 0, claimed for 0 filers born in 1960
    # or earlier.
    age_maximum = position("age_maximum: credit amount 9028 (half-up to 0.01)", "9028.00")
    age_threshold = position(
        "age_income_threshold: credit amount 45522 (half-up to 0.01)", "45522.00"
    )
    age_over_threshold = position(
        "age_income_over_threshold: net_income 115000 less age_income_threshold 45522, not below 0 "
        "= 69478",
        "69478",
    )
    age_reduction = position(
        "age_reduction: 15% of age_income_over_threshold 69478 (half-up to 0.01)", "10421.70"
    )
    age_before_count = position(
        "age_amount_before_count: age_maximum 9028 less age_reduction 10421.7, not below 0 = 0",
        "0",
    )
    age = position(
        "age_amount: age_amount_before_count 0 for each of 0 born_in_1960_or_earlier = 0",
        "0",
        AGE_AMOUNT_BEFORE_COUNT,
    )
    # Schedule 5 (5000-S5) line 30300 lines 2 to 5 and T1 line 30300, for 0 spouse amounts claimed.
    spouse_supplement = position(
        "spouse_infirmity_supplement: 2687 for each of 0 spouse_caregiver_eligible = 0 "
        "(half-up to 0.01)",
        "0",
    )
    spouse_basis = position(
        "spouse_amount_basis: basic_personal_amount 16129 + spouse_infirmity_supplement 0 = 16129",
        "16129",
    )
    spouse_before_count = position(
        "spouse_amount_before_count: spouse_amount_basis 16129 "
        "less spouse_net_income 0, not below 0 = 16129",
        "16129",
    )
    spouse = position(
        "spouse_amount: spouse_amount_before_count 16129 for each of 0 spouses_claimed = 0", "0"
    )
    # Schedule 5 line 30425 lines 1 to 5 and T1 line 30425, for 0 spouses eligible for the Canada
    # caregiver amount.
    caregiver_base = position(
        "spouse_caregiver_base: credit amount 28798 (half-up to 0.01)", "28798.00"
    )
    caregiver_before_maximum = position(
        "spouse_caregiver_before_maximum: spouse_caregiver_base 28798 "
        "less spouse_net_income 0, not below 0 = 28798",
        "28798",
    )
    caregiver_limit = position(
        "spouse_caregiver_limit: lesser of spouse_caregiver_before_maximum 28798 and 8601 "
        "(half-up to 0.01)",
        "8601",
    )
    caregiver_before_count = position(
        "spouse_caregiver_amount_before_count: spouse_caregiver_limit 8601 "
        "less spouse_amount 0, not below 0 = 8601",
        "8601",
    )
    caregiver = position(
        "spouse_caregiver_amount: spouse_caregiver_amount_before_count 8601 "
        "for each of 0 spouse_caregiver_eligible = 0",
        "0",
    )
    federal_amounts = position(
        "non_refundable_credit_amounts: basic_personal_amount 16129 "
        "+ age_amount 0 + spouse_amount 0 "
        "+ eligible_dependant_amount 0 + spouse_caregiver_amount 0 + caregiver_amount 0 "
        "+ infirm_children_amount 0 "
        "+ cpp_base_contributions 3356.1 + ei_premiums 1077.48 "
        "+ canada_employment_amount 1471 + disability_transferred_amount 0 "
        "+ medical_claim 0 = 22033.58",
        "22033.58",
    )
    # T1 line 115 (line 33800); line 118 (line 35000) adds lines 115 to 117 further below.
    federal_credit = position(
        "credit_amounts_at_credit_rate: 14.5% of non_refundable_credit_amounts 22033.58 "
        "(half-up to 0.01)",
        "3194.87",
    )
    federal_after = position(
        "federal_tax_after_credits: federal_basic_tax 20146.25 "
        "less credits_against_basic_federal_tax 3194.87, not below 0 = 16951.38",
        "16951.38",
    )
    # ON428 Part A, the column "more than $105,775 but not more than $150,000": line 4 is
    # 115000 - 105775 = 9225, line 6 is 11.16% of it, 1029.51, and line 8 adds line 7's 7,510.09.
    ontario_column = position("11.16% on 9225 over 105775 plus 7510.09", "8539.60")
    ontario_basic = position(
        "ontario_basic_tax on taxable_income 115000 (half-up to 0.01)", "8539.60"
    )
    ontario_amount = position(
        "basic_personal_amount: credit amount 12747 (half-up to 0.01)", "12747"
    )
    # ON428 lines 14 to 16 (line 58160), for 0 eligible dependants.
    ontario_base = position(
        "eligible_dependant_base: credit amount 11905 (half-up to 0.01)", "11905"
    )
    ontario_before_maximum = position(
        "eligible_dependant_amount_before_maximum: eligible_dependant_base 11905 "
        "less dependant_net_income 0, not below 0 = 11905",
        "11905",
    )
    ontario_dependant = position(
        "eligible_dependant_amount_before_count: lesser of "
        "eligible_dependant_amount_before_maximum 11905 and 10823 (half-up to 0.01)",
        "10823",
    )
    ontario_dependant_claimed = position(
        "eligible_dependant_amount: eligible_dependant_amount_before_count 10823 "
        "for each of 0 eligible_dependants = 0",
        "0",
    )
    # Worksheet ON428 (5006-D) lines 1 to 7 and ON428 line 10 (line 58080): 15% x (115000 -
    # 46330) = 10300.50 is more than the maximum 6223, so line 7 is 0, claimed for 0 filers born
    # in 1960 or earlier; ON428 lines 11 to 13 (line 58120), for 0 spouse amounts claimed.
    ontario_age_maximum = position("age_maximum: credit amount 6223 (half-up to 0.01)", "6223.00")
    ontario_age_threshold = position(
        "age_income_threshold: credit amount 46330 (half-up to 0.01)", "46330.00"
    )
    ontario_age_over_threshold = position(
        "age_income_over_threshold: net_income 115000 less age_income_threshold 46330, not below 0 "
        "= 68670",
        "68670",
    )
    ontario_age_reduction = position(
        "age_reduction: 15% of age_income_over_threshold 68670 (half-up to 0.01)", "10300.50"
    )
    ontario_age_before_count = position(
        "age_amount_before_count: age_maximum 6223 less age_reduction 10300.5, not below 0 = 0",
        "0",
    )
    ontario_age = position(
        "age_amount: age_amount_before_count 0 for each of 0 born_in_1960_or_earlier = 0",
        "0",
        ontario.AGE_AMOUNT_BEFORE_COUNT,
    )
    ontario_spouse_base = position("spouse_base: credit amount 11905 (half-up to 0.01)", "11905")
    ontario_spouse_before_maximum = position(
        "spouse_amount_before_maximum: spouse_base 11905 "
        "less spouse_net_income 0, not below 0 = 11905",
        "11905",
    )
    ontario_spouse_before_count = position(
        "spouse_amount_before_count: lesser of spouse_amount_before_maximum 11905 and 10823 "
        "(half-up to 0.01)",
        "10823",
    )
    ontario_spouse = position(
        "spouse_amount: spouse_amount_before_count 10823 for each of 0 spouses_claimed = 0", "0"
    )
    ontario_amounts = position(
        "non_refundable_credit_amounts: basic_personal_amount 12747 "
        "+ age_amount 0 + spouse_amount 0 + eligible_dependant_amount 0 "
        "+ caregiver_amount 0 + cpp_base_contributions 3356.1 + ei_premiums 1077.48 "
        "+ medical_claim 0 = 17180.58",
        "17180.58",
    )
    # ON428 line 46 (line 58840); line 50 (line 61500) adds lines 46 and 49 further below.
    ontario_credit = position(
        "credit_amounts_at_credit_rate: 5.05% of non_refundable_credit_amounts 17180.58 "
        "(half-up to 0.01)",
        "867.62",
    )
    ontario_first_tier_credit = position(
        "donations_first_tier_credit: 5.05% of donations_first_tier 0 (half-up to 0.01)", "0"
    )
    ontario_over_first_tier_credit = position(
        "donations_over_first_tier_credit: 11.16% of donations_over_first_tier 0 (half-up to 0.01)",
        "0",
    )
    ontario_donations_credit = position(
        "donations_and_gifts_credit: donations_first_tier_credit 0 "
        "+ donations_over_first_tier_credit 0 = 0",
        "0",
    )
    ontario_line_50 = position(
        "non_refundable_tax_credits: credit_amounts_at_credit_rate 867.62 "
        "+ donations_and_gifts_credit 0 = 867.62",
        "867.62",
    )
    ontario_after = position(
        "ontario_tax_after_credits: ontario_basic_tax 8539.6 "
        "less non_refundable_tax_credits 867.62, not below 0 = 7671.98",
        "7671.98",
    )
    surtax_first = position(
        "ontario_surtax: 20% of ontario_tax_after_credits 7671.98 over 5710 (half-up to 0.01)",
        "392.40",
    )
    surtax_second = position(
        "ontario_surtax: 36% of ontario_tax_after_credits 7671.98 over 7307 (half-up to 0.01)",
        "131.39",
    )
    with_surtax = position(
        "ontario_tax_with_surtax: ontario_tax_after_credits 7671.98 "
        "+ ontario_surtax 523.79 = 8195.77",
        "8195.77",
    )
    dividend_a = position("dividends_amount_a: taxable_dividends 0 = 0", "0")
    dividend_b = position("dividends_amount_b: taxable_dividends_other_than_eligible 0 = 0", "0")
    dividend_other = position(
        "other_dividends_credit: 2.9863% of dividends_amount_b 0 (half-up to 0.01)", "0"
    )
    dividend_eligible = position(
        "eligible_dividends_credit: 10% of dividends_amount_a_less_b 0 (half-up to 0.01)", "0"
    )
    dividend_credit = position(
        "dividend_tax_credit: other_dividends_credit 0 + eligible_dividends_credit 0 = 0", "0"
    )
    line_56 = position(
        "ontario_tax_before_dividend_credit: ontario_tax_after_credits 7671.98 = 7671.98",
        "7671.98",
    )
    line_58 = position(
        "ontario_tax_less_dividend_credit: ontario_tax_before_dividend_credit 7671.98 "
        "less dividend_tax_credit 0, not below 0 = 7671.98",
        "7671.98",
    )
    line_70 = position("dividend_credit_from_line_57: dividend_tax_credit 0 = 0", "0")
    line_71 = position(
        "ontario_tax_after_dividend_credit: ontario_tax_with_surtax 8195.77 "
        "less dividend_credit_from_line_57 0, not below 0 = 8195.77",
        "8195.77",
    )
    reduction_basic = position(
        "tax_reduction_basic: credit amount 294 (half-up to 0.01)",
        "294.00",
    )
    reduction_children = position(
        "tax_reduction_for_children: 544 for each of 0 dependent_children = 0 (half-up to 0.01)",
        "0",
    )
    reduction_dependants = position(
        "tax_reduction_for_dependants: 544 for each of 0 dependants = 0 (half-up to 0.01)",
        "0",
    )
    reduction_amounts = position(
        "tax_reduction_amounts: tax_reduction_basic 294 + tax_reduction_for_children 0 "
        "+ tax_reduction_for_dependants 0 = 294",
        "294.00",
    )
    reduction = position(
        "ontario_tax_reduction: 2 × tax_reduction_amounts 294 "
        "over ontario_tax_after_dividend_credit 8195.77, not below 0 (half-up to 0.01)",
        "0",
    )
    after_reduction = position(
        "ontario_tax_after_reduction: ontario_tax_after_dividend_credit 8195.77 "
        "less ontario_tax_reduction 0, not below 0 = 8195.77",
        "8195.77",
    )
    lift_before_maximum = position(
        "lift_credit_before_maximum: 5.05% of employment_income 110000 (half-up to 0.01)", "5555"
    )
    lift_maximum = position(
        "lift_maximum_credit: lesser of lift_credit_before_maximum 5555 and 875 (half-up to 0.01)",
        "875",
    )
    lift_reduction = position(
        "lift_reduction: 5% of net_income 115000 over 32500 (half-up to 0.01)", "4125"
    )
    lift = position(
        "lift_credit: lift_maximum_credit 875 less lift_reduction 4125, not below 0 = 0", "0"
    )
    after_lift = position(
        "ontario_tax_after_lift_credit: ontario_tax_after_reduction 8195.77 "
        "less lift_credit 0, not below 0 = 8195.77",
        "8195.77",
    )
    food_credit = position(
        "community_food_program_credit: 25% of community_food_program_donations 0 "
        "(half-up to 0.01)",
        "0",
    )
    after_food = position(
        "ontario_tax_after_food_credit: ontario_tax_after_lift_credit 8195.77 "
        "less community_food_program_credit 0, not below 0 = 8195.77",
        "8195.77",
    )
    premium_first = position(
        "ontario_health_premium: 6% of taxable_income 115000 over 20000, at most 300 "
        "(half-up to 0.01)",
        "300",
    )
    premium_second = position(
        "ontario_health_premium: 6% of taxable_income 115000 over 36000, at most 150 "
        "(half-up to 0.01)",
        "150",
    )
    premium_third = position(
        "ontario_health_premium: 25% of taxable_income 115000 over 48000, at most 150 "
        "(half-up to 0.01)",
        "150",
    )
    premium_fourth = position(
        "ontario_health_premium: 25% of taxable_income 115000 over 72000, at most 150 "
        "(half-up to 0.01)",
        "150",
    )
    premium_fifth = position(
        "ontario_health_premium: 25% of taxable_income 115000 over 200000, at most 150 "
        "(half-up to 0.01)",
        "0",
    )
    ontario_tax = position(
        "ontario_tax: ontario_tax_after_food_credit 8195.77 + ontario_health_premium 750 = 8945.77",
        "8945.77",
    )
    # T1 line 131 (T2038(IND) Part C) and line 132 for no recapture; line 41400 and lines 138 and
    # 139 for a net cost of 0; Form T1172 Parts A and B for no AIPs, Part B chosen by a count of 0;
    # and line 41800.
    recapture_at_15 = position(
        "itc_recapture_at_15_percent: 15% of itc_recapture_expenditure_at_15_percent 0 "
        "(half-up to 0.01)",
        "0",
    )
    recapture_at_20 = position(
        "itc_recapture_at_20_percent: 20% of itc_recapture_expenditure_at_20_percent 0 "
        "(half-up to 0.01)",
        "0",
    )
    recapture = position(
        "itc_recapture: itc_recapture_at_15_percent 0 + itc_recapture_at_20_percent 0 = 0", "0"
    )
    with_recapture = position(
        "federal_tax_with_itc_recapture: federal_tax_after_credits 16951.38 + itc_recapture 0 "
        "= 16951.38",
        "16951.38",
    )
    labour_before_maximum = position(
        "labour_sponsored_funds_credit_before_maximum: 15% of labour_sponsored_funds_net_cost 0 "
        "(half-up to 0.01)",
        "0",
    )
    labour_credit = position(
        "labour_sponsored_funds_credit: lesser of labour_sponsored_funds_credit_before_maximum 0 "
        "and 750 (half-up to 0.01)",
        "0",
    )
    federal_credits = position(
        "credits_against_federal_tax: political_credit 0 + labour_sponsored_funds_credit 0 = 0", "0"
    )
    less_credits = position(
        "federal_tax_less_credits: federal_tax_with_itc_recapture 16951.38 "
        "less credits_against_federal_tax 0, not below 0 = 16951.38",
        "16951.38",
    )
    aips_counted = position(
        "resp_aips_contributions_counted: lesser of resp_aips_received_part_a 0 "
        "and resp_aips_rrsp_contributions 0 = 0",
        "0",
    )
    aips_limit = position(
        "resp_aips_lifetime_limit: credit amount 50000 (half-up to 0.01)", "50000"
    )
    aips_remaining = position(
        "resp_aips_limit_remaining: resp_aips_lifetime_limit 50000 "
        "less resp_aips_reduction_used_in_previous_years 0 = 50000",
        "50000",
    )
    aips_reduction = position(
        "resp_aips_reduction: lesser of resp_aips_contributions_counted 0 "
        "and resp_aips_limit_remaining 50000 = 0",
        "0",
    )
    aips_subject = position(
        "resp_aips_subject_to_tax: resp_aips_received_part_a 0 less resp_aips_reduction 0 = 0", "0"
    )
    aips_part_a = position(
        "resp_aips_part_a_tax: 20% of resp_aips_subject_to_tax 0 (half-up to 0.01)", "0"
    )
    aips_part_b = position(
        "resp_aips_part_b_tax: 20% of resp_aips_received_part_b 0 (half-up to 0.01)", "0"
    )
    aips_tax = position(
        "resp_aips_additional_tax: resp_aips_part_b_tax 0, chosen as resp_aips_part_a_applies is 0",
        "0",
    )
    special = position(
        "special_taxes: resp_aips_additional_tax 0 + rl_10_labour_sponsored_fund_amount 0 = 0", "0"
    )
    net_federal = position(
        "net_federal_tax: federal_tax_less_credits 16951.38 + advanced_canada_workers_benefit 0 "
        "+ special_taxes 0 = 16951.38",
        "16951.38",
    )
    payable = position(
        "total_payable: net_federal_tax 16951.38 + ontario_tax 8945.77 = 25897.15",
        "25897.15",
    )
    working = position("working_income: employment_income 110000 = 110000", "110000")
    family_net = position("adjusted_family_net_income: net_income 115000 = 115000", "115000")
    cwb_before_reduction = position(
        "cwb_before_reduction_without_dependant: 27% of working_income 110000 over 3000, "
        "at most 1633 (half-up to 0.01)",
        "1633",
    )
    cwb_reduction = position(
        "cwb_reduction_without_dependant: 15% of adjusted_family_net_income 115000 over 26855 "
        "(half-up to 0.01)",
        "13221.75",
    )
    cwb_without = position(
        "canada_workers_benefit_without_dependant: cwb_before_reduction_without_dependant 1633 "
        "less cwb_reduction_without_dependant 13221.75, not below 0 = 0",
        "0",
    )
    cwb_before_reduction_dependant = position(
        "cwb_before_reduction_with_dependant: 27% of working_income 110000 over 3000, "
        "at most 2813 (half-up to 0.01)",
        "2813",
    )
    cwb_reduction_dependant = position(
        "cwb_reduction_with_dependant: 15% of adjusted_family_net_income 115000 over 30639 "
        "(half-up to 0.01)",
        "12654.15",
    )
    cwb_with = position(
        "canada_workers_benefit_with_dependant: cwb_before_reduction_with_dependant 2813 "
        "less cwb_reduction_with_dependant 12654.15, not below 0 = 0",
        "0",
    )
    cwb = position(
        "canada_workers_benefit: canada_workers_benefit_without_dependant 0, "
        "chosen as cwb_eligible_dependants is 0",
        "0",
    )
    fertility_before_maximum = position(
        "fertility_credit_before_maximum: 25% of fertility_expenses 0 (half-up to 0.01)", "0"
    )
    fertility = position(
        "fertility_credit: lesser of fertility_credit_before_maximum 0 and 5000 (half-up to 0.01)",
        "0",
    )
    care_before_maximum = position(
        "seniors_care_before_maximum: 25% of medical_claim 0 (half-up to 0.01)", "0"
    )
    care_amount = position(
        "seniors_care_amount: lesser of seniors_care_before_maximum 0 and 1500 (half-up to 0.01)",
        "0",
    )
    care_family_net_income = position(
        "seniors_care_family_net_income: net_income 115000 + spouse_net_income 0 = 115000",
        "115000",
    )
    care_base = position("seniors_care_base_amount: credit amount 35000 (half-up to 0.01)", "35000")
    care_over_base = position(
        "seniors_care_income_over_base: seniors_care_family_net_income 115000 "
        "less seniors_care_base_amount 35000, not below 0 = 80000",
        "80000",
    )
    care_reduction = position(
        "seniors_care_reduction: 5% of seniors_care_income_over_base 80000 (half-up to 0.01)",
        "4000",
    )
    care_before_claim = position(
        "seniors_care_before_claim: seniors_care_amount 0 "
        "less seniors_care_reduction 4000, not below 0 = 0",
        "0",
    )
    care_credit = position(
        "seniors_care_credit: seniors_care_before_claim 0 "
        "for each of 0 claims_seniors_care_credit = 0",
        "0",
    )
    transit_paid = position(
        "seniors_transit_amount_paid_at_most_maximum: lesser of seniors_transit_paid 0 and 3000 "
        "(half-up to 0.01)",
        "0",
    )
    transit = position(
        "seniors_transit_credit: 15% of seniors_transit_amount_paid_at_most_maximum 0 "
        "(half-up to 0.01)",
        "0",
    )
    flow_through_expenses = position("flow_through_share_expenses: no items = 0", "0")
    flow_through = position(
        "flow_through_share_credit: 5% of flow_through_share_expenses 0 (half-up to 0.01)", "0"
    )
    ontario_credits_subtotal = position(
        "ontario_credits_subtotal: fertility_credit 0 + seniors_care_credit 0 "
        "+ seniors_transit_credit 0 + political_credit 0 + flow_through_share_credit 0 = 0",
        "0",
    )
    coop_threshold = position(
        "coop_education_payroll_threshold: credit amount 400000 (half-up to 0.01)", "400000"
    )
    coop_over_threshold = position(
        "coop_education_payroll_over_threshold: coop_education_payroll 0 "
        "less coop_education_payroll_threshold 400000, not below 0 = 0",
        "0",
    )
    coop_range = position(
        "coop_education_payroll_range: credit amount 200000 (half-up to 0.01)", "200000"
    )
    coop_phase_out = position(
        "coop_education_phase_out_share: coop_education_payroll_over_threshold 0 "
        "divided by coop_education_payroll_range 200000 = 0",
        "0",
    )
    coop_full_share = position("coop_education_full_share: credit amount 1 (half-up to 0.01)", "1")
    coop_remaining = position(
        "coop_education_remaining_share: coop_education_full_share 1 "
        "less coop_education_phase_out_share 0, not below 0 = 1",
        "1",
    )
    coop_credit = position("coop_education_credit: no items = 0", "0")
    coop_count = position(
        "coop_education_placement_count: no items in coop_education_placements = 0", "0"
    )
    ontario_credits = position(
        "ontario_credits: ontario_credits_subtotal 0 + coop_education_credit 0 = 0", "0"
    )
    provincial = position("provincial_credits: ontario_credits 0 = 0", "0")
    educator_expenses = position(
        "educator_supplies_expenses_at_most_maximum: lesser of educator_supplies_expenses 0 "
        "and 1000 (half-up to 0.01)",
        "0",
    )
    educator_credit = position(
        "educator_school_supply_credit: 25% of educator_supplies_expenses_at_most_maximum 0 "
        "(half-up to 0.01)",
        "0",
    )
    credits = position(
        "total_credits: income_tax_deducted 25000 + refundable_medical_expense_supplement 0 "
        "+ canada_workers_benefit 0 "
        "+ part_xii_2_tax_credit 0 + employee_and_partner_gst_hst_rebate 0 "
        "+ educator_school_supply_credit 0 + journalism_labour_tax_credit 0 "
        "+ tax_paid_by_instalments 0 + provincial_credits 0 = 25000",
        "25000",
    )
    balance = position(
        "refund_or_balance_owing: total_payable 25897.15 less total_credits 25000 = 897.15",
        "897.15",
    )
    refund = position(
        "refund: total_credits 25000 less total_payable 25897.15, not below 0 = 0", "0"
    )
    refund_before_donation = position("refund_before_donation: refund 0 = 0", "0")
    net_refund = position(
        "net_refund: refund_before_donation 0 less opportunities_fund_donation 0 = 0", "0"
    )
    # Schedule 9 and its charts, and the Federal Worksheet's line 34990, for donations of 0.
    depreciable_proceeds_or_cost = position(
        "depreciable_gift_proceeds_or_cost: lesser of depreciable_gift_net_proceeds 0 "
        "and depreciable_gift_capital_cost 0 = 0",
        "0",
    )
    depreciable_gifts = position(
        "depreciable_gifts: lesser of depreciable_gift_recaptured_depreciation 0 "
        "and depreciable_gift_proceeds_or_cost 0 = 0",
        "0",
    )
    capital_gifts = position(
        "capital_property_gifts: capital_gift_taxable_gains 0 "
        "less capital_gift_gains_deduction 0 = 0",
        "0",
    )
    donations_total = position(
        "total_charitable_donations: charitable_donations 0 + government_donations 0 "
        "+ university_donations_outside_canada 0 + foreign_charity_donations 0 = 0",
        "0",
    )
    limit_on_net_income = position(
        "donation_limit_on_net_income: 75% of net_income 115000 (half-up to 0.01)", "86250"
    )
    capital_gifts_total = position(
        "capital_gifts_total: depreciable_gifts 0 + capital_property_gifts 0 = 0", "0"
    )
    capital_gifts_addition = position(
        "capital_gifts_limit_addition: 25% of capital_gifts_total 0 (half-up to 0.01)", "0"
    )
    limit_with_gifts = position(
        "donation_limit_with_capital_gifts: donation_limit_on_net_income 86250 "
        "+ capital_gifts_limit_addition 0 = 86250",
        "86250",
    )
    donations_limit = position(
        "charitable_donations_limit: lesser of net_income 115000 "
        "and donation_limit_with_capital_gifts 86250 = 86250",
        "86250",
    )
    donations_claimed = position(
        "charitable_donations_claimed: lesser of total_charitable_donations 0 "
        "and charitable_donations_limit 86250 = 0",
        "0",
    )
    donations_and_gifts = position(
        "donations_and_gifts_total: charitable_donations_claimed 0 "
        "+ ecological_and_cultural_gifts 0 = 0",
        "0",
    )
    first_tier_maximum = position(
        "donation_first_tier_maximum: credit amount 200 (half-up to 0.01)", "200"
    )
    first_tier = position(
        "donations_first_tier: lesser of donations_and_gifts_total 0 "
        "and donation_first_tier_maximum 200 = 0",
        "0",
    )
    over_first_tier = position(
        "donations_over_first_tier: donations_and_gifts_total 0 less donations_first_tier 0 = 0",
        "0",
    )
    over_first_tier_after_2016 = position(
        "donations_over_first_tier_after_2016_gifts: donations_over_first_tier 0 "
        "less ecological_gifts_before_2016 0, not below 0 = 0",
        "0",
    )
    high_income_threshold = position(
        "donation_high_income_threshold: credit amount 253414 (half-up to 0.01)", "253414"
    )
    taxable_over_threshold = position(
        "taxable_income_over_donation_threshold: taxable_income 115000 "
        "less donation_high_income_threshold 253414, not below 0 = 0",
        "0",
    )
    high_income_donations = position(
        "high_income_donations: lesser of donations_over_first_tier_after_2016_gifts 0 "
        "and taxable_income_over_donation_threshold 0 = 0",
        "0",
    )
    high_income_credit = position(
        "high_income_donation_credit: 33% of high_income_donations 0 (half-up to 0.01)", "0"
    )
    regular_donations = position(
        "regular_rate_donations: donations_over_first_tier 0 less high_income_donations 0 = 0",
        "0",
    )
    regular_credit = position(
        "regular_rate_donation_credit: 29% of regular_rate_donations 0 (half-up to 0.01)", "0"
    )
    first_tier_credit = position(
        "first_tier_donation_credit: 14.5% of donations_first_tier 0 (half-up to 0.01)", "0"
    )
    donations_credit = position(
        "donations_and_gifts_credit: high_income_donation_credit 0 "
        "+ regular_rate_donation_credit 0 + first_tier_donation_credit 0 = 0",
        "0",
    )
    top_up_base = position(
        "top_up_credits_base: credit_amounts_at_credit_rate 3194.87 "
        "+ first_tier_donation_credit 0 = 3194.87",
        "3194.87",
    )
    top_up_threshold = position(
        "top_up_threshold: credit amount 8319.38 (half-up to 0.01)", "8319.38"
    )
    top_up_excess = position(
        "top_up_excess: top_up_credits_base 3194.87 less top_up_threshold 8319.38, not below 0 = 0",
        "0",
    )
    top_up_credit = position("top_up_tax_credit: 3.45% of top_up_excess 0 (half-up to 0.01)", "0")
    federal_credits = position(
        "non_refundable_tax_credits: credit_amounts_at_credit_rate 3194.87 "
        "+ donations_and_gifts_credit 0 + top_up_tax_credit 0 = 3194.87",
        "3194.87",
    )
    assert taxable_gains < total < net
    assert investment_before < interest < total
    assert support < total
    assert cpp_first < cpp_enhanced < deductions < net
    assert rrsp_available < rrsp_maximum < rrsp < deductions
    assert rrsp < rrsp_carried
    assert child_care_under_seven < child_care_basic
    assert child_care_disability < child_care_basic
    assert child_care_seven_to_sixteen < child_care_basic < child_care
    assert child_care_earned < child_care_earned_limit < child_care < deductions
    assert cpp_second < cpp_enhanced
    assert cpp_base < federal_amounts
    assert cpp_base < ontario_amounts
    assert ei < federal_amounts
    assert ei < ontario_amounts
    assert net < taxable
    # Line 9 feeds nothing yet: the count of line 9 over $93,454 is a starting count.
    assert net < line_5 < line_9
    assert support < after_limit < other_payments < net_deductions < taxable
    assert uccb_and_rdsp < line_5
    assert repayments < line_9
    assert support < after_limit
    assert taxable < federal_column < federal_basic < federal_after
    assert taxable < ontario_column < ontario_basic
    assert ontario_basic < ontario_after
    assert net < federal_amount < federal_amounts < federal_credit < federal_after
    assert depreciable_proceeds_or_cost < depreciable_gifts < capital_gifts_total
    assert capital_gifts < capital_gifts_total < capital_gifts_addition < limit_with_gifts
    assert net < limit_on_net_income < limit_with_gifts < donations_limit < donations_claimed
    assert donations_total < donations_claimed < donations_and_gifts
    assert first_tier_maximum < first_tier < over_first_tier < over_first_tier_after_2016
    assert donations_and_gifts < first_tier
    assert taxable < taxable_over_threshold
    assert high_income_threshold < taxable_over_threshold < high_income_donations
    assert over_first_tier_after_2016 < high_income_donations < high_income_credit
    assert high_income_donations < regular_donations < regular_credit
    assert first_tier < first_tier_credit
    assert high_income_credit < donations_credit
    assert regular_credit < donations_credit
    assert first_tier_credit < donations_credit < federal_credits
    assert federal_credit < top_up_base < top_up_excess < top_up_credit < federal_credits
    assert first_tier_credit < top_up_base
    assert top_up_threshold < top_up_excess
    assert federal_credit < federal_credits < federal_after
    assert employment_amount < federal_amounts
    assert federal_amount < federal_dependant < federal_dependant_claimed < federal_amounts
    assert federal_caregiver < federal_amounts
    assert disability_transfer < federal_amounts
    assert infirm_children < federal_amounts
    assert net < medical_share < medical_threshold < medical_over < medical_claim < federal_amounts
    assert other_medical < medical_claim
    assert net < ontario_medical_share < ontario_medical_threshold < ontario_medical_over
    assert ontario_medical_over < ontario_medical_claim < ontario_amounts
    assert ontario_other_medical < ontario_medical_claim
    assert net < age_over_threshold < age_reduction < age_before_count < age < federal_amounts
    assert age_threshold < age_over_threshold
    assert age_maximum < age_before_count
    assert federal_amount < spouse_basis < spouse_before_count < spouse < federal_amounts
    assert spouse_supplement < spouse_basis
    assert caregiver_base < caregiver_before_maximum < caregiver_limit < caregiver_before_count
    assert spouse < caregiver_before_count < caregiver < federal_amounts
    assert ontario_base < ontario_before_maximum < ontario_dependant
    assert ontario_dependant < ontario_dependant_claimed < ontario_caregiver < ontario_amounts
    assert net < ontario_age_over_threshold < ontario_age_reduction < ontario_age_before_count
    assert ontario_age_before_count < ontario_age < ontario_amounts
    assert ontario_age_threshold < ontario_age_over_threshold
    assert ontario_age_maximum < ontario_age_before_count
    assert ontario_spouse_base < ontario_spouse_before_maximum < ontario_spouse_before_count
    assert ontario_spouse_before_count < ontario_spouse < ontario_amounts
    assert ontario_amount < ontario_amounts < ontario_credit < ontario_line_50 < ontario_after
    assert first_tier < ontario_first_tier_credit < ontario_donations_credit < ontario_line_50
    assert over_first_tier < ontario_over_first_tier_credit < ontario_donations_credit
    assert ontario_after < surtax_first < surtax_second < with_surtax
    assert reduction_basic < reduction_amounts
    assert reduction_children < reduction_amounts
    assert reduction_dependants < reduction_amounts
    assert dividend_a < dividend_eligible < dividend_credit < line_70
    assert dividend_b < dividend_other < dividend_credit
    assert ontario_after < line_56 < line_58
    assert with_surtax < line_71 < reduction < after_reduction
    assert reduction_amounts < reduction
    assert taxable < premium_first < premium_second < premium_third < premium_fourth
    assert premium_fourth < premium_fifth < ontario_tax
    assert lift_before_maximum < lift_maximum < lift < after_lift < after_food < ontario_tax
    assert food_credit < after_food
    assert net < lift_reduction < lift
    assert after_reduction < after_lift
    assert federal_after < with_recapture < less_credits < net_federal < payable
    assert recapture_at_15 < recapture < with_recapture
    assert recapture_at_20 < recapture
    assert labour_before_maximum < labour_credit < federal_credits < less_credits
    assert aips_counted < aips_reduction < aips_subject < aips_part_a < aips_tax < special
    assert aips_limit < aips_remaining < aips_reduction
    assert aips_part_b < aips_tax
    assert special < net_federal
    assert ontario_tax < payable < balance
    assert working < cwb_before_reduction < cwb_without < cwb
    assert net < family_net < cwb_reduction < cwb_without
    assert working < cwb_before_reduction_dependant < cwb_with < cwb
    assert family_net < cwb_reduction_dependant < cwb_with
    assert fertility_before_maximum < fertility < ontario_credits_subtotal
    assert care_before_maximum < care_amount < care_before_claim < care_credit
    assert net < care_family_net_income < care_over_base < care_reduction < care_before_claim
    assert care_base < care_over_base
    assert care_credit < ontario_credits_subtotal
    assert transit_paid < transit < ontario_credits_subtotal
    assert flow_through_expenses < flow_through < ontario_credits_subtotal
    assert coop_threshold < coop_over_threshold < coop_phase_out < coop_remaining < coop_credit
    assert coop_range < coop_phase_out
    assert coop_full_share < coop_remaining
    assert coop_credit < ontario_credits
    assert coop_count != coop_credit
    assert ontario_credits_subtotal < ontario_credits < provincial < credits
    assert cwb < credits
    assert credits < balance
    assert educator_expenses < educator_credit < credits
    assert credits < refund < refund_before_donation < net_refund
    assert payable < refund


def test_the_trace_records_each_total_as_a_structured_line() -> None:
    trace = return_a().trace

    rated = {line.output: line for line in trace if isinstance(line, RateAppliedLine)}
    sums = {line.output: line for line in trace if isinstance(line, SumLine)}
    floored = {line.output: line for line in trace if isinstance(line, SubtractedNotBelowZeroLine)}
    subtracted = {line.output: line for line in trace if isinstance(line, SubtractedLine)}
    totals = {line.output: line for line in trace if isinstance(line, RoundedTotalLine)}
    amounts = {line.output: line for line in trace if isinstance(line, CreditAmountLine)}
    tapered = {line.output: line for line in trace if isinstance(line, TaperedAmountLine)}
    capped = {line.output: line for line in trace if isinstance(line, CappedAmountLine)}
    tiers = {line.output: line for line in trace if isinstance(line, ContributionTierLine)}
    lesser = {line.output: line for line in trace if isinstance(line, LesserOfLine)}
    at_most = {line.output: line for line in trace if isinstance(line, AtMostLine)}
    surcharged = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == ONTARIO_SURTAX
    ]
    lift_tiers = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == LIFT_REDUCTION
    ]
    premium_tiers = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine) and line.output == ONTARIO_HEALTH_PREMIUM
    ]
    cwb_basic_tiers = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine)
        and line.output
        in (CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT, CWB_BEFORE_REDUCTION_WITH_DEPENDANT)
    ]
    cwb_reduction_tiers = [
        line
        for line in trace
        if isinstance(line, SurchargeTierLine)
        and line.output in (CWB_REDUCTION_WITHOUT_DEPENDANT, CWB_REDUCTION_WITH_DEPENDANT)
    ]
    per_unit = {line.output: line for line in trace if isinstance(line, PerUnitAmountLine)}
    multiples = {line.output: line for line in trace if isinstance(line, MultipleOverLine)}
    times = {line.output: line for line in trace if isinstance(line, TimesCountLine)}
    gated = {line.output: line for line in trace if isinstance(line, ThresholdGateLine)}
    fractions = {line.output: line for line in trace if isinstance(line, FractionAppliedLine)}
    chosen = {line.output: line for line in trace if isinstance(line, ChosenByCountLine)}
    record_totals = {line.output: line for line in trace if isinstance(line, RecordTotalLine)}
    ranged = {line.output: line for line in trace if isinstance(line, ChosenByRangeLine)}
    quotients = {line.output: line for line in trace if isinstance(line, QuotientLine)}
    record_counts = {line.output: line for line in trace if isinstance(line, RecordCountLine)}
    placement_credits = [line for line in trace if isinstance(line, PlacementCreditLine)]
    items_totals = {
        line.output: line
        for line in trace
        if isinstance(line, ItemsTotalLine) and line.output is COOP_EDUCATION_CREDIT
    }

    # The rate is applied once, to each form's total of credit amounts (T1 line 33800, ON428
    # line 58840), giving each form's credit amounts at the credit rate (T1 line 35000 adds the
    # donations and gifts credit and the top-up tax credit to them; ON428 line 61500 adds the
    # donations and gifts credit of lines 47 to 49 to them).
    assert rated == {
        # T2038(IND) Part C amounts 1 and 2: the expenditures on lines 67193 and 67195 at 15% and
        # 20%, here 0.
        ITC_RECAPTURE_AT_15_PERCENT: RateAppliedLine(
            ITC_RECAPTURE_AT_15_PERCENT,
            ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT,
            D("0"),
            Rate(D("0.15")),
            CENT,
            D("0"),
        ),
        ITC_RECAPTURE_AT_20_PERCENT: RateAppliedLine(
            ITC_RECAPTURE_AT_20_PERCENT,
            ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT,
            D("0"),
            Rate(D("0.20")),
            CENT,
            D("0"),
        ),
        # Line 41400's "15% of the net cost reported on line 41300", before the maximum of $750.
        LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM: RateAppliedLine(
            LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
            LABOUR_SPONSORED_FUNDS_NET_COST,
            D("0"),
            Rate(D("0.15")),
            CENT,
            D("0"),
        ),
        # Form T1172 line 10 (line 8 x 20%, Part A) and line 13 (line 11 x 20%, Part B).
        RESP_AIPS_PART_A_TAX: RateAppliedLine(
            RESP_AIPS_PART_A_TAX,
            RESP_AIPS_SUBJECT_TO_TAX,
            D("0"),
            Rate(D("0.20")),
            CENT,
            D("0"),
        ),
        RESP_AIPS_PART_B_TAX: RateAppliedLine(
            RESP_AIPS_PART_B_TAX,
            RESP_AIPS_RECEIVED_PART_B,
            D("0"),
            Rate(D("0.20")),
            CENT,
            D("0"),
        ),
        # The Federal Worksheet's "Line 40425" line 6 (line B x 9.0301%) and line 7 (line C x
        # 15.0198%), on no dividends with no slip.
        OTHER_DIVIDENDS_CREDIT: RateAppliedLine(
            OTHER_DIVIDENDS_CREDIT,
            DIVIDENDS_AMOUNT_B,
            D("0"),
            Rate(D("0.090301")),
            CENT,
            D("0"),
        ),
        ELIGIBLE_DIVIDENDS_CREDIT: RateAppliedLine(
            ELIGIBLE_DIVIDENDS_CREDIT,
            DIVIDENDS_AMOUNT_A_LESS_B,
            D("0"),
            Rate(D("0.150198")),
            CENT,
            D("0"),
        ),
        # Worksheet ON428's "Line 61520" line 1 (line B x 2.9863%) and line 2 (line C x 10%), on
        # no dividends.
        ontario.OTHER_DIVIDENDS_CREDIT: RateAppliedLine(
            ontario.OTHER_DIVIDENDS_CREDIT,
            ontario.DIVIDENDS_AMOUNT_B,
            D("0"),
            Rate(D("0.029863")),
            CENT,
            D("0"),
        ),
        ontario.ELIGIBLE_DIVIDENDS_CREDIT: RateAppliedLine(
            ontario.ELIGIBLE_DIVIDENDS_CREDIT,
            ontario.DIVIDENDS_AMOUNT_A_LESS_B,
            D("0"),
            Rate(D("0.1")),
            CENT,
            D("0"),
        ),
        TAXABLE_CAPITAL_GAINS: RateAppliedLine(
            TAXABLE_CAPITAL_GAINS, CAPITAL_GAIN, D("20000"), Rate(D("0.5")), CENT, D("10000")
        ),
        CREDIT_AMOUNTS_AT_CREDIT_RATE: RateAppliedLine(
            CREDIT_AMOUNTS_AT_CREDIT_RATE,
            NON_REFUNDABLE_CREDIT_AMOUNTS,
            D("22033.58"),
            Rate(D("0.145")),
            CENT,
            D("3194.87"),
        ),
        # Schedule 9 line 6 "Enter your net income from line 23600 of your return. Line A"
        # "multiplied by 75%", line 7 "Amount B plus amount C Line D" "multiplied by 25%", line 20
        # "Line F" "multiplied by 33%", line 21 "Line G" "multiplied by 29%" and line 22 "Line H"
        # "multiplied by 14.5%": Return A has donations of 0, so every line but line 6 is 0.
        DONATION_LIMIT_ON_NET_INCOME: RateAppliedLine(
            DONATION_LIMIT_ON_NET_INCOME, NET_INCOME, D("115000"), Rate(D("0.75")), CENT, D("86250")
        ),
        # T1 line 108 "Amount from line 23600 multiplied by 3%".
        MEDICAL_NET_INCOME_SHARE: RateAppliedLine(
            MEDICAL_NET_INCOME_SHARE, NET_INCOME, D("115000"), Rate(D("0.03")), CENT, D("3450.00")
        ),
        # ON428 line 39 "Line 37 multiplied by the percentage from line 38".
        ontario.MEDICAL_NET_INCOME_SHARE: RateAppliedLine(
            ontario.MEDICAL_NET_INCOME_SHARE,
            NET_INCOME,
            D("115000"),
            Rate(D("0.03")),
            CENT,
            D("3450.00"),
        ),
        CAPITAL_GIFTS_LIMIT_ADDITION: RateAppliedLine(
            CAPITAL_GIFTS_LIMIT_ADDITION,
            CAPITAL_GIFTS_TOTAL,
            D("0"),
            Rate(D("0.25")),
            CENT,
            D("0.00"),
        ),
        HIGH_INCOME_DONATION_CREDIT: RateAppliedLine(
            HIGH_INCOME_DONATION_CREDIT,
            HIGH_INCOME_DONATIONS,
            D("0"),
            Rate(D("0.33")),
            CENT,
            D("0.00"),
        ),
        REGULAR_RATE_DONATION_CREDIT: RateAppliedLine(
            REGULAR_RATE_DONATION_CREDIT,
            REGULAR_RATE_DONATIONS,
            D("0"),
            Rate(D("0.29")),
            CENT,
            D("0.00"),
        ),
        FIRST_TIER_DONATION_CREDIT: RateAppliedLine(
            FIRST_TIER_DONATION_CREDIT,
            DONATIONS_FIRST_TIER,
            D("0"),
            Rate(D("0.145")),
            CENT,
            D("0.00"),
        ),
        # Federal Worksheet line 6 "Applicable rate 3.45%" and line 7 "Line 5 multiplied by the
        # percentage from line 6": line 5 is 0.
        TOP_UP_TAX_CREDIT: RateAppliedLine(
            TOP_UP_TAX_CREDIT, TOP_UP_EXCESS, D("0"), Rate(D("0.0345")), CENT, D("0.00")
        ),
        ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE: RateAppliedLine(
            ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE,
            ontario.NON_REFUNDABLE_CREDIT_AMOUNTS,
            D("17180.58"),
            Rate(D("0.0505")),
            CENT,
            D("867.62"),
        ),
        # ON428 line 47 "Amount from line 13 of your federal Schedule 9" "multiplied by 5.05%" and
        # line 48 "Amount from line 14 of your federal Schedule 9" "multiplied by 11.16%": lines
        # 13 and 14 are 0.
        ontario.DONATIONS_FIRST_TIER_CREDIT: RateAppliedLine(
            ontario.DONATIONS_FIRST_TIER_CREDIT,
            DONATIONS_FIRST_TIER,
            D("0"),
            Rate(D("0.0505")),
            CENT,
            D("0.00"),
        ),
        ontario.DONATIONS_OVER_FIRST_TIER_CREDIT: RateAppliedLine(
            ontario.DONATIONS_OVER_FIRST_TIER_CREDIT,
            DONATIONS_OVER_FIRST_TIER,
            D("0"),
            Rate(D("0.1116")),
            CENT,
            D("0.00"),
        ),
        # ON479 line 1 "Eligible medical expenses for fertility treatment multiplied by 25%
        # (maximum $5,000)", before its maximum: no expenses.
        FERTILITY_CREDIT_BEFORE_MAXIMUM: RateAppliedLine(
            FERTILITY_CREDIT_BEFORE_MAXIMUM,
            FERTILITY_EXPENSES,
            D("0"),
            Rate(D("0.25")),
            CENT,
            D("0"),
        ),
        # ON479 line 4 "Allowable percentage 25%" and line 5 "Line 3 multiplied by the percentage
        # from line 4", before its maximum: line 3 is ON428 line 58769, 0 for Return A.
        SENIORS_CARE_BEFORE_MAXIMUM: RateAppliedLine(
            SENIORS_CARE_BEFORE_MAXIMUM,
            ontario.MEDICAL_CLAIM,
            D("0"),
            Rate(D("0.25")),
            CENT,
            D("0"),
        ),
        # ON479 line 11 "Applicable rate 5%" and line 12 "Line 10 multiplied by the percentage from
        # line 11": 5% of 115000.00 - 35000.00 = 80000.00.
        SENIORS_CARE_REDUCTION: RateAppliedLine(
            SENIORS_CARE_REDUCTION,
            SENIORS_CARE_INCOME_OVER_BASE,
            D("80000.00"),
            Rate(D("0.05")),
            CENT,
            D("4000.00"),
        ),
        # T1 line 161 (line 46900) "multiplied by 25%", on the supplies expenses after their
        # maximum of $1,000.
        EDUCATOR_SCHOOL_SUPPLY_CREDIT: RateAppliedLine(
            EDUCATOR_SCHOOL_SUPPLY_CREDIT,
            EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
            D("0"),
            Rate(D("0.25")),
            CENT,
            D("0"),
        ),
        # ON479 line 14 "multiplied by 15%", on the amount paid after its maximum of $3,000.
        SENIORS_TRANSIT_CREDIT: RateAppliedLine(
            SENIORS_TRANSIT_CREDIT,
            SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
            D("0"),
            Rate(D("0.15")),
            CENT,
            D("0"),
        ),
        # Federal Worksheet line 5 "Applicable rate 15%" and line 6 "Line 4 multiplied by the
        # percentage from line 5": line 4 is the net income 115000 over the income threshold.
        AGE_REDUCTION: RateAppliedLine(
            AGE_REDUCTION,
            AGE_INCOME_OVER_THRESHOLD,
            D("69478.00"),
            Rate(D("0.15")),
            CENT,
            D("10421.70"),
        ),
        # Worksheet ON479 column 1 line 5 "Line 3 multiplied by the percentage from line 4":
        # line 3 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_1_LINE_5: RateAppliedLine(
            ontario.POLITICAL_CREDIT_COLUMN_1_LINE_5,
            ontario.POLITICAL_CREDIT_COLUMN_1_LINE_3,
            D("0"),
            Rate(D("0.75")),
            CENT,
            D("0.00"),
        ),
        # Worksheet ON479 column 2 line 5 "Line 3 multiplied by the percentage from line 4":
        # line 3 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_2_LINE_5: RateAppliedLine(
            ontario.POLITICAL_CREDIT_COLUMN_2_LINE_5,
            ontario.POLITICAL_CREDIT_COLUMN_2_LINE_3,
            D("0"),
            Rate(D("0.5")),
            CENT,
            D("0.00"),
        ),
        # Worksheet ON479 column 3 line 5 "Line 3 multiplied by the percentage from line 4":
        # line 3 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_3_LINE_5: RateAppliedLine(
            ontario.POLITICAL_CREDIT_COLUMN_3_LINE_5,
            ontario.POLITICAL_CREDIT_COLUMN_3_LINE_3,
            D("0"),
            Rate(D("0.3333")),
            CENT,
            D("0.00"),
        ),
        # Federal Worksheet column 1 line 5 "Line 3 multiplied by the percentage from line 4 =":
        # line 3 is 0.
        POLITICAL_CREDIT_COLUMN_1_LINE_5: RateAppliedLine(
            POLITICAL_CREDIT_COLUMN_1_LINE_5,
            POLITICAL_CREDIT_COLUMN_1_LINE_3,
            D("0"),
            Rate(D("0.75")),
            CENT,
            D("0.00"),
        ),
        # Federal Worksheet column 2 line 5 "Line 3 multiplied by the percentage from line 4 =":
        # line 3 is 0.
        POLITICAL_CREDIT_COLUMN_2_LINE_5: RateAppliedLine(
            POLITICAL_CREDIT_COLUMN_2_LINE_5,
            POLITICAL_CREDIT_COLUMN_2_LINE_3,
            D("0"),
            Rate(D("0.5")),
            CENT,
            D("0.00"),
        ),
        # Federal Worksheet column 3 line 5 "Line 3 multiplied by the percentage from line 4 =":
        # line 3 is 0.
        POLITICAL_CREDIT_COLUMN_3_LINE_5: RateAppliedLine(
            POLITICAL_CREDIT_COLUMN_3_LINE_5,
            POLITICAL_CREDIT_COLUMN_3_LINE_3,
            D("0"),
            Rate(D("0.3333")),
            CENT,
            D("0.00"),
        ),
        # ON479 line 17 and line 63220 "multiplied by 5%", on Form T1221 line 4: no slips, 0.
        FLOW_THROUGH_SHARE_CREDIT: RateAppliedLine(
            FLOW_THROUGH_SHARE_CREDIT,
            FLOW_THROUGH_SHARE_EXPENSES,
            D("0"),
            Rate(D("0.05")),
            CENT,
            D("0"),
        ),
        # Worksheet ON428 line 5 "Applicable rate 15%" and line 6 "Line 4 multiplied by the
        # percentage from line 5": line 4 is the net income 115000 over the income threshold.
        ontario.AGE_REDUCTION: RateAppliedLine(
            ontario.AGE_REDUCTION,
            ontario.AGE_INCOME_OVER_THRESHOLD,
            D("68670.00"),
            Rate(D("0.15")),
            CENT,
            D("10300.50"),
        ),
        # ON428 line 87 and line 62150 "multiplied by 25%": the qualifying donations of 0.
        COMMUNITY_FOOD_PROGRAM_CREDIT: RateAppliedLine(
            COMMUNITY_FOOD_PROGRAM_CREDIT,
            COMMUNITY_FOOD_PROGRAM_DONATIONS,
            D("0"),
            Rate(D("0.25")),
            CENT,
            D("0.00"),
        ),
        # Schedule ON428-A line 5 "Line 3 multiplied by the percentage from line 4 (maximum
        # $875)", before its maximum: line 3 is employment income (line 10100), as line 2 (line
        # 10400) is not triggered.
        LIFT_CREDIT_BEFORE_MAXIMUM: RateAppliedLine(
            LIFT_CREDIT_BEFORE_MAXIMUM,
            EMPLOYMENT_INCOME,
            D("110000"),
            Rate(D("0.0505")),
            CENT,
            D("5555.00"),
        ),
        # Form T1436 line 20 (T1 line 21700).
        ALLOWABLE_BUSINESS_INVESTMENT_LOSS: RateAppliedLine(
            ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
            BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
            D("0"),
            Rate(D("0.5")),
            CENT,
            D("0.00"),
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_LINE_13: RateAppliedLine(
            output=MEDICAL_SUPPLEMENT_LINE_13,
            base=MEDICAL_SUPPLEMENT_LINE_11,
            base_amount=D("0"),
            rate=Rate(D("0.25")),
            rounding=CENT,
            result=D("0.00"),
        ),
        MEDICAL_SUPPLEMENT_LINE_15: RateAppliedLine(
            output=MEDICAL_SUPPLEMENT_LINE_15,
            base=MEDICAL_SUPPLEMENT_LINE_8,
            base_amount=D("81706.00"),
            rate=Rate(D("0.05")),
            rounding=CENT,
            result=D("4085.30"),
        ),
    }
    assert sums == {
        # The Federal Worksheet's "Lines 12000 and 12010" lines 5 and 10, line 17 and, with the
        # slip amounts, lines 12010 and 12000: no dividends, so every line is 0.
        SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE: SumLine(
            SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            (
                (T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D("0")),
                (T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D("0")),
                (T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D("0")),
                (T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D("0")),
            ),
            D("0"),
        ),
        SLIP_TAXABLE_DIVIDENDS: SumLine(
            SLIP_TAXABLE_DIVIDENDS,
            (
                (T3_TAXABLE_DIVIDENDS, D("0")),
                (T4PS_TAXABLE_DIVIDENDS, D("0")),
                (T5_TAXABLE_DIVIDENDS, D("0")),
                (T5013_TAXABLE_DIVIDENDS, D("0")),
            ),
            D("0"),
        ),
        DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP: SumLine(
            DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
            (
                (ELIGIBLE_DIVIDENDS_GROSSED_UP, D("0")),
                (OTHER_DIVIDENDS_GROSSED_UP, D("0")),
            ),
            D("0"),
        ),
        TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE: SumLine(
            TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            (
                (SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D("0")),
                (OTHER_DIVIDENDS_GROSSED_UP, D("0")),
            ),
            D("0"),
        ),
        TAXABLE_DIVIDENDS: SumLine(
            TAXABLE_DIVIDENDS,
            (
                (SLIP_TAXABLE_DIVIDENDS, D("0")),
                (DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP, D("0")),
            ),
            D("0"),
        ),
        # The Federal Worksheet's "Line 40425 - Federal dividend tax credit" lines 5, A, B, 8 and
        # 9 and T1 line 125 "Add lines 122 to 124.": lines A and B are each one part.
        SLIP_DIVIDEND_TAX_CREDIT: SumLine(
            SLIP_DIVIDEND_TAX_CREDIT,
            (
                (T3_DIVIDEND_TAX_CREDIT, D("0")),
                (T4PS_DIVIDEND_TAX_CREDIT, D("0")),
                (T5_DIVIDEND_TAX_CREDIT, D("0")),
                (T5013_DIVIDEND_TAX_CREDIT, D("0")),
            ),
            D("0"),
        ),
        DIVIDENDS_AMOUNT_A: SumLine(
            DIVIDENDS_AMOUNT_A,
            ((DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP, D("0")),),
            D("0"),
        ),
        DIVIDENDS_AMOUNT_B: SumLine(
            DIVIDENDS_AMOUNT_B,
            ((OTHER_DIVIDENDS_GROSSED_UP, D("0")),),
            D("0"),
        ),
        NO_SLIP_DIVIDEND_TAX_CREDIT: SumLine(
            NO_SLIP_DIVIDEND_TAX_CREDIT,
            (
                (OTHER_DIVIDENDS_CREDIT, D("0")),
                (ELIGIBLE_DIVIDENDS_CREDIT, D("0")),
            ),
            D("0"),
        ),
        DIVIDEND_TAX_CREDIT: SumLine(
            DIVIDEND_TAX_CREDIT,
            (
                (SLIP_DIVIDEND_TAX_CREDIT, D("0")),
                (NO_SLIP_DIVIDEND_TAX_CREDIT, D("0")),
            ),
            D("0"),
        ),
        CREDITS_AGAINST_BASIC_FEDERAL_TAX: SumLine(
            CREDITS_AGAINST_BASIC_FEDERAL_TAX,
            ((NON_REFUNDABLE_TAX_CREDITS, D("3194.87")), (DIVIDEND_TAX_CREDIT, D("0"))),
            D("3194.87"),
        ),
        # T1 line 15000 "Line 28 plus line 32 Total income": the income lines, in line order.
        TOTAL_INCOME: SumLine(
            TOTAL_INCOME,
            (
                (EMPLOYMENT_INCOME, D("110000")),
                (OTHER_EMPLOYMENT_INCOME, D("0")),
                (OLD_AGE_SECURITY, D("0")),
                (CPP_OR_QPP_BENEFITS, D("0")),
                (OTHER_PENSIONS_AND_SUPERANNUATION, D("0")),
                (ELECTED_SPLIT_PENSION_AMOUNT, D("0")),
                (UNIVERSAL_CHILD_CARE_BENEFIT, D("0")),
                (EI_AND_OTHER_BENEFITS, D("0")),
                (TAXABLE_DIVIDENDS, D("0")),
                (INTEREST_AND_OTHER_INVESTMENT_INCOME, D("0")),
                (NET_PARTNERSHIP_INCOME, D("0")),
                (RDSP_INCOME, D("0")),
                (TAXABLE_CAPITAL_GAINS, D("10000")),
                (TAXABLE_SUPPORT_PAYMENTS, D("0")),
                (RRSP_INCOME, D("0")),
                (FHSA_INCOME, D("0")),
                (OTHER_FHSA_INCOME, D("0")),
                (OTHER_INCOME, D("0")),
                (TAXABLE_SCHOLARSHIPS, D("0")),
                (INCOME_SUPPORT_BENEFITS, D("0")),
            ),
            D("120000"),
        ),
        # The Federal Worksheet's "Line 12100 - Interest and other investment income" line 9
        # "Add lines 1 to 8.", and T1 line 14700 "Add lines 29 to 31", each in line order.
        INVESTMENT_INCOME_BEFORE_PRIOR_YEARS: SumLine(
            INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
            (
                (T3_INVESTMENT_INCOME, D("0")),
                (T5_INVESTMENT_INCOME, D("0")),
                (T5013_INVESTMENT_INCOME, D("0")),
                (INVESTMENT_INCOME_CREDITED_NOT_RECEIVED, D("0")),
                (TAX_REFUND_INTEREST, D("0")),
                (FOREIGN_INVESTMENT_INCOME, D("0")),
                (INVESTMENT_INCOME_WITHOUT_A_SLIP, D("0")),
                (INVESTMENT_ROYALTIES, D("0")),
            ),
            D("0"),
        ),
        INCOME_SUPPORT_BENEFITS: SumLine(
            INCOME_SUPPORT_BENEFITS,
            (
                (WORKERS_COMPENSATION_BENEFITS, D("0")),
                (SOCIAL_ASSISTANCE_PAYMENTS, D("0")),
                (NET_FEDERAL_SUPPLEMENTS, D("0")),
            ),
            D("0"),
        ),
        # Schedule 8 Part 3a line 28 "Line 26 plus line 27", to T1 line 22215.
        CPP_ENHANCED_CONTRIBUTIONS: SumLine(
            CPP_ENHANCED_CONTRIBUTIONS,
            (
                (CPP_FIRST_ADDITIONAL_CONTRIBUTIONS, D("678.00")),
                (CPP_SECOND_ADDITIONAL_CONTRIBUTIONS, D("396.00")),
            ),
            D("1074.00"),
        ),
        # Schedule 7 line 5 "Line 1 plus line 4 ... Total contributions", to line 10
        # "Contributions available to deduct" with no HBP or LLP repayments (line 9).
        RRSP_CONTRIBUTIONS_AVAILABLE: SumLine(
            RRSP_CONTRIBUTIONS_AVAILABLE,
            ((UNUSED_RRSP_CONTRIBUTIONS, D("0")), (RRSP_CONTRIBUTIONS, D("1926"))),
            D("1926"),
        ),
        # Form T778 line 4 "Add lines 1 to 3.", and line 6's earned income, the employment
        # income.
        CHILD_CARE_BASIC_LIMIT: SumLine(
            CHILD_CARE_BASIC_LIMIT,
            (
                (CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN, D("0")),
                (CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY, D("0")),
                (CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN, D("0")),
            ),
            D("0"),
        ),
        CHILD_CARE_EARNED_INCOME: SumLine(
            CHILD_CARE_EARNED_INCOME, ((EMPLOYMENT_INCOME, D("110000")),), D("110000")
        ),
        # T1 line 23300, in line order: 20700, 20800, 20805, 21000, 21200, 21300, 21400, 21700,
        # 22000, 22100, 22215, 22400, 23200.
        DEDUCTIONS_FROM_TOTAL_INCOME: SumLine(
            DEDUCTIONS_FROM_TOTAL_INCOME,
            (
                (RPP_DEDUCTION, D("0")),
                (RRSP_DEDUCTION, D("1926")),
                (FHSA_DEDUCTION, D("0")),
                (ELECTED_SPLIT_PENSION_DEDUCTION, D("0")),
                (UNION_DUES, D("2000")),
                (UCCB_REPAYMENT, D("0")),
                (CHILD_CARE_EXPENSES, D("0")),
                (ALLOWABLE_BUSINESS_INVESTMENT_LOSS, D("0")),
                (SUPPORT_PAYMENTS_DEDUCTION, D("0")),
                (CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES, D("0")),
                (CPP_ENHANCED_CONTRIBUTIONS, D("1074.00")),
                (EXPLORATION_AND_DEVELOPMENT_EXPENSES, D("0")),
                (OTHER_DEDUCTIONS, D("0")),
            ),
            D("5000"),
        ),
        # The Federal Worksheet's "Line 25000 - Other payments deduction" lines 4, 8 and 9, each
        # in line order.
        UCCB_AND_RDSP_INCOME: SumLine(
            UCCB_AND_RDSP_INCOME,
            ((UNIVERSAL_CHILD_CARE_BENEFIT, D("0")), (RDSP_INCOME, D("0"))),
            D("0"),
        ),
        UCCB_AND_RDSP_INCOME_REPAYMENTS: SumLine(
            UCCB_AND_RDSP_INCOME_REPAYMENTS,
            ((UCCB_REPAYMENT, D("0")), (RDSP_INCOME_REPAYMENT, D("0"))),
            D("0"),
        ),
        OTHER_PAYMENTS_LIMIT_INCOME: SumLine(
            OTHER_PAYMENTS_LIMIT_INCOME,
            (
                (NET_INCOME_LESS_UCCB_AND_RDSP_INCOME, D("115000")),
                (UCCB_AND_RDSP_INCOME_REPAYMENTS, D("0")),
            ),
            D("115000"),
        ),
        # T1 line 68 and line 25700 "Add lines 58 to 67.", in line order, line 63 (25300) included.
        DEDUCTIONS_FROM_NET_INCOME: SumLine(
            DEDUCTIONS_FROM_NET_INCOME,
            (
                (CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION, D("0")),
                (SECURITY_OPTIONS_DEDUCTIONS, D("0")),
                (OTHER_PAYMENTS_DEDUCTION, D("0")),
                (LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS, D("0")),
                (NON_CAPITAL_LOSSES_OF_OTHER_YEARS, D("0")),
                (NET_CAPITAL_LOSSES_OF_OTHER_YEARS, D("0")),
                (ADDITIONAL_DEDUCTIONS, D("0")),
            ),
            D("0"),
        ),
        # T1 line 118 (line 35000) "Add lines 115 to 117. Total federal non-refundable tax credits":
        # line 115 (line 33800), line 116 (line 34900) and line 117 (line 34990), in line order.
        NON_REFUNDABLE_TAX_CREDITS: SumLine(
            NON_REFUNDABLE_TAX_CREDITS,
            (
                (CREDIT_AMOUNTS_AT_CREDIT_RATE, D("3194.87")),
                (DONATIONS_AND_GIFTS_CREDIT, D("0.00")),
                (TOP_UP_TAX_CREDIT, D("0.00")),
            ),
            D("3194.87"),
        ),
        # ON428 line 49 and line 58969 "Line 47 plus line 48", and line 50 and line 61500 "Line 46
        # plus line 49 Enter this amount on line 52. Ontario non-refundable tax credits".
        ontario.DONATIONS_AND_GIFTS_CREDIT: SumLine(
            ontario.DONATIONS_AND_GIFTS_CREDIT,
            (
                (ontario.DONATIONS_FIRST_TIER_CREDIT, D("0.00")),
                (ontario.DONATIONS_OVER_FIRST_TIER_CREDIT, D("0.00")),
            ),
            D("0.00"),
        ),
        ontario.NON_REFUNDABLE_TAX_CREDITS: SumLine(
            ontario.NON_REFUNDABLE_TAX_CREDITS,
            (
                (ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE, D("867.62")),
                (ontario.DONATIONS_AND_GIFTS_CREDIT, D("0.00")),
            ),
            D("867.62"),
        ),
        # Schedule 9 line 5 "Add lines 1 to 4.", line 7 "Amount B plus amount C Line D", line 8
        # "Line 6 plus line 7", line 12 "Line 10 plus line 11" and line 23 "Add lines 20 to 22.".
        TOTAL_CHARITABLE_DONATIONS: SumLine(
            TOTAL_CHARITABLE_DONATIONS,
            (
                (CHARITABLE_DONATIONS, D("0")),
                (GOVERNMENT_DONATIONS, D("0")),
                (UNIVERSITY_DONATIONS_OUTSIDE_CANADA, D("0")),
                (FOREIGN_CHARITY_DONATIONS, D("0")),
            ),
            D("0"),
        ),
        CAPITAL_GIFTS_TOTAL: SumLine(
            CAPITAL_GIFTS_TOTAL,
            ((DEPRECIABLE_GIFTS, D("0")), (CAPITAL_PROPERTY_GIFTS, D("0"))),
            D("0"),
        ),
        # T1 line 112 "Line 110 plus line 111".
        MEDICAL_CLAIM: SumLine(
            MEDICAL_CLAIM,
            (
                (MEDICAL_EXPENSES_OVER_THRESHOLD, D("0")),
                (OTHER_DEPENDANTS_MEDICAL, D("0")),
            ),
            D("0"),
        ),
        # ON428 line 43 and line 58769 "Line 41 plus line 42".
        ontario.MEDICAL_CLAIM: SumLine(
            ontario.MEDICAL_CLAIM,
            (
                (ontario.MEDICAL_EXPENSES_OVER_THRESHOLD, D("0")),
                (ontario.OTHER_DEPENDANTS_MEDICAL, D("0")),
            ),
            D("0"),
        ),
        DONATION_LIMIT_WITH_CAPITAL_GIFTS: SumLine(
            DONATION_LIMIT_WITH_CAPITAL_GIFTS,
            (
                (DONATION_LIMIT_ON_NET_INCOME, D("86250")),
                (CAPITAL_GIFTS_LIMIT_ADDITION, D("0.00")),
            ),
            D("86250"),
        ),
        DONATIONS_AND_GIFTS_TOTAL: SumLine(
            DONATIONS_AND_GIFTS_TOTAL,
            ((CHARITABLE_DONATIONS_CLAIMED, D("0")), (ECOLOGICAL_AND_CULTURAL_GIFTS, D("0"))),
            D("0"),
        ),
        DONATIONS_AND_GIFTS_CREDIT: SumLine(
            DONATIONS_AND_GIFTS_CREDIT,
            (
                (HIGH_INCOME_DONATION_CREDIT, D("0.00")),
                (REGULAR_RATE_DONATION_CREDIT, D("0.00")),
                (FIRST_TIER_DONATION_CREDIT, D("0.00")),
            ),
            D("0.00"),
        ),
        # Federal Worksheet line 3 "Line 1 plus line 2": line 33800 and Schedule 9 line 22.
        TOP_UP_CREDITS_BASE: SumLine(
            TOP_UP_CREDITS_BASE,
            (
                (CREDIT_AMOUNTS_AT_CREDIT_RATE, D("3194.87")),
                (FIRST_TIER_DONATION_CREDIT, D("0.00")),
            ),
            D("3194.87"),
        ),
        NON_REFUNDABLE_CREDIT_AMOUNTS: SumLine(
            NON_REFUNDABLE_CREDIT_AMOUNTS,
            (
                (BASIC_PERSONAL_AMOUNT, D("16129")),
                (AGE_AMOUNT, D("0")),
                (SPOUSE_AMOUNT, D("0")),
                (ELIGIBLE_DEPENDANT_AMOUNT, D("0")),
                (SPOUSE_CAREGIVER_AMOUNT, D("0")),
                (CAREGIVER_AMOUNT, D("0")),
                (INFIRM_CHILDREN_AMOUNT, D("0")),
                (CPP_BASE_CONTRIBUTIONS, D("3356.10")),
                (EI_PREMIUMS, D("1077.48")),
                (CANADA_EMPLOYMENT_AMOUNT, D("1471")),
                (DISABILITY_TRANSFERRED_AMOUNT, D("0")),
                (MEDICAL_CLAIM, D("0")),
            ),
            D("22033.58"),
        ),
        # Schedule 5 (5000-S5) line 3 "Line 1 plus line 2": the basic personal amount plus the
        # amount for a spouse eligible for the Canada caregiver amount, here none.
        SPOUSE_AMOUNT_BASIS: SumLine(
            SPOUSE_AMOUNT_BASIS,
            (
                (BASIC_PERSONAL_AMOUNT, D("16129.00")),
                (SPOUSE_INFIRMITY_SUPPLEMENT, D("0")),
            ),
            D("16129.00"),
        ),
        # ON428 has no Canada employment amount; its lines 58240 and 58300 read the federal
        # amounts (lines 30800 and 31200).
        ontario.NON_REFUNDABLE_CREDIT_AMOUNTS: SumLine(
            ontario.NON_REFUNDABLE_CREDIT_AMOUNTS,
            (
                (ontario.BASIC_PERSONAL_AMOUNT, D("12747")),
                (ontario.AGE_AMOUNT, D("0")),
                (ontario.SPOUSE_AMOUNT, D("0")),
                (ontario.ELIGIBLE_DEPENDANT_AMOUNT, D("0")),
                (ontario.CAREGIVER_AMOUNT, D("0")),
                (CPP_BASE_CONTRIBUTIONS, D("3356.10")),
                (EI_PREMIUMS, D("1077.48")),
                (ontario.MEDICAL_CLAIM, D("0")),
            ),
            D("17180.58"),
        ),
        # Worksheet ON428's "Line 61520" lines A and B (whole lines 12000 and 12010) and line 3
        # "Line 1 plus line 2", and ON428 lines 56 "Enter the amount from line 53 above." and 70
        # "Ontario dividend tax credit from line 57": each of A, B, 56 and 70 is one part.
        ontario.DIVIDENDS_AMOUNT_A: SumLine(
            ontario.DIVIDENDS_AMOUNT_A, ((TAXABLE_DIVIDENDS, D("0")),), D("0")
        ),
        ontario.DIVIDENDS_AMOUNT_B: SumLine(
            ontario.DIVIDENDS_AMOUNT_B,
            ((TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, D("0")),),
            D("0"),
        ),
        ontario.DIVIDEND_TAX_CREDIT: SumLine(
            ontario.DIVIDEND_TAX_CREDIT,
            ((ontario.OTHER_DIVIDENDS_CREDIT, D("0")), (ontario.ELIGIBLE_DIVIDENDS_CREDIT, D("0"))),
            D("0"),
        ),
        ontario.ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT: SumLine(
            ontario.ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT,
            ((ONTARIO_TAX_AFTER_CREDITS, D("7671.98")),),
            D("7671.98"),
        ),
        ontario.DIVIDEND_CREDIT_FROM_LINE_57: SumLine(
            ontario.DIVIDEND_CREDIT_FROM_LINE_57,
            ((ontario.DIVIDEND_TAX_CREDIT, D("0")),),
            D("0"),
        ),
        # ON428 line 69 "Line 62 plus line 68": the Ontario tax after credits plus the surtax.
        ONTARIO_TAX_WITH_SURTAX: SumLine(
            ONTARIO_TAX_WITH_SURTAX,
            ((ONTARIO_TAX_AFTER_CREDITS, D("7671.98")), (ONTARIO_SURTAX, D("523.79"))),
            D("8195.77"),
        ),
        # ON428 line 77 "Add lines 74 to 76.", in line order.
        TAX_REDUCTION_AMOUNTS: SumLine(
            TAX_REDUCTION_AMOUNTS,
            (
                (TAX_REDUCTION_BASIC, D("294.00")),
                (TAX_REDUCTION_FOR_CHILDREN, D("0")),
                (TAX_REDUCTION_FOR_DEPENDANTS, D("0")),
            ),
            D("294.00"),
        ),
        # ON428 line 90 "Line 88 plus line 89 Enter this amount on line 42800 of your return.
        # Ontario tax": line 88 is line 86, as line 87 is 0.
        ONTARIO_TAX: SumLine(
            ONTARIO_TAX,
            (
                (ONTARIO_TAX_AFTER_FOOD_CREDIT, D("8195.77")),
                (ONTARIO_HEALTH_PREMIUM, D("750")),
            ),
            D("8945.77"),
        ),
        # T1 line 142 (line 42000) "Add lines 139 to 141. Net federal tax", in line order: line
        # 139 (41700), line 140 (41500, the advanced Canada workers benefit) and line 141 (41800,
        # special taxes), the last two 0 here.
        NET_FEDERAL_TAX: SumLine(
            NET_FEDERAL_TAX,
            (
                (FEDERAL_TAX_LESS_CREDITS, D("16951.38")),
                (ADVANCED_CANADA_WORKERS_BENEFIT, D("0")),
                (SPECIAL_TAXES, D("0")),
            ),
            D("16951.38"),
        ),
        # T2038(IND) Part C amount 3 "Total recapture of investment tax credit on SR&ED
        # expenditures (add amounts 1 and 2)", T1 line 131, and line 132 "Line 130 plus line 131"
        # with line 130 carrying line 126.
        ITC_RECAPTURE: SumLine(
            ITC_RECAPTURE,
            ((ITC_RECAPTURE_AT_15_PERCENT, D("0")), (ITC_RECAPTURE_AT_20_PERCENT, D("0"))),
            D("0"),
        ),
        FEDERAL_TAX_WITH_ITC_RECAPTURE: SumLine(
            FEDERAL_TAX_WITH_ITC_RECAPTURE,
            ((FEDERAL_TAX_AFTER_CREDITS, D("16951.38")), (ITC_RECAPTURE, D("0"))),
            D("16951.38"),
        ),
        # T1 line 138 (line 41600) "Add lines 135 to 137.": lines 135 and 137, in line order.
        CREDITS_AGAINST_FEDERAL_TAX: SumLine(
            CREDITS_AGAINST_FEDERAL_TAX,
            ((POLITICAL_CREDIT, D("0.00")), (LABOUR_SPONSORED_FUNDS_CREDIT, D("0"))),
            D("0.00"),
        ),
        # Federal Worksheet column 1 line 7 "Line 5 plus line 6 =": line 5 is 0.
        POLITICAL_CREDIT_COLUMN_1_LINE_7: SumLine(
            POLITICAL_CREDIT_COLUMN_1_LINE_7,
            (
                (POLITICAL_CREDIT_COLUMN_1_LINE_5, D("0.00")),
                (POLITICAL_CREDIT_COLUMN_1_LINE_6, D("0.00")),
            ),
            D("0.00"),
        ),
        # Federal Worksheet column 2 line 7 "Line 5 plus line 6 =": line 5 is 0.
        POLITICAL_CREDIT_COLUMN_2_LINE_7: SumLine(
            POLITICAL_CREDIT_COLUMN_2_LINE_7,
            (
                (POLITICAL_CREDIT_COLUMN_2_LINE_5, D("0.00")),
                (POLITICAL_CREDIT_COLUMN_2_LINE_6, D("300.00")),
            ),
            D("300.00"),
        ),
        # Federal Worksheet column 3 line 7 "Line 5 plus line 6 =": line 5 is 0.
        POLITICAL_CREDIT_COLUMN_3_LINE_7: SumLine(
            POLITICAL_CREDIT_COLUMN_3_LINE_7,
            (
                (POLITICAL_CREDIT_COLUMN_3_LINE_5, D("0.00")),
                (POLITICAL_CREDIT_COLUMN_3_LINE_6, D("475.00")),
            ),
            D("475.00"),
        ),
        # T1 line 141 (line 41800) "Special taxes": Form T1172's line 10 or 13 and the RL-10 amount.
        SPECIAL_TAXES: SumLine(
            SPECIAL_TAXES,
            ((RESP_AIPS_ADDITIONAL_TAX, D("0")), (RL_10_LABOUR_SPONSORED_FUND_AMOUNT, D("0"))),
            D("0"),
        ),
        # T1 line 148 (line 43500) "Add lines 143 to 147. Total payable", in line order: line
        # 143 "Amount from line 42000" and line 147 (42800), the Ontario tax.
        TOTAL_PAYABLE: SumLine(
            TOTAL_PAYABLE,
            ((NET_FEDERAL_TAX, D("16951.38")), (ONTARIO_TAX, D("8945.77"))),
            D("25897.15"),
        ),
        # Schedule 6 line 5 "Add lines 1 to 4. Enter the result, even if it is "0". Working
        # income": line 1 "Employment income and other employment income from line 10100 and line
        # 10400 of the return" alone, as lines 2 to 4 are not triggered.
        WORKING_INCOME: SumLine(WORKING_INCOME, ((EMPLOYMENT_INCOME, D("110000")),), D("110000")),
        # Schedule 6 line 15 "Line 13 minus line 14 Enter this amount on line 23 and line 35.
        # Adjusted family net income": line 7, net income (line 23600), carried unchanged.
        ADJUSTED_FAMILY_NET_INCOME: SumLine(
            ADJUSTED_FAMILY_NET_INCOME, ((NET_INCOME, D("115000")),), D("115000")
        ),
        # Worksheet ON479 column 1 line 7 "Line 5 plus line 6": line 5 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_1_LINE_7: SumLine(
            ontario.POLITICAL_CREDIT_COLUMN_1_LINE_7,
            (
                (ontario.POLITICAL_CREDIT_COLUMN_1_LINE_5, D("0.00")),
                (ontario.POLITICAL_CREDIT_COLUMN_1_LINE_6, D("0.00")),
            ),
            D("0.00"),
        ),
        # Worksheet ON479 column 2 line 7 "Line 5 plus line 6": line 5 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_2_LINE_7: SumLine(
            ontario.POLITICAL_CREDIT_COLUMN_2_LINE_7,
            (
                (ontario.POLITICAL_CREDIT_COLUMN_2_LINE_5, D("0.00")),
                (ontario.POLITICAL_CREDIT_COLUMN_2_LINE_6, D("375.03")),
            ),
            D("375.03"),
        ),
        # Worksheet ON479 column 3 line 7 "Line 5 plus line 6": line 5 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_3_LINE_7: SumLine(
            ontario.POLITICAL_CREDIT_COLUMN_3_LINE_7,
            (
                (ontario.POLITICAL_CREDIT_COLUMN_3_LINE_5, D("0.00")),
                (ontario.POLITICAL_CREDIT_COLUMN_3_LINE_6, D("958.41")),
            ),
            D("958.41"),
        ),
        # ON479 line 8 "Line 6 plus line 7 Family net income": the net income (line 6) and the
        # spouse's (line 7, 0 with no spouse).
        SENIORS_CARE_FAMILY_NET_INCOME: SumLine(
            SENIORS_CARE_FAMILY_NET_INCOME,
            ((NET_INCOME, D("115000.00")), (SPOUSE_NET_INCOME, D("0"))),
            D("115000.00"),
        ),
        # ON479 line 18 "Add lines 1, 2, 13, 14, 16, and 17.": lines 1, 13, 14, 16 and 17, in order.
        ONTARIO_CREDITS_SUBTOTAL: SumLine(
            ONTARIO_CREDITS_SUBTOTAL,
            (
                (FERTILITY_CREDIT, D("0")),
                (SENIORS_CARE_CREDIT, D("0")),
                (SENIORS_TRANSIT_CREDIT, D("0")),
                (ontario.POLITICAL_CREDIT, D("0.00")),
                (FLOW_THROUGH_SHARE_CREDIT, D("0")),
            ),
            D("0"),
        ),
        # ON479 line 21 "Line 19 plus line 20": line 19 carries line 18, and line 20 is the
        # co-operative education credit, 0 for no work placements.
        ONTARIO_CREDITS: SumLine(
            ONTARIO_CREDITS,
            ((ONTARIO_CREDITS_SUBTOTAL, D("0")), (COOP_EDUCATION_CREDIT, D("0"))),
            D("0"),
        ),
        # T1 line 165 (line 47900) "Provincial or territorial credits": ON479 line 21.
        PROVINCIAL_CREDITS: SumLine(PROVINCIAL_CREDITS, ((ONTARIO_CREDITS, D("0")),), D("0")),
        # T1 line 166 (line 48200) "Add lines 150 to 165. Total credits": line 150 (43700), line
        # 155 (45300), the Canada workers benefit, and line 165 (47900), in line order.
        TOTAL_CREDITS: SumLine(
            TOTAL_CREDITS,
            (
                (INCOME_TAX_DEDUCTED, D("25000")),
                (REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT, D("0.00")),
                (CANADA_WORKERS_BENEFIT, D("0")),
                (PART_XII_2_TAX_CREDIT, D("0")),
                (EMPLOYEE_AND_PARTNER_GST_HST_REBATE, D("0")),
                (EDUCATOR_SCHOOL_SUPPLY_CREDIT, D("0")),
                (JOURNALISM_LABOUR_TAX_CREDIT, D("0")),
                (TAX_PAID_BY_INSTALMENTS, D("0")),
                (PROVINCIAL_CREDITS, D("0")),
            ),
            D("25000"),
        ),
        # The Ontario opportunities fund, line 1 "Amount from line 48400 above".
        ontario.REFUND_BEFORE_DONATION: SumLine(
            ontario.REFUND_BEFORE_DONATION, ((REFUND, D("0")),), D("0")
        ),
        # Federal Worksheet line 22100, line 4.
        CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES: SumLine(
            CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
            (
                (TOTAL_CARRYING_CHARGES, D("0")),
                (TOTAL_INTEREST_EXPENSES, D("0")),
                (TOTAL_OTHER_EXPENSES, D("0")),
            ),
            D("0"),
        ),
        # Form T1436 line 7.
        CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024: SumLine(
            CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
            (
                (CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987, D("0")),
                (
                    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
                    D("0"),
                ),
                (CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY, D("0")),
                (CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999, D("0")),
                (CAPITAL_GAINS_DEDUCTIONS_2000, D("0")),
                (CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024, D("0")),
            ),
            D("0"),
        ),
        # Form T1436 line 14.
        OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024: SumLine(
            OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
            (
                (OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994, D("0")),
                (OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996, D("0")),
                (OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999, D("0")),
                (OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000, D("0")),
                (OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023, D("0")),
                (OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024, D("0")),
            ),
            D("0"),
        ),
        # Schedule 15 line 5.
        FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT: SumLine(
            FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT,
            (
                (FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL, D("0")),
                (FHSA_VARIABLE_B_AMOUNT, D("0")),
            ),
            D("0"),
        ),
        # Schedule 15 line 11.
        FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL: SumLine(
            FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
            (
                (FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL, D("0")),
                (FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL, D("0")),
            ),
            D("0"),
        ),
        # Schedule 15 line 16.
        FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD: SumLine(
            FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD,
            ((FHSA_ANNUAL_AMOUNT, D("8000.00")), (FHSA_CARRYFORWARD_FOR_2025, D("0"))),
            D("8000.00"),
        ),
        # Schedule 15 line 19.
        FHSA_TOTAL_RRSP_TRANSFERS: SumLine(
            FHSA_TOTAL_RRSP_TRANSFERS,
            (
                (FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS, D("0")),
                (FHSA_RRSP_TRANSFERS_IN_2025, D("0")),
            ),
            D("0"),
        ),
        # Schedule 15 line 22.
        FHSA_TOTAL_DESIGNATED_TRANSFERS: SumLine(
            FHSA_TOTAL_DESIGNATED_TRANSFERS,
            (
                (FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS, D("0")),
                (FHSA_DESIGNATED_TRANSFERS_IN_2025, D("0")),
            ),
            D("0"),
        ),
        # Schedule 15 line 32.
        FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD: SumLine(
            FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD,
            ((FHSA_ANNUAL_AMOUNT_FOR_2024, D("8000.00")), (FHSA_CARRYFORWARD_FOR_2024, D("0"))),
            D("8000.00"),
        ),
        # Schedule 15 line 35.
        FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT: SumLine(
            FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT,
            ((FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT, D("0")), (FHSA_VARIABLE_F_AMOUNT, D("0"))),
            D("0"),
        ),
        # Schedule 15 line 43.
        FHSA_TOTAL_ANNUAL_LIMITS: SumLine(
            FHSA_TOTAL_ANNUAL_LIMITS,
            ((FHSA_ANNUAL_LIMIT, D("0")), (FHSA_ANNUAL_LIMITS_FOR_2024_AND_PRIOR_YEARS, D("0"))),
            D("0"),
        ),
        # Schedule 15 line 54.
        FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS: SumLine(
            FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS,
            (
                (FHSA_UNUSED_CONTRIBUTIONS_BROUGHT_FORWARD, D("0")),
                (FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL, D("0")),
            ),
            D("0"),
        ),
        # Form T1436 line 4 "Total of column C from Chart A", for no unapplied losses.
        TOTAL_ADJUSTED_NET_CAPITAL_LOSSES: SumLine(
            TOTAL_ADJUSTED_NET_CAPITAL_LOSSES,
            (
                (ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987, D("0.00")),
                (ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989, D("0.00")),
                (ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999, D("0.00")),
                (ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024, D("0.00")),
            ),
            D("0.00"),
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2: SumLine(
            output=MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2,
            parts=(
                (
                    SPOUSE_UCCB_REPAYMENT,
                    D("0"),
                ),
                (
                    SPOUSE_RDSP_INCOME_REPAYMENT,
                    D("0"),
                ),
            ),
            total=D("0"),
        ),
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3: SumLine(
            output=MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3,
            parts=(
                (
                    SPOUSE_NET_INCOME_BEFORE_ADJUSTMENTS,
                    D("0"),
                ),
                (
                    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2,
                    D("0"),
                ),
            ),
            total=D("0"),
        ),
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4: SumLine(
            output=MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4,
            parts=(
                (
                    SPOUSE_UNIVERSAL_CHILD_CARE_BENEFIT,
                    D("0"),
                ),
                (
                    SPOUSE_RDSP_INCOME,
                    D("0"),
                ),
            ),
            total=D("0"),
        ),
        MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS: SumLine(
            output=MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS,
            parts=(
                (
                    RPP_DEDUCTION,
                    D("0"),
                ),
                (
                    UNION_DUES,
                    D("2000"),
                ),
                (
                    OTHER_EMPLOYMENT_EXPENSES,
                    D("0"),
                ),
                (
                    CLERGY_RESIDENCE_DEDUCTION,
                    D("0"),
                ),
            ),
            total=D("2000"),
        ),
        MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME: SumLine(
            output=MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME,
            parts=(
                (
                    EMPLOYMENT_INCOME,
                    D("110000"),
                ),
                (
                    OTHER_EMPLOYMENT_INCOME,
                    D("0"),
                ),
            ),
            total=D("110000"),
        ),
        MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME: SumLine(
            output=MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME,
            parts=(
                (
                    NET_BUSINESS_INCOME,
                    D("0"),
                ),
                (
                    NET_PROFESSIONAL_INCOME,
                    D("0"),
                ),
                (
                    NET_COMMISSION_INCOME,
                    D("0"),
                ),
                (
                    NET_FARMING_INCOME,
                    D("0"),
                ),
                (
                    NET_FISHING_INCOME,
                    D("0"),
                ),
            ),
            total=D("0"),
        ),
        MEDICAL_SUPPLEMENT_WORKING_INCOME: SumLine(
            output=MEDICAL_SUPPLEMENT_WORKING_INCOME,
            parts=(
                (
                    MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME,
                    D("108000"),
                ),
                (
                    MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME,
                    D("0"),
                ),
            ),
            total=D("108000"),
        ),
        MEDICAL_SUPPLEMENT_LINE_11: SumLine(
            output=MEDICAL_SUPPLEMENT_LINE_11,
            parts=(
                (
                    DISABILITY_SUPPORTS_DEDUCTION,
                    D("0"),
                ),
                (
                    MEDICAL_CLAIM,
                    D("0"),
                ),
            ),
            total=D("0"),
        ),
        MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3: SumLine(
            output=MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3,
            parts=(
                (
                    NET_INCOME_BEFORE_ADJUSTMENTS,
                    D("115000.00"),
                ),
                (
                    UCCB_AND_RDSP_INCOME_REPAYMENTS,
                    D("0"),
                ),
            ),
            total=D("115000.00"),
        ),
        MEDICAL_SUPPLEMENT_LINE_6: SumLine(
            output=MEDICAL_SUPPLEMENT_LINE_6,
            parts=(
                (
                    MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5,
                    D("115000.00"),
                ),
                (
                    MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5,
                    D("0"),
                ),
            ),
            total=D("115000.00"),
        ),
    }
    assert subtracted == {
        # Form T1172 line 6 "Line 4 minus line 5" and line 8 "line 1 minus line 7", with no
        # floor on either.
        RESP_AIPS_LIMIT_REMAINING: SubtractedLine(
            output=RESP_AIPS_LIMIT_REMAINING,
            minuend=RESP_AIPS_LIFETIME_LIMIT,
            minuend_amount=D("50000.00"),
            subtrahend=RESP_AIPS_REDUCTION_USED_IN_PREVIOUS_YEARS,
            subtrahend_amount=D("0"),
            result=D("50000.00"),
        ),
        RESP_AIPS_SUBJECT_TO_TAX: SubtractedLine(
            output=RESP_AIPS_SUBJECT_TO_TAX,
            minuend=RESP_AIPS_RECEIVED_PART_A,
            minuend_amount=D("0"),
            subtrahend=RESP_AIPS_REDUCTION,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Worksheet ON428's line C "Amount A minus amount B": no dividends.
        ontario.DIVIDENDS_AMOUNT_A_LESS_B: SubtractedLine(
            output=ontario.DIVIDENDS_AMOUNT_A_LESS_B,
            minuend=ontario.DIVIDENDS_AMOUNT_A,
            minuend_amount=D("0"),
            subtrahend=ontario.DIVIDENDS_AMOUNT_B,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # The Federal Worksheet's line C "Amount A minus amount B": no dividends with no slip.
        DIVIDENDS_AMOUNT_A_LESS_B: SubtractedLine(
            output=DIVIDENDS_AMOUNT_A_LESS_B,
            minuend=DIVIDENDS_AMOUNT_A,
            minuend_amount=D("0"),
            subtrahend=DIVIDENDS_AMOUNT_B,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # The Federal Worksheet's line 5 "Line 1 minus line 4 =": no floor is printed.
        NET_INCOME_LESS_UCCB_AND_RDSP_INCOME: SubtractedLine(
            output=NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
            minuend=NET_INCOME,
            minuend_amount=D("115000"),
            subtrahend=UCCB_AND_RDSP_INCOME,
            subtrahend_amount=D("0"),
            result=D("115000"),
        ),
        # Schedule 9 chart for line 33900 line 3 "Line 1 minus Line 2", line 14 "Line 12 minus line
        # 13" and line 21's amount G, "Amount E minus amount F": all 0 for donations of 0.
        CAPITAL_PROPERTY_GIFTS: SubtractedLine(
            output=CAPITAL_PROPERTY_GIFTS,
            minuend=CAPITAL_GIFT_TAXABLE_GAINS,
            minuend_amount=D("0"),
            subtrahend=CAPITAL_GIFT_GAINS_DEDUCTION,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        DONATIONS_OVER_FIRST_TIER: SubtractedLine(
            output=DONATIONS_OVER_FIRST_TIER,
            minuend=DONATIONS_AND_GIFTS_TOTAL,
            minuend_amount=D("0"),
            subtrahend=DONATIONS_FIRST_TIER,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        REGULAR_RATE_DONATIONS: SubtractedLine(
            output=REGULAR_RATE_DONATIONS,
            minuend=DONATIONS_OVER_FIRST_TIER,
            minuend_amount=D("0"),
            subtrahend=HIGH_INCOME_DONATIONS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # The Federal Worksheet's line 11 "Line 9 minus line 10. Enter this amount on line 12100
        # of your return.": nothing reported in previous years comes off nothing.
        INTEREST_AND_OTHER_INVESTMENT_INCOME: SubtractedLine(
            output=INTEREST_AND_OTHER_INVESTMENT_INCOME,
            minuend=INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
            minuend_amount=D("0"),
            subtrahend=INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 7 line 23 "Line 21 minus line 22 Your unused contributions available to carry
        # forward to a future year": all of the 1926 available is deducted, so nothing is left.
        UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD: SubtractedLine(
            output=UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
            minuend=RRSP_CONTRIBUTIONS_AVAILABLE,
            minuend_amount=D("1926"),
            subtrahend=RRSP_DEDUCTION,
            subtrahend_amount=D("1926"),
            result=D("0"),
        ),
        # T1 line 167 "Line 149 minus line 166 ... Refund or balance owing": it takes amounts
        # already in cents, is not floored, and is positive here, so a balance owing (line 48500).
        REFUND_OR_BALANCE_OWING: SubtractedLine(
            output=REFUND_OR_BALANCE_OWING,
            minuend=TOTAL_PAYABLE,
            minuend_amount=D("25897.15"),
            subtrahend=TOTAL_CREDITS,
            subtrahend_amount=D("25000"),
            result=D("897.15"),
        ),
        # The Ontario opportunities fund, line 3 and line 46600 "Net refund (line 1 minus line 2)".
        ontario.NET_REFUND: SubtractedLine(
            output=ontario.NET_REFUND,
            minuend=ontario.REFUND_BEFORE_DONATION,
            minuend_amount=D("0"),
            subtrahend=ontario.OPPORTUNITIES_FUND_DONATION,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T1436 line 15.
        BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE: SubtractedLine(
            output=BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
            minuend=CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
            minuend_amount=D("0"),
            subtrahend=OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Form T1436 line 18.
        BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION: SubtractedLine(
            output=BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
            minuend=BUSINESS_INVESTMENT_LOSS,
            minuend_amount=D("0"),
            subtrahend=BUSINESS_INVESTMENT_LOSS_REDUCTION,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 3.
        FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL: SubtractedLine(
            output=FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
            minuend=FHSA_CONTRIBUTIONS_IN_2025,
            minuend_amount=D("0"),
            subtrahend=FHSA_CONTRIBUTIONS_IN_2025_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 9.
        FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL: SubtractedLine(
            output=FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
            minuend=FHSA_CONTRIBUTIONS_IN_2024,
            minuend_amount=D("0"),
            subtrahend=FHSA_CONTRIBUTIONS_IN_2024_BEFORE_FIRST_QUALIFYING_WITHDRAWAL,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 23.
        FHSA_NET_RRSP_TRANSFER_AMOUNT: SubtractedLine(
            output=FHSA_NET_RRSP_TRANSFER_AMOUNT,
            minuend=FHSA_TOTAL_RRSP_TRANSFERS,
            minuend_amount=D("0"),
            subtrahend=FHSA_TOTAL_DESIGNATED_TRANSFERS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 27.
        FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS: SubtractedLine(
            output=FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS,
            minuend=FHSA_RRSP_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
            minuend_amount=D("0"),
            subtrahend=FHSA_DESIGNATED_TRANSFERS_IN_2024_AND_PRIOR_YEARS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 36.
        FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS: SubtractedLine(
            output=FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS,
            minuend=FHSA_NET_RRSP_TRANSFER_AMOUNT,
            minuend_amount=D("0"),
            subtrahend=FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 45.
        FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS: SubtractedLine(
            output=FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS,
            minuend=FHSA_TOTAL_ANNUAL_LIMITS,
            minuend_amount=D("0"),
            subtrahend=FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 48.
        FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS: SubtractedLine(
            output=FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS,
            minuend=FHSA_LIFETIME_LIMIT,
            minuend_amount=D("40000.00"),
            subtrahend=FHSA_DEDUCTIONS_FOR_2024_AND_PRIOR_YEARS,
            subtrahend_amount=D("0"),
            result=D("40000.00"),
        ),
        # Schedule 15 line 56.
        FHSA_CONTRIBUTIONS_AVAILABLE: SubtractedLine(
            output=FHSA_CONTRIBUTIONS_AVAILABLE,
            minuend=FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 58.
        FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD: SubtractedLine(
            output=FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD,
            minuend=FHSA_CONTRIBUTIONS_AVAILABLE,
            minuend_amount=D("0"),
            subtrahend=FHSA_DEDUCTION,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # T1 line 23400.
        NET_INCOME_BEFORE_ADJUSTMENTS: SubtractedLine(
            output=NET_INCOME_BEFORE_ADJUSTMENTS,
            minuend=TOTAL_INCOME,
            minuend_amount=D("120000"),
            subtrahend=DEDUCTIONS_FROM_TOTAL_INCOME,
            subtrahend_amount=D("5000"),
            result=D("115000"),
        ),
        # Form T1436 Chart A: what is left of line 13 (the amount claimed, 0) after each of the
        # older rows, and column E "Remaining adjusted net capital losses (column C minus column
        # D)".
        ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987: SubtractedLine(
            output=ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987,
            minuend=NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
            minuend_amount=D("0"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_1985_TO_1987,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        REMAINING_ADJUSTED_LOSSES_1985_TO_1987: SubtractedLine(
            output=REMAINING_ADJUSTED_LOSSES_1985_TO_1987,
            minuend=ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_1985_TO_1987,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989: SubtractedLine(
            output=ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989,
            minuend=ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_1988_AND_1989,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        REMAINING_ADJUSTED_LOSSES_1988_AND_1989: SubtractedLine(
            output=REMAINING_ADJUSTED_LOSSES_1988_AND_1989,
            minuend=ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_1988_AND_1989,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999: SubtractedLine(
            output=ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999,
            minuend=ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_1990_TO_1999,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        REMAINING_ADJUSTED_LOSSES_1990_TO_1999: SubtractedLine(
            output=REMAINING_ADJUSTED_LOSSES_1990_TO_1999,
            minuend=ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_1990_TO_1999,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        REMAINING_ADJUSTED_LOSSES_2001_TO_2024: SubtractedLine(
            output=REMAINING_ADJUSTED_LOSSES_2001_TO_2024,
            minuend=ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
            minuend_amount=D("0.00"),
            subtrahend=ADJUSTED_LOSSES_APPLIED_2001_TO_2024,
            subtrahend_amount=D("0.00"),
            result=D("0.00"),
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS: SubtractedLine(
            output=MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS,
            minuend=MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME,
            minuend_amount=D("110000"),
            subtrahend=WAGE_LOSS_REPLACEMENT_PLAN_INCOME,
            subtrahend_amount=D("0"),
            result=D("110000"),
        ),
    }
    # T1 line 30000 and the Federal Worksheet (5000-D1): net income of 115000 is at or below
    # the 177882 threshold, so the reduction (line 9) is 0 and the amount is the base plus the
    # whole supplement, 14538 + 1591 = 16129, rounded half-up to the cent.
    assert tapered == {
        BASIC_PERSONAL_AMOUNT: TaperedAmountLine(
            output=BASIC_PERSONAL_AMOUNT,
            base=NET_INCOME,
            base_amount=D("115000"),
            taper=Taper(
                base=D("14538"), supplement=D("1591"), threshold=D("177882"), range=D("75532")
            ),
            rounding=CENT,
            reduction=ExactFraction(0),
            result=D("16129.00"),
        )
    }
    # ON428 line 58040 has no reduction: the Ontario amount is the dataset's credit amount. ON428
    # line 74 "Basic reduction 294.00" is claimed whole too.
    assert gated == {
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET: ThresholdGateLine(
            output=MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET,
            amount_kind=MEDICAL_SUPPLEMENT_LINE_16,
            amount_value=D("0"),
            gate_kind=MEDICAL_SUPPLEMENT_WORKING_INCOME,
            gate_value=D("108000"),
            threshold=Amount(D("4390")),
            rounding=CENT,
            result=D("0.00"),
        ),
    }

    assert amounts == {
        # Form T1172 line 4 "Maximum lifetime RRSP contribution limit ... $ 50,000.00".
        RESP_AIPS_LIFETIME_LIMIT: CreditAmountLine(
            RESP_AIPS_LIFETIME_LIMIT, Credit(amount=D("50000.00")), CENT, D("50000.00")
        ),
        ontario.BASIC_PERSONAL_AMOUNT: CreditAmountLine(
            ontario.BASIC_PERSONAL_AMOUNT, Credit(amount=D("12747")), CENT, D("12747")
        ),
        TAX_REDUCTION_BASIC: CreditAmountLine(
            TAX_REDUCTION_BASIC, Credit(amount=D("294.00")), CENT, D("294.00")
        ),
        # Federal Worksheet line 1 "Maximum amount 9,028.00" and Schedule 5 line 1 of the line
        # 30425 part "Base amount 28,798.00".
        AGE_MAXIMUM: CreditAmountLine(AGE_MAXIMUM, Credit(amount=D("9028.00")), CENT, D("9028.00")),
        # Federal Worksheet line 3 "Income threshold 45,522.00".
        AGE_INCOME_THRESHOLD: CreditAmountLine(
            AGE_INCOME_THRESHOLD, Credit(amount=D("45522.00")), CENT, D("45522.00")
        ),
        SPOUSE_CAREGIVER_BASE: CreditAmountLine(
            SPOUSE_CAREGIVER_BASE, Credit(amount=D("28798.00")), CENT, D("28798.00")
        ),
        # Worksheet ON428 line 1 "Maximum amount 6,223.00" and line 3 "Income threshold
        # 46,330.00".
        ontario.AGE_MAXIMUM: CreditAmountLine(
            ontario.AGE_MAXIMUM, Credit(amount=D("6223.00")), CENT, D("6223.00")
        ),
        ontario.AGE_INCOME_THRESHOLD: CreditAmountLine(
            ontario.AGE_INCOME_THRESHOLD, Credit(amount=D("46330.00")), CENT, D("46330.00")
        ),
        # ON428 line 11 "Base amount 11,905.00".
        ontario.SPOUSE_BASE: CreditAmountLine(
            ontario.SPOUSE_BASE, Credit(amount=D("11905.00")), CENT, D("11905.00")
        ),
        # ON428 line 14 "Base amount 11,905.00".
        ELIGIBLE_DEPENDANT_BASE: CreditAmountLine(
            ELIGIBLE_DEPENDANT_BASE, Credit(amount=D("11905.00")), CENT, D("11905.00")
        ),
        # Schedule 9 line 13 "$200" and line 18 "Income threshold 253,414.00"; Federal Worksheet
        # line 4 "8,319.38": each claimed whole.
        DONATION_FIRST_TIER_MAXIMUM: CreditAmountLine(
            DONATION_FIRST_TIER_MAXIMUM, Credit(amount=D("200")), CENT, D("200.00")
        ),
        DONATION_HIGH_INCOME_THRESHOLD: CreditAmountLine(
            DONATION_HIGH_INCOME_THRESHOLD, Credit(amount=D("253414.00")), CENT, D("253414.00")
        ),
        TOP_UP_THRESHOLD: CreditAmountLine(
            TOP_UP_THRESHOLD, Credit(amount=D("8319.38")), CENT, D("8319.38")
        ),
        # Schedule 15 line 14.
        FHSA_ANNUAL_AMOUNT: CreditAmountLine(
            FHSA_ANNUAL_AMOUNT, Credit(amount=D("8000.00")), CENT, D("8000.00")
        ),
        # Schedule 15 line 30.
        FHSA_ANNUAL_AMOUNT_FOR_2024: CreditAmountLine(
            FHSA_ANNUAL_AMOUNT_FOR_2024, Credit(amount=D("8000.00")), CENT, D("8000.00")
        ),
        # Schedule 15 Step 2's printed "0".
        FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD: CreditAmountLine(
            FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD,
            Credit(amount=D("0")),
            CENT,
            D("0.00"),
        ),
        # Schedule 15 line 46.
        FHSA_LIFETIME_LIMIT: CreditAmountLine(
            FHSA_LIFETIME_LIMIT, Credit(amount=D("40000.00")), CENT, D("40000.00")
        ),
        # Worksheet ON479 column 1 line 2: 0.00, a printed constant.
        ontario.POLITICAL_CREDIT_COLUMN_1_LINE_2: CreditAmountLine(
            ontario.POLITICAL_CREDIT_COLUMN_1_LINE_2, Credit(amount=D("0.00")), CENT, D("0.00")
        ),
        # Worksheet ON479 column 1 line 6: 0.00, a printed constant.
        ontario.POLITICAL_CREDIT_COLUMN_1_LINE_6: CreditAmountLine(
            ontario.POLITICAL_CREDIT_COLUMN_1_LINE_6, Credit(amount=D("0.00")), CENT, D("0.00")
        ),
        # Worksheet ON479 column 2 line 2: 500.05, a printed constant.
        ontario.POLITICAL_CREDIT_COLUMN_2_LINE_2: CreditAmountLine(
            ontario.POLITICAL_CREDIT_COLUMN_2_LINE_2, Credit(amount=D("500.05")), CENT, D("500.05")
        ),
        # Worksheet ON479 column 2 line 6: 375.03, a printed constant.
        ontario.POLITICAL_CREDIT_COLUMN_2_LINE_6: CreditAmountLine(
            ontario.POLITICAL_CREDIT_COLUMN_2_LINE_6, Credit(amount=D("375.03")), CENT, D("375.03")
        ),
        # Worksheet ON479 column 3 line 2: 1666.82, a printed constant.
        ontario.POLITICAL_CREDIT_COLUMN_3_LINE_2: CreditAmountLine(
            ontario.POLITICAL_CREDIT_COLUMN_3_LINE_2,
            Credit(amount=D("1666.82")),
            CENT,
            D("1666.82"),
        ),
        # Worksheet ON479 column 3 line 6: 958.41, a printed constant.
        ontario.POLITICAL_CREDIT_COLUMN_3_LINE_6: CreditAmountLine(
            ontario.POLITICAL_CREDIT_COLUMN_3_LINE_6, Credit(amount=D("958.41")), CENT, D("958.41")
        ),
        # Federal Worksheet column 1 line 2: 0.00, a printed constant.
        POLITICAL_CREDIT_COLUMN_1_LINE_2: CreditAmountLine(
            POLITICAL_CREDIT_COLUMN_1_LINE_2, Credit(amount=D("0.00")), CENT, D("0.00")
        ),
        # Federal Worksheet column 1 line 6: 0.00, a printed constant.
        POLITICAL_CREDIT_COLUMN_1_LINE_6: CreditAmountLine(
            POLITICAL_CREDIT_COLUMN_1_LINE_6, Credit(amount=D("0.00")), CENT, D("0.00")
        ),
        # Federal Worksheet column 2 line 2: 400.00, a printed constant.
        POLITICAL_CREDIT_COLUMN_2_LINE_2: CreditAmountLine(
            POLITICAL_CREDIT_COLUMN_2_LINE_2, Credit(amount=D("400.00")), CENT, D("400.00")
        ),
        # Federal Worksheet column 2 line 6: 300.00, a printed constant.
        POLITICAL_CREDIT_COLUMN_2_LINE_6: CreditAmountLine(
            POLITICAL_CREDIT_COLUMN_2_LINE_6, Credit(amount=D("300.00")), CENT, D("300.00")
        ),
        # Federal Worksheet column 3 line 2: 750.00, a printed constant.
        POLITICAL_CREDIT_COLUMN_3_LINE_2: CreditAmountLine(
            POLITICAL_CREDIT_COLUMN_3_LINE_2, Credit(amount=D("750.00")), CENT, D("750.00")
        ),
        # Federal Worksheet column 3 line 6: 475.00, a printed constant.
        POLITICAL_CREDIT_COLUMN_3_LINE_6: CreditAmountLine(
            POLITICAL_CREDIT_COLUMN_3_LINE_6, Credit(amount=D("475.00")), CENT, D("475.00")
        ),
        # Federal Worksheet shortcut "$1,275 or more": the printed threshold.
        POLITICAL_CREDIT_SHORTCUT_THRESHOLD: CreditAmountLine(
            POLITICAL_CREDIT_SHORTCUT_THRESHOLD, Credit(amount=D("1275")), CENT, D("1275")
        ),
        # Federal Worksheet shortcut "enter $650 on line 41000": the printed amount.
        POLITICAL_CREDIT_SHORTCUT_AMOUNT: CreditAmountLine(
            POLITICAL_CREDIT_SHORTCUT_AMOUNT, Credit(amount=D("650")), CENT, D("650")
        ),
        # ON479 line 9 "Base amount 35,000.00".
        SENIORS_CARE_BASE_AMOUNT: CreditAmountLine(
            SENIORS_CARE_BASE_AMOUNT, Credit(amount=D("35000.00")), CENT, D("35000.00")
        ),
        # Worksheet ON479 "Line 20" line 5 "400,000.00", line 7 "200,000.00" and line 9 "1.00".
        COOP_EDUCATION_PAYROLL_THRESHOLD: CreditAmountLine(
            COOP_EDUCATION_PAYROLL_THRESHOLD, Credit(amount=D("400000.00")), CENT, D("400000.00")
        ),
        COOP_EDUCATION_PAYROLL_RANGE: CreditAmountLine(
            COOP_EDUCATION_PAYROLL_RANGE, Credit(amount=D("200000.00")), CENT, D("200000.00")
        ),
        COOP_EDUCATION_FULL_SHARE: CreditAmountLine(
            COOP_EDUCATION_FULL_SHARE, Credit(amount=D("1.00")), CENT, D("1.00")
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_INCOME_THRESHOLD: CreditAmountLine(
            output=MEDICAL_SUPPLEMENT_INCOME_THRESHOLD,
            basis=Credit(amount=D("33294.00")),
            rounding=CENT,
            value=D("33294.00"),
        ),
    }
    # ON428 line 75 (line 60969) "Number of dependent children multiplied by $544" and line 76
    # (line 60970) "Number of dependants multiplied by $544": Return A has neither.
    assert per_unit == {
        TAX_REDUCTION_FOR_CHILDREN: PerUnitAmountLine(
            output=TAX_REDUCTION_FOR_CHILDREN,
            count_kind=DEPENDENT_CHILDREN,
            count=0,
            per_unit=Amount(D("544")),
            rounding=CENT,
            result=D("0"),
        ),
        TAX_REDUCTION_FOR_DEPENDANTS: PerUnitAmountLine(
            output=TAX_REDUCTION_FOR_DEPENDANTS,
            count_kind=DEPENDANTS,
            count=0,
            per_unit=Amount(D("544")),
            rounding=CENT,
            result=D("0"),
        ),
        # Schedule 5 line 2 (line 51090) "enter $2,687" for each spouse eligible for the Canada
        # caregiver amount: Return A has none.
        SPOUSE_INFIRMITY_SUPPLEMENT: PerUnitAmountLine(
            output=SPOUSE_INFIRMITY_SUPPLEMENT,
            count_kind=SPOUSE_CAREGIVER_ELIGIBLE,
            count=0,
            per_unit=Amount(D("2687")),
            rounding=CENT,
            result=D("0"),
        ),
        # T1 line 30500 "Number of children you are claiming this amount for Line 30499"
        # "multiplied by $2,687": Return A has no infirm child.
        INFIRM_CHILDREN_AMOUNT: PerUnitAmountLine(
            output=INFIRM_CHILDREN_AMOUNT,
            count_kind=INFIRM_CHILDREN,
            count=0,
            per_unit=Amount(D("2687")),
            rounding=CENT,
            result=D("0"),
        ),
        # Form T778 Part B lines 1 to 3, "multiplied by $8,000", "$11,000" and "$5,000": Return A
        # has no eligible child.
        CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN: PerUnitAmountLine(
            output=CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
            count_kind=CHILDREN_UNDER_SEVEN,
            count=0,
            per_unit=Amount(D("8000")),
            rounding=CENT,
            result=D("0"),
        ),
        CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY: PerUnitAmountLine(
            output=CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
            count_kind=CHILDREN_WITH_DISABILITY,
            count=0,
            per_unit=Amount(D("11000")),
            rounding=CENT,
            result=D("0"),
        ),
        CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN: PerUnitAmountLine(
            output=CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
            count_kind=CHILDREN_SEVEN_TO_SIXTEEN,
            count=0,
            per_unit=Amount(D("5000")),
            rounding=CENT,
            result=D("0"),
        ),
    }
    # Form T778 line 6 "Enter your earned income." "multiplied by two-thirds": 220000 / 3,
    # rounded half-up to the cent.
    assert fractions == {
        # The Federal Worksheet's lines 13 and 16: 138% and 115% of no dividends with no slip.
        ELIGIBLE_DIVIDENDS_GROSSED_UP: FractionAppliedLine(
            output=ELIGIBLE_DIVIDENDS_GROSSED_UP,
            base=ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
            base_amount=D("0"),
            fraction=Fraction(138, 100),
            rounding=CENT,
            result=D("0"),
        ),
        OTHER_DIVIDENDS_GROSSED_UP: FractionAppliedLine(
            output=OTHER_DIVIDENDS_GROSSED_UP,
            base=OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
            base_amount=D("0"),
            fraction=Fraction(115, 100),
            rounding=CENT,
            result=D("0"),
        ),
        CHILD_CARE_EARNED_INCOME_LIMIT: FractionAppliedLine(
            output=CHILD_CARE_EARNED_INCOME_LIMIT,
            base=CHILD_CARE_EARNED_INCOME,
            base_amount=D("110000"),
            fraction=Fraction(2, 3),
            rounding=CENT,
            result=D("73333.33"),
        ),
        # Form T1436 Chart A column C "Adjusted gross capital losses (column A multiplied by column
        # B)" for no unapplied losses, and column G "Net capital loss balance available to carry
        # forward (column E multiplied by column F)" for none remaining, each a fraction of 0.
        ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987: FractionAppliedLine(
            output=ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
            base=UNAPPLIED_NET_CAPITAL_LOSSES_1985_TO_1987,
            base_amount=D("0"),
            fraction=Fraction(1, 1),
            rounding=CENT,
            result=D("0.00"),
        ),
        ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989: FractionAppliedLine(
            output=ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
            base=UNAPPLIED_NET_CAPITAL_LOSSES_1988_AND_1989,
            base_amount=D("0"),
            fraction=Fraction(3, 4),
            rounding=CENT,
            result=D("0.00"),
        ),
        ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999: FractionAppliedLine(
            output=ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
            base=UNAPPLIED_NET_CAPITAL_LOSSES_1990_TO_1999,
            base_amount=D("0"),
            fraction=Fraction(2, 3),
            rounding=CENT,
            result=D("0.00"),
        ),
        ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024: FractionAppliedLine(
            output=ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
            base=UNAPPLIED_NET_CAPITAL_LOSSES_2001_TO_2024,
            base_amount=D("0"),
            fraction=Fraction(1, 1),
            rounding=CENT,
            result=D("0.00"),
        ),
        NET_CAPITAL_LOSS_BALANCE_1985_TO_1987: FractionAppliedLine(
            output=NET_CAPITAL_LOSS_BALANCE_1985_TO_1987,
            base=REMAINING_ADJUSTED_LOSSES_1985_TO_1987,
            base_amount=D("0.00"),
            fraction=Fraction(1, 1),
            rounding=CENT,
            result=D("0.00"),
        ),
        NET_CAPITAL_LOSS_BALANCE_1988_AND_1989: FractionAppliedLine(
            output=NET_CAPITAL_LOSS_BALANCE_1988_AND_1989,
            base=REMAINING_ADJUSTED_LOSSES_1988_AND_1989,
            base_amount=D("0.00"),
            fraction=Fraction(4, 3),
            rounding=CENT,
            result=D("0.00"),
        ),
        NET_CAPITAL_LOSS_BALANCE_1990_TO_1999: FractionAppliedLine(
            output=NET_CAPITAL_LOSS_BALANCE_1990_TO_1999,
            base=REMAINING_ADJUSTED_LOSSES_1990_TO_1999,
            base_amount=D("0.00"),
            fraction=Fraction(3, 2),
            rounding=CENT,
            result=D("0.00"),
        ),
        NET_CAPITAL_LOSS_BALANCE_2001_TO_2024: FractionAppliedLine(
            output=NET_CAPITAL_LOSS_BALANCE_2001_TO_2024,
            base=REMAINING_ADJUSTED_LOSSES_2001_TO_2024,
            base_amount=D("0.00"),
            fraction=Fraction(1, 1),
            rounding=CENT,
            result=D("0.00"),
        ),
    }
    # T1 line 30400 and ON428 line 58160: Schedule 5 line 5 and ON428 line 16, each claimed for
    # the 0 eligible dependants of Return A, a plain 0.
    assert times == {
        ELIGIBLE_DEPENDANT_AMOUNT: TimesCountLine(
            output=ELIGIBLE_DEPENDANT_AMOUNT,
            amount_kind=ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
            amount_value=D("16129.00"),
            count_kind=ELIGIBLE_DEPENDANTS,
            count=0,
            result=D("0"),
        ),
        # T1 line 30100, line 30300 and line 30425, each line 7 or 5 claimed for the 0 filers
        # born in 1960 or earlier, 0 spouse amounts and 0 spouses eligible for the Canada
        # caregiver amount of Return A, a plain 0.
        AGE_AMOUNT: TimesCountLine(
            output=AGE_AMOUNT,
            amount_kind=AGE_AMOUNT_BEFORE_COUNT,
            amount_value=D("0"),
            count_kind=BORN_IN_1960_OR_EARLIER,
            count=0,
            result=D("0"),
        ),
        SPOUSE_AMOUNT: TimesCountLine(
            output=SPOUSE_AMOUNT,
            amount_kind=SPOUSE_AMOUNT_BEFORE_COUNT,
            amount_value=D("16129.00"),
            count_kind=SPOUSES_CLAIMED,
            count=0,
            result=D("0"),
        ),
        SPOUSE_CAREGIVER_AMOUNT: TimesCountLine(
            output=SPOUSE_CAREGIVER_AMOUNT,
            amount_kind=SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT,
            amount_value=D("8601.00"),
            count_kind=SPOUSE_CAREGIVER_ELIGIBLE,
            count=0,
            result=D("0"),
        ),
        # The caller's count "claims the Ontario seniors care at home tax credit" times ON479 line
        # 13: Return A claims none, so a plain 0.
        SENIORS_CARE_CREDIT: TimesCountLine(
            output=SENIORS_CARE_CREDIT,
            amount_kind=SENIORS_CARE_BEFORE_CLAIM,
            amount_value=D("0"),
            count_kind=CLAIMS_SENIORS_CARE_CREDIT,
            count=0,
            result=D("0"),
        ),
        # ON428 line 10 (line 58080) and lines 11 to 13 (line 58120), each claimed for the 0
        # filers born in 1960 or earlier and 0 spouse amounts of Return A, a plain 0.
        ontario.AGE_AMOUNT: TimesCountLine(
            output=ontario.AGE_AMOUNT,
            amount_kind=ontario.AGE_AMOUNT_BEFORE_COUNT,
            amount_value=D("0"),
            count_kind=BORN_IN_1960_OR_EARLIER,
            count=0,
            result=D("0"),
        ),
        ontario.SPOUSE_AMOUNT: TimesCountLine(
            output=ontario.SPOUSE_AMOUNT,
            amount_kind=ontario.SPOUSE_AMOUNT_BEFORE_COUNT,
            amount_value=D("10823"),
            count_kind=SPOUSES_CLAIMED,
            count=0,
            result=D("0"),
        ),
        ontario.ELIGIBLE_DEPENDANT_AMOUNT: TimesCountLine(
            output=ontario.ELIGIBLE_DEPENDANT_AMOUNT,
            amount_kind=ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
            amount_value=D("10823"),
            count_kind=ELIGIBLE_DEPENDANTS,
            count=0,
            result=D("0"),
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_IF_RESIDENT: TimesCountLine(
            output=MEDICAL_SUPPLEMENT_IF_RESIDENT,
            amount_kind=MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET,
            amount_value=D("0.00"),
            count_kind=RESIDENT_IN_CANADA_THROUGHOUT_2025,
            count=1,
            result=D("0.00"),
        ),
        REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT: TimesCountLine(
            output=REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT,
            amount_kind=MEDICAL_SUPPLEMENT_IF_RESIDENT,
            amount_value=D("0.00"),
            count_kind=AGED_18_OR_OLDER_AT_END_OF_2025,
            count=1,
            result=D("0.00"),
        ),
    }
    # ON428 line 78 "Amount from line 77 above multiplied by 2", line 79 "Amount from line 73
    # above" and line 80 "Line 78 minus line 79 (if negative, enter "0") Ontario tax reduction":
    # line 73 is line 71, the tax after the dividend credit, 8195.77; 588.00 is below it, so the
    # reduction is 0.
    assert multiples == {
        ONTARIO_TAX_REDUCTION: MultipleOverLine(
            output=ONTARIO_TAX_REDUCTION,
            base=TAX_REDUCTION_AMOUNTS,
            base_amount=D("294.00"),
            factor=Factor(D("2")),
            less=ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT,
            less_amount=D("8195.77"),
            rounding=CENT,
            result=D("0"),
        )
    }
    # T1 line 92 (line 31260) "Enter whichever is less: $1,471 or line 1 plus line 2.":
    # employment income of 110000 is above the cap, so the amount is the cap.
    assert capped == {
        # The guide's line 41400 "to a maximum of $750", after the 15%: 0 is below it.
        LABOUR_SPONSORED_FUNDS_CREDIT: CappedAmountLine(
            LABOUR_SPONSORED_FUNDS_CREDIT,
            LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM,
            D("0"),
            Amount(D("750")),
            CENT,
            D("0"),
        ),
        CANADA_EMPLOYMENT_AMOUNT: CappedAmountLine(
            CANADA_EMPLOYMENT_AMOUNT,
            EMPLOYMENT_INCOME,
            D("110000"),
            Amount(D("1471")),
            CENT,
            D("1471"),
        ),
        # T1 line 109 "Enter whichever is less: $2,834 or the amount from line 108.": 3450.00 is
        # above it.
        MEDICAL_THRESHOLD: CappedAmountLine(
            MEDICAL_THRESHOLD,
            MEDICAL_NET_INCOME_SHARE,
            D("3450.00"),
            Amount(D("2834")),
            CENT,
            D("2834"),
        ),
        # ON428 line 40 "Enter whichever is less: $2,885 or the amount on line 39."
        ontario.MEDICAL_THRESHOLD: CappedAmountLine(
            ontario.MEDICAL_THRESHOLD,
            ontario.MEDICAL_NET_INCOME_SHARE,
            D("3450.00"),
            Amount(D("2885")),
            CENT,
            D("2885"),
        ),
        # Schedule ON428-A line 5's "(maximum $875)" and line 14 "Amount from line 5 above
        # (maximum $875)": 5555.00 is above it.
        LIFT_MAXIMUM_CREDIT: CappedAmountLine(
            LIFT_MAXIMUM_CREDIT,
            LIFT_CREDIT_BEFORE_MAXIMUM,
            D("5555.00"),
            Amount(D("875")),
            CENT,
            D("875"),
        ),
        # ON479 line 1's "(maximum $5,000)", printed after the percentage: it caps the credit.
        FERTILITY_CREDIT: CappedAmountLine(
            FERTILITY_CREDIT,
            FERTILITY_CREDIT_BEFORE_MAXIMUM,
            D("0"),
            Amount(D("5000")),
            CENT,
            D("0"),
        ),
        # ON479 line 5's "(maximum $1,500)", printed after the percentage: it caps the result.
        SENIORS_CARE_AMOUNT: CappedAmountLine(
            SENIORS_CARE_AMOUNT,
            SENIORS_CARE_BEFORE_MAXIMUM,
            D("0"),
            Amount(D("1500")),
            CENT,
            D("0"),
        ),
        # T1 line 161's "(maximum $1,000)", printed before the percentage: it caps the supplies
        # expenses (line 46800).
        EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM: CappedAmountLine(
            EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM,
            EDUCATOR_SUPPLIES_EXPENSES,
            D("0"),
            Amount(D("1000")),
            CENT,
            D("0"),
        ),
        # ON479 line 14's "(maximum $3,000)", printed before the percentage: it caps the amount
        # paid.
        SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM: CappedAmountLine(
            SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
            SENIORS_TRANSIT_PAID,
            D("0"),
            Amount(D("3000")),
            CENT,
            D("0"),
        ),
        # Schedule 5 line 3 of the line 30425 part "(maximum $8,601)": 28798.00 is above it.
        SPOUSE_CAREGIVER_LIMIT: CappedAmountLine(
            SPOUSE_CAREGIVER_LIMIT,
            SPOUSE_CAREGIVER_BEFORE_MAXIMUM,
            D("28798.00"),
            Amount(D("8601")),
            CENT,
            D("8601"),
        ),
        # ON428 line 13's "(maximum $10,823)": 11905.00 is above it.
        ontario.SPOUSE_AMOUNT_BEFORE_COUNT: CappedAmountLine(
            ontario.SPOUSE_AMOUNT_BEFORE_COUNT,
            ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM,
            D("11905.00"),
            Amount(D("10823")),
            CENT,
            D("10823"),
        ),
        # ON479 line 16's "(maximum $1,666.82)": the pick for contributions of 0 is 0.
        ontario.POLITICAL_CREDIT: CappedAmountLine(
            ontario.POLITICAL_CREDIT,
            ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM,
            D("0.00"),
            Amount(D("1666.82")),
            CENT,
            D("0.00"),
        ),
        # T1 line 135 and line 41000 "(maximum $650)": the pick for contributions of 0 is 0.
        POLITICAL_CREDIT: CappedAmountLine(
            POLITICAL_CREDIT,
            POLITICAL_CREDIT_BEFORE_MAXIMUM,
            D("0.00"),
            Amount(D("650")),
            CENT,
            D("0.00"),
        ),
        # ON428 line 16's "(maximum $10,823)": 11905.00 is above it.
        ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT: CappedAmountLine(
            ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
            ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
            D("11905.00"),
            Amount(D("10823")),
            CENT,
            D("10823"),
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_LINE_14: CappedAmountLine(
            output=MEDICAL_SUPPLEMENT_LINE_14,
            base=MEDICAL_SUPPLEMENT_LINE_13,
            base_amount=D("0.00"),
            cap=Amount(D("1504")),
            rounding=CENT,
            result=D("0.00"),
        ),
    }
    # Schedule 7 line 17 "Enter whichever is less: amount from line 13 or line 16.": the
    # contributions available to deduct of 1926 are below the deduction limit of 19800, so the
    # most that may be deducted is the contributions available to deduct.
    assert lesser == {
        # Form T1172 line 3 "Amount from line 1 or 2, whichever is less" and line 7 "Amount from
        # line 3 or 6, whichever is less", for no AIPs.
        RESP_AIPS_CONTRIBUTIONS_COUNTED: LesserOfLine(
            RESP_AIPS_CONTRIBUTIONS_COUNTED,
            ((RESP_AIPS_RECEIVED_PART_A, D("0")), (RESP_AIPS_RRSP_CONTRIBUTIONS, D("0"))),
            D("0"),
        ),
        RESP_AIPS_REDUCTION: LesserOfLine(
            RESP_AIPS_REDUCTION,
            (
                (RESP_AIPS_CONTRIBUTIONS_COUNTED, D("0")),
                (RESP_AIPS_LIMIT_REMAINING, D("50000.00")),
            ),
            D("0"),
        ),
        # Schedule 9 chart for line 33700, line 4 "Enter whichever is less: amount from line 2 or
        # line 3." and line 5 "amount from line 1 or line 4", both 0.
        DEPRECIABLE_GIFT_PROCEEDS_OR_COST: LesserOfLine(
            DEPRECIABLE_GIFT_PROCEEDS_OR_COST,
            ((DEPRECIABLE_GIFT_NET_PROCEEDS, D("0")), (DEPRECIABLE_GIFT_CAPITAL_COST, D("0"))),
            D("0"),
        ),
        DEPRECIABLE_GIFTS: LesserOfLine(
            DEPRECIABLE_GIFTS,
            (
                (DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION, D("0")),
                (DEPRECIABLE_GIFT_PROCEEDS_OR_COST, D("0")),
            ),
            D("0"),
        ),
        # Schedule 9 line 9 "Enter whichever is less: amount A or line 8.": amount A is the net
        # income, 115000, above line 8 (75% of it), so line 9 is line 8 when line 7 is 0. Line 10
        # "amount from line 5 or line 9", line 13 "amount from line 12 or $200." and line 20 "amount
        # from line 16 or line 19".
        CHARITABLE_DONATIONS_LIMIT: LesserOfLine(
            CHARITABLE_DONATIONS_LIMIT,
            ((NET_INCOME, D("115000")), (DONATION_LIMIT_WITH_CAPITAL_GIFTS, D("86250"))),
            D("86250"),
        ),
        CHARITABLE_DONATIONS_CLAIMED: LesserOfLine(
            CHARITABLE_DONATIONS_CLAIMED,
            ((TOTAL_CHARITABLE_DONATIONS, D("0")), (CHARITABLE_DONATIONS_LIMIT, D("86250"))),
            D("0"),
        ),
        DONATIONS_FIRST_TIER: LesserOfLine(
            DONATIONS_FIRST_TIER,
            ((DONATIONS_AND_GIFTS_TOTAL, D("0")), (DONATION_FIRST_TIER_MAXIMUM, D("200.00"))),
            D("0"),
        ),
        HIGH_INCOME_DONATIONS: LesserOfLine(
            HIGH_INCOME_DONATIONS,
            (
                (DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS, D("0")),
                (TAXABLE_INCOME_OVER_DONATION_THRESHOLD, D("0")),
            ),
            D("0"),
        ),
        RRSP_DEDUCTION_MAXIMUM: LesserOfLine(
            RRSP_DEDUCTION_MAXIMUM,
            ((RRSP_CONTRIBUTIONS_AVAILABLE, D("1926")), (RRSP_DEDUCTION_LIMIT, D("19800"))),
            D("1926"),
        ),
        # Form T778 line 7 "Enter whichever amount is the least: line 4, line 5 or line 6.", in
        # that order: lines 4 and 5 are both 0, and the first listed is produced.
        CHILD_CARE_EXPENSES: LesserOfLine(
            CHILD_CARE_EXPENSES,
            (
                (CHILD_CARE_BASIC_LIMIT, D("0")),
                (CHILD_CARE_EXPENSES_PAID, D("0")),
                (CHILD_CARE_EARNED_INCOME_LIMIT, D("73333.33")),
            ),
            D("0"),
        ),
        # Form T1436 line 17.
        BUSINESS_INVESTMENT_LOSS_REDUCTION: LesserOfLine(
            BUSINESS_INVESTMENT_LOSS_REDUCTION,
            (
                (BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE, D("0")),
                (BUSINESS_INVESTMENT_LOSS, D("0")),
            ),
            D("0"),
        ),
        # Schedule 15 line 33.
        FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT: LesserOfLine(
            FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT,
            (
                (FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT, D("0")),
                (FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD, D("8000.00")),
            ),
            D("0"),
        ),
        # Schedule 15 line 40, Step 2's result.
        FHSA_ANNUAL_LIMIT_FROM_STEP_2: LesserOfLine(
            FHSA_ANNUAL_LIMIT_FROM_STEP_2,
            (
                (FHSA_CONTRIBUTIONS_LIMIT, D("0")),
                (FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS, D("8000.00")),
            ),
            D("0"),
        ),
        # Schedule 15 line 51.
        FHSA_MAXIMUM_DEDUCTION: LesserOfLine(
            FHSA_MAXIMUM_DEDUCTION,
            (
                (FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS, D("0")),
                (FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS, D("40000.00")),
            ),
            D("0"),
        ),
        # Form T1436 line 6 "Enter whichever is less: amount from line 4 or line 5.": the total of
        # column C, 0.00, is below the taxable capital gains of 10000.00 (half of the 20000 gain).
        NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM: LesserOfLine(
            NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
            (
                (TOTAL_ADJUSTED_NET_CAPITAL_LOSSES, D("0.00")),
                (TAXABLE_CAPITAL_GAINS, D("10000.00")),
            ),
            D("0.00"),
        ),
        # Form T1436 Chart A column D "Total adjusted net capital losses applied against taxable
        # capital gains in 2025": the lesser of column C and what is left of line 13, 0 for no
        # claim.
        ADJUSTED_LOSSES_APPLIED_1985_TO_1987: LesserOfLine(
            ADJUSTED_LOSSES_APPLIED_1985_TO_1987,
            (
                (ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987, D("0.00")),
                (NET_CAPITAL_LOSSES_OF_OTHER_YEARS, D("0")),
            ),
            D("0.00"),
        ),
        ADJUSTED_LOSSES_APPLIED_1988_AND_1989: LesserOfLine(
            ADJUSTED_LOSSES_APPLIED_1988_AND_1989,
            (
                (ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989, D("0.00")),
                (ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987, D("0.00")),
            ),
            D("0.00"),
        ),
        ADJUSTED_LOSSES_APPLIED_1990_TO_1999: LesserOfLine(
            ADJUSTED_LOSSES_APPLIED_1990_TO_1999,
            (
                (ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999, D("0.00")),
                (ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989, D("0.00")),
            ),
            D("0.00"),
        ),
        ADJUSTED_LOSSES_APPLIED_2001_TO_2024: LesserOfLine(
            ADJUSTED_LOSSES_APPLIED_2001_TO_2024,
            (
                (ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024, D("0.00")),
                (ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999, D("0.00")),
            ),
            D("0.00"),
        ),
    }
    # Schedule 7 line 18 "(cannot be more than the amount on line 17)": the full 1926 is
    # deducted, equal to line 17, so line 20 is line 18.
    assert at_most == {
        RRSP_DEDUCTION: AtMostLine(
            output=RRSP_DEDUCTION,
            amount_kind=RRSP_AMOUNT_DEDUCTED,
            amount_value=D("1926"),
            bound=RRSP_DEDUCTION_MAXIMUM,
            bound_value=D("1926"),
        ),
        # Schedule 15 line 57 (T1 line 20805).
        FHSA_DEDUCTION: AtMostLine(
            output=FHSA_DEDUCTION,
            amount_kind=FHSA_CONTRIBUTIONS_DEDUCTED,
            amount_value=D("0"),
            bound=FHSA_MAXIMUM_DEDUCTION,
            bound_value=D("0"),
        ),
        # Form T1436 line 7 "Enter the amount of losses you want to claim (3).", which is T1 line
        # 25300 and line 13: a claim of 0 against a line 6 of 0.00.
        NET_CAPITAL_LOSSES_OF_OTHER_YEARS: AtMostLine(
            output=NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
            amount_kind=NET_CAPITAL_LOSSES_CLAIMED,
            amount_value=D("0"),
            bound=NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM,
            bound_value=D("0.00"),
        ),
    }
    # Schedule 8 Part 3 lines 11, 12 and 22: employment income of 110000 is above both
    # ceilings, so each band is full and each contribution is its maximum. T1 line 31200: it
    # is above the $65,700 maximum insurable earnings, so the EI premiums are their maximum.
    assert tiers == {
        CPP_BASE_CONTRIBUTIONS: ContributionTierLine(
            CPP_BASE_CONTRIBUTIONS,
            EMPLOYMENT_INCOME,
            D("110000"),
            ContributionTier(Rate(D("0.0495")), D("3500"), D("71300"), D("3356.10")),
            CENT,
            D("67800"),
            D("3356.10"),
        ),
        CPP_FIRST_ADDITIONAL_CONTRIBUTIONS: ContributionTierLine(
            CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
            EMPLOYMENT_INCOME,
            D("110000"),
            ContributionTier(Rate(D("0.01")), D("3500"), D("71300"), D("678.00")),
            CENT,
            D("67800"),
            D("678.00"),
        ),
        CPP_SECOND_ADDITIONAL_CONTRIBUTIONS: ContributionTierLine(
            CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
            EMPLOYMENT_INCOME,
            D("110000"),
            ContributionTier(Rate(D("0.04")), D("71300"), D("81200"), D("396.00")),
            CENT,
            D("9900"),
            D("396.00"),
        ),
        EI_PREMIUMS: ContributionTierLine(
            EI_PREMIUMS,
            EMPLOYMENT_INCOME,
            D("110000"),
            ContributionTier(Rate(D("0.0164")), D("0"), D("65700"), D("1077.48")),
            CENT,
            D("65700"),
            D("1077.48"),
        ),
    }
    # ON428 line 66 "(Line 65 minus $5,710) multiplied by 20% (if negative, enter "0")" and line
    # 67 "(Line 65 minus $7,307) multiplied by 36% (if negative, enter "0")", in that order, on
    # the Ontario tax after credits (line 65, as line 64 is not modelled); each part rounded
    # half-up to the cent.
    assert surcharged == [
        SurchargeTierLine(
            output=ONTARIO_SURTAX,
            base=ONTARIO_TAX_AFTER_CREDITS,
            base_amount=D("7671.98"),
            threshold=D("5710"),
            rate=Rate(D("0.20")),
            rounding=CENT,
            part=D("392.40"),
        ),
        SurchargeTierLine(
            output=ONTARIO_SURTAX,
            base=ONTARIO_TAX_AFTER_CREDITS,
            base_amount=D("7671.98"),
            threshold=D("7307"),
            rate=Rate(D("0.36")),
            rounding=CENT,
            part=D("131.39"),
        ),
    ]
    # ON428 line 89 and its chart, on line 1 "Enter your taxable income from line 26000 of your
    # return", in threshold order: taxable income of 115000 is "more than $72,600 but not more
    # than $200,000", so the four lower tiers each charge their maximum, 300 + 150 + 150 + 150 =
    # 750, and the top tier nothing; each tier rounded half-up to the cent.
    assert premium_tiers == [
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("20000"),
            rate=Rate(D("0.06")),
            rounding=CENT,
            part=D("300"),
            maximum=D("300"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("36000"),
            rate=Rate(D("0.06")),
            rounding=CENT,
            part=D("150"),
            maximum=D("150"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("48000"),
            rate=Rate(D("0.25")),
            rounding=CENT,
            part=D("150"),
            maximum=D("150"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("72000"),
            rate=Rate(D("0.25")),
            rounding=CENT,
            part=D("150"),
            maximum=D("150"),
        ),
        SurchargeTierLine(
            output=ONTARIO_HEALTH_PREMIUM,
            base=TAXABLE_INCOME,
            base_amount=D("115000"),
            threshold=D("200000"),
            rate=Rate(D("0.25")),
            rounding=CENT,
            part=D("0"),
            maximum=D("150"),
        ),
    ]
    # Schedule ON428-A line 17 "Line 15 minus line 16 (if negative, enter "0")" and line 19 "Line
    # 17 multiplied by the percentage from line 18": net income (line 15, from line 13) of 115000
    # less the 32,500.00 threshold (line 16), times 5% (line 18), rounded half-up to the cent.
    assert lift_tiers == [
        SurchargeTierLine(
            output=LIFT_REDUCTION,
            base=NET_INCOME,
            base_amount=D("115000"),
            threshold=D("32500"),
            rate=Rate(D("0.05")),
            rounding=CENT,
            part=D("4125.00"),
        )
    ]
    # Schedule 6 line 18 "Line 16 minus line 17 (if negative, enter "0")", line 20 "Line 18
    # multiplied by the percentage from line 19" and line 22 "Enter whichever is less: amount from
    # line 20 or line 21.": (110000 - 3000) x 27% is above both of line 21's amounts, so line 22
    # is 1633 with no eligible spouse or dependant and 2813 with one, rounded half-up to the cent.
    assert set(cwb_basic_tiers) == {
        SurchargeTierLine(
            output=CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
            base=WORKING_INCOME,
            base_amount=D("110000"),
            threshold=D("3000"),
            rate=Rate(D("0.27")),
            rounding=CENT,
            part=D("1633"),
            maximum=D("1633"),
        ),
        SurchargeTierLine(
            output=CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
            base=WORKING_INCOME,
            base_amount=D("110000"),
            threshold=D("3000"),
            rate=Rate(D("0.27")),
            rounding=CENT,
            part=D("2813"),
            maximum=D("2813"),
        ),
    }
    assert len(cwb_basic_tiers) == 2
    # Schedule 6 line 25 "Line 23 minus line 24 (if negative, enter "0")" and line 27 "Line 25
    # multiplied by the percentage from line 26": (115000 - 26855) x 15% with no eligible spouse
    # or dependant and (115000 - 30639) x 15% with one, rounded half-up to the cent.
    assert set(cwb_reduction_tiers) == {
        SurchargeTierLine(
            output=CWB_REDUCTION_WITHOUT_DEPENDANT,
            base=ADJUSTED_FAMILY_NET_INCOME,
            base_amount=D("115000"),
            threshold=D("26855"),
            rate=Rate(D("0.15")),
            rounding=CENT,
            part=D("13221.75"),
        ),
        SurchargeTierLine(
            output=CWB_REDUCTION_WITH_DEPENDANT,
            base=ADJUSTED_FAMILY_NET_INCOME,
            base_amount=D("115000"),
            threshold=D("30639"),
            rate=Rate(D("0.15")),
            rounding=CENT,
            part=D("12654.15"),
        ),
    }
    assert len(cwb_reduction_tiers) == 2
    assert floored == {
        # T1 line 110 "Line 107 minus line 109 (if negative, enter "0")": no medical expenses.
        MEDICAL_EXPENSES_OVER_THRESHOLD: SubtractedNotBelowZeroLine(
            output=MEDICAL_EXPENSES_OVER_THRESHOLD,
            minuend=MEDICAL_EXPENSES,
            minuend_amount=D("0"),
            subtrahend=MEDICAL_THRESHOLD,
            subtrahend_amount=D("2834"),
            result=D("0"),
        ),
        # ON428 line 41 "Line 36 minus line 40 (if negative, enter "0")".
        ontario.MEDICAL_EXPENSES_OVER_THRESHOLD: SubtractedNotBelowZeroLine(
            output=ontario.MEDICAL_EXPENSES_OVER_THRESHOLD,
            minuend=MEDICAL_EXPENSES,
            minuend_amount=D("0"),
            subtrahend=ontario.MEDICAL_THRESHOLD,
            subtrahend_amount=D("2885"),
            result=D("0"),
        ),
        # T1 line 139 (line 41700) "Line 134 minus line 138 (if negative, enter "0")", with line
        # 134 carrying line 132: no credit against a federal tax of 16951.38.
        FEDERAL_TAX_LESS_CREDITS: SubtractedNotBelowZeroLine(
            output=FEDERAL_TAX_LESS_CREDITS,
            minuend=FEDERAL_TAX_WITH_ITC_RECAPTURE,
            minuend_amount=D("16951.38"),
            subtrahend=CREDITS_AGAINST_FEDERAL_TAX,
            subtrahend_amount=D("0"),
            result=D("16951.38"),
        ),
        # ON479 line 10 "Line 8 minus line 9 (if negative, enter "0")" and line 13 "Line 5 minus
        # line 12 (if negative, enter "0")": Return A's family net income is its own 115000.00
        # (line 7 is 0), 80000.00 over the base, so line 12 is 4000.00 and line 13 is 0 - 4000.00,
        # negative, so 0.
        SENIORS_CARE_INCOME_OVER_BASE: SubtractedNotBelowZeroLine(
            output=SENIORS_CARE_INCOME_OVER_BASE,
            minuend=SENIORS_CARE_FAMILY_NET_INCOME,
            minuend_amount=D("115000.00"),
            subtrahend=SENIORS_CARE_BASE_AMOUNT,
            subtrahend_amount=D("35000.00"),
            result=D("80000.00"),
        ),
        SENIORS_CARE_BEFORE_CLAIM: SubtractedNotBelowZeroLine(
            output=SENIORS_CARE_BEFORE_CLAIM,
            minuend=SENIORS_CARE_AMOUNT,
            minuend_amount=D("0"),
            subtrahend=SENIORS_CARE_REDUCTION,
            subtrahend_amount=D("4000.00"),
            result=D("0"),
        ),
        # Worksheet ON479 "Line 20" line 6 "Line 4 minus line 5 (if negative, enter "0")" and line
        # 11 "Line 9 minus line 10 (if negative, enter "0")": Return A has no payroll entered (0),
        # so line 6 is 0, line 8 is 0 and line 11 is the whole 1.00.
        COOP_EDUCATION_PAYROLL_OVER_THRESHOLD: SubtractedNotBelowZeroLine(
            output=COOP_EDUCATION_PAYROLL_OVER_THRESHOLD,
            minuend=COOP_EDUCATION_PAYROLL,
            minuend_amount=D("0"),
            subtrahend=COOP_EDUCATION_PAYROLL_THRESHOLD,
            subtrahend_amount=D("400000.00"),
            result=D("0"),
        ),
        COOP_EDUCATION_REMAINING_SHARE: SubtractedNotBelowZeroLine(
            output=COOP_EDUCATION_REMAINING_SHARE,
            minuend=COOP_EDUCATION_FULL_SHARE,
            minuend_amount=D("1.00"),
            subtrahend=COOP_EDUCATION_PHASE_OUT_SHARE,
            subtrahend_amount=D("0"),
            result=D("1.00"),
        ),
        # Schedule 9 line 16 "Line 14 minus line 15 (if negative, enter "0")" and line 19 "Line 17
        # minus line 18 (if negative, enter "0")": the taxable income of 115000 is below the
        # threshold of 253414.00. Federal Worksheet line 5 "Line 3 minus line 4 (if negative,
        # enter "0")": 3194.87 is below 8319.38.
        DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS: SubtractedNotBelowZeroLine(
            output=DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS,
            minuend=DONATIONS_OVER_FIRST_TIER,
            minuend_amount=D("0"),
            subtrahend=ECOLOGICAL_GIFTS_BEFORE_2016,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        TAXABLE_INCOME_OVER_DONATION_THRESHOLD: SubtractedNotBelowZeroLine(
            output=TAXABLE_INCOME_OVER_DONATION_THRESHOLD,
            minuend=TAXABLE_INCOME,
            minuend_amount=D("115000"),
            subtrahend=DONATION_HIGH_INCOME_THRESHOLD,
            subtrahend_amount=D("253414.00"),
            result=D("0"),
        ),
        TOP_UP_EXCESS: SubtractedNotBelowZeroLine(
            output=TOP_UP_EXCESS,
            minuend=TOP_UP_CREDITS_BASE,
            minuend_amount=D("3194.87"),
            subtrahend=TOP_UP_THRESHOLD,
            subtrahend_amount=D("8319.38"),
            result=D("0"),
        ),
        # Worksheet ON479 column 1 line 3 "Line 1 minus line 2 (cannot be negative)": line 1 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_1_LINE_3: SubtractedNotBelowZeroLine(
            output=ontario.POLITICAL_CREDIT_COLUMN_1_LINE_3,
            minuend=ontario.POLITICAL_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=ontario.POLITICAL_CREDIT_COLUMN_1_LINE_2,
            subtrahend_amount=D("0.00"),
            result=D("0"),
        ),
        # Worksheet ON479 column 2 line 3 "Line 1 minus line 2 (cannot be negative)": line 1 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_2_LINE_3: SubtractedNotBelowZeroLine(
            output=ontario.POLITICAL_CREDIT_COLUMN_2_LINE_3,
            minuend=ontario.POLITICAL_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=ontario.POLITICAL_CREDIT_COLUMN_2_LINE_2,
            subtrahend_amount=D("500.05"),
            result=D("0"),
        ),
        # Worksheet ON479 column 3 line 3 "Line 1 minus line 2 (cannot be negative)": line 1 is 0.
        ontario.POLITICAL_CREDIT_COLUMN_3_LINE_3: SubtractedNotBelowZeroLine(
            output=ontario.POLITICAL_CREDIT_COLUMN_3_LINE_3,
            minuend=ontario.POLITICAL_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=ontario.POLITICAL_CREDIT_COLUMN_3_LINE_2,
            subtrahend_amount=D("1666.82"),
            result=D("0"),
        ),
        # Federal Worksheet column 1 line 3 "Line 1 minus line 2 (if negative, enter "0") =": line 1
        # is 0.
        POLITICAL_CREDIT_COLUMN_1_LINE_3: SubtractedNotBelowZeroLine(
            output=POLITICAL_CREDIT_COLUMN_1_LINE_3,
            minuend=POLITICAL_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=POLITICAL_CREDIT_COLUMN_1_LINE_2,
            subtrahend_amount=D("0.00"),
            result=D("0"),
        ),
        # Federal Worksheet column 2 line 3 "Line 1 minus line 2 (if negative, enter "0") =": line 1
        # is 0.
        POLITICAL_CREDIT_COLUMN_2_LINE_3: SubtractedNotBelowZeroLine(
            output=POLITICAL_CREDIT_COLUMN_2_LINE_3,
            minuend=POLITICAL_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=POLITICAL_CREDIT_COLUMN_2_LINE_2,
            subtrahend_amount=D("400.00"),
            result=D("0"),
        ),
        # Federal Worksheet column 3 line 3 "Line 1 minus line 2 (if negative, enter "0") =": line 1
        # is 0.
        POLITICAL_CREDIT_COLUMN_3_LINE_3: SubtractedNotBelowZeroLine(
            output=POLITICAL_CREDIT_COLUMN_3_LINE_3,
            minuend=POLITICAL_CONTRIBUTIONS,
            minuend_amount=D("0"),
            subtrahend=POLITICAL_CREDIT_COLUMN_3_LINE_2,
            subtrahend_amount=D("750.00"),
            result=D("0"),
        ),
        NET_INCOME: SubtractedNotBelowZeroLine(
            output=NET_INCOME,
            minuend=TOTAL_INCOME,
            minuend_amount=D("120000"),
            subtrahend=DEDUCTIONS_FROM_TOTAL_INCOME,
            subtrahend_amount=D("5000"),
            result=D("115000"),
        ),
        TAXABLE_INCOME: SubtractedNotBelowZeroLine(
            output=TAXABLE_INCOME,
            minuend=NET_INCOME,
            minuend_amount=D("115000"),
            subtrahend=DEDUCTIONS_FROM_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("115000"),
        ),
        # Each form's credits come off its basic tax, not below zero; here both taxes exceed
        # their credits.
        FEDERAL_TAX_AFTER_CREDITS: SubtractedNotBelowZeroLine(
            output=FEDERAL_TAX_AFTER_CREDITS,
            minuend=FEDERAL_BASIC_TAX,
            minuend_amount=D("20146.25"),
            subtrahend=CREDITS_AGAINST_BASIC_FEDERAL_TAX,
            subtrahend_amount=D("3194.87"),
            result=D("16951.38"),
        ),
        ONTARIO_TAX_AFTER_CREDITS: SubtractedNotBelowZeroLine(
            output=ONTARIO_TAX_AFTER_CREDITS,
            minuend=ONTARIO_BASIC_TAX,
            minuend_amount=D("8539.60"),
            subtrahend=ontario.NON_REFUNDABLE_TAX_CREDITS,
            subtrahend_amount=D("867.62"),
            result=D("7671.98"),
        ),
        # Schedule 5 line 5 "Line 3 minus line 4 (if negative, enter "0")": line 3 is line 1,
        # the basic personal amount, as line 2 is not triggered; line 4 the dependant's net
        # income, entered as 0.
        ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT: SubtractedNotBelowZeroLine(
            output=ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
            minuend=BASIC_PERSONAL_AMOUNT,
            minuend_amount=D("16129.00"),
            subtrahend=DEPENDANT_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("16129.00"),
        ),
        # Federal Worksheet line 4 "Line 2 minus line 3 (if negative, enter "0")": the net income
        # 115000 less the income threshold 45522.00.
        AGE_INCOME_OVER_THRESHOLD: SubtractedNotBelowZeroLine(
            output=AGE_INCOME_OVER_THRESHOLD,
            minuend=NET_INCOME,
            minuend_amount=D("115000"),
            subtrahend=AGE_INCOME_THRESHOLD,
            subtrahend_amount=D("45522.00"),
            result=D("69478.00"),
        ),
        # Federal Worksheet line 7 "Line 1 minus line 6 (if negative, enter "0")": 9028.00 less
        # 10421.70 is negative, so 0.
        AGE_AMOUNT_BEFORE_COUNT: SubtractedNotBelowZeroLine(
            output=AGE_AMOUNT_BEFORE_COUNT,
            minuend=AGE_MAXIMUM,
            minuend_amount=D("9028.00"),
            subtrahend=AGE_REDUCTION,
            subtrahend_amount=D("10421.70"),
            result=D("0"),
        ),
        # Schedule 5 line 5 of the line 30300 part "Line 3 minus line 4 (if negative, enter "0")",
        # with the spouse's net income entered as 0.
        SPOUSE_AMOUNT_BEFORE_COUNT: SubtractedNotBelowZeroLine(
            output=SPOUSE_AMOUNT_BEFORE_COUNT,
            minuend=SPOUSE_AMOUNT_BASIS,
            minuend_amount=D("16129.00"),
            subtrahend=SPOUSE_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("16129.00"),
        ),
        # Schedule 5 line 3 and line 5 of the line 30425 part, "Line 1 minus line 2" and "Line 3
        # minus line 4", each "(if negative, enter "0")".
        SPOUSE_CAREGIVER_BEFORE_MAXIMUM: SubtractedNotBelowZeroLine(
            output=SPOUSE_CAREGIVER_BEFORE_MAXIMUM,
            minuend=SPOUSE_CAREGIVER_BASE,
            minuend_amount=D("28798.00"),
            subtrahend=SPOUSE_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("28798.00"),
        ),
        SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT: SubtractedNotBelowZeroLine(
            output=SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT,
            minuend=SPOUSE_CAREGIVER_LIMIT,
            minuend_amount=D("8601"),
            subtrahend=SPOUSE_AMOUNT,
            subtrahend_amount=D("0"),
            result=D("8601"),
        ),
        # Worksheet ON428 line 4 "Line 2 minus line 3 (if negative, enter "0")": the net income
        # 115000 less the income threshold 46330.00.
        ontario.AGE_INCOME_OVER_THRESHOLD: SubtractedNotBelowZeroLine(
            output=ontario.AGE_INCOME_OVER_THRESHOLD,
            minuend=NET_INCOME,
            minuend_amount=D("115000"),
            subtrahend=ontario.AGE_INCOME_THRESHOLD,
            subtrahend_amount=D("46330.00"),
            result=D("68670.00"),
        ),
        # Worksheet ON428 line 7 "Line 1 minus line 6 (if negative, enter "0")": 6223.00 less
        # 10300.50 is negative, so 0.
        ontario.AGE_AMOUNT_BEFORE_COUNT: SubtractedNotBelowZeroLine(
            output=ontario.AGE_AMOUNT_BEFORE_COUNT,
            minuend=ontario.AGE_MAXIMUM,
            minuend_amount=D("6223.00"),
            subtrahend=ontario.AGE_REDUCTION,
            subtrahend_amount=D("10300.50"),
            result=D("0"),
        ),
        # ON428 line 13 "Line 11 minus line 12 (if negative, enter "0")", before its maximum,
        # with the spouse's net income entered as 0.
        ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM: SubtractedNotBelowZeroLine(
            output=ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM,
            minuend=ontario.SPOUSE_BASE,
            minuend_amount=D("11905.00"),
            subtrahend=SPOUSE_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("11905.00"),
        ),
        # ON428 line 16 "Line 14 minus line 15 (if negative, enter "0")", before its maximum.
        ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM: SubtractedNotBelowZeroLine(
            output=ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
            minuend=ELIGIBLE_DEPENDANT_BASE,
            minuend_amount=D("11905.00"),
            subtrahend=DEPENDANT_NET_INCOME,
            subtrahend_amount=D("0"),
            result=D("11905.00"),
        ),
        # ON428 line 58 "Line 56 minus line 57 (if negative, enter "0")" and line 71 "Line 69
        # minus line 70 (if negative, enter "0")": the credit is 0.
        ontario.ONTARIO_TAX_LESS_DIVIDEND_CREDIT: SubtractedNotBelowZeroLine(
            output=ontario.ONTARIO_TAX_LESS_DIVIDEND_CREDIT,
            minuend=ontario.ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT,
            minuend_amount=D("7671.98"),
            subtrahend=ontario.DIVIDEND_TAX_CREDIT,
            subtrahend_amount=D("0"),
            result=D("7671.98"),
        ),
        ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT: SubtractedNotBelowZeroLine(
            output=ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT,
            minuend=ONTARIO_TAX_WITH_SURTAX,
            minuend_amount=D("8195.77"),
            subtrahend=ontario.DIVIDEND_CREDIT_FROM_LINE_57,
            subtrahend_amount=D("0"),
            result=D("8195.77"),
        ),
        # ON428 line 81 "Line 73 minus line 80 (if negative, enter "0")".
        ONTARIO_TAX_AFTER_REDUCTION: SubtractedNotBelowZeroLine(
            output=ONTARIO_TAX_AFTER_REDUCTION,
            minuend=ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT,
            minuend_amount=D("8195.77"),
            subtrahend=ONTARIO_TAX_REDUCTION,
            subtrahend_amount=D("0"),
            result=D("8195.77"),
        ),
        # Schedule ON428-A line 20 "Line 14 minus line 19 (if negative, enter "0")": the
        # reduction of 4125.00 exceeds the 875, so the credit (ON428 line 85) is 0.
        LIFT_CREDIT: SubtractedNotBelowZeroLine(
            output=LIFT_CREDIT,
            minuend=LIFT_MAXIMUM_CREDIT,
            minuend_amount=D("875"),
            subtrahend=LIFT_REDUCTION,
            subtrahend_amount=D("4125.00"),
            result=D("0"),
        ),
        # T1 line 48400 "Refund": the total credits of 25000 less the total payable of 25897.15 is
        # not above zero, so the refund is 0 (the balance owing of 897.15 is line 48500).
        REFUND: SubtractedNotBelowZeroLine(
            output=REFUND,
            minuend=TOTAL_CREDITS,
            minuend_amount=D("25000"),
            subtrahend=TOTAL_PAYABLE,
            subtrahend_amount=D("25897.15"),
            result=D("0"),
        ),
        # ON428 line 86 "Line 84 minus line 85 (if negative, enter "0")".
        ONTARIO_TAX_AFTER_LIFT_CREDIT: SubtractedNotBelowZeroLine(
            output=ONTARIO_TAX_AFTER_LIFT_CREDIT,
            minuend=ONTARIO_TAX_AFTER_REDUCTION,
            minuend_amount=D("8195.77"),
            subtrahend=LIFT_CREDIT,
            subtrahend_amount=D("0"),
            result=D("8195.77"),
        ),
        # ON428 line 88 "Line 86 minus line 87 (if negative, enter "0")": line 87 is 0.
        ONTARIO_TAX_AFTER_FOOD_CREDIT: SubtractedNotBelowZeroLine(
            output=ONTARIO_TAX_AFTER_FOOD_CREDIT,
            minuend=ONTARIO_TAX_AFTER_LIFT_CREDIT,
            minuend_amount=D("8195.77"),
            subtrahend=COMMUNITY_FOOD_PROGRAM_CREDIT,
            subtrahend_amount=D("0.00"),
            result=D("8195.77"),
        ),
        # Schedule 6 line 28 "Line 22 minus line 27 (if negative, enter "0")": the reduction of
        # 13221.75 exceeds the 1633, and that of 12654.15 the 2813, so the benefit is 0 with or
        # without an eligible dependant.
        CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT: SubtractedNotBelowZeroLine(
            output=CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
            minuend=CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
            minuend_amount=D("1633"),
            subtrahend=CWB_REDUCTION_WITHOUT_DEPENDANT,
            subtrahend_amount=D("13221.75"),
            result=D("0"),
        ),
        CANADA_WORKERS_BENEFIT_WITH_DEPENDANT: SubtractedNotBelowZeroLine(
            output=CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
            minuend=CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
            minuend_amount=D("2813"),
            subtrahend=CWB_REDUCTION_WITH_DEPENDANT,
            subtrahend_amount=D("12654.15"),
            result=D("0"),
        ),
        # Schedule 15 line 12.
        FHSA_EXCESS_DESIGNATED_WITHDRAWALS: SubtractedNotBelowZeroLine(
            output=FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
            minuend=FHSA_DESIGNATED_WITHDRAWALS_IN_2025,
            minuend_amount=D("0"),
            subtrahend=FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 13.
        FHSA_CONTRIBUTIONS_LIMIT: SubtractedNotBelowZeroLine(
            output=FHSA_CONTRIBUTIONS_LIMIT,
            minuend=FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT,
            minuend_amount=D("0"),
            subtrahend=FHSA_EXCESS_DESIGNATED_WITHDRAWALS,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 29.
        FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT: SubtractedNotBelowZeroLine(
            output=FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT,
            minuend=FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS,
            minuend_amount=D("0"),
            subtrahend=FHSA_VARIABLE_H_AMOUNT,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        # Schedule 15 line 39.
        FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS: SubtractedNotBelowZeroLine(
            output=FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS,
            minuend=FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD,
            minuend_amount=D("8000.00"),
            subtrahend=FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS,
            subtrahend_amount=D("0"),
            result=D("8000.00"),
        ),
        # Schedule 15 line 50.
        FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS: SubtractedNotBelowZeroLine(
            output=FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS,
            minuend=FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS,
            minuend_amount=D("40000.00"),
            subtrahend=FHSA_NET_RRSP_TRANSFER_AMOUNT,
            subtrahend_amount=D("0"),
            result=D("40000.00"),
        ),
        # Federal Worksheet "Line 45200 - Refundable medical expense supplement" (T1 line 154),
        # Return A: line 21500 and line 33200 are 0, so line 11 and line 13 are 0.
        MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5: SubtractedNotBelowZeroLine(
            output=MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5,
            minuend=MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3,
            minuend_amount=D("0"),
            subtrahend=MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4,
            subtrahend_amount=D("0"),
            result=D("0"),
        ),
        MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME: SubtractedNotBelowZeroLine(
            output=MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME,
            minuend=MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS,
            minuend_amount=D("110000"),
            subtrahend=MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS,
            subtrahend_amount=D("2000"),
            result=D("108000"),
        ),
        MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5: SubtractedNotBelowZeroLine(
            output=MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5,
            minuend=MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3,
            minuend_amount=D("115000.00"),
            subtrahend=UCCB_AND_RDSP_INCOME,
            subtrahend_amount=D("0"),
            result=D("115000.00"),
        ),
        MEDICAL_SUPPLEMENT_LINE_8: SubtractedNotBelowZeroLine(
            output=MEDICAL_SUPPLEMENT_LINE_8,
            minuend=MEDICAL_SUPPLEMENT_LINE_6,
            minuend_amount=D("115000.00"),
            subtrahend=MEDICAL_SUPPLEMENT_INCOME_THRESHOLD,
            subtrahend_amount=D("33294.00"),
            result=D("81706.00"),
        ),
        MEDICAL_SUPPLEMENT_LINE_16: SubtractedNotBelowZeroLine(
            output=MEDICAL_SUPPLEMENT_LINE_16,
            minuend=MEDICAL_SUPPLEMENT_LINE_14,
            minuend_amount=D("0.00"),
            subtrahend=MEDICAL_SUPPLEMENT_LINE_15,
            subtrahend_amount=D("4085.30"),
            result=D("0"),
        ),
    }
    # Form T1221 line 4 "Add lines 1 to 3.": Return A has no slips, so no items and a total of 0.
    assert record_totals == {
        FLOW_THROUGH_SHARE_EXPENSES: RecordTotalLine(
            FLOW_THROUGH_SHARE_EXPENSES, FLOW_THROUGH_SHARE_SLIP_EXPENSES, (), D("0")
        ),
    }
    # Worksheet ON479 "Line 20" line 8 "Line 6 divided by line 7": 0 divided by 200,000.00.
    assert quotients == {
        COOP_EDUCATION_PHASE_OUT_SHARE: QuotientLine(
            output=COOP_EDUCATION_PHASE_OUT_SHARE,
            dividend=COOP_EDUCATION_PAYROLL_OVER_THRESHOLD,
            dividend_amount=D("0"),
            divisor=COOP_EDUCATION_PAYROLL_RANGE,
            divisor_amount=D("200000.00"),
            result=D("0"),
        ),
    }
    # ON479 line 63260, the number of eligible work placements: Return A claims none.
    assert record_counts == {
        COOP_EDUCATION_PLACEMENT_COUNT: RecordCountLine(
            COOP_EDUCATION_PLACEMENT_COUNT, COOP_EDUCATION_PLACEMENTS, 0
        ),
    }
    # ON479 line 20 and line 63300, the total of the placements' line 13: no placements, 0.
    assert placement_credits == []
    assert items_totals == {
        COOP_EDUCATION_CREDIT: ItemsTotalLine(COOP_EDUCATION_CREDIT, (), D("0"))
    }
    # T1 line 45300: Schedule 6 line 28 for Return A's family status, no eligible spouse and 0
    # Schedule 6 eligible dependants (line 38100), so the amounts with neither.
    assert chosen == {
        # Form T1172: a count of 0 (Part A does not apply) chooses Part B's line 13.
        RESP_AIPS_ADDITIONAL_TAX: ChosenByCountLine(
            output=RESP_AIPS_ADDITIONAL_TAX,
            count_kind=RESP_AIPS_PART_A_APPLIES,
            count=0,
            chosen_kind=RESP_AIPS_PART_B_TAX,
            chosen_value=D("0"),
        ),
        # Line 25000: line 9 is not over $93,454 and no amount was entered on line 14600, so
        # line 14700 (0 here) twice.
        OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT: ChosenByCountLine(
            output=OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
            count_kind=OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
            count=0,
            chosen_kind=INCOME_SUPPORT_BENEFITS,
            chosen_value=D("0"),
        ),
        OTHER_PAYMENTS_DEDUCTION: ChosenByCountLine(
            output=OTHER_PAYMENTS_DEDUCTION,
            count_kind=OTHER_PAYMENTS_WORKSHEET_REQUIRED,
            count=0,
            chosen_kind=INCOME_SUPPORT_BENEFITS,
            chosen_value=D("0"),
        ),
        CANADA_WORKERS_BENEFIT: ChosenByCountLine(
            output=CANADA_WORKERS_BENEFIT,
            count_kind=CWB_ELIGIBLE_DEPENDANTS,
            count=0,
            chosen_kind=CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
            chosen_value=D("0"),
        ),
        # Schedule 15 line 40.
        FHSA_ANNUAL_LIMIT: ChosenByCountLine(
            output=FHSA_ANNUAL_LIMIT,
            count_kind=FHSA_MAXIMUM_PARTICIPATION_PERIOD_ENDED,
            count=0,
            chosen_kind=FHSA_ANNUAL_LIMIT_FROM_STEP_2,
            chosen_value=D("0"),
        ),
    }

    # ON479 line 16: the worksheet's column for contributions of 0 (line 63110), column 1. T1 line
    # 135: the Federal Worksheet's column for contributions of 0 (line 40900), column 1, then the
    # shortcut's $1,275 against the contributions: not reached, so the column stands.
    assert ranged == {
        ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM: ChosenByRangeLine(
            output=ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM,
            tested_kind=ontario.POLITICAL_CONTRIBUTIONS,
            tested_value=D("0"),
            chosen_kind=ontario.POLITICAL_CREDIT_COLUMN_1_LINE_7,
            chosen_value=D("0.00"),
        ),
        POLITICAL_CREDIT_CHOSEN_COLUMN: ChosenByRangeLine(
            output=POLITICAL_CREDIT_CHOSEN_COLUMN,
            tested_kind=POLITICAL_CONTRIBUTIONS,
            tested_value=D("0"),
            chosen_kind=POLITICAL_CREDIT_COLUMN_1_LINE_7,
            chosen_value=D("0.00"),
        ),
        POLITICAL_CREDIT_BEFORE_MAXIMUM: ChosenByRangeLine(
            output=POLITICAL_CREDIT_BEFORE_MAXIMUM,
            tested_kind=POLITICAL_CREDIT_SHORTCUT_THRESHOLD,
            tested_value=D("1275"),
            chosen_kind=POLITICAL_CREDIT_CHOSEN_COLUMN,
            chosen_value=D("0.00"),
        ),
    }

    assert totals[FEDERAL_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[FEDERAL_BASIC_TAX].base_amount == D("115000")
    assert totals[FEDERAL_BASIC_TAX].amount == D("20146.25")
    assert totals[ONTARIO_BASIC_TAX].base == TAXABLE_INCOME
    assert totals[ONTARIO_BASIC_TAX].amount == D("8539.60")
    # One line per tax for the bracket column the taxable income falls in, read like the form:
    # T1 lines 71 to 76 and ON428 lines 3 to 8.
    columns = [line for line in trace if isinstance(line, BracketColumnLine)]
    assert len(columns) == 2
    assert set(columns) == {
        BracketColumnLine(
            lower=D("114750"),
            rate=D("0.26"),
            excess=D("250"),
            tax_at_start=D("20081.25"),
            tax=D("20146.25"),
        ),
        BracketColumnLine(
            lower=D("105775"),
            rate=D("0.1116"),
            excess=D("9225"),
            tax_at_start=D("7510.09"),
            tax=D("8539.60"),
        ),
    }
    # T1 line 111 (line 33199): Return A has no other dependants, so no per-dependant lines and a
    # total of 0.
    assert [
        line
        for line in trace
        if isinstance(line, OtherDependantMedicalLine | ItemsTotalLine)
        and line.output == OTHER_DEPENDANTS_MEDICAL
    ] == [ItemsTotalLine(output=OTHER_DEPENDANTS_MEDICAL, items=(), total=D("0"))]


def test_each_capability_runs_after_what_it_consumes() -> None:
    order = service().compose(CA_ON, 2025).order

    assert len(order) == 344
    position = {kind: i for i, capability in enumerate(order) for kind in capability.produces}
    assert position[TAXABLE_CAPITAL_GAINS] < position[TOTAL_INCOME] < position[NET_INCOME]
    assert (
        position[INVESTMENT_INCOME_BEFORE_PRIOR_YEARS]
        < position[INTEREST_AND_OTHER_INVESTMENT_INCOME]
    )
    assert position[INTEREST_AND_OTHER_INVESTMENT_INCOME] < position[TOTAL_INCOME]
    assert position[INCOME_SUPPORT_BENEFITS] < position[TOTAL_INCOME]
    assert (
        position[SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE]
        < position[TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE]
    )
    assert position[SLIP_TAXABLE_DIVIDENDS] < position[TAXABLE_DIVIDENDS] < position[TOTAL_INCOME]
    assert (
        position[ELIGIBLE_DIVIDENDS_GROSSED_UP]
        < position[DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP]
        < position[TAXABLE_DIVIDENDS]
    )
    assert position[OTHER_DIVIDENDS_GROSSED_UP] < position[DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP]
    assert position[OTHER_DIVIDENDS_GROSSED_UP] < position[TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE]
    assert (
        position[DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP]
        < position[DIVIDENDS_AMOUNT_A]
        < position[DIVIDENDS_AMOUNT_A_LESS_B]
        < position[ELIGIBLE_DIVIDENDS_CREDIT]
        < position[NO_SLIP_DIVIDEND_TAX_CREDIT]
        < position[DIVIDEND_TAX_CREDIT]
        < position[CREDITS_AGAINST_BASIC_FEDERAL_TAX]
    )
    assert (
        position[OTHER_DIVIDENDS_GROSSED_UP]
        < position[DIVIDENDS_AMOUNT_B]
        < position[OTHER_DIVIDENDS_CREDIT]
        < position[NO_SLIP_DIVIDEND_TAX_CREDIT]
    )
    assert position[DIVIDENDS_AMOUNT_B] < position[DIVIDENDS_AMOUNT_A_LESS_B]
    assert position[SLIP_DIVIDEND_TAX_CREDIT] < position[DIVIDEND_TAX_CREDIT]
    # T1 line 23400 is total income less the deductions, before line 23600 floors it.
    assert position[TOTAL_INCOME] < position[NET_INCOME_BEFORE_ADJUSTMENTS]
    assert position[DEDUCTIONS_FROM_TOTAL_INCOME] < position[NET_INCOME_BEFORE_ADJUSTMENTS]
    # The deductions Step 3 adds are all computed before line 23300 adds them.
    assert (
        position[CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES]
        < position[DEDUCTIONS_FROM_TOTAL_INCOME]
    )
    assert position[ALLOWABLE_BUSINESS_INVESTMENT_LOSS] < position[DEDUCTIONS_FROM_TOTAL_INCOME]
    assert position[FHSA_DEDUCTION] < position[DEDUCTIONS_FROM_TOTAL_INCOME]
    # Form T1436: lines 7 and 14, then 15, then 17 (which reads line 16 as well), 18 and 20.
    assert (
        position[CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024]
        < position[BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE]
        < position[BUSINESS_INVESTMENT_LOSS_REDUCTION]
        < position[BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION]
        < position[ALLOWABLE_BUSINESS_INVESTMENT_LOSS]
    )
    assert (
        position[OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024]
        < position[BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE]
    )
    # Schedule 15: Step 2 before line 40, line 40 before Step 3's lines 43 to 51, the deduction
    # (line 57) after the maximum (line 51), and line 58 after the deduction.
    assert (
        position[FHSA_CONTRIBUTIONS_LIMIT]
        < position[FHSA_ANNUAL_LIMIT_FROM_STEP_2]
        < position[FHSA_ANNUAL_LIMIT]
        < position[FHSA_TOTAL_ANNUAL_LIMITS]
        < position[FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS]
        < position[FHSA_MAXIMUM_DEDUCTION]
        < position[FHSA_DEDUCTION]
        < position[FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD]
    )
    assert (
        position[FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD] < position[FHSA_ANNUAL_LIMIT]
    )
    assert (
        position[FHSA_NET_RRSP_TRANSFER_AMOUNT]
        < position[FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS]
    )
    assert position[FHSA_ANNUAL_AMOUNT] < position[FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD]
    assert (
        position[FHSA_ANNUAL_AMOUNT_FOR_2024]
        < position[FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD]
    )
    assert position[FHSA_LIFETIME_LIMIT] < position[FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS]
    assert (
        position[FHSA_CONTRIBUTIONS_AVAILABLE] < position[FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD]
    )
    assert position[DEDUCTIONS_FROM_TOTAL_INCOME] < position[NET_INCOME]
    assert position[RRSP_CONTRIBUTIONS_AVAILABLE] < position[RRSP_DEDUCTION_MAXIMUM]
    assert position[RRSP_DEDUCTION_MAXIMUM] < position[RRSP_DEDUCTION]
    assert position[RRSP_DEDUCTION] < position[UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD]
    assert position[RRSP_DEDUCTION] < position[DEDUCTIONS_FROM_TOTAL_INCOME]
    assert position[CPP_FIRST_ADDITIONAL_CONTRIBUTIONS] < position[CPP_ENHANCED_CONTRIBUTIONS]
    assert position[CPP_SECOND_ADDITIONAL_CONTRIBUTIONS] < position[CPP_ENHANCED_CONTRIBUTIONS]
    assert position[CPP_ENHANCED_CONTRIBUTIONS] < position[DEDUCTIONS_FROM_TOTAL_INCOME]
    for limit in (
        CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
        CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
        CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
    ):
        assert position[limit] < position[CHILD_CARE_BASIC_LIMIT]
    assert position[CHILD_CARE_BASIC_LIMIT] < position[CHILD_CARE_EXPENSES]
    assert (
        position[CHILD_CARE_EARNED_INCOME]
        < position[CHILD_CARE_EARNED_INCOME_LIMIT]
        < position[CHILD_CARE_EXPENSES]
        < position[DEDUCTIONS_FROM_TOTAL_INCOME]
    )
    assert position[CPP_BASE_CONTRIBUTIONS] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert position[CPP_BASE_CONTRIBUTIONS] < position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert position[EI_PREMIUMS] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert position[EI_PREMIUMS] < position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert position[NET_INCOME] < position[TAXABLE_INCOME]
    assert position[DEDUCTIONS_FROM_NET_INCOME] < position[TAXABLE_INCOME]
    # Form T1436: column C of each row, then line 4, line 6 (which reads line 12700), line 7 (T1
    # line 25300, also line 13), then column D oldest row first, each reading what the older rows
    # left of line 13, then columns E and G; and the deduction before taxable income.
    assert position[TAXABLE_CAPITAL_GAINS] < position[NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM]
    assert (
        max(
            position[ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987],
            position[ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989],
            position[ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999],
            position[ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024],
        )
        < position[TOTAL_ADJUSTED_NET_CAPITAL_LOSSES]
        < position[NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM]
        < position[NET_CAPITAL_LOSSES_OF_OTHER_YEARS]
        < position[ADJUSTED_LOSSES_APPLIED_1985_TO_1987]
        < position[ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987]
        < position[ADJUSTED_LOSSES_APPLIED_1988_AND_1989]
        < position[ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989]
        < position[ADJUSTED_LOSSES_APPLIED_1990_TO_1999]
        < position[ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999]
        < position[ADJUSTED_LOSSES_APPLIED_2001_TO_2024]
    )
    assert (
        position[ADJUSTED_LOSSES_APPLIED_1985_TO_1987]
        < position[REMAINING_ADJUSTED_LOSSES_1985_TO_1987]
    )
    assert (
        position[REMAINING_ADJUSTED_LOSSES_1985_TO_1987]
        < position[NET_CAPITAL_LOSS_BALANCE_1985_TO_1987]
    )
    assert (
        position[ADJUSTED_LOSSES_APPLIED_1988_AND_1989]
        < position[REMAINING_ADJUSTED_LOSSES_1988_AND_1989]
    )
    assert (
        position[REMAINING_ADJUSTED_LOSSES_1988_AND_1989]
        < position[NET_CAPITAL_LOSS_BALANCE_1988_AND_1989]
    )
    assert (
        position[ADJUSTED_LOSSES_APPLIED_1990_TO_1999]
        < position[REMAINING_ADJUSTED_LOSSES_1990_TO_1999]
    )
    assert (
        position[REMAINING_ADJUSTED_LOSSES_1990_TO_1999]
        < position[NET_CAPITAL_LOSS_BALANCE_1990_TO_1999]
    )
    assert (
        position[ADJUSTED_LOSSES_APPLIED_2001_TO_2024]
        < position[REMAINING_ADJUSTED_LOSSES_2001_TO_2024]
    )
    assert (
        position[REMAINING_ADJUSTED_LOSSES_2001_TO_2024]
        < position[NET_CAPITAL_LOSS_BALANCE_2001_TO_2024]
    )
    assert position[NET_CAPITAL_LOSSES_OF_OTHER_YEARS] < position[DEDUCTIONS_FROM_NET_INCOME]
    # The Federal Worksheet's "Line 25000 - Other payments deduction": line 1 is the net income.
    assert position[NET_INCOME] < position[NET_INCOME_LESS_UCCB_AND_RDSP_INCOME]
    assert position[UCCB_AND_RDSP_INCOME] < position[NET_INCOME_LESS_UCCB_AND_RDSP_INCOME]
    # Line 9 feeds nothing yet: the count of line 9 over $93,454 is a starting count.
    assert position[NET_INCOME_LESS_UCCB_AND_RDSP_INCOME] < position[OTHER_PAYMENTS_LIMIT_INCOME]
    assert (
        position[INCOME_SUPPORT_BENEFITS]
        < position[OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT]
        < position[OTHER_PAYMENTS_DEDUCTION]
        < position[DEDUCTIONS_FROM_NET_INCOME]
    )
    assert position[UCCB_AND_RDSP_INCOME_REPAYMENTS] < position[OTHER_PAYMENTS_LIMIT_INCOME]
    assert position[TAXABLE_INCOME] < position[FEDERAL_BASIC_TAX]
    assert position[TAXABLE_INCOME] < position[ONTARIO_BASIC_TAX]
    assert position[FEDERAL_BASIC_TAX] < position[FEDERAL_TAX_AFTER_CREDITS]
    assert position[ONTARIO_BASIC_TAX] < position[ONTARIO_TAX_AFTER_CREDITS]
    assert position[NET_INCOME] < position[BASIC_PERSONAL_AMOUNT]
    assert position[BASIC_PERSONAL_AMOUNT] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert position[CANADA_EMPLOYMENT_AMOUNT] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert (
        position[BASIC_PERSONAL_AMOUNT]
        < position[ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT]
        < position[ELIGIBLE_DEPENDANT_AMOUNT]
        < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    )
    assert position[CAREGIVER_AMOUNT] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    # T1 lines 107 to 112, each after the lines it reads, and line 33200 before the line 33500 sum
    # that adds it (line 113).
    assert position[NET_INCOME] < position[MEDICAL_NET_INCOME_SHARE] < position[MEDICAL_THRESHOLD]
    assert position[MEDICAL_THRESHOLD] < position[MEDICAL_EXPENSES_OVER_THRESHOLD]
    assert position[MEDICAL_EXPENSES_OVER_THRESHOLD] < position[MEDICAL_CLAIM]
    assert position[OTHER_DEPENDANTS_MEDICAL] < position[MEDICAL_CLAIM]
    assert position[MEDICAL_CLAIM] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    # ON428 line 17 (line 58185) after the dependants it reads and line 58160, before the total.
    assert (
        position[ontario.ELIGIBLE_DEPENDANT_AMOUNT]
        < position[ontario.CAREGIVER_AMOUNT]
        < position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
    )
    assert position[DISABILITY_TRANSFERRED_AMOUNT] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    assert position[INFIRM_CHILDREN_AMOUNT] < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    # T1 lines 30100, 30300 and 30425, each after the lines it reads (net income for the age
    # reduction, the basic personal amount for the spouse amount, the spouse amount for the Canada
    # caregiver amount) and before the total of credit amounts.
    assert (
        position[NET_INCOME]
        < position[AGE_INCOME_OVER_THRESHOLD]
        < position[AGE_REDUCTION]
        < position[AGE_AMOUNT_BEFORE_COUNT]
        < position[AGE_AMOUNT]
        < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    )
    assert position[AGE_INCOME_THRESHOLD] < position[AGE_INCOME_OVER_THRESHOLD]
    assert position[AGE_MAXIMUM] < position[AGE_AMOUNT_BEFORE_COUNT]
    assert (
        position[BASIC_PERSONAL_AMOUNT]
        < position[SPOUSE_AMOUNT_BASIS]
        < position[SPOUSE_AMOUNT_BEFORE_COUNT]
        < position[SPOUSE_AMOUNT]
        < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    )
    assert position[SPOUSE_INFIRMITY_SUPPLEMENT] < position[SPOUSE_AMOUNT_BASIS]
    assert (
        position[SPOUSE_CAREGIVER_BASE]
        < position[SPOUSE_CAREGIVER_BEFORE_MAXIMUM]
        < position[SPOUSE_CAREGIVER_LIMIT]
        < position[SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT]
        < position[SPOUSE_CAREGIVER_AMOUNT]
        < position[NON_REFUNDABLE_CREDIT_AMOUNTS]
    )
    assert position[SPOUSE_AMOUNT] < position[SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT]
    assert (
        position[ELIGIBLE_DEPENDANT_BASE]
        < position[ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM]
        < position[ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT]
        < position[ontario.ELIGIBLE_DEPENDANT_AMOUNT]
        < position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
    )
    assert (
        position[NET_INCOME]
        < position[ontario.AGE_INCOME_OVER_THRESHOLD]
        < position[ontario.AGE_REDUCTION]
        < position[ontario.AGE_AMOUNT_BEFORE_COUNT]
        < position[ontario.AGE_AMOUNT]
        < position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
    )
    assert position[ontario.AGE_INCOME_THRESHOLD] < position[ontario.AGE_INCOME_OVER_THRESHOLD]
    assert position[ontario.AGE_MAXIMUM] < position[ontario.AGE_AMOUNT_BEFORE_COUNT]
    assert (
        position[ontario.SPOUSE_BASE]
        < position[ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM]
        < position[ontario.SPOUSE_AMOUNT_BEFORE_COUNT]
        < position[ontario.SPOUSE_AMOUNT]
        < position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
    )
    assert position[NON_REFUNDABLE_CREDIT_AMOUNTS] < position[CREDIT_AMOUNTS_AT_CREDIT_RATE]
    assert position[CREDIT_AMOUNTS_AT_CREDIT_RATE] < position[NON_REFUNDABLE_TAX_CREDITS]
    assert position[NON_REFUNDABLE_TAX_CREDITS] < position[CREDITS_AGAINST_BASIC_FEDERAL_TAX]
    assert position[CREDITS_AGAINST_BASIC_FEDERAL_TAX] < position[FEDERAL_TAX_AFTER_CREDITS]
    # Schedule 9, in line order, from its two charts and the net and taxable income it reads.
    assert position[DEPRECIABLE_GIFT_PROCEEDS_OR_COST] < position[DEPRECIABLE_GIFTS]
    assert position[DEPRECIABLE_GIFTS] < position[CAPITAL_GIFTS_TOTAL]
    assert position[CAPITAL_PROPERTY_GIFTS] < position[CAPITAL_GIFTS_TOTAL]
    assert position[CAPITAL_GIFTS_TOTAL] < position[CAPITAL_GIFTS_LIMIT_ADDITION]
    assert position[NET_INCOME] < position[DONATION_LIMIT_ON_NET_INCOME]
    assert position[DONATION_LIMIT_ON_NET_INCOME] < position[DONATION_LIMIT_WITH_CAPITAL_GIFTS]
    assert position[CAPITAL_GIFTS_LIMIT_ADDITION] < position[DONATION_LIMIT_WITH_CAPITAL_GIFTS]
    assert position[NET_INCOME] < position[CHARITABLE_DONATIONS_LIMIT]
    assert position[DONATION_LIMIT_WITH_CAPITAL_GIFTS] < position[CHARITABLE_DONATIONS_LIMIT]
    assert position[CHARITABLE_DONATIONS_LIMIT] < position[CHARITABLE_DONATIONS_CLAIMED]
    assert position[TOTAL_CHARITABLE_DONATIONS] < position[CHARITABLE_DONATIONS_CLAIMED]
    assert position[CHARITABLE_DONATIONS_CLAIMED] < position[DONATIONS_AND_GIFTS_TOTAL]
    assert position[DONATIONS_AND_GIFTS_TOTAL] < position[DONATIONS_FIRST_TIER]
    assert position[DONATION_FIRST_TIER_MAXIMUM] < position[DONATIONS_FIRST_TIER]
    assert position[DONATIONS_FIRST_TIER] < position[DONATIONS_OVER_FIRST_TIER]
    assert (
        position[DONATIONS_OVER_FIRST_TIER] < position[DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS]
    )
    assert position[TAXABLE_INCOME] < position[TAXABLE_INCOME_OVER_DONATION_THRESHOLD]
    assert (
        position[DONATION_HIGH_INCOME_THRESHOLD] < position[TAXABLE_INCOME_OVER_DONATION_THRESHOLD]
    )
    assert position[DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS] < position[HIGH_INCOME_DONATIONS]
    assert position[TAXABLE_INCOME_OVER_DONATION_THRESHOLD] < position[HIGH_INCOME_DONATIONS]
    assert position[HIGH_INCOME_DONATIONS] < position[HIGH_INCOME_DONATION_CREDIT]
    assert position[HIGH_INCOME_DONATIONS] < position[REGULAR_RATE_DONATIONS]
    assert position[DONATIONS_OVER_FIRST_TIER] < position[REGULAR_RATE_DONATIONS]
    assert position[REGULAR_RATE_DONATIONS] < position[REGULAR_RATE_DONATION_CREDIT]
    assert position[DONATIONS_FIRST_TIER] < position[FIRST_TIER_DONATION_CREDIT]
    assert (
        position[HIGH_INCOME_DONATION_CREDIT]
        < position[DONATIONS_AND_GIFTS_CREDIT]
        < position[NON_REFUNDABLE_TAX_CREDITS]
    )
    assert position[REGULAR_RATE_DONATION_CREDIT] < position[DONATIONS_AND_GIFTS_CREDIT]
    assert position[FIRST_TIER_DONATION_CREDIT] < position[DONATIONS_AND_GIFTS_CREDIT]
    # The Federal Worksheet's line 34990 reads line 33800 and Schedule 9 line 22.
    assert position[CREDIT_AMOUNTS_AT_CREDIT_RATE] < position[TOP_UP_CREDITS_BASE]
    assert position[FIRST_TIER_DONATION_CREDIT] < position[TOP_UP_CREDITS_BASE]
    assert position[TOP_UP_CREDITS_BASE] < position[TOP_UP_EXCESS]
    assert position[TOP_UP_THRESHOLD] < position[TOP_UP_EXCESS]
    assert (
        position[TOP_UP_EXCESS] < position[TOP_UP_TAX_CREDIT] < position[NON_REFUNDABLE_TAX_CREDITS]
    )
    assert position[ontario.BASIC_PERSONAL_AMOUNT] < position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
    # ON428 line 46 reads line 44; lines 47 and 48 read the federal Schedule 9 lines 13 and 14;
    # line 49 adds them; line 50 adds line 46 and line 49 and line 53 takes it off the basic tax.
    assert (
        position[ontario.NON_REFUNDABLE_CREDIT_AMOUNTS]
        < position[ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE]
        < position[ontario.NON_REFUNDABLE_TAX_CREDITS]
        < position[ONTARIO_TAX_AFTER_CREDITS]
    )
    assert position[DONATIONS_FIRST_TIER] < position[ontario.DONATIONS_FIRST_TIER_CREDIT]
    assert position[DONATIONS_OVER_FIRST_TIER] < position[ontario.DONATIONS_OVER_FIRST_TIER_CREDIT]
    assert (
        position[ontario.DONATIONS_FIRST_TIER_CREDIT]
        < position[ontario.DONATIONS_AND_GIFTS_CREDIT]
        < position[ontario.NON_REFUNDABLE_TAX_CREDITS]
    )
    assert (
        position[ontario.DONATIONS_OVER_FIRST_TIER_CREDIT]
        < position[ontario.DONATIONS_AND_GIFTS_CREDIT]
    )
    assert (
        position[ONTARIO_TAX_AFTER_CREDITS]
        < position[ONTARIO_SURTAX]
        < position[ONTARIO_TAX_WITH_SURTAX]
    )
    assert (
        position[TAXABLE_DIVIDENDS]
        < position[ontario.DIVIDENDS_AMOUNT_A]
        < position[ontario.DIVIDENDS_AMOUNT_A_LESS_B]
        < position[ontario.ELIGIBLE_DIVIDENDS_CREDIT]
        < position[ontario.DIVIDEND_TAX_CREDIT]
        < position[ontario.ONTARIO_TAX_LESS_DIVIDEND_CREDIT]
    )
    assert (
        position[TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE]
        < position[ontario.DIVIDENDS_AMOUNT_B]
        < position[ontario.OTHER_DIVIDENDS_CREDIT]
        < position[ontario.DIVIDEND_TAX_CREDIT]
    )
    assert position[ontario.DIVIDENDS_AMOUNT_B] < position[ontario.DIVIDENDS_AMOUNT_A_LESS_B]
    assert (
        position[ONTARIO_TAX_AFTER_CREDITS]
        < position[ontario.ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT]
        < position[ontario.ONTARIO_TAX_LESS_DIVIDEND_CREDIT]
    )
    assert (
        position[ONTARIO_TAX_WITH_SURTAX]
        < position[ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT]
        < position[ONTARIO_TAX_REDUCTION]
    )
    assert (
        position[ontario.DIVIDEND_TAX_CREDIT]
        < position[ontario.DIVIDEND_CREDIT_FROM_LINE_57]
        < position[ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT]
    )
    assert position[TAX_REDUCTION_BASIC] < position[TAX_REDUCTION_AMOUNTS]
    assert position[TAX_REDUCTION_FOR_CHILDREN] < position[TAX_REDUCTION_AMOUNTS]
    assert position[TAX_REDUCTION_FOR_DEPENDANTS] < position[TAX_REDUCTION_AMOUNTS]
    assert position[TAX_REDUCTION_AMOUNTS] < position[ONTARIO_TAX_REDUCTION]
    assert (
        position[ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT]
        < position[ONTARIO_TAX_REDUCTION]
        < position[ONTARIO_TAX_AFTER_REDUCTION]
        < position[ONTARIO_TAX]
    )
    assert position[TAXABLE_INCOME] < position[ONTARIO_HEALTH_PREMIUM] < position[ONTARIO_TAX]
    assert position[LIFT_CREDIT_BEFORE_MAXIMUM] < position[LIFT_MAXIMUM_CREDIT]
    assert position[NET_INCOME] < position[LIFT_REDUCTION]
    assert position[LIFT_MAXIMUM_CREDIT] < position[LIFT_CREDIT]
    assert position[LIFT_REDUCTION] < position[LIFT_CREDIT]
    assert position[LIFT_CREDIT] < position[ONTARIO_TAX_AFTER_LIFT_CREDIT] < position[ONTARIO_TAX]
    assert position[ONTARIO_TAX_AFTER_REDUCTION] < position[ONTARIO_TAX_AFTER_LIFT_CREDIT]
    assert (
        position[COMMUNITY_FOOD_PROGRAM_CREDIT]
        < position[ONTARIO_TAX_AFTER_FOOD_CREDIT]
        < position[ONTARIO_TAX]
    )
    assert position[ONTARIO_TAX_AFTER_LIFT_CREDIT] < position[ONTARIO_TAX_AFTER_FOOD_CREDIT]
    assert position[FEDERAL_TAX_AFTER_CREDITS] < position[NET_FEDERAL_TAX]
    # Line 131: each expenditure at its rate, then amount 3; line 132 adds it to line 126.
    assert position[ITC_RECAPTURE_AT_15_PERCENT] < position[ITC_RECAPTURE]
    assert position[ITC_RECAPTURE_AT_20_PERCENT] < position[ITC_RECAPTURE]
    assert position[ITC_RECAPTURE] < position[FEDERAL_TAX_WITH_ITC_RECAPTURE]
    assert position[FEDERAL_TAX_AFTER_CREDITS] < position[FEDERAL_TAX_WITH_ITC_RECAPTURE]
    # Line 41400: the rate, then the maximum; line 138 adds it and line 139 takes it off line 132.
    assert (
        position[LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM]
        < position[LABOUR_SPONSORED_FUNDS_CREDIT]
        < position[CREDITS_AGAINST_FEDERAL_TAX]
        < position[FEDERAL_TAX_LESS_CREDITS]
    )
    # Line 41000: the lines of each column, the column that applies, the shortcut and the maximum
    # in that order; line 138 adds it.
    for column in (1, 2, 3):
        lines = FEDERAL_POLITICAL_COLUMN_LINES[column]
        assert position[lines[2]] < position[lines[3]] < position[lines[5]] < position[lines[7]]
        assert position[lines[6]] < position[lines[7]] < position[POLITICAL_CREDIT_CHOSEN_COLUMN]
    assert (
        position[POLITICAL_CREDIT_CHOSEN_COLUMN]
        < position[POLITICAL_CREDIT_BEFORE_MAXIMUM]
        < position[POLITICAL_CREDIT]
        < position[CREDITS_AGAINST_FEDERAL_TAX]
    )
    assert position[POLITICAL_CREDIT_SHORTCUT_THRESHOLD] < position[POLITICAL_CREDIT_BEFORE_MAXIMUM]
    assert position[POLITICAL_CREDIT_SHORTCUT_AMOUNT] < position[POLITICAL_CREDIT_BEFORE_MAXIMUM]
    assert position[FEDERAL_TAX_WITH_ITC_RECAPTURE] < position[FEDERAL_TAX_LESS_CREDITS]
    # Form T1172: line 3, line 4, line 6, line 7, line 8, line 10, the count's choice, line 41800
    # and line 42000 each read the one before.
    assert position[RESP_AIPS_CONTRIBUTIONS_COUNTED] < position[RESP_AIPS_REDUCTION]
    assert (
        position[RESP_AIPS_LIFETIME_LIMIT]
        < position[RESP_AIPS_LIMIT_REMAINING]
        < position[RESP_AIPS_REDUCTION]
        < position[RESP_AIPS_SUBJECT_TO_TAX]
        < position[RESP_AIPS_PART_A_TAX]
        < position[RESP_AIPS_ADDITIONAL_TAX]
        < position[SPECIAL_TAXES]
    )
    assert position[RESP_AIPS_PART_B_TAX] < position[RESP_AIPS_ADDITIONAL_TAX]
    assert position[FEDERAL_TAX_LESS_CREDITS] < position[NET_FEDERAL_TAX]
    assert position[SPECIAL_TAXES] < position[NET_FEDERAL_TAX]
    assert position[NET_FEDERAL_TAX] < position[TOTAL_PAYABLE]
    assert position[ONTARIO_TAX] < position[TOTAL_PAYABLE]
    assert position[TOTAL_PAYABLE] < position[REFUND_OR_BALANCE_OWING]
    assert position[TOTAL_CREDITS] < position[REFUND_OR_BALANCE_OWING]
    for family_status in (
        (
            CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
            CWB_REDUCTION_WITHOUT_DEPENDANT,
            CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
        ),
        (
            CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
            CWB_REDUCTION_WITH_DEPENDANT,
            CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
        ),
    ):
        basic, reduction, benefit = family_status
        assert position[WORKING_INCOME] < position[basic] < position[benefit]
        assert position[NET_INCOME] < position[ADJUSTED_FAMILY_NET_INCOME] < position[reduction]
        assert position[reduction] < position[benefit] < position[CANADA_WORKERS_BENEFIT]
    # Line 45200: the working income and the columns first, then lines 6 to 8 and 11 to 16 in line
    # order, the working income gate, the residence count and the age count; line 166 adds it.
    assert (
        position[MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME]
        < position[MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS]
        < position[MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME]
        < position[MEDICAL_SUPPLEMENT_WORKING_INCOME]
    )
    assert (
        position[MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS]
        < position[MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME]
    )
    assert (
        position[MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME]
        < position[MEDICAL_SUPPLEMENT_WORKING_INCOME]
    )
    assert position[NET_INCOME_BEFORE_ADJUSTMENTS] < position[MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3]
    assert position[UCCB_AND_RDSP_INCOME_REPAYMENTS] < position[MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3]
    assert (
        position[MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3]
        < position[MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5]
        < position[MEDICAL_SUPPLEMENT_LINE_6]
    )
    assert (
        position[MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2]
        < position[MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3]
        < position[MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5]
        < position[MEDICAL_SUPPLEMENT_LINE_6]
    )
    assert (
        position[MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4] < position[MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5]
    )
    assert (
        position[MEDICAL_SUPPLEMENT_LINE_6]
        < position[MEDICAL_SUPPLEMENT_LINE_8]
        < position[MEDICAL_SUPPLEMENT_LINE_15]
        < position[MEDICAL_SUPPLEMENT_LINE_16]
    )
    assert position[MEDICAL_SUPPLEMENT_INCOME_THRESHOLD] < position[MEDICAL_SUPPLEMENT_LINE_8]
    assert position[MEDICAL_CLAIM] < position[MEDICAL_SUPPLEMENT_LINE_11]
    assert (
        position[MEDICAL_SUPPLEMENT_LINE_11]
        < position[MEDICAL_SUPPLEMENT_LINE_13]
        < position[MEDICAL_SUPPLEMENT_LINE_14]
        < position[MEDICAL_SUPPLEMENT_LINE_16]
    )
    assert (
        position[MEDICAL_SUPPLEMENT_LINE_16]
        < position[MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET]
        < position[MEDICAL_SUPPLEMENT_IF_RESIDENT]
        < position[REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT]
        < position[TOTAL_CREDITS]
    )
    assert (
        position[MEDICAL_SUPPLEMENT_WORKING_INCOME]
        < position[MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET]
    )
    assert position[CANADA_WORKERS_BENEFIT] < position[TOTAL_CREDITS]
    # Line 161 (46900): the cap on line 46800 first, then the rate; the total credits add it.
    assert (
        position[EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM]
        < position[EDUCATOR_SCHOOL_SUPPLY_CREDIT]
        < position[TOTAL_CREDITS]
    )
    # Line 48400 reads the total credits and the total payable; the opportunities fund page reads
    # line 48400, and line 46600 reads its line 1.
    assert position[TOTAL_CREDITS] < position[REFUND]
    assert position[TOTAL_PAYABLE] < position[REFUND]
    assert (
        position[REFUND] < position[ontario.REFUND_BEFORE_DONATION] < position[ontario.NET_REFUND]
    )
    assert position[FERTILITY_CREDIT_BEFORE_MAXIMUM] < position[FERTILITY_CREDIT]
    # ON479 lines 3 to 13: line 5 after the percentage of line 3, line 8 after the net incomes,
    # line 10 after lines 8 and 9, line 12 after line 10, line 13 after lines 5 and 12, and the
    # claim after line 13; line 18 after the claim.
    assert position[ontario.MEDICAL_CLAIM] < position[SENIORS_CARE_BEFORE_MAXIMUM]
    assert position[SENIORS_CARE_BEFORE_MAXIMUM] < position[SENIORS_CARE_AMOUNT]
    assert position[NET_INCOME] < position[SENIORS_CARE_FAMILY_NET_INCOME]
    assert position[SENIORS_CARE_FAMILY_NET_INCOME] < position[SENIORS_CARE_INCOME_OVER_BASE]
    assert position[SENIORS_CARE_BASE_AMOUNT] < position[SENIORS_CARE_INCOME_OVER_BASE]
    assert position[SENIORS_CARE_INCOME_OVER_BASE] < position[SENIORS_CARE_REDUCTION]
    assert position[SENIORS_CARE_AMOUNT] < position[SENIORS_CARE_BEFORE_CLAIM]
    assert position[SENIORS_CARE_REDUCTION] < position[SENIORS_CARE_BEFORE_CLAIM]
    assert position[SENIORS_CARE_BEFORE_CLAIM] < position[SENIORS_CARE_CREDIT]
    assert position[SENIORS_CARE_CREDIT] < position[ONTARIO_CREDITS_SUBTOTAL]
    assert position[SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM] < position[SENIORS_TRANSIT_CREDIT]
    assert position[FLOW_THROUGH_SHARE_EXPENSES] < position[FLOW_THROUGH_SHARE_CREDIT]
    assert position[FLOW_THROUGH_SHARE_CREDIT] < position[ONTARIO_CREDITS_SUBTOTAL]
    # Worksheet ON479 "Line 20": each line runs after the lines it reads, and ON479 line 21 after
    # line 20.
    assert (
        position[COOP_EDUCATION_PAYROLL_THRESHOLD] < position[COOP_EDUCATION_PAYROLL_OVER_THRESHOLD]
    )
    assert (
        position[COOP_EDUCATION_PAYROLL_OVER_THRESHOLD] < position[COOP_EDUCATION_PHASE_OUT_SHARE]
    )
    assert position[COOP_EDUCATION_PAYROLL_RANGE] < position[COOP_EDUCATION_PHASE_OUT_SHARE]
    assert position[COOP_EDUCATION_PHASE_OUT_SHARE] < position[COOP_EDUCATION_REMAINING_SHARE]
    assert position[COOP_EDUCATION_FULL_SHARE] < position[COOP_EDUCATION_REMAINING_SHARE]
    assert position[COOP_EDUCATION_REMAINING_SHARE] < position[COOP_EDUCATION_CREDIT]
    assert position[COOP_EDUCATION_CREDIT] < position[ONTARIO_CREDITS]
    assert position[ONTARIO_CREDITS_SUBTOTAL] < position[ONTARIO_CREDITS]
    assert position[FERTILITY_CREDIT] < position[ONTARIO_CREDITS_SUBTOTAL]
    assert position[SENIORS_TRANSIT_CREDIT] < position[ONTARIO_CREDITS_SUBTOTAL]
    for column in (1, 2, 3):
        lines = POLITICAL_COLUMN_LINES[column]
        assert position[lines[2]] < position[lines[3]] < position[lines[5]] < position[lines[7]]
        assert position[lines[6]] < position[lines[7]]
        assert position[lines[7]] < position[ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM]
    assert (
        position[POLITICAL_COLUMN_LINES[2][2]] < position[ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM]
    )
    assert (
        position[POLITICAL_COLUMN_LINES[3][2]] < position[ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM]
    )
    assert (
        position[ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM]
        < position[ontario.POLITICAL_CREDIT]
        < position[ONTARIO_CREDITS_SUBTOTAL]
    )
    assert (
        position[ONTARIO_CREDITS_SUBTOTAL]
        < position[ONTARIO_CREDITS]
        < position[PROVINCIAL_CREDITS]
        < position[TOTAL_CREDITS]
    )


def test_a_credit_larger_than_the_tax_leaves_zero_not_a_refund() -> None:
    # Employment income of 10000, with the CPP contributions computed by Schedule 8's tiers:
    # base 4.95% x (10000 - 3500) = 321.75, first additional 1% x 6500 = 65.00, no second
    # additional, so enhanced 65.00; the EI premiums computed from employment income, 1.64% x
    # 10000 = 164.00; no unused or new RRSP contributions, so the most that may be deducted is
    # the lesser of 0 and the deduction limit of 1800, and the amount deducted is 0; the Canada
    # employment amount is the lesser of 10000 and 1471.
    worksheet = compute("10000", "0", "0", "0", "1800", "0", "0")

    assert worksheet.get(TOTAL_INCOME).value == D("10000")
    assert worksheet.get(CPP_BASE_CONTRIBUTIONS).value == D("321.75")
    assert worksheet.get(CPP_FIRST_ADDITIONAL_CONTRIBUTIONS).value == D("65.00")
    assert worksheet.get(CPP_SECOND_ADDITIONAL_CONTRIBUTIONS).value == D("0")
    assert worksheet.get(CPP_ENHANCED_CONTRIBUTIONS).value == D("65.00")
    assert worksheet.get(EI_PREMIUMS).value == D("164.00")
    assert worksheet.get(RRSP_CONTRIBUTIONS_AVAILABLE).value == D("0")
    assert worksheet.get(RRSP_DEDUCTION_MAXIMUM).value == D("0")
    assert worksheet.get(RRSP_DEDUCTION).value == D("0")
    assert worksheet.get(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD).value == D("0")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("65.00")
    assert worksheet.get(NET_INCOME).value == D("9935.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("9935.00")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("1440.58")
    assert worksheet.get(CANADA_EMPLOYMENT_AMOUNT).value == D("1471")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("18085.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("13232.75")
    # 14.5% of 18085.75 = 2622.43375 and 5.05% of 13232.75 = 668.253875, each rounded half-up to
    # the cent: each larger than its basic tax (14.5% of 9935.00 = 1440.575, rounded half-up to
    # the cent: 1440.58).
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("2622.43")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("668.25")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("0")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("0")
    # A zero Ontario tax is below the first surtax threshold: no surtax.
    assert worksheet.get(ONTARIO_SURTAX).value == D("0")
    assert worksheet.get(ONTARIO_TAX_WITH_SURTAX).value == D("0")
    # ON428 line 80: twice the basic reduction of 294.00, less a tax of zero, is 588.00, all of
    # it unused; line 81 leaves zero, not a refund.
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("294.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("588.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("0")
    # Schedule ON428-A: line 5 is 5.05% x 10000 = 505.00, below the $875 maximum, and net
    # income of 9935.00 is below the 32,500.00 threshold, so no reduction: the credit (ON428 line
    # 85) is 505.00, more than the Ontario tax after the reduction of zero, so line 86 is zero.
    assert worksheet.get(LIFT_CREDIT_BEFORE_MAXIMUM).value == D("505.00")
    assert worksheet.get(LIFT_MAXIMUM_CREDIT).value == D("505.00")
    assert worksheet.get(LIFT_REDUCTION).value == D("0")
    assert worksheet.get(LIFT_CREDIT).value == D("505.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("0")
    # A taxable income of 9935.00 is "$20,000 or less" on the health premium chart: no premium.
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("0")
    assert worksheet.get(ONTARIO_TAX).value == D("0")
    # Schedule 6: the working income is the employment income of 10000, and line 20 is (10000 -
    # 3000) x 27% = 1890.00, more than the $1,633 of line 21, so line 22 is 1633; the adjusted
    # family net income of 9935.00 is below the $26,855 of line 24, so no reduction: the benefit
    # (line 28) is 1633. With an eligible dependant line 22 would be 1890.00, below the $2,813,
    # and line 24's $30,639 is above the income too, so its line 28 is 1890.00; with 0 eligible
    # dependants the amounts without one are the ones claimed (T1 line 45300): 1633.
    assert worksheet.get(WORKING_INCOME).value == D("10000")
    assert worksheet.get(ADJUSTED_FAMILY_NET_INCOME).value == D("9935.00")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT).value == D("1633")
    assert worksheet.get(CWB_REDUCTION_WITHOUT_DEPENDANT).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT).value == D("1633")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITH_DEPENDANT).value == D("1890.00")
    assert worksheet.get(CWB_REDUCTION_WITH_DEPENDANT).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT).value == D("1890.00")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("1633")
    # With no tax deducted, nothing is payable and the benefit is the only credit: line 167 is
    # 0 - 1633 = -1633, a refund.
    assert worksheet.get(NET_FEDERAL_TAX).value == D("0")
    assert worksheet.get(TOTAL_PAYABLE).value == D("0")
    assert worksheet.get(TOTAL_CREDITS).value == D("1633")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-1633")


def test_the_tax_reduction_lowers_a_tax_below_twice_the_reduction_amounts() -> None:
    # Employment income of 24000, with no capital gain, no RRSP contributions and no union dues:
    # base CPP contributions 4.95% x (24000 - 3500) = 1014.75, first additional 1% x 20500 =
    # 205.00, EI premiums 1.64% x 24000 = 393.60; net and taxable income 23795.00; Ontario basic
    # tax 5.05% x 23795.00 = 1201.6475, rounded half-up to the cent: 1201.65, less the Ontario
    # credits 5.05% x (12747 + 1014.75 + 393.60 = 14155.35) = 714.845175, rounded half-up to the
    # cent: 714.85, is 486.80, below the first surtax threshold, so the Ontario tax with surtax
    # (ON428 line 73) is 486.80. With no dependent children and no dependants, line 78 is 2 x
    # 294.00 = 588.00, and line 80 is 588.00 - 486.80 = 101.20; line 81 is 486.80 - 101.20 =
    # 385.60.
    worksheet = compute("24000", "0", "0", "0", "4320", "0", "0")

    assert worksheet.get(ONTARIO_TAX_WITH_SURTAX).value == D("486.80")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("294.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("101.20")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("385.60")


def test_dependent_children_and_dependants_raise_the_tax_reduction() -> None:
    # Return A's amounts with five dependent children (ON428 line 75, line 60969) and three
    # dependants (line 76, line 60970): line 75 is 5 x 544 = 2720, line 76 is 3 x 544 = 1632,
    # line 77 is 294.00 + 2720 + 1632 = 4646.00 and line 78 is 9292.00; line 80 is 9292.00 -
    # 8195.77 = 1096.23, and line 81 is 8195.77 - 1096.23 = 7099.54.
    worksheet = compute(
        "110000", "20000", "0", "1926", "19800", "1926", "2000", dependent_children=5, dependants=3
    )

    assert worksheet.get(DEPENDENT_CHILDREN).value == 5
    assert worksheet.get(DEPENDANTS).value == 3
    assert worksheet.get(TAX_REDUCTION_FOR_CHILDREN).value == D("2720")
    assert worksheet.get(TAX_REDUCTION_FOR_DEPENDANTS).value == D("1632")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("4646.00")
    assert worksheet.get(ONTARIO_TAX_WITH_SURTAX).value == D("8195.77")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("1096.23")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("7099.54")


def test_the_health_premium_in_a_sloped_row_adds_the_rate_to_the_plateau() -> None:
    # A capital gain of 74000 alone, with no employment income, no RRSP contributions and no
    # union dues: taxable income is half the gain, 37000, and the Ontario credits are 5.05% x
    # 12747 = 643.7235, rounded half-up to the cent: 643.72. ON428 line 89's chart, "more than
    # $36,000 but not more than $38,500": (37000 - 36000) x 6% + 300 = 360.00; the Ontario basic
    # tax 5.05% x 37000 = 1868.50 less the credits is 1224.78, above 588.00, so no reduction,
    # and line 90 is 1224.78 + 360.00 = 1584.78.
    worksheet = compute("0", "74000", "0", "0", "0", "0", "0")

    assert worksheet.get(TAXABLE_INCOME).value == D("37000")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("1224.78")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("360.00")
    assert worksheet.get(ONTARIO_TAX).value == D("1584.78")


def test_the_health_premium_at_the_top_of_a_sloped_row_is_the_plateau() -> None:
    # A capital gain of 50000 alone: taxable income 25000, "more than $20,000 but not more than
    # $25,000": (25000 - 20000) x 6% = 300.00, the plateau itself; the Ontario basic tax 5.05%
    # x 25000 = 1262.50 less the credits of 643.72 is 618.78, above 588.00, so no reduction,
    # and line 90 is 618.78 + 300.00 = 918.78.
    worksheet = compute("0", "50000", "0", "0", "0", "0", "0")

    assert worksheet.get(TAXABLE_INCOME).value == D("25000")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("618.78")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("300.00")
    assert worksheet.get(ONTARIO_TAX).value == D("918.78")


def test_no_health_premium_at_the_first_threshold() -> None:
    # A capital gain of 40000 alone: taxable income 20000, "$20,000 or less", so no premium;
    # the Ontario basic tax 5.05% x 20000 = 1010.00 less the credits of 643.72 is 366.28, below
    # 588.00, so the reduction is 221.72 and line 81 is 144.56, which is line 90.
    worksheet = compute("0", "40000", "0", "0", "0", "0", "0")

    assert worksheet.get(TAXABLE_INCOME).value == D("20000")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("144.56")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("0")
    assert worksheet.get(ONTARIO_TAX).value == D("144.56")


def test_the_lift_credit_between_the_thresholds_is_reduced_and_comes_off_the_tax() -> None:
    # Employment income of 40000, with no capital gain, no RRSP contributions and no union dues:
    # base CPP contributions 4.95% x (40000 - 3500) = 1806.75, first additional 1% x 36500 =
    # 365.00, EI premiums 1.64% x 40000 = 656.00; net and taxable income 39635.00. Ontario basic
    # tax 5.05% x 39635.00 = 2001.5675, rounded half-up to the cent: 2001.57, less the Ontario
    # credits 5.05% x (12747 + 1806.75 + 656.00 = 15209.75) = 768.092375, rounded half-up to the
    # cent: 768.09, is 1233.48, below the first surtax threshold and above 588.00, so line 81 is
    # 1233.48.
    # Schedule ON428-A: line 5 is 5.05% x 40000 = 2020.00, at most 875 (line 14); line 17 is
    # 39635.00 - 32500 = 7135.00 and line 19 7135.00 x 5% = 356.75; line 20 is 875 - 356.75 =
    # 518.25 (ON428 line 85). Line 86 is 1233.48 - 518.25 = 715.23; the health premium on
    # 39635.00, "more than $38,500 but not more than $48,000", is 450, so line 90 is 715.23 + 450
    # = 1165.23.
    worksheet = compute("40000", "0", "0", "0", "7200", "0", "0")

    assert worksheet.get(NET_INCOME).value == D("39635.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("1233.48")
    assert worksheet.get(LIFT_CREDIT_BEFORE_MAXIMUM).value == D("2020.00")
    assert worksheet.get(LIFT_MAXIMUM_CREDIT).value == D("875")
    assert worksheet.get(LIFT_REDUCTION).value == D("356.75")
    assert worksheet.get(LIFT_CREDIT).value == D("518.25")
    assert worksheet.get(ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("715.23")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("450")
    assert worksheet.get(ONTARIO_TAX).value == D("1165.23")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "lift_credit: lift_maximum_credit 875 less lift_reduction 356.75, not below 0 = 518.25"
    ) in rendered
    assert (
        "ontario_tax_after_lift_credit: ontario_tax_after_reduction 1233.48 "
        "less lift_credit 518.25, not below 0 = 715.23"
    ) in rendered


def test_return_is_community_food_program_credit_comes_off_the_tax_after_the_lift_credit() -> None:
    # Return I: employment income of 48000, with no capital gain, no RRSP contributions and no
    # union dues: base CPP contributions 4.95% x (48000 - 3500) = 2202.75, first additional 1% x
    # 44500 = 445.00, EI premiums 1.64% x 48000 = 787.20; net and taxable income 48000 - 445.00
    # = 47555.00. Ontario basic tax 5.05% x 47555.00 = 2401.5275, rounded half-up to the cent:
    # 2401.53, less the Ontario credits 5.05% x (12747 + 2202.75 + 787.20 = 15736.95) =
    # 794.715975, rounded half-up to the cent: 794.72, is 1606.81, below the first surtax
    # threshold and above 588.00, so line 81 is 1606.81.
    # Schedule ON428-A: line 5 is 5.05% x 48000 = 2424.00, at most 875 (line 14); line 17 is
    # 47555.00 - 32500 = 15055.00 and line 19 15055.00 x 5% = 752.75; line 20 is 875 - 752.75 =
    # 122.25 (ON428 line 85). Line 86 is 1606.81 - 122.25 = 1484.56. Qualifying donations of 1000
    # (a caller input, within the donations claimed): line 87 is 25% x 1000 = 250.00 and line 88
    # is 1484.56 - 250.00 = 1234.56. The health premium on 47555.00, "more than $38,500 but not
    # more than $48,000", is 450, so line 90 is 1234.56 + 450 = 1684.56.
    # The federal tax after credits is 14.5% x 47555.00 = 6895.475, rounded half-up to the cent:
    # 6895.48, less 14.5% x (16129 + 2202.75 + 787.20 + 1471 = 20589.95) = 2985.54275, rounded
    # half-up to the cent: 2985.54, is 3909.94. The total payable is 3909.94 + 1684.56 =
    # 5594.50, and with the chosen tax deducted of 4800 and no Canada workers benefit (the
    # reduction 15% x (47555.00 - 26855) = 3105.00 exceeds the 1633), line 167 is 5594.50 - 4800
    # = 794.50, a balance owing.
    worksheet = compute(
        "48000",
        "0",
        "0",
        "0",
        "8640",
        "0",
        "0",
        income_tax_deducted="4800",
        community_food_program_donations="1000",
    )

    assert worksheet.get(NET_INCOME).value == D("47555.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("1606.81")
    assert worksheet.get(LIFT_CREDIT).value == D("122.25")
    assert worksheet.get(ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("1484.56")
    assert worksheet.get(COMMUNITY_FOOD_PROGRAM_DONATIONS).value == D("1000")
    assert worksheet.get(COMMUNITY_FOOD_PROGRAM_CREDIT).value == D("250.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_FOOD_CREDIT).value == D("1234.56")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("450")
    assert worksheet.get(ONTARIO_TAX).value == D("1684.56")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("3909.94")
    assert worksheet.get(TOTAL_PAYABLE).value == D("5594.50")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("794.50")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "community_food_program_credit: 25% of community_food_program_donations 1000 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "ontario_tax_after_food_credit: ontario_tax_after_lift_credit 1484.56 "
        "less community_food_program_credit 250, not below 0 = 1234.56"
    ) in rendered
    assert (
        "ontario_tax: ontario_tax_after_food_credit 1234.56 + ontario_health_premium 450 = 1684.56"
    ) in rendered


def test_donations_without_a_larger_line_86_leave_line_88_at_zero_not_negative() -> None:
    # Employment income of 40000 as in the LIFT test above: line 86 is 715.23. Qualifying
    # donations of 4000 give line 87 = 25% x 4000 = 1000.00, more than line 86, so line 88 is 0,
    # not negative, and line 90 is the health premium of 450 alone.
    worksheet = compute(
        "40000", "0", "0", "0", "7200", "0", "0", community_food_program_donations="4000"
    )

    assert worksheet.get(ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("715.23")
    assert worksheet.get(COMMUNITY_FOOD_PROGRAM_CREDIT).value == D("1000.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_FOOD_CREDIT).value == D("0")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("450")
    assert worksheet.get(ONTARIO_TAX).value == D("450")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "ontario_tax_after_food_credit: ontario_tax_after_lift_credit 715.23 "
        "less community_food_program_credit 1000, not below 0 = 0"
    ) in rendered


def test_no_donations_leave_line_88_at_line_86() -> None:
    # The default of 0 donations, as for Returns A to H: line 87 is 0 and line 88 is line 86.
    worksheet = compute("40000", "0", "0", "0", "7200", "0", "0")

    assert worksheet.get(COMMUNITY_FOOD_PROGRAM_DONATIONS).value == D("0")
    assert worksheet.get(COMMUNITY_FOOD_PROGRAM_CREDIT).value == D("0")
    assert worksheet.get(ONTARIO_TAX_AFTER_FOOD_CREDIT).value == D("715.23")
    assert worksheet.get(ONTARIO_TAX).value == D("1165.23")


def test_return_ns_donations_and_gifts_credit_and_top_up_come_off_the_federal_tax() -> None:
    # Return N is Return I with charitable donations of 1500.00 (Schedule 9 line 1): net and
    # taxable income 47555.00 as in Return I. Line 5 = 1500.00; line 6 = 75% x 47555.00 =
    # 35666.25; no gifts of capital property, so line 7 = 25% x 0 = 0.00 and line 8 = 35666.25;
    # line 9 is the lesser of the net income (amount A) and line 8: 35666.25; line 10 = 1500.00;
    # line 12 = 1500.00; line 13 = 200 (the lesser of 1500.00 and $200); line 14 = 1300.00; line 16
    # = 1300.00; line 19 = 47555.00 - 253414.00, negative, so 0; line F = 0 and line 20 = 33% x 0
    # = 0.00; line G = 1300.00 and line 21 = 29% x 1300.00 = 377.00; line 22 = 14.5% x 200 = 29.00;
    # line 23 = 406.00 (T1 line 34900). Federal Worksheet: line 33800 = 14.5% x 20589.95 =
    # 2985.54275, rounded half-up to the cent: 2985.54; line 3 = 2985.54 + 29.00 = 3014.54, less
    # 8319.38 is negative, so line 5 = 0 and line 34990 = 0.00. Line 35000 = 2985.54 + 406.00 +
    # 0.00 = 3391.54, off the federal basic tax of 6895.48: 3503.94. ON428 reads Schedule 9
    # lines 13 and 14: line 46 = 5.05% x 15736.95 = 794.715975, rounded half-up to the cent:
    # 794.72; line 47 = 5.05% x 200 = 10.10; line 48 = 11.16% x 1300.00 = 145.08; line 49 (line
    # 58969) = 10.10 + 145.08 = 155.18; line 50 (line 61500) = 794.72 + 155.18 = 949.90, off the
    # Ontario basic tax of 2401.53: 1451.63, with no surtax and no tax reduction (twice the
    # 294.00 is 588.00, less than the 1451.63, so line 80 is 0); the LIFT credit of 122.25
    # gives 1329.38 and the food credit of 250.00 gives 1079.38; with the health premium of
    # 450, line 90 is 1529.38. The total payable is 3503.94 + 1529.38 = 5033.32 and, with the
    # chosen tax deducted of 4800 and no Canada workers benefit, line 167 is 5033.32 - 4800 =
    # 233.32, a balance owing.
    worksheet = compute(
        "48000",
        "0",
        "0",
        "0",
        "8640",
        "0",
        "0",
        income_tax_deducted="4800",
        community_food_program_donations="1000",
        charitable_donations="1500",
    )

    assert worksheet.get(NET_INCOME).value == D("47555.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("47555.00")
    assert worksheet.get(CHARITABLE_DONATIONS).value == D("1500")
    assert worksheet.get(TOTAL_CHARITABLE_DONATIONS).value == D("1500")
    assert worksheet.get(DONATION_LIMIT_ON_NET_INCOME).value == D("35666.25")
    assert worksheet.get(DEPRECIABLE_GIFTS).value == D("0")
    assert worksheet.get(CAPITAL_PROPERTY_GIFTS).value == D("0")
    assert worksheet.get(CAPITAL_GIFTS_TOTAL).value == D("0")
    assert worksheet.get(CAPITAL_GIFTS_LIMIT_ADDITION).value == D("0.00")
    assert worksheet.get(DONATION_LIMIT_WITH_CAPITAL_GIFTS).value == D("35666.25")
    assert worksheet.get(CHARITABLE_DONATIONS_LIMIT).value == D("35666.25")
    assert worksheet.get(CHARITABLE_DONATIONS_CLAIMED).value == D("1500")
    assert worksheet.get(DONATIONS_AND_GIFTS_TOTAL).value == D("1500")
    assert worksheet.get(DONATIONS_FIRST_TIER).value == D("200")
    assert worksheet.get(DONATIONS_OVER_FIRST_TIER).value == D("1300")
    assert worksheet.get(DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS).value == D("1300")
    assert worksheet.get(TAXABLE_INCOME_OVER_DONATION_THRESHOLD).value == D("0")
    assert worksheet.get(HIGH_INCOME_DONATIONS).value == D("0")
    assert worksheet.get(HIGH_INCOME_DONATION_CREDIT).value == D("0.00")
    assert worksheet.get(REGULAR_RATE_DONATIONS).value == D("1300")
    assert worksheet.get(REGULAR_RATE_DONATION_CREDIT).value == D("377.00")
    assert worksheet.get(FIRST_TIER_DONATION_CREDIT).value == D("29.00")
    assert worksheet.get(DONATIONS_AND_GIFTS_CREDIT).value == D("406.00")
    assert worksheet.get(CREDIT_AMOUNTS_AT_CREDIT_RATE).value == D("2985.54")
    assert worksheet.get(TOP_UP_CREDITS_BASE).value == D("3014.54")
    assert worksheet.get(TOP_UP_EXCESS).value == D("0")
    assert worksheet.get(TOP_UP_TAX_CREDIT).value == D("0.00")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("3391.54")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("3503.94")
    assert worksheet.get(ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE).value == D("794.72")
    assert worksheet.get(ontario.DONATIONS_FIRST_TIER_CREDIT).value == D("10.10")
    assert worksheet.get(ontario.DONATIONS_OVER_FIRST_TIER_CREDIT).value == D("145.08")
    assert worksheet.get(ontario.DONATIONS_AND_GIFTS_CREDIT).value == D("155.18")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("949.90")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("1451.63")
    assert worksheet.get(ONTARIO_TAX_WITH_SURTAX).value == D("1451.63")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("1451.63")
    assert worksheet.get(ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("1329.38")
    assert worksheet.get(ONTARIO_TAX_AFTER_FOOD_CREDIT).value == D("1079.38")
    assert worksheet.get(ONTARIO_TAX).value == D("1529.38")
    assert worksheet.get(TOTAL_PAYABLE).value == D("5033.32")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("233.32")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert ("donation_limit_on_net_income: 75% of net_income 47555 (half-up to 0.01)") in rendered
    assert (
        "charitable_donations_limit: lesser of net_income 47555 "
        "and donation_limit_with_capital_gifts 35666.25 = 35666.25"
    ) in rendered
    assert (
        "donations_first_tier: lesser of donations_and_gifts_total 1500 "
        "and donation_first_tier_maximum 200 = 200"
    ) in rendered
    assert (
        "regular_rate_donation_credit: 29% of regular_rate_donations 1300 (half-up to 0.01)"
    ) in rendered
    assert (
        "first_tier_donation_credit: 14.5% of donations_first_tier 200 (half-up to 0.01)"
    ) in rendered
    assert (
        "donations_and_gifts_credit: high_income_donation_credit 0 "
        "+ regular_rate_donation_credit 377 + first_tier_donation_credit 29 = 406"
    ) in rendered
    assert (
        "top_up_credits_base: credit_amounts_at_credit_rate 2985.54 "
        "+ first_tier_donation_credit 29 = 3014.54"
    ) in rendered
    assert (
        "top_up_excess: top_up_credits_base 3014.54 less top_up_threshold 8319.38, not below 0 = 0"
    ) in rendered
    assert (
        "non_refundable_tax_credits: credit_amounts_at_credit_rate 2985.54 "
        "+ donations_and_gifts_credit 406 + top_up_tax_credit 0 = 3391.54"
    ) in rendered
    assert (
        "credits_against_basic_federal_tax: non_refundable_tax_credits 3391.54 "
        "+ dividend_tax_credit 0 = 3391.54"
    ) in rendered
    assert (
        "federal_tax_after_credits: federal_basic_tax 6895.48 "
        "less credits_against_basic_federal_tax 3391.54, not below 0 = 3503.94"
    ) in rendered
    assert (
        "donations_first_tier_credit: 5.05% of donations_first_tier 200 (half-up to 0.01)"
    ) in rendered
    assert (
        "donations_over_first_tier_credit: 11.16% of donations_over_first_tier 1300 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "donations_and_gifts_credit: donations_first_tier_credit 10.1 "
        "+ donations_over_first_tier_credit 145.08 = 155.18"
    ) in rendered
    assert (
        "non_refundable_tax_credits: credit_amounts_at_credit_rate 794.72 "
        "+ donations_and_gifts_credit 155.18 = 949.9"
    ) in rendered
    assert (
        "ontario_tax_after_credits: ontario_basic_tax 2401.53 "
        "less non_refundable_tax_credits 949.9, not below 0 = 1451.63"
    ) in rendered
    assert (
        "ontario_tax: ontario_tax_after_food_credit 1079.38 + ontario_health_premium 450 = 1529.38"
    ) in rendered


def test_taxable_income_over_the_threshold_is_charged_33_percent_up_to_line_16() -> None:
    # Employment income of 300000, with donations of 50200 (Schedule 9 line 1): enhanced CPP
    # contributions of 1074.00 give net and taxable income 300000 - 1074.00 = 298926.00. Line 6 =
    # 75% x 298926.00 = 224194.50, line 9 = 224194.50, line 10 = 50200, line 12 = 50200, line 13 =
    # 200, line 14 = 50000 and line 16 = 50000. Line 19 = 298926.00 - 253414.00 = 45512.00, below
    # line 16, so line F = 45512.00 and line 20 = 33% x 45512.00 = 15018.96; line G = 50000 -
    # 45512.00 = 4488.00 and line 21 = 29% x 4488.00 = 1301.52; line 22 = 29.00; line 23 =
    # 15018.96 + 1301.52 + 29.00 = 16349.48. The credit amounts are 14538 (the basic personal
    # amount at or above 253,414) + 3356.10 + 1077.48 + 1471 = 20442.58, and line 33800 = 14.5% x
    # it = 2964.1741, rounded half-up to the cent: 2964.17; the top-up base 2964.17 + 29.00 is
    # below 8319.38, so line 34990 is 0; line 35000 = 2964.17 + 16349.48 + 0.00 = 19313.65.
    worksheet = compute("300000", "0", "0", "0", "0", "0", "0", charitable_donations="50200")

    assert worksheet.get(NET_INCOME).value == D("298926.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("298926.00")
    assert worksheet.get(DONATION_LIMIT_ON_NET_INCOME).value == D("224194.50")
    assert worksheet.get(CHARITABLE_DONATIONS_LIMIT).value == D("224194.50")
    assert worksheet.get(CHARITABLE_DONATIONS_CLAIMED).value == D("50200")
    assert worksheet.get(DONATIONS_FIRST_TIER).value == D("200")
    assert worksheet.get(DONATIONS_OVER_FIRST_TIER).value == D("50000")
    assert worksheet.get(DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS).value == D("50000")
    assert worksheet.get(TAXABLE_INCOME_OVER_DONATION_THRESHOLD).value == D("45512.00")
    assert worksheet.get(HIGH_INCOME_DONATIONS).value == D("45512.00")
    assert worksheet.get(HIGH_INCOME_DONATION_CREDIT).value == D("15018.96")
    assert worksheet.get(REGULAR_RATE_DONATIONS).value == D("4488.00")
    assert worksheet.get(REGULAR_RATE_DONATION_CREDIT).value == D("1301.52")
    assert worksheet.get(FIRST_TIER_DONATION_CREDIT).value == D("29.00")
    assert worksheet.get(DONATIONS_AND_GIFTS_CREDIT).value == D("16349.48")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("20442.58")
    assert worksheet.get(CREDIT_AMOUNTS_AT_CREDIT_RATE).value == D("2964.17")
    assert worksheet.get(TOP_UP_CREDITS_BASE).value == D("2993.17")
    assert worksheet.get(TOP_UP_TAX_CREDIT).value == D("0.00")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("19313.65")
    # ON428 reads lines 13 and 14, not the 33% and 29% parts: line 47 = 5.05% x 200 = 10.10 and
    # line 48 = 11.16% x 50000 = 5580.00, so line 49 = 5590.10; line 46 = 5.05% x 17180.58 =
    # 867.61929, rounded half-up to the cent: 867.62; line 50 = 867.62 + 5590.10 = 6457.72.
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("17180.58")
    assert worksheet.get(ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE).value == D("867.62")
    assert worksheet.get(ontario.DONATIONS_FIRST_TIER_CREDIT).value == D("10.10")
    assert worksheet.get(ontario.DONATIONS_OVER_FIRST_TIER_CREDIT).value == D("5580.00")
    assert worksheet.get(ontario.DONATIONS_AND_GIFTS_CREDIT).value == D("5590.10")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("6457.72")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == (
        worksheet.get(ONTARIO_BASIC_TAX).value - D("6457.72")
    )
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "high_income_donations: lesser of donations_over_first_tier_after_2016_gifts 50000 "
        "and taxable_income_over_donation_threshold 45512 = 45512"
    ) in rendered
    assert (
        "high_income_donation_credit: 33% of high_income_donations 45512 (half-up to 0.01)"
    ) in rendered


def test_the_top_up_tax_credit_is_3_45_percent_of_the_credits_over_8319_38() -> None:
    # Employment income of 48000, 15 infirm children (line 30500: 15 x 2687 = 40305.00) and
    # donations of 1500.00: the credit amounts are 16129 + 0 + 40305.00 + 2202.75 + 787.20 + 1471
    # = 60894.95 and line 33800 = 14.5% x 60894.95 = 8829.77275, rounded half-up to the cent:
    # 8829.77. Federal Worksheet line 3 = 8829.77 + 29.00 (Schedule 9 line 22) = 8858.77; line 5 =
    # 8858.77 - 8319.38 = 539.39; line 7 = 3.45% x 539.39 = 18.608955, rounded half-up to the
    # cent: 18.61 (line 34990). Line 35000 = 8829.77 + 406.00 + 18.61 = 9254.38, more than the
    # federal basic tax of 6895.48, so the federal tax after credits is 0.
    worksheet = compute(
        "48000", "0", "0", "0", "8640", "0", "0", infirm_children=15, charitable_donations="1500"
    )

    assert worksheet.get(INFIRM_CHILDREN_AMOUNT).value == D("40305.00")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("60894.95")
    assert worksheet.get(CREDIT_AMOUNTS_AT_CREDIT_RATE).value == D("8829.77")
    assert worksheet.get(FIRST_TIER_DONATION_CREDIT).value == D("29.00")
    assert worksheet.get(TOP_UP_CREDITS_BASE).value == D("8858.77")
    assert worksheet.get(TOP_UP_THRESHOLD).value == D("8319.38")
    assert worksheet.get(TOP_UP_EXCESS).value == D("539.39")
    assert worksheet.get(TOP_UP_TAX_CREDIT).value == D("18.61")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("9254.38")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("0")
    # The infirm children are federal only: ON428 line 46 is 794.72 as for Return N, and lines
    # 47 to 49 give 10.10 + 145.08 = 155.18, so line 61500 is 949.90 whatever the federal credits.
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("15736.95")
    assert worksheet.get(ontario.DONATIONS_AND_GIFTS_CREDIT).value == D("155.18")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("949.90")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "top_up_excess: top_up_credits_base 8858.77 less top_up_threshold 8319.38, not below 0 "
        "= 539.39"
    ) in rendered
    assert "top_up_tax_credit: 3.45% of top_up_excess 539.39 (half-up to 0.01)" in rendered


def test_gifts_of_capital_property_raise_the_donation_limit_above_75_percent_of_net_income() -> (
    None
):
    # Employment income of 48000: net income 47555.00, so line 6 = 35666.25. Depreciable property
    # (chart for line 33700): recaptured depreciation 3000, net proceeds 5000, capital cost 4000:
    # line 4 = 4000, line 5 (line B) = 3000. Other capital property (chart for line 33900): taxable
    # gains 4000 less the capital gains deduction 1000: 3000 (line C). Line D = 6000 and line 7 =
    # 25% x 6000 = 1500.00; line 8 = 35666.25 + 1500.00 = 37166.25; line 9 is the lesser of the net
    # income 47555.00 and line 8: 37166.25. Donations of 40000 (line 5) are limited to it (line 10),
    # so line 12 = 37166.25, line 14 = 37166.25 - 200 = 36966.25 and, below the threshold, line 21
    # = 29% x 36966.25 = 10720.2125, rounded half-up to the cent: 10720.21; line 22 = 29.00; line
    # 23 = 10749.21.
    worksheet = compute(
        "48000",
        "0",
        "0",
        "0",
        "8640",
        "0",
        "0",
        charitable_donations="40000",
        depreciable_gift_recaptured_depreciation="3000",
        depreciable_gift_net_proceeds="5000",
        depreciable_gift_capital_cost="4000",
        capital_gift_taxable_gains="4000",
        capital_gift_gains_deduction="1000",
    )

    assert worksheet.get(DEPRECIABLE_GIFT_PROCEEDS_OR_COST).value == D("4000")
    assert worksheet.get(DEPRECIABLE_GIFTS).value == D("3000")
    assert worksheet.get(CAPITAL_PROPERTY_GIFTS).value == D("3000")
    assert worksheet.get(CAPITAL_GIFTS_TOTAL).value == D("6000")
    assert worksheet.get(DONATION_LIMIT_ON_NET_INCOME).value == D("35666.25")
    assert worksheet.get(CAPITAL_GIFTS_LIMIT_ADDITION).value == D("1500.00")
    assert worksheet.get(DONATION_LIMIT_WITH_CAPITAL_GIFTS).value == D("37166.25")
    assert worksheet.get(CHARITABLE_DONATIONS_LIMIT).value == D("37166.25")
    assert worksheet.get(CHARITABLE_DONATIONS_CLAIMED).value == D("37166.25")
    assert worksheet.get(DONATIONS_AND_GIFTS_TOTAL).value == D("37166.25")
    assert worksheet.get(DONATIONS_OVER_FIRST_TIER).value == D("36966.25")
    assert worksheet.get(REGULAR_RATE_DONATION_CREDIT).value == D("10720.21")
    assert worksheet.get(DONATIONS_AND_GIFTS_CREDIT).value == D("10749.21")
    # ON428 line 47 = 5.05% x 200 = 10.10 and line 48 = 11.16% x 36966.25 = 4125.4335, rounded
    # half-up to the cent: 4125.43; line 49 = 4135.53; line 50 = 794.72 + 4135.53 = 4930.25,
    # more than the Ontario basic tax of 2401.53, so line 53 is 0, not negative.
    assert worksheet.get(ontario.DONATIONS_FIRST_TIER_CREDIT).value == D("10.10")
    assert worksheet.get(ontario.DONATIONS_OVER_FIRST_TIER_CREDIT).value == D("4125.43")
    assert worksheet.get(ontario.DONATIONS_AND_GIFTS_CREDIT).value == D("4135.53")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("4930.25")
    assert worksheet.get(ONTARIO_BASIC_TAX).value == D("2401.53")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("0")


def test_ecological_and_cultural_gifts_join_line_12_and_those_before_2016_come_off_line_16() -> (
    None
):
    # Employment income of 300000: taxable income 298926.00, line 19 = 45512.00. Donations of
    # 50000 (line 1) and ecological gifts of 10000 (line 11), 4000 of them made before 2016 (line
    # 15): line 12 = 60000, line 13 = 200, line 14 = 59800, line 16 = 59800 - 4000 = 55800, line F
    # = the lesser of 55800 and 45512.00: 45512.00, line 20 = 33% x 45512.00 = 15018.96; line G =
    # 59800 - 45512.00 = 14288.00 and line 21 = 29% x 14288.00 = 4143.52; line 22 = 29.00; line
    # 23 = 19191.48. The 4000 made before 2016 is in line G, at 29%, not at 33%.
    worksheet = compute(
        "300000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        charitable_donations="50000",
        ecological_and_cultural_gifts="10000",
        ecological_gifts_before_2016="4000",
    )

    assert worksheet.get(DONATIONS_AND_GIFTS_TOTAL).value == D("60000")
    assert worksheet.get(DONATIONS_OVER_FIRST_TIER).value == D("59800")
    assert worksheet.get(DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS).value == D("55800")
    assert worksheet.get(HIGH_INCOME_DONATIONS).value == D("45512.00")
    assert worksheet.get(HIGH_INCOME_DONATION_CREDIT).value == D("15018.96")
    assert worksheet.get(REGULAR_RATE_DONATIONS).value == D("14288.00")
    assert worksheet.get(REGULAR_RATE_DONATION_CREDIT).value == D("4143.52")
    assert worksheet.get(DONATIONS_AND_GIFTS_CREDIT).value == D("19191.48")
    # ON428 line 48 takes Schedule 9 line 14 whole, 59800, with the 4000 made before 2016 and
    # the part federal charges at 33% in it: 11.16% x 59800 = 6673.68; line 47 = 10.10; line 49 =
    # 6683.78; line 50 = 867.62 + 6683.78 = 7551.40.
    assert worksheet.get(ontario.DONATIONS_FIRST_TIER_CREDIT).value == D("10.10")
    assert worksheet.get(ontario.DONATIONS_OVER_FIRST_TIER_CREDIT).value == D("6673.68")
    assert worksheet.get(ontario.DONATIONS_AND_GIFTS_CREDIT).value == D("6683.78")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("7551.40")


def test_no_donations_leave_the_federal_credits_at_the_credit_rate() -> None:
    # The defaults of 0, as for Returns A to I: lines 34900 and 34990 are 0.00, so line 35000 is
    # line 33800 alone.
    worksheet = compute("40000", "0", "0", "0", "7200", "0", "0")

    assert worksheet.get(DONATIONS_AND_GIFTS_CREDIT).value == D("0.00")
    assert worksheet.get(TOP_UP_TAX_CREDIT).value == D("0.00")
    assert (
        worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value
        == worksheet.get(CREDIT_AMOUNTS_AT_CREDIT_RATE).value
    )


def test_no_donations_leave_the_ontario_credits_at_the_credit_rate() -> None:
    # The defaults of 0, as for Returns A to M: lines 47 to 49 are 0.00, so line 50 is line 46
    # alone.
    worksheet = compute("40000", "0", "0", "0", "7200", "0", "0")

    assert worksheet.get(ontario.DONATIONS_FIRST_TIER_CREDIT).value == D("0.00")
    assert worksheet.get(ontario.DONATIONS_OVER_FIRST_TIER_CREDIT).value == D("0.00")
    assert worksheet.get(ontario.DONATIONS_AND_GIFTS_CREDIT).value == D("0.00")
    assert (
        worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value
        == worksheet.get(ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE).value
    )


@pytest.mark.parametrize(
    ("charitable_donations", "line_47", "line_48", "line_49"),
    [
        # Schedule 9 line 13 is the lesser of line 12 and $200, line 14 the rest.
        ("0", "0.00", "0.00", "0.00"),
        ("100", "5.05", "0.00", "5.05"),
        ("200", "10.10", "0.00", "10.10"),
        ("200.01", "10.10", "0.00", "10.10"),
        ("201", "10.10", "0.11", "10.21"),
        # 11.16% x 1300 = 145.08; x 1234.57 = 137.778012, rounded half-up to 137.78 (line 14 is
        # 1234.57 for a line 12 of 1434.57).
        ("1500", "10.10", "145.08", "155.18"),
        ("1434.57", "10.10", "137.78", "147.88"),
    ],
)
def test_the_ontario_donations_credit_follows_schedule_9_lines_13_and_14(
    charitable_donations: str, line_47: str, line_48: str, line_49: str
) -> None:
    worksheet = compute(
        "48000", "0", "0", "0", "8640", "0", "0", charitable_donations=charitable_donations
    )

    assert worksheet.get(ontario.DONATIONS_FIRST_TIER_CREDIT).value == D(line_47)
    assert worksheet.get(ontario.DONATIONS_OVER_FIRST_TIER_CREDIT).value == D(line_48)
    assert worksheet.get(ontario.DONATIONS_AND_GIFTS_CREDIT).value == D(line_49)
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("794.72") + D(line_49)


def test_the_canada_workers_benefit_below_its_maximum_is_27_percent_over_3000() -> None:
    # Employment income of 8000, with no capital gain, no RRSP contributions and no union dues:
    # base CPP contributions 4.95% x (8000 - 3500) = 222.75, first additional 1% x 4500 = 45.00,
    # EI premiums 1.64% x 8000 = 131.20; net income 8000 - 45.00 = 7955.00. Each form's credits
    # exceed its tax, so nothing is payable. Schedule 6: the working income (line 5) is 8000,
    # line 18 is 8000 - 3000 = 5000 and line 20 5000 x 27% = 1350.00, less than the $1,633 of
    # line 21, so line 22 is 1350.00; the adjusted family net income (line 15) of 7955.00 is
    # below the $26,855 of line 24, so line 27 is 0 and line 28 (T1 line 45300) is 1350.00. With
    # an eligible dependant the same 1350.00, below its $2,813 and over nothing above its
    # $30,639. With no tax deducted, the total credits are 0 + 1350.00 and line 167 is
    # 0 - 1350.00 = -1350.00, a refund.
    worksheet = compute("8000", "0", "0", "0", "1440", "0", "0")

    assert worksheet.get(NET_INCOME).value == D("7955.00")
    assert worksheet.get(TOTAL_PAYABLE).value == D("0")
    assert worksheet.get(WORKING_INCOME).value == D("8000")
    assert worksheet.get(ADJUSTED_FAMILY_NET_INCOME).value == D("7955.00")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT).value == D("1350.00")
    assert worksheet.get(CWB_REDUCTION_WITHOUT_DEPENDANT).value == D("0")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITH_DEPENDANT).value == D("1350.00")
    assert worksheet.get(CWB_REDUCTION_WITH_DEPENDANT).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("1350.00")
    assert worksheet.get(TOTAL_CREDITS).value == D("1350.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-1350.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "cwb_before_reduction_without_dependant: 27% of working_income 8000 over 3000, "
        "at most 1633 (half-up to 0.01)"
    ) in rendered
    assert (
        "canada_workers_benefit_without_dependant: cwb_before_reduction_without_dependant 1350 "
        "less cwb_reduction_without_dependant 0, not below 0 = 1350"
    ) in rendered
    assert (
        "canada_workers_benefit: canada_workers_benefit_without_dependant 1350, "
        "chosen as cwb_eligible_dependants is 0"
    ) in rendered


def test_an_eligible_dependant_takes_the_schedule_6_amounts_of_2813_and_30639() -> None:
    # Employment income of 35000 and one eligible dependant, a dependent child: base CPP
    # contributions 4.95% x (35000 - 3500) = 1559.25, first additional 1% x 31500 = 315.00, so
    # net income is 35000 - 315.00 = 34685.00. Schedule 6 lines 21 and 24, "If you had an
    # eligible spouse or an eligible dependant, enter $2,813. If not, enter $1,633." and "...
    # enter $30,639. If not, enter $26,855.": with no eligible spouse or dependant, line 22 is
    # 1633 (32000 x 27% = 8640.00 is more), line 27 (34685.00 - 26855) x 15% = 1174.50 and
    # line 28 458.50; with one, line 22 is 2813, line 27 (34685.00 - 30639) x 15% = 606.90
    # and line 28 2206.10, each rounded half-up to the cent, which changes none of them. The
    # count of 1 Schedule 6 eligible dependant (line 38100) chooses the second for line 45300, so
    # with no tax deducted the total credits are 2206.10.
    worksheet = compute(
        "35000",
        "0",
        "0",
        "0",
        "6300",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
    )

    assert worksheet.get(NET_INCOME).value == D("34685.00")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT).value == D("1633")
    assert worksheet.get(CWB_REDUCTION_WITHOUT_DEPENDANT).value == D("1174.50")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT).value == D("458.50")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITH_DEPENDANT).value == D("2813")
    assert worksheet.get(CWB_REDUCTION_WITH_DEPENDANT).value == D("606.90")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT).value == D("2206.10")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("2206.10")
    assert worksheet.get(TOTAL_CREDITS).value == D("2206.10")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "cwb_before_reduction_with_dependant: 27% of working_income 35000 over 3000, "
        "at most 2813 (half-up to 0.01)"
    ) in rendered
    assert (
        "cwb_reduction_with_dependant: 15% of adjusted_family_net_income 34685 over 30639 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "canada_workers_benefit: canada_workers_benefit_with_dependant 2206.1, "
        "chosen as cwb_eligible_dependants is 1"
    ) in rendered


def test_with_no_eligible_dependant_the_same_income_takes_the_amounts_of_1633_and_26855() -> None:
    # The amounts of the test above with no eligible dependant claimed for, and no dependent
    # child: both family statuses are computed alike, and the count of 0 chooses the one
    # without an eligible dependant, 458.50.
    worksheet = compute("35000", "0", "0", "0", "6300", "0", "0")

    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT).value == D("458.50")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT).value == D("2206.10")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("458.50")
    assert worksheet.get(TOTAL_CREDITS).value == D("458.50")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "canada_workers_benefit: canada_workers_benefit_without_dependant 458.5, "
        "chosen as cwb_eligible_dependants is 0"
    ) in rendered


def test_a_line_30400_dependant_who_is_not_schedule_6s_leaves_the_amounts_without_one() -> None:
    # The amounts of the tests above with one eligible dependant claimed for on T1 line 30400, a
    # parent, say, who is not Schedule 6's eligible dependant ("They were your or your spouse's
    # or common-law partner's child"): the Schedule 6 count of 0 (line 38100), not the line
    # 30400 count of 1, chooses the amounts with no eligible dependant, 458.50.
    worksheet = compute("35000", "0", "0", "0", "6300", "0", "0", eligible_dependants=1)

    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT).value == D("458.50")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT).value == D("2206.10")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("458.50")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "canada_workers_benefit: canada_workers_benefit_without_dependant 458.5, "
        "chosen as cwb_eligible_dependants is 0"
    ) in rendered


def test_a_schedule_6_dependant_not_claimed_on_line_30400_takes_the_amounts_with_one() -> None:
    # The same income with a child under 19 who lived with the filer but is not claimed for on
    # T1 line 30400 (claimed by the other parent, say): the Schedule 6 count of 1 (line 38100)
    # chooses the amounts with an eligible dependant, 2206.10, though the line 30400 count is 0.
    worksheet = compute("35000", "0", "0", "0", "6300", "0", "0", cwb_eligible_dependants=1)

    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT).value == D("458.50")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT).value == D("2206.10")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("2206.10")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "canada_workers_benefit: canada_workers_benefit_with_dependant 2206.1, "
        "chosen as cwb_eligible_dependants is 1"
    ) in rendered


def test_tax_deducted_above_the_total_payable_is_a_refund() -> None:
    # Return A's amounts with 30000 of income tax deducted (T1 line 43700): line 167 is the total
    # payable of 25897.15 less the total credits of 30000, -4102.85, negative, so a refund (line
    # 48400), in cents as every line before it is.
    worksheet = compute(
        "110000", "20000", "0", "1926", "19800", "1926", "2000", income_tax_deducted="30000"
    )

    assert worksheet.get(TOTAL_PAYABLE).value == D("25897.15")
    assert worksheet.get(TOTAL_CREDITS).value == D("30000")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-4102.85")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "refund_or_balance_owing: total_payable 25897.15 less total_credits 30000 = -4102.85"
    ) in rendered


def test_tax_deducted_equal_to_the_total_payable_leaves_no_balance() -> None:
    worksheet = compute(
        "110000", "20000", "0", "1926", "19800", "1926", "2000", income_tax_deducted="25897.15"
    )

    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("0")


def test_with_no_tax_payable_all_the_tax_deducted_is_refunded() -> None:
    # Employment income of 10000 leaves no federal and no Ontario tax and a Canada workers
    # benefit of 1633 (see the test of a credit larger than the tax), so the total payable is 0;
    # with 500 deducted, the total credits are 500 + 1633 = 2133 and line 167 is 0 - 2133 =
    # -2133, a refund of everything deducted and the benefit, not floored at zero.
    worksheet = compute("10000", "0", "0", "0", "1800", "0", "0", income_tax_deducted="500")

    assert worksheet.get(TOTAL_PAYABLE).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("1633")
    assert worksheet.get(TOTAL_CREDITS).value == D("2133")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-2133")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "total_credits: income_tax_deducted 500 + refundable_medical_expense_supplement 0 "
        "+ canada_workers_benefit 1633 "
        "+ part_xii_2_tax_credit 0 + employee_and_partner_gst_hst_rebate 0 "
        "+ educator_school_supply_credit 0 + journalism_labour_tax_credit 0 "
        "+ tax_paid_by_instalments 0 + provincial_credits 0 = 2133"
    ) in rendered


def test_contributions_above_the_deduction_limit_deduct_the_limit() -> None:
    # Schedule 7 line 17 "Enter whichever is less: amount from line 13 or line 16.": Return A's
    # amounts with contributions of 25000, above the deduction limit of 19800, so the most that
    # may be deducted is the limit, and deducting all of it (line 18) makes it the deduction;
    # total deductions are 19800 + 2000 + 1074.00 = 22874.00. Line 23 carries 25000 - 19800 =
    # 5200 forward.
    worksheet = compute("110000", "20000", "0", "25000", "19800", "19800", "2000")

    assert worksheet.get(RRSP_DEDUCTION_MAXIMUM).value == D("19800")
    assert worksheet.get(RRSP_DEDUCTION).value == D("19800")
    assert worksheet.get(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD).value == D("5200")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("22874.00")
    assert worksheet.get(NET_INCOME).value == D("97126.00")


def test_unused_contributions_and_no_new_ones_still_deduct() -> None:
    # Schedule 7 line 5 "Line 1 plus line 4 ... Total contributions" and line 17 "Enter
    # whichever is less: amount from line 13 or line 16.": Return A's amounts with unused
    # contributions of 5000 from earlier years (line 1) and no new contributions (line 4), so
    # the contributions available to deduct (line 10) are 5000 + 0 = 5000, below the deduction
    # limit of 19800; all 5000 is deducted (line 18); total deductions are 5000 + 2000 + 1074.00
    # = 8074.00.
    worksheet = compute("110000", "20000", "5000", "0", "19800", "5000", "2000")

    assert worksheet.get(RRSP_CONTRIBUTIONS_AVAILABLE).value == D("5000")
    assert worksheet.get(RRSP_DEDUCTION_MAXIMUM).value == D("5000")
    assert worksheet.get(RRSP_DEDUCTION).value == D("5000")
    assert worksheet.get(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD).value == D("0")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("8074.00")
    assert worksheet.get(NET_INCOME).value == D("111926.00")


def test_a_claim_below_the_maximum_deducts_the_claim_and_carries_the_rest_forward() -> None:
    # Schedule 7 line 18 "Enter your RRSP, PRPP, or SPP contributions you are deducting for 2025
    # (cannot be more than the amount on line 17).": Return A's amounts deducting 1000 of the
    # 1926 that line 17 allows, so the deduction (line 20) is 1000, and line 23 "Line 21 minus
    # line 22 Your unused contributions available to carry forward to a future year" is 1926 -
    # 1000 = 926. Total deductions are 1000 + 2000 + 1074.00 = 4074.00, and net income
    # 120000 - 4074.00 = 115926.00.
    worksheet = compute("110000", "20000", "0", "1926", "19800", "1000", "2000")

    assert worksheet.get(RRSP_DEDUCTION_MAXIMUM).value == D("1926")
    assert worksheet.get(RRSP_DEDUCTION).value == D("1000")
    assert worksheet.get(UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD).value == D("926")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("4074.00")
    assert worksheet.get(NET_INCOME).value == D("115926.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert "rrsp_deduction: rrsp_amount_deducted 1000, at most rrsp_deduction_maximum 1926" in (
        rendered
    )
    assert (
        "unused_rrsp_contributions_carried_forward: rrsp_contributions_available 1926 "
        "less rrsp_deduction 1000 = 926"
    ) in rendered


def test_a_claim_above_the_maximum_is_refused_naming_both_kinds() -> None:
    # Line 18 "cannot be more than the amount on line 17": Return A's amounts claiming 3000
    # against a line 17 of 1926 is an input error, not capped to 1926.
    with pytest.raises(InputAboveBoundError) as raised:
        compute("110000", "20000", "0", "1926", "19800", "3000", "2000")

    assert str(raised.value) == (
        "ca/rrsp_amount_deducted 3000 is above ca/rrsp_deduction_maximum 1926"
    )


def test_an_eligible_dependant_with_no_income_adds_the_basic_personal_amount_and_10823() -> None:
    # Return F: employment income of 60000, one dependent child who is an eligible dependant with
    # no net income, and the child care expenses deduction of 5000 (T1 line 21400), so net
    # income is 60000 - (5000 + 565.00) = 54435.00. Schedule 5 line 5 is its line 30000 of
    # 16129.00 less 0, claimed for 1 eligible dependant: line 30400 is 16129.00. ON428 line 16
    # is 11905.00 less 0, at most 10823: line 58160 is 10823. Line 33500 is 16129 + 16129.00 + 0
    # + 2796.75 + 984.00 + 1471 = 37509.75, and line 35000 37509.75 x 14.5% = 5438.91375,
    # rounded half-up to the cent: 5438.91, so the federal tax after credits is 14.5% x 54435.00
    # = 7893.075, rounded half-up to the cent: 7893.08, less it, 2454.17. ON428 line 58800 is
    # 12747 + 10823 + 2796.75 + 984.00 = 27350.75, and line 61500 27350.75 x 5.05% =
    # 1381.212875, rounded half-up to the cent: 1381.21, so the Ontario tax after credits is
    # 2670.74 + 9.15% x (54435.00 - 52886) = 2812.4735, rounded half-up to the cent: 2812.47,
    # less it, 1431.26. The child is a dependent child for the Ontario tax reduction: 294.00 +
    # 544 = 838.00, twice it 1676.00, less 1431.26 is a reduction of 244.74, leaving 1186.52.
    # With the health premium of 600 the Ontario tax is 1786.52, the total payable 2454.17 +
    # 1786.52 = 4240.69, and line 167 4240.69 - 8000 = -3759.31, a refund.
    worksheet = compute(
        "60000",
        "0",
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
    )

    assert worksheet.get(NET_INCOME).value == D("54435.00")
    assert worksheet.get(BASIC_PERSONAL_AMOUNT).value == D("16129.00")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("16129.00")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT).value == D("16129.00")
    assert worksheet.get(INFIRM_CHILDREN_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("37509.75")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("5438.91")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("2454.17")
    assert worksheet.get(ELIGIBLE_DEPENDANT_BASE).value == D("11905.00")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM).value == D("11905.00")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("10823")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("10823")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("27350.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("1381.21")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("1431.26")
    assert worksheet.get(TAX_REDUCTION_AMOUNTS).value == D("838.00")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("244.74")
    assert worksheet.get(ONTARIO_TAX).value == D("1786.52")
    assert worksheet.get(TOTAL_PAYABLE).value == D("4240.69")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-3759.31")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "eligible_dependant_amount: eligible_dependant_amount_before_count 16129 "
        "for each of 1 eligible_dependants = 16129"
    ) in rendered
    assert (
        "eligible_dependant_amount: eligible_dependant_amount_before_count 10823 "
        "for each of 1 eligible_dependants = 10823"
    ) in rendered
    assert (
        "non_refundable_credit_amounts: basic_personal_amount 16129 "
        "+ age_amount 0 + spouse_amount 0 "
        "+ eligible_dependant_amount 16129 + spouse_caregiver_amount 0 + caregiver_amount 0 "
        "+ infirm_children_amount 0 "
        "+ cpp_base_contributions 2796.75 + ei_premiums 984 "
        "+ canada_employment_amount 1471 + disability_transferred_amount 0 "
        "+ medical_claim 0 = 37509.75"
    ) in rendered
    assert (
        "non_refundable_credit_amounts: basic_personal_amount 12747 + age_amount 0 "
        "+ spouse_amount 0 + eligible_dependant_amount 10823 + caregiver_amount 0 "
        "+ cpp_base_contributions 2796.75 + ei_premiums 984 + medical_claim 0 = 27350.75"
    ) in rendered


def test_return_fs_canada_workers_benefit_is_zero_with_an_eligible_dependant() -> None:
    # Return F, Schedule 6: working income 60000 (line 5) and adjusted family net income
    # 54435.00 (line 15). With the eligible dependant, line 22 is the lesser of (60000 - 3000) x
    # 27% = 15390.00 and 2813: 2813; line 27 is (54435.00 - 30639) x 15% = 3569.40; line 28 is
    # 2813 - 3569.40, negative, so 0. Without an eligible dependant, line 22 1633 and line 27
    # (54435.00 - 26855) x 15% = 4137.00, is computed too and is also 0; the count of 1
    # Schedule 6 eligible dependant (line 38100) chooses the amounts with one for T1 line 45300.
    worksheet = compute(
        "60000",
        "0",
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
    )

    assert worksheet.get(WORKING_INCOME).value == D("60000")
    assert worksheet.get(ADJUSTED_FAMILY_NET_INCOME).value == D("54435.00")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITH_DEPENDANT).value == D("2813")
    assert worksheet.get(CWB_REDUCTION_WITH_DEPENDANT).value == D("3569.40")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITH_DEPENDANT).value == D("0")
    assert worksheet.get(CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT).value == D("1633")
    assert worksheet.get(CWB_REDUCTION_WITHOUT_DEPENDANT).value == D("4137.00")
    assert worksheet.get(CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("0")
    assert worksheet.get(TOTAL_CREDITS).value == D("8000")
    (chosen,) = [
        line
        for line in worksheet.trace
        if isinstance(line, ChosenByCountLine) and line.output == CANADA_WORKERS_BENEFIT
    ]
    assert chosen == ChosenByCountLine(
        output=CANADA_WORKERS_BENEFIT,
        count_kind=CWB_ELIGIBLE_DEPENDANTS,
        count=1,
        chosen_kind=CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
        chosen_value=D("0"),
    )
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "canada_workers_benefit_with_dependant: cwb_before_reduction_with_dependant 2813 "
        "less cwb_reduction_with_dependant 3569.4, not below 0 = 0"
    ) in rendered
    assert (
        "canada_workers_benefit: canada_workers_benefit_with_dependant 0, "
        "chosen as cwb_eligible_dependants is 1"
    ) in rendered


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
        "0",
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


def test_return_gs_ontario_credits_are_5180_and_lower_the_refund_by_that_much() -> None:
    # Return G is Return F with fertility expenses of 24000 and 1200 paid for seniors' transit.
    # ON479 line 1: 24000 x 25% = 6000.00, at most 5000: 5000. Line 14: 1200, at most 3000, x 15%
    # = 180.00. Line 18 is 5000 + 180.00 = 5180.00, line 19 carries it, line 21 and T1 line
    # 47900 are 5180.00; the total credits are 8000 + 0 + 5180.00 = 13180.00 and line 167 is
    # 4240.69 - 13180.00 = -8939.31, Return F's -3759.31 less 5180.00.
    without = return_f_with_credits("0", "0")
    worksheet = return_f_with_credits("24000", "1200")

    assert worksheet.get(FERTILITY_CREDIT_BEFORE_MAXIMUM).value == D("6000.00")
    assert worksheet.get(FERTILITY_CREDIT).value == D("5000")
    assert worksheet.get(SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM).value == D("1200")
    assert worksheet.get(SENIORS_TRANSIT_CREDIT).value == D("180.00")
    assert worksheet.get(ONTARIO_CREDITS_SUBTOTAL).value == D("5180.00")
    assert worksheet.get(ONTARIO_CREDITS).value == D("5180.00")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("5180.00")
    assert worksheet.get(TOTAL_PAYABLE).value == D("4240.69")
    assert worksheet.get(TOTAL_CREDITS).value == D("13180.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-8939.31")
    assert without.get(PROVINCIAL_CREDITS).value == D("0")
    assert without.get(REFUND_OR_BALANCE_OWING).value == D("-3759.31")
    assert without.get(REFUND_OR_BALANCE_OWING).value - worksheet.get(
        REFUND_OR_BALANCE_OWING
    ).value == D("5180.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "fertility_credit_before_maximum: 25% of fertility_expenses 24000 (half-up to 0.01)"
    ) in rendered
    assert (
        "fertility_credit: lesser of fertility_credit_before_maximum 6000 and 5000 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "seniors_transit_amount_paid_at_most_maximum: lesser of seniors_transit_paid 1200 and "
        "3000 (half-up to 0.01)"
    ) in rendered
    assert (
        "seniors_transit_credit: 15% of seniors_transit_amount_paid_at_most_maximum 1200 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "ontario_credits_subtotal: fertility_credit 5000 + seniors_care_credit 0 "
        "+ seniors_transit_credit 180 "
        "+ political_credit 0 + flow_through_share_credit 0 = 5180"
    ) in rendered
    assert (
        "ontario_credits: ontario_credits_subtotal 5180 + coop_education_credit 0 = 5180"
    ) in rendered
    assert "provincial_credits: ontario_credits 5180 = 5180" in rendered
    assert (
        "total_credits: income_tax_deducted 8000 + refundable_medical_expense_supplement 0 "
        "+ canada_workers_benefit 0 "
        "+ part_xii_2_tax_credit 0 + employee_and_partner_gst_hst_rebate 0 "
        "+ educator_school_supply_credit 0 + journalism_labour_tax_credit 0 "
        "+ tax_paid_by_instalments 0 + provincial_credits 5180 = 13180"
    ) in rendered
    assert (
        "refund_or_balance_owing: total_payable 4240.69 less total_credits 13180 = -8939.31"
    ) in rendered


def test_return_ms_flow_through_share_credit_is_500_and_lowers_the_refund_by_that_much() -> None:
    # Return M is Return G with two Form T1221 slips, of 6000 and 4000 (two corporations). T1221
    # line 4 is 6000 + 4000 = 10000, entered on ON479 line 17 and line 63220, x 5% = 500.00. Line
    # 18 is 5000 + 180.00 + 500.00 = 5680.00, line 19 carries it, line 21 and T1 line 47900 are
    # 5680.00; the total credits are 8000 + 0 + 5680.00 = 13680.00 and line 167 is 4240.69 -
    # 13680.00 = -9439.31, Return G's -8939.31 less 500.00.
    return_g = return_f_with_credits("24000", "1200")
    worksheet = return_f_with_credits("24000", "1200", ("6000", "4000"))

    assert worksheet.get(FLOW_THROUGH_SHARE_SLIPS) == slips("6000", "4000")
    assert worksheet.get(FLOW_THROUGH_SHARE_EXPENSES).value == D("10000")
    assert worksheet.get(FLOW_THROUGH_SHARE_CREDIT).value == D("500.00")
    assert worksheet.get(FERTILITY_CREDIT).value == D("5000")
    assert worksheet.get(SENIORS_TRANSIT_CREDIT).value == D("180.00")
    assert worksheet.get(ONTARIO_CREDITS_SUBTOTAL).value == D("5680.00")
    assert worksheet.get(ONTARIO_CREDITS).value == D("5680.00")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("5680.00")
    assert worksheet.get(TOTAL_PAYABLE).value == D("4240.69")
    assert worksheet.get(TOTAL_CREDITS).value == D("13680.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-9439.31")
    assert return_g.get(FLOW_THROUGH_SHARE_CREDIT).value == D("0")
    assert return_g.get(REFUND_OR_BALANCE_OWING).value == D("-8939.31")
    assert return_g.get(REFUND_OR_BALANCE_OWING).value - worksheet.get(
        REFUND_OR_BALANCE_OWING
    ).value == D("500.00")
    (total,) = [line for line in worksheet.trace if isinstance(line, RecordTotalLine)]
    assert total == RecordTotalLine(
        FLOW_THROUGH_SHARE_EXPENSES,
        FLOW_THROUGH_SHARE_SLIP_EXPENSES,
        (D("6000"), D("4000")),
        D("10000"),
    )
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "flow_through_share_expenses: item 1 flow_through_share_slip_expenses 6000 "
        "+ item 2 flow_through_share_slip_expenses 4000 = 10000"
    ) in rendered
    assert (
        "flow_through_share_credit: 5% of flow_through_share_expenses 10000 (half-up to 0.01)"
    ) in rendered
    assert (
        "ontario_credits_subtotal: fertility_credit 5000 + seniors_care_credit 0 "
        "+ seniors_transit_credit 180 "
        "+ political_credit 0 + flow_through_share_credit 500 = 5680"
    ) in rendered
    assert (
        "ontario_credits: ontario_credits_subtotal 5680 + coop_education_credit 0 = 5680"
    ) in rendered
    assert "provincial_credits: ontario_credits 5680 = 5680" in rendered
    assert (
        "total_credits: income_tax_deducted 8000 + refundable_medical_expense_supplement 0 "
        "+ canada_workers_benefit 0 "
        "+ part_xii_2_tax_credit 0 + employee_and_partner_gst_hst_rebate 0 "
        "+ educator_school_supply_credit 0 + journalism_labour_tax_credit 0 "
        "+ tax_paid_by_instalments 0 + provincial_credits 5680 = 13680"
    ) in rendered
    assert (
        "refund_or_balance_owing: total_payable 4240.69 less total_credits 13680 = -9439.31"
    ) in rendered


def test_no_slips_leave_the_flow_through_share_credit_at_zero() -> None:
    worksheet = return_f_with_credits("0", "0")

    assert worksheet.get(FLOW_THROUGH_SHARE_SLIPS) == slips()
    assert worksheet.get(FLOW_THROUGH_SHARE_EXPENSES).value == D("0")
    assert worksheet.get(FLOW_THROUGH_SHARE_CREDIT).value == D("0")
    assert worksheet.get(ONTARIO_CREDITS).value == D("0")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-3759.31")
    assert "flow_through_share_expenses: no items = 0" in EnglishTraceRenderer().render_all(
        worksheet.trace
    )


def test_a_single_slip_gives_its_own_5_percent_as_the_only_ontario_credit() -> None:
    # T1221 line 4 is the one slip, 6000; ON479 line 17 is 6000 x 5% = 300.00 with no lines 1
    # or 14, so lines 18 and 21 and T1 line 47900 are 300.00.
    worksheet = return_f_with_credits("0", "0", ("6000",))

    assert worksheet.get(FLOW_THROUGH_SHARE_EXPENSES).value == D("6000")
    assert worksheet.get(FLOW_THROUGH_SHARE_CREDIT).value == D("300.00")
    assert worksheet.get(ONTARIO_CREDITS_SUBTOTAL).value == D("300.00")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("300.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-4059.31")
    assert "flow_through_share_expenses: item 1 flow_through_share_slip_expenses 6000 = 6000" in (
        EnglishTraceRenderer().render_all(worksheet.trace)
    )


def test_each_slip_is_an_item_named_by_its_position_and_added_before_the_rate() -> None:
    # Four slips, one of them 0: 1000.10 + 0 + 2000.20 + 3000.30 = 6000.60, x 5% = 300.03 exactly.
    worksheet = return_f_with_credits("0", "0", ("1000.10", "0", "2000.20", "3000.30"))

    assert worksheet.get(FLOW_THROUGH_SHARE_EXPENSES).value == D("6000.60")
    assert worksheet.get(FLOW_THROUGH_SHARE_CREDIT).value == D("300.03")
    assert (
        "flow_through_share_expenses: item 1 flow_through_share_slip_expenses 1000.1 "
        "+ item 2 flow_through_share_slip_expenses 0 "
        "+ item 3 flow_through_share_slip_expenses 2000.2 "
        "+ item 4 flow_through_share_slip_expenses 3000.3 = 6000.6"
    ) in EnglishTraceRenderer().render_all(worksheet.trace)


def test_the_5_percent_is_applied_once_to_the_total_not_to_each_slip() -> None:
    # Two slips of 0.10: the total 0.20 x 5% = 0.01 exactly. Rounding each slip's 0.005 half-up
    # (0.01 each) would give 0.02.
    worksheet = return_f_with_credits("0", "0", ("0.10", "0.10"))

    assert worksheet.get(FLOW_THROUGH_SHARE_EXPENSES).value == D("0.20")
    assert worksheet.get(FLOW_THROUGH_SHARE_CREDIT).value == D("0.01")


def test_the_flow_through_share_credit_is_not_limited_by_the_tax() -> None:
    # ON479 is a refundable-credits form: line 17 is not taken off the Ontario tax. Slips of
    # 200000 give 200000 x 5% = 10000.00, far above Return F's Ontario tax of 1786.52, and it is
    # added to the credits whole.
    worksheet = return_f_with_credits("0", "0", ("200000",))

    assert worksheet.get(ONTARIO_TAX).value == D("1786.52")
    assert worksheet.get(FLOW_THROUGH_SHARE_CREDIT).value == D("10000.00")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("10000.00")
    assert worksheet.get(TOTAL_CREDITS).value == D("18000.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-13759.31")


def return_r(payroll: str = "500000", placements: tuple[str, ...] = ("8000", "15000")) -> Worksheet:
    """Return R's inputs, as in `returns/2025_return_r.yaml`: Return M with work placements."""
    return return_f_with_credits(
        "24000",
        "1200",
        ("6000", "4000"),
        coop_education_payroll=payroll,
        coop_education_placements=placements,
    )


def test_return_rs_co_operative_education_credit_is_5200_and_lowers_the_refund_by_that_much() -> (
    None
):
    # Return R is Return M with two work placements, of eligible expenditures 8000 and 15000, and
    # total salaries and wages paid in 2024 of 500000. Worksheet ON479 line 6 is 500000 -
    # 400000.00 = 100000.00, line 8 is 100000.00 / 200000.00 = 0.5 and line 11 is 1.00 - 0.5 =
    # 0.5. Placement 1: line 1 is 2000.00, line 3 400.00, line 12 200.00, line 13 2200.00.
    # Placement 2: line 1 is 3750.00, line 3 750.00, line 12 375.00, line 13 4125.00, capped at
    # 3000. ON479 line 20 is 5200.00; line 21 is 5680.00 + 5200.00 = 10880.00, T1 line 47900 the
    # same; the total credits are 8000 + 0 + 10880.00 = 18880.00 and line 167 is 4240.69 -
    # 18880.00 = -14639.31, Return M's -9439.31 less 5200.00.
    return_m = return_f_with_credits("24000", "1200", ("6000", "4000"))
    worksheet = return_r()

    assert worksheet.get(COOP_EDUCATION_PAYROLL).value == D("500000")
    assert worksheet.get(COOP_EDUCATION_PLACEMENTS) == placement_list("8000", "15000")
    assert worksheet.get(COOP_EDUCATION_PAYROLL_THRESHOLD).value == D("400000.00")
    assert worksheet.get(COOP_EDUCATION_PAYROLL_OVER_THRESHOLD).value == D("100000.00")
    assert worksheet.get(COOP_EDUCATION_PAYROLL_RANGE).value == D("200000.00")
    assert worksheet.get(COOP_EDUCATION_PHASE_OUT_SHARE).value == D("0.5")
    assert worksheet.get(COOP_EDUCATION_FULL_SHARE).value == D("1.00")
    assert worksheet.get(COOP_EDUCATION_REMAINING_SHARE).value == D("0.5")
    assert worksheet.get(COOP_EDUCATION_CREDIT).value == D("5200.00")
    assert worksheet.get(COOP_EDUCATION_PLACEMENT_COUNT).value == 2
    assert type(worksheet.get(COOP_EDUCATION_PLACEMENT_COUNT).value) is int
    assert worksheet.get(ONTARIO_CREDITS_SUBTOTAL).value == D("5680.00")
    assert worksheet.get(ONTARIO_CREDITS).value == D("10880.00")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("10880.00")
    assert worksheet.get(TOTAL_PAYABLE).value == D("4240.69")
    assert worksheet.get(TOTAL_CREDITS).value == D("18880.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-14639.31")
    assert return_m.get(COOP_EDUCATION_CREDIT).value == D("0")
    assert return_m.get(REFUND_OR_BALANCE_OWING).value == D("-9439.31")
    assert return_m.get(REFUND_OR_BALANCE_OWING).value - worksheet.get(
        REFUND_OR_BALANCE_OWING
    ).value == D("5200.00")
    first, second = [line for line in worksheet.trace if isinstance(line, PlacementCreditLine)]
    assert first == PlacementCreditLine(
        output=COOP_EDUCATION_CREDIT,
        position=1,
        field=COOP_EDUCATION_PLACEMENT_EXPENDITURES,
        expenditure=D("8000"),
        line_1=D("2000.00"),
        line_3=D("400.00"),
        line_12=D("200.00"),
        line_13=D("2200.00"),
        remaining_share=COOP_EDUCATION_REMAINING_SHARE,
        remaining_share_amount=D("0.5"),
        expenditure_rate=Rate(D("0.25")),
        supplement_rate=Rate(D("0.05")),
        maximum=Amount(D("3000")),
        rounding=CENT,
    )
    assert second == PlacementCreditLine(
        output=COOP_EDUCATION_CREDIT,
        position=2,
        field=COOP_EDUCATION_PLACEMENT_EXPENDITURES,
        expenditure=D("15000"),
        line_1=D("3750.00"),
        line_3=D("750.00"),
        line_12=D("375.00"),
        line_13=D("3000.00"),
        remaining_share=COOP_EDUCATION_REMAINING_SHARE,
        remaining_share_amount=D("0.5"),
        expenditure_rate=Rate(D("0.25")),
        supplement_rate=Rate(D("0.05")),
        maximum=Amount(D("3000")),
        rounding=CENT,
    )
    (credit_total,) = [
        line
        for line in worksheet.trace
        if isinstance(line, ItemsTotalLine) and line.output is COOP_EDUCATION_CREDIT
    ]
    assert credit_total == ItemsTotalLine(
        COOP_EDUCATION_CREDIT, ((1, D("2200.00")), (2, D("3000.00"))), D("5200.00")
    )
    (quotient,) = [line for line in worksheet.trace if isinstance(line, QuotientLine)]
    assert quotient == QuotientLine(
        output=COOP_EDUCATION_PHASE_OUT_SHARE,
        dividend=COOP_EDUCATION_PAYROLL_OVER_THRESHOLD,
        dividend_amount=D("100000.00"),
        divisor=COOP_EDUCATION_PAYROLL_RANGE,
        divisor_amount=D("200000.00"),
        result=D("0.5"),
    )
    (count,) = [line for line in worksheet.trace if isinstance(line, RecordCountLine)]
    assert count == RecordCountLine(COOP_EDUCATION_PLACEMENT_COUNT, COOP_EDUCATION_PLACEMENTS, 2)
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert "coop_education_payroll_threshold: credit amount 400000 (half-up to 0.01)" in rendered
    assert (
        "coop_education_payroll_over_threshold: coop_education_payroll 500000 "
        "less coop_education_payroll_threshold 400000, not below 0 = 100000"
    ) in rendered
    assert "coop_education_payroll_range: credit amount 200000 (half-up to 0.01)" in rendered
    assert (
        "coop_education_phase_out_share: coop_education_payroll_over_threshold 100000 "
        "divided by coop_education_payroll_range 200000 = 0.5"
    ) in rendered
    assert "coop_education_full_share: credit amount 1 (half-up to 0.01)" in rendered
    assert (
        "coop_education_remaining_share: coop_education_full_share 1 "
        "less coop_education_phase_out_share 0.5, not below 0 = 0.5"
    ) in rendered
    assert (
        "coop_education_credit: item 1 coop_education_placement_expenditures 8000: "
        "line 1 2000, line 3 400, line 12 200, line 13 2200 (half-up to 0.01)"
    ) in rendered
    assert (
        "coop_education_credit: item 2 coop_education_placement_expenditures 15000: "
        "line 1 3750, line 3 750, line 12 375, line 13 3000 (half-up to 0.01)"
    ) in rendered
    assert "coop_education_credit: item 1 2200 + item 2 3000 = 5200" in rendered
    assert ("coop_education_placement_count: 2 items in coop_education_placements = 2") in rendered
    assert (
        "ontario_credits: ontario_credits_subtotal 5680 + coop_education_credit 5200 = 10880"
    ) in rendered
    assert "provincial_credits: ontario_credits 10880 = 10880" in rendered
    assert (
        "total_credits: income_tax_deducted 8000 + refundable_medical_expense_supplement 0 "
        "+ canada_workers_benefit 0 "
        "+ part_xii_2_tax_credit 0 + employee_and_partner_gst_hst_rebate 0 "
        "+ educator_school_supply_credit 0 + journalism_labour_tax_credit 0 "
        "+ tax_paid_by_instalments 0 + provincial_credits 10880 = 18880"
    ) in rendered
    assert (
        "refund_or_balance_owing: total_payable 4240.69 less total_credits 18880 = -14639.31"
    ) in rendered


@pytest.mark.parametrize(
    ("payroll", "line_8", "line_11", "credit"),
    [
        # The worked examples, for placements of 8000 and 15000.
        ("500000", "0.5", "0.5", "5200"),
        ("700000", "1.5", "0", "5000"),
        ("300000", "0", "1", "5400"),
        # 400000 is the 30% result and 600000 the 25% result for each placement.
        ("400000", "0", "1", "5400"),
        ("600000", "1", "0", "5000"),
    ],
)
def test_the_worksheets_worked_examples_for_two_placements(
    payroll: str, line_8: str, line_11: str, credit: str
) -> None:
    worksheet = return_f_with_credits(
        "0", "0", (), coop_education_payroll=payroll, coop_education_placements=("8000", "15000")
    )

    assert worksheet.get(COOP_EDUCATION_PHASE_OUT_SHARE).value == D(line_8)
    assert worksheet.get(COOP_EDUCATION_REMAINING_SHARE).value == D(line_11)
    assert worksheet.get(COOP_EDUCATION_CREDIT).value == D(credit)
    assert worksheet.get(ONTARIO_CREDITS).value == D(credit)
    assert worksheet.get(PROVINCIAL_CREDITS).value == D(credit)
    assert worksheet.get(COOP_EDUCATION_PLACEMENT_COUNT).value == 2


@pytest.mark.parametrize(
    ("payroll", "credit"),
    [
        # At or below 400000 the percentage is 30%, at 600000 or more 25%, in between 25% plus 5%
        # times the remaining share: 8000 x 30% = 2400, 8000 x 25% = 2000, and 2000 + 400 x 0.75.
        ("0", "2400"),
        ("300000", "2400"),
        ("400000", "2400"),
        ("450000", "2300"),
        ("500000", "2200"),
        ("550000", "2100"),
        ("600000", "2000"),
        ("700000", "2000"),
    ],
)
def test_one_placement_of_8000_is_30_percent_to_25_percent_across_the_payroll_range(
    payroll: str, credit: str
) -> None:
    worksheet = return_f_with_credits(
        "0", "0", (), coop_education_payroll=payroll, coop_education_placements=("8000",)
    )

    assert worksheet.get(COOP_EDUCATION_CREDIT).value == D(credit)
    assert worksheet.get(COOP_EDUCATION_PLACEMENT_COUNT).value == 1


def test_line_8_is_an_exact_fraction_and_is_not_rounded() -> None:
    # 0.07 / 200000.00 = 0.00000035, so line 11 is 1.00 - 0.00000035 = 0.99999965.
    worksheet = return_f_with_credits(
        "0", "0", (), coop_education_payroll="400000.07", coop_education_placements=("8000",)
    )

    assert worksheet.get(COOP_EDUCATION_PAYROLL_OVER_THRESHOLD).value == D("0.07")
    assert worksheet.get(COOP_EDUCATION_PHASE_OUT_SHARE).value == D("0.00000035")
    assert worksheet.get(COOP_EDUCATION_REMAINING_SHARE).value == D("0.99999965")
    # 2000 + 400 x 0.99999965 = 2399.9998600, rounded half-up to the cent: 2400.00.
    assert worksheet.get(COOP_EDUCATION_CREDIT).value == D("2400.00")
    assert (
        "coop_education_phase_out_share: coop_education_payroll_over_threshold 0.07 "
        "divided by coop_education_payroll_range 200000 = 0.00000035"
    ) in EnglishTraceRenderer().render_all(worksheet.trace)


def test_a_payroll_over_600000_leaves_line_11_at_zero_not_negative() -> None:
    # Line 8 is 1.5, 1.00 - 1.5 is negative, so line 11 is "0".
    worksheet = return_f_with_credits(
        "0", "0", (), coop_education_payroll="700000", coop_education_placements=("8000",)
    )

    assert worksheet.get(COOP_EDUCATION_PHASE_OUT_SHARE).value == D("1.5")
    assert worksheet.get(COOP_EDUCATION_REMAINING_SHARE).value == D("0")
    assert (
        "coop_education_remaining_share: coop_education_full_share 1 "
        "less coop_education_phase_out_share 1.5, not below 0 = 0"
    ) in EnglishTraceRenderer().render_all(worksheet.trace)


def test_a_payroll_of_less_than_400000_leaves_line_6_at_zero_not_negative() -> None:
    worksheet = return_f_with_credits(
        "0", "0", (), coop_education_payroll="300000", coop_education_placements=("8000",)
    )

    assert worksheet.get(COOP_EDUCATION_PAYROLL_OVER_THRESHOLD).value == D("0")
    assert worksheet.get(COOP_EDUCATION_PHASE_OUT_SHARE).value == D("0")
    assert (
        "coop_education_payroll_over_threshold: coop_education_payroll 300000 "
        "less coop_education_payroll_threshold 400000, not below 0 = 0"
    ) in EnglishTraceRenderer().render_all(worksheet.trace)


@pytest.mark.parametrize("payroll", ["0", "300000", "500000", "700000"])
def test_no_placements_leave_the_credit_and_the_count_at_zero_whatever_the_payroll(
    payroll: str,
) -> None:
    worksheet = return_f_with_credits("0", "0", (), coop_education_payroll=payroll)

    assert worksheet.get(COOP_EDUCATION_PLACEMENTS) == placement_list()
    assert worksheet.get(COOP_EDUCATION_CREDIT).value == D("0")
    assert worksheet.get(COOP_EDUCATION_PLACEMENT_COUNT).value == 0
    assert worksheet.get(ONTARIO_CREDITS).value == D("0")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-3759.31")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert "coop_education_placement_count: no items in coop_education_placements = 0" in rendered
    assert "coop_education_credit: no items = 0" in rendered


def test_one_placement_gives_a_count_of_one_in_the_singular() -> None:
    worksheet = return_f_with_credits(
        "0", "0", (), coop_education_payroll="400000", coop_education_placements=("8000",)
    )

    assert worksheet.get(COOP_EDUCATION_PLACEMENT_COUNT).value == 1
    assert (
        "coop_education_placement_count: 1 item in coop_education_placements = 1"
    ) in EnglishTraceRenderer().render_all(worksheet.trace)


def test_the_count_of_placements_is_not_the_number_of_dollars_or_the_credit() -> None:
    worksheet = return_f_with_credits(
        "0",
        "0",
        (),
        coop_education_payroll="400000",
        coop_education_placements=("100", "200", "300", "400", "500"),
    )

    assert worksheet.get(COOP_EDUCATION_PLACEMENT_COUNT).value == 5
    assert worksheet.get(COOP_EDUCATION_CREDIT).value == D("450.00")
    assert (
        "coop_education_placement_count: 5 items in coop_education_placements = 5"
    ) in EnglishTraceRenderer().render_all(worksheet.trace)


def test_the_maximum_of_3000_applies_to_each_student_and_not_to_the_total() -> None:
    # Ten placements of 15000 at 30%: 4500 each, capped at 3000 each, 30000 in all.
    worksheet = return_f_with_credits(
        "0", "0", (), coop_education_payroll="400000", coop_education_placements=("15000",) * 10
    )

    assert worksheet.get(COOP_EDUCATION_CREDIT).value == D("30000.00")
    assert worksheet.get(COOP_EDUCATION_PLACEMENT_COUNT).value == 10


def test_the_co_operative_education_credit_is_not_limited_by_the_tax() -> None:
    # ON479 is a refundable-credits form: line 20 is not taken off the Ontario tax of 1786.52; it
    # is added to line 21 and T1 line 47900 whole.
    worksheet = return_f_with_credits(
        "0", "0", (), coop_education_payroll="400000", coop_education_placements=("15000",) * 10
    )

    assert worksheet.get(ONTARIO_TAX).value == D("1786.52")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("30000.00")
    assert worksheet.get(TOTAL_CREDITS).value == D("38000.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-33759.31")


def test_each_placements_line_13_is_rounded_before_they_are_added() -> None:
    # Two placements of 0.10 at 25% (payroll 600000): 0.025 each, 0.03 each half-up, 0.06 in all.
    # Rounding their sum 0.05 once would give 0.05.
    worksheet = return_f_with_credits(
        "0", "0", (), coop_education_payroll="600000", coop_education_placements=("0.10", "0.10")
    )

    assert worksheet.get(COOP_EDUCATION_CREDIT).value == D("0.06")
    assert worksheet.get(ONTARIO_CREDITS).value == D("0.06")


def test_lines_1_and_12_are_added_before_line_13_is_rounded() -> None:
    # 0.14 at 30% (payroll 400000): line 1 is 0.035 and line 12 is 0.007, so line 13 is 0.042,
    # rounded half-up to 0.04. Rounding the two lines first would give 0.04 + 0.01 = 0.05.
    worksheet = return_f_with_credits(
        "0", "0", (), coop_education_payroll="400000", coop_education_placements=("0.14",)
    )

    assert worksheet.get(COOP_EDUCATION_CREDIT).value == D("0.04")


def test_the_credit_follows_the_order_of_the_placements_in_the_trace() -> None:
    worksheet = return_f_with_credits(
        "0", "0", (), coop_education_payroll="500000", coop_education_placements=("15000", "8000")
    )

    lines = [line for line in worksheet.trace if isinstance(line, PlacementCreditLine)]
    assert [(line.position, line.expenditure) for line in lines] == [
        (1, D("15000")),
        (2, D("8000")),
    ]
    assert worksheet.get(COOP_EDUCATION_CREDIT).value == D("5200.00")


def test_a_negative_payroll_is_refused() -> None:
    with pytest.raises(NegativeArtifactError, match="coop_education_payroll"):
        return_f_with_credits("0", "0", (), coop_education_payroll="-1")


def test_a_negative_eligible_expenditure_is_refused_naming_the_placement() -> None:
    with pytest.raises(
        NegativeArtifactError, match="item 2: .*coop_education_placement_expenditures"
    ):
        return_f_with_credits("0", "0", (), coop_education_placements=("8000", "-1"))


def test_the_fertility_credit_below_its_maximum_is_25_percent_of_the_expenses() -> None:
    # 12000 x 25% = 3000.00, below the maximum of 5000, so line 1 is 3000.00 and the credits are
    # 3000.00 with no transit amount.
    worksheet = return_f_with_credits("12000", "0")

    assert worksheet.get(FERTILITY_CREDIT_BEFORE_MAXIMUM).value == D("3000.00")
    assert worksheet.get(FERTILITY_CREDIT).value == D("3000.00")
    assert worksheet.get(SENIORS_TRANSIT_CREDIT).value == D("0")
    assert worksheet.get(ONTARIO_CREDITS).value == D("3000.00")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("3000.00")
    assert worksheet.get(TOTAL_CREDITS).value == D("11000.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-6759.31")


def test_the_transit_amount_paid_is_capped_before_the_rate() -> None:
    # 3500 paid is capped at 3000 (ON479 line 14, "(maximum $3,000)" before the percentage), and
    # 3000 x 15% = 450.00, not 3500 x 15% = 525.00.
    worksheet = return_f_with_credits("0", "3500")

    assert worksheet.get(SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM).value == D("3000")
    assert worksheet.get(SENIORS_TRANSIT_CREDIT).value == D("450.00")
    assert worksheet.get(FERTILITY_CREDIT).value == D("0")
    assert worksheet.get(ONTARIO_CREDITS).value == D("450.00")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("450.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-4209.31")
    (capped_paid,) = [
        line
        for line in worksheet.trace
        if isinstance(line, CappedAmountLine)
        and line.output == SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM
    ]
    assert capped_paid == CappedAmountLine(
        SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
        SENIORS_TRANSIT_PAID,
        D("3500"),
        Amount(D("3000")),
        CENT,
        D("3000"),
    )


def test_the_fertility_credit_is_capped_after_the_rate() -> None:
    # 24000 x 25% = 6000.00 is above 5000, so line 1 is the maximum, whereas capping the expenses
    # at 5000 first would give 1250.00.
    worksheet = return_f_with_credits("24000", "0")

    (capped,) = [
        line
        for line in worksheet.trace
        if isinstance(line, CappedAmountLine) and line.output == FERTILITY_CREDIT
    ]
    assert capped == CappedAmountLine(
        FERTILITY_CREDIT,
        FERTILITY_CREDIT_BEFORE_MAXIMUM,
        D("6000.00"),
        Amount(D("5000")),
        CENT,
        D("5000"),
    )


def test_the_dependants_net_income_comes_off_both_amounts() -> None:
    # Return F's amounts with a dependant's net income of 1500 (Schedule 5 line 4, ON428 line
    # 15): line 5 is 16129.00 - 1500 = 14629.00, and ON428 line 16 is 11905.00 - 1500 =
    # 10405.00, below the $10,823 maximum, so kept. Line 33500 is 16129 + 14629.00 + 0 +
    # 2796.75 + 984.00 + 1471 = 36009.75; ON428 line 58800 is 12747 + 10405.00 + 2796.75 +
    # 984.00 = 26932.75.
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        dependant_net_income="1500",
        child_care_expenses_paid="6000",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
    )

    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT).value == D("14629.00")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("10405.00")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("10405.00")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("36009.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("26932.75")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "eligible_dependant_amount_before_count: basic_personal_amount 16129 "
        "less dependant_net_income 1500, not below 0 = 14629"
    ) in rendered
    assert (
        "eligible_dependant_amount_before_count: lesser of "
        "eligible_dependant_amount_before_maximum 10405 and 10823 (half-up to 0.01)"
    ) in rendered


def test_a_dependant_with_more_income_than_the_amounts_adds_nothing() -> None:
    # Schedule 5 line 5 and ON428 line 16 "(if negative, enter "0")": a dependant's net income
    # of 20000 is above both 16129.00 and 11905.00, so each amount is 0 and the totals are those
    # without a dependant: 16129 + 0 + 0 + 2796.75 + 984.00 + 1471 = 21380.75 and 12747 + 0 +
    # 2796.75 + 984.00 = 16527.75.
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        dependant_net_income="20000",
        child_care_expenses_paid="6000",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
    )

    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("0")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT).value == D("0")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM).value == D("0")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("21380.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("16527.75")


def test_no_eligible_dependant_claims_nothing_whatever_the_dependants_income() -> None:
    # Return F's amounts with no eligible dependant claimed for but a dependant's net income of
    # 1500 entered: Schedule 5 line 5 is still 14629.00, but line 30400 claims it for 0
    # eligible dependants, so it is 0, and so is line 58160.
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        dependant_net_income="1500",
        child_care_expenses_paid="6000",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
    )

    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("14629.00")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT).value == D("0")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT).value == D("10405.00")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("21380.75")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("16527.75")


def test_infirm_children_add_2687_each_to_the_federal_amounts_only() -> None:
    # Return A's amounts with two infirm children (T1 line 30499): line 30500 is 2 x 2687 =
    # 5374, so line 33500 is 22033.58 + 5374 = 27407.58, line 35000 27407.58 x 14.5% =
    # 3974.0991, rounded half-up to the cent: 3974.10, and the federal tax after credits
    # 20146.25 - 3974.10 = 16172.15. ON428 has
    # no such line here (its caregiver amount, line 58185, is not triggered), so its total is
    # unchanged at 17180.58.
    worksheet = compute("110000", "20000", "0", "1926", "19800", "1926", "2000", infirm_children=2)

    assert worksheet.get(INFIRM_CHILDREN).value == 2
    assert worksheet.get(INFIRM_CHILDREN_AMOUNT).value == D("5374")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("27407.58")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("3974.10")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("16172.15")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("17180.58")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "infirm_children_amount: 2687 for each of 2 infirm_children = 5374 (half-up to 0.01)"
        in (rendered)
    )


def test_the_child_care_expenses_deduction_is_5000_for_one_child_and_lowers_net_income() -> None:
    # Return F, Form T778: the child, born in 2015, is counted on Part B line 3, so line 1 is 0
    # x 8000 = 0, line 2 0 x 11000 = 0 and line 3 1 x 5000 = 5000; line 4 is 0 + 0 + 5000 =
    # 5000; line 5 is the 6000 paid; line 6 is two-thirds of the earned income, the employment
    # income of 60000: 40000. Line 7 is the least of 5000, 6000 and 40000: 5000, line 21400. T1
    # line 23300 is 0 + 0 + 5000 + 565.00 = 5565.00, and net income 60000 - 5565.00 =
    # 54435.00, which the LIFT reduction (5% of 54435.00 over 32500 = 1096.75) and Schedule 6
    # (15% of 54435.00 over 30639 = 3569.40, with the eligible dependant) read; the federal and
    # Ontario taxes on it are 7893.075 and 2812.4735, rounded half-up to the cent.
    worksheet = compute(
        "60000",
        "0",
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
    )

    assert worksheet.get(CHILDREN_SEVEN_TO_SIXTEEN).value == 1
    assert worksheet.get(CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN).value == D("0")
    assert worksheet.get(CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY).value == D("0")
    assert worksheet.get(CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN).value == D("5000")
    assert worksheet.get(CHILD_CARE_BASIC_LIMIT).value == D("5000")
    assert worksheet.get(CHILD_CARE_EARNED_INCOME).value == D("60000")
    assert worksheet.get(CHILD_CARE_EARNED_INCOME_LIMIT).value == D("40000")
    assert worksheet.get(CHILD_CARE_EXPENSES).value == D("5000")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("5565.00")
    assert worksheet.get(NET_INCOME).value == D("54435.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("54435.00")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("7893.08")
    assert worksheet.get(ONTARIO_BASIC_TAX).value == D("2812.47")
    assert worksheet.get(LIFT_REDUCTION).value == D("1096.75")
    assert worksheet.get(LIFT_CREDIT).value == D("0")
    assert worksheet.get(ADJUSTED_FAMILY_NET_INCOME).value == D("54435.00")
    assert worksheet.get(CWB_REDUCTION_WITH_DEPENDANT).value == D("3569.40")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("0")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "child_care_limit_for_children_seven_to_sixteen: 5000 for each of 1 "
        "children_seven_to_sixteen = 5000 (half-up to 0.01)"
    ) in rendered
    assert (
        "child_care_earned_income_limit: 2/3 of child_care_earned_income 60000 (half-up to 0.01)"
    ) in rendered
    assert (
        "child_care_expenses: lesser of child_care_basic_limit 5000 and child_care_expenses_paid "
        "6000 and child_care_earned_income_limit 40000 = 5000"
    ) in rendered
    assert (
        "deductions_from_total_income: rpp_deduction 0 + rrsp_deduction 0 + fhsa_deduction 0 "
        "+ elected_split_pension_deduction 0 + union_dues 0 + uccb_repayment 0 "
        "+ child_care_expenses 5000 + allowable_business_investment_loss 0 "
        "+ support_payments_deduction 0 "
        "+ carrying_charges_interest_expenses_and_other_expenses 0 "
        "+ cpp_enhanced_contributions 565 + exploration_and_development_expenses 0 "
        "+ other_deductions 0 = 5565"
    ) in rendered


def test_expenses_paid_below_the_basic_limit_are_deducted_whole() -> None:
    # Return F with 3500 paid (T778 line 5): the least of 5000, 3500 and 40000 is 3500, so T1
    # line 23300 is 3500 + 565.00 = 4065.00 and net income 60000 - 4065.00 = 55935.00.
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        child_care_expenses_paid="3500",
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
    )

    assert worksheet.get(CHILD_CARE_EXPENSES).value == D("3500")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("4065.00")
    assert worksheet.get(NET_INCOME).value == D("55935.00")


def test_the_limits_for_each_kind_of_eligible_child_add_up() -> None:
    # Return F with one child on each of T778 Part B lines 1, 2 and 3 and 30000 paid: line 4 is
    # 8000 + 11000 + 5000 = 24000, below the 30000 paid and the 40000 of line 6, so the
    # deduction is 24000, T1 line 23300 is 24000 + 565.00 = 24565.00 and net income 60000 -
    # 24565.00 = 35435.00.
    worksheet = compute(
        "60000",
        "0",
        "0",
        "0",
        "10800",
        "0",
        "0",
        dependent_children=1,
        eligible_dependants=1,
        cwb_eligible_dependants=1,
        child_care_expenses_paid="30000",
        children_under_seven=1,
        children_with_disability=1,
        children_seven_to_sixteen=1,
        income_tax_deducted="8000",
    )

    assert worksheet.get(CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN).value == D("8000")
    assert worksheet.get(CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY).value == D("11000")
    assert worksheet.get(CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN).value == D("5000")
    assert worksheet.get(CHILD_CARE_BASIC_LIMIT).value == D("24000")
    assert worksheet.get(CHILD_CARE_EXPENSES).value == D("24000")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("24565.00")
    assert worksheet.get(NET_INCOME).value == D("35435.00")


def test_two_thirds_of_a_low_earned_income_caps_the_deduction() -> None:
    # Employment income of 9000, two children born in 2019 or later and 12000 paid: line 4 is 2
    # x 8000 = 16000, line 5 12000, line 6 two-thirds of 9000 = 6000, the least, so the
    # deduction is 6000. The first additional CPP contribution is 1% x (9000 - 3500) = 55.00, so
    # T1 line 23300 is 6000 + 55.00 = 6055.00 and net income 9000 - 6055.00 = 2945.00.
    worksheet = compute(
        "9000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        child_care_expenses_paid="12000",
        children_under_seven=2,
    )

    assert worksheet.get(CHILD_CARE_BASIC_LIMIT).value == D("16000")
    assert worksheet.get(CHILD_CARE_EARNED_INCOME_LIMIT).value == D("6000")
    assert worksheet.get(CHILD_CARE_EXPENSES).value == D("6000")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("6055.00")
    assert worksheet.get(NET_INCOME).value == D("2945.00")


def test_the_interest_and_other_investment_income_is_the_worksheets_line_9_less_line_10() -> None:
    # The Federal Worksheet's "Line 12100 - Interest and other investment income": line 2 (the T5
    # boxes) 1200 and line 7 (bank interest with no slip) 300 add to line 9 "Add lines 1 to 8."
    # of 1500; line 10 (reported in previous years) 100 comes off it: line 11, and so line
    # 12100, is 1400.
    worksheet = compute(
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        t5_investment_income="1200",
        investment_income_without_a_slip="300",
        investment_income_reported_in_previous_years="100",
    )

    assert worksheet.get(INVESTMENT_INCOME_BEFORE_PRIOR_YEARS).value == D("1500")
    assert worksheet.get(INTEREST_AND_OTHER_INVESTMENT_INCOME).value == D("1400")
    assert worksheet.get(TOTAL_INCOME).value == D("1400")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "investment_income_before_prior_years: t3_investment_income 0 + t5_investment_income 1200 "
        "+ t5013_investment_income 0 + investment_income_credited_not_received 0 "
        "+ tax_refund_interest 0 + foreign_investment_income 0 "
        "+ investment_income_without_a_slip 300 + investment_royalties 0 = 1500"
    ) in rendered
    assert (
        "interest_and_other_investment_income: investment_income_before_prior_years 1500 "
        "less investment_income_reported_in_previous_years 100 = 1400"
    ) in rendered


def test_prior_year_investment_income_above_line_9_is_refused_as_a_negative_line_11() -> None:
    # The Federal Worksheet's line 10 (reported in previous years) of 200 is more than line 9 of
    # 150, so line 11 "Line 9 minus line 10", and so line 12100, would be negative; the kind
    # cannot be below zero, so the capability's output breaks its contract.
    with pytest.raises(
        CapabilityContractError,
        match="ca/interest_and_other_investment_income -50, which cannot be negative",
    ):
        compute(
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            t5_investment_income="150",
            investment_income_reported_in_previous_years="200",
        )


def test_each_of_the_worksheets_lines_1_to_8_adds_to_line_9() -> None:
    # Distinct amounts, one per line, so a line left out or added twice changes the sum: 1 + 2 +
    # 4 + 8 + 16 + 32 + 64 + 128 = 255, and line 10 of 5 leaves 250.
    worksheet = compute(
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        t3_investment_income="1",
        t5_investment_income="2",
        t5013_investment_income="4",
        investment_income_credited_not_received="8",
        tax_refund_interest="16",
        foreign_investment_income="32",
        investment_income_without_a_slip="64",
        investment_royalties="128",
        investment_income_reported_in_previous_years="5",
    )

    assert worksheet.get(INVESTMENT_INCOME_BEFORE_PRIOR_YEARS).value == D("255")
    assert worksheet.get(INTEREST_AND_OTHER_INVESTMENT_INCOME).value == D("250")


def test_line_14700_adds_lines_29_to_31() -> None:
    # T1 line 32 and line 14700 "Add lines 29 to 31 (see line 25000 in Step 4).": the workers'
    # compensation benefits (14400), the social assistance payments (14500) and the net federal
    # supplements (14600), 2000 + 300 + 40 = 2340, which line 15000 adds.
    worksheet = compute(
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        workers_compensation_benefits="2000",
        social_assistance_payments="300",
        net_federal_supplements="40",
    )

    assert worksheet.get(INCOME_SUPPORT_BENEFITS).value == D("2340")
    assert worksheet.get(TOTAL_INCOME).value == D("2340")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "income_support_benefits: workers_compensation_benefits 2000 "
        "+ social_assistance_payments 300 + net_federal_supplements 40 = 2340"
    ) in rendered


def test_total_income_adds_every_income_line_once() -> None:
    # T1 line 33 and line 15000 "Line 28 plus line 32 Total income": one distinct power of two
    # for each of the nineteen amounts that enter it, so a line left out or added twice changes
    # the total: 2^0 + ... + 2^18 = 524287. Employment income 1 (line 10100), other employment
    # income 2 (10400), OAS 4 (11300), CPP benefits 8 (11400), other pensions 16 (11500),
    # elected split-pension amount 32 (11600), UCCB 64 (11700), EI 128 (11900), interest and
    # other investment income 256 (12100, from the T5 slips), net partnership income 512
    # (12200), RDSP income 1024 (12500), taxable capital gains 2048 (12700, 50% of a capital
    # gain of 4096), taxable support payments 4096 (12800), RRSP income 8192 (12900), FHSA
    # income 16384 (12905), taxable FHSA income - other 32768 (12906), other income 65536
    # (13000), scholarships 131072 (13010) and the lines 14400 to 14600 of 262144 (14700).
    worksheet = compute(
        "1",
        "4096",
        "0",
        "0",
        "0",
        "0",
        "0",
        other_employment_income="2",
        old_age_security="4",
        cpp_or_qpp_benefits="8",
        other_pensions_and_superannuation="16",
        elected_split_pension_amount="32",
        universal_child_care_benefit="64",
        ei_and_other_benefits="128",
        t5_investment_income="256",
        net_partnership_income="512",
        rdsp_income="1024",
        taxable_support_payments="4096",
        rrsp_income="8192",
        fhsa_income="16384",
        other_fhsa_income="32768",
        other_income="65536",
        taxable_scholarships="131072",
        workers_compensation_benefits="262144",
    )

    assert worksheet.get(TAXABLE_CAPITAL_GAINS).value == D("2048.00")
    assert worksheet.get(INTEREST_AND_OTHER_INVESTMENT_INCOME).value == D("256")
    assert worksheet.get(INCOME_SUPPORT_BENEFITS).value == D("262144")
    assert worksheet.get(TOTAL_INCOME).value == D("524287")


def test_return_hs_pension_and_benefit_income_is_all_of_its_total_income() -> None:
    # Return H, a retiree: OAS 8000 (line 11300), CPP benefits 9000 (11400), other pensions
    # 20000 (11500), RRSP income 5000 (12900) and workers' compensation 2000 (14400, so line
    # 14700); interest from the Federal Worksheet: T5 slips 1200 (line 2) plus bank interest with
    # no slip 300 (line 7) is 1500 (line 9), less 100 reported in previous years (line 10): 1400
    # (line 12100). Total income 8000 + 9000 + 20000 + 1400 + 5000 + 2000 = 45400, with no
    # employment income, so no CPP contributions, EI premiums, Canada employment amount, LIFT
    # credit or Canada workers benefit. With no amount entered on line 14600, line 25000 is line
    # 14700, 2000, so taxable income is 45400 - 2000 = 43400.
    worksheet = compute(
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        old_age_security="8000",
        cpp_or_qpp_benefits="9000",
        other_pensions_and_superannuation="20000",
        t5_investment_income="1200",
        investment_income_without_a_slip="300",
        investment_income_reported_in_previous_years="100",
        rrsp_income="5000",
        workers_compensation_benefits="2000",
        income_tax_deducted="3000",
    )

    assert worksheet.get(INVESTMENT_INCOME_BEFORE_PRIOR_YEARS).value == D("1500")
    assert worksheet.get(INTEREST_AND_OTHER_INVESTMENT_INCOME).value == D("1400")
    assert worksheet.get(INCOME_SUPPORT_BENEFITS).value == D("2000")
    assert worksheet.get(TOTAL_INCOME).value == D("45400")
    assert worksheet.get(CPP_ENHANCED_CONTRIBUTIONS).value == D("0")
    assert worksheet.get(NET_INCOME).value == D("45400")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("2000")
    assert worksheet.get(DEDUCTIONS_FROM_NET_INCOME).value == D("2000")
    assert worksheet.get(TAXABLE_INCOME).value == D("43400.00")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("6293.00")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("2338.71")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("3954.29")
    assert worksheet.get(ONTARIO_BASIC_TAX).value == D("2191.70")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("643.72")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("1547.98")
    assert worksheet.get(LIFT_REDUCTION).value == D("645.00")
    assert worksheet.get(LIFT_CREDIT).value == D("0")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("450")
    assert worksheet.get(ONTARIO_TAX).value == D("1997.98")
    assert worksheet.get(TOTAL_PAYABLE).value == D("5952.27")
    assert worksheet.get(WORKING_INCOME).value == D("0")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("0")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("2952.27")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "total_income: employment_income 0 + other_employment_income 0 + old_age_security 8000 "
        "+ cpp_or_qpp_benefits 9000 + other_pensions_and_superannuation 20000 "
        "+ elected_split_pension_amount 0 + universal_child_care_benefit 0 "
        "+ ei_and_other_benefits 0 + taxable_dividends 0 "
        "+ interest_and_other_investment_income 1400 "
        "+ net_partnership_income 0 + rdsp_income 0 + taxable_capital_gains 0 "
        "+ taxable_support_payments 0 + rrsp_income 5000 + fhsa_income 0 + other_fhsa_income 0 "
        "+ other_income 0 + taxable_scholarships 0 + income_support_benefits 2000 = 45400"
    ) in rendered


def return_j(
    born_in_1960_or_earlier: int = 1,
    spouse_net_income: str = "12000",
    spouses_claimed: int = 1,
    spouse_caregiver_eligible: int = 1,
) -> Worksheet:
    """Return J's inputs, as in `returns/2025_return_j.yaml`, with the age and spouse ones given."""
    return compute(
        "50000",
        "930",
        "0",
        "0",
        "9000",
        "0",
        "0",
        born_in_1960_or_earlier=born_in_1960_or_earlier,
        spouse_net_income=spouse_net_income,
        spouses_claimed=spouses_claimed,
        spouse_caregiver_eligible=spouse_caregiver_eligible,
        income_tax_deducted="6000",
    )


def test_return_js_age_spouse_and_caregiver_amounts_come_off_net_income_and_the_spouses() -> None:
    # Return J: employment income of 50000 and a capital gain of 930, so total income is 50000 +
    # 465.00 = 50465.00 and, less the enhanced CPP contributions of 465.00, net income is
    # 50000.00. The filer was born in 1960 or earlier and the spouse, whose net income is 12000,
    # is infirm and eligible for the Canada caregiver amount (line 51090). Age amount (5000-D1):
    # 9028.00 - 15% x (50000.00 - 45522) = 9028.00 - 671.70 = 8356.30. Spouse amount (5000-S5):
    # (16129.00 + 2687) - 12000 = 6816.00. Canada caregiver amount for the spouse: 28798.00 -
    # 12000 = 16798.00, at most 8601, less the spouse amount 6816.00: 1785.00. Line 33500 is
    # 16129.00 + 8356.30 + 6816.00 + 0 + 1785.00 + 0 + 2301.75 + 820.00 + 1471 = 37679.05, and
    # line 35000 37679.05 x 14.5% = 5463.46225, rounded half-up to the cent: 5463.46.
    worksheet = return_j()

    assert worksheet.get(NET_INCOME).value == D("50000.00")
    assert worksheet.get(BORN_IN_1960_OR_EARLIER).value == 1
    assert worksheet.get(SPOUSE_NET_INCOME).value == D("12000")
    assert worksheet.get(SPOUSES_CLAIMED).value == 1
    assert worksheet.get(SPOUSE_CAREGIVER_ELIGIBLE).value == 1
    assert worksheet.get(AGE_MAXIMUM).value == D("9028.00")
    assert worksheet.get(AGE_INCOME_THRESHOLD).value == D("45522.00")
    assert worksheet.get(AGE_INCOME_OVER_THRESHOLD).value == D("4478.00")
    assert worksheet.get(AGE_REDUCTION).value == D("671.70")
    assert worksheet.get(AGE_AMOUNT_BEFORE_COUNT).value == D("8356.30")
    assert worksheet.get(AGE_AMOUNT).value == D("8356.30")
    assert worksheet.get(SPOUSE_INFIRMITY_SUPPLEMENT).value == D("2687")
    assert worksheet.get(SPOUSE_AMOUNT_BASIS).value == D("18816.00")
    assert worksheet.get(SPOUSE_AMOUNT_BEFORE_COUNT).value == D("6816.00")
    assert worksheet.get(SPOUSE_AMOUNT).value == D("6816.00")
    assert worksheet.get(SPOUSE_CAREGIVER_BASE).value == D("28798.00")
    assert worksheet.get(SPOUSE_CAREGIVER_BEFORE_MAXIMUM).value == D("16798.00")
    assert worksheet.get(SPOUSE_CAREGIVER_LIMIT).value == D("8601")
    assert worksheet.get(SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT).value == D("1785.00")
    assert worksheet.get(SPOUSE_CAREGIVER_AMOUNT).value == D("1785.00")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("37679.05")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("5463.46")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("1786.54")
    # Worksheet ON428 (form 5006-D), "Line 58080 - Age amount": line 1 6223.00, line 3 46330.00;
    # line 4 is 50000.00 - 46330.00 = 3670.00, line 6 15% of it, 550.50, and line 7 is 6223.00 -
    # 550.50 = 5672.50, claimed once. ON428 line 11 is 11905.00 and line 12 the spouse's net income,
    # 12000, so line 13 is 11905.00 - 12000, negative, so 0, at most 10823: 0.
    assert worksheet.get(ontario.AGE_MAXIMUM).value == D("6223.00")
    assert worksheet.get(ontario.AGE_INCOME_THRESHOLD).value == D("46330.00")
    assert worksheet.get(ontario.AGE_INCOME_OVER_THRESHOLD).value == D("3670.00")
    assert worksheet.get(ontario.AGE_REDUCTION).value == D("550.50")
    assert worksheet.get(ontario.AGE_AMOUNT_BEFORE_COUNT).value == D("5672.50")
    assert worksheet.get(ontario.AGE_AMOUNT).value == D("5672.50")
    assert worksheet.get(ontario.SPOUSE_BASE).value == D("11905.00")
    assert worksheet.get(ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM).value == D("0")
    assert worksheet.get(ontario.SPOUSE_AMOUNT_BEFORE_COUNT).value == D("0")
    assert worksheet.get(ontario.SPOUSE_AMOUNT).value == D("0")
    # ON428 line 58800 is 12747 + 5672.50 + 0 + 0 + 2301.75 + 820.00 = 21541.25, and line 61500
    # 21541.25 x 5.05% = 1087.833125, rounded half-up to the cent: 1087.83.
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("21541.25")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("1087.83")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("1437.17")
    assert worksheet.get(ONTARIO_TAX).value == D("2037.17")
    assert worksheet.get(TOTAL_PAYABLE).value == D("3823.71")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-2176.29")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    for line in (
        "age_income_over_threshold: net_income 50000 less age_income_threshold 45522, not below 0 "
        "= 4478",
        "age_reduction: 15% of age_income_over_threshold 4478 (half-up to 0.01)",
        "age_amount_before_count: age_maximum 9028 less age_reduction 671.7, not below 0 = 8356.3",
        "age_amount: age_amount_before_count 8356.3 for each of 1 born_in_1960_or_earlier = 8356.3",
        "spouse_infirmity_supplement: 2687 for each of 1 spouse_caregiver_eligible = 2687 "
        "(half-up to 0.01)",
        "spouse_amount_basis: basic_personal_amount 16129 + spouse_infirmity_supplement 2687 "
        "= 18816",
        "spouse_amount_before_count: spouse_amount_basis 18816 "
        "less spouse_net_income 12000, not below 0 = 6816",
        "spouse_amount: spouse_amount_before_count 6816 for each of 1 spouses_claimed = 6816",
        "spouse_caregiver_before_maximum: spouse_caregiver_base 28798 "
        "less spouse_net_income 12000, not below 0 = 16798",
        "spouse_caregiver_limit: lesser of spouse_caregiver_before_maximum 16798 and 8601 "
        "(half-up to 0.01)",
        "spouse_caregiver_amount_before_count: spouse_caregiver_limit 8601 "
        "less spouse_amount 6816, not below 0 = 1785",
        "spouse_caregiver_amount: spouse_caregiver_amount_before_count 1785 "
        "for each of 1 spouse_caregiver_eligible = 1785",
        "non_refundable_credit_amounts: basic_personal_amount 16129 + age_amount 8356.3 "
        "+ spouse_amount 6816 + eligible_dependant_amount 0 + spouse_caregiver_amount 1785 "
        "+ caregiver_amount 0 + infirm_children_amount 0 + cpp_base_contributions 2301.75 "
        "+ ei_premiums 820 + canada_employment_amount 1471 + disability_transferred_amount 0 "
        "+ medical_claim 0 "
        "= 37679.05",
        "age_income_over_threshold: net_income 50000 less age_income_threshold 46330, not below 0 "
        "= 3670",
        "age_reduction: 15% of age_income_over_threshold 3670 (half-up to 0.01)",
        "age_amount_before_count: age_maximum 6223 less age_reduction 550.5, not below 0 = 5672.5",
        "age_amount: age_amount_before_count 5672.5 for each of 1 born_in_1960_or_earlier = 5672.5",
        "spouse_amount_before_maximum: spouse_base 11905 "
        "less spouse_net_income 12000, not below 0 = 0",
        "spouse_amount_before_count: lesser of spouse_amount_before_maximum 0 and 10823 "
        "(half-up to 0.01)",
        "spouse_amount: spouse_amount_before_count 0 for each of 1 spouses_claimed = 0",
        "non_refundable_credit_amounts: basic_personal_amount 12747 + age_amount 5672.5 "
        "+ spouse_amount 0 + eligible_dependant_amount 0 + caregiver_amount 0 "
        "+ cpp_base_contributions 2301.75 + ei_premiums 820 + medical_claim 0 = 21541.25",
    ):
        assert line in rendered


def test_a_filer_born_in_1961_or_later_claims_no_age_amount_whatever_the_net_income() -> None:
    # Federal Worksheet line 7 is 8356.30 at net income 50000.00, but the count of filers born in
    # 1960 or earlier is 0: line 30100 is 0, and the other amounts are as in Return J.
    worksheet = return_j(born_in_1960_or_earlier=0)

    assert worksheet.get(AGE_AMOUNT_BEFORE_COUNT).value == D("8356.30")
    assert worksheet.get(AGE_AMOUNT).value == D("0")
    assert worksheet.get(SPOUSE_AMOUNT).value == D("6816.00")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("29322.75")


def test_the_ontario_age_amount_is_zero_at_net_income_87817() -> None:
    # Net income is employment income less the enhanced CPP contributions at their maximum
    # (1074.00): 88891 - 1074.00 = 87817.00. Worksheet ON428 line 6 is 15% x (87817.00 - 46330) =
    # 6223.05, more than the 6223.00 maximum, so line 7 "(if negative, enter "0")" is 0.
    worksheet = compute("88891", "0", "0", "0", "0", "0", "0", born_in_1960_or_earlier=1)

    assert worksheet.get(NET_INCOME).value == D("87817.00")
    assert worksheet.get(ontario.AGE_REDUCTION).value == D("6223.05")
    assert worksheet.get(ontario.AGE_AMOUNT_BEFORE_COUNT).value == D("0")
    assert worksheet.get(ontario.AGE_AMOUNT).value == D("0")


def test_the_ontario_age_amount_is_still_a_dollar_short_of_zero_at_net_income_87816() -> None:
    # 88890 - 1074.00 = 87816.00: line 6 is 15% x (87816.00 - 46330) = 6222.90, so line 7 is
    # 6223.00 - 6222.90 = 0.10.
    worksheet = compute("88890", "0", "0", "0", "0", "0", "0", born_in_1960_or_earlier=1)

    assert worksheet.get(NET_INCOME).value == D("87816.00")
    assert worksheet.get(ontario.AGE_REDUCTION).value == D("6222.90")
    assert worksheet.get(ontario.AGE_AMOUNT).value == D("0.10")


def test_the_ontario_age_amount_is_the_whole_maximum_at_a_net_income_below_the_threshold() -> None:
    # Net income is 44585.00 (as for the federal case), below 46330: line 4 is negative, so 0,
    # line 6 is 0 and line 7 is 6223.00: "$46,330 or less, enter $6,223".
    worksheet = compute("45000", "0", "0", "0", "0", "0", "0", born_in_1960_or_earlier=1)

    assert worksheet.get(ontario.AGE_INCOME_OVER_THRESHOLD).value == D("0")
    assert worksheet.get(ontario.AGE_AMOUNT).value == D("6223.00")


def test_a_filer_born_in_1961_or_later_claims_no_ontario_age_amount() -> None:
    worksheet = return_j(born_in_1960_or_earlier=0)

    assert worksheet.get(ontario.AGE_AMOUNT_BEFORE_COUNT).value == D("5672.50")
    assert worksheet.get(ontario.AGE_AMOUNT).value == D("0")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("15868.75")


def test_a_spouse_with_net_income_4000_who_is_not_infirm_gives_ontario_line_58120_of_7905() -> None:
    # ON428 line 11 11905.00 less line 12, 4000: line 13 is 7905.00, below the 10823 maximum,
    # claimed once. (The federal line 30300 is 16129.00 - 4000 = 12129.00.)
    worksheet = return_j(spouse_net_income="4000", spouse_caregiver_eligible=0)

    assert worksheet.get(ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM).value == D("7905.00")
    assert worksheet.get(ontario.SPOUSE_AMOUNT_BEFORE_COUNT).value == D("7905.00")
    assert worksheet.get(ontario.SPOUSE_AMOUNT).value == D("7905.00")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("29446.25")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "spouse_amount_before_maximum: spouse_base 11905 "
        "less spouse_net_income 4000, not below 0 = 7905"
    ) in rendered


def test_a_spouse_amount_not_claimed_gives_no_ontario_spouse_amount() -> None:
    worksheet = return_j(spouse_net_income="4000", spouse_caregiver_eligible=0, spouses_claimed=0)

    assert worksheet.get(ontario.SPOUSE_AMOUNT_BEFORE_COUNT).value == D("7905.00")
    assert worksheet.get(ontario.SPOUSE_AMOUNT).value == D("0")


@pytest.mark.parametrize(
    ("spouse_net_income", "amount"),
    [
        # Line 13 is 11905.00 less the spouse's net income, at most 10823: the cap holds up to a
        # net income of 1082.
        ("0", "10823.00"),
        ("1082", "10823.00"),
        ("1083", "10822.00"),
        ("4000", "7905.00"),
        ("11904.99", "0.01"),
        ("11905", "0"),
        ("20000", "0"),
    ],
)
def test_the_ontario_spouse_amount_is_11905_less_their_net_income_at_most_10823(
    spouse_net_income: str, amount: str
) -> None:
    worksheet = return_j(spouse_net_income=spouse_net_income)

    assert worksheet.get(ontario.SPOUSE_AMOUNT).value == D(amount)


def test_the_age_amount_is_reduced_to_ten_cents_at_net_income_105708() -> None:
    # Net income is employment income less the enhanced CPP contributions at their maximum
    # (1074.00): 106782 - 1074.00 = 105708.00. The Federal Worksheet's line 6 is 15% x (105708.00
    # - 45522) = 9027.90, so line 7 is 9028.00 - 9027.90 = 0.10.
    worksheet = compute("106782", "0", "0", "0", "0", "0", "0", born_in_1960_or_earlier=1)

    assert worksheet.get(NET_INCOME).value == D("105708.00")
    assert worksheet.get(AGE_REDUCTION).value == D("9027.90")
    assert worksheet.get(AGE_AMOUNT).value == D("0.10")


def test_the_age_amount_is_zero_at_net_income_105709() -> None:
    # 106783 - 1074.00 = 105709.00: line 6 is 15% x (105709.00 - 45522) = 9028.05, more than the
    # maximum 9028.00, so line 7 "(if negative, enter "0")" is 0.
    worksheet = compute("106783", "0", "0", "0", "0", "0", "0", born_in_1960_or_earlier=1)

    assert worksheet.get(NET_INCOME).value == D("105709.00")
    assert worksheet.get(AGE_REDUCTION).value == D("9028.05")
    assert worksheet.get(AGE_AMOUNT_BEFORE_COUNT).value == D("0")
    assert worksheet.get(AGE_AMOUNT).value == D("0")


def test_the_caregiver_amount_is_zero_at_a_spouse_net_income_of_8623() -> None:
    # Schedule 5: with the spouse eligible for the Canada caregiver amount, line 3 of the
    # line 30300 part is 16129.00 + 2687 = 18816.00 and line 5 is 18816.00 - 8623 = 10193.00,
    # claimed. The caregiver part's line 3 is 28798.00 - 8623 = 20175.00, at most 8601, and line 5
    # is 8601 - 10193.00, negative, so 0.
    worksheet = return_j(spouse_net_income="8623")

    assert worksheet.get(SPOUSE_AMOUNT).value == D("10193.00")
    assert worksheet.get(SPOUSE_CAREGIVER_BEFORE_MAXIMUM).value == D("20175.00")
    assert worksheet.get(SPOUSE_CAREGIVER_LIMIT).value == D("8601")
    assert worksheet.get(SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT).value == D("0")
    assert worksheet.get(SPOUSE_CAREGIVER_AMOUNT).value == D("0")


def test_the_caregiver_amount_starts_at_a_dollar_past_a_spouse_net_income_of_10215() -> None:
    # 18816.00 - 10216 = 8600.00 is the spouse amount, so the caregiver amount is 8601 - 8600.00
    # = 1.00; at 10215 the spouse amount is 8601.00 and the caregiver amount is 0.
    at = return_j(spouse_net_income="10215")
    past = return_j(spouse_net_income="10216")

    assert at.get(SPOUSE_AMOUNT).value == D("8601.00")
    assert at.get(SPOUSE_CAREGIVER_AMOUNT).value == D("0")
    assert past.get(SPOUSE_AMOUNT).value == D("8600.00")
    assert past.get(SPOUSE_CAREGIVER_AMOUNT).value == D("1.00")


def test_a_spouse_not_eligible_for_the_caregiver_amount_adds_no_supplement() -> None:
    # The count for line 51090 is 0: line 2 is 0, so line 3 is 16129.00 and line 5 is 16129.00 -
    # 4000 = 12129.00, claimed; the caregiver amount is 0 although its line 5 is 8601 - 12129.00,
    # negative, so 0 as well.
    worksheet = return_j(spouse_net_income="4000", spouse_caregiver_eligible=0)

    assert worksheet.get(SPOUSE_INFIRMITY_SUPPLEMENT).value == D("0")
    assert worksheet.get(SPOUSE_AMOUNT_BASIS).value == D("16129.00")
    assert worksheet.get(SPOUSE_AMOUNT).value == D("12129.00")
    assert worksheet.get(SPOUSE_CAREGIVER_AMOUNT).value == D("0")


def test_a_spouse_amount_not_claimed_leaves_the_whole_caregiver_limit() -> None:
    # The count of spouse amounts claimed is 0: line 30300 is 0 (line 5 of the line 30300 part is
    # 6816.00). The model takes line 4 of the line 30425 part, "Amount claimed on line 30300 or
    # line 30400 of your return, if applicable", to be the line 30300 artifact, so line 4 is 0
    # and line 5 is 8601 - 0 = 8601.
    worksheet = return_j(spouses_claimed=0)

    assert worksheet.get(SPOUSE_AMOUNT_BEFORE_COUNT).value == D("6816.00")
    assert worksheet.get(SPOUSE_AMOUNT).value == D("0")
    assert worksheet.get(SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT).value == D("8601")
    assert worksheet.get(SPOUSE_CAREGIVER_AMOUNT).value == D("8601")


def test_the_age_amount_is_the_whole_maximum_at_a_net_income_below_the_threshold() -> None:
    # Net income is 45000 - 415.00 (1% x (45000 - 3500), the enhanced CPP contributions) =
    # 44585.00. Federal Worksheet line 4 is 44585.00 - 45522.00, negative, so 0, line 6 is 0 and
    # line 7 is 9028.00 - 0.00: "$45,522 or less, enter $9,028".
    worksheet = compute("45000", "0", "0", "0", "0", "0", "0", born_in_1960_or_earlier=1)

    assert worksheet.get(NET_INCOME).value == D("44585.00")
    assert worksheet.get(AGE_INCOME_OVER_THRESHOLD).value == D("0")
    assert worksheet.get(AGE_REDUCTION).value == D("0")
    assert worksheet.get(AGE_AMOUNT).value == D("9028.00")


@pytest.mark.parametrize(
    ("spouse_net_income", "eligible", "amount"),
    [
        # Line 3 is 16129.00 (no supplement) or 18816.00 (16129.00 + 2687), less the net income.
        ("0", 0, "16129.00"),
        ("4000", 0, "12129.00"),
        ("12000", 0, "4129.00"),
        # Net income at the basic personal amount leaves nothing; a cent under it, a cent.
        ("16128.99", 0, "0.01"),
        ("16129", 0, "0"),
        ("20000", 0, "0"),
        ("0", 1, "18816.00"),
        ("12000", 1, "6816.00"),
        ("18815.50", 1, "0.50"),
        ("18816", 1, "0"),
        ("20000", 1, "0"),
    ],
)
def test_the_spouse_amount_is_the_basic_personal_amount_and_2687_less_their_net_income(
    spouse_net_income: str, eligible: int, amount: str
) -> None:
    worksheet = return_j(spouse_net_income=spouse_net_income, spouse_caregiver_eligible=eligible)

    assert worksheet.get(SPOUSE_AMOUNT).value == D(amount)


@pytest.mark.parametrize(
    ("spouse_net_income", "amount"),
    [
        # Up to a net income of 10215 line 4 is 8601 or more; 10216 leaves 8601 - 8600.
        ("10215", "0"),
        ("10216", "1.00"),
        # Line 4 (the line 30300 amount) falls as the net income rises: 18816 - 16129 = 2687.
        ("16129", "5914.00"),
        # From 18816 up line 30300 is 0, so line 5 is line 3, at most 8601.
        ("18816", "8601.00"),
        ("20000", "8601.00"),
        # Line 3 falls below the maximum above 20197 (28798 - 8601): 28798 - 25000 = 3798.
        ("25000", "3798.00"),
        ("28797.99", "0.01"),
        # "net income is between $8,624 and $28,798": at and above the base, line 3 is 0.
        ("28798", "0"),
        ("30000", "0"),
    ],
)
def test_the_caregiver_amount_for_an_infirm_spouse_is_28798_less_their_net_income(
    spouse_net_income: str, amount: str
) -> None:
    worksheet = return_j(spouse_net_income=spouse_net_income)

    assert worksheet.get(SPOUSE_CAREGIVER_AMOUNT).value == D(amount)


@pytest.mark.parametrize("spouse_net_income", ["0", "8623", "12000", "20000"])
def test_there_is_no_caregiver_amount_for_a_spouse_not_eligible_for_it(
    spouse_net_income: str,
) -> None:
    # Line 51090 not entered (the count of eligible spouses is 0): line 30425 is not triggered.
    worksheet = return_j(spouse_net_income=spouse_net_income, spouse_caregiver_eligible=0)

    assert worksheet.get(SPOUSE_CAREGIVER_AMOUNT).value == D("0")


def return_k() -> Worksheet:
    """Return K's inputs, as in `returns/2025_return_k.yaml`: slip and no-slip dividends."""
    return compute(
        "50000",
        "0",
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


def test_return_ks_taxable_dividends_are_the_federal_worksheets_lines_12000_and_12010() -> None:
    # The Federal Worksheet for lines 12000 and 12010: a T5 slip with box 11 of 200 (line 3) and
    # boxes 11 and 25 of 500 (line 8), so lines 5 and 10; no information slip for eligible
    # dividends of 1000 (line 11) and dividends other than eligible of 500 (line 14): line 13 is
    # 1000 x 138% = 1380.00, line 16 is 500 x 115% = 575.00 and line 17 is 1955.00. Line 12010 is
    # line 5 plus line 16, 775.00, and line 12000 is line 10 plus line 17, 2455.00.
    worksheet = return_k()

    assert worksheet.get(SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE).value == D("200")
    assert worksheet.get(SLIP_TAXABLE_DIVIDENDS).value == D("500")
    assert worksheet.get(ELIGIBLE_DIVIDENDS_GROSSED_UP).value == D("1380.00")
    assert worksheet.get(OTHER_DIVIDENDS_GROSSED_UP).value == D("575.00")
    assert worksheet.get(DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP).value == D("1955.00")
    assert worksheet.get(TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE).value == D("775.00")
    assert worksheet.get(TAXABLE_DIVIDENDS).value == D("2455.00")
    assert worksheet.get(TOTAL_INCOME).value == D("52455.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    for line in (
        "slip_taxable_dividends_other_than_eligible: t3_taxable_dividends_other_than_eligible 0 "
        "+ t4ps_taxable_dividends_other_than_eligible 0 "
        "+ t5_taxable_dividends_other_than_eligible 200 "
        "+ t5013_taxable_dividends_other_than_eligible 0 = 200",
        "slip_taxable_dividends: t3_taxable_dividends 0 + t4ps_taxable_dividends 0 "
        "+ t5_taxable_dividends 500 + t5013_taxable_dividends 0 = 500",
        "eligible_dividends_grossed_up: 138/100 of eligible_dividends_received_without_a_slip "
        "1000 (half-up to 0.01)",
        "other_dividends_grossed_up: 115/100 of other_dividends_received_without_a_slip 500 "
        "(half-up to 0.01)",
        "dividends_without_a_slip_grossed_up: eligible_dividends_grossed_up 1380 "
        "+ other_dividends_grossed_up 575 = 1955",
        "taxable_dividends_other_than_eligible: slip_taxable_dividends_other_than_eligible 200 "
        "+ other_dividends_grossed_up 575 = 775",
        "taxable_dividends: slip_taxable_dividends 500 "
        "+ dividends_without_a_slip_grossed_up 1955 = 2455",
    ):
        assert line in rendered, line


def test_return_ks_federal_dividend_tax_credit_counts_the_no_slip_dividends_only() -> None:
    # The Federal Worksheet's "Line 40425": line 5 is the slip credit, 60.00 (T5 boxes 12 and
    # 26). Note 1 "Enter only the amount of dividends that were not shown on an information
    # slip." makes line A the worksheet's line 17, 1955.00, not the 2455.00 of line 12000, and
    # line B its line 16, 575.00, not the 775.00 of line 12010. Line 6 is 575.00 x 9.0301% =
    # 51.92, line C is 1955.00 - 575.00 = 1380.00, line 7 is 1380.00 x 15.0198% = 207.27, line
    # 8 is 259.19 and line 9, and so line 40425, is 60.00 + 259.19 = 319.19.
    worksheet = return_k()

    assert worksheet.get(SLIP_DIVIDEND_TAX_CREDIT).value == D("60.00")
    assert worksheet.get(DIVIDENDS_AMOUNT_A).value == D("1955.00")
    assert worksheet.get(DIVIDENDS_AMOUNT_B).value == D("575.00")
    assert worksheet.get(OTHER_DIVIDENDS_CREDIT).value == D("51.92")
    assert worksheet.get(DIVIDENDS_AMOUNT_A_LESS_B).value == D("1380.00")
    assert worksheet.get(ELIGIBLE_DIVIDENDS_CREDIT).value == D("207.27")
    assert worksheet.get(NO_SLIP_DIVIDEND_TAX_CREDIT).value == D("259.19")
    assert worksheet.get(DIVIDEND_TAX_CREDIT).value == D("319.19")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    for line in (
        "slip_dividend_tax_credit: t3_dividend_tax_credit 0 + t4ps_dividend_tax_credit 0 "
        "+ t5_dividend_tax_credit 60 + t5013_dividend_tax_credit 0 = 60",
        "dividends_amount_a: dividends_without_a_slip_grossed_up 1955 = 1955",
        "dividends_amount_b: other_dividends_grossed_up 575 = 575",
        "other_dividends_credit: 9.0301% of dividends_amount_b 575 (half-up to 0.01)",
        "dividends_amount_a_less_b: dividends_amount_a 1955 less dividends_amount_b 575 = 1380",
        "eligible_dividends_credit: 15.0198% of dividends_amount_a_less_b 1380 (half-up to 0.01)",
        "no_slip_dividend_tax_credit: other_dividends_credit 51.92 "
        "+ eligible_dividends_credit 207.27 = 259.19",
        "dividend_tax_credit: slip_dividend_tax_credit 60 + no_slip_dividend_tax_credit 259.19 "
        "= 319.19",
    ):
        assert line in rendered, line


def test_the_dividend_tax_credit_comes_off_the_basic_federal_tax_with_the_other_credits() -> None:
    # T1 line 125 "Add lines 122 to 124.": line 122 (35000) 3004.65 and line 123 (40425)
    # 319.19, 3323.84; line 126 "Line 121 minus line 125 (if negative, enter "0")" is
    # 7538.55 - 3323.84 = 4214.71, the federal tax after credits carried to the net federal tax.
    worksheet = return_k()

    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("3004.65")
    assert worksheet.get(CREDITS_AGAINST_BASIC_FEDERAL_TAX).value == D("3323.84")
    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("7538.55")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("4214.71")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("4214.71")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("2232.99")
    assert worksheet.get(TOTAL_PAYABLE).value == D("6447.70")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-2552.30")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "credits_against_basic_federal_tax: non_refundable_tax_credits 3004.65 "
        "+ dividend_tax_credit 319.19 = 3323.84"
    ) in rendered
    assert (
        "federal_tax_after_credits: federal_basic_tax 7538.55 "
        "less credits_against_basic_federal_tax 3323.84, not below 0 = 4214.71"
    ) in rendered


def test_slip_credits_of_100_and_no_other_dividends_give_line_40425_of_100() -> None:
    # Line 5 of the credit chart is 100.00 and nothing is on line A or B: "Otherwise, enter the
    # amount from line 5 on line 40425 of your return."
    worksheet = compute("50000", "0", "0", "0", "0", "0", "0", t5_dividend_tax_credit="100.00")

    assert worksheet.get(SLIP_DIVIDEND_TAX_CREDIT).value == D("100.00")
    assert worksheet.get(OTHER_DIVIDENDS_CREDIT).value == D("0")
    assert worksheet.get(ELIGIBLE_DIVIDENDS_CREDIT).value == D("0")
    assert worksheet.get(NO_SLIP_DIVIDEND_TAX_CREDIT).value == D("0")
    assert worksheet.get(DIVIDEND_TAX_CREDIT).value == D("100.00")
    assert worksheet.get(TAXABLE_DIVIDENDS).value == D("0")
    assert worksheet.get(CREDITS_AGAINST_BASIC_FEDERAL_TAX).value == (
        worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value + D("100.00")
    )


def test_dividends_on_slips_alone_are_not_grossed_up_and_leave_lines_a_and_b_at_zero() -> None:
    # Slip amounts of 800 (T5 boxes 11 and 25) and 300 (box 11) are lines 12000 and 12010 as
    # they stand, and the slip credit of 70.00 is line 40425: with nothing received without a
    # slip, lines A and B and the credits computed from them are 0.
    worksheet = compute(
        "50000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        t5_taxable_dividends_other_than_eligible="300",
        t5_taxable_dividends="800",
        t5_dividend_tax_credit="70.00",
    )

    assert worksheet.get(TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE).value == D("300")
    assert worksheet.get(TAXABLE_DIVIDENDS).value == D("800")
    assert worksheet.get(DIVIDENDS_AMOUNT_A).value == D("0")
    assert worksheet.get(DIVIDENDS_AMOUNT_B).value == D("0")
    assert worksheet.get(NO_SLIP_DIVIDEND_TAX_CREDIT).value == D("0")
    assert worksheet.get(DIVIDEND_TAX_CREDIT).value == D("70.00")
    assert worksheet.get(TOTAL_INCOME).value == D("50800")


def test_each_slip_box_adds_to_its_worksheet_line_once() -> None:
    # Distinct powers of two, one per slip line, so a line left out or added twice changes the
    # sum: lines 1 to 4 (T3, T4PS, T5, T5013) 1 + 2 + 4 + 8 = 15, lines 6 to 9 16 + 32 + 64 +
    # 128 = 240, and credit lines 1 to 4 256 + 512 + 1024 + 2048 = 3840.
    worksheet = compute(
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        t3_taxable_dividends_other_than_eligible="1",
        t4ps_taxable_dividends_other_than_eligible="2",
        t5_taxable_dividends_other_than_eligible="4",
        t5013_taxable_dividends_other_than_eligible="8",
        t3_taxable_dividends="16",
        t4ps_taxable_dividends="32",
        t5_taxable_dividends="64",
        t5013_taxable_dividends="128",
        t3_dividend_tax_credit="256",
        t4ps_dividend_tax_credit="512",
        t5_dividend_tax_credit="1024",
        t5013_dividend_tax_credit="2048",
    )

    assert worksheet.get(SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE).value == D("15")
    assert worksheet.get(SLIP_TAXABLE_DIVIDENDS).value == D("240")
    assert worksheet.get(SLIP_DIVIDEND_TAX_CREDIT).value == D("3840")
    assert worksheet.get(DIVIDEND_TAX_CREDIT).value == D("3840")


def test_a_dividend_credit_above_the_basic_tax_leaves_zero_federal_tax_not_a_refund() -> None:
    # Low income, so a small basic tax: the credits against it (35000 and 40425) are more, and
    # the unused part is lost, as line 126 is "if negative, enter "0"".
    worksheet = compute("10000", "0", "0", "0", "0", "0", "0", t5_dividend_tax_credit="5000")

    assert (
        worksheet.get(CREDITS_AGAINST_BASIC_FEDERAL_TAX).value
        > worksheet.get(FEDERAL_BASIC_TAX).value
    )
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("0")


def test_the_other_payments_deduction_is_line_14700_when_nothing_was_entered_on_line_14600() -> (
    None
):
    # T1 line 60 and line 25000 "enter the amount from line 14700 if you did not enter an amount on
    # line 14600": workers' compensation 2000 (line 14400) and social assistance 300 (line 14500)
    # make line 14700 2300, and with no amount on line 14600 (count 0) that is line 25000, whatever
    # the chart amount of 999 and the count of 1 for a line 9 over the limit, which only the
    # worksheet reads. Employment income 30000: enhanced CPP contributions 1% x (30000 - 3500) =
    # 265.00, total income 30000 + 2300 = 32300, net income 32035.00, taxable income
    # 32035.00 - 2300 = 29735.00.
    worksheet = compute(
        "30000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        workers_compensation_benefits="2000",
        social_assistance_payments="300",
        other_payments_deduction_above_limit="999",
        other_payments_worksheet_line_9_over_limit=1,
    )

    assert worksheet.get(INCOME_SUPPORT_BENEFITS).value == D("2300")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT).value == D("999")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("2300")
    assert worksheet.get(DEDUCTIONS_FROM_NET_INCOME).value == D("2300")
    assert worksheet.get(NET_INCOME).value == D("32035.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("29735.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "other_payments_deduction: income_support_benefits 2300, "
        "chosen as other_payments_worksheet_required is 0"
    ) in rendered


def test_the_worksheets_lines_4_5_8_and_9_with_supplements_uccb_rdsp_income_and_repayments() -> (
    None
):
    # Federal Worksheet "Line 25000 - Other payments deduction" for a filer with net federal
    # supplements of 400 on line 14600 (count 1). Employment income 50000, UCCB 1000 (line
    # 11700), RDSP income 3000 (line 12500): total income 50000 + 1000 + 3000 + 400 = 54400,
    # enhanced CPP contributions 1% x (50000 - 3500) = 465.00. Line 6 (UCCB repayment) 200 is
    # also T1 line 21300, and line 7 (RDSP income repayment) 100 is "included in the amount on
    # line 23200 of your return", so line 23200 is 100: total deductions are 200 + 100 + 465.00 =
    # 765.00, so net income (line 1) is 54400 - 765.00 = 53635.00. Line 4 is 1000 + 3000 = 4000;
    # line 5 is 53635.00 - 4000 = 49635.00; lines 6 and 7 make line 8 300; line 9 is 49635.00 +
    # 300 = 49935.00, not more than $93,454 (count 0), so line 25000 is line 14700, 400, and
    # taxable income is 53635.00 - 400 = 53235.00.
    worksheet = compute(
        "50000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        universal_child_care_benefit="1000",
        rdsp_income="3000",
        net_federal_supplements="400",
        uccb_repayment="200",
        rdsp_income_repayment="100",
        other_deductions="100",
        other_payments_worksheet_required=1,
    )

    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("765.00")
    assert worksheet.get(NET_INCOME).value == D("53635.00")
    assert worksheet.get(UCCB_AND_RDSP_INCOME).value == D("4000")
    assert worksheet.get(NET_INCOME_LESS_UCCB_AND_RDSP_INCOME).value == D("49635.00")
    assert worksheet.get(UCCB_AND_RDSP_INCOME_REPAYMENTS).value == D("300")
    assert worksheet.get(OTHER_PAYMENTS_LIMIT_INCOME).value == D("49935.00")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT).value == D("400")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("400")
    assert worksheet.get(TAXABLE_INCOME).value == D("53235.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert "uccb_and_rdsp_income: universal_child_care_benefit 1000 + rdsp_income 3000 = 4000" in (
        rendered
    )
    assert (
        "net_income_less_uccb_and_rdsp_income: net_income 53635 less uccb_and_rdsp_income 4000 "
        "= 49635"
    ) in rendered
    assert (
        "uccb_and_rdsp_income_repayments: uccb_repayment 200 + rdsp_income_repayment 100 = 300"
    ) in rendered
    assert (
        "other_payments_limit_income: net_income_less_uccb_and_rdsp_income 49635 "
        "+ uccb_and_rdsp_income_repayments 300 = 49935"
    ) in rendered
    assert (
        "other_payments_deduction_after_limit: income_support_benefits 400, "
        "chosen as other_payments_worksheet_line_9_over_limit is 0"
    ) in rendered
    assert (
        "other_payments_deduction: other_payments_deduction_after_limit 400, "
        "chosen as other_payments_worksheet_required is 1"
    ) in rendered


def test_a_line_9_over_93454_takes_the_charts_amount_as_line_25000() -> None:
    # "If the amount on line 9 is more than $93,454, go to canada.ca/line-25000 to find out how
    # much you can deduct": employment income 100000, workers' compensation 1500 and net federal
    # supplements 500 (line 14700 is 2000), total income 102000, enhanced CPP contributions
    # 678.00 + 396.00 = 1074.00, net income 100926.00; with no UCCB, RDSP income or repayments
    # line 9 is 100926.00, over the limit (count 1), so line 25000 is the chart's amount, a
    # chosen 700, not line 14700, and taxable income is 100926.00 - 700 = 100226.00.
    worksheet = compute(
        "100000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        workers_compensation_benefits="1500",
        net_federal_supplements="500",
        other_payments_deduction_above_limit="700",
        other_payments_worksheet_required=1,
        other_payments_worksheet_line_9_over_limit=1,
    )

    assert worksheet.get(INCOME_SUPPORT_BENEFITS).value == D("2000")
    assert worksheet.get(NET_INCOME).value == D("100926.00")
    assert worksheet.get(OTHER_PAYMENTS_LIMIT_INCOME).value == D("100926.00")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT).value == D("700")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("700")
    assert worksheet.get(TAXABLE_INCOME).value == D("100226.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "other_payments_deduction_after_limit: other_payments_deduction_above_limit 700, "
        "chosen as other_payments_worksheet_line_9_over_limit is 1"
    ) in rendered
    assert (
        "other_payments_deduction: other_payments_deduction_after_limit 700, "
        "chosen as other_payments_worksheet_required is 1"
    ) in rendered


def test_line_9_may_be_negative_as_the_form_prints_no_floor() -> None:
    # Net income 0 (UCCB of 1000 less union dues of 1500, not below zero) less line 4 (1000) is
    # line 5, -1000, with no repayments line 9 is -1000, not over the limit, so with an amount on
    # line 14600 of 0 entered as such (count 1) line 25000 is line 14700, 0.
    worksheet = compute(
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "1500",
        universal_child_care_benefit="1000",
        other_payments_worksheet_required=1,
    )

    assert worksheet.get(NET_INCOME).value == D("0")
    assert worksheet.get(NET_INCOME_LESS_UCCB_AND_RDSP_INCOME).value == D("-1000")
    assert worksheet.get(OTHER_PAYMENTS_LIMIT_INCOME).value == D("-1000")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("0")


def test_deductions_from_net_income_add_lines_58_to_63_and_67_once_each() -> None:
    # T1 line 68 and line 25700 "Add lines 58 to 67.": one distinct power of two for each of the
    # seven lines wired: line 24400 1, line 24900 2, line 25000 4 (workers' compensation of 4, so
    # line 14700, with no amount on line 14600), line 25100 8, line 25200 16, line 25300 32 (a
    # capital gain of 64, taxable capital gains of 32.00, and unapplied net capital losses of 32
    # claimed whole) and line 25600 64, so a line left out or added twice changes the sum: 127.
    # Other income 1000 and workers' compensation 4 and taxable capital gains 32.00 give total
    # income 1036.00 and taxable income 1036.00 - 127 = 909.00.
    worksheet = compute(
        "0",
        "64",
        "0",
        "0",
        "0",
        "0",
        "0",
        other_income="1000",
        workers_compensation_benefits="4",
        canadian_armed_forces_and_police_deduction="1",
        security_options_deductions="2",
        limited_partnership_losses_of_other_years="8",
        non_capital_losses_of_other_years="16",
        unapplied_net_capital_losses_2001_to_2024="32",
        net_capital_losses_claimed="32",
        additional_deductions="64",
    )

    assert worksheet.get(TAXABLE_CAPITAL_GAINS).value == D("32.00")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("4")
    assert worksheet.get(NET_CAPITAL_LOSSES_OF_OTHER_YEARS).value == D("32")
    assert worksheet.get(DEDUCTIONS_FROM_NET_INCOME).value == D("127")
    assert worksheet.get(TAXABLE_INCOME).value == D("909.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "deductions_from_net_income: canadian_armed_forces_and_police_deduction 1 "
        "+ security_options_deductions 2 + other_payments_deduction 4 "
        "+ limited_partnership_losses_of_other_years 8 + non_capital_losses_of_other_years 16 "
        "+ net_capital_losses_of_other_years 32 + additional_deductions 64 = 127"
    ) in rendered


def test_return_ls_deductions_from_net_income_are_8500_and_its_taxable_income_34500() -> None:
    # Return L: employment income 40000 and other income 1365 (line 13000), both chosen, and
    # workers' compensation 2000 (line 14400): total income 43365; enhanced CPP contributions
    # 1% x (40000 - 3500) = 365.00; net income 43000.00. Line 25000 is line 14700, 2000.00;
    # security options deduction 1500 (line 24900) and non-capital losses of other years 5000
    # (line 25200): line 25700 is 1500 + 2000 + 5000 = 8500, taxable income 43000.00 - 8500 =
    # 34500.00.
    worksheet = compute(
        "40000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        other_income="1365",
        workers_compensation_benefits="2000",
        security_options_deductions="1500",
        non_capital_losses_of_other_years="5000",
    )

    assert worksheet.get(TOTAL_INCOME).value == D("43365")
    assert worksheet.get(NET_INCOME).value == D("43000.00")
    assert worksheet.get(OTHER_PAYMENTS_DEDUCTION).value == D("2000")
    assert worksheet.get(DEDUCTIONS_FROM_NET_INCOME).value == D("8500")
    assert worksheet.get(TAXABLE_INCOME).value == D("34500.00")


def return_af(capital_gain: str = "5000", **overrides: Any) -> Worksheet:
    """Return AF's inputs, as in `returns/2025_return_af.yaml`: Return AE's filer, no political
    contributions, with a capital gain and unapplied net capital losses of other years.

    Employment income of 48000, a capital gain of 5000 (taxable capital gains of 2500.00),
    4800 deducted, unapplied net capital losses of 3000 from 1990 to 1999 and 1000 from 2001 to
    2024 (Form T1436 Chart A column A), and an amount claimed (line 7) of 2500.
    """
    inputs: dict[str, Any] = {
        "income_tax_deducted": "4800",
        "unapplied_net_capital_losses_1990_to_1999": "3000",
        "unapplied_net_capital_losses_2001_to_2024": "1000",
        "net_capital_losses_claimed": "2500",
    }
    return compute("48000", capital_gain, "0", "0", "8640", "0", "0", **{**inputs, **overrides})


def test_return_afs_claim_is_applied_to_the_oldest_row_first_and_lowers_taxable_income() -> None:
    # Form T1436 Chart A: a 1995 loss of 3000 (row "After 1989 and before 2000", column B 2/3) gives
    # column C 3000 x 2/3 = 2000.00; a 2010 loss of 1000 (row "After 2000 and before 2025", column B
    # 1) gives 1000 x 1 = 1000.00; the other two rows have no loss: 0.00. Line 4 is 3000.00 and line
    # 5, the taxable capital gains (line 12700), is 5000 x 50% = 2500.00, so line 6 is 2500.00. The
    # claim of 2500 (line 7, which is also T1 line 25300 and line 13) is at most line 6. It is
    # applied oldest row first: column D is 0.00 for each of the first two rows, 2000.00 for the
    # 1990 to 1999 row (of the 2500 left, 500.00 remains) and 500.00 for the 2001 to 2024 row.
    # Column E is column C less column D: 0.00, 0.00, 0.00 and 500.00; column G is column E x
    # column F (1, 4/3, 3/2 and 1): 0.00, 0.00, 0.00 and 500.00. Net income is 50500.00 - 445.00 =
    # 50055.00 (the deduction is below net income); line 25700 is 2500 and taxable income is
    # 47555.00. The LIFT credit's reduction is 5% x (50055.00 - 32500) = 877.75, more than 875, so
    # the credit is 0; the Ontario tax is 1606.81 + 450 = 2056.81 and the total payable is
    # 3909.94 + 2056.81 = 5966.75, against total credits of 4800.00: 1166.75 owing.
    worksheet = return_af()

    assert worksheet.get(TAXABLE_CAPITAL_GAINS).value == D("2500.00")
    assert worksheet.get(ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987).value == D("0.00")
    assert worksheet.get(ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989).value == D("0.00")
    assert worksheet.get(ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999).value == D("2000.00")
    assert worksheet.get(ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024).value == D("1000.00")
    assert worksheet.get(TOTAL_ADJUSTED_NET_CAPITAL_LOSSES).value == D("3000.00")
    assert worksheet.get(NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM).value == D("2500.00")
    assert worksheet.get(NET_CAPITAL_LOSSES_OF_OTHER_YEARS).value == D("2500")
    assert worksheet.get(ADJUSTED_LOSSES_APPLIED_1985_TO_1987).value == D("0.00")
    assert worksheet.get(ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987).value == D("2500.00")
    assert worksheet.get(ADJUSTED_LOSSES_APPLIED_1988_AND_1989).value == D("0.00")
    assert worksheet.get(ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989).value == D("2500.00")
    assert worksheet.get(ADJUSTED_LOSSES_APPLIED_1990_TO_1999).value == D("2000.00")
    assert worksheet.get(ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999).value == D("500.00")
    assert worksheet.get(ADJUSTED_LOSSES_APPLIED_2001_TO_2024).value == D("500.00")
    assert worksheet.get(REMAINING_ADJUSTED_LOSSES_1985_TO_1987).value == D("0.00")
    assert worksheet.get(REMAINING_ADJUSTED_LOSSES_1988_AND_1989).value == D("0.00")
    assert worksheet.get(REMAINING_ADJUSTED_LOSSES_1990_TO_1999).value == D("0.00")
    assert worksheet.get(REMAINING_ADJUSTED_LOSSES_2001_TO_2024).value == D("500.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_1985_TO_1987).value == D("0.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_1988_AND_1989).value == D("0.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_1990_TO_1999).value == D("0.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_2001_TO_2024).value == D("500.00")
    assert worksheet.get(DEDUCTIONS_FROM_NET_INCOME).value == D("2500")
    assert worksheet.get(NET_INCOME).value == D("50055.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("47555.00")
    assert worksheet.get(LIFT_CREDIT).value == D("0")
    assert worksheet.get(ONTARIO_TAX).value == D("2056.81")
    assert worksheet.get(TOTAL_PAYABLE).value == D("5966.75")
    assert worksheet.get(TOTAL_CREDITS).value == D("4800.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("1166.75")
    assert worksheet.get(REFUND).value == D("0")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "adjusted_gross_capital_losses_1990_to_1999: 2/3 of "
        "unapplied_net_capital_losses_1990_to_1999 3000 (half-up to 0.01)"
    ) in rendered
    assert (
        "adjusted_gross_capital_losses_2001_to_2024: 1/1 of "
        "unapplied_net_capital_losses_2001_to_2024 1000 (half-up to 0.01)"
    ) in rendered
    assert (
        "total_adjusted_net_capital_losses: adjusted_gross_capital_losses_1985_to_1987 0 "
        "+ adjusted_gross_capital_losses_1988_and_1989 0 "
        "+ adjusted_gross_capital_losses_1990_to_1999 2000 "
        "+ adjusted_gross_capital_losses_2001_to_2024 1000 = 3000"
    ) in rendered
    assert (
        "net_capital_losses_available_to_claim: lesser of total_adjusted_net_capital_losses 3000 "
        "and taxable_capital_gains 2500 = 2500"
    ) in rendered
    assert (
        "net_capital_losses_of_other_years: net_capital_losses_claimed 2500, "
        "at most net_capital_losses_available_to_claim 2500"
    ) in rendered
    assert (
        "adjusted_losses_applied_1990_to_1999: lesser of "
        "adjusted_gross_capital_losses_1990_to_1999 2000 "
        "and adjusted_losses_left_after_1988_and_1989 2500 = 2000"
    ) in rendered
    assert (
        "adjusted_losses_left_after_1990_to_1999: adjusted_losses_left_after_1988_and_1989 2500 "
        "less adjusted_losses_applied_1990_to_1999 2000 = 500"
    ) in rendered
    assert (
        "adjusted_losses_applied_2001_to_2024: lesser of "
        "adjusted_gross_capital_losses_2001_to_2024 1000 "
        "and adjusted_losses_left_after_1990_to_1999 500 = 500"
    ) in rendered
    assert (
        "remaining_adjusted_losses_2001_to_2024: adjusted_gross_capital_losses_2001_to_2024 1000 "
        "less adjusted_losses_applied_2001_to_2024 500 = 500"
    ) in rendered
    assert (
        "net_capital_loss_balance_2001_to_2024: 1/1 of remaining_adjusted_losses_2001_to_2024 500 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "deductions_from_net_income: canadian_armed_forces_and_police_deduction 0 "
        "+ security_options_deductions 0 + other_payments_deduction 0 "
        "+ limited_partnership_losses_of_other_years 0 + non_capital_losses_of_other_years 0 "
        "+ net_capital_losses_of_other_years 2500 + additional_deductions 0 = 2500"
    ) in rendered
    assert (
        "taxable_income: net_income 50055 less deductions_from_net_income 2500, not below 0 = 47555"
    ) in rendered


def test_the_claim_lowers_taxable_income_and_leaves_net_income() -> None:
    # Guide T4037: applying a net capital loss of another year "will not change" net income, which
    # is used to calculate certain credits and benefits; it reduces taxable income only.
    claimed = return_af()
    unclaimed = return_af(net_capital_losses_claimed="0")

    assert claimed.get(NET_INCOME).value == D("50055.00")
    assert unclaimed.get(NET_INCOME).value == D("50055.00")
    assert claimed.get(ADJUSTED_FAMILY_NET_INCOME).value == D("50055.00")
    assert claimed.get(TAXABLE_INCOME).value == D("47555.00")
    assert unclaimed.get(TAXABLE_INCOME).value == D("50055.00")
    assert unclaimed.get(DEDUCTIONS_FROM_NET_INCOME).value == D("0")


def test_a_claim_above_the_lesser_of_the_losses_and_the_taxable_gains_is_refused() -> None:
    # Form T1436 line 7, note (3): "You can apply all or part of the amount from line 6": line 6 is
    # 2500.00 (the taxable capital gains, below the 3000.00 of losses), so 2500.01 is an input
    # error, not capped to 2500.00.
    with pytest.raises(InputAboveBoundError) as raised:
        return_af(net_capital_losses_claimed="2500.01")

    assert str(raised.value) == (
        "ca/net_capital_losses_claimed 2500.01 is above "
        "ca/net_capital_losses_available_to_claim 2500.00"
    )


def test_a_claim_with_no_taxable_capital_gains_is_refused_naming_both_kinds() -> None:
    # No capital gain: line 5 is 0.00, so line 6 is 0.00 whatever the losses, and a claim of 1 is
    # above it.
    with pytest.raises(InputAboveBoundError) as raised:
        compute(
            "48000",
            "0",
            "0",
            "0",
            "8640",
            "0",
            "0",
            unapplied_net_capital_losses_2001_to_2024="1000",
            net_capital_losses_claimed="1",
        )

    assert str(raised.value) == (
        "ca/net_capital_losses_claimed 1 is above ca/net_capital_losses_available_to_claim 0.00"
    )


def test_a_claim_of_zero_with_no_taxable_capital_gains_is_allowed() -> None:
    worksheet = compute(
        "48000",
        "0",
        "0",
        "0",
        "8640",
        "0",
        "0",
        unapplied_net_capital_losses_2001_to_2024="1000",
    )

    assert worksheet.get(NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM).value == D("0.00")
    assert worksheet.get(NET_CAPITAL_LOSSES_OF_OTHER_YEARS).value == D("0")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_2001_TO_2024).value == D("1000.00")


def test_line_6_is_the_taxable_capital_gains_when_the_losses_are_larger() -> None:
    # Losses of 10000 from 2001 to 2024 (column C 10000.00) against taxable capital gains of
    # 2500.00: line 6 is 2500.00 and a claim of 2500 leaves 7500.00 for next year.
    worksheet = return_af(
        unapplied_net_capital_losses_1990_to_1999="0",
        unapplied_net_capital_losses_2001_to_2024="10000",
    )

    assert worksheet.get(TOTAL_ADJUSTED_NET_CAPITAL_LOSSES).value == D("10000.00")
    assert worksheet.get(NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM).value == D("2500.00")
    assert worksheet.get(ADJUSTED_LOSSES_APPLIED_2001_TO_2024).value == D("2500.00")
    assert worksheet.get(REMAINING_ADJUSTED_LOSSES_2001_TO_2024).value == D("7500.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_2001_TO_2024).value == D("7500.00")
    with pytest.raises(InputAboveBoundError):
        return_af(
            unapplied_net_capital_losses_1990_to_1999="0",
            unapplied_net_capital_losses_2001_to_2024="10000",
            net_capital_losses_claimed="2500.01",
        )


def test_line_6_is_the_total_of_column_c_when_the_taxable_gains_are_larger() -> None:
    # A capital gain of 20000 (taxable capital gains of 10000.00) against column C of 3000.00: line
    # 6 is 3000.00, the whole of both rows is applied and nothing is left to carry forward.
    worksheet = return_af(capital_gain="20000", net_capital_losses_claimed="3000")

    assert worksheet.get(TAXABLE_CAPITAL_GAINS).value == D("10000.00")
    assert worksheet.get(NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM).value == D("3000.00")
    assert worksheet.get(NET_CAPITAL_LOSSES_OF_OTHER_YEARS).value == D("3000")
    assert worksheet.get(ADJUSTED_LOSSES_APPLIED_1990_TO_1999).value == D("2000.00")
    assert worksheet.get(ADJUSTED_LOSSES_APPLIED_2001_TO_2024).value == D("1000.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_1990_TO_1999).value == D("0.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_2001_TO_2024).value == D("0.00")
    assert worksheet.get(DEDUCTIONS_FROM_NET_INCOME).value == D("3000")


def test_a_partial_claim_uses_the_oldest_row_first_and_carries_the_rest_forward() -> None:
    # A claim of 1000 against column C of 2000.00 (1990 to 1999) and 1000.00 (2001 to 2024): all
    # of it comes off the older row, column D 1000.00 and 0.00; column E is 1000.00 for each;
    # column G is 1000.00 x 3/2 = 1500.00 for the older row and 1000.00 x 1 = 1000.00.
    worksheet = return_af(net_capital_losses_claimed="1000")

    assert worksheet.get(ADJUSTED_LOSSES_APPLIED_1990_TO_1999).value == D("1000.00")
    assert worksheet.get(ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999).value == D("0.00")
    assert worksheet.get(ADJUSTED_LOSSES_APPLIED_2001_TO_2024).value == D("0.00")
    assert worksheet.get(REMAINING_ADJUSTED_LOSSES_1990_TO_1999).value == D("1000.00")
    assert worksheet.get(REMAINING_ADJUSTED_LOSSES_2001_TO_2024).value == D("1000.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_1990_TO_1999).value == D("1500.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_2001_TO_2024).value == D("1000.00")
    assert worksheet.get(DEDUCTIONS_FROM_NET_INCOME).value == D("1000")


def test_no_claim_keeps_every_loss_and_gives_back_the_unapplied_amounts() -> None:
    # Nothing claimed: column D is 0.00 everywhere, column E is column C, and column G is column E x
    # column F: 2000.00 x 3/2 = 3000.00 and 1000.00 x 1, the unapplied losses of column A again.
    worksheet = return_af(net_capital_losses_claimed="0")

    assert worksheet.get(NET_CAPITAL_LOSSES_OF_OTHER_YEARS).value == D("0")
    assert worksheet.get(ADJUSTED_LOSSES_APPLIED_1990_TO_1999).value == D("0.00")
    assert worksheet.get(ADJUSTED_LOSSES_APPLIED_2001_TO_2024).value == D("0.00")
    assert worksheet.get(REMAINING_ADJUSTED_LOSSES_1990_TO_1999).value == D("2000.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_1990_TO_1999).value == D("3000.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_2001_TO_2024).value == D("1000.00")


def test_all_four_rows_are_applied_oldest_first_and_column_d_adds_up_to_line_13() -> None:
    # Column A: 100, 400, 600 and 500. Column C (x 1, 3/4, 2/3, 1): 100.00, 300.00, 400.00 and
    # 500.00; line 4 is 1300.00, below the taxable capital gains of 2500.00, so line 6 is 1300.00. A
    # claim of 700: column D is 100.00, 300.00, 300.00 and 0.00 (700 left, then 600.00, 300.00 and
    # 0.00 left after each of the first three), which add up to 700, line 13. Column E is 0.00,
    # 0.00, 100.00 and 500.00; column G (x 1, 4/3, 3/2 and 1) is 0.00, 0.00, 150.00 and 500.00.
    worksheet = return_af(
        unapplied_net_capital_losses_1985_to_1987="100",
        unapplied_net_capital_losses_1988_and_1989="400",
        unapplied_net_capital_losses_1990_to_1999="600",
        unapplied_net_capital_losses_2001_to_2024="500",
        net_capital_losses_claimed="700",
    )

    assert worksheet.get(ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987).value == D("100.00")
    assert worksheet.get(ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989).value == D("300.00")
    assert worksheet.get(ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999).value == D("400.00")
    assert worksheet.get(ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024).value == D("500.00")
    assert worksheet.get(TOTAL_ADJUSTED_NET_CAPITAL_LOSSES).value == D("1300.00")
    assert worksheet.get(NET_CAPITAL_LOSSES_AVAILABLE_TO_CLAIM).value == D("1300.00")
    applied = [
        worksheet.get(kind).value
        for kind in (
            ADJUSTED_LOSSES_APPLIED_1985_TO_1987,
            ADJUSTED_LOSSES_APPLIED_1988_AND_1989,
            ADJUSTED_LOSSES_APPLIED_1990_TO_1999,
            ADJUSTED_LOSSES_APPLIED_2001_TO_2024,
        )
    ]
    assert applied == [D("100.00"), D("300.00"), D("300.00"), D("0.00")]
    assert sum(applied) == worksheet.get(NET_CAPITAL_LOSSES_OF_OTHER_YEARS).value == D("700")
    assert worksheet.get(ADJUSTED_LOSSES_LEFT_AFTER_1985_TO_1987).value == D("600.00")
    assert worksheet.get(ADJUSTED_LOSSES_LEFT_AFTER_1988_AND_1989).value == D("300.00")
    assert worksheet.get(ADJUSTED_LOSSES_LEFT_AFTER_1990_TO_1999).value == D("0.00")
    assert worksheet.get(REMAINING_ADJUSTED_LOSSES_1985_TO_1987).value == D("0.00")
    assert worksheet.get(REMAINING_ADJUSTED_LOSSES_1988_AND_1989).value == D("0.00")
    assert worksheet.get(REMAINING_ADJUSTED_LOSSES_1990_TO_1999).value == D("100.00")
    assert worksheet.get(REMAINING_ADJUSTED_LOSSES_2001_TO_2024).value == D("500.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_1985_TO_1987).value == D("0.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_1988_AND_1989).value == D("0.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_1990_TO_1999).value == D("150.00")
    assert worksheet.get(NET_CAPITAL_LOSS_BALANCE_2001_TO_2024).value == D("500.00")


@pytest.mark.parametrize(
    ("row", "loss", "adjusted", "balance"),
    [
        # The form prints 0.75 and 1.33, whose product is 0.9975; the exact fractions 3/4 and 4/3
        # give the loss back: 900 x 3/4 = 675.00 and 675.00 x 4/3 = 900.00.
        ("1988_and_1989", "900", "675.00", "900.00"),
        # The form prints 0.6667 and 1.5; the exact fractions 2/3 and 3/2: 900 x 2/3 = 600.00 and
        # 600.00 x 3/2 = 900.00.
        ("1990_to_1999", "900", "600.00", "900.00"),
        # Half-up to the cent at column C: 0.02 x 3/4 = 0.015 is 0.02, and at column G: 0.02 x 4/3
        # = 0.02666... is 0.03.
        ("1988_and_1989", "0.02", "0.02", "0.03"),
        # 1.01 x 2/3 = 0.67333... is 0.67 (not carried unrounded to column G); 0.67 x 3/2 = 1.005
        # is 1.01.
        ("1990_to_1999", "1.01", "0.67", "1.01"),
        # Factors of 1 change nothing: 1234.56 x 1.
        ("1985_to_1987", "1234.56", "1234.56", "1234.56"),
        ("2001_to_2024", "1234.56", "1234.56", "1234.56"),
    ],
)
def test_columns_c_and_g_use_the_exact_fractions_rounded_half_up_to_the_cent(
    row: str, loss: str, adjusted: str, balance: str
) -> None:
    kinds = {
        "1985_to_1987": (
            ADJUSTED_GROSS_CAPITAL_LOSSES_1985_TO_1987,
            NET_CAPITAL_LOSS_BALANCE_1985_TO_1987,
        ),
        "1988_and_1989": (
            ADJUSTED_GROSS_CAPITAL_LOSSES_1988_AND_1989,
            NET_CAPITAL_LOSS_BALANCE_1988_AND_1989,
        ),
        "1990_to_1999": (
            ADJUSTED_GROSS_CAPITAL_LOSSES_1990_TO_1999,
            NET_CAPITAL_LOSS_BALANCE_1990_TO_1999,
        ),
        "2001_to_2024": (
            ADJUSTED_GROSS_CAPITAL_LOSSES_2001_TO_2024,
            NET_CAPITAL_LOSS_BALANCE_2001_TO_2024,
        ),
    }
    column_c, column_g = kinds[row]
    losses: dict[str, Any] = {f"unapplied_net_capital_losses_{row}": loss}
    worksheet = compute("48000", "20000", "0", "0", "8640", "0", "0", **losses)

    assert worksheet.get(column_c).value == D(adjusted)
    assert worksheet.get(column_g).value == D(balance)


def test_return_ks_ontario_dividend_tax_credit_uses_the_whole_lines_12000_and_12010() -> None:
    # Worksheet ON428's "Line 61520" has no Note 1: line A is the whole line 12000, 2455.00, and
    # line B the whole line 12010, 775.00 (the federal lines A and B, 1955.00 and 575.00, count
    # the no-slip dividends only). Line 1 is 775.00 x 2.9863% = 23.143825, 23.14; line C is
    # 2455.00 - 775.00 = 1680.00; line 2 is 1680.00 x 10% = 168.00; line 3, and so line 61520
    # and ON428 line 57, is 23.14 + 168.00 = 191.14. The slip credit of 60.00 is the federal
    # credit's and is not read.
    worksheet = return_k()

    assert worksheet.get(ontario.DIVIDENDS_AMOUNT_A).value == D("2455.00")
    assert worksheet.get(ontario.DIVIDENDS_AMOUNT_B).value == D("775.00")
    assert worksheet.get(ontario.OTHER_DIVIDENDS_CREDIT).value == D("23.14")
    assert worksheet.get(ontario.DIVIDENDS_AMOUNT_A_LESS_B).value == D("1680.00")
    assert worksheet.get(ontario.ELIGIBLE_DIVIDENDS_CREDIT).value == D("168.00")
    assert worksheet.get(ontario.DIVIDEND_TAX_CREDIT).value == D("191.14")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    for line in (
        "dividends_amount_a: taxable_dividends 2455 = 2455",
        "dividends_amount_b: taxable_dividends_other_than_eligible 775 = 775",
        "other_dividends_credit: 2.9863% of dividends_amount_b 775 (half-up to 0.01)",
        "dividends_amount_a_less_b: dividends_amount_a 2455 less dividends_amount_b 775 = 1680",
        "eligible_dividends_credit: 10% of dividends_amount_a_less_b 1680 (half-up to 0.01)",
        "dividend_tax_credit: other_dividends_credit 23.14 + eligible_dividends_credit 168 "
        "= 191.14",
    ):
        assert line in rendered, line


def test_the_ontario_dividend_tax_credit_comes_off_the_tax_at_lines_58_and_71() -> None:
    # ON428 line 56 is line 53, 1824.13, and line 58 "Line 56 minus line 57" is 1824.13 -
    # 191.14 = 1632.99. Line 69 is 1824.13 (no surtax below 5710) and line 70 is line 57,
    # 191.14, so line 71 "Line 69 minus line 70" is 1632.99, as is line 73. Twice the reduction
    # amounts, 588.00, is below it, so line 80 is 0 and line 81 is 1632.99; the lift credit
    # (line 85) is 0; the health premium of 600.00 is added: line 90, the Ontario tax, is
    # 2232.99.
    worksheet = return_k()

    assert worksheet.get(ontario.ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT).value == D("1824.13")
    assert worksheet.get(ontario.ONTARIO_TAX_LESS_DIVIDEND_CREDIT).value == D("1632.99")
    assert worksheet.get(ontario.ONTARIO_TAX_WITH_SURTAX).value == D("1824.13")
    assert worksheet.get(ontario.DIVIDEND_CREDIT_FROM_LINE_57).value == D("191.14")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT).value == D("1632.99")
    assert worksheet.get(ontario.ONTARIO_TAX_REDUCTION).value == D("0")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_REDUCTION).value == D("1632.99")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_FOOD_CREDIT).value == D("1632.99")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("2232.99")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    for line in (
        "ontario_tax_before_dividend_credit: ontario_tax_after_credits 1824.13 = 1824.13",
        "ontario_tax_less_dividend_credit: ontario_tax_before_dividend_credit 1824.13 "
        "less dividend_tax_credit 191.14, not below 0 = 1632.99",
        "dividend_credit_from_line_57: dividend_tax_credit 191.14 = 191.14",
        "ontario_tax_after_dividend_credit: ontario_tax_with_surtax 1824.13 "
        "less dividend_credit_from_line_57 191.14, not below 0 = 1632.99",
        "ontario_tax_after_reduction: ontario_tax_after_dividend_credit 1632.99 "
        "less ontario_tax_reduction 0, not below 0 = 1632.99",
    ):
        assert line in rendered, line


def test_dividends_received_with_no_slip_give_the_ontario_credit_of_155_17() -> None:
    # The worked example of the Worksheet: eligible dividends received 1000 and dividends other
    # than eligible 500, no slips. Line 13 is 1380.00 and line 16 575.00, so line 12000 is
    # 1955.00 and line 12010 575.00. Ontario line B is 575.00 x 2.9863% = 17.171225, 17.17;
    # line C is 1955.00 - 575.00 = 1380.00 and line 2 is 1380.00 x 10% = 138.00; line 3 is
    # 17.17 + 138.00 = 155.17.
    worksheet = compute(
        "50000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        eligible_dividends_received_without_a_slip="1000",
        other_dividends_received_without_a_slip="500",
    )

    assert worksheet.get(TAXABLE_DIVIDENDS).value == D("1955.00")
    assert worksheet.get(TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE).value == D("575.00")
    assert worksheet.get(ontario.DIVIDENDS_AMOUNT_A).value == D("1955.00")
    assert worksheet.get(ontario.DIVIDENDS_AMOUNT_B).value == D("575.00")
    assert worksheet.get(ontario.OTHER_DIVIDENDS_CREDIT).value == D("17.17")
    assert worksheet.get(ontario.DIVIDENDS_AMOUNT_A_LESS_B).value == D("1380.00")
    assert worksheet.get(ontario.ELIGIBLE_DIVIDENDS_CREDIT).value == D("138.00")
    assert worksheet.get(ontario.DIVIDEND_TAX_CREDIT).value == D("155.17")
    assert worksheet.get(DIVIDEND_TAX_CREDIT).value == D("259.19")


def test_dividends_on_slips_alone_are_the_whole_ontario_lines_a_and_b() -> None:
    # Slip amounts of 800 (T5 boxes 11 and 25) and 300 (box 11) are lines 12000 and 12010, and
    # the Ontario worksheet reads both whole (the federal lines A and B are 0 here): line 1 is
    # 300 x 2.9863% = 8.9589, 8.96; line C is 800 - 300 = 500; line 2 is 500 x 10% = 50.00; line
    # 3 is 58.96.
    worksheet = compute(
        "50000",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        t5_taxable_dividends_other_than_eligible="300",
        t5_taxable_dividends="800",
        t5_dividend_tax_credit="70.00",
    )

    assert worksheet.get(DIVIDENDS_AMOUNT_A).value == D("0")
    assert worksheet.get(ontario.DIVIDENDS_AMOUNT_A).value == D("800")
    assert worksheet.get(ontario.DIVIDENDS_AMOUNT_B).value == D("300")
    assert worksheet.get(ontario.OTHER_DIVIDENDS_CREDIT).value == D("8.96")
    assert worksheet.get(ontario.DIVIDENDS_AMOUNT_A_LESS_B).value == D("500")
    assert worksheet.get(ontario.ELIGIBLE_DIVIDENDS_CREDIT).value == D("50.00")
    assert worksheet.get(ontario.DIVIDEND_TAX_CREDIT).value == D("58.96")


def test_slip_credits_alone_give_no_ontario_dividend_tax_credit() -> None:
    # The Ontario credit is computed from lines 12000 and 12010, not taken from the slips'
    # credit boxes: with no dividends the federal line 40425 is the slip credit of 100.00 and
    # ON428 line 57 is 0.
    worksheet = compute("50000", "0", "0", "0", "0", "0", "0", t5_dividend_tax_credit="100.00")

    assert worksheet.get(DIVIDEND_TAX_CREDIT).value == D("100.00")
    assert worksheet.get(ontario.DIVIDEND_TAX_CREDIT).value == D("0")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT).value == (
        worksheet.get(ONTARIO_TAX_WITH_SURTAX).value
    )


def test_the_dividend_credit_is_taken_off_line_69_after_the_surtax() -> None:
    # Line 70 comes off line 69, the tax plus the surtax (line 68), and the surtax is still
    # computed on line 65 before it: line 71 is line 69 less the credit.
    worksheet = compute("100000", "0", "0", "0", "0", "0", "0", t5_taxable_dividends="100000")

    credit = worksheet.get(ontario.DIVIDEND_TAX_CREDIT).value
    assert credit == D("10000.00")
    assert worksheet.get(ONTARIO_SURTAX).value > D("0")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT).value == (
        worksheet.get(ONTARIO_TAX_WITH_SURTAX).value - credit
    )


def test_the_ontario_tax_reduction_is_set_against_line_71_not_line_69() -> None:
    # Employment income of 26000 and a T5 slip with boxes 11 and 25 of 1000 (box 11 0): line 12000
    # is 1000 and line 12010 is 0, so line 1 is 0, line C is 1000.00 and line 2 is 100.00, line
    # 57 being 100.00. Line 69 is 630.64, above twice the reduction amounts, 588.00; line 71,
    # and so line 73, is 630.64 - 100.00 = 530.64, so line 80 "Line 78 minus line 79" is 588.00
    # - 530.64 = 57.36 and line 81 is 530.64 - 57.36 = 473.28.
    worksheet = compute("26000", "0", "0", "0", "0", "0", "0", t5_taxable_dividends="1000")

    assert worksheet.get(ontario.DIVIDEND_TAX_CREDIT).value == D("100.00")
    assert worksheet.get(ONTARIO_TAX_WITH_SURTAX).value == D("630.64")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT).value == D("530.64")
    assert worksheet.get(ONTARIO_TAX_REDUCTION).value == D("57.36")
    assert worksheet.get(ONTARIO_TAX_AFTER_REDUCTION).value == D("473.28")


def test_an_ontario_dividend_credit_above_the_tax_leaves_zero_not_a_negative() -> None:
    # Employment income of 20000 and slip dividends of 20000: the credit (line 57) is 2000.00,
    # above the Ontario tax of 1310.14, so lines 58 and 71 are "0" (if negative, enter "0").
    worksheet = compute("20000", "0", "0", "0", "0", "0", "0", t5_taxable_dividends="20000")

    assert worksheet.get(ontario.DIVIDEND_TAX_CREDIT).value == D("2000.00")
    assert worksheet.get(ontario.ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT).value == D("1310.14")
    assert worksheet.get(ontario.ONTARIO_TAX_LESS_DIVIDEND_CREDIT).value == D("0")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_DIVIDEND_CREDIT).value == D("0")


def return_q() -> Worksheet:
    """Return Q's inputs (`returns/2025_return_q.yaml`): Return I's and two infirm dependants."""
    return compute(
        "48000",
        "0",
        "0",
        "0",
        "8640",
        "0",
        "0",
        income_tax_deducted="4800",
        community_food_program_donations="1000",
        infirm_dependants=("5000", "25000"),
    )


def test_return_qs_two_infirm_dependants_are_claimed_one_by_one_on_line_30450() -> None:
    # Return Q is Return I (employment income of 48000, taxable income 47555.00, federal tax on
    # it 6895.48, Ontario tax 1684.56 after the LIFT and food credits and the health premium)
    # with two infirm dependants age 18 or older, of net incomes 5000 and 25000. Schedule 5 line
    # 30450, per dependant: 28798.00 - 5000 = 23798.00, at most 8601: 8601; 28798.00 - 25000 =
    # 3798.00; the total of the allowable amounts is 8601 + 3798.00 = 12399.00 (pooled, 28798.00
    # - 30000 would be negative and give 0). The amount for an eligible dependant is not claimed
    # for them (0 eligible dependants), the age, spouse and spouse caregiver amounts (lines 30100,
    # 30300 and 30425) are 0 from inputs at their no-claim values, and the Ontario caregiver
    # amount (ON428 line 58185) is computed from an empty list of dependants, 0. The federal
    # credit amounts are 16129 + 0 +
    # 0 + 0 + 0 + 12399.00 + 0 + 2202.75 + 787.20 + 1471 = 32988.95; 14.5% of it is
    # 4783.39775, rounded half-up to the cent: 4783.40, so the federal tax after credits is
    # 6895.48 - 4783.40 = 2112.08. The Ontario total of credit amounts is unchanged, 15736.95.
    # The total payable is 2112.08 + 1684.56 = 3796.64, and with the chosen tax deducted of 4800
    # and no Canada workers benefit, line 167 is 3796.64 - 4800 = -1003.36, a refund.
    worksheet = return_q()

    assert worksheet.get(INFIRM_DEPENDANTS).value == RecordList(
        INFIRM_DEPENDANTS.fields,
        [{DEPENDANT_NET_INCOME: D("5000")}, {DEPENDANT_NET_INCOME: D("25000")}],
    )
    assert worksheet.producer_of(INFIRM_DEPENDANTS) is None
    assert isinstance(worksheet.producer_of(CAREGIVER_AMOUNT), CaregiverAmount)
    assert worksheet.get(CAREGIVER_AMOUNT).value == D("12399.00")
    assert worksheet.get(ELIGIBLE_DEPENDANT_AMOUNT).value == D("0")
    assert worksheet.get(INFIRM_CHILDREN_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("32988.95")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("4783.40")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("2112.08")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("15736.95")
    assert worksheet.get(ONTARIO_TAX).value == D("1684.56")
    assert worksheet.get(TOTAL_PAYABLE).value == D("3796.64")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("0")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-1003.36")


def test_return_qs_trace_names_each_dependant_and_totals_the_credit_amounts() -> None:
    worksheet = return_q()

    lines = [
        line
        for line in worksheet.trace
        if isinstance(line, CaregiverClaimLine | ItemsTotalLine) and line.output == CAREGIVER_AMOUNT
    ]
    assert lines == [
        CaregiverClaimLine(
            output=CAREGIVER_AMOUNT,
            position=1,
            base=Amount(D("28798.00")),
            net_income=D("5000"),
            maximum=Amount(D("8601")),
            rounding=CENT,
            result=D("8601.00"),
        ),
        CaregiverClaimLine(
            output=CAREGIVER_AMOUNT,
            position=2,
            base=Amount(D("28798.00")),
            net_income=D("25000"),
            maximum=Amount(D("8601")),
            rounding=CENT,
            result=D("3798.00"),
        ),
        ItemsTotalLine(
            output=CAREGIVER_AMOUNT,
            items=((1, D("8601.00")), (2, D("3798.00"))),
            total=D("12399.00"),
        ),
    ]
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    first = rendered.index(
        "caregiver_amount: dependant 1: 28798 less net income 5000, at most 8601 = 8601 "
        "(half-up to 0.01)"
    )
    assert rendered[first : first + 3] == (
        "caregiver_amount: dependant 1: 28798 less net income 5000, at most 8601 = 8601 "
        "(half-up to 0.01)",
        "caregiver_amount: dependant 2: 28798 less net income 25000, at most 8601 = 3798 "
        "(half-up to 0.01)",
        "caregiver_amount: item 1 8601 + item 2 3798 = 12399",
    )
    assert (
        "non_refundable_credit_amounts: basic_personal_amount 16129 + age_amount 0 "
        "+ spouse_amount 0 + eligible_dependant_amount 0 + spouse_caregiver_amount 0 "
        "+ caregiver_amount 12399 + infirm_children_amount 0 + cpp_base_contributions 2202.75 "
        "+ ei_premiums 787.2 + canada_employment_amount 1471 + disability_transferred_amount 0 "
        "+ medical_claim 0 "
        "= 32988.95"
    ) in rendered


def test_infirm_dependants_pooled_would_give_the_wrong_line_30450() -> None:
    separate = compute(
        "48000", "0", "0", "0", "8640", "0", "0", infirm_dependants=("5000", "25000")
    )
    pooled = compute("48000", "0", "0", "0", "8640", "0", "0", infirm_dependants=("30000",))

    assert separate.get(CAREGIVER_AMOUNT).value == D("12399.00")
    assert pooled.get(CAREGIVER_AMOUNT).value == D("0")


def test_no_infirm_dependants_claim_nothing_on_line_30450() -> None:
    worksheet = compute("48000", "0", "0", "0", "8640", "0", "0")

    assert worksheet.get(CAREGIVER_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("20589.95")


def test_infirm_dependants_do_not_change_the_ontario_credits() -> None:
    # ON428 line 58185 (the Ontario caregiver amount) is computed from an empty list here: 0.
    without = compute("48000", "0", "0", "0", "8640", "0", "0")
    with_dependants = return_q()

    assert with_dependants.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS) == (
        without.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS)
    )


def return_x() -> Worksheet:
    """Return X's inputs (`returns/2025_return_x.yaml`): Return I's, own medical expenses and two
    other dependants."""
    return compute(
        "48000",
        "0",
        "0",
        "0",
        "8640",
        "0",
        "0",
        income_tax_deducted="4800",
        community_food_program_donations="1000",
        medical_expenses="4500",
        other_dependants=(("3000", "10000"), ("1000", "40000")),
    )


def test_return_xs_medical_expenses_are_claimed_on_lines_33099_and_33199() -> None:
    # Return X is Return I (employment income of 48000, net income 47555.00, taxable income
    # 47555.00, federal tax on it 6895.48) with medical expenses of 4500 for
    # the filer (a chosen figure, T1 line 107, line 33099) and two other dependants (a chosen
    # figure) with expenses 3000 and net income 10000, and expenses 1000 and net income 40000.
    # Line 108 is 3% of 47555.00 = 1426.65; line 109 is the lesser of 2834 and 1426.65 = 1426.65;
    # line 110 is 4500 - 1426.65 = 3073.35. Line 33199, per dependant: 3000 - lesser(300.00,
    # 2834) = 2700.00; 1000 - lesser(1200.00, 2834) is negative, so 0; the total, line 111, is
    # 2700.00 (pooled, 4000 - lesser(1500.00, 2834) = 2500.00 is the wrong figure). Line 112
    # (line 33200) is 3073.35 + 2700.00 = 5773.35. The federal credit amounts are 16129 + 0 + 0 +
    # 0 + 0 + 0 + 0 + 2202.75 + 787.20 + 1471 = 20589.95, plus 5773.35 = 26363.30; 14.5% of it is
    # 3822.6785, rounded half-up to the cent: 3822.68, so the federal tax after credits is
    # 6895.48 - 3822.68 = 3072.80. ON428 has the same lines: line 39 is 3% of 47555.00 =
    # 1426.65; line 40 is the lesser of 2885 and 1426.65 = 1426.65; line 41 is 4500 - 1426.65 =
    # 3073.35. Line 58729, per dependant: 3000 - lesser(300.00, 2885) = 2700.00; 1000 -
    # lesser(1200.00, 2885) is negative, so 0, neither near the maximum of 15551; the total,
    # line 42, is 2700.00. Line 43 (line 58769) is 3073.35 + 2700.00 = 5773.35. The Ontario total
    # of credit amounts (line 58800) is 12747 + 0 + 0 + 0 + 2202.75 + 787.20 + 5773.35 =
    # 21510.30; 5.05% of it is 1086.27015, rounded half-up to the cent: 1086.27, so the Ontario
    # tax after credits is 2401.53 - 1086.27 = 1315.26, below the surtax thresholds. The tax
    # reduction is 0 (twice 294.00 is less than the tax), the LIFT credit is 122.25 and the food
    # credit 250.00: 1315.26 - 122.25 - 250.00 = 943.01, and with the health premium of 450, the
    # Ontario tax is 1393.01. The total payable is 3072.80 + 1393.01 = 4465.81, and with the
    # chosen tax deducted of 4800 and no Canada workers benefit, line 167 is 4465.81 - 4800 =
    # -334.19, a refund.
    worksheet = return_x()

    assert worksheet.get(MEDICAL_EXPENSES).value == D("4500")
    assert worksheet.producer_of(MEDICAL_EXPENSES) is None
    assert worksheet.producer_of(OTHER_DEPENDANTS) is None
    assert worksheet.get(OTHER_DEPENDANTS).value == RecordList(
        OTHER_DEPENDANTS.fields,
        [
            {OTHER_DEPENDANT_MEDICAL_EXPENSES: D("3000"), DEPENDANT_NET_INCOME: D("10000")},
            {OTHER_DEPENDANT_MEDICAL_EXPENSES: D("1000"), DEPENDANT_NET_INCOME: D("40000")},
        ],
    )
    assert worksheet.get(NET_INCOME).value == D("47555.00")
    assert worksheet.get(MEDICAL_NET_INCOME_SHARE).value == D("1426.65")
    assert worksheet.get(MEDICAL_THRESHOLD).value == D("1426.65")
    assert worksheet.get(MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("3073.35")
    assert worksheet.get(OTHER_DEPENDANTS_MEDICAL).value == D("2700.00")
    assert worksheet.get(MEDICAL_CLAIM).value == D("5773.35")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("26363.30")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("3822.68")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("3072.80")
    assert worksheet.producer_of(ontario.MEDICAL_NET_INCOME_SHARE) is not None
    assert worksheet.get(ontario.MEDICAL_NET_INCOME_SHARE).value == D("1426.65")
    assert worksheet.get(ontario.MEDICAL_THRESHOLD).value == D("1426.65")
    assert worksheet.get(ontario.MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("3073.35")
    assert worksheet.get(ontario.OTHER_DEPENDANTS_MEDICAL).value == D("2700.00")
    assert worksheet.get(ontario.MEDICAL_CLAIM).value == D("5773.35")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("21510.30")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("1086.27")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("1315.26")
    assert worksheet.get(ONTARIO_TAX).value == D("1393.01")
    assert worksheet.get(TOTAL_PAYABLE).value == D("4465.81")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("0")
    # T1 line 154 (line 45200): line 16 of the Federal Worksheet, 25% of the medical claim of
    # 5773.35 (1443.34) less 5% of the net income of 47555.00 over 33294.00 (713.05).
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_11).value == D("5773.35")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_13).value == D("1443.34")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_14).value == D("1443.34")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_15).value == D("713.05")
    assert worksheet.get(REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT).value == D("730.29")
    assert worksheet.get(TOTAL_CREDITS).value == D("5530.29")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-1064.48")


def test_return_xs_trace_names_each_step_and_each_dependant() -> None:
    worksheet = return_x()

    lines = [
        line
        for line in worksheet.trace
        if isinstance(line, OtherDependantMedicalLine | ItemsTotalLine)
        and line.output == OTHER_DEPENDANTS_MEDICAL
    ]
    assert lines == [
        OtherDependantMedicalLine(
            output=OTHER_DEPENDANTS_MEDICAL,
            position=1,
            expenses=D("3000"),
            net_income=D("10000"),
            reduction=ClaimReduction(Rate(D("0.03")), D("2834")),
            rounding=CENT,
            result=D("2700.00"),
        ),
        OtherDependantMedicalLine(
            output=OTHER_DEPENDANTS_MEDICAL,
            position=2,
            expenses=D("1000"),
            net_income=D("40000"),
            reduction=ClaimReduction(Rate(D("0.03")), D("2834")),
            rounding=CENT,
            result=D("0"),
        ),
        ItemsTotalLine(
            output=OTHER_DEPENDANTS_MEDICAL,
            items=((1, D("2700.00")), (2, D("0"))),
            total=D("2700.00"),
        ),
    ]
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    first = rendered.index(
        "other_dependants_medical: dependant 1: expenses 3000 less the lesser of 3% of net income "
        "10000 and 2834 = 2700 (half-up to 0.01)"
    )
    assert rendered[first : first + 3] == (
        "other_dependants_medical: dependant 1: expenses 3000 less the lesser of 3% of net income "
        "10000 and 2834 = 2700 (half-up to 0.01)",
        "other_dependants_medical: dependant 2: expenses 1000 less the lesser of 3% of net income "
        "40000 and 2834 = 0 (half-up to 0.01)",
        "other_dependants_medical: item 1 2700 + item 2 0 = 2700",
    )
    for sentence in (
        "medical_net_income_share: 3% of net_income 47555 (half-up to 0.01)",
        "medical_threshold: lesser of medical_net_income_share 1426.65 and 2834 (half-up to 0.01)",
        "medical_expenses_over_threshold: medical_expenses 4500 less medical_threshold 1426.65, "
        "not below 0 = 3073.35",
        "medical_claim: medical_expenses_over_threshold 3073.35 + other_dependants_medical 2700 "
        "= 5773.35",
        "non_refundable_credit_amounts: basic_personal_amount 16129 + age_amount 0 "
        "+ spouse_amount 0 + eligible_dependant_amount 0 + spouse_caregiver_amount 0 "
        "+ caregiver_amount 0 + infirm_children_amount 0 + cpp_base_contributions 2202.75 "
        "+ ei_premiums 787.2 + canada_employment_amount 1471 + disability_transferred_amount 0 "
        "+ medical_claim 5773.35 = 26363.3",
    ):
        assert sentence in rendered


def test_other_dependants_pooled_would_give_the_wrong_line_33199() -> None:
    separate = compute(
        "48000",
        "0",
        "0",
        "0",
        "8640",
        "0",
        "0",
        other_dependants=(("3000", "10000"), ("1000", "40000")),
    )
    pooled = compute(
        "48000", "0", "0", "0", "8640", "0", "0", other_dependants=(("4000", "50000"),)
    )

    assert separate.get(OTHER_DEPENDANTS_MEDICAL).value == D("2700.00")
    # 4000 - lesser(1500.00, 2834) = 2500.00, not 2700.00.
    assert pooled.get(OTHER_DEPENDANTS_MEDICAL).value == D("2500.00")


def test_no_medical_expenses_claim_nothing_on_line_33200() -> None:
    worksheet = compute("48000", "0", "0", "0", "8640", "0", "0")

    assert worksheet.get(MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("0")
    assert worksheet.get(OTHER_DEPENDANTS_MEDICAL).value == D("0")
    assert worksheet.get(MEDICAL_CLAIM).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("20589.95")


def test_medical_expenses_below_the_threshold_claim_nothing_on_line_33099() -> None:
    # 3% of 47555.00 is 1426.65: expenses of 1426.65 or less give line 110 of 0.
    at = compute("48000", "0", "0", "0", "8640", "0", "0", medical_expenses="1426.65")
    over = compute("48000", "0", "0", "0", "8640", "0", "0", medical_expenses="1426.66")

    assert at.get(MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("0")
    assert over.get(MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("0.01")


def test_the_threshold_on_line_109_stops_at_2834() -> None:
    # 3% of a net income above 94466.67 is above the 2834 ceiling, so expenses of 5000 leave
    # 5000 - 2834 = 2166 on line 110.
    worksheet = compute("115000", "0", "0", "0", "0", "0", "0", medical_expenses="5000")

    assert worksheet.get(MEDICAL_NET_INCOME_SHARE).value > D("2834")
    assert worksheet.get(MEDICAL_THRESHOLD).value == D("2834")
    assert worksheet.get(MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("2166")


def test_return_xs_ontario_trace_names_each_step_and_each_dependant() -> None:
    worksheet = return_x()

    lines = [
        line
        for line in worksheet.trace
        if isinstance(line, OtherDependantMedicalLine | ItemsTotalLine)
        and line.output == ontario.OTHER_DEPENDANTS_MEDICAL
    ]
    reduction = ClaimReduction(Rate(D("0.03")), D("2885"), D("15551"))
    assert lines == [
        OtherDependantMedicalLine(
            output=ontario.OTHER_DEPENDANTS_MEDICAL,
            position=1,
            expenses=D("3000"),
            net_income=D("10000"),
            reduction=reduction,
            rounding=CENT,
            result=D("2700.00"),
        ),
        OtherDependantMedicalLine(
            output=ontario.OTHER_DEPENDANTS_MEDICAL,
            position=2,
            expenses=D("1000"),
            net_income=D("40000"),
            reduction=reduction,
            rounding=CENT,
            result=D("0"),
        ),
        ItemsTotalLine(
            output=ontario.OTHER_DEPENDANTS_MEDICAL,
            items=((1, D("2700.00")), (2, D("0"))),
            total=D("2700.00"),
        ),
    ]
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    first = rendered.index(
        "other_dependants_medical: dependant 1: expenses 3000 less the lesser of 3% of net income "
        "10000 and 2885 = 2700, at most 15551 (half-up to 0.01)"
    )
    assert rendered[first : first + 3] == (
        "other_dependants_medical: dependant 1: expenses 3000 less the lesser of 3% of net income "
        "10000 and 2885 = 2700, at most 15551 (half-up to 0.01)",
        "other_dependants_medical: dependant 2: expenses 1000 less the lesser of 3% of net income "
        "40000 and 2885 = 0, at most 15551 (half-up to 0.01)",
        "other_dependants_medical: item 1 2700 + item 2 0 = 2700",
    )
    for sentence in (
        "medical_threshold: lesser of medical_net_income_share 1426.65 and 2885 (half-up to 0.01)",
        "medical_expenses_over_threshold: medical_expenses 4500 less medical_threshold 1426.65, "
        "not below 0 = 3073.35",
        "non_refundable_credit_amounts: basic_personal_amount 12747 + age_amount 0 "
        "+ spouse_amount 0 + eligible_dependant_amount 0 + caregiver_amount 0 "
        "+ cpp_base_contributions 2202.75 + ei_premiums 787.2 + medical_claim 5773.35 = 21510.3",
        "credit_amounts_at_credit_rate: 5.05% of non_refundable_credit_amounts 21510.3 "
        "(half-up to 0.01)",
    ):
        assert sentence in rendered


def test_ontario_shares_the_filers_expenses_and_the_dependants_with_the_t1() -> None:
    worksheet = return_x()

    assert worksheet.producer_of(ontario.MEDICAL_CLAIM) is not worksheet.producer_of(MEDICAL_CLAIM)
    ontario_dependants = worksheet.producer_of(ontario.OTHER_DEPENDANTS_MEDICAL)
    assert isinstance(ontario_dependants, OtherDependantsMedical)
    assert ontario_dependants.consumes == frozenset({OTHER_DEPENDANTS})
    assert worksheet.producer_of(MEDICAL_EXPENSES) is None
    assert worksheet.get(ontario.MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("3073.35")


def test_ontario_medical_expenses_change_only_the_ontario_credits_by_the_claim() -> None:
    without = compute("48000", "0", "0", "0", "8640", "0", "0")
    with_medical = return_x()

    assert without.get(ontario.MEDICAL_CLAIM).value == D("0")
    assert with_medical.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == (
        without.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value + D("5773.35")
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
    return compute("48000", "0", "0", "0", "8640", "0", "0", **{**given, **overrides})


def test_return_ws_two_ontario_caregiver_dependants_are_claimed_one_by_one_on_line_58185() -> None:
    # Return W is Return Q (employment income of 48000, taxable income 47555.00, the Ontario tax
    # on it 2401.53) with two dependants for the Ontario caregiver amount, of net incomes 5000
    # and 25000, neither claimed on line 58160. Worksheet ON428 line 58185, per dependant:
    # 26562.00 - 5000 = 21562.00, at most 6008: 6008; 26562.00 - 25000 = 1562.00; line 4 is 0 for
    # both, so line 5 is line 3 and the total is 6008 + 1562.00 = 7570.00 (pooled, 26562.00 -
    # 30000 would be negative and give 0). ON428 line 58800 is 12747 + 0 + 0 + 0 + 7570.00 +
    # 2202.75 + 787.20 = 23306.95; 5.05% of it is 1177.000975, rounded half-up to the cent:
    # 1177.00, so the Ontario tax after credits is 2401.53 - 1177.00 = 1224.53, with no surtax
    # and no tax reduction (588.00 less 1224.53 is negative). After the LIFT credit of 122.25
    # that is 1102.28, after the food credit of 250.00 it is 852.28, and with the health premium
    # of 450 the Ontario tax is 1302.28. The federal side is Return Q's: the tax after credits
    # is 2112.08, the total payable 2112.08 + 1302.28 = 3414.36 and, with the chosen tax
    # deducted of 4800 and no Canada workers benefit, line 167 is 3414.36 - 4800 = -1385.64, a
    # refund.
    worksheet = return_w()

    assert worksheet.get(ontario.CAREGIVER_DEPENDANTS).value == RecordList(
        ontario.CAREGIVER_DEPENDANTS.fields,
        [
            {DEPENDANT_NET_INCOME: D("5000"), ontario.CLAIMED_AS_ELIGIBLE_DEPENDANT: 0},
            {DEPENDANT_NET_INCOME: D("25000"), ontario.CLAIMED_AS_ELIGIBLE_DEPENDANT: 0},
        ],
    )
    assert worksheet.producer_of(ontario.CAREGIVER_DEPENDANTS) is None
    assert isinstance(worksheet.producer_of(ontario.CAREGIVER_AMOUNT), OntarioCaregiverAmount)
    assert worksheet.get(ontario.CAREGIVER_AMOUNT).value == D("7570.00")
    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("0")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("23306.95")
    assert worksheet.get(ontario.NON_REFUNDABLE_TAX_CREDITS).value == D("1177.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("1224.53")
    assert worksheet.get(ontario.ONTARIO_SURTAX).value == D("0")
    assert worksheet.get(ontario.ONTARIO_TAX_REDUCTION).value == D("0")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_LIFT_CREDIT).value == D("1102.28")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_FOOD_CREDIT).value == D("852.28")
    assert worksheet.get(ONTARIO_TAX).value == D("1302.28")
    assert worksheet.get(CAREGIVER_AMOUNT).value == D("12399.00")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("32988.95")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("2112.08")
    assert worksheet.get(TOTAL_PAYABLE).value == D("3414.36")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("0")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-1385.64")


def test_return_ws_trace_names_each_ontario_dependant_and_totals_the_credit_amounts() -> None:
    worksheet = return_w()

    lines = [
        line
        for line in worksheet.trace
        if isinstance(line, CaregiverClaimLessClaimedLine | ItemsTotalLine)
        and line.output == ontario.CAREGIVER_AMOUNT
    ]
    assert lines == [
        CaregiverClaimLessClaimedLine(
            output=ontario.CAREGIVER_AMOUNT,
            position=1,
            base=Amount(D("26562.00")),
            net_income=D("5000"),
            maximum=Amount(D("6008")),
            allowable_before_claimed=D("6008.00"),
            claimed=D("0"),
            rounding=CENT,
            result=D("6008.00"),
        ),
        CaregiverClaimLessClaimedLine(
            output=ontario.CAREGIVER_AMOUNT,
            position=2,
            base=Amount(D("26562.00")),
            net_income=D("25000"),
            maximum=Amount(D("6008")),
            allowable_before_claimed=D("1562.00"),
            claimed=D("0"),
            rounding=CENT,
            result=D("1562.00"),
        ),
        ItemsTotalLine(
            output=ontario.CAREGIVER_AMOUNT,
            items=((1, D("6008.00")), (2, D("1562.00"))),
            total=D("7570.00"),
        ),
    ]
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    first = rendered.index(
        "caregiver_amount: dependant 1: 26562 less net income 5000, at most 6008 = 6008, "
        "less claimed 0 = 6008 (half-up to 0.01)"
    )
    assert rendered[first : first + 3] == (
        "caregiver_amount: dependant 1: 26562 less net income 5000, at most 6008 = 6008, "
        "less claimed 0 = 6008 (half-up to 0.01)",
        "caregiver_amount: dependant 2: 26562 less net income 25000, at most 6008 = 1562, "
        "less claimed 0 = 1562 (half-up to 0.01)",
        "caregiver_amount: item 1 6008 + item 2 1562 = 7570",
    )
    assert (
        "non_refundable_credit_amounts: basic_personal_amount 12747 + age_amount 0 "
        "+ spouse_amount 0 + eligible_dependant_amount 0 + caregiver_amount 7570 "
        "+ cpp_base_contributions 2202.75 + ei_premiums 787.2 + medical_claim 0 = 23306.95"
    ) in rendered


def test_the_ontario_dependants_pooled_would_give_the_wrong_line_58185() -> None:
    separate = return_w()
    pooled = return_w(caregiver_dependants=(("30000", 0),))

    assert separate.get(ontario.CAREGIVER_AMOUNT).value == D("7570.00")
    assert pooled.get(ontario.CAREGIVER_AMOUNT).value == D("0")


def test_no_ontario_caregiver_dependants_claim_nothing_on_line_58185() -> None:
    worksheet = return_w(caregiver_dependants=())

    assert worksheet.get(ontario.CAREGIVER_AMOUNT).value == D("0")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("15736.95")
    assert worksheet.get(CAREGIVER_AMOUNT).value == D("12399.00")


def test_the_ontario_caregiver_dependants_are_a_list_of_their_own() -> None:
    # The list of line 30450 (Schedule 5) and that of line 58185 are separate inputs: the Ontario
    # amount may be claimed for the line 30400 dependant too, which line 30450 excludes.
    only_ontario = return_w(infirm_dependants=())
    only_federal = return_w(caregiver_dependants=())

    assert only_ontario.get(CAREGIVER_AMOUNT).value == D("0")
    assert only_ontario.get(ontario.CAREGIVER_AMOUNT).value == D("7570.00")
    assert only_federal.get(CAREGIVER_AMOUNT).value == D("12399.00")
    assert only_federal.get(ontario.CAREGIVER_AMOUNT).value == D("0")


def test_the_dependant_claimed_on_line_58160_takes_it_off_line_58185() -> None:
    # Return W with an eligible dependant of net income 9000, claimed on ON428 line 58160 (and on
    # line 30400): line 58160 is 11905.00 - 9000 = 2905.00, at most 10823, for 1 eligible
    # dependant. That dependant is also listed for the Ontario caregiver amount, flagged: line 3
    # is 26562.00 - 9000 = 17562.00, at most 6008: 6008; line 4 is the 2905.00 of line 58160;
    # line 5 is 6008 - 2905.00 = 3103.00. The other dependant (net income 25000, unflagged) has
    # line 3 of 1562.00 and a line 4 of 0: 1562.00. Line 58185 is 3103.00 + 1562.00 = 4665.00,
    # and ON428 line 58800 is 12747 + 0 + 0 + 2905.00 + 4665.00 + 2202.75 + 787.20 = 23306.95,
    # the same total as without the eligible dependant (2905.00 + 4665.00 = 7570.00): what line
    # 58160 claims, line 58185 does not claim again.
    worksheet = return_w(
        eligible_dependants=1,
        dependant_net_income="9000",
        infirm_dependants=("25000",),
        caregiver_dependants=(("9000", 1), ("25000", 0)),
    )

    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("2905.00")
    assert worksheet.get(ontario.CAREGIVER_AMOUNT).value == D("4665.00")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("23306.95")
    lines = [
        line
        for line in worksheet.trace
        if isinstance(line, CaregiverClaimLessClaimedLine | ItemsTotalLine)
        and line.output == ontario.CAREGIVER_AMOUNT
    ]
    assert lines == [
        CaregiverClaimLessClaimedLine(
            output=ontario.CAREGIVER_AMOUNT,
            position=1,
            base=Amount(D("26562.00")),
            net_income=D("9000"),
            maximum=Amount(D("6008")),
            allowable_before_claimed=D("6008.00"),
            claimed=D("2905.00"),
            rounding=CENT,
            result=D("3103.00"),
        ),
        CaregiverClaimLessClaimedLine(
            output=ontario.CAREGIVER_AMOUNT,
            position=2,
            base=Amount(D("26562.00")),
            net_income=D("25000"),
            maximum=Amount(D("6008")),
            allowable_before_claimed=D("1562.00"),
            claimed=D("0"),
            rounding=CENT,
            result=D("1562.00"),
        ),
        ItemsTotalLine(
            output=ontario.CAREGIVER_AMOUNT,
            items=((1, D("3103.00")), (2, D("1562.00"))),
            total=D("4665.00"),
        ),
    ]
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "caregiver_amount: dependant 1: 26562 less net income 9000, at most 6008 = 6008, "
        "less claimed 2905 = 3103 (half-up to 0.01)"
    ) in rendered
    assert (
        "non_refundable_credit_amounts: basic_personal_amount 12747 + age_amount 0 "
        "+ spouse_amount 0 + eligible_dependant_amount 2905 + caregiver_amount 4665 "
        "+ cpp_base_contributions 2202.75 + ei_premiums 787.2 + medical_claim 0 = 23306.95"
    ) in rendered


def test_a_line_58160_amount_above_line_3_leaves_line_5_at_zero_not_a_negative() -> None:
    # An eligible dependant with no net income claims 11905.00 - 0, at most 10823 on line 58160.
    # Flagged on the worksheet, its line 3 is 6008 and its line 4 10823, so line 3 minus line 4 is
    # negative and line 5 is "0"; the other dependant keeps its 1562.00. Line 58185 is 1562.00,
    # not 6008 + 1562.00 - 10823 (negative), and ON428 line 58800 is 12747 + 0 + 0 + 10823 +
    # 1562.00 + 2202.75 + 787.20 = 28121.95.
    worksheet = return_w(
        eligible_dependants=1,
        dependant_net_income="0",
        infirm_dependants=("25000",),
        caregiver_dependants=(("0", 1), ("25000", 0)),
    )

    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("10823")
    claim_lines = [
        line
        for line in worksheet.trace
        if isinstance(line, CaregiverClaimLessClaimedLine)
        and line.output == ontario.CAREGIVER_AMOUNT
    ]
    assert [(line.allowable_before_claimed, line.claimed, line.result) for line in claim_lines] == [
        (D("6008.00"), D("10823"), D("0")),
        (D("1562.00"), D("0"), D("1562.00")),
    ]
    assert not claim_lines[0].result.is_signed()
    assert worksheet.get(ontario.CAREGIVER_AMOUNT).value == D("1562.00")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("28121.95")


def test_an_unflagged_dependant_takes_nothing_off_line_58185_whatever_line_58160_is() -> None:
    worksheet = return_w(
        eligible_dependants=1,
        dependant_net_income="9000",
        infirm_dependants=("25000",),
        caregiver_dependants=(("5000", 0), ("25000", 0)),
    )

    assert worksheet.get(ontario.ELIGIBLE_DEPENDANT_AMOUNT).value == D("2905.00")
    assert worksheet.get(ontario.CAREGIVER_AMOUNT).value == D("7570.00")


def return_ab(**overrides: Any) -> Worksheet:
    """Return AB's inputs (`returns/2025_return_ab.yaml`): Return W's and a dependant aged 20.

    `overrides` replace any keyword of `return_w`, for the variants below.
    """
    given: dict[str, Any] = {"disability_dependants": ((0, "0", "16129", "20000"),)}
    return return_w(**{**given, **overrides})


def test_return_abs_dependant_with_a_disability_transfers_6267_on_line_31800() -> None:
    # Return AB is Return W (employment income of 48000, taxable income 47555.00, federal tax on
    # it 6895.48, the Ontario figures of Return W, the Canada caregiver amount for two infirm
    # dependants 12399.00) with one dependant with a disability, aged 20 (so worksheet line 7 is
    # "0"), no care expenses, line 98 of their return 16129 and their taxable income 20000, all
    # chosen figures. Federal Worksheet line 31800: line 8 = 10138.00 + 0; line 10 = 10138.00 +
    # 16129 = 26267.00; line 12 = 26267.00 - 20000 = 6267.00; line 13 = lesser(10138.00,
    # 6267.00) = 6267.00, the total of the allowable amounts. The federal credit amounts are
    # 16129 + 0 + 0 + 0 + 0 + 12399.00 + 0 + 2202.75 + 787.20 + 1471 + 6267.00 = 39255.95; 14.5%
    # of it is 5692.11275, rounded half-up to the cent: 5692.11, so the federal tax after
    # credits is 6895.48 - 5692.11 = 1203.37. The Ontario total of credit amounts is Return W's,
    # 23306.95 (the Ontario disability amount, ON428 line 58480, is not yet computed), so the
    # Ontario tax is 1302.28. The total payable is 1203.37 + 1302.28 = 2505.65, and with the
    # chosen tax deducted of 4800 and no Canada workers benefit, line 167 is 2505.65 - 4800 =
    # -2294.35, a refund.
    worksheet = return_ab()

    assert worksheet.get(DISABILITY_DEPENDANTS).value == RecordList(
        DISABILITY_DEPENDANTS.fields,
        [
            {
                DEPENDANT_UNDER_18: 0,
                DEPENDANT_CARE_EXPENSES: D("0"),
                DEPENDANT_CREDIT_AMOUNTS: D("16129"),
                DEPENDANT_TAXABLE_INCOME: D("20000"),
            }
        ],
    )
    assert worksheet.producer_of(DISABILITY_DEPENDANTS) is None
    assert isinstance(
        worksheet.producer_of(DISABILITY_TRANSFERRED_AMOUNT), DisabilityTransferAmount
    )
    assert worksheet.get(DISABILITY_TRANSFERRED_AMOUNT).value == D("6267.00")
    assert worksheet.get(CAREGIVER_AMOUNT).value == D("12399.00")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("39255.95")
    assert worksheet.get(NON_REFUNDABLE_TAX_CREDITS).value == D("5692.11")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("1203.37")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("23306.95")
    assert worksheet.get(ONTARIO_TAX).value == D("1302.28")
    assert worksheet.get(TOTAL_PAYABLE).value == D("2505.65")
    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("0")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-2294.35")


def test_return_abs_trace_names_the_dependant_and_totals_the_credit_amounts() -> None:
    worksheet = return_ab()

    lines = [
        line
        for line in worksheet.trace
        if isinstance(line, DisabilityTransferLine | ItemsTotalLine)
        and line.output == DISABILITY_TRANSFERRED_AMOUNT
    ]
    assert lines == [
        DisabilityTransferLine(
            output=DISABILITY_TRANSFERRED_AMOUNT,
            position=1,
            base=Amount(D("10138.00")),
            supplement=Amount(D("5914.00")),
            threshold=Amount(D("3464.00")),
            maximum=Amount(D("16052")),
            under_18=0,
            care_expenses=D("0"),
            line_5=D("0"),
            line_6=D("5914.00"),
            line_7=D("0"),
            line_8=D("10138.00"),
            credit_amounts=D("16129"),
            line_10=D("26267.00"),
            taxable_income=D("20000"),
            line_12=D("6267.00"),
            rounding=CENT,
            result=D("6267.00"),
        ),
        ItemsTotalLine(
            output=DISABILITY_TRANSFERRED_AMOUNT,
            items=((1, D("6267.00")),),
            total=D("6267.00"),
        ),
    ]
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    first = rendered.index(
        "disability_transferred_amount: dependant 1: 18 or older: base 10138 + 0, at most 16052 "
        "= 10138; 10138 + credit amounts 16129 less taxable income 20000 = 6267; "
        "the lesser of 10138 and 6267 = 6267 (half-up to 0.01)"
    )
    assert rendered[first : first + 2] == (
        "disability_transferred_amount: dependant 1: 18 or older: base 10138 + 0, at most 16052 "
        "= 10138; 10138 + credit amounts 16129 less taxable income 20000 = 6267; "
        "the lesser of 10138 and 6267 = 6267 (half-up to 0.01)",
        "disability_transferred_amount: item 1 6267 = 6267",
    )
    assert (
        "non_refundable_credit_amounts: basic_personal_amount 16129 + age_amount 0 "
        "+ spouse_amount 0 + eligible_dependant_amount 0 + spouse_caregiver_amount 0 "
        "+ caregiver_amount 12399 + infirm_children_amount 0 + cpp_base_contributions 2202.75 "
        "+ ei_premiums 787.2 + canada_employment_amount 1471 + disability_transferred_amount 6267 "
        "+ medical_claim 0 "
        "= 39255.95"
    ) in rendered


def test_a_dependant_under_18_with_care_expenses_transfers_the_reduced_supplement() -> None:
    # Care expenses of 5000: line 5 = 5000 - 3464.00 = 1536.00; line 6 = 5914.00 - 1536.00 =
    # 4378.00; line 7 = line 6; line 8 = 10138.00 + 4378.00 = 14516.00; with no credit amounts
    # and no taxable income line 12 = 14516.00, and line 13 is 14516.00.
    worksheet = compute(
        "48000", "0", "0", "0", "8640", "0", "0", disability_dependants=((1, "5000", "0", "0"),)
    )

    assert worksheet.get(DISABILITY_TRANSFERRED_AMOUNT).value == D("14516.00")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("35105.95")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "disability_transferred_amount: dependant 1: under 18: care expenses 5000 less threshold "
        "3464 = 1536; supplement 5914 less 1536 = 4378; base 10138 + 4378, at most 16052 = 14516; "
        "14516 + credit amounts 0 less taxable income 0 = 14516; "
        "the lesser of 14516 and 14516 = 14516 (half-up to 0.01)"
    ) in rendered


def test_two_dependants_with_a_disability_are_transferred_one_by_one_on_line_31800() -> None:
    worksheet = compute(
        "48000",
        "0",
        "0",
        "0",
        "8640",
        "0",
        "0",
        disability_dependants=((0, "0", "16129", "20000"), (1, "5000", "0", "0")),
    )

    # 6267.00 + 14516.00 = 20783.00.
    assert worksheet.get(DISABILITY_TRANSFERRED_AMOUNT).value == D("20783.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert "disability_transferred_amount: item 1 6267 + item 2 14516 = 20783" in rendered


def test_a_dependants_taxable_income_above_their_credits_transfers_nothing() -> None:
    # Line 10 = 10138.00 + 0; line 12 = 10138.00 - 20000 is negative, "0".
    worksheet = compute(
        "48000", "0", "0", "0", "8640", "0", "0", disability_dependants=((0, "0", "0", "20000"),)
    )

    assert worksheet.get(DISABILITY_TRANSFERRED_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("20589.95")


def test_no_dependants_with_a_disability_transfer_nothing_on_line_31800() -> None:
    worksheet = compute("48000", "0", "0", "0", "8640", "0", "0")

    assert worksheet.get(DISABILITY_TRANSFERRED_AMOUNT).value == D("0")
    assert worksheet.get(NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("20589.95")


def test_dependants_with_a_disability_do_not_change_the_ontario_credits() -> None:
    # ON428 line 58480 (the Ontario disability amount transferred from a dependant) is not yet
    # computed.
    without = return_w()
    with_dependants = return_ab()

    assert with_dependants.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS) == (
        without.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS)
    )
    assert with_dependants.get(ONTARIO_TAX) == without.get(ONTARIO_TAX)


def test_ontarios_ceiling_is_2885_not_the_federal_2834() -> None:
    # Employment income of 96000 gives a net income of 94926.00, and 3% of it is 2847.78: above
    # the federal ceiling of 2834 and below Ontario's 2885, so line 109 is 2834 and ON428 line
    # 40 is 2847.78.
    worksheet = compute("96000", "0", "0", "0", "0", "0", "0", medical_expenses="5000")

    assert worksheet.get(NET_INCOME).value == D("94926.00")
    assert worksheet.get(MEDICAL_THRESHOLD).value == D("2834")
    assert worksheet.get(ontario.MEDICAL_THRESHOLD).value == D("2847.78")
    assert worksheet.get(MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("2166")
    assert worksheet.get(ontario.MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("2152.22")


def test_ontarios_threshold_on_line_40_stops_at_2885() -> None:
    worksheet = compute("115000", "0", "0", "0", "0", "0", "0", medical_expenses="5000")

    assert worksheet.get(ontario.MEDICAL_NET_INCOME_SHARE).value > D("2885")
    assert worksheet.get(ontario.MEDICAL_THRESHOLD).value == D("2885")
    assert worksheet.get(ontario.MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("2115")


def test_ontario_caps_each_dependants_claim_at_15551_and_the_t1_does_not() -> None:
    # A dependant with no net income and expenses of 20000: the Federal Worksheet's line 3 is the
    # whole 20000, Worksheet ON428's line 3 is at most 15551.
    worksheet = compute(
        "48000", "0", "0", "0", "8640", "0", "0", other_dependants=(("20000", "0"),)
    )

    assert worksheet.get(OTHER_DEPENDANTS_MEDICAL).value == D("20000.00")
    assert worksheet.get(ontario.OTHER_DEPENDANTS_MEDICAL).value == D("15551.00")
    assert worksheet.get(ontario.MEDICAL_CLAIM).value == D("15551.00")
    assert worksheet.get(MEDICAL_CLAIM).value == D("20000.00")


def test_ontario_pooled_dependants_would_give_the_wrong_line_58729() -> None:
    separate = compute(
        "48000",
        "0",
        "0",
        "0",
        "8640",
        "0",
        "0",
        other_dependants=(("3000", "10000"), ("1000", "40000")),
    )
    pooled = compute(
        "48000", "0", "0", "0", "8640", "0", "0", other_dependants=(("4000", "50000"),)
    )

    assert separate.get(ontario.OTHER_DEPENDANTS_MEDICAL).value == D("2700.00")
    # 4000 - lesser(1500.00, 2885) = 2500.00, not 2700.00.
    assert pooled.get(ontario.OTHER_DEPENDANTS_MEDICAL).value == D("2500.00")


def test_no_medical_expenses_claim_nothing_on_line_58769() -> None:
    worksheet = compute("48000", "0", "0", "0", "8640", "0", "0")

    assert worksheet.get(ontario.MEDICAL_EXPENSES_OVER_THRESHOLD).value == D("0")
    assert worksheet.get(ontario.OTHER_DEPENDANTS_MEDICAL).value == D("0")
    assert worksheet.get(ontario.MEDICAL_CLAIM).value == D("0")
    assert worksheet.get(ontario.NON_REFUNDABLE_CREDIT_AMOUNTS).value == D("15736.95")


def step_3(**amounts: Any) -> Worksheet:
    """A return with no income, no CPP, no RRSP and no deductions but the keyword `amounts`."""
    return compute("0", "0", "0", "0", "0", "0", "0", **amounts)


def return_o() -> Worksheet:
    """Return O's inputs, as in `returns/2025_return_o.yaml`: a pension and the Step 3 lines."""
    return compute(
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        "0",
        other_pensions_and_superannuation="60000",
        rpp_deduction="3000",
        support_payments_deduction="6000",
        total_carrying_charges="300",
        total_interest_expenses="200",
        business_investment_loss="10000",
        income_tax_deducted="6000",
    )


def test_return_os_deductions_are_14500_and_its_net_income_before_adjustments_45500() -> None:
    # Return O: other pensions and superannuation of 60000 (line 11500), the only income, so total
    # income is 60000. RPP deduction 3000 (line 20700); a business investment loss of 10000 (line
    # 21699) with no earlier capital gains deduction, so Form T1436 line 15 is 0 and line 18 is
    # 10000, 50% of it 5000.00 (line 21700); the deductible support payments 6000 (line 22000); the
    # Federal Worksheet's carrying charges 300 and interest expenses 200 (line 22100, 500). Line
    # 23300 is 3000 + 5000.00 + 6000 + 500 = 14500.00, line 23400 is 60000 - 14500.00 = 45500.00,
    # and net income (line 23600) and taxable income are the same.
    worksheet = return_o()

    assert worksheet.get(TOTAL_INCOME).value == D("60000")
    assert worksheet.get(CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES).value == D("500.00")
    assert worksheet.get(CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024).value == D("0")
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE).value == D("0")
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION).value == D("0")
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION).value == D("10000")
    assert worksheet.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D("5000.00")
    assert worksheet.get(FHSA_DEDUCTION).value == D("0")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("14500.00")
    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("45500.00")
    assert worksheet.get(NET_INCOME).value == D("45500.00")
    assert worksheet.get(TAXABLE_INCOME).value == D("45500.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "carrying_charges_interest_expenses_and_other_expenses: total_carrying_charges 300 "
        "+ total_interest_expenses 200 + total_other_expenses 0 = 500"
    ) in rendered
    assert (
        "business_investment_loss_reduction_available: "
        "capital_gains_deductions_claimed_1985_to_2024 0 "
        "less other_business_investment_loss_reductions_1986_to_2024 0 = 0"
    ) in rendered
    assert (
        "business_investment_loss_reduction: lesser of "
        "business_investment_loss_reduction_available 0 and business_investment_loss 10000 = 0"
    ) in rendered
    assert (
        "business_investment_loss_after_reduction: business_investment_loss 10000 "
        "less business_investment_loss_reduction 0 = 10000"
    ) in rendered
    assert (
        "allowable_business_investment_loss: 50% of business_investment_loss_after_reduction "
        "10000 (half-up to 0.01)"
    ) in rendered
    assert (
        "deductions_from_total_income: rpp_deduction 3000 + rrsp_deduction 0 + fhsa_deduction 0 "
        "+ elected_split_pension_deduction 0 + union_dues 0 + uccb_repayment 0 "
        "+ child_care_expenses 0 + allowable_business_investment_loss 5000 "
        "+ support_payments_deduction 6000 "
        "+ carrying_charges_interest_expenses_and_other_expenses 500 "
        "+ cpp_enhanced_contributions 0 + exploration_and_development_expenses 0 "
        "+ other_deductions 0 = 14500"
    ) in rendered
    assert (
        "net_income_before_adjustments: total_income 60000 "
        "less deductions_from_total_income 14500 = 45500"
    ) in rendered
    assert (
        "net_income: total_income 60000 less deductions_from_total_income 14500, "
        "not below 0 = 45500"
    ) in rendered


def test_return_os_taxes_follow_from_its_taxable_income_of_45500() -> None:
    # Taxable income 45500.00: 14.5% federally, 6597.50, less 14.5% of the basic personal amount
    # 16129.00, 2338.71 (the Canada employment amount is 0 with no employment income): 4258.79.
    # Ontario: 5.05% of 45500.00 is 2297.75, less 5.05% of 12747.00, 643.72: 1654.03, no surtax,
    # no tax reduction, no LIFT credit; the health premium on taxable income of more than 38500
    # but not more than 48000 is 450, so the Ontario tax is 2104.03 and the total payable
    # 4258.79 + 2104.03 = 6362.82. The income tax deducted of 6000 leaves a balance owing of
    # 362.82.
    worksheet = return_o()

    assert worksheet.get(FEDERAL_BASIC_TAX).value == D("6597.50")
    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("4258.79")
    assert worksheet.get(ONTARIO_TAX_AFTER_CREDITS).value == D("1654.03")
    assert worksheet.get(ONTARIO_HEALTH_PREMIUM).value == D("450")
    assert worksheet.get(ONTARIO_TAX).value == D("2104.03")
    assert worksheet.get(TOTAL_PAYABLE).value == D("6362.82")
    assert worksheet.get(TOTAL_CREDITS).value == D("6000")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("362.82")


@pytest.mark.parametrize(
    ("carrying_charges", "interest_expenses", "other_expenses", "line_22100"),
    [
        # Carrying charges 300 and interest expenses 200, as in Return O.
        ("300", "200", "0", "500.00"),
        # One distinct power of two for each line, so a line left out or added twice changes it.
        ("1", "2", "4", "7"),
        ("0", "0", "0", "0"),
    ],
)
def test_line_22100_adds_the_worksheets_lines_1_to_3(
    carrying_charges: str, interest_expenses: str, other_expenses: str, line_22100: str
) -> None:
    # Federal Worksheet "Line 22100": line 4 "Add lines 1 to 3. Enter this amount on line 22100 of
    # your return."
    worksheet = step_3(
        total_carrying_charges=carrying_charges,
        total_interest_expenses=interest_expenses,
        total_other_expenses=other_expenses,
    )

    assert worksheet.get(CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES).value == D(
        line_22100
    )
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D(line_22100)


@pytest.mark.parametrize(
    ("gains_deductions", "other_reductions", "line_15", "line_17", "line_18", "line_20"),
    [
        # No capital gains deduction in earlier years: the whole loss of 10000 is reduced by
        # nothing, and 50% of it is deductible.
        ("0", "0", "0", "0", "10000", "5000.00"),
        # Line 15 of 4000 and a loss of 10000 give line 17 of 4000 and line 21700 of 3000.00.
        ("4000", "0", "4000", "4000", "6000", "3000.00"),
        # Line 7 is 6000 and line 14 is 2000 (the 2024 amounts of Schedule 3): line 15 is 4000.
        ("6000", "2000", "4000", "4000", "6000", "3000.00"),
        # Line 15 above the loss: line 17 is the loss itself, so nothing is left to deduct.
        ("12000", "0", "12000", "10000", "0", "0.00"),
        # Line 15 equal to the loss.
        ("10000", "0", "10000", "10000", "0", "0.00"),
    ],
)
def test_the_business_investment_loss_is_reduced_by_the_earlier_gains_deductions_then_halved(
    gains_deductions: str,
    other_reductions: str,
    line_15: str,
    line_17: str,
    line_18: str,
    line_20: str,
) -> None:
    # Form T1436 line 21700: line 15 "Line 7 minus line 14"; line 16 the loss in 2025; line 17
    # "Enter whichever is less: amount from line 15 or line 16."; line 18 "Line 16 minus line
    # 17"; line 20 "Line 18 multiplied by the percentage on line 19" (50 %).
    worksheet = step_3(
        capital_gains_deductions_2001_to_2024=gains_deductions,
        other_business_investment_loss_reductions_2024=other_reductions,
        business_investment_loss="10000",
    )

    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE).value == D(line_15)
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION).value == D(line_17)
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION).value == D(line_18)
    assert worksheet.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D(line_20)
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D(line_20)


def test_a_line_15_of_4000_renders_the_reduction_lines_of_the_trace() -> None:
    # Line 15 of 4000 (line 6, the 2001 to 2024 deductions) and a loss of 10000.
    worksheet = step_3(
        capital_gains_deductions_2001_to_2024="4000", business_investment_loss="10000"
    )

    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "business_investment_loss_reduction: lesser of "
        "business_investment_loss_reduction_available 4000 and business_investment_loss 10000 "
        "= 4000"
    ) in rendered
    assert (
        "business_investment_loss_after_reduction: business_investment_loss 10000 "
        "less business_investment_loss_reduction 4000 = 6000"
    ) in rendered
    assert (
        "allowable_business_investment_loss: 50% of business_investment_loss_after_reduction "
        "6000 (half-up to 0.01)"
    ) in rendered


def test_t1436_line_15_goes_negative_when_line_14_exceeds_line_7() -> None:
    # Form T1436 line 15 "Line 7 minus line 14" prints no "(if negative, enter "0")", and line 17
    # "Enter whichever is less: amount from line 15 or line 16." prints no floor either, so the
    # lines follow the form as printed: line 7 of 0 and line 14 of 2000 give line 15 of -2000,
    # line 17 of -2000 (the lesser of -2000 and 10000), line 18 of 10000 - (-2000) = 12000 and
    # line 21700 of 12000 x 50% = 6000.00, more than half of the loss of 10000. The form states
    # no treatment of this case, so this records the printed arithmetic, not a confirmed one.
    worksheet = step_3(
        other_business_investment_loss_reductions_2024="2000", business_investment_loss="10000"
    )

    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE).value == D("-2000")
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION).value == D("-2000")
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION).value == D("12000")
    assert worksheet.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D("6000.00")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("6000.00")


def test_t1436_lines_7_and_14_add_lines_1_to_6_and_8_to_13_once_each() -> None:
    # Line 7 "Add lines 1 to 6." and line 14 "Add lines 8 to 13.": one distinct power of two for
    # each of the twelve lines, so a line left out or added twice changes the sums: 1 + 2 + 4 + 8
    # + 16 + 32 = 63 and 64 + 128 + 256 + 512 + 1024 + 2048 = 4032. Line 15, "Line 7 minus line
    # 14", is -3969: the form prints no "(if negative, enter "0")".
    worksheet = step_3(
        capital_gains_deductions_1985_to_1987="1",
        capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property="2",
        capital_gains_deductions_1988_and_1989_eligible_capital_property="4",
        capital_gains_deductions_1990_to_1999="8",
        capital_gains_deductions_2000="16",
        capital_gains_deductions_2001_to_2024="32",
        other_business_investment_loss_reductions_1986_to_1994="64",
        other_business_investment_loss_reductions_1994_to_1996="128",
        other_business_investment_loss_reductions_1997_to_1999="256",
        other_business_investment_loss_reductions_2000="512",
        other_business_investment_loss_reductions_2001_to_2023="1024",
        other_business_investment_loss_reductions_2024="2048",
    )

    assert worksheet.get(CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024).value == D("63")
    assert worksheet.get(OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024).value == D("4032")
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE).value == D("-3969")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "capital_gains_deductions_claimed_1985_to_2024: capital_gains_deductions_1985_to_1987 1 "
        "+ capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property 2 "
        "+ capital_gains_deductions_1988_and_1989_eligible_capital_property 4 "
        "+ capital_gains_deductions_1990_to_1999 8 + capital_gains_deductions_2000 16 "
        "+ capital_gains_deductions_2001_to_2024 32 = 63"
    ) in rendered
    assert (
        "other_business_investment_loss_reductions_1986_to_2024: "
        "other_business_investment_loss_reductions_1986_to_1994 64 "
        "+ other_business_investment_loss_reductions_1994_to_1996 128 "
        "+ other_business_investment_loss_reductions_1997_to_1999 256 "
        "+ other_business_investment_loss_reductions_2000 512 "
        "+ other_business_investment_loss_reductions_2001_to_2023 1024 "
        "+ other_business_investment_loss_reductions_2024 2048 = 4032"
    ) in rendered
    assert (
        "business_investment_loss_reduction_available: "
        "capital_gains_deductions_claimed_1985_to_2024 63 "
        "less other_business_investment_loss_reductions_1986_to_2024 4032 = -3969"
    ) in rendered


def test_line_15_may_be_negative_as_the_form_prints_no_floor() -> None:
    # Other reductions (line 14) of 500 and no capital gains deductions (line 7): line 15 is -500,
    # and line 17 "Enter whichever is less: amount from line 15 or line 16." is -500 too, so line 18
    # "Line 16 minus line 17" is 10000 + 500 = 10500 and line 20 is 5250.00. The form prints no
    # floor on lines 15 and 17, so the kinds are signed and the result follows the printed lines.
    worksheet = step_3(
        other_business_investment_loss_reductions_2024="500", business_investment_loss="10000"
    )

    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE).value == D("-500")
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_REDUCTION).value == D("-500")
    assert worksheet.get(BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION).value == D("10500")
    assert worksheet.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D("5250.00")


def test_the_allowable_business_investment_loss_is_rounded_half_up_to_the_cent() -> None:
    # Line 20 is a dollars-and-cents box: 10000.01 x 50% = 5000.005, a tie, up to 5000.01.
    worksheet = step_3(business_investment_loss="10000.01")

    assert worksheet.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D("5000.01")


def test_a_loss_of_0_gives_an_allowable_loss_of_0() -> None:
    worksheet = step_3()

    assert worksheet.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D("0")


def test_line_23300_adds_every_wired_deduction_once_in_the_forms_line_order() -> None:
    # T1 line 53 and line 23300 "Add lines 35 to 52.": one distinct power of two for each line
    # wired but the child care expenses and the enhanced CPP contributions (0 here, with no child
    # and no employment income), so a line left out or added twice changes the sum: RPP deduction
    # 1 (line 20700), RRSP deduction 2 (line 20800), FHSA deduction 4 (line 20805), split-pension
    # deduction 8 (line 21000), union dues 16 (line 21200), UCCB repayment 32 (line 21300), the
    # allowable business investment loss 64.00 (line 21700, 50% of a loss of 128), the deductible
    # support payments 128 (line 22000), the Federal Worksheet's 100 + 100 + 56 = 256 (line
    # 22100), exploration and development expenses 512 (line 22400) and other deductions 1024
    # (line 23200): 2047. Other income of 5000 is total income, so line 23400 is 2953.
    worksheet = compute(
        "0",
        "0",
        "0",
        "2",
        "2",
        "2",
        "16",
        other_income="5000",
        rpp_deduction="1",
        fhsa_contributions_in_2025="4",
        fhsa_contributions_deducted="4",
        elected_split_pension_deduction="8",
        uccb_repayment="32",
        business_investment_loss="128",
        support_payments_deduction="128",
        total_carrying_charges="100",
        total_interest_expenses="100",
        total_other_expenses="56",
        exploration_and_development_expenses="512",
        other_deductions="1024",
    )

    assert worksheet.get(RRSP_DEDUCTION).value == D("2")
    assert worksheet.get(FHSA_DEDUCTION).value == D("4")
    assert worksheet.get(ALLOWABLE_BUSINESS_INVESTMENT_LOSS).value == D("64.00")
    assert worksheet.get(CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES).value == D("256")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("2047")
    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("2953")
    assert worksheet.get(NET_INCOME).value == D("2953")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "deductions_from_total_income: rpp_deduction 1 + rrsp_deduction 2 + fhsa_deduction 4 "
        "+ elected_split_pension_deduction 8 + union_dues 16 + uccb_repayment 32 "
        "+ child_care_expenses 0 + allowable_business_investment_loss 64 "
        "+ support_payments_deduction 128 "
        "+ carrying_charges_interest_expenses_and_other_expenses 256 "
        "+ cpp_enhanced_contributions 0 + exploration_and_development_expenses 512 "
        "+ other_deductions 1024 = 2047"
    ) in rendered


def test_line_23400_is_negative_when_the_deductions_exceed_total_income() -> None:
    # T1 line 54 and line 23400 "Line 34 minus line 53 (if negative, show in brackets)": total
    # income of 1000 less deductions of 2047 (the same lines as above) is -1047. The net income of
    # line 56 (line 23600) "Line 54 minus line 55 (if negative, enter "0")" is 0, as is the
    # taxable income, until line 23500 is wired.
    worksheet = compute(
        "0",
        "0",
        "0",
        "2",
        "2",
        "2",
        "16",
        other_income="1000",
        rpp_deduction="1",
        fhsa_contributions_in_2025="4",
        fhsa_contributions_deducted="4",
        elected_split_pension_deduction="8",
        uccb_repayment="32",
        business_investment_loss="128",
        support_payments_deduction="128",
        total_carrying_charges="100",
        total_interest_expenses="100",
        total_other_expenses="56",
        exploration_and_development_expenses="512",
        other_deductions="1024",
    )

    assert worksheet.get(TOTAL_INCOME).value == D("1000")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("2047")
    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("-1047")
    assert worksheet.get(NET_INCOME).value == D("0")
    assert worksheet.get(TAXABLE_INCOME).value == D("0")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "net_income_before_adjustments: total_income 1000 "
        "less deductions_from_total_income 2047 = -1047"
    ) in rendered
    assert (
        "net_income: total_income 1000 less deductions_from_total_income 2047, not below 0 = 0"
    ) in rendered


def test_line_23400_equals_net_income_when_the_deductions_are_below_total_income() -> None:
    worksheet = step_3(other_income="1000", other_deductions="400")

    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("600")
    assert worksheet.get(NET_INCOME).value == D("600")


def test_the_uccb_repayment_is_a_deduction_on_line_21300_and_still_the_worksheets_line_6() -> None:
    # T1 line 40 and line 21300 "Universal child care benefit (UCCB) repayment": the same input
    # the Federal Worksheet's line 6 "Amount from line 21300 of your return" reads. UCCB of 1000
    # (line 11700) and a repayment of 300: total income 1000, line 23300 300, net income 700, and
    # the worksheet's line 8 is 300.
    worksheet = step_3(universal_child_care_benefit="1000", uccb_repayment="300")

    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("300")
    assert worksheet.get(NET_INCOME).value == D("700")
    assert worksheet.get(UCCB_AND_RDSP_INCOME_REPAYMENTS).value == D("300")


def test_a_first_fhsa_with_8000_contributed_and_deducted_gives_20805_of_8000() -> None:
    # Schedule 15: a first FHSA opened in 2025, 8000 contributed (line 1), no statement figures,
    # all 8000 deducted (line 57). Line 3 is 8000 - 0, line 5 8000 + 0, line 13 8000; line 16 is
    # 8000.00 + 0; line 39 is 8000.00 - 0, so line 40 is the lesser of 8000 and 8000.00, 8000.
    # Step 3: line 43 is 8000 + 0, line 45 8000 - 0, line 48 is 40000.00 - 0 and line 50 the same;
    # line 51 is the lesser of 8000 and 40000.00: 8000. Line 57 is 8000, at most line 51, line
    # 20805; line 56 is 0 + 8000 - 0, so line 58 is 0.
    worksheet = step_3(fhsa_contributions_in_2025="8000", fhsa_contributions_deducted="8000")

    assert worksheet.get(FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL).value == D(
        "8000"
    )
    assert worksheet.get(FHSA_CONTRIBUTIONS_LIMIT).value == D("8000.00")
    assert worksheet.get(FHSA_ANNUAL_AMOUNT).value == D("8000.00")
    assert worksheet.get(FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD).value == D("8000.00")
    assert worksheet.get(FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS).value == D("8000.00")
    assert worksheet.get(FHSA_ANNUAL_LIMIT_FROM_STEP_2).value == D("8000.00")
    assert worksheet.get(FHSA_ANNUAL_LIMIT).value == D("8000.00")
    assert worksheet.get(FHSA_TOTAL_ANNUAL_LIMITS).value == D("8000.00")
    assert worksheet.get(FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS).value == D("8000.00")
    assert worksheet.get(FHSA_LIFETIME_LIMIT).value == D("40000.00")
    assert worksheet.get(FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS).value == D("40000.00")
    assert worksheet.get(FHSA_MAXIMUM_DEDUCTION).value == D("8000.00")
    assert worksheet.get(FHSA_CONTRIBUTIONS_AVAILABLE).value == D("8000")
    assert worksheet.get(FHSA_DEDUCTION).value == D("8000")
    assert worksheet.get(FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD).value == D("0")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("8000")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert "fhsa_annual_amount: credit amount 8000 (half-up to 0.01)" in rendered
    assert "fhsa_annual_amount_for_2024: credit amount 8000 (half-up to 0.01)" in rendered
    assert "fhsa_lifetime_limit: credit amount 40000 (half-up to 0.01)" in rendered
    assert (
        "fhsa_annual_limit: fhsa_annual_limit_from_step_2 8000, "
        "chosen as fhsa_maximum_participation_period_ended is 0"
    ) in rendered
    assert (
        "fhsa_maximum_deduction: lesser of fhsa_annual_limits_less_deductions 8000 "
        "and fhsa_lifetime_limit_less_deductions_and_transfers 40000 = 8000"
    ) in rendered
    assert (
        "fhsa_deduction: fhsa_contributions_deducted 8000, at most fhsa_maximum_deduction 8000"
    ) in rendered
    assert (
        "fhsa_unused_contributions_carried_forward: fhsa_contributions_available 8000 "
        "less fhsa_deduction 8000 = 0"
    ) in rendered


def test_a_deduction_below_line_51_carries_the_rest_forward_as_line_58() -> None:
    # Line 57 of 5000 against a line 51 of 8000: line 20805 is 5000, and line 58 "Line 56 minus
    # line 57 Your unused FHSA contributions available to deduct in future years" is 8000 - 5000.
    worksheet = step_3(fhsa_contributions_in_2025="8000", fhsa_contributions_deducted="5000")

    assert worksheet.get(FHSA_MAXIMUM_DEDUCTION).value == D("8000")
    assert worksheet.get(FHSA_DEDUCTION).value == D("5000")
    assert worksheet.get(FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD).value == D("3000")
    assert worksheet.get(DEDUCTIONS_FROM_TOTAL_INCOME).value == D("5000")


def test_a_claim_above_line_51_is_refused_naming_both_kinds() -> None:
    # Line 57 "(cannot be more than the amount on line 51 of the previous page)": 8000.01 against a
    # line 51 of 8000 is an input error, not capped to 8000.
    with pytest.raises(InputAboveBoundError) as raised:
        step_3(fhsa_contributions_in_2025="8000", fhsa_contributions_deducted="8000.01")

    assert str(raised.value).startswith(
        "ca/fhsa_contributions_deducted 8000.01 is above ca/fhsa_maximum_deduction 8000"
    )


def test_any_claim_is_refused_when_line_51_is_0() -> None:
    # No contributions and no room: line 51 is 0, so a claim of 1 is above it.
    with pytest.raises(InputAboveBoundError) as raised:
        step_3(fhsa_contributions_deducted="1")

    assert str(raised.value).startswith(
        "ca/fhsa_contributions_deducted 1 is above ca/fhsa_maximum_deduction 0"
    )


def test_a_maximum_participation_period_ended_in_a_prior_year_sets_line_40_to_0() -> None:
    # Step 2: "If your maximum participation period (MPP) ended in a prior year, do not complete
    # this step. Your 2025 annual FHSA limit is "0". Enter "0" on line 40 and continue at Step 3."
    # With 8000 contributed Step 2 would give 8000 (the count 0), but with the count 1 line 40 is
    # the printed 0, so lines 43 and 45 are 0 + 0 - 0, line 51 is the lesser of 0 and 40000.00:
    # 0, and 8000 is carried forward (line 58 is 8000 + 0 - 0 - 0).
    worksheet = step_3(
        fhsa_contributions_in_2025="8000",
        fhsa_maximum_participation_period_ended=1,
        fhsa_contributions_deducted="0",
    )

    assert worksheet.get(FHSA_ANNUAL_LIMIT_FROM_STEP_2).value == D("8000")
    assert worksheet.get(FHSA_ANNUAL_LIMIT_AFTER_MAXIMUM_PARTICIPATION_PERIOD).value == D("0")
    assert worksheet.get(FHSA_ANNUAL_LIMIT).value == D("0")
    assert worksheet.get(FHSA_TOTAL_ANNUAL_LIMITS).value == D("0")
    assert worksheet.get(FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS).value == D("0")
    assert worksheet.get(FHSA_MAXIMUM_DEDUCTION).value == D("0")
    assert worksheet.get(FHSA_DEDUCTION).value == D("0")
    assert worksheet.get(FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD).value == D("8000")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "fhsa_annual_limit_after_maximum_participation_period: credit amount 0 (half-up to 0.01)"
    ) in rendered
    assert (
        "fhsa_annual_limit: fhsa_annual_limit_after_maximum_participation_period 0, "
        "chosen as fhsa_maximum_participation_period_ended is 1"
    ) in rendered


def test_a_claim_is_refused_once_the_maximum_participation_period_has_ended() -> None:
    with pytest.raises(InputAboveBoundError) as raised:
        step_3(
            fhsa_contributions_in_2025="8000",
            fhsa_maximum_participation_period_ended=1,
            fhsa_contributions_deducted="1000",
        )

    assert str(raised.value).startswith(
        "ca/fhsa_contributions_deducted 1000 is above ca/fhsa_maximum_deduction 0"
    )


def test_a_second_year_adds_the_statements_totals_to_the_new_annual_limit() -> None:
    # An FHSA opened in 2024 with 8000 contributed and deducted that year. The 2025 participation
    # room statement gives line 7 (contributions in 2024) 8000, line 8 (before a first qualifying
    # withdrawal) 8000, line 42 (total annual limits for 2024 and prior years) 8000 and line 44
    # (total deductions for 2024 and prior years) 8000. With 8000 contributed in 2025 the annual
    # limit (line 40) is 8000, line 43 is 8000 + 8000 = 16000, line 45 16000 - 8000 = 8000, line
    # 48 is 40000.00 - 8000 = 32000.00 and line 51 the lesser of 8000 and 32000.00: 8000.
    worksheet = step_3(
        fhsa_contributions_in_2025="8000",
        fhsa_contributions_in_2024="8000",
        fhsa_contributions_in_2024_before_first_qualifying_withdrawal="8000",
        fhsa_annual_limits_for_2024_and_prior_years="8000",
        fhsa_deductions_for_2024_and_prior_years="8000",
        fhsa_contributions_deducted="8000",
    )

    assert worksheet.get(FHSA_CONTRIBUTIONS_IN_2024_AFTER_FIRST_QUALIFYING_WITHDRAWAL).value == D(
        "0"
    )
    assert worksheet.get(FHSA_ANNUAL_LIMIT).value == D("8000")
    assert worksheet.get(FHSA_TOTAL_ANNUAL_LIMITS).value == D("16000")
    assert worksheet.get(FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS).value == D("8000")
    assert worksheet.get(FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS).value == D("32000")
    assert worksheet.get(FHSA_MAXIMUM_DEDUCTION).value == D("8000")
    assert worksheet.get(FHSA_DEDUCTION).value == D("8000")
    assert worksheet.get(FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD).value == D("0")


def test_an_rrsp_transfer_in_2025_lowers_the_annual_limit_and_the_lifetime_room() -> None:
    # Line 18 (transfers from RRSPs to FHSAs in 2025) of 3000: lines 19 and 23 are 3000; line 36
    # is line 24 (3000) less line 35 (0); line 39 is 8000.00 - 3000 = 5000.00, so line 40, the
    # lesser of line 13 (8000) and 5000.00, is 5000.00. Line 50 is 40000.00 - 0 - 3000 =
    # 37000.00, so line 51 is the lesser of 5000.00 and 37000.00: 5000.00. A deduction of 5000
    # leaves 8000 - 5000 = 3000 as line 58.
    worksheet = step_3(
        fhsa_contributions_in_2025="8000",
        fhsa_rrsp_transfers_in_2025="3000",
        fhsa_contributions_deducted="5000",
    )

    assert worksheet.get(FHSA_TOTAL_RRSP_TRANSFERS).value == D("3000")
    assert worksheet.get(FHSA_NET_RRSP_TRANSFER_AMOUNT).value == D("3000")
    assert worksheet.get(FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS).value == D("3000")
    assert worksheet.get(FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS).value == D("5000")
    assert worksheet.get(FHSA_ANNUAL_LIMIT).value == D("5000")
    assert worksheet.get(FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS_AND_TRANSFERS).value == D("37000")
    assert worksheet.get(FHSA_MAXIMUM_DEDUCTION).value == D("5000")
    assert worksheet.get(FHSA_DEDUCTION).value == D("5000")
    assert worksheet.get(FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD).value == D("3000")
    with pytest.raises(InputAboveBoundError):
        step_3(
            fhsa_contributions_in_2025="8000",
            fhsa_rrsp_transfers_in_2025="3000",
            fhsa_contributions_deducted="5000.01",
        )


def test_a_designated_withdrawal_lowers_line_13_and_comes_off_line_56() -> None:
    # Line 6 (designated withdrawals in 2025) of 1000 against contributions after a first
    # qualifying withdrawal (line 11) of 0: line 12 is 1000, line 13 is 8000 - 1000 = 7000, so
    # line 40 is 7000 and line 51 7000; line 56 is 0 + 8000 - 1000 = 7000, and a deduction of
    # 7000 leaves 0 as line 58.
    worksheet = step_3(
        fhsa_contributions_in_2025="8000",
        fhsa_designated_withdrawals_in_2025="1000",
        fhsa_contributions_deducted="7000",
    )

    assert worksheet.get(FHSA_EXCESS_DESIGNATED_WITHDRAWALS).value == D("1000")
    assert worksheet.get(FHSA_CONTRIBUTIONS_LIMIT).value == D("7000")
    assert worksheet.get(FHSA_ANNUAL_LIMIT).value == D("7000")
    assert worksheet.get(FHSA_CONTRIBUTIONS_AVAILABLE).value == D("7000")
    assert worksheet.get(FHSA_DEDUCTION).value == D("7000")
    assert worksheet.get(FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD).value == D("0")


def test_contributions_after_a_first_qualifying_withdrawal_count_against_the_withdrawals() -> None:
    # Lines 1 and 2: 8000 contributed in 2025, of which 600 after the first qualifying withdrawal,
    # so line 3 is 7400; designated withdrawals (line 6) of 1000 less line 11 (0 for 2024 + 600
    # after the withdrawal in 2025) is line 12, 400, and line 13 is 7400 - 400 = 7000.
    worksheet = step_3(
        fhsa_contributions_in_2025="8000",
        fhsa_contributions_in_2025_after_first_qualifying_withdrawal="600",
        fhsa_designated_withdrawals_in_2025="1000",
    )

    assert worksheet.get(FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL).value == D(
        "7400"
    )
    assert worksheet.get(FHSA_CONTRIBUTIONS_AFTER_FIRST_QUALIFYING_WITHDRAWAL).value == D("600")
    assert worksheet.get(FHSA_EXCESS_DESIGNATED_WITHDRAWALS).value == D("400")
    assert worksheet.get(FHSA_CONTRIBUTIONS_LIMIT).value == D("7000")


def test_line_3_may_be_negative_as_the_form_prints_no_floor() -> None:
    # Line 2 of 500 above line 1 of 100: line 3 "Line 1 minus line 2 =" is -400 and so is line 5
    # "Line 3 plus line 4 =", but line 13 "Line 5 minus line 12 (if negative, enter "0")" is 0.
    worksheet = step_3(
        fhsa_contributions_in_2025="100",
        fhsa_contributions_in_2025_after_first_qualifying_withdrawal="500",
    )

    assert worksheet.get(FHSA_CONTRIBUTIONS_IN_2025_BEFORE_FIRST_QUALIFYING_WITHDRAWAL).value == D(
        "-400"
    )
    assert worksheet.get(FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT).value == D("-400")
    assert worksheet.get(FHSA_CONTRIBUTIONS_LIMIT).value == D("0")
    assert worksheet.get(FHSA_ANNUAL_LIMIT).value == D("0")


def test_the_statements_carryforwards_and_variables_each_enter_their_line_once() -> None:
    # One distinct figure for each statement figure, so a figure left out or added twice changes
    # the result: line 4 ("B") 1, line 15 (carryforward for 2025) 10, line 17 100, line 20 1000,
    # line 28 ("H") 5, line 31 (carryforward for 2024) 20 and line 34 ("F") 50. Line 3 is 0, so
    # line 5 is 0 + 1 = 1 and line 13 is 1. Line 16 is 8000.00 + 10 = 8010.00. Line 19 is 100 + 0
    # and line 22 is 1000 + 0, so line 23 (and line 24) is 100 - 1000 = -900, and line 27 (line 25
    # minus line 26) is 100 - 1000 = -900 too; line 29 is -900 - 5 floored at 0, line 32 is
    # 8000.00 + 20 = 8020.00, line 33 is the lesser of 0 and 8020.00, 0, line 35 is 0 + 50 = 50 and
    # line 36 is -900 - 50 = -950. Line 39 is 8010.00 - (-950) = 8960.00 and line 40 the lesser of
    # line 13 (1) and 8960.00: 1.
    worksheet = step_3(
        fhsa_variable_b_amount="1",
        fhsa_carryforward_for_2025="10",
        fhsa_rrsp_transfers_in_2024_and_prior_years="100",
        fhsa_designated_transfers_in_2024_and_prior_years="1000",
        fhsa_variable_h_amount="5",
        fhsa_carryforward_for_2024="20",
        fhsa_variable_f_amount="50",
    )

    assert worksheet.get(FHSA_CONTRIBUTIONS_PLUS_VARIABLE_B_AMOUNT).value == D("1")
    assert worksheet.get(FHSA_CONTRIBUTIONS_LIMIT).value == D("1")
    assert worksheet.get(FHSA_ANNUAL_AMOUNT_WITH_CARRYFORWARD).value == D("8010")
    assert worksheet.get(FHSA_TOTAL_RRSP_TRANSFERS).value == D("100")
    assert worksheet.get(FHSA_TOTAL_DESIGNATED_TRANSFERS).value == D("1000")
    assert worksheet.get(FHSA_NET_RRSP_TRANSFER_AMOUNT).value == D("-900")
    assert worksheet.get(FHSA_NET_RRSP_TRANSFER_AMOUNT_FOR_2024_AND_PRIOR_YEARS).value == D("-900")
    assert worksheet.get(FHSA_NET_TRANSFER_AMOUNT_LESS_VARIABLE_H_AMOUNT).value == D("0")
    assert worksheet.get(FHSA_ANNUAL_AMOUNT_FOR_2024_WITH_CARRYFORWARD).value == D("8020")
    assert worksheet.get(FHSA_TRANSFER_AMOUNT_AT_MOST_LIMIT).value == D("0")
    assert worksheet.get(FHSA_TRANSFER_AMOUNT_PLUS_VARIABLE_F_AMOUNT).value == D("50")
    assert worksheet.get(FHSA_NET_TRANSFER_AMOUNT_AFTER_PRIOR_YEARS).value == D("-950")
    assert worksheet.get(FHSA_ANNUAL_AMOUNT_AFTER_TRANSFERS).value == D("8960")
    assert worksheet.get(FHSA_ANNUAL_LIMIT).value == D("1")


def test_the_unused_contributions_from_the_statement_add_to_line_56() -> None:
    # Line 52 (unused contributions available to deduct, from the statement) of 2500 and 8000
    # contributed in 2025: line 54 is 2500 + 8000 = 10500 and line 56 is 10500 - 0. The annual
    # limit is 8000, so line 51 is 8000 and 8000 is deducted: line 58 is 10500 - 8000 = 2500.
    worksheet = step_3(
        fhsa_contributions_in_2025="8000",
        fhsa_unused_contributions_brought_forward="2500",
        fhsa_contributions_deducted="8000",
    )

    assert worksheet.get(FHSA_UNUSED_CONTRIBUTIONS_PLUS_CONTRIBUTIONS).value == D("10500")
    assert worksheet.get(FHSA_CONTRIBUTIONS_AVAILABLE).value == D("10500")
    assert worksheet.get(FHSA_MAXIMUM_DEDUCTION).value == D("8000")
    assert worksheet.get(FHSA_UNUSED_CONTRIBUTIONS_CARRIED_FORWARD).value == D("2500")


def test_the_lifetime_limit_caps_the_maximum_deduction() -> None:
    # Total deductions for 2024 and prior years (line 44) of 38000 and total annual limits (line
    # 42) of 38000: line 45 is 8000 + 38000 - 38000 = 8000 but line 48 is 40000.00 - 38000 =
    # 2000.00, so line 51 is the lesser of 8000 and 2000.00: 2000.00.
    worksheet = step_3(
        fhsa_contributions_in_2025="8000",
        fhsa_annual_limits_for_2024_and_prior_years="38000",
        fhsa_deductions_for_2024_and_prior_years="38000",
    )

    assert worksheet.get(FHSA_ANNUAL_LIMITS_LESS_DEDUCTIONS).value == D("8000")
    assert worksheet.get(FHSA_LIFETIME_LIMIT_LESS_DEDUCTIONS).value == D("2000")
    assert worksheet.get(FHSA_MAXIMUM_DEDUCTION).value == D("2000")


def test_return_ps_political_contribution_credit_is_1402_76_and_lowers_the_refund() -> None:
    # Return P is Return I without the community food program donations and with Ontario political
    # contributions of 3000 (ON479 line 15, line 63100; the worksheet reads it as line 63110):
    # employment income of 48000, as Return I, to line 86 of 1484.56 and, with no donations, line
    # 88 of 1484.56; the health premium of 450 gives the Ontario tax 1934.56. The federal tax after
    # credits is 3909.94, so the total payable is 3909.94 + 1934.56 = 5844.50.
    # Worksheet ON479 line 16: 3000 is more than 1,666.82, so column 3 applies. Line 2 is 1,666.82,
    # line 3 is 3000 - 1,666.82 = 1,333.18, line 5 is 1,333.18 x 33.33% = 444.3494, rounded
    # half-up to the cent: 444.35, line 6 is the printed 958.41 and line 7 is 444.35 + 958.41 =
    # 1,402.76, below the maximum of 1,666.82, so ON479 line 16 is 1,402.76. (Columns 1 and 2 are
    # also built: column 1 line 7 is 75% x 3000 = 2,250.00 and column 2 line 7 is 50% x 2,499.95 =
    # 1,249.975, up to 1,249.98, + 375.03 = 1,625.01; neither applies.) Line 18 is the sum of
    # lines 1, 14 and 16, 0 + 0 + 1,402.76, line 21 and T1 line 47900 are 1,402.76; the total
    # credits are 4800 + 0 + 1,402.76 = 6,202.76 and line 167 is 5,844.50 - 6,202.76 = -358.26, a
    # refund.
    worksheet = compute(
        "48000",
        "0",
        "0",
        "0",
        "8640",
        "0",
        "0",
        income_tax_deducted="4800",
        political_contributions="3000",
    )

    assert worksheet.get(NET_INCOME).value == D("47555.00")
    assert worksheet.get(ONTARIO_TAX_AFTER_FOOD_CREDIT).value == D("1484.56")
    assert worksheet.get(ONTARIO_TAX).value == D("1934.56")
    assert worksheet.get(TOTAL_PAYABLE).value == D("5844.50")
    assert worksheet.get(ontario.POLITICAL_CONTRIBUTIONS).value == D("3000")
    assert worksheet.get(ontario.POLITICAL_CREDIT_COLUMN_3_LINE_2).value == D("1666.82")
    assert worksheet.get(ontario.POLITICAL_CREDIT_COLUMN_3_LINE_3).value == D("1333.18")
    assert worksheet.get(ontario.POLITICAL_CREDIT_COLUMN_3_LINE_5).value == D("444.35")
    assert worksheet.get(ontario.POLITICAL_CREDIT_COLUMN_3_LINE_6).value == D("958.41")
    assert worksheet.get(ontario.POLITICAL_CREDIT_COLUMN_3_LINE_7).value == D("1402.76")
    assert worksheet.get(ontario.POLITICAL_CREDIT_COLUMN_1_LINE_7).value == D("2250.00")
    assert worksheet.get(ontario.POLITICAL_CREDIT_COLUMN_2_LINE_7).value == D("1625.01")
    assert worksheet.get(ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM).value == D("1402.76")
    assert worksheet.get(ontario.POLITICAL_CREDIT).value == D("1402.76")
    assert worksheet.get(ONTARIO_CREDITS_SUBTOTAL).value == D("1402.76")
    assert worksheet.get(ONTARIO_CREDITS).value == D("1402.76")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("1402.76")
    assert worksheet.get(TOTAL_CREDITS).value == D("6202.76")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-358.26")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "political_credit_column_3_line_3: political_contributions 3000 "
        "less political_credit_column_3_line_2 1666.82, not below 0 = 1333.18"
    ) in rendered
    assert (
        "political_credit_column_3_line_5: 33.33% of political_credit_column_3_line_3 1333.18 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "political_credit_column_3_line_7: political_credit_column_3_line_5 444.35 "
        "+ political_credit_column_3_line_6 958.41 = 1402.76"
    ) in rendered
    assert (
        "political_credit_before_maximum: political_credit_column_3_line_7 1402.76, "
        "chosen as political_contributions is 3000"
    ) in rendered
    assert (
        "political_credit: lesser of political_credit_before_maximum 1402.76 and 1666.82 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "ontario_credits_subtotal: fertility_credit 0 + seniors_care_credit 0 "
        "+ seniors_transit_credit 0 "
        "+ political_credit 1402.76 + flow_through_share_credit 0 = 1402.76"
    ) in rendered
    assert (
        "total_credits: income_tax_deducted 4800 + refundable_medical_expense_supplement 0 "
        "+ canada_workers_benefit 0 "
        "+ part_xii_2_tax_credit 0 + employee_and_partner_gst_hst_rebate 0 "
        "+ educator_school_supply_credit 0 + journalism_labour_tax_credit 0 "
        "+ tax_paid_by_instalments 0 + provincial_credits 1402.76 = 6202.76"
    ) in rendered


@pytest.mark.parametrize(
    ("contributions", "column", "credit"),
    [
        ("0", 1, "0.00"),
        ("300", 1, "225.00"),
        ("500.05", 1, "375.04"),
        ("500.06", 2, "375.04"),
        ("1000", 2, "625.01"),
        ("1666.82", 2, "958.42"),
        ("1666.83", 3, "958.41"),
        ("3000", 3, "1402.76"),
        ("3793", 3, "1666.82"),
        ("4000", 3, "1666.82"),
    ],
)
def test_the_credit_is_the_applicable_columns_line_7_at_most_1666_82(
    contributions: str, column: int, credit: str
) -> None:
    worksheet = compute(
        "48000", "0", "0", "0", "8640", "0", "0", political_contributions=contributions
    )

    (picked,) = [
        line
        for line in worksheet.trace
        if isinstance(line, ChosenByRangeLine)
        and line.output == ontario.POLITICAL_CREDIT_BEFORE_MAXIMUM
    ]
    assert picked.chosen_kind == POLITICAL_COLUMN_LINES[column][7]
    assert worksheet.get(ontario.POLITICAL_CREDIT).value == D(credit)
    assert worksheet.get(ONTARIO_CREDITS).value == D(credit)
    assert worksheet.get(PROVINCIAL_CREDITS).value == D(credit)


def test_no_contributions_leave_the_ontario_credits_at_zero() -> None:
    # The default of 0 contributions, as for Returns A to N: column 1 applies and line 16 is 0.
    worksheet = compute("48000", "0", "0", "0", "8640", "0", "0")

    assert worksheet.get(ontario.POLITICAL_CONTRIBUTIONS).value == D("0")
    assert worksheet.get(ontario.POLITICAL_CREDIT).value == D("0")
    assert worksheet.get(ONTARIO_CREDITS).value == D("0")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("0")


def return_ae(**overrides: Any) -> Worksheet:
    """Return AE's inputs, as in `returns/2025_return_ae.yaml`: Return P's with federal ones.

    Return P's filer (employment income of 48000, the federal tax after credits of 3909.94, the
    Ontario tax of 1934.56, Ontario political contributions of 3000 and 4800 deducted) with
    federal political contributions of 1000 (T1 line 135, line 40900).
    """
    inputs: dict[str, Any] = {
        "income_tax_deducted": "4800",
        "political_contributions": "3000",
        "federal_political_contributions": "1000",
    }
    return compute("48000", "0", "0", "0", "8640", "0", "0", **{**inputs, **overrides})


def test_return_aes_federal_political_contribution_credit_is_558_33_and_lowers_the_refund() -> None:
    # Return AE is Return P with federal political contributions of 1000 (T1 line 135, line
    # 40900): the federal tax after credits is 3909.94 and the Ontario tax 1934.56, as for Return P.
    # Federal Worksheet "Line 41000": 1000 is more than 750, so column 3 applies. Line 2 is 750.00,
    # line 3 is 1000 - 750.00 = 250.00, line 5 is 250.00 x 33.33% = 83.325, rounded half-up to the
    # cent: 83.33, line 6 is the printed 475.00 and line 7 is 83.33 + 475.00 = 558.33. (Columns 1
    # and 2 are also built: column 1 line 7 is 75% x 1000 = 750.00 and column 2 line 7 is 50% x
    # 600.00 = 300.00, + 300.00 = 600.00; neither applies.) 1000 is less than the $1,275 of the
    # shortcut, so the column's 558.33 stands, at most the maximum of $650: line 41000 is 558.33.
    # Line 138 adds lines 135 and 137, 558.33 + 0, and line 139 is 3909.94 - 558.33 = 3351.61, the
    # net federal tax; the total payable is 3351.61 + 1934.56 = 5286.17 and, with total credits of
    # 4800 + 0 + 1402.76 = 6202.76 as for Return P, line 167 is 5286.17 - 6202.76 = -916.59.
    worksheet = return_ae()

    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("3909.94")
    assert worksheet.get(POLITICAL_CONTRIBUTIONS).value == D("1000")
    assert worksheet.get(POLITICAL_CREDIT_COLUMN_3_LINE_2).value == D("750.00")
    assert worksheet.get(POLITICAL_CREDIT_COLUMN_3_LINE_3).value == D("250.00")
    assert worksheet.get(POLITICAL_CREDIT_COLUMN_3_LINE_5).value == D("83.33")
    assert worksheet.get(POLITICAL_CREDIT_COLUMN_3_LINE_6).value == D("475.00")
    assert worksheet.get(POLITICAL_CREDIT_COLUMN_3_LINE_7).value == D("558.33")
    assert worksheet.get(POLITICAL_CREDIT_COLUMN_1_LINE_7).value == D("750.00")
    assert worksheet.get(POLITICAL_CREDIT_COLUMN_2_LINE_7).value == D("600.00")
    assert worksheet.get(POLITICAL_CREDIT_CHOSEN_COLUMN).value == D("558.33")
    assert worksheet.get(POLITICAL_CREDIT_SHORTCUT_THRESHOLD).value == D("1275")
    assert worksheet.get(POLITICAL_CREDIT_SHORTCUT_AMOUNT).value == D("650")
    assert worksheet.get(POLITICAL_CREDIT_BEFORE_MAXIMUM).value == D("558.33")
    assert worksheet.get(POLITICAL_CREDIT).value == D("558.33")
    assert worksheet.get(CREDITS_AGAINST_FEDERAL_TAX).value == D("558.33")
    assert worksheet.get(FEDERAL_TAX_LESS_CREDITS).value == D("3351.61")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("3351.61")
    assert worksheet.get(TOTAL_PAYABLE).value == D("5286.17")
    assert worksheet.get(ontario.POLITICAL_CREDIT).value == D("1402.76")
    assert worksheet.get(TOTAL_CREDITS).value == D("6202.76")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-916.59")
    assert worksheet.get(REFUND).value == D("916.59")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "political_credit_column_3_line_3: political_contributions 1000 "
        "less political_credit_column_3_line_2 750, not below 0 = 250"
    ) in rendered
    assert (
        "political_credit_column_3_line_5: 33.33% of political_credit_column_3_line_3 250 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "political_credit_column_3_line_7: political_credit_column_3_line_5 83.33 "
        "+ political_credit_column_3_line_6 475 = 558.33"
    ) in rendered
    assert (
        "political_credit_chosen_column: political_credit_column_3_line_7 558.33, "
        "chosen as political_contributions is 1000"
    ) in rendered
    assert (
        "political_credit_before_maximum: political_credit_chosen_column 558.33, "
        "chosen as political_credit_shortcut_threshold is 1275"
    ) in rendered
    assert (
        "political_credit: lesser of political_credit_before_maximum 558.33 and 650 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "credits_against_federal_tax: political_credit 558.33 "
        "+ labour_sponsored_funds_credit 0 = 558.33"
    ) in rendered
    assert (
        "federal_tax_less_credits: federal_tax_with_itc_recapture 3909.94 "
        "less credits_against_federal_tax 558.33, not below 0 = 3351.61"
    ) in rendered


@pytest.mark.parametrize(
    ("contributions", "column", "credit"),
    [
        # The acceptance figures.
        ("0", 1, "0.00"),
        ("400", 1, "300.00"),
        ("750", 2, "475.00"),
        ("1000", 3, "558.33"),
        ("1275", None, "650"),
        ("5000", None, "650"),
        # The ends of the columns: column 1 line 7 at 400 is 300.00; a cent over, column 2 line 5
        # is 0.01 x 50% = 0.005, up to 0.01; a cent over 750, column 3 line 5 is 0.003333, down to
        # 0.00.
        ("400.01", 2, "300.01"),
        ("750.01", 3, "475.00"),
        # A cent under the $1,275: column 3 line 3 is 524.99, line 5 is 174.9792, down to 174.98.
        ("1274.99", 3, "649.98"),
        ("1275.01", None, "650"),
    ],
)
def test_line_41000_is_the_applicable_column_or_the_shortcut_at_most_650(
    contributions: str, column: int | None, credit: str
) -> None:
    worksheet = return_ae(federal_political_contributions=contributions)

    (chosen,) = [
        line
        for line in worksheet.trace
        if isinstance(line, ChosenByRangeLine) and line.output == POLITICAL_CREDIT_BEFORE_MAXIMUM
    ]
    if column is None:
        assert chosen.chosen_kind == POLITICAL_CREDIT_SHORTCUT_AMOUNT
    else:
        assert chosen.chosen_kind == POLITICAL_CREDIT_CHOSEN_COLUMN
        (column_pick,) = [
            line
            for line in worksheet.trace
            if isinstance(line, ChosenByRangeLine) and line.output == POLITICAL_CREDIT_CHOSEN_COLUMN
        ]
        assert column_pick.chosen_kind == FEDERAL_POLITICAL_COLUMN_LINES[column][7]
    assert worksheet.get(POLITICAL_CREDIT).value == D(credit)
    assert worksheet.get(CREDITS_AGAINST_FEDERAL_TAX).value == D(credit)


def test_the_federal_credit_does_not_change_the_ontario_credit() -> None:
    # Ontario contributions of 0 leave ON479 line 16 at 0, whatever the federal contributions.
    worksheet = return_ae(political_contributions="0")

    assert worksheet.get(POLITICAL_CREDIT).value == D("558.33")
    assert worksheet.get(ontario.POLITICAL_CREDIT).value == D("0")
    assert worksheet.get(ontario.ONTARIO_CREDITS).value == D("0")
    assert worksheet.get(TOTAL_CREDITS).value == D("4800")


def test_line_138_adds_the_political_credit_and_the_labour_sponsored_funds_credit() -> None:
    # 558.33 + 600.00 (15% of a net cost of 4000), in line order; line 139 is 3909.94 - 1158.33.
    worksheet = return_ae(labour_sponsored_funds_net_cost="4000")

    assert worksheet.get(LABOUR_SPONSORED_FUNDS_CREDIT).value == D("600.00")
    assert worksheet.get(CREDITS_AGAINST_FEDERAL_TAX).value == D("1158.33")
    assert worksheet.get(FEDERAL_TAX_LESS_CREDITS).value == D("2751.61")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "credits_against_federal_tax: political_credit 558.33 "
        "+ labour_sponsored_funds_credit 600 = 1158.33"
    ) in rendered


def test_a_credit_above_the_federal_tax_leaves_zero_on_line_139() -> None:
    # Employment income of 10000 leaves the federal tax after credits at 0; contributions of 5000
    # give the credit of 650, which is more than that: line 139 is 0, not -650, and it is lost.
    worksheet = compute(
        "10000", "0", "0", "0", "1800", "0", "0", federal_political_contributions="5000"
    )

    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("0")
    assert worksheet.get(POLITICAL_CREDIT).value == D("650")
    assert worksheet.get(CREDITS_AGAINST_FEDERAL_TAX).value == D("650")
    assert worksheet.get(FEDERAL_TAX_LESS_CREDITS).value == D("0")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("0")


def return_t(
    *,
    income_tax_deducted: str = "4929.83",
    part_xii_2_tax_credit: str = "50",
    employee_and_partner_gst_hst_rebate: str = "150",
    educator_supplies_expenses: str = "1200",
    journalism_labour_tax_credit: str = "75",
    tax_paid_by_instalments: str = "2000",
    opportunities_fund_donation: str = "100",
) -> Worksheet:
    """Return T's inputs, as in `returns/2025_return_t.yaml`: Return C's with the Step 6 lines.

    Employment income of 50000 gives a total payable of 6454.83 and no Canada workers benefit. The
    Part XII.2 credit (45600) is 50, the GST/HST rebate (45700) 150, the supplies paid (46800)
    1200, the journalism labour credit (47555) 75 and the instalments (47600) 2000; the income tax
    deducted (43700) of 4929.83 makes the refund (48400) 1000.00, of which 100 is donated (46500).
    """
    return compute(
        "50000",
        "0",
        "0",
        "0",
        "9000",
        "0",
        "0",
        income_tax_deducted=income_tax_deducted,
        part_xii_2_tax_credit=part_xii_2_tax_credit,
        employee_and_partner_gst_hst_rebate=employee_and_partner_gst_hst_rebate,
        educator_supplies_expenses=educator_supplies_expenses,
        journalism_labour_tax_credit=journalism_labour_tax_credit,
        tax_paid_by_instalments=tax_paid_by_instalments,
        opportunities_fund_donation=opportunities_fund_donation,
    )


def test_return_ts_lines_46800_and_46900_are_1000_and_250() -> None:
    # Line 46800, the supplies paid, is 1200: it counts as 1000, the maximum, and line 46900 is
    # 1000 x 25% = 250.00.
    worksheet = return_t()

    assert worksheet.get(EDUCATOR_SUPPLIES_EXPENSES).value == D("1200")
    assert worksheet.get(EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM).value == D("1000")
    assert worksheet.get(EDUCATOR_SCHOOL_SUPPLY_CREDIT).value == D("250.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "educator_supplies_expenses_at_most_maximum: lesser of educator_supplies_expenses 1200 "
        "and 1000 (half-up to 0.01)"
    ) in rendered
    assert (
        "educator_school_supply_credit: 25% of educator_supplies_expenses_at_most_maximum 1000 "
        "(half-up to 0.01)"
    ) in rendered


def test_return_ts_total_credits_add_lines_150_to_165_in_line_order() -> None:
    # 4929.83 (43700) + 0 (45300, the benefit) + 50 (45600) + 150 (45700) + 250.00 (46900) + 75
    # (47555) + 2000 (47600) + 0 (47900) = 7454.83: 2525 more than the tax deducted, the added
    # credits being 50 + 150 + 250 + 75 + 2000.
    worksheet = return_t()

    assert worksheet.get(CANADA_WORKERS_BENEFIT).value == D("0")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("0")
    assert worksheet.get(TOTAL_CREDITS).value == D("7454.83")
    assert worksheet.get(TOTAL_CREDITS).value - worksheet.get(INCOME_TAX_DEDUCTED).value == D(
        "2525.00"
    )
    (line,) = [
        line
        for line in worksheet.trace
        if isinstance(line, SumLine) and line.output == TOTAL_CREDITS
    ]
    assert line.parts == (
        (INCOME_TAX_DEDUCTED, D("4929.83")),
        (REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT, D("0.00")),
        (CANADA_WORKERS_BENEFIT, D("0")),
        (PART_XII_2_TAX_CREDIT, D("50")),
        (EMPLOYEE_AND_PARTNER_GST_HST_REBATE, D("150")),
        (EDUCATOR_SCHOOL_SUPPLY_CREDIT, D("250.00")),
        (JOURNALISM_LABOUR_TAX_CREDIT, D("75")),
        (TAX_PAID_BY_INSTALMENTS, D("2000")),
        (PROVINCIAL_CREDITS, D("0")),
    )
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "total_credits: income_tax_deducted 4929.83 + refundable_medical_expense_supplement 0 "
        "+ canada_workers_benefit 0 "
        "+ part_xii_2_tax_credit 50 + employee_and_partner_gst_hst_rebate 150 "
        "+ educator_school_supply_credit 250 + journalism_labour_tax_credit 75 "
        "+ tax_paid_by_instalments 2000 + provincial_credits 0 = 7454.83"
    ) in rendered


def test_return_ts_refund_is_1000_and_the_net_refund_after_a_donation_of_100_is_900() -> None:
    # Line 167 is 6454.83 - 7454.83 = -1000.00, negative so a refund, entered on line 48400 as a
    # positive 1000.00; the opportunities fund page's line 1 is that, line 2 (46500) is 100 and
    # line 3 (46600) is 900.00.
    worksheet = return_t()

    assert worksheet.get(TOTAL_PAYABLE).value == D("6454.83")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-1000.00")
    assert worksheet.get(REFUND).value == D("1000.00")
    assert worksheet.get(ontario.REFUND_BEFORE_DONATION).value == D("1000.00")
    assert worksheet.get(ontario.OPPORTUNITIES_FUND_DONATION).value == D("100")
    assert worksheet.get(ontario.NET_REFUND).value == D("900.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "refund: total_credits 7454.83 less total_payable 6454.83, not below 0 = 1000"
    ) in rendered
    assert "refund_before_donation: refund 1000 = 1000" in rendered
    assert (
        "net_refund: refund_before_donation 1000 less opportunities_fund_donation 100 = 900"
    ) in rendered


def test_a_balance_owing_gives_a_refund_of_zero_and_a_net_refund_of_zero() -> None:
    # Return T with 3929.82 deducted, 0.01 short of the total payable once the 2525.00 of other
    # credits are added: line 167 is +0.01 (line 48500), so line 48400 is 0
    # and the page's line 1 is 0; with no donation line 3 is 0.
    worksheet = return_t(income_tax_deducted="3929.82", opportunities_fund_donation="0")

    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("0.01")
    assert worksheet.get(REFUND).value == D("0")
    assert worksheet.get(ontario.REFUND_BEFORE_DONATION).value == D("0")
    assert worksheet.get(ontario.NET_REFUND).value == D("0")


def test_total_credits_equal_to_the_total_payable_give_a_refund_of_zero() -> None:
    worksheet = return_t(income_tax_deducted="3929.83", opportunities_fund_donation="0")

    assert worksheet.get(TOTAL_CREDITS).value == D("6454.83")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("0.00")
    assert worksheet.get(REFUND).value == D("0")


def test_donating_the_whole_refund_leaves_a_net_refund_of_zero() -> None:
    worksheet = return_t(opportunities_fund_donation="1000.00")

    assert worksheet.get(ontario.NET_REFUND).value == D("0.00")


def test_each_credit_line_enters_the_total_credits_once() -> None:
    # Distinct figures for each line, so a line left out or added twice changes the total:
    # 1 (43700) + 2 (45600) + 4 (45700) + 200.00 (46900, 25% of the 800 paid) + 8 (47555) + 16
    # (47600) = 231.00.
    worksheet = return_t(
        income_tax_deducted="1",
        part_xii_2_tax_credit="2",
        employee_and_partner_gst_hst_rebate="4",
        educator_supplies_expenses="800",
        journalism_labour_tax_credit="8",
        tax_paid_by_instalments="16",
        opportunities_fund_donation="0",
    )

    assert worksheet.get(EDUCATOR_SUPPLIES_EXPENSES_AT_MOST_MAXIMUM).value == D("800")
    assert worksheet.get(EDUCATOR_SCHOOL_SUPPLY_CREDIT).value == D("200.00")
    assert worksheet.get(TOTAL_CREDITS).value == D("231.00")


@pytest.mark.parametrize(
    ("supplies_paid", "credit"),
    [
        ("0", "0"),
        ("800", "200.00"),
        ("1000", "250.00"),
        ("1000.01", "250.00"),
        ("1200", "250.00"),
        ("100000", "250.00"),
        # 0.02 x 25% = 0.005, a tie, rounded half-up to 0.01.
        ("0.02", "0.01"),
    ],
)
def test_line_46900_is_25_percent_of_line_46800_at_most_1000(
    supplies_paid: str, credit: str
) -> None:
    worksheet = return_t(educator_supplies_expenses=supplies_paid)

    assert worksheet.get(EDUCATOR_SCHOOL_SUPPLY_CREDIT).value == D(credit)


def test_the_new_lines_do_not_change_a_return_that_does_not_take_them() -> None:
    # Return A's balance owing is unchanged: 25897.15 less 25000 with every new line 0.
    worksheet = return_a()

    assert worksheet.get(TOTAL_CREDITS).value == D("25000")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("897.15")
    assert worksheet.get(REFUND).value == D("0")
    assert worksheet.get(ontario.NET_REFUND).value == D("0")


def return_v(
    *,
    income_tax_deducted: str = "6929.83",
    opportunities_fund_donation: str = "100",
    itc_recapture_expenditure_at_15_percent: str = "2000",
    itc_recapture_expenditure_at_20_percent: str = "500",
    labour_sponsored_funds_net_cost: str = "4000",
    advanced_canada_workers_benefit: str = "300",
    resp_aips_received_part_a: str = "0",
    resp_aips_rrsp_contributions: str = "0",
    resp_aips_reduction_used_in_previous_years: str = "0",
    resp_aips_received_part_b: str = "10000",
    resp_aips_part_a_applies: int = 0,
    rl_10_labour_sponsored_fund_amount: str = "150",
) -> Worksheet:
    """Return V's inputs, as in `returns/2025_return_v.yaml`: Return T's with the special lines.

    Return T's filer (employment income of 50000, the federal tax after credits of 4177.93, the
    Ontario tax of 2276.90 and the Step 6 credits of 2525.00 besides the tax deducted) with the
    recapture of an investment tax credit on 2000 at 15% and 500 at 20% (line 131, 400.00), a net
    cost of 4000 of labour-sponsored fund shares (line 41400, 600.00), the advanced Canada workers
    benefit of 300 (line 41500) and special taxes (line 41800) of 2000.00 from Form T1172 Part B
    on 10000 of AIPs and 150 from the RL-10 slip. The net federal tax (line 42000) is 6427.93, the
    total payable 8704.83 and, with 6929.83 deducted, the refund (line 48400) is 750.00.
    """
    return compute(
        "50000",
        "0",
        "0",
        "0",
        "9000",
        "0",
        "0",
        income_tax_deducted=income_tax_deducted,
        part_xii_2_tax_credit="50",
        employee_and_partner_gst_hst_rebate="150",
        educator_supplies_expenses="1200",
        journalism_labour_tax_credit="75",
        tax_paid_by_instalments="2000",
        opportunities_fund_donation=opportunities_fund_donation,
        itc_recapture_expenditure_at_15_percent=itc_recapture_expenditure_at_15_percent,
        itc_recapture_expenditure_at_20_percent=itc_recapture_expenditure_at_20_percent,
        labour_sponsored_funds_net_cost=labour_sponsored_funds_net_cost,
        advanced_canada_workers_benefit=advanced_canada_workers_benefit,
        resp_aips_received_part_a=resp_aips_received_part_a,
        resp_aips_rrsp_contributions=resp_aips_rrsp_contributions,
        resp_aips_reduction_used_in_previous_years=resp_aips_reduction_used_in_previous_years,
        resp_aips_received_part_b=resp_aips_received_part_b,
        resp_aips_part_a_applies=resp_aips_part_a_applies,
        rl_10_labour_sponsored_fund_amount=rl_10_labour_sponsored_fund_amount,
    )


def test_return_vs_line_41400_is_600_for_a_net_cost_of_4000() -> None:
    # Line 41300 is 4000: 15% is 600.00, below the maximum of 750, so line 41400 is 600.00.
    worksheet = return_v()

    assert worksheet.get(LABOUR_SPONSORED_FUNDS_NET_COST).value == D("4000")
    assert worksheet.get(LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM).value == D("600.00")
    assert worksheet.get(LABOUR_SPONSORED_FUNDS_CREDIT).value == D("600.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "labour_sponsored_funds_credit_before_maximum: 15% of labour_sponsored_funds_net_cost 4000 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "labour_sponsored_funds_credit: lesser of labour_sponsored_funds_credit_before_maximum 600 "
        "and 750 (half-up to 0.01)"
    ) in rendered


def test_a_net_cost_of_6000_gives_900_capped_at_750() -> None:
    worksheet = return_v(labour_sponsored_funds_net_cost="6000")

    assert worksheet.get(LABOUR_SPONSORED_FUNDS_CREDIT_BEFORE_MAXIMUM).value == D("900.00")
    assert worksheet.get(LABOUR_SPONSORED_FUNDS_CREDIT).value == D("750.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "labour_sponsored_funds_credit: lesser of labour_sponsored_funds_credit_before_maximum 900 "
        "and 750 (half-up to 0.01)"
    ) in rendered


@pytest.mark.parametrize(
    ("net_cost", "credit"),
    [
        ("0", "0"),
        ("4000", "600.00"),
        # 4999.90 x 15% = 749.985, a tie, rounded half-up to 749.99, below the maximum.
        ("4999.90", "749.99"),
        # 5000 x 15% is 750.00 exactly, the net cost at which the maximum starts.
        ("5000", "750.00"),
        ("5000.01", "750.00"),
        ("6000", "750.00"),
        ("100000", "750.00"),
        # 0.10 x 15% = 0.015, a tie, rounded half-up to 0.02.
        ("0.10", "0.02"),
    ],
)
def test_line_41400_is_15_percent_of_line_41300_at_most_750(net_cost: str, credit: str) -> None:
    worksheet = return_v(labour_sponsored_funds_net_cost=net_cost)

    assert worksheet.get(LABOUR_SPONSORED_FUNDS_CREDIT).value == D(credit)


def test_return_vs_recapture_is_300_plus_100_and_adds_to_the_federal_tax_on_line_132() -> None:
    # T2038(IND) Part C: amount 1 is 2000 x 0.15 = 300.00, amount 2 is 500 x 0.20 = 100.00 and
    # amount 3, line 131, is 400.00; line 132 is line 126 (4177.93) plus it, 4577.93.
    worksheet = return_v()

    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("4177.93")
    assert worksheet.get(ITC_RECAPTURE_AT_15_PERCENT).value == D("300.00")
    assert worksheet.get(ITC_RECAPTURE_AT_20_PERCENT).value == D("100.00")
    assert worksheet.get(ITC_RECAPTURE).value == D("400.00")
    assert worksheet.get(FEDERAL_TAX_WITH_ITC_RECAPTURE).value == D("4577.93")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "itc_recapture_at_15_percent: 15% of itc_recapture_expenditure_at_15_percent 2000 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "itc_recapture_at_20_percent: 20% of itc_recapture_expenditure_at_20_percent 500 "
        "(half-up to 0.01)"
    ) in rendered
    assert (
        "itc_recapture: itc_recapture_at_15_percent 300 + itc_recapture_at_20_percent 100 = 400"
    ) in rendered
    assert (
        "federal_tax_with_itc_recapture: federal_tax_after_credits 4177.93 + itc_recapture 400 "
        "= 4577.93"
    ) in rendered


def test_each_recapture_rate_applies_to_its_own_expenditure() -> None:
    # Distinct figures, so an expenditure at the wrong rate changes the total: 1000 x 0.15 =
    # 150.00 and 3000 x 0.20 = 600.00, not 1000 x 0.20 + 3000 x 0.15 = 650.00.
    worksheet = return_v(
        itc_recapture_expenditure_at_15_percent="1000",
        itc_recapture_expenditure_at_20_percent="3000",
    )

    assert worksheet.get(ITC_RECAPTURE_AT_15_PERCENT).value == D("150.00")
    assert worksheet.get(ITC_RECAPTURE_AT_20_PERCENT).value == D("600.00")
    assert worksheet.get(ITC_RECAPTURE).value == D("750.00")


def test_no_expenditure_leaves_line_132_at_line_126() -> None:
    worksheet = return_v(
        itc_recapture_expenditure_at_15_percent="0", itc_recapture_expenditure_at_20_percent="0"
    )

    assert worksheet.get(ITC_RECAPTURE).value == D("0")
    assert worksheet.get(FEDERAL_TAX_WITH_ITC_RECAPTURE).value == D("4177.93")


def test_return_vs_credit_comes_off_line_132_and_line_139_is_3977_93() -> None:
    # Line 138 (41600) is line 137 (41400) alone, 600.00; line 139 (41700) is line 134, which
    # carries line 132 (4577.93), less it: 3977.93.
    worksheet = return_v()

    assert worksheet.get(CREDITS_AGAINST_FEDERAL_TAX).value == D("600.00")
    assert worksheet.get(FEDERAL_TAX_LESS_CREDITS).value == D("3977.93")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "credits_against_federal_tax: political_credit 0 + labour_sponsored_funds_credit 600 = 600"
    ) in rendered
    assert (
        "federal_tax_less_credits: federal_tax_with_itc_recapture 4577.93 "
        "less credits_against_federal_tax 600, not below 0 = 3977.93"
    ) in rendered


def test_a_credit_above_the_federal_tax_with_the_recapture_leaves_zero_on_line_139() -> None:
    # Employment income of 10000 leaves the federal tax after credits at 0 (see the credit larger
    # than the tax above); a recapture of 500 x 0.20 = 100.00 makes line 132 100.00, and the
    # credit of 6000 x 15% = 900.00, at most 750.00, is more than that: line 139 is 0, not
    # -650.00, and the unused credit is lost.
    worksheet = compute(
        "10000",
        "0",
        "0",
        "0",
        "1800",
        "0",
        "0",
        itc_recapture_expenditure_at_20_percent="500",
        labour_sponsored_funds_net_cost="6000",
    )

    assert worksheet.get(FEDERAL_TAX_AFTER_CREDITS).value == D("0")
    assert worksheet.get(ITC_RECAPTURE).value == D("100.00")
    assert worksheet.get(FEDERAL_TAX_WITH_ITC_RECAPTURE).value == D("100.00")
    assert worksheet.get(LABOUR_SPONSORED_FUNDS_CREDIT).value == D("750.00")
    assert worksheet.get(FEDERAL_TAX_LESS_CREDITS).value == D("0")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("0")


def test_return_vs_t1172_part_b_on_10000_of_aips_is_2000_on_line_13_and_line_41800() -> None:
    # Part A does not apply (the count is 0): line 13 is line 11 (10000) x 20% = 2000.00, the
    # amount for line 41800; the RL-10 amount of 150 is added: 2150.00.
    worksheet = return_v()

    assert worksheet.get(RESP_AIPS_RECEIVED_PART_B).value == D("10000")
    assert worksheet.get(RESP_AIPS_PART_B_TAX).value == D("2000.00")
    assert worksheet.get(RESP_AIPS_PART_A_APPLIES).value == 0
    assert worksheet.get(RESP_AIPS_ADDITIONAL_TAX).value == D("2000.00")
    assert worksheet.get(RL_10_LABOUR_SPONSORED_FUND_AMOUNT).value == D("150")
    assert worksheet.get(SPECIAL_TAXES).value == D("2150.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "resp_aips_part_b_tax: 20% of resp_aips_received_part_b 10000 (half-up to 0.01)"
    ) in rendered
    assert (
        "resp_aips_additional_tax: resp_aips_part_b_tax 2000, chosen as resp_aips_part_a_applies "
        "is 0"
    ) in rendered
    assert (
        "special_taxes: resp_aips_additional_tax 2000 + rl_10_labour_sponsored_fund_amount 150 "
        "= 2150"
    ) in rendered


def test_part_a_is_not_applicable_so_its_lines_are_computed_on_figures_of_0() -> None:
    # Return V enters 0 on lines 1, 2 and 5: line 3 is 0, line 4 is 50,000.00, line 6 is
    # 50,000.00 less 0, line 7 is the lesser of 0 and 50,000.00, line 8 is 0 less 0 and line 10
    # is 0.00.
    worksheet = return_v()

    assert worksheet.get(RESP_AIPS_CONTRIBUTIONS_COUNTED).value == D("0")
    assert worksheet.get(RESP_AIPS_LIFETIME_LIMIT).value == D("50000.00")
    assert worksheet.get(RESP_AIPS_LIMIT_REMAINING).value == D("50000.00")
    assert worksheet.get(RESP_AIPS_REDUCTION).value == D("0")
    assert worksheet.get(RESP_AIPS_SUBJECT_TO_TAX).value == D("0")
    assert worksheet.get(RESP_AIPS_PART_A_TAX).value == D("0.00")


def test_a_count_of_1_takes_part_a_and_line_10_for_line_41800() -> None:
    # Part A: 10000 of AIPs (line 1) and 4000 contributed to an RRSP and deducted (line 2): line
    # 3 is 4000, line 4 50,000.00, line 6 50,000.00 less the 0 used before, line 7 the lesser of
    # 4000 and 50,000.00, line 8 10000 - 4000 = 6000 and line 10 6000 x 20% = 1200.00. Part B's
    # 2000.00 is not the one for line 41800 now.
    worksheet = return_v(
        resp_aips_received_part_a="10000",
        resp_aips_rrsp_contributions="4000",
        resp_aips_part_a_applies=1,
    )

    assert worksheet.get(RESP_AIPS_CONTRIBUTIONS_COUNTED).value == D("4000")
    assert worksheet.get(RESP_AIPS_LIFETIME_LIMIT).value == D("50000.00")
    assert worksheet.get(RESP_AIPS_LIMIT_REMAINING).value == D("50000.00")
    assert worksheet.get(RESP_AIPS_REDUCTION).value == D("4000")
    assert worksheet.get(RESP_AIPS_SUBJECT_TO_TAX).value == D("6000")
    assert worksheet.get(RESP_AIPS_PART_A_TAX).value == D("1200.00")
    assert worksheet.get(RESP_AIPS_PART_B_TAX).value == D("2000.00")
    assert worksheet.get(RESP_AIPS_ADDITIONAL_TAX).value == D("1200.00")
    assert worksheet.get(SPECIAL_TAXES).value == D("1350.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "resp_aips_contributions_counted: lesser of resp_aips_received_part_a 10000 "
        "and resp_aips_rrsp_contributions 4000 = 4000"
    ) in rendered
    assert (
        "resp_aips_reduction: lesser of resp_aips_contributions_counted 4000 "
        "and resp_aips_limit_remaining 50000 = 4000"
    ) in rendered
    assert (
        "resp_aips_subject_to_tax: resp_aips_received_part_a 10000 less resp_aips_reduction 4000 "
        "= 6000"
    ) in rendered
    assert (
        "resp_aips_part_a_tax: 20% of resp_aips_subject_to_tax 6000 (half-up to 0.01)"
    ) in rendered
    assert (
        "resp_aips_additional_tax: resp_aips_part_a_tax 1200, chosen as resp_aips_part_a_applies "
        "is 1"
    ) in rendered


@pytest.mark.parametrize(
    ("aips", "contributions", "used_before", "reduction", "subject", "tax"),
    [
        # Contributions below the AIPs and the room: the contributions reduce the AIPs.
        ("10000", "4000", "0", "4000", "6000", "1200.00"),
        # No contributions: nothing reduces the AIPs, all of them are taxed.
        ("10000", "0", "0", "0", "10000", "2000.00"),
        # Contributions above the AIPs: line 3 is the AIPs, so the whole amount is reduced.
        ("10000", "12000", "0", "10000", "0", "0.00"),
        # 48,000 of the lifetime limit used before leaves 2,000 of room, below the contributions.
        ("10000", "4000", "48000", "2000", "8000", "1600.00"),
        # The whole 50,000.00 used before leaves no room: line 6 is 0.
        ("10000", "4000", "50000", "0", "10000", "2000.00"),
        # Room of exactly the contributions: either line gives the same line 7.
        ("10000", "4000", "46000", "4000", "6000", "1200.00"),
    ],
)
def test_part_a_reduces_the_aips_by_the_lesser_of_the_contributions_and_the_lifetime_room(
    aips: str, contributions: str, used_before: str, reduction: str, subject: str, tax: str
) -> None:
    worksheet = return_v(
        resp_aips_received_part_a=aips,
        resp_aips_rrsp_contributions=contributions,
        resp_aips_reduction_used_in_previous_years=used_before,
        resp_aips_part_a_applies=1,
    )

    assert worksheet.get(RESP_AIPS_REDUCTION).value == D(reduction)
    assert worksheet.get(RESP_AIPS_SUBJECT_TO_TAX).value == D(subject)
    assert worksheet.get(RESP_AIPS_PART_A_TAX).value == D(tax)
    assert worksheet.get(RESP_AIPS_ADDITIONAL_TAX).value == D(tax)


def test_line_6_may_be_negative_as_the_form_prints_no_floor() -> None:
    # T1172 line 6 "Line 4 minus line 5" prints no "(if negative, enter "0")": 60,000 used before
    # gives -10,000.00, and line 7, the lesser of 4000 and that, is -10000.00, as the form prints:
    # line 8 is 10000 less that, 20000.00, and line 10 is 20% of it, 4000.00.
    worksheet = return_v(
        resp_aips_received_part_a="10000",
        resp_aips_rrsp_contributions="4000",
        resp_aips_reduction_used_in_previous_years="60000",
        resp_aips_part_a_applies=1,
        opportunities_fund_donation="0",
    )

    assert worksheet.get(RESP_AIPS_LIMIT_REMAINING).value == D("-10000.00")
    assert worksheet.get(RESP_AIPS_REDUCTION).value == D("-10000.00")
    assert worksheet.get(RESP_AIPS_SUBJECT_TO_TAX).value == D("20000.00")
    assert worksheet.get(RESP_AIPS_PART_A_TAX).value == D("4000.00")


@pytest.mark.parametrize("part_a_applies", [0, 1])
def test_only_the_chosen_part_is_the_additional_tax_whatever_the_other_part_holds(
    part_a_applies: int,
) -> None:
    # Part A lines give 1200.00 and Part B's line 11 gives 2000.00; the count picks one.
    worksheet = return_v(
        resp_aips_received_part_a="10000",
        resp_aips_rrsp_contributions="4000",
        resp_aips_part_a_applies=part_a_applies,
    )

    assert worksheet.get(RESP_AIPS_PART_A_TAX).value == D("1200.00")
    assert worksheet.get(RESP_AIPS_PART_B_TAX).value == D("2000.00")
    assert worksheet.get(RESP_AIPS_ADDITIONAL_TAX).value == D(
        "1200.00" if part_a_applies else "2000.00"
    )


@pytest.mark.parametrize(
    ("aips", "tax"),
    [
        ("10000", "2000.00"),
        ("0", "0"),
        # 0.02 x 20% = 0.004, rounded half-up to 0.00; 0.03 x 20% = 0.006, to 0.01.
        ("0.02", "0.00"),
        ("0.03", "0.01"),
    ],
)
def test_line_13_is_20_percent_of_line_11(aips: str, tax: str) -> None:
    worksheet = return_v(resp_aips_received_part_b=aips)

    assert worksheet.get(RESP_AIPS_PART_B_TAX).value == D(tax)


def test_return_vs_net_federal_tax_adds_lines_139_140_and_141_in_line_order() -> None:
    # 3977.93 (139) + 300 (140, the advanced Canada workers benefit) + 2150.00 (141) = 6427.93.
    worksheet = return_v()

    assert worksheet.get(ADVANCED_CANADA_WORKERS_BENEFIT).value == D("300")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("6427.93")
    (line,) = [
        line
        for line in worksheet.trace
        if isinstance(line, SumLine) and line.output == NET_FEDERAL_TAX
    ]
    assert line.parts == (
        (FEDERAL_TAX_LESS_CREDITS, D("3977.93")),
        (ADVANCED_CANADA_WORKERS_BENEFIT, D("300")),
        (SPECIAL_TAXES, D("2150.00")),
    )
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "net_federal_tax: federal_tax_less_credits 3977.93 + advanced_canada_workers_benefit 300 "
        "+ special_taxes 2150 = 6427.93"
    ) in rendered


def test_each_line_between_126_and_142_enters_the_net_federal_tax_once() -> None:
    # Distinct figures for each line, so a line left out or added twice changes the total: 4177.93
    # (126) + 3 x 0.15 = 0.45 (131 from 3) - 0.15 x 100 = 15.00 (137 from 100) + 1000 (140) + 20%
    # of 100 = 20.00 (141, Part B) + 7 (141, RL-10) = 5190.38.
    worksheet = return_v(
        itc_recapture_expenditure_at_15_percent="3",
        itc_recapture_expenditure_at_20_percent="0",
        labour_sponsored_funds_net_cost="100",
        advanced_canada_workers_benefit="1000",
        resp_aips_received_part_b="100",
        rl_10_labour_sponsored_fund_amount="7",
    )

    assert worksheet.get(ITC_RECAPTURE).value == D("0.45")
    assert worksheet.get(LABOUR_SPONSORED_FUNDS_CREDIT).value == D("15.00")
    assert worksheet.get(FEDERAL_TAX_LESS_CREDITS).value == D("4163.38")
    assert worksheet.get(SPECIAL_TAXES).value == D("27.00")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("5190.38")


def test_return_vs_total_payable_is_8704_83_and_the_refund_is_750() -> None:
    # Line 148 is 6427.93 + 2276.90 = 8704.83; the total credits are the 6929.83 deducted plus
    # 2525.00 of the Step 6 credits, 9454.83; line 167 is 8704.83 - 9454.83 = -750.00, a refund
    # of 750.00, of which 100 is donated: the net refund is 650.00.
    worksheet = return_v()

    assert worksheet.get(ONTARIO_TAX).value == D("2276.90")
    assert worksheet.get(TOTAL_PAYABLE).value == D("8704.83")
    assert worksheet.get(TOTAL_CREDITS).value == D("9454.83")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-750.00")
    assert worksheet.get(REFUND).value == D("750.00")
    assert worksheet.get(ontario.NET_REFUND).value == D("650.00")


def test_the_special_and_credit_lines_do_not_change_a_return_that_does_not_take_them() -> None:
    # Return A's balance owing is unchanged: 25897.15 less 25000 with every new line 0.
    worksheet = return_a()

    assert worksheet.get(ITC_RECAPTURE).value == D("0")
    assert worksheet.get(LABOUR_SPONSORED_FUNDS_CREDIT).value == D("0")
    assert worksheet.get(SPECIAL_TAXES).value == D("0")
    assert worksheet.get(FEDERAL_TAX_LESS_CREDITS).value == D("16951.38")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("16951.38")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("897.15")


def return_ag(**overrides: Any) -> Worksheet:
    """Return AG's inputs, as in `returns/2025_return_ag.yaml`: a retiree with a spouse.

    Other pensions and superannuation of 30000 are the whole income, so the net income is
    30000.00; the filer, born in 1960 or earlier, claims the spouse amount for a spouse of net
    income 10000 and 4900 of medical expenses (line 58769 of 4000.00), claims the Ontario seniors
    care at home tax credit and has 3000 deducted.
    """
    inputs: dict[str, Any] = {
        "other_pensions_and_superannuation": "30000",
        "born_in_1960_or_earlier": 1,
        "spouse_net_income": "10000",
        "spouses_claimed": 1,
        "medical_expenses": "4900",
        "income_tax_deducted": "3000",
        "claims_seniors_care_credit": 1,
    }
    return compute("0", "0", "0", "0", "0", "0", "0", **{**inputs, **overrides})


def test_return_ags_seniors_care_at_home_credit_is_750_and_lowers_the_refund() -> None:
    # Return AG has other pensions and superannuation of 30000 and no other income: total income
    # and net income are 30000.00, and taxable income too. Its medical expenses of 4900 (T1 line
    # 107, ON428 line 36) less the lesser of 2885 and 3% of 30000.00 (900.00) are 4000.00: ON428
    # line 41, and with no other dependants line 43 (line 58769) is 4000.00.
    # ON479 line 3 is that 4000.00; line 5 is 25% of it, 1000.00, at most 1500; line 6 is the net
    # income 30000.00 and line 7 the spouse's 10000, so line 8 is 40000.00; line 9 is 35000.00,
    # line 10 is 40000.00 - 35000.00 = 5000.00, line 12 is 5% of it, 250.00, and line 13 is
    # 1000.00 - 250.00 = 750.00, claimed once. Line 18 adds lines 1, 13, 14, 16 and 17: 0 + 750.00
    # + 0 + 0 + 0, line 21 is that 750.00 with no co-operative education credit, and so is T1 line
    # 47900. The total credits (line 166) are the 3000 deducted plus 750.00, 3750.00; the total
    # payable is the Ontario tax of 300.00 (the health premium alone, the rest taken off by the
    # credits) with no federal tax: line 167 is 300.00 - 3750.00 = -3450.00, a refund.
    worksheet = return_ag()

    assert worksheet.get(NET_INCOME).value == D("30000.00")
    assert worksheet.get(MEDICAL_CLAIM).value == D("4000.00")
    assert worksheet.get(ontario.MEDICAL_CLAIM).value == D("4000.00")
    assert worksheet.get(SENIORS_CARE_BEFORE_MAXIMUM).value == D("1000.00")
    assert worksheet.get(SENIORS_CARE_AMOUNT).value == D("1000.00")
    assert worksheet.get(SENIORS_CARE_FAMILY_NET_INCOME).value == D("40000.00")
    assert worksheet.get(SENIORS_CARE_BASE_AMOUNT).value == D("35000.00")
    assert worksheet.get(SENIORS_CARE_INCOME_OVER_BASE).value == D("5000.00")
    assert worksheet.get(SENIORS_CARE_REDUCTION).value == D("250.00")
    assert worksheet.get(SENIORS_CARE_BEFORE_CLAIM).value == D("750.00")
    assert worksheet.get(SENIORS_CARE_CREDIT).value == D("750.00")
    assert worksheet.get(ONTARIO_CREDITS_SUBTOTAL).value == D("750.00")
    assert worksheet.get(ONTARIO_CREDITS).value == D("750.00")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("750.00")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("300.00")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("0")
    assert worksheet.get(TOTAL_PAYABLE).value == D("300.00")
    assert worksheet.get(TOTAL_CREDITS).value == D("3750.00")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-3450.00")
    assert worksheet.get(REFUND).value == D("3450.00")
    assert worksheet.get(ontario.NET_REFUND).value == D("3450.00")


def test_return_ags_trace_names_each_line_of_the_seniors_care_at_home_credit() -> None:
    rendered = EnglishTraceRenderer().render_all(return_ag().trace)

    for line in (
        "seniors_care_before_maximum: 25% of medical_claim 4000 (half-up to 0.01)",
        "seniors_care_amount: lesser of seniors_care_before_maximum 1000 and 1500 "
        "(half-up to 0.01)",
        "seniors_care_family_net_income: net_income 30000 + spouse_net_income 10000 = 40000",
        "seniors_care_base_amount: credit amount 35000 (half-up to 0.01)",
        "seniors_care_income_over_base: seniors_care_family_net_income 40000 "
        "less seniors_care_base_amount 35000, not below 0 = 5000",
        "seniors_care_reduction: 5% of seniors_care_income_over_base 5000 (half-up to 0.01)",
        "seniors_care_before_claim: seniors_care_amount 1000 "
        "less seniors_care_reduction 250, not below 0 = 750",
        "seniors_care_credit: seniors_care_before_claim 750 "
        "for each of 1 claims_seniors_care_credit = 750",
        "ontario_credits_subtotal: fertility_credit 0 + seniors_care_credit 750 "
        "+ seniors_transit_credit 0 + political_credit 0 + flow_through_share_credit 0 = 750",
        "ontario_credits: ontario_credits_subtotal 750 + coop_education_credit 0 = 750",
        "provincial_credits: ontario_credits 750 = 750",
    ):
        assert line in rendered, line


def test_a_filer_who_does_not_claim_the_credit_gets_none_whatever_line_13_is() -> None:
    # The count is the caller's: the engine checks no eligibility condition. Line 13 is still
    # worked out, 750.00, but the credit is 0 and so are lines 18 and 21 and the provincial credits.
    worksheet = return_ag(claims_seniors_care_credit=0)

    assert worksheet.get(SENIORS_CARE_BEFORE_CLAIM).value == D("750.00")
    assert worksheet.get(SENIORS_CARE_CREDIT).value == D("0")
    assert worksheet.get(ONTARIO_CREDITS_SUBTOTAL).value == D("0")
    assert worksheet.get(ONTARIO_CREDITS).value == D("0")
    assert worksheet.get(PROVINCIAL_CREDITS).value == D("0")
    assert worksheet.get(TOTAL_CREDITS).value == D("3000")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("-2700.00")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "seniors_care_credit: seniors_care_before_claim 750 "
        "for each of 0 claims_seniors_care_credit = 0"
    ) in rendered


@pytest.mark.parametrize(
    ("spouse_net_income", "medical_expenses", "line_5", "line_12", "credit"),
    [
        # The acceptance figures: family net income 40000 gives 750.00; 30000 (no spouse income)
        # gives 1000.00; 70000 gives 0.
        ("10000", "4900", "1000.00", "250.00", "750.00"),
        ("0", "4900", "1000.00", "0", "1000.00"),
        ("40000", "4900", "1000.00", "1750.00", "0"),
        # Line 58769 of 8000 (medical expenses of 8900 less 900.00) gives line 5 of 1500, the
        # maximum: 25% of 8000 is 2000.00.
        ("0", "8900", "1500", "0", "1500.00"),
        ("10000", "8900", "1500", "250.00", "1250.00"),
        # A spouse's 5000 makes the family net income 35000, where nothing comes off. At 65000
        # line 12 is 5% of 30000, 1500.00, and at 65000.01 it is 1500.0005, down to 1500.00: line
        # 13 is 0 at both, whatever the spouse's net income above.
        ("5000", "8900", "1500", "0", "1500.00"),
        ("35000", "8900", "1500", "1500.00", "0"),
        ("35000.01", "8900", "1500", "1500.00", "0"),
        ("35000", "4900", "1000.00", "1500.00", "0"),
    ],
)
def test_the_credit_follows_the_family_net_income_and_the_maximum(
    spouse_net_income: str, medical_expenses: str, line_5: str, line_12: str, credit: str
) -> None:
    worksheet = return_ag(spouse_net_income=spouse_net_income, medical_expenses=medical_expenses)

    assert worksheet.get(SENIORS_CARE_AMOUNT).value == D(line_5)
    assert worksheet.get(SENIORS_CARE_REDUCTION).value == D(line_12)
    assert worksheet.get(SENIORS_CARE_CREDIT).value == D(credit)
    assert worksheet.get(ONTARIO_CREDITS).value == D(credit)


def test_line_7_is_the_spouses_net_income_that_the_spouse_amount_reads_too() -> None:
    # The same caller input as T1 line 30300 and ON428 line 58120: a spouse of net income 10000
    # takes 10000 off the spouse amount (16129 - 10000 = 6129.00; 11905 - 10000 = 1905.00) and
    # adds 10000 to ON479 line 8.
    worksheet = return_ag()

    assert worksheet.get(SPOUSE_NET_INCOME).value == D("10000")
    assert worksheet.get(SPOUSE_AMOUNT).value == D("6129.00")
    assert worksheet.get(ontario.SPOUSE_AMOUNT).value == D("1905.00")
    assert worksheet.get(SENIORS_CARE_FAMILY_NET_INCOME).value == D("40000.00")


def test_line_3_is_the_ontario_medical_claim_and_not_the_federal_one() -> None:
    # ON479 line 3 reads line 58769 of the ON428, so a figure only the ON428 changes moves it: two
    # other dependants' expenses are the same on both forms, but the Ontario per-dependant maximum
    # of 15551 is not on the T1. A dependant with expenses of 20000 and no income: 15551 on ON428,
    # 20000 on the T1.
    worksheet = return_ag(other_dependants=(("20000", "0"),))

    assert worksheet.get(MEDICAL_CLAIM).value == D("24000.00")
    assert worksheet.get(ontario.MEDICAL_CLAIM).value == D("19551.00")
    assert worksheet.get(SENIORS_CARE_BEFORE_MAXIMUM).value == D("4887.75")
    assert worksheet.get(SENIORS_CARE_AMOUNT).value == D("1500")
    assert worksheet.get(SENIORS_CARE_BEFORE_CLAIM).value == D("1250.00")


def return_ah(employment: str = "4390", union_dues: str = "0", **overrides: Any) -> Worksheet:
    """Return AH's inputs, as in `returns/2025_return_ah.yaml`, over the keyword overrides given.

    Lina, 30, resident in Canada throughout 2025: employment income of 4390 (the working income,
    exactly the $4,390 the supplement asks), other income of 15618.90 so that the net income is
    20000.00 after the enhanced CPP contributions of 8.90, and medical expenses of 6600, of which
    3% of the net income, 600.00, comes off: a medical claim (line 33200) of 6000.00.
    """
    inputs: dict[str, Any] = {
        "other_income": "15618.90",
        "medical_expenses": "6600",
        "income_tax_deducted": "500",
    }
    inputs.update(overrides)
    return compute(employment, "0", "0", "0", "0", "0", union_dues, **inputs)


def test_return_ah_claims_the_refundable_medical_expense_supplement_of_1500_on_line_45200() -> None:
    worksheet = return_ah()

    assert worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value == D("20000.00")
    assert worksheet.get(MEDICAL_CLAIM).value == D("6000.00")
    # "your employment income from lines 10100 and 10400" less lines 20700, 21200, 22900 and
    # 23100: 4390 less 0; no net self-employment income: exactly the 4,390 the worksheet asks.
    assert worksheet.get(MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME).value == D("4390")
    assert worksheet.get(MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS).value == D("4390")
    assert worksheet.get(MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS).value == D("0")
    assert worksheet.get(MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME).value == D("4390")
    assert worksheet.get(MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME).value == D("0")
    assert worksheet.get(MEDICAL_SUPPLEMENT_WORKING_INCOME).value == D("4390")
    # Lines 1 to 5 of the two columns: the filer's net income, the spouse's column 0.
    assert worksheet.get(MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3).value == D("20000.00")
    assert worksheet.get(MEDICAL_SUPPLEMENT_COLUMN_1_LINE_5).value == D("20000.00")
    assert worksheet.get(MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5).value == D("0")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_6).value == D("20000.00")
    assert worksheet.get(MEDICAL_SUPPLEMENT_INCOME_THRESHOLD).value == D("33294.00")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_8).value == D("0")
    # 21500 + 33200 = 0 + 6000.00, 25% = 1500.00, under the 1,504 maximum, no reduction.
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_11).value == D("6000.00")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_13).value == D("1500.00")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_14).value == D("1500.00")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_15).value == D("0")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_16).value == D("1500.00")
    assert worksheet.get(MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET).value == D("1500.00")
    assert worksheet.get(MEDICAL_SUPPLEMENT_IF_RESIDENT).value == D("1500.00")
    assert worksheet.get(REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT).value == D("1500.00")
    # Line 166 adds it to the income tax deducted of 500.
    assert worksheet.get(TOTAL_CREDITS).value >= D("2000.00")
    (total,) = [
        line
        for line in worksheet.trace
        if isinstance(line, SumLine) and line.output == TOTAL_CREDITS
    ]
    assert total.parts[:2] == (
        (INCOME_TAX_DEDUCTED, D("500")),
        (REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT, D("1500.00")),
    )


def test_return_ahs_trace_names_the_gate_and_the_two_counts() -> None:
    worksheet = return_ah()
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)

    assert (
        "medical_supplement_if_working_income_met: medical_supplement_line_16 1500 "
        "if medical_supplement_working_income 4390 is at least 4390 (half-up to 0.01) = 1500"
    ) in rendered
    assert (
        "medical_supplement_if_resident: medical_supplement_if_working_income_met 1500 "
        "for each of 1 resident_in_canada_throughout_2025 = 1500"
    ) in rendered
    assert (
        "refundable_medical_expense_supplement: medical_supplement_if_resident 1500 "
        "for each of 1 aged_18_or_older_at_end_of_2025 = 1500"
    ) in rendered
    assert any(
        isinstance(line, ThresholdGateLine)
        and line.output == MEDICAL_SUPPLEMENT_IF_WORKING_INCOME_MET
        for line in worksheet.trace
    )


def supplement_only_if(worksheet: Worksheet, met: bool) -> None:
    """Line 16 is positive; the supplement is it when the conditions are met and 0 otherwise."""
    line_16 = worksheet.get(MEDICAL_SUPPLEMENT_LINE_16).value
    assert line_16 > 0
    expected = line_16 if met else D("0")
    assert worksheet.get(REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT).value == expected


@pytest.mark.parametrize(
    ("net_business_income", "met"),
    [("389.99", False), ("390", True), ("390.01", True)],
)
def test_the_working_income_of_4390_or_more_includes_the_net_self_employment_income(
    net_business_income: str, met: bool
) -> None:
    # Employment income of 4000 plus net business income (line 13500): 4,389.99 does not meet
    # "must be $4,390 or more", 4,390 and 4,390.01 do.
    worksheet = return_ah("4000", net_business_income=net_business_income)

    assert worksheet.get(MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME).value == D(net_business_income)
    supplement_only_if(worksheet, met)


def test_each_of_the_five_self_employment_lines_counts_toward_the_working_income() -> None:
    worksheet = return_ah(
        "4000",
        net_business_income="100",
        net_professional_income="90",
        net_commission_income="80",
        net_farming_income="70",
        net_fishing_income="50",
    )

    assert worksheet.get(MEDICAL_SUPPLEMENT_SELF_EMPLOYMENT_INCOME).value == D("390")
    assert worksheet.get(MEDICAL_SUPPLEMENT_WORKING_INCOME).value == D("4390")
    supplement_only_if(worksheet, True)


@pytest.mark.parametrize(("wage_loss", "met"), [("0", True), ("0.01", False), ("4390", False)])
def test_wage_loss_replacement_plan_amounts_do_not_count_toward_the_working_income(
    wage_loss: str, met: bool
) -> None:
    worksheet = return_ah(wage_loss_replacement_plan_income=wage_loss)

    assert worksheet.get(MEDICAL_SUPPLEMENT_EMPLOYMENT_INCOME_LESS_WAGE_LOSS).value == D(
        "4390"
    ) - D(wage_loss)
    supplement_only_if(worksheet, met)


@pytest.mark.parametrize(
    "deduction",
    ["other_employment_expenses", "clergy_residence_deduction"],
)
@pytest.mark.parametrize(("amount", "met"), [("100", True), ("100.01", False)])
def test_lines_22900_and_23100_come_off_the_employment_income(
    deduction: str, amount: str, met: bool
) -> None:
    # Employment income of 4490 less 100 is exactly 4390; a cent more comes off and it is short.
    worksheet = return_ah("4490", **{deduction: amount})

    assert worksheet.get(MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS).value == D(amount)
    supplement_only_if(worksheet, met)


def test_the_deductions_of_lines_20700_and_21200_come_off_the_employment_income() -> None:
    # Union dues of 100 (line 21200) leave 4390 of 4490; the registered pension plan deduction
    # (line 20700) of a cent more leaves 4389.99.
    assert_met = return_ah("4490", union_dues="100")
    assert assert_met.get(MEDICAL_SUPPLEMENT_EMPLOYMENT_DEDUCTIONS).value == D("100")
    supplement_only_if(assert_met, True)
    short = return_ah("4490", union_dues="100", rpp_deduction="0.01")
    assert short.get(MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME).value == D("4389.99")
    supplement_only_if(short, False)


def test_a_negative_employment_part_is_zero_and_does_not_reduce_the_self_employment_part() -> None:
    # "(if the result is negative, consider it as "0")": 4000 less 5000 is 0, not -1000, so the
    # 4390 of net business income alone meets the condition.
    worksheet = return_ah("4000", other_employment_expenses="5000", net_business_income="4390")

    assert worksheet.get(MEDICAL_SUPPLEMENT_EMPLOYMENT_WORKING_INCOME).value == D("0")
    assert worksheet.get(MEDICAL_SUPPLEMENT_WORKING_INCOME).value == D("4390")
    supplement_only_if(worksheet, True)


@pytest.mark.parametrize(
    ("resident", "aged_18_or_older", "met"),
    [(1, 1, True), (0, 1, False), (1, 0, False), (0, 0, False)],
)
def test_the_residence_and_age_conditions_are_counts_of_one(
    resident: int, aged_18_or_older: int, met: bool
) -> None:
    worksheet = return_ah(
        resident_in_canada_throughout_2025=resident,
        aged_18_or_older_at_end_of_2025=aged_18_or_older,
    )

    supplement_only_if(worksheet, met)


def test_line_21500_alone_gives_the_supplement_without_a_medical_claim() -> None:
    # "You entered an amount on line 21500 or line 33200": line 9 of 6000 with no line 33200.
    worksheet = return_ah(medical_expenses="0", disability_supports_deduction="6000")

    assert worksheet.get(MEDICAL_CLAIM).value == D("0")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_11).value == D("6000")
    assert worksheet.get(REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT).value == D("1500.00")


def test_lines_21500_and_33200_are_added_before_the_rate() -> None:
    worksheet = return_ah(medical_expenses="1600", disability_supports_deduction="3000")

    # Line 33200: 1600 less 3% of 20000.00 is 1000.00; line 11 is 4000.00, 25% is 1000.00.
    assert worksheet.get(MEDICAL_CLAIM).value == D("1000.00")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_11).value == D("4000.00")
    assert worksheet.get(REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT).value == D("1000.00")


def test_no_amount_on_line_21500_or_line_33200_gives_no_supplement() -> None:
    worksheet = return_ah(medical_expenses="0")

    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_11).value == D("0")
    assert worksheet.get(REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT).value == D("0")


def test_the_supplement_is_at_most_1504() -> None:
    # 25% of 8000 is 2000.00, line 14 is the 1,504 maximum.
    worksheet = return_ah(medical_expenses="8600")

    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_13).value == D("2000.00")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_14).value == D("1504")
    assert worksheet.get(REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT).value == D("1504.00")


@pytest.mark.parametrize(
    ("spouse_net_income", "line_6", "supplement"),
    [
        # Line 6 adds the two columns' line 5; line 8 is line 6 over 33,294.00 and line 15 5% of it;
        # with medical expenses of 6616 line 14 is the 1,504 maximum.
        ("0", "20000.00", "1504.00"),
        ("13294", "33294.00", "1504.00"),
        ("13295", "33295.00", "1503.95"),
        ("43373", "63373.00", "0.05"),
        # "Your adjusted family net income is less than $63,374": no step of its own, as at 63,374
        # line 15 is 5% x 30,080 = 1,504.00 and line 16 is 0.
        ("43374", "63374.00", "0"),
        ("43375", "63375.00", "0"),
    ],
)
def test_the_spouses_column_is_added_to_the_adjusted_family_net_income(
    spouse_net_income: str, line_6: str, supplement: str
) -> None:
    worksheet = return_ah(
        medical_expenses="6616", spouse_net_income_before_adjustments=spouse_net_income
    )

    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_14).value == D("1504")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_6).value == D(line_6)
    assert worksheet.get(REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT).value == D(supplement)


def test_a_spouse_with_a_net_loss_shown_in_brackets_adds_nothing_to_line_6() -> None:
    # Column 2 line 1 may be negative ("if negative, show in brackets"); line 5 is "0" then.
    worksheet = return_ah(spouse_net_income_before_adjustments="-5000")

    assert worksheet.get(MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3).value == D("-5000")
    assert worksheet.get(MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5).value == D("0")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_6).value == D("20000.00")


def test_the_spouses_repayments_are_added_and_the_spouses_uccb_and_rdsp_income_taken_off() -> None:
    worksheet = return_ah(
        spouse_net_income_before_adjustments="30000",
        spouse_uccb_repayment="100",
        spouse_rdsp_income_repayment="50",
        spouse_universal_child_care_benefit="1000",
        spouse_rdsp_income="200",
    )

    # Line 2 100 + 50, line 3 30000 + 150, line 4 1000 + 200, line 5 30150 - 1200.
    assert worksheet.get(MEDICAL_SUPPLEMENT_COLUMN_2_LINE_2).value == D("150")
    assert worksheet.get(MEDICAL_SUPPLEMENT_COLUMN_2_LINE_3).value == D("30150")
    assert worksheet.get(MEDICAL_SUPPLEMENT_COLUMN_2_LINE_4).value == D("1200")
    assert worksheet.get(MEDICAL_SUPPLEMENT_COLUMN_2_LINE_5).value == D("28950")
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_6).value == D("48950.00")
    # Line 8 = 48950.00 - 33294.00 = 15656.00, line 15 = 782.80, line 16 = 1500.00 - 782.80.
    assert worksheet.get(MEDICAL_SUPPLEMENT_LINE_15).value == D("782.80")
    assert worksheet.get(REFUNDABLE_MEDICAL_EXPENSE_SUPPLEMENT).value == D("717.20")


def test_the_filers_uccb_and_rdsp_amounts_adjust_column_1() -> None:
    worksheet = return_ah(uccb_repayment="100", rdsp_income_repayment="50")

    # The repayments are deductions of line 23300 (UCCB) and a part of line 23200 caller input;
    # column 1 line 2 adds both to the net income before adjustments.
    assert worksheet.get(MEDICAL_SUPPLEMENT_COLUMN_1_LINE_3).value == (
        worksheet.get(NET_INCOME_BEFORE_ADJUSTMENTS).value + D("150")
    )
