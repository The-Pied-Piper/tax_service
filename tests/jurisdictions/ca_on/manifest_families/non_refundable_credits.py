"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.at_most import AtMost
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.times_count import TimesCount
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.amount_or_divided_by_rate import AmountOrDividedByRate
from app.jurisdictions.ca.capabilities.divided_by_rate import DividedByRate
from app.jurisdictions.ca.capabilities.foreign_non_business_tax_credit import (
    ForeignNonBusinessTaxCredit,
)
from app.jurisdictions.ca.catalog import (
    AGE_AMOUNT,
    AMOUNTS_TRANSFERRED_FROM_SPOUSE,
    BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT,
    BASIC_PERSONAL_AMOUNT,
    CANADA_EMPLOYMENT_AMOUNT,
    CANADA_TRAINING_CREDIT,
    CANADA_TRAINING_CREDIT_BASIS,
    CANADA_TRAINING_CREDIT_CLAIMED,
    CANADA_TRAINING_CREDIT_LIMIT,
    CANADA_TRAINING_CREDIT_MAXIMUM,
    CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
    CANADIAN_TUITION_AVAILABLE,
    CANADIAN_TUITION_FEES,
    CAPITAL_GAINS_DEDUCTION,
    CAPITAL_GIFT_GAINS_DEDUCTION,
    CAPITAL_GIFT_TAXABLE_GAINS,
    CAPITAL_GIFTS_LIMIT_ADDITION,
    CAPITAL_GIFTS_TOTAL,
    CAPITAL_PROPERTY_GIFTS,
    CAREGIVER_AMOUNT,
    CHARITABLE_DONATIONS,
    CHARITABLE_DONATIONS_CLAIMED,
    CHARITABLE_DONATIONS_LIMIT,
    CPP_BASE_CONTRIBUTIONS_ON_RETURN,
    CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT,
    CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
    CPP_PART_4_COMPLETED,
    CPP_PART_5_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT,
    CPP_PART_5_COMPLETED,
    CPP_PART_5_LINE_70,
    CREDIT_AMOUNTS_AT_CREDIT_RATE,
    CREDIT_AMOUNTS_SUBTOTAL,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    CURRENT_YEAR_TUITION_AVAILABLE,
    CURRENT_YEAR_TUITION_CLAIMED,
    DEPRECIABLE_GIFT_CAPITAL_COST,
    DEPRECIABLE_GIFT_NET_PROCEEDS,
    DEPRECIABLE_GIFT_PROCEEDS_OR_COST,
    DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION,
    DEPRECIABLE_GIFTS,
    DISABILITY_AMOUNT_FOR_SELF,
    DISABILITY_TRANSFERRED_AMOUNT,
    DIVIDEND_TAX_CREDIT,
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
    EI_PREMIUMS,
    EI_PREMIUMS_ON_SELF_EMPLOYMENT,
    EI_SPECIAL_BENEFITS_AGREEMENT,
    ELIGIBLE_DEPENDANT_AMOUNT,
    EMPLOYMENT_INCOME,
    EXEMPT_INCOME_DEDUCTIONS,
    FEDERAL_BASIC_TAX,
    FEDERAL_FOREIGN_TAX_CREDIT,
    FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT,
    FEDERAL_TAX_AFTER_CREDITS,
    FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT,
    FEDERAL_TAX_ON_SPLIT_INCOME,
    FEDERAL_TAX_WITH_ITC_RECAPTURE,
    FEDERAL_TAX_WITH_SPLIT_INCOME,
    FEDERAL_TUITION_AMOUNT,
    FIRST_NATIONS_ABATEMENT,
    FIRST_TIER_DONATION_CREDIT,
    FOREIGN_CHARITY_DONATIONS,
    FOREIGN_TAX_COUNTRIES,
    FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX,
    FOREIGN_TAX_CREDIT_NET_INCOME,
    FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME,
    FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS,
    FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME,
    FOREIGN_TAX_CREDIT_SHEETS,
    FOREIGN_TUITION_FEES,
    GOVERNMENT_DONATIONS,
    HIGH_INCOME_DONATION_CREDIT,
    HIGH_INCOME_DONATIONS,
    INFIRM_CHILDREN_AMOUNT,
    ITC_RECAPTURE,
    ITC_RECAPTURE_AT_15_PERCENT,
    ITC_RECAPTURE_AT_20_PERCENT,
    ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT,
    ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT,
    MEDICAL_CLAIM,
    NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    OTHER_PAYMENTS_DEDUCTION,
    QBT_CAPITAL_GAINS_DEDUCTION,
    RC381_CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
    REGULAR_RATE_DONATION_CREDIT,
    REGULAR_RATE_DONATIONS,
    SECURITY_OPTIONS_DEDUCTIONS,
    SELF_EMPLOYED_CPP_BASE_CREDIT,
    SELF_EMPLOYED_EI_PREMIUMS,
    SOCIAL_BENEFITS_REPAYMENT,
    SPOUSE_ADJUSTED_TAXABLE_INCOME,
    SPOUSE_AMOUNT,
    SPOUSE_CAREGIVER_AMOUNT,
    SPOUSE_CREDITS_USED,
    SPOUSE_DESIGNATED_TUITION,
    SPOUSE_INCOME_FOR_TRANSFER,
    SPOUSE_NOT_SEPARATED_90_DAYS,
    SPOUSE_RETURN_AGE_AMOUNT,
    SPOUSE_RETURN_BASIC_PERSONAL_AMOUNT,
    SPOUSE_RETURN_DISABILITY_AMOUNT,
    SPOUSE_RETURN_FEDERAL_BASIC_TAX,
    SPOUSE_RETURN_FEDERAL_TUITION_AMOUNT,
    SPOUSE_RETURN_INFIRM_CHILDREN_AMOUNT,
    SPOUSE_RETURN_LINE_96,
    SPOUSE_RETURN_PENSION_INCOME_AMOUNT,
    SPOUSE_RETURN_TAXABLE_INCOME,
    SPOUSE_TRANSFERABLE_AMOUNTS,
    SPOUSE_UNUSED_AMOUNTS,
    TAXABLE_INCOME,
    TAXABLE_INCOME_OVER_DONATION_THRESHOLD,
    TOP_UP_CREDITS_BASE,
    TOP_UP_EXCESS,
    TOP_UP_TAX_CREDIT,
    TOP_UP_THRESHOLD,
    TOSI_ADJUSTED_TAXABLE_INCOME,
    TOTAL_CHARITABLE_DONATIONS,
    TOTAL_SPLIT_INCOME,
    TOTAL_TUITION_AVAILABLE,
    TUITION_AVAILABLE_TO_TRANSFER,
    TUITION_CARRIED_FORWARD,
    TUITION_INCOME_BASE,
    TUITION_INCOME_LESS_CREDITS,
    TUITION_INCOME_REMAINING,
    TUITION_INCOME_WITH_TOSI,
    TUITION_TRANSFER_ELECTED,
    TUITION_TRANSFER_LIMIT,
    TUITION_TRANSFERRED,
    TUITION_TRANSFERRED_FROM_CHILD,
    UNIVERSITY_DONATIONS_OUTSIDE_CANADA,
    UNUSED_FEDERAL_TUITION,
    UNUSED_TUITION_CLAIMED,
    UNUSED_TUITION_FROM_2024,
)

INPUTS = frozenset(
    {
        # Form T2209, "the federal refundable First Nations abatement (line 44100 of your return)"
        # of note (4), and the countries of lines 1 and 2, each with lines 43100 and 43300.
        "ca/first_nations_abatement",
        "ca/foreign_tax_countries",
        "ca/itc_recapture_expenditure_at_15_percent",
        "ca/itc_recapture_expenditure_at_20_percent",
        "ca/charitable_donations",
        "ca/government_donations",
        "ca/university_donations_outside_canada",
        "ca/foreign_charity_donations",
        "ca/ecological_and_cultural_gifts",
        "ca/ecological_gifts_before_2016",
        "ca/depreciable_gift_recaptured_depreciation",
        "ca/depreciable_gift_net_proceeds",
        "ca/depreciable_gift_capital_cost",
        "ca/capital_gift_taxable_gains",
        "ca/capital_gift_gains_deduction",
        "ca/ei_special_benefits_agreement",
        "ca/canadian_tuition_fees",
        "ca/canada_training_credit_limit",
        "ca/canada_training_credit_claimed",
        "ca/foreign_tuition_fees",
        "ca/unused_tuition_from_2024",
        "ca/tuition_transfer_elected",
        "ca/tuition_transferred_from_child",
        "ca/spouse_return_age_amount",
        "ca/spouse_return_infirm_children_amount",
        "ca/spouse_return_pension_income_amount",
        "ca/spouse_return_disability_amount",
        "ca/spouse_designated_tuition",
        "ca/spouse_return_taxable_income",
        "ca/spouse_return_federal_basic_tax",
        "ca/spouse_return_basic_personal_amount",
        "ca/spouse_return_line_96",
        "ca/spouse_return_federal_tuition_amount",
        "ca/spouse_not_separated_90_days",
    }
)

OUTPUTS = frozenset({"ca/tuition_carried_forward", "ca/foreign_tax_credit_sheets"})

STEPS = {
    # T1 line 31200 "through employment (boxes 18 and 55 of all T4 slips) (maximum
    # $1,077.48)": the EI premiums, 1.64% of the employment income up to the $65,700
    # maximum insurable earnings, with no exemption (the EI premium rates and maximums,
    # 2025 federal row).
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/ei_premium"},
        consumes={"earnings": "ca/employment_income"},
        produces={"output": "ca/ei_premiums"},
    ),
    # The Canada employment amount: the lesser of the T1's cap and employment income.
    CapabilitySelection(
        name="core/capped_amount",
        params={"cap": "ca/canada_employment_amount"},
        consumes={"base": "ca/employment_income"},
        produces={"output": "ca/canada_employment_amount"},
    ),
    # T1 line 87 and line 31000, entered from Schedule 8 Part 4 line 15: Part 4 is completed only
    # when the filer reports self-employment income alone, so the amount is counted once for
    # each Part 4 completed, 1 or 0.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/self_employed_cpp_base_credit",
            "count": "ca/cpp_part_4_completed",
        },
        produces={"output": "ca/cpp_base_contributions_on_self_employment"},
    ),
    # T1 line 87 and line 31000, entered from Schedule 8 Part 5 line 70: counted once for each
    # Part 5 completed, 1 or 0. The form prints line 70 as the amount for line 31000.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/cpp_part_5_line_70",
            "count": "ca/cpp_part_5_completed",
        },
        produces={"output": "ca/cpp_part_5_base_contributions_on_self_employment"},
    ),
    # T1 line 87 and line 31000: the Part 4 amount plus the Part 5 amount; both are added when
    # both parts are marked completed, as the form leaves the choice to the filer. Plus Form RC381
    # Part 4 line 111 (the form's total, 0 with no copy; the return carries Schedule 8 or Form
    # RC381, never both).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/cpp_base_contributions_on_self_employment",
                "ca/cpp_part_5_base_contributions_on_self_employment",
                "ca/rc381_cpp_base_contributions_on_self_employment_and_other_earnings",
            ),
        },
        produces={"output": "ca/cpp_base_contributions_on_self_employment_and_other_earnings"},
    ),
    # "Enter the amount from line 9 or line 10, whichever applies, on line 31217 and line 42120
    # of your return.": Schedule 13 is completed only with an agreement with the Canada
    # Employment Insurance Commission, so line 9 is counted once for each agreement, 1 or 0, on
    # each of the two lines.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/self_employed_ei_premiums",
            "count": "ca/ei_special_benefits_agreement",
        },
        produces={"output": "ca/ei_premiums_on_self_employment"},
    ),
    # Schedule 11 line 2 "Amount from line 1" "multiplied by 50% =": line 1 and line 32000 "Eligible
    # tuition fees paid to Canadian educational institutions for 2025" is a caller input.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/canada_training_credit_rate"},
        consumes={"base": "ca/canadian_tuition_fees"},
        produces={"output": "ca/canada_training_credit_basis"},
    ),
    # Schedule 11 line 3 "Your Canada training credit limit from your latest notice of assessment
    # or reassessment", a caller input, and line 4 "Enter whichever is less: amount from line 2
    # or line 3."
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": ("ca/canada_training_credit_basis", "ca/canada_training_credit_limit")
        },
        produces={"output": "ca/canada_training_credit_maximum"},
    ),
    # Schedule 11 "Enter the Canada training credit amount that you are claiming for 2025 (cannot
    # be more than the amount on line 4)." and line 5 "Enter this amount on line 45350 of your
    # return. Your Canada training credit": the amount claimed is the filer's election, a caller
    # input, at most line 4; T1 line 156 and line 45350 "Canada training credit (CTC) (complete
    # Schedule 11)".
    CapabilitySelection(
        name="core/at_most",
        params={},
        consumes={
            "amount": "ca/canada_training_credit_claimed",
            "bound": "ca/canada_training_credit_maximum",
        },
        produces={"output": "ca/canada_training_credit"},
    ),
    # Schedule 11 line 6 "Line 1 minus line 5 =".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/canadian_tuition_fees", "less": "ca/canada_training_credit"},
        produces={"output": "ca/canadian_tuition_available"},
    ),
    # Schedule 11 line 7 and line 32001 "Eligible tuition fees paid to foreign educational
    # institutions for 2025", a caller input, and line 8 "Line 6 plus line 7 =".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/canadian_tuition_available", "ca/foreign_tuition_fees")},
        produces={"output": "ca/current_year_tuition_available"},
    ),
    # Schedule 11 line 9 "Unused federal tuition from your 2024 notice of assessment or
    # reassessment (note 1)", a caller input, and line 10 "Line 8 plus line 9 =".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/current_year_tuition_available", "ca/unused_tuition_from_2024")},
        produces={"output": "ca/total_tuition_available"},
    ),
    # Schedule 11 "Enter the amount from line 26000 of your return on line 11 if it is $57,375 or
    # less. If it is more than $57,375, enter the result of the following calculation:" and line
    # 11 "Amount from line 76 of your return divided by 14.5% =".
    CapabilitySelection(
        name="ca/amount_or_divided_by_rate",
        params={"limit": "ca/tuition_income_limit"},
        consumes={"amount": "ca/taxable_income", "dividend": "ca/federal_basic_tax"},
        produces={"output": "ca/tuition_income_base"},
    ),
    # T1 line 101 "Add lines 98 to 100. =": the credit amounts of the lines wired up to line 100
    # (line 31800), in the forms' line order, before line 102; Schedule 11 line 12 "Enter the
    # amount from line 101 of your return" reads it.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/basic_personal_amount",
                "ca/age_amount",
                "ca/spouse_amount",
                "ca/eligible_dependant_amount",
                "ca/spouse_caregiver_amount",
                "ca/caregiver_amount",
                "ca/infirm_children_amount",
                "ca/cpp_base_contributions_on_return",
                "ca/cpp_base_contributions_on_self_employment_and_other_earnings",
                "ca/ei_premiums",
                "ca/ei_premiums_on_self_employment",
                "ca/canada_employment_amount",
                "ca/disability_amount_for_self",
                "ca/disability_transferred_amount",
            )
        },
        produces={"output": "ca/credit_amounts_subtotal"},
    ),
    # Schedule 11 line 13 "Line 11 minus line 12 (if negative, enter "0") =".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/tuition_income_with_tosi", "less": "ca/credit_amounts_subtotal"},
        produces={"output": "ca/tuition_income_less_credits"},
    ),
    # Schedule 11 line 14 "Enter whichever is less amount from line 9 or line 13."
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/unused_tuition_from_2024", "ca/tuition_income_less_credits")},
        produces={"output": "ca/unused_tuition_claimed"},
    ),
    # Schedule 11 line 15 "Line 13 minus line 14 =".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/tuition_income_less_credits", "less": "ca/unused_tuition_claimed"},
        produces={"output": "ca/tuition_income_remaining"},
    ),
    # Schedule 11 line 16 "Enter whichever is less amount from line 8 or line 15."
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/current_year_tuition_available", "ca/tuition_income_remaining")},
        produces={"output": "ca/current_year_tuition_claimed"},
    ),
    # Schedule 11 line 17 "Line 14 plus line 16 Enter this amount on line 32300 of your return.
    # Your federal tuition amount =", T1 line 103 and line 32300 "Your federal tuition amount
    # (complete Schedule 11)".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/unused_tuition_claimed", "ca/current_year_tuition_claimed")},
        produces={"output": "ca/federal_tuition_amount"},
    ),
    # Schedule 11 line 18 "Amount from line 10 of the previous page", line 19 "Amount from line
    # 17 of the previous page" and line 20 "Line 18 minus line 19 Total unused federal tuition
    # amount =".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/total_tuition_available", "less": "ca/federal_tuition_amount"},
        produces={"output": "ca/unused_federal_tuition"},
    ),
    # Schedule 11 line 21 "Amount from line 8 of the previous page (maximum $5,000)".
    CapabilitySelection(
        name="core/capped_amount",
        params={"cap": "ca/tuition_transfer_maximum"},
        consumes={"base": "ca/current_year_tuition_available"},
        produces={"output": "ca/tuition_transfer_limit"},
    ),
    # Schedule 11 line 22 "Amount from line 16 of the previous page" and line 23 "minus line 22
    # (if negative, enter "0") Unused federal tuition amount available to transfer =", line 21
    # less line 22.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/tuition_transfer_limit",
            "less": "ca/current_year_tuition_claimed",
        },
        produces={"output": "ca/tuition_available_to_transfer"},
    ),
    # Schedule 11 line 24 and line 32700 "Enter the amount you are transferring to a designated
    # individual as shown on your Tuition and Enrolment Certificate (cannot be more than the
    # amount on line 23). Federal tuition amount transferred": the filer's election, a caller
    # input, at most line 23.
    CapabilitySelection(
        name="core/at_most",
        params={},
        consumes={
            "amount": "ca/tuition_transfer_elected",
            "bound": "ca/tuition_available_to_transfer",
        },
        produces={"output": "ca/tuition_transferred"},
    ),
    # Schedule 11 line 25 "Line 20 minus line 24 Unused federal tuition amount available to carry
    # forward to a future year =".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/unused_federal_tuition", "less": "ca/tuition_transferred"},
        produces={"output": "ca/tuition_carried_forward"},
    ),
    # Schedule 2 line 6 "Add lines 1 to 5. =": line 1 and line 35200 "Enter the amount from line
    # 30100 of their return.", line 2 and line 35300 "Enter the amount from line 30500 of their
    # return.", line 3 and line 35500 "Enter the amount from line 31400 of their return.
    # (maximum $2,000)", line 4 and line 35700 "Enter the amount from line 31600 of their return.
    # (Note 1)" and line 5 and line 36000 "Enter the federal amount designated to you from their
    # forms T2202, TL11A, or TL11C. (Note 2)", all of them figures from another person's return,
    # caller inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/spouse_return_age_amount",
                "ca/spouse_return_infirm_children_amount",
                "ca/spouse_return_pension_income_amount",
                "ca/spouse_return_disability_amount",
                "ca/spouse_designated_tuition",
            )
        },
        produces={"output": "ca/spouse_transferable_amounts"},
    ),
    # Schedule 2 line 7 "Enter the amount from line 26000 of their return on line 7 if it is
    # $57,375 or less. If it is more than $57,375, enter the result of the following calculation:
    # amount from line 76 of their return divided by 14.5% =": their line 26000 and their line 76
    # are caller inputs.
    CapabilitySelection(
        name="ca/amount_or_divided_by_rate",
        params={"limit": "ca/spouse_transfer_income_limit"},
        consumes={
            "amount": "ca/spouse_return_taxable_income",
            "dividend": "ca/spouse_return_federal_basic_tax",
        },
        produces={"output": "ca/spouse_income_for_transfer"},
    ),
    # Schedule 2 line 8 "Amount from line 30000 of their return", line 9 "Amount from line 96 of
    # their return" and line 10 "Amount from line 32300 of their return", caller inputs, and line
    # 11 "Add lines 8 to 10. =".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/spouse_return_basic_personal_amount",
                "ca/spouse_return_line_96",
                "ca/spouse_return_federal_tuition_amount",
            )
        },
        produces={"output": "ca/spouse_credits_used"},
    ),
    # Schedule 2 line 12 and line 36100 "Line 7 minus line 11 (if negative, enter "0") =".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/spouse_income_for_transfer", "less": "ca/spouse_credits_used"},
        produces={"output": "ca/spouse_adjusted_taxable_income"},
    ),
    # Schedule 2 line 13 "Line 6 minus line 12 (if negative, enter "0")".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/spouse_transferable_amounts",
            "less": "ca/spouse_adjusted_taxable_income",
        },
        produces={"output": "ca/spouse_unused_amounts"},
    ),
    # Schedule 2 "If you were separated because of a breakdown in your relationship for a period
    # of 90 days or more including December 31, 2025, your spouse or common-law partner cannot
    # transfer any unused amounts to you." and line 13 "Enter this amount on line 32600 of your
    # return. Federal amounts transferred from your spouse or common-law partner", T1 line 105
    # and line 32600 "Amounts transferred from your spouse or common-law partner (complete
    # Schedule 2)": line 13 is counted once when not separated and not at all when separated, a
    # caller's 1 or 0.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/spouse_unused_amounts",
            "count": "ca/spouse_not_separated_90_days",
        },
        produces={"output": "ca/amounts_transferred_from_spouse"},
    ),
    # T1 line 33500 (lines 30000, 30100, 30300, 30400, 30425, 30450, 30500, 30800, 31000, 31200,
    # 31217, 31260, 31800, 32300, 32400, 32600, 33200) and ON428 line 58800 (lines 58040, 58080,
    # 58120, 58160, 58185, 58240, 58280, 58300, 58305, 58769), in the forms' line order. T1 line
    # 113 and line 33500 is "Line 106 plus line 112", and line 112 (line 33200) follows the lines
    # that line 106 adds; ON428 line 44 and line 58800 is "Line 35 plus line 43", and line 43
    # (line 58769) follows the lines that line 35 adds. ON428 lines 58240, 58280, 58300 and 58305
    # are "Amount from line 30800 / 31000 / 31200 / 31217 of your return", so the Ontario sum
    # reads the federal kinds; it has no Canada employment amount. Lines 31000 "on self-employment
    # income and other earnings" and 31217 "on self-employment and other eligible earnings
    # (complete Schedule 13)" follow lines 30800 and 31200, as ON428's lines 58280 and 58305
    # follow its lines 58240 and 58300.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/basic_personal_amount",
                "ca/age_amount",
                "ca/spouse_amount",
                "ca/eligible_dependant_amount",
                "ca/spouse_caregiver_amount",
                "ca/caregiver_amount",
                "ca/infirm_children_amount",
                "ca/cpp_base_contributions_on_return",
                "ca/cpp_base_contributions_on_self_employment_and_other_earnings",
                "ca/ei_premiums",
                "ca/ei_premiums_on_self_employment",
                "ca/canada_employment_amount",
                "ca/disability_amount_for_self",
                "ca/disability_transferred_amount",
                "ca/federal_tuition_amount",
                "ca/tuition_transferred_from_child",
                "ca/amounts_transferred_from_spouse",
                "ca/medical_claim",
            )
        },
        produces={"output": "ca/non_refundable_credit_amounts"},
    ),
    # Schedule 9 chart for line 33700 "Gifts of capital property that is depreciable property",
    # line 4 "Enter whichever is less: amount from line 2 or line 3.": the net proceeds of
    # disposition of the property donated in 2025 (line 2) and its capital cost (line 3), caller
    # inputs for the one class and property the return claims.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": ("ca/depreciable_gift_net_proceeds", "ca/depreciable_gift_capital_cost")
        },
        produces={"output": "ca/depreciable_gift_proceeds_or_cost"},
    ),
    # Schedule 9 chart for line 33700, line 5 "Enter whichever is less: amount from line 1 or
    # line 4. Enter this amount on line 33700 of the previous page.": line 1 "Amount of
    # recaptured depreciation included on your 2025 return" is a caller input. This is the
    # previous page's line B, "Gifts of capital property that are depreciable property".
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/depreciable_gift_recaptured_depreciation",
                "ca/depreciable_gift_proceeds_or_cost",
            )
        },
        produces={"output": "ca/depreciable_gifts"},
    ),
    # Schedule 9 chart for line 33900 "Gifts of capital property", line 3 "Line 1 minus Line 2
    # Enter this amount on line 33900 on the previous page.": line 1 "Amount of current-year
    # taxable capital gains from capital property donated in 2025" and line 2 "Amount of
    # current-year capital gains deduction from capital property donated in 2025" are caller
    # inputs. This is the previous page's line C, "Gifts of capital property".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/capital_gift_taxable_gains",
            "less": "ca/capital_gift_gains_deduction",
        },
        produces={"output": "ca/capital_property_gifts"},
    ),
    # Schedule 9 line 5 "Add lines 1 to 4. Total eligible amount of charitable donations": line
    # 1 donations to registered charities and similar organizations, line 2 (line 32900)
    # donations to the Government of Canada, a province or territory and similar bodies, line 3
    # (line 33300) donations to registered universities outside Canada and line 4 (line 33400)
    # donations to the United Nations and its agencies and registered foreign charities, caller
    # inputs taken as the receipts state them, with any unused donations of the previous five
    # years that the filer chooses to claim.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/charitable_donations",
                "ca/government_donations",
                "ca/university_donations_outside_canada",
                "ca/foreign_charity_donations",
            )
        },
        produces={"output": "ca/total_charitable_donations"},
    ),
    # Schedule 9 line 6 "Enter your net income from line 23600 of your return. Line A"
    # "multiplied by 75%": 75% of the net income.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/donation_net_income_rate"},
        consumes={"base": "ca/net_income"},
        produces={"output": "ca/donation_limit_on_net_income"},
    ),
    # Schedule 9 line 7 "Amount B plus amount C Line D" "multiplied by 25%": line D is the gifts
    # of capital property that are depreciable property (line B, line 33700) plus the gifts of
    # capital property (line C, line 33900), and line 7 is 25% of it.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/depreciable_gifts", "ca/capital_property_gifts")},
        produces={"output": "ca/capital_gifts_total"},
    ),
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/capital_gifts_limit_rate"},
        consumes={"base": "ca/capital_gifts_total"},
        produces={"output": "ca/capital_gifts_limit_addition"},
    ),
    # Schedule 9 line 8 "Line 6 plus line 7".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/donation_limit_on_net_income", "ca/capital_gifts_limit_addition")},
        produces={"output": "ca/donation_limit_with_capital_gifts"},
    ),
    # Schedule 9 line 9 "Enter whichever is less: amount A or line 8. Total charitable donations
    # limit": amount A is the net income of line 6, so the 25% of the gifts of capital property
    # can raise the limit above 75% of the net income, but not above the net income itself.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/net_income", "ca/donation_limit_with_capital_gifts")},
        produces={"output": "ca/charitable_donations_limit"},
    ),
    # Schedule 9 line 10 and line 34000 "Enter whichever is less: amount from line 5 or line 9."
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/total_charitable_donations", "ca/charitable_donations_limit")},
        produces={"output": "ca/charitable_donations_claimed"},
    ),
    # Schedule 9 line 11 and line 34200 "Eligible amount of ecological gifts and cultural gifts
    # (see Guide P113)", a caller input, and line 12 "Line 10 plus line 11".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/charitable_donations_claimed", "ca/ecological_and_cultural_gifts")},
        produces={"output": "ca/donations_and_gifts_total"},
    ),
    # Schedule 9 line 13 "Enter whichever is less: amount from line 12 or $200.": the $200 is a
    # dataset, claimed whole.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/donation_first_tier_maximum"},
        consumes={},
        produces={"output": "ca/donation_first_tier_maximum"},
    ),
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/donations_and_gifts_total", "ca/donation_first_tier_maximum")},
        produces={"output": "ca/donations_first_tier"},
    ),
    # Schedule 9 line 14 "Line 12 minus line 13".
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/donations_and_gifts_total", "less": "ca/donations_first_tier"},
        produces={"output": "ca/donations_over_first_tier"},
    ),
    # Schedule 9 line 15 and line 34210 "Total ecological gifts made after February 10, 2014,
    # and before 2016 included in the amount on line 11", a caller input, and line 16 "Line 14
    # minus line 15 (if negative, enter "0")".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/donations_over_first_tier",
            "less": "ca/ecological_gifts_before_2016",
        },
        produces={"output": "ca/donations_over_first_tier_after_2016_gifts"},
    ),
    # Schedule 9 line 18 "Income threshold 253,414.00": the dataset becomes an artifact of the
    # same name.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/donation_high_income_threshold"},
        consumes={},
        produces={"output": "ca/donation_high_income_threshold"},
    ),
    # Schedule 9 line 17 "Enter your taxable income from line 26000 of your return." and line 19
    # "Line 17 minus line 18 (if negative, enter "0")".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/taxable_income", "less": "ca/donation_high_income_threshold"},
        produces={"output": "ca/taxable_income_over_donation_threshold"},
    ),
    # Schedule 9 line 20 "Enter whichever is less: amount from line 16 or line 19. Line F"
    # "multiplied by 33%": line F, then 33% of it.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/donations_over_first_tier_after_2016_gifts",
                "ca/taxable_income_over_donation_threshold",
            )
        },
        produces={"output": "ca/high_income_donations"},
    ),
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/donation_high_income_rate"},
        consumes={"base": "ca/high_income_donations"},
        produces={"output": "ca/high_income_donation_credit"},
    ),
    # Schedule 9 line 21 "Amount E minus amount F Line G" "multiplied by 29%": amount E is the
    # amount from line 14 of the previous page and amount F is line F; line G, then 29% of it.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/donations_over_first_tier", "less": "ca/high_income_donations"},
        produces={"output": "ca/regular_rate_donations"},
    ),
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/donation_regular_rate"},
        consumes={"base": "ca/regular_rate_donations"},
        produces={"output": "ca/regular_rate_donation_credit"},
    ),
    # Schedule 9 line 22 "Amount from line 13 of the previous page Line H" "multiplied by
    # 14.5%".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/donation_first_tier_rate"},
        consumes={"base": "ca/donations_first_tier"},
        produces={"output": "ca/first_tier_donation_credit"},
    ),
    # Schedule 9 line 23 "Add lines 20 to 22. Enter this amount on line 34900 of your return.
    # Allowable donations for 2025", T1 line 116 (line 34900) "Donations and gifts (complete
    # Schedule 9)".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/high_income_donation_credit",
                "ca/regular_rate_donation_credit",
                "ca/first_tier_donation_credit",
            )
        },
        produces={"output": "ca/donations_and_gifts_credit"},
    ),
    # T1 line 115 (line 33800) "Line 113 multiplied by the percentage from line 114": the
    # federal credit rate is applied once, to the total of credit amounts. It is the first of
    # the three lines that line 35000 adds, and the base of the top-up tax credit.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/credit_rate"},
        consumes={"base": "ca/non_refundable_credit_amounts"},
        produces={"output": "ca/credit_amounts_at_credit_rate"},
    ),
    # Federal Worksheet 5000-D1, "Line 34990 - Top-up tax credit": line 1 "Amount from line
    # 33800 of your return", line 2 "Amount from line 22 of your Schedule 9" and line 3 "Line 1
    # plus line 2".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/credit_amounts_at_credit_rate", "ca/first_tier_donation_credit")},
        produces={"output": "ca/top_up_credits_base"},
    ),
    # Federal Worksheet 5000-D1, "Line 34990 - Top-up tax credit", line 4 "8,319.38": the
    # dataset becomes an artifact of the same name; line 5 "Line 3 minus line 4 (if negative,
    # enter "0")".
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/top_up_threshold"},
        consumes={},
        produces={"output": "ca/top_up_threshold"},
    ),
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/top_up_credits_base", "less": "ca/top_up_threshold"},
        produces={"output": "ca/top_up_excess"},
    ),
    # Federal Worksheet 5000-D1, "Line 34990 - Top-up tax credit", line 6 "Applicable rate
    # 3.45%" and line 7 "Line 5 multiplied by the percentage from line 6 Enter this amount on
    # line 34990 of your return.", T1 line 117 (line 34990) "Top-up tax credit (use Federal
    # Worksheet)".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/top_up_rate"},
        consumes={"base": "ca/top_up_excess"},
        produces={"output": "ca/top_up_tax_credit"},
    ),
    # T1 line 118 (line 35000) "Add lines 115 to 117. Total federal non-refundable tax credits":
    # line 115 (line 33800), line 116 (line 34900) and line 117 (line 34990), in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/credit_amounts_at_credit_rate",
                "ca/donations_and_gifts_credit",
                "ca/top_up_tax_credit",
            )
        },
        produces={"output": "ca/non_refundable_tax_credits"},
    ),
    # Form T1206 Part 2 line 8 "Amount from line 7 multiplied by 33% Enter this amount on line 40424
    # of your return. Federal tax on split income", line 7 being "Total split income from line 4",
    # which is line 4 itself: T1 line 120 and line 40424 "Federal tax on split income (TOSI)
    # (complete Form T1206)".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/split_income_rate"},
        consumes={"base": "ca/total_split_income"},
        produces={"output": "ca/federal_tax_on_split_income"},
    ),
    # Form T1206 Part 2 line 8A "TOSI-adjusted taxable income: Amount from line 8 ÷ 14.5% =", line 8
    # being the federal tax on split income.
    CapabilitySelection(
        name="ca/divided_by_rate",
        params={"rate": "ca/tosi_taxable_income_rate"},
        consumes={"dividend": "ca/federal_tax_on_split_income"},
        produces={"output": "ca/tosi_adjusted_taxable_income"},
    ),
    # Form T1206 "If you are completing a federal Schedule 11, calculate line 8A and add it to the
    # amount on line 11 of Schedule 11": the amount on line 11 (the taxable income, or the tax
    # divided by 14.5%) plus line 8A.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/tuition_income_base", "ca/tosi_adjusted_taxable_income")},
        produces={"output": "ca/tuition_income_with_tosi"},
    ),
    # T1 line 121 and line 40400 "Line 119 plus line 120 =": line 119 "Enter the amount from line
    # 76." is the federal basic tax and line 120 is the federal tax on split income, in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/federal_basic_tax",
                "ca/federal_tax_on_split_income",
            )
        },
        produces={"output": "ca/federal_tax_with_split_income"},
    ),
    # Each form's credits come off its tax, not below zero: the unused part is lost. Federally the
    # tax is line 121 (line 119, the basic tax, plus line 120, the tax on split income) and the
    # credits are line 125 (T1 line 126 "Line 121 minus line 125 (if negative, enter "0")").
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/federal_tax_with_split_income",
            "less": "ca/credits_against_basic_federal_tax",
        },
        produces={"output": "ca/federal_tax_after_credits"},
    ),
    # T2038(IND) Part C "Recapture", "Amount of expenditure on which ITC earned at 15% (after
    # 2013) is recaptured. Do not enter more than the amount of the original expenditure" (line
    # 67193), times 0.15, amount 1: the caller's line 67193 at 15%.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/itc_recapture_rate_after_2013"},
        consumes={"base": "ca/itc_recapture_expenditure_at_15_percent"},
        produces={"output": "ca/itc_recapture_at_15_percent"},
    ),
    # Line 67195 "Amount of expenditure on which ITC earned at 20% (before 2014) is recaptured.
    # Do not enter more than the amount of the original expenditure", times 0.20, amount 2: the
    # caller's line 67195 at 20%.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/itc_recapture_rate_before_2014"},
        consumes={"base": "ca/itc_recapture_expenditure_at_20_percent"},
        produces={"output": "ca/itc_recapture_at_20_percent"},
    ),
    # "Total recapture of investment tax credit on SR&ED expenditures (add amounts 1 and 2)
    # Enter this amount on the Recapture of investment tax credit line of your income tax and
    # benefit return" (amount 3), T1 line 131 "Recapture of investment tax credit (complete Form
    # T2038(IND))": amounts 1 and 2 added.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/itc_recapture_at_15_percent", "ca/itc_recapture_at_20_percent")},
        produces={"output": "ca/itc_recapture"},
    ),
    # Form T2209 note (3), net income: "Amount from line 23600 of your return (or the amount you
    # would have entered if the instructions said "if negative, show in brackets") plus the amount
    # on line 68360 of Form T1206, Total split income, minus any:" "amount deductible as a
    # Canadian Forces personnel and police deduction (line 24400 of your return)", "amount
    # deductible as security options deductions (line 24900 of your return)", "amount deductible
    # as an other payments deduction (line 25000 of your return)", "net capital losses of other
    # years you claimed (line 25300 of your return)", "capital gains deduction for qualifying
    # business transfer or qualifying cooperative conversion you claimed (line 25395 of your
    # return)", "capital gains deduction you claimed (line 25400 of your return)" and "amounts
    # deductible as net employment income from a prescribed international organization, as foreign
    # income exempt under a tax treaty, or as adult basic education tuition assistance (included
    # on line 25600 of your return)", in the note's order, added.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/canadian_armed_forces_and_police_deduction",
                "ca/security_options_deductions",
                "ca/other_payments_deduction",
                "ca/net_capital_losses_of_other_years",
                "ca/qbt_capital_gains_deduction",
                "ca/capital_gains_deduction",
                "ca/exempt_income_deductions",
            )
        },
        produces={"output": "ca/foreign_tax_credit_net_income_deductions"},
    ),
    # The net income of note (3), "Amount from line 23600 of your return (or the amount you would
    # have entered if the instructions said "if negative, show in brackets")": line 23400 less line
    # 23500, not floored, so signed. It is not the line 23600 kind, which is floored at 0.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/net_income_before_adjustments",
            "less": "ca/social_benefits_repayment",
        },
        produces={"output": "ca/foreign_tax_credit_net_income_before_split_income"},
    ),
    # Note (3), "plus the amount on line 68360 of Form T1206, Total split income": that amount
    # added. It is the same figure as the TOSI-adjusted net income, which adds line 68360 to line
    # 23400 less line 23500.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/foreign_tax_credit_net_income_before_split_income",
                "ca/total_split_income",
            )
        },
        produces={"output": "ca/foreign_tax_credit_net_income_with_split_income"},
    ),
    # Note (3), "minus any:" the deductions above. The note prints no "(if negative, enter "0")",
    # so the result is signed.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/foreign_tax_credit_net_income_with_split_income",
            "less": "ca/foreign_tax_credit_net_income_deductions",
        },
        produces={"output": "ca/foreign_tax_credit_net_income"},
    ),
    # Form T2209 note (4), basic federal tax: "Line 42900 of your return plus any:" "federal
    # dividend tax credit (line 40425 of your return)" (note (8) is this sum alone, for the
    # business lines).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/federal_tax_after_credits", "ca/dividend_tax_credit")},
        produces={"output": "ca/basic_federal_tax_with_dividend_credit"},
    ),
    # Note (4), "minus any:" "federal refundable First Nations abatement (line 44100 of your
    # return)". The federal surtax on income allocated to "Other (Outside Canada)" (line 127 of the
    # return, not wired and not triggered on an Ontario return) and the refundable Quebec
    # abatement (line 44000, which does not apply to an Ontario return) are not part of it.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/basic_federal_tax_with_dividend_credit",
            "less": "ca/first_nations_abatement",
        },
        produces={"output": "ca/foreign_tax_credit_basic_federal_tax"},
    ),
    # Form T2209, federal non-business foreign tax credit: line 1 "Non-business income tax paid to
    # a foreign country (1) 43100", line 2 "Net foreign non-business income (2) 43300" "× Basic
    # federal tax (4) =" over "Net income (3)", line 3 "Enter whichever is less: the amount from
    # line 1 or line 2. Federal non-business foreign tax credit", for each country on its own
    # when "you paid tax to more than one foreign country, and the total foreign taxes paid to all
    # foreign countries was more than $200", otherwise once on the totals; the total of line 3.
    CapabilitySelection(
        name="ca/foreign_non_business_tax_credit",
        params={
            "rounding": "ca/foreign_non_business_tax_credit_rounding",
            "pooling_threshold": "ca/foreign_tax_pooling_threshold",
        },
        consumes={
            "countries": "ca/foreign_tax_countries",
            "net_income": "ca/foreign_tax_credit_net_income",
            "basic_federal_tax": "ca/foreign_tax_credit_basic_federal_tax",
        },
        produces={
            "total": "ca/federal_non_business_foreign_tax_credit",
            "sheets": "ca/foreign_tax_credit_sheets",
        },
    ),
    # T2209 line 13 "Federal foreign tax credit", which is line 3 while the business lines (lines
    # 4 to 12) are not wired, and T1 line 129 (line 40500) "Federal foreign tax credit (complete
    # Form T2209)": "The amount on line 3 should not be more than the total of the amount on line
    # 42900 of your return plus any federal surtax on income earned outside of Canada." Line 127
    # (the surtax) is not wired, so the limit is line 42900.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/federal_non_business_foreign_tax_credit",
                "ca/federal_tax_after_credits",
            )
        },
        produces={"output": "ca/federal_foreign_tax_credit"},
    ),
    # T1 line 130 "Line 128 minus line 129 =": line 128 "Line 126 plus line 127 =" is line 126
    # (42900) "Basic federal tax", as line 127 "Federal surtax on income earned outside Canada
    # (complete Form T2203)" is not wired and not triggered on an Ontario return, and line 129
    # (40500) comes off it. The line prints no "(if negative, enter "0")" but line 129 is at most
    # line 126, so the result is not below zero.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/federal_tax_after_credits",
            "less": "ca/federal_foreign_tax_credit",
        },
        produces={"output": "ca/federal_tax_less_foreign_tax_credit"},
    ),
    # T1 line 132 "Line 130 plus line 131 =": line 130 and line 131 "Recapture of investment tax
    # credit (complete Form T2038(IND))".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/federal_tax_less_foreign_tax_credit", "ca/itc_recapture")},
        produces={"output": "ca/federal_tax_with_itc_recapture"},
    ),
}

WIRING = {
    (TieredContribution, frozenset({EMPLOYMENT_INCOME}), frozenset({EI_PREMIUMS})),
    (CappedAmount, frozenset({EMPLOYMENT_INCOME}), frozenset({CANADA_EMPLOYMENT_AMOUNT})),
    (
        TimesCount,
        frozenset({SELF_EMPLOYED_CPP_BASE_CREDIT, CPP_PART_4_COMPLETED}),
        frozenset({CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT}),
    ),
    (
        TimesCount,
        frozenset({CPP_PART_5_LINE_70, CPP_PART_5_COMPLETED}),
        frozenset({CPP_PART_5_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT}),
    ),
    (
        Sum,
        frozenset(
            {
                CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT,
                CPP_PART_5_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT,
                RC381_CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
            }
        ),
        frozenset({CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS}),
    ),
    (
        TimesCount,
        frozenset({SELF_EMPLOYED_EI_PREMIUMS, EI_SPECIAL_BENEFITS_AGREEMENT}),
        frozenset({EI_PREMIUMS_ON_SELF_EMPLOYMENT}),
    ),
    (
        ApplyRate,
        frozenset({CANADIAN_TUITION_FEES}),
        frozenset({CANADA_TRAINING_CREDIT_BASIS}),
    ),
    (
        LesserOf,
        frozenset({CANADA_TRAINING_CREDIT_BASIS, CANADA_TRAINING_CREDIT_LIMIT}),
        frozenset({CANADA_TRAINING_CREDIT_MAXIMUM}),
    ),
    (
        AtMost,
        frozenset({CANADA_TRAINING_CREDIT_CLAIMED, CANADA_TRAINING_CREDIT_MAXIMUM}),
        frozenset({CANADA_TRAINING_CREDIT}),
    ),
    (
        Subtract,
        frozenset({CANADIAN_TUITION_FEES, CANADA_TRAINING_CREDIT}),
        frozenset({CANADIAN_TUITION_AVAILABLE}),
    ),
    (
        Sum,
        frozenset({CANADIAN_TUITION_AVAILABLE, FOREIGN_TUITION_FEES}),
        frozenset({CURRENT_YEAR_TUITION_AVAILABLE}),
    ),
    (
        Sum,
        frozenset({CURRENT_YEAR_TUITION_AVAILABLE, UNUSED_TUITION_FROM_2024}),
        frozenset({TOTAL_TUITION_AVAILABLE}),
    ),
    (
        AmountOrDividedByRate,
        frozenset({TAXABLE_INCOME, FEDERAL_BASIC_TAX}),
        frozenset({TUITION_INCOME_BASE}),
    ),
    (
        Sum,
        frozenset(
            {
                BASIC_PERSONAL_AMOUNT,
                AGE_AMOUNT,
                SPOUSE_AMOUNT,
                ELIGIBLE_DEPENDANT_AMOUNT,
                SPOUSE_CAREGIVER_AMOUNT,
                CAREGIVER_AMOUNT,
                INFIRM_CHILDREN_AMOUNT,
                CPP_BASE_CONTRIBUTIONS_ON_RETURN,
                CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
                EI_PREMIUMS,
                EI_PREMIUMS_ON_SELF_EMPLOYMENT,
                CANADA_EMPLOYMENT_AMOUNT,
                DISABILITY_AMOUNT_FOR_SELF,
                DISABILITY_TRANSFERRED_AMOUNT,
            }
        ),
        frozenset({CREDIT_AMOUNTS_SUBTOTAL}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({TUITION_INCOME_WITH_TOSI, CREDIT_AMOUNTS_SUBTOTAL}),
        frozenset({TUITION_INCOME_LESS_CREDITS}),
    ),
    (
        LesserOf,
        frozenset({UNUSED_TUITION_FROM_2024, TUITION_INCOME_LESS_CREDITS}),
        frozenset({UNUSED_TUITION_CLAIMED}),
    ),
    (
        Subtract,
        frozenset({TUITION_INCOME_LESS_CREDITS, UNUSED_TUITION_CLAIMED}),
        frozenset({TUITION_INCOME_REMAINING}),
    ),
    (
        LesserOf,
        frozenset({CURRENT_YEAR_TUITION_AVAILABLE, TUITION_INCOME_REMAINING}),
        frozenset({CURRENT_YEAR_TUITION_CLAIMED}),
    ),
    (
        Sum,
        frozenset({UNUSED_TUITION_CLAIMED, CURRENT_YEAR_TUITION_CLAIMED}),
        frozenset({FEDERAL_TUITION_AMOUNT}),
    ),
    (
        Subtract,
        frozenset({TOTAL_TUITION_AVAILABLE, FEDERAL_TUITION_AMOUNT}),
        frozenset({UNUSED_FEDERAL_TUITION}),
    ),
    (
        CappedAmount,
        frozenset({CURRENT_YEAR_TUITION_AVAILABLE}),
        frozenset({TUITION_TRANSFER_LIMIT}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({TUITION_TRANSFER_LIMIT, CURRENT_YEAR_TUITION_CLAIMED}),
        frozenset({TUITION_AVAILABLE_TO_TRANSFER}),
    ),
    (
        AtMost,
        frozenset({TUITION_TRANSFER_ELECTED, TUITION_AVAILABLE_TO_TRANSFER}),
        frozenset({TUITION_TRANSFERRED}),
    ),
    (
        Subtract,
        frozenset({UNUSED_FEDERAL_TUITION, TUITION_TRANSFERRED}),
        frozenset({TUITION_CARRIED_FORWARD}),
    ),
    (
        Sum,
        frozenset(
            {
                SPOUSE_RETURN_AGE_AMOUNT,
                SPOUSE_RETURN_INFIRM_CHILDREN_AMOUNT,
                SPOUSE_RETURN_PENSION_INCOME_AMOUNT,
                SPOUSE_RETURN_DISABILITY_AMOUNT,
                SPOUSE_DESIGNATED_TUITION,
            }
        ),
        frozenset({SPOUSE_TRANSFERABLE_AMOUNTS}),
    ),
    (
        AmountOrDividedByRate,
        frozenset({SPOUSE_RETURN_TAXABLE_INCOME, SPOUSE_RETURN_FEDERAL_BASIC_TAX}),
        frozenset({SPOUSE_INCOME_FOR_TRANSFER}),
    ),
    (
        Sum,
        frozenset(
            {
                SPOUSE_RETURN_BASIC_PERSONAL_AMOUNT,
                SPOUSE_RETURN_LINE_96,
                SPOUSE_RETURN_FEDERAL_TUITION_AMOUNT,
            }
        ),
        frozenset({SPOUSE_CREDITS_USED}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({SPOUSE_INCOME_FOR_TRANSFER, SPOUSE_CREDITS_USED}),
        frozenset({SPOUSE_ADJUSTED_TAXABLE_INCOME}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({SPOUSE_TRANSFERABLE_AMOUNTS, SPOUSE_ADJUSTED_TAXABLE_INCOME}),
        frozenset({SPOUSE_UNUSED_AMOUNTS}),
    ),
    (
        TimesCount,
        frozenset({SPOUSE_UNUSED_AMOUNTS, SPOUSE_NOT_SEPARATED_90_DAYS}),
        frozenset({AMOUNTS_TRANSFERRED_FROM_SPOUSE}),
    ),
    (
        Sum,
        frozenset(
            {
                BASIC_PERSONAL_AMOUNT,
                AGE_AMOUNT,
                SPOUSE_AMOUNT,
                ELIGIBLE_DEPENDANT_AMOUNT,
                SPOUSE_CAREGIVER_AMOUNT,
                CAREGIVER_AMOUNT,
                INFIRM_CHILDREN_AMOUNT,
                CPP_BASE_CONTRIBUTIONS_ON_RETURN,
                CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
                EI_PREMIUMS,
                EI_PREMIUMS_ON_SELF_EMPLOYMENT,
                CANADA_EMPLOYMENT_AMOUNT,
                MEDICAL_CLAIM,
                DISABILITY_AMOUNT_FOR_SELF,
                DISABILITY_TRANSFERRED_AMOUNT,
                FEDERAL_TUITION_AMOUNT,
                TUITION_TRANSFERRED_FROM_CHILD,
                AMOUNTS_TRANSFERRED_FROM_SPOUSE,
            }
        ),
        frozenset({NON_REFUNDABLE_CREDIT_AMOUNTS}),
    ),
    (
        ApplyRate,
        frozenset({NON_REFUNDABLE_CREDIT_AMOUNTS}),
        frozenset({CREDIT_AMOUNTS_AT_CREDIT_RATE}),
    ),
    (
        LesserOf,
        frozenset({DEPRECIABLE_GIFT_NET_PROCEEDS, DEPRECIABLE_GIFT_CAPITAL_COST}),
        frozenset({DEPRECIABLE_GIFT_PROCEEDS_OR_COST}),
    ),
    (
        LesserOf,
        frozenset({DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION, DEPRECIABLE_GIFT_PROCEEDS_OR_COST}),
        frozenset({DEPRECIABLE_GIFTS}),
    ),
    (
        Subtract,
        frozenset({CAPITAL_GIFT_TAXABLE_GAINS, CAPITAL_GIFT_GAINS_DEDUCTION}),
        frozenset({CAPITAL_PROPERTY_GIFTS}),
    ),
    (
        Sum,
        frozenset(
            {
                CHARITABLE_DONATIONS,
                GOVERNMENT_DONATIONS,
                UNIVERSITY_DONATIONS_OUTSIDE_CANADA,
                FOREIGN_CHARITY_DONATIONS,
            }
        ),
        frozenset({TOTAL_CHARITABLE_DONATIONS}),
    ),
    (ApplyRate, frozenset({NET_INCOME}), frozenset({DONATION_LIMIT_ON_NET_INCOME})),
    (
        Sum,
        frozenset({DEPRECIABLE_GIFTS, CAPITAL_PROPERTY_GIFTS}),
        frozenset({CAPITAL_GIFTS_TOTAL}),
    ),
    (ApplyRate, frozenset({CAPITAL_GIFTS_TOTAL}), frozenset({CAPITAL_GIFTS_LIMIT_ADDITION})),
    (
        Sum,
        frozenset({DONATION_LIMIT_ON_NET_INCOME, CAPITAL_GIFTS_LIMIT_ADDITION}),
        frozenset({DONATION_LIMIT_WITH_CAPITAL_GIFTS}),
    ),
    (
        LesserOf,
        frozenset({NET_INCOME, DONATION_LIMIT_WITH_CAPITAL_GIFTS}),
        frozenset({CHARITABLE_DONATIONS_LIMIT}),
    ),
    (
        LesserOf,
        frozenset({TOTAL_CHARITABLE_DONATIONS, CHARITABLE_DONATIONS_LIMIT}),
        frozenset({CHARITABLE_DONATIONS_CLAIMED}),
    ),
    (
        Sum,
        frozenset({CHARITABLE_DONATIONS_CLAIMED, ECOLOGICAL_AND_CULTURAL_GIFTS}),
        frozenset({DONATIONS_AND_GIFTS_TOTAL}),
    ),
    (CreditAmount, frozenset(), frozenset({DONATION_FIRST_TIER_MAXIMUM})),
    (
        LesserOf,
        frozenset({DONATIONS_AND_GIFTS_TOTAL, DONATION_FIRST_TIER_MAXIMUM}),
        frozenset({DONATIONS_FIRST_TIER}),
    ),
    (
        Subtract,
        frozenset({DONATIONS_AND_GIFTS_TOTAL, DONATIONS_FIRST_TIER}),
        frozenset({DONATIONS_OVER_FIRST_TIER}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({DONATIONS_OVER_FIRST_TIER, ECOLOGICAL_GIFTS_BEFORE_2016}),
        frozenset({DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS}),
    ),
    (CreditAmount, frozenset(), frozenset({DONATION_HIGH_INCOME_THRESHOLD})),
    (
        SubtractNotBelowZero,
        frozenset({TAXABLE_INCOME, DONATION_HIGH_INCOME_THRESHOLD}),
        frozenset({TAXABLE_INCOME_OVER_DONATION_THRESHOLD}),
    ),
    (
        LesserOf,
        frozenset(
            {DONATIONS_OVER_FIRST_TIER_AFTER_2016_GIFTS, TAXABLE_INCOME_OVER_DONATION_THRESHOLD}
        ),
        frozenset({HIGH_INCOME_DONATIONS}),
    ),
    (ApplyRate, frozenset({HIGH_INCOME_DONATIONS}), frozenset({HIGH_INCOME_DONATION_CREDIT})),
    (
        Subtract,
        frozenset({DONATIONS_OVER_FIRST_TIER, HIGH_INCOME_DONATIONS}),
        frozenset({REGULAR_RATE_DONATIONS}),
    ),
    (ApplyRate, frozenset({REGULAR_RATE_DONATIONS}), frozenset({REGULAR_RATE_DONATION_CREDIT})),
    (ApplyRate, frozenset({DONATIONS_FIRST_TIER}), frozenset({FIRST_TIER_DONATION_CREDIT})),
    (
        Sum,
        frozenset(
            {
                HIGH_INCOME_DONATION_CREDIT,
                REGULAR_RATE_DONATION_CREDIT,
                FIRST_TIER_DONATION_CREDIT,
            }
        ),
        frozenset({DONATIONS_AND_GIFTS_CREDIT}),
    ),
    (
        Sum,
        frozenset({CREDIT_AMOUNTS_AT_CREDIT_RATE, FIRST_TIER_DONATION_CREDIT}),
        frozenset({TOP_UP_CREDITS_BASE}),
    ),
    (CreditAmount, frozenset(), frozenset({TOP_UP_THRESHOLD})),
    (
        SubtractNotBelowZero,
        frozenset({TOP_UP_CREDITS_BASE, TOP_UP_THRESHOLD}),
        frozenset({TOP_UP_EXCESS}),
    ),
    (ApplyRate, frozenset({TOP_UP_EXCESS}), frozenset({TOP_UP_TAX_CREDIT})),
    (
        Sum,
        frozenset({CREDIT_AMOUNTS_AT_CREDIT_RATE, DONATIONS_AND_GIFTS_CREDIT, TOP_UP_TAX_CREDIT}),
        frozenset({NON_REFUNDABLE_TAX_CREDITS}),
    ),
    (ApplyRate, frozenset({TOTAL_SPLIT_INCOME}), frozenset({FEDERAL_TAX_ON_SPLIT_INCOME})),
    (
        DividedByRate,
        frozenset({FEDERAL_TAX_ON_SPLIT_INCOME}),
        frozenset({TOSI_ADJUSTED_TAXABLE_INCOME}),
    ),
    (
        Sum,
        frozenset({TUITION_INCOME_BASE, TOSI_ADJUSTED_TAXABLE_INCOME}),
        frozenset({TUITION_INCOME_WITH_TOSI}),
    ),
    (
        Sum,
        frozenset({FEDERAL_BASIC_TAX, FEDERAL_TAX_ON_SPLIT_INCOME}),
        frozenset({FEDERAL_TAX_WITH_SPLIT_INCOME}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({FEDERAL_TAX_WITH_SPLIT_INCOME, CREDITS_AGAINST_BASIC_FEDERAL_TAX}),
        frozenset({FEDERAL_TAX_AFTER_CREDITS}),
    ),
    (
        ApplyRate,
        frozenset({ITC_RECAPTURE_EXPENDITURE_AT_15_PERCENT}),
        frozenset({ITC_RECAPTURE_AT_15_PERCENT}),
    ),
    (
        ApplyRate,
        frozenset({ITC_RECAPTURE_EXPENDITURE_AT_20_PERCENT}),
        frozenset({ITC_RECAPTURE_AT_20_PERCENT}),
    ),
    (
        Sum,
        frozenset({ITC_RECAPTURE_AT_15_PERCENT, ITC_RECAPTURE_AT_20_PERCENT}),
        frozenset({ITC_RECAPTURE}),
    ),
    (
        Sum,
        frozenset(
            {
                CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
                SECURITY_OPTIONS_DEDUCTIONS,
                OTHER_PAYMENTS_DEDUCTION,
                NET_CAPITAL_LOSSES_OF_OTHER_YEARS,
                QBT_CAPITAL_GAINS_DEDUCTION,
                CAPITAL_GAINS_DEDUCTION,
                EXEMPT_INCOME_DEDUCTIONS,
            }
        ),
        frozenset({FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS}),
    ),
    (
        Subtract,
        frozenset({NET_INCOME_BEFORE_ADJUSTMENTS, SOCIAL_BENEFITS_REPAYMENT}),
        frozenset({FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME}),
    ),
    (
        Sum,
        frozenset({FOREIGN_TAX_CREDIT_NET_INCOME_BEFORE_SPLIT_INCOME, TOTAL_SPLIT_INCOME}),
        frozenset({FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME}),
    ),
    (
        Subtract,
        frozenset(
            {
                FOREIGN_TAX_CREDIT_NET_INCOME_WITH_SPLIT_INCOME,
                FOREIGN_TAX_CREDIT_NET_INCOME_DEDUCTIONS,
            }
        ),
        frozenset({FOREIGN_TAX_CREDIT_NET_INCOME}),
    ),
    (
        Sum,
        frozenset({FEDERAL_TAX_AFTER_CREDITS, DIVIDEND_TAX_CREDIT}),
        frozenset({BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT}),
    ),
    (
        Subtract,
        frozenset({BASIC_FEDERAL_TAX_WITH_DIVIDEND_CREDIT, FIRST_NATIONS_ABATEMENT}),
        frozenset({FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX}),
    ),
    (
        ForeignNonBusinessTaxCredit,
        frozenset(
            {
                FOREIGN_TAX_COUNTRIES,
                FOREIGN_TAX_CREDIT_NET_INCOME,
                FOREIGN_TAX_CREDIT_BASIC_FEDERAL_TAX,
            }
        ),
        frozenset({FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT, FOREIGN_TAX_CREDIT_SHEETS}),
    ),
    (
        LesserOf,
        frozenset({FEDERAL_NON_BUSINESS_FOREIGN_TAX_CREDIT, FEDERAL_TAX_AFTER_CREDITS}),
        frozenset({FEDERAL_FOREIGN_TAX_CREDIT}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({FEDERAL_TAX_AFTER_CREDITS, FEDERAL_FOREIGN_TAX_CREDIT}),
        frozenset({FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT}),
    ),
    (
        Sum,
        frozenset({FEDERAL_TAX_LESS_FOREIGN_TAX_CREDIT, ITC_RECAPTURE}),
        frozenset({FEDERAL_TAX_WITH_ITC_RECAPTURE}),
    ),
}
