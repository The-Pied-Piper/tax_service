"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.times_count import TimesCount
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    AGE_AMOUNT,
    BASIC_PERSONAL_AMOUNT,
    CANADA_EMPLOYMENT_AMOUNT,
    CAPITAL_GIFT_GAINS_DEDUCTION,
    CAPITAL_GIFT_TAXABLE_GAINS,
    CAPITAL_GIFTS_LIMIT_ADDITION,
    CAPITAL_GIFTS_TOTAL,
    CAPITAL_PROPERTY_GIFTS,
    CAREGIVER_AMOUNT,
    CHARITABLE_DONATIONS,
    CHARITABLE_DONATIONS_CLAIMED,
    CHARITABLE_DONATIONS_LIMIT,
    CPP_BASE_CONTRIBUTIONS,
    CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT,
    CPP_PART_4_COMPLETED,
    CREDIT_AMOUNTS_AT_CREDIT_RATE,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    DEPRECIABLE_GIFT_CAPITAL_COST,
    DEPRECIABLE_GIFT_NET_PROCEEDS,
    DEPRECIABLE_GIFT_PROCEEDS_OR_COST,
    DEPRECIABLE_GIFT_RECAPTURED_DEPRECIATION,
    DEPRECIABLE_GIFTS,
    DISABILITY_TRANSFERRED_AMOUNT,
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
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    FEDERAL_TAX_WITH_ITC_RECAPTURE,
    FIRST_TIER_DONATION_CREDIT,
    FOREIGN_CHARITY_DONATIONS,
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
    NET_INCOME,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    REGULAR_RATE_DONATION_CREDIT,
    REGULAR_RATE_DONATIONS,
    SELF_EMPLOYED_CPP_BASE_CREDIT,
    SELF_EMPLOYED_EI_PREMIUMS,
    SPOUSE_AMOUNT,
    SPOUSE_CAREGIVER_AMOUNT,
    TAXABLE_INCOME,
    TAXABLE_INCOME_OVER_DONATION_THRESHOLD,
    TOP_UP_CREDITS_BASE,
    TOP_UP_EXCESS,
    TOP_UP_TAX_CREDIT,
    TOP_UP_THRESHOLD,
    TOTAL_CHARITABLE_DONATIONS,
    UNIVERSITY_DONATIONS_OUTSIDE_CANADA,
)

INPUTS = frozenset(
    {
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
    }
)

OUTPUTS = frozenset[str]()

STEPS = {
    # Schedule 8 Part 3, each contribution on employment income: line 11 (base, 4.95% of the
    # earnings between the $3,500 exemption and the $71,300 ceiling, lines 2 to 7), line 12
    # (first additional, 1% of the same band) and line 22 (second additional, 4% of the
    # earnings between the $71,300 and $81,200 ceilings, lines 2 to 4).
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/cpp_base_contribution"},
        consumes={"earnings": "ca/employment_income"},
        produces={"output": "ca/cpp_base_contributions"},
    ),
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
    # T1 line 33500 (lines 30000, 30100, 30300, 30400, 30425, 30450, 30500, 30800, 31000, 31200,
    # 31217, 31260, 31800, 33200) and ON428 line 58800 (lines 58040, 58080, 58120, 58160, 58185,
    # 58240, 58300, 58769), in the forms' line order. T1 line 113 and line 33500 is "Line 106 plus
    # line 112", and line 112 (line 33200) follows the lines that line 106 adds; ON428 line 44 and
    # line 58800 is "Line 35 plus line 43", and line 43 (line 58769) follows the lines that line 35
    # adds. ON428 lines 58240 and 58300 are "Amount from line 30800 / 31200 of your return", so the
    # Ontario sum reads the federal kinds; it has no Canada employment amount. Lines 31000 "on
    # self-employment income and other earnings" and 31217 "on self-employment and other eligible
    # earnings (complete Schedule 13)" follow lines 30800 and 31200; ON428's counterparts (lines
    # 58280 and 58305) are not wired.
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
                "ca/cpp_base_contributions",
                "ca/cpp_base_contributions_on_self_employment",
                "ca/ei_premiums",
                "ca/ei_premiums_on_self_employment",
                "ca/canada_employment_amount",
                "ca/disability_transferred_amount",
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
    # Each form's credits come off its basic tax, not below zero: the unused part is lost.
    # Federally the credits are line 125 (T1 line 126 "Line 121 minus line 125 (if negative,
    # enter "0")").
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/federal_basic_tax",
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
    # T1 line 132 "Line 130 plus line 131 =": line 126 (42900) "Basic federal tax" and line 131.
    # Line 127 "Federal surtax on income earned outside Canada (complete Form T2203)" is not
    # triggered on a return whose income is all allocated to Ontario and line 129 (40500) is not
    # yet wired, so lines 128 and 130 carry line 126 unchanged.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/federal_tax_after_credits", "ca/itc_recapture")},
        produces={"output": "ca/federal_tax_with_itc_recapture"},
    ),
}

WIRING = {
    (
        TieredContribution,
        frozenset({EMPLOYMENT_INCOME}),
        frozenset({CPP_BASE_CONTRIBUTIONS}),
    ),
    (TieredContribution, frozenset({EMPLOYMENT_INCOME}), frozenset({EI_PREMIUMS})),
    (CappedAmount, frozenset({EMPLOYMENT_INCOME}), frozenset({CANADA_EMPLOYMENT_AMOUNT})),
    (
        TimesCount,
        frozenset({SELF_EMPLOYED_CPP_BASE_CREDIT, CPP_PART_4_COMPLETED}),
        frozenset({CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT}),
    ),
    (
        TimesCount,
        frozenset({SELF_EMPLOYED_EI_PREMIUMS, EI_SPECIAL_BENEFITS_AGREEMENT}),
        frozenset({EI_PREMIUMS_ON_SELF_EMPLOYMENT}),
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
                CPP_BASE_CONTRIBUTIONS,
                CPP_BASE_CONTRIBUTIONS_ON_SELF_EMPLOYMENT,
                EI_PREMIUMS,
                EI_PREMIUMS_ON_SELF_EMPLOYMENT,
                CANADA_EMPLOYMENT_AMOUNT,
                MEDICAL_CLAIM,
                DISABILITY_TRANSFERRED_AMOUNT,
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
    (
        SubtractNotBelowZero,
        frozenset({FEDERAL_BASIC_TAX, CREDITS_AGAINST_BASIC_FEDERAL_TAX}),
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
        frozenset({FEDERAL_TAX_AFTER_CREDITS, ITC_RECAPTURE}),
        frozenset({FEDERAL_TAX_WITH_ITC_RECAPTURE}),
    ),
}
