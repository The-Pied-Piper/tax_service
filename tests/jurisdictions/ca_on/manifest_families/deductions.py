"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.amount_by_count import AmountForCount
from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.choose_by_count import ChooseByCount
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.per_unit_amount import PerUnitAmount
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.sum_not_below_zero import SumNotBelowZero
from app.domain.capabilities.times_count import TimesCount
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.chart_a_row_c_total import ChartARowCTotal
from app.jurisdictions.ca.capabilities.chart_b_zone_a_total import ChartBZoneATotal
from app.jurisdictions.ca.capabilities.chart_b_zone_b_total import ChartBZoneBTotal
from app.jurisdictions.ca.capabilities.count_by_conditions import CountByConditions
from app.jurisdictions.ca.capabilities.ei_excluded_slips_net_income import (
    EiExcludedSlipsNetIncome,
)
from app.jurisdictions.ca.catalog import (
    ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS,
    BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE,
    CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
    CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
    CAPITAL_GAINS_DEDUCTIONS_2000,
    CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
    CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
    CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
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
    CPP_ADDITIONAL_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_BASIC_EXEMPTION,
    CPP_DEDUCTION_ON_SELF_EMPLOYMENT,
    CPP_DEDUCTION_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
    CPP_EARNINGS_SUBJECT_TO_BASE_AND_FIRST_ADDITIONAL,
    CPP_EARNINGS_SUBJECT_TO_SECOND_ADDITIONAL,
    CPP_EARNINGS_UP_TO_MAXIMUM,
    CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
    CPP_MAXIMUM_PENSIONABLE_EARNINGS,
    CPP_MONTHS,
    CPP_PART_4_COMPLETED,
    CPP_PART_5_COMPLETED,
    CPP_PART_5_DEDUCTION_ON_SELF_EMPLOYMENT,
    CPP_PART_5_LINE_88,
    CPP_PENSIONABLE_EARNINGS,
    CPP_PENSIONABLE_EARNINGS_UP_TO_ADDITIONAL_MAXIMUM,
    CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM,
    CPT20_EARNINGS,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    EI_AND_OTHER_BENEFITS,
    EI_BENEFITS_REPAYMENT,
    EI_CONTROLLED_CORPORATION_EARNINGS,
    EI_EARNINGS_SUBJECT_TO_PREMIUM,
    EI_EXCLUDED_SLIPS,
    EI_EXCLUDED_SLIPS_NET_INCOME,
    EI_EXEMPT_SELF_EMPLOYMENT_INCOME,
    EI_INSURABLE_EARNINGS,
    EI_INSURABLE_EARNINGS_REMAINING,
    EI_MAXIMUM_INSURABLE_EARNINGS,
    EI_NET_SELF_EMPLOYMENT_INCOME,
    EI_SELF_EMPLOYMENT_BEFORE_SLIPS,
    EI_SELF_EMPLOYMENT_EARNINGS,
    ELECTED_SPLIT_PENSION_DEDUCTION,
    EMPLOYMENT_INCOME,
    EXPLORATION_AND_DEVELOPMENT_EXPENSES,
    FHSA_DEDUCTION,
    INCOME_SUPPORT_BENEFITS,
    NET_FEDERAL_SUPPLEMENTS,
    NET_INCOME,
    NET_INCOME_BEFORE_ADJUSTMENTS,
    NET_INCOME_BEFORE_ADJUSTMENTS_NOT_BELOW_ZERO,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
    NET_INCOME_SIGNED,
    NET_PARTNERSHIP_INCOME,
    NET_SELF_EMPLOYMENT_INCOME,
    NORTHERN_RESIDENTS_DEDUCTIONS,
    OAS_AND_FEDERAL_SUPPLEMENTS,
    OAS_BENEFITS_BASE_AMOUNT,
    OAS_OVERPAYMENT_RECOVERED,
    OLD_AGE_SECURITY,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
    OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
    OTHER_DEDUCTIONS,
    OTHER_PAYMENTS_DEDUCTION,
    OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT,
    OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
    OTHER_PAYMENTS_LIMIT_INCOME,
    OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
    OTHER_PAYMENTS_WORKSHEET_REQUIRED,
    OTHER_SPLIT_INCOME,
    PENSIONABLE_NET_SELF_EMPLOYMENT_EARNINGS,
    RC381_CPP_DEDUCTION_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
    RDSP_INCOME,
    RDSP_INCOME_REPAYMENT,
    RESIDENCY_AMOUNT,
    RESIDENCY_DEDUCTION,
    RESIDENCY_NET_INCOME_LIMIT,
    RPP_DEDUCTION,
    RRSP_DEDUCTION,
    SELF_EMPLOYED_CPP_BASE_CONTRIBUTIONS,
    SELF_EMPLOYED_CPP_BASE_CREDIT,
    SELF_EMPLOYED_CPP_CONTRIBUTIONS_PAYABLE,
    SELF_EMPLOYED_CPP_DEDUCTION,
    SELF_EMPLOYED_CPP_ENHANCED_CONTRIBUTIONS,
    SELF_EMPLOYED_CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    SELF_EMPLOYED_CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    SELF_EMPLOYED_EI_PREMIUMS,
    SOCIAL_BENEFITS_LINE_5,
    SOCIAL_BENEFITS_LINE_6,
    SOCIAL_BENEFITS_LINE_10,
    SOCIAL_BENEFITS_LINE_11,
    SOCIAL_BENEFITS_LINE_14,
    SOCIAL_BENEFITS_LINE_15,
    SOCIAL_BENEFITS_LINE_17,
    SOCIAL_BENEFITS_LINE_18,
    SOCIAL_BENEFITS_LINE_19,
    SOCIAL_BENEFITS_LINE_21,
    SOCIAL_BENEFITS_REPAYMENT,
    SOCIAL_BENEFITS_REPAYMENT_APPLIES,
    SPLIT_INCOME_DIVIDENDS,
    STANDARD_AMOUNT_ALLOCATED,
    SUPPORT_PAYMENTS_DEDUCTION,
    TOSI_ADJUSTED_NET_INCOME,
    TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO,
    TOTAL_CARRYING_CHARGES,
    TOTAL_INCOME,
    TOTAL_INTEREST_EXPENSES,
    TOTAL_OTHER_EXPENSES,
    TOTAL_SPLIT_INCOME,
    TRAVEL_DEDUCTION,
    TRAVEL_INDIVIDUALS,
    TRAVEL_TOTAL_ZONE_A,
    TRAVEL_TOTAL_ZONE_B,
    TRAVEL_TRIPS,
    TRAVEL_ZONE_B_DEDUCTION,
    UCCB_AND_RDSP_INCOME,
    UCCB_AND_RDSP_INCOME_REPAYMENTS,
    UCCB_REPAYMENT,
    UNION_DUES,
    UNIVERSAL_CHILD_CARE_BENEFIT,
    ZONE_A_ADDITIONAL_RESIDENCY_AMOUNT,
    ZONE_A_ADDITIONAL_RESIDENCY_DAYS,
    ZONE_A_BASIC_RESIDENCY_AMOUNT,
    ZONE_A_DAYS_LIVED,
    ZONE_A_RESIDENCY_AFTER_WORK_SITE,
    ZONE_A_RESIDENCY_AMOUNT,
    ZONE_A_SPECIAL_WORK_SITE_BENEFITS,
    ZONE_B_ADDITIONAL_RESIDENCY_AMOUNT,
    ZONE_B_ADDITIONAL_RESIDENCY_DAYS,
    ZONE_B_BASIC_RESIDENCY_AMOUNT,
    ZONE_B_DAYS_LIVED,
    ZONE_B_RESIDENCY_AFTER_WORK_SITE,
    ZONE_B_RESIDENCY_AMOUNT,
    ZONE_B_SPECIAL_WORK_SITE_BENEFITS,
)

INPUTS = frozenset(
    {
        "ca/oas_overpayment_recovered",
        "ca/ei_benefits_repayment",
        "ca/uccb_repayment",
        "ca/rdsp_income_repayment",
        "ca/canadian_armed_forces_and_police_deduction",
        "ca/security_options_deductions",
        "ca/other_payments_deduction_above_limit",
        "ca/other_payments_worksheet_required",
        "ca/other_payments_worksheet_line_9_over_limit",
        "ca/union_dues",
        "ca/cpp_months",
        "ca/cpt20_earnings",
        "ca/cpp_part_4_completed",
        "ca/cpp_part_5_completed",
        "ca/ei_controlled_corporation_earnings",
        "ca/ei_exempt_self_employment_income",
        "ca/ei_excluded_slips",
        "ca/ei_insurable_earnings",
        "ca/elected_split_pension_deduction",
        "ca/support_payments_deduction",
        "ca/exploration_and_development_expenses",
        "ca/other_deductions",
        "ca/split_income_dividends",
        "ca/split_income_dividends_other_than_eligible",
        "ca/other_split_income",
        "ca/split_income_from_foreign_sources",
        "ca/total_income_from_foreign_sources",
        "ca/total_carrying_charges",
        "ca/total_interest_expenses",
        "ca/total_other_expenses",
        "ca/capital_gains_deductions_1985_to_1987",
        "ca/capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property",
        "ca/capital_gains_deductions_1988_and_1989_eligible_capital_property",
        "ca/capital_gains_deductions_1990_to_1999",
        "ca/capital_gains_deductions_2000",
        "ca/capital_gains_deductions_2001_to_2024",
        "ca/other_business_investment_loss_reductions_1986_to_1994",
        "ca/other_business_investment_loss_reductions_1994_to_1996",
        "ca/other_business_investment_loss_reductions_1997_to_1999",
        "ca/other_business_investment_loss_reductions_2000",
        "ca/other_business_investment_loss_reductions_2001_to_2023",
        "ca/other_business_investment_loss_reductions_2024",
        "ca/business_investment_loss",
        "ca/child_care_expenses_paid",
        "ca/children_under_seven",
        "ca/children_with_disability",
        "ca/children_seven_to_sixteen",
        "ca/zone_a_days_lived",
        "ca/zone_a_additional_residency_days",
        "ca/zone_a_special_work_site_benefits",
        "ca/zone_b_days_lived",
        "ca/zone_b_additional_residency_days",
        "ca/zone_b_special_work_site_benefits",
        "ca/travel_trips",
        "ca/travel_individuals",
        "ca/cpp_t4_base_and_first_additional_contributions",
        "ca/cpp_t4_second_additional_contributions",
    }
)

OUTPUTS = frozenset(
    {
        "ca/net_income_before_adjustments",
        "ca/other_payments_limit_income",
        "ca/standard_amount_allocated",
        "ca/cpp_second_additional_earnings_maximum",
    }
)

STEPS = {
    # Schedule 8 Part 2 "Box A: Enter the number of months that CPP applied in 2025." and the
    # "Monthly proration for 2025" table, a row for each number of months (1 to 12): line B
    # (maximum pensionable earnings), line C (maximum amount subject to second additional
    # contributions), line D (additional maximum pensionable earnings) and line E (maximum
    # basic exemption), each the figure of the row for the months in box A.
    CapabilitySelection(
        name="core/amount_by_count",
        params={"table": "ca/cpp_maximum_pensionable_earnings"},
        consumes={"count": "ca/cpp_months"},
        produces={"output": "ca/cpp_maximum_pensionable_earnings"},
    ),
    CapabilitySelection(
        name="core/amount_by_count",
        params={"table": "ca/cpp_second_additional_earnings_maximum"},
        consumes={"count": "ca/cpp_months"},
        produces={"output": "ca/cpp_second_additional_earnings_maximum"},
    ),
    CapabilitySelection(
        name="core/amount_by_count",
        params={"table": "ca/cpp_additional_maximum_pensionable_earnings"},
        consumes={"count": "ca/cpp_months"},
        produces={"output": "ca/cpp_additional_maximum_pensionable_earnings"},
    ),
    CapabilitySelection(
        name="core/amount_by_count",
        params={"table": "ca/cpp_basic_exemption"},
        consumes={"count": "ca/cpp_months"},
        produces={"output": "ca/cpp_basic_exemption"},
    ),
    # Schedule 8 Part 4 line 1 "amount from line 12200 of your return plus line 27 of your
    # return": the pensionable net self-employment earnings, the net partnership income then
    # the net self-employment income.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/net_partnership_income", "ca/net_self_employment_income")},
        produces={"output": "ca/pensionable_net_self_employment_earnings"},
    ),
    # Part 4 line 2 and line 50373 "Employment earnings not shown on a T4 slip that you are
    # electing to pay additional CPP contributions on (complete Form CPT20)" and line 3 "Line 1
    # plus line 2 (if negative, enter "0")": the CPP pensionable earnings.
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={
            "parts": ("ca/pensionable_net_self_employment_earnings", "ca/cpt20_earnings"),
        },
        produces={"output": "ca/cpp_pensionable_earnings"},
    ),
    # Part 4 line 4 "Enter whichever is less: amount from line D of Part 2 or line 3.", line D
    # in the form's order first.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/cpp_additional_maximum_pensionable_earnings",
                "ca/cpp_pensionable_earnings",
            ),
        },
        produces={"output": "ca/cpp_pensionable_earnings_up_to_additional_maximum"},
    ),
    # Part 4 line 6 "Line 4 minus line 5 (if negative, enter "0")", line 5 "Amount from line B
    # of Part 2": the earnings subject to second additional contributions; line 7 "Line 4 minus
    # line 6 (if negative, enter "0")"; and line 9 "Line 7 minus line 8 (if negative, enter
    # "0") (maximum $67,800)", line 8 "Amount from line E of Part 2": the earnings subject to
    # base and first additional contributions.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/cpp_pensionable_earnings_up_to_additional_maximum",
            "less": "ca/cpp_maximum_pensionable_earnings",
        },
        produces={"output": "ca/cpp_earnings_subject_to_second_additional"},
    ),
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/cpp_pensionable_earnings_up_to_additional_maximum",
            "less": "ca/cpp_earnings_subject_to_second_additional",
        },
        produces={"output": "ca/cpp_earnings_up_to_maximum"},
    ),
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/cpp_earnings_up_to_maximum", "less": "ca/cpp_basic_exemption"},
        produces={"output": "ca/cpp_earnings_subject_to_base_and_first_additional"},
    ),
    # Part 4 line 10 "amount from line 9 multiplied by 9.9% (maximum $6,712.20)", line 11
    # "amount from line 9 multiplied by 2% (maximum $1,356.00)" and line 12 "amount from line 6
    # multiplied by 8% (maximum $792.00)": the self-employed person's base, first additional
    # and second additional contributions, each the tier on the earnings of its line (lines 9,
    # 9 and 6).
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/cpp_self_employed_base_contribution"},
        consumes={"earnings": "ca/cpp_earnings_subject_to_base_and_first_additional"},
        produces={"output": "ca/self_employed_cpp_base_contributions"},
    ),
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/cpp_self_employed_first_additional_contribution"},
        consumes={"earnings": "ca/cpp_earnings_subject_to_base_and_first_additional"},
        produces={"output": "ca/self_employed_cpp_first_additional_contributions"},
    ),
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/cpp_self_employed_second_additional_contribution"},
        consumes={"earnings": "ca/cpp_earnings_subject_to_second_additional"},
        produces={"output": "ca/self_employed_cpp_second_additional_contributions"},
    ),
    # Part 4 line 13 "Line 11 plus line 12" and line 14 "Line 10 plus line 13 Enter this amount
    # (in dollars and cents) on line 42100 of your return.": the enhanced contributions, then
    # the CPP contributions payable.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/self_employed_cpp_first_additional_contributions",
                "ca/self_employed_cpp_second_additional_contributions",
            ),
        },
        produces={"output": "ca/self_employed_cpp_enhanced_contributions"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/self_employed_cpp_base_contributions",
                "ca/self_employed_cpp_enhanced_contributions",
            ),
        },
        produces={"output": "ca/self_employed_cpp_contributions_payable"},
    ),
    # Part 4 line 15 "amount from line 10 multiplied by 50%" (enter on line 31000) and line 17
    # "Line 15 plus line 16 Enter this amount (in dollars and cents) on line 22200 of your
    # return.", line 16 "Amount from line 13": the base CPP contributions credit and the
    # deduction.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/cpp_self_employed_base_credit_rate"},
        consumes={"base": "ca/self_employed_cpp_base_contributions"},
        produces={"output": "ca/self_employed_cpp_base_credit"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/self_employed_cpp_base_credit",
                "ca/self_employed_cpp_enhanced_contributions",
            ),
        },
        produces={"output": "ca/self_employed_cpp_deduction"},
    ),
    # T1 line 47 (22200), entered from Part 4 line 17: Part 4 is completed only when the filer
    # reports self-employment income alone, so the amount is counted once for each Part 4
    # completed, 1 or 0.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/self_employed_cpp_deduction",
            "count": "ca/cpp_part_4_completed",
        },
        produces={"output": "ca/cpp_deduction_on_self_employment"},
    ),
    # T1 line 47 (22200), entered from Part 5 line 88: Part 5 is completed when the filer
    # reports employment income and self-employment income or other earnings, so the amount is
    # counted once for each Part 5 completed, 1 or 0.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/cpp_part_5_line_88",
            "count": "ca/cpp_part_5_completed",
        },
        produces={"output": "ca/cpp_part_5_deduction_on_self_employment"},
    ),
    # T1 line 47 (22200): the Part 4 amount plus the Part 5 amount; both are added when both
    # parts are marked completed, as the form leaves the choice to the filer. Plus Form RC381 Part 4
    # line 129 (the form's total, 0 with no copy; the return carries Schedule 8 or Form RC381,
    # never both).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/cpp_deduction_on_self_employment",
                "ca/cpp_part_5_deduction_on_self_employment",
                "ca/rc381_cpp_deduction_on_self_employment_and_other_earnings",
            ),
        },
        produces={"output": "ca/cpp_deduction_on_self_employment_and_other_earnings"},
    ),
    # Schedule 13 line 1 "Enter the total amount from line 1 1 plus line 27 of your return. If
    # you received a T4 slip for self-employment income with EI premiums in box 18, do not
    # include any net income (or net loss) reported on lines 13500, 13700, 13900, 14100, and
    # 14300 of your return for that slip (Note 1) (if negative, enter "0")", read as line 12200
    # plus line 27 (before the slips), less the net income of those slips, not below zero, and
    # line 4 "Add lines 1 to 3. Net self-employment income": line 2 and line 54493 (a
    # corporation controlled by the filer) and line 3 and line 54494 (tax-exempt
    # self-employment income) follow line 1.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/net_partnership_income", "ca/net_self_employment_income")},
        produces={"output": "ca/ei_self_employment_before_slips"},
    ),
    CapabilitySelection(
        name="ca/ei_excluded_slips_net_income",
        params={},
        consumes={"slips": "ca/ei_excluded_slips"},
        produces={"output": "ca/ei_excluded_slips_net_income"},
    ),
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/ei_self_employment_before_slips",
            "less": "ca/ei_excluded_slips_net_income",
        },
        produces={"output": "ca/ei_self_employment_earnings"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/ei_self_employment_earnings",
                "ca/ei_controlled_corporation_earnings",
                "ca/ei_exempt_self_employment_income",
            ),
        },
        produces={"output": "ca/ei_net_self_employment_income"},
    ),
    # Schedule 13 line 5 "Maximum insurable earnings 65,700.00", line 6 and line 54780 "Total
    # EI insurable earnings (amount from box 24 of all your T4 slips ...)" and line 7 "Line 5
    # minus line 6 (if negative, enter "0")".
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/ei_maximum_insurable_earnings"},
        consumes={},
        produces={"output": "ca/ei_maximum_insurable_earnings"},
    ),
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/ei_maximum_insurable_earnings",
            "less": "ca/ei_insurable_earnings",
        },
        produces={"output": "ca/ei_insurable_earnings_remaining"},
    ),
    # Schedule 13 line 8 "Enter whichever is less: amount from line 4 or line 7." and line 9
    # "Residents of a province or territory other than Quebec: Line 9: Amount from line 8
    # multiplied by 1.64% (maximum $1,077.48)": the premiums on the earnings of line 8.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/ei_net_self_employment_income",
                "ca/ei_insurable_earnings_remaining",
            ),
        },
        produces={"output": "ca/ei_earnings_subject_to_premium"},
    ),
    CapabilitySelection(
        name="core/contribution_tier",
        params={"tier": "ca/ei_self_employed_premium"},
        consumes={"earnings": "ca/ei_earnings_subject_to_premium"},
        produces={"output": "ca/self_employed_ei_premiums"},
    ),
    # Form T778 Part B line 1 "Number of eligible children born in 2019 or later whom the
    # disability amount cannot be claimed for" "multiplied by $8,000", line 2 (line 67960)
    # "Number of eligible children born in 2025 or earlier whom the disability amount can be
    # claimed for" "multiplied by $11,000" and line 3 "Number of eligible children born in
    # 2009 to 2018 (and born in 2008 or earlier with a mental or physical infirmity whom the
    # disability amount cannot be claimed for)" "multiplied by $5,000".
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca/child_care_limit_under_seven"},
        consumes={"count": "ca/children_under_seven"},
        produces={"output": "ca/child_care_limit_for_children_under_seven"},
    ),
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca/child_care_limit_disability"},
        consumes={"count": "ca/children_with_disability"},
        produces={"output": "ca/child_care_limit_for_children_with_disability"},
    ),
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca/child_care_limit_seven_to_sixteen"},
        consumes={"count": "ca/children_seven_to_sixteen"},
        produces={"output": "ca/child_care_limit_for_children_seven_to_sixteen"},
    ),
    # T778 line 4 "Add lines 1 to 3.", in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/child_care_limit_for_children_under_seven",
                "ca/child_care_limit_for_children_with_disability",
                "ca/child_care_limit_for_children_seven_to_sixteen",
            )
        },
        produces={"output": "ca/child_care_basic_limit"},
    ),
    # T778 line 6 "Enter your earned income.", "the total of the following: employment
    # income (including tips and gratuities, and the non-taxable part of an allowance
    # received as an emergency volunteer) ...": the employment income, the other earned
    # income lines not triggered; then "multiplied by two-thirds": one part.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/employment_income",)},
        produces={"output": "ca/child_care_earned_income"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/child_care_earned_income_fraction"},
        consumes={"base": "ca/child_care_earned_income"},
        produces={"output": "ca/child_care_earned_income_limit"},
    ),
    # T778 line 7 "Enter whichever amount is the least: line 4, line 5 or line 6.", in that
    # order, line 5 "Enter the amount from line 67950." being the expenses paid; with line 8
    # (the other person with the higher net income) not triggered, line 9 "Line 7 minus line
    # 8. ... enter this amount on line 21400 of your return. Allowable deduction" is line 7.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/child_care_basic_limit",
                "ca/child_care_expenses_paid",
                "ca/child_care_earned_income_limit",
            )
        },
        produces={"output": "ca/child_care_expenses"},
    ),
    # Federal Worksheet "Line 22100 - Carrying charges, interest expenses, and other expenses":
    # line 1 "Total carrying charges", line 2 "Total interest expenses" and line 3 "Total other
    # expenses" (starting amounts), and line 4 "Add lines 1 to 3. Enter this amount on line
    # 22100 of your return.", in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/total_carrying_charges",
                "ca/total_interest_expenses",
                "ca/total_other_expenses",
            )
        },
        produces={"output": "ca/carrying_charges_interest_expenses_and_other_expenses"},
    ),
    # Form T1436 (Capital Gains Worksheet), "Line 21700 – Allowable business investment loss",
    # "Calculating your business investment loss reduction, if any": lines 1 to 6 (the capital
    # gains deductions claimed for 1985 to 1987, for 1988 and 1989 other than for eligible
    # capital property, for 1988 and 1989 for eligible capital property, for 1990 to 1999, for
    # 2000 and for 2001 to 2024) are starting amounts, each as its line prints it after its
    # multiplier (the figures come from the returns of 1985 to 2024); line 7 "Add lines 1 to 6."
    # Total of all capital gains deductions claimed from 1985 to 2024.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/capital_gains_deductions_1985_to_1987",
                "ca/capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property",
                "ca/capital_gains_deductions_1988_and_1989_eligible_capital_property",
                "ca/capital_gains_deductions_1990_to_1999",
                "ca/capital_gains_deductions_2000",
                "ca/capital_gains_deductions_2001_to_2024",
            )
        },
        produces={"output": "ca/capital_gains_deductions_claimed_1985_to_2024"},
    ),
    # Lines 8 to 13 (the amounts of Schedule 3 for 1986 to 1994, 1994 to 1996, 1997 to 1999,
    # 2000, 2001 to 2023 and 2024) are starting amounts; line 14 "Add lines 8 to 13." Total of
    # all other business investment loss reductions for 1986 to 2024.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/other_business_investment_loss_reductions_1986_to_1994",
                "ca/other_business_investment_loss_reductions_1994_to_1996",
                "ca/other_business_investment_loss_reductions_1997_to_1999",
                "ca/other_business_investment_loss_reductions_2000",
                "ca/other_business_investment_loss_reductions_2001_to_2023",
                "ca/other_business_investment_loss_reductions_2024",
            )
        },
        produces={"output": "ca/other_business_investment_loss_reductions_1986_to_2024"},
    ),
    # Line 15 "Line 7 minus line 14" prints no "(if negative, enter "0")", so it may be
    # negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/capital_gains_deductions_claimed_1985_to_2024",
            "less": "ca/other_business_investment_loss_reductions_1986_to_2024",
        },
        produces={"output": "ca/business_investment_loss_reduction_available"},
    ),
    # Line 16 "Business investment loss in 2025 Enter this amount on line 21699 of your return."
    # is a starting amount, the gross of line 21699; line 17 "Enter whichever is less: amount
    # from line 15 or line 16. Enter this amount on line 17800 of Schedule 3." prints no "(if
    # negative, enter "0")" either, so it may be negative with line 15.
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={
            "amounts": (
                "ca/business_investment_loss_reduction_available",
                "ca/business_investment_loss",
            )
        },
        produces={"output": "ca/business_investment_loss_reduction"},
    ),
    # Line 18 "Line 16 minus line 17 Business investment loss reduction": never negative, as
    # line 17 is at most line 16.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/business_investment_loss",
            "less": "ca/business_investment_loss_reduction",
        },
        produces={"output": "ca/business_investment_loss_after_reduction"},
    ),
    # Line 19 "Inclusion rate for 2025 × 50 %", the rate dataset, and line 20 "Line 18
    # multiplied by the percentage on line 19 Enter this amount on line 21700 of your return.
    # Allowable business investment loss".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/business_investment_loss_inclusion_rate"},
        consumes={"base": "ca/business_investment_loss_after_reduction"},
        produces={"output": "ca/allowable_business_investment_loss"},
    ),
    # T1 line 53 and line 23300 "Add lines 35 to 52.": the deductions wired so far in the form's
    # line order (20700, 20800, 20805, 21000, 21200, 21300, 21400, 21700, 22000, 22100, 22200,
    # 22215, 22400, 23200), line 23200 being the caller's other deductions and then the total split
    # income of Form T1206 Part 1 line 4 ("Enter this amount on line 23200 of your return."). Not
    # wired yet: 21500, 21900, 22900 and 23100; lines 20810 and 21999 have no line among lines 35
    # to 52 and nothing on this return reads them.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rpp_deduction",
                "ca/rrsp_deduction",
                "ca/fhsa_deduction",
                "ca/elected_split_pension_deduction",
                "ca/union_dues",
                "ca/uccb_repayment",
                "ca/child_care_expenses",
                "ca/allowable_business_investment_loss",
                "ca/support_payments_deduction",
                "ca/carrying_charges_interest_expenses_and_other_expenses",
                "ca/cpp_deduction_on_self_employment_and_other_earnings",
                "ca/cpp_enhanced_contributions_on_return",
                "ca/exploration_and_development_expenses",
                "ca/other_deductions",
                "ca/total_split_income",
            )
        },
        produces={"output": "ca/deductions_from_total_income"},
    ),
    # T1 line 54 and line 23400 "Line 34 minus line 53 (if negative, show in brackets) Net
    # income before adjustments": total income less total deductions, not floored, so a negative
    # result is shown in brackets.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/total_income", "less": "ca/deductions_from_total_income"},
        produces={"output": "ca/net_income_before_adjustments"},
    ),
    # Federal Worksheet "Line 25000 - Other payments deduction" line 1 "Amount from line 23400 of
    # your return (if negative, enter "0")": line 23400 not below zero, a kind of its own as the
    # net income of line 23600 is now line 23400 less line 23500.
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={"parts": ("ca/net_income_before_adjustments",)},
        produces={"output": "ca/net_income_before_adjustments_not_below_zero"},
    ),
    # Federal Worksheet "Line 23500 - Social benefits repayment": "Complete the chart below if one
    # or both of the following applies:" "You entered an amount on line 11900 of your return and
    # the amount on line 23400 is more than $82,125" and "You entered an amount on line 11300 or
    # line 14600 of your return and the amount on line 23400 is more than $93,454", and T1 line 55
    # and line 23500 "If not, enter "0" on line 23500.": a count of 1 when either holds.
    CapabilitySelection(
        name="ca/count_by_conditions",
        params={"conditions": "ca/social_benefits_repayment_conditions"},
        consumes={
            "counts": (),
            "amounts": (
                "ca/ei_and_other_benefits",
                "ca/net_income_before_adjustments",
                "ca/old_age_security",
                "ca/net_federal_supplements",
            ),
        },
        produces={"output": "ca/social_benefits_repayment_applies"},
    ),
    # Chart line 3 "Line 1 plus line 2 =": line 1 "Old age security (OAS) pension from line 11300
    # of your return" and line 2 "Net federal supplements paid from line 14600 of your return".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/old_age_security", "ca/net_federal_supplements")},
        produces={"output": "ca/oas_and_federal_supplements"},
    ),
    # Line 4 "Overpayment of OAS benefits recovered (box 20 of your T4A(OAS) slip)" is the caller's
    # amount; line 5 "Line 3 minus line 4 (if negative, enter "0") =".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/oas_and_federal_supplements",
            "less": "ca/oas_overpayment_recovered",
        },
        produces={"output": "ca/social_benefits_line_5"},
    ),
    # Line 6 "Net income before adjustments from line 23400 of your return", plus, as Form T1206
    # Part 1 says, "add the amount from line 4 of this form to line 6 of your Federal Worksheet in
    # the calculation of the social benefits repayment for the calculation of lines 23500 and
    # 42200 of your tax return, if applicable": the total split income. It prints no "(if
    # negative, enter "0")", so it is signed.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/net_income_before_adjustments", "ca/total_split_income")},
        produces={"output": "ca/social_benefits_line_6"},
    ),
    # Line 7 "EI benefits repayment from line 4 of the repayment chart on your T4E slip, if any"
    # is the caller's amount; line 8 "Universal child care benefit (UCCB) from line 11700 of your
    # return"; line 9 "Registered disability savings plan (RDSP) income from line 12500 of your
    # return"; line 10 "Add lines 7 to 9. =".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/ei_benefits_repayment",
                "ca/universal_child_care_benefit",
                "ca/rdsp_income",
            )
        },
        produces={"output": "ca/social_benefits_line_10"},
    ),
    # Line 11 "Line 6 minus line 10 =" prints no "(if negative, enter "0")", so it is signed.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/social_benefits_line_6", "less": "ca/social_benefits_line_10"},
        produces={"output": "ca/social_benefits_line_11"},
    ),
    # Line 12 "UCCB repayment from line 21300 of your return" and line 13 "RDSP income repayment
    # (included in the amount on line 23200 of your return)"; line 14 "Line 12 plus line 13 =".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/uccb_repayment", "ca/rdsp_income_repayment")},
        produces={"output": "ca/social_benefits_line_14"},
    ),
    # Line 15 "Line 11 plus line 14 Adjusted net income =", signed.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/social_benefits_line_11", "ca/social_benefits_line_14")},
        produces={"output": "ca/social_benefits_line_15"},
    ),
    # Line 16 "OAS benefits base amount 93,343.00", claimed whole.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/oas_benefits_base_amount"},
        consumes={},
        produces={"output": "ca/oas_benefits_base_amount"},
    ),
    # Line 17 "Line 15 minus line 16 (if negative, enter "0")".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/social_benefits_line_15",
            "less": "ca/oas_benefits_base_amount",
        },
        produces={"output": "ca/social_benefits_line_17"},
    ),
    # Line 18 "Amount from line 17 multiplied by 15% =".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/social_benefits_repayment_rate"},
        consumes={"base": "ca/social_benefits_line_17"},
        produces={"output": "ca/social_benefits_line_18"},
    ),
    # Line 19 "Enter whichever is less: amount from line 5 or line 18."
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/social_benefits_line_5", "ca/social_benefits_line_18")},
        produces={"output": "ca/social_benefits_line_19"},
    ),
    # Line 20 "Amount from line 7, if any" and line 21 "Line 19 plus line 20. Enter this amount on
    # line 23500 and line 42200 of your return. =".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/social_benefits_line_19", "ca/ei_benefits_repayment")},
        produces={"output": "ca/social_benefits_line_21"},
    ),
    # T1 line 55 and line 23500 (the chart's line 21, or "0" "If not"): the chart's result counted
    # once when the chart applies, else 0.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/social_benefits_line_21",
            "count": "ca/social_benefits_repayment_applies",
        },
        produces={"output": "ca/social_benefits_repayment"},
    ),
    # T1 line 56 and line 23600 "Line 54 minus line 55 (if negative, enter "0") If negative, you
    # may have a non-capital loss (see Form T1A) and the negative amount is to be used for certain
    # calculations (go to canada.ca/line-23600) Net income" before its floor: Form T1206 Part 1
    # line 5 reads "Net income from line 23600 of your tax return (or the amount you would have
    # entered if the instructions on line 23600 read "if negative, show in brackets")", which is
    # line 23400 less line 23500, signed.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/net_income_before_adjustments",
            "less": "ca/social_benefits_repayment",
        },
        produces={"output": "ca/net_income_signed"},
    ),
    # Line 56 itself: line 23400 less line 23500, not below zero.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/net_income_before_adjustments",
            "less": "ca/social_benefits_repayment",
        },
        produces={"output": "ca/net_income"},
    ),
    # Form T1206 Part 1 "TOSI-adjusted net income", line 4 (68360) "Total split income: line 1 plus
    # line 3 Enter this amount on line 23200 of your return.": line 1 (68330) "Part of the taxable
    # amount of dividends (eligible and other than eligible) described in the information section
    # received from taxable Canadian corporations" and line 3 "All other split income (see "Split
    # income" on page 1)", the caller's amounts as the form takes them; line 2 (68340) "Part of the
    # taxable amount of dividends other than eligible dividends, included on line 1, from taxable
    # Canadian corporations" is the caller's too and is read by Part 2. Line 4 is a part of the T1
    # line 23300 sum above.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/split_income_dividends",
                "ca/other_split_income",
            )
        },
        produces={"output": "ca/total_split_income"},
    ),
    # Line 5 "Net income from line 23600 of your tax return (or the amount you would have entered if
    # the instructions on line 23600 read "if negative, show in brackets")" is line 23400 less line
    # 23500, signed (`ca/net_income_signed`), and line 6 "TOSI-adjusted net income: line 4 plus
    # line 5 If negative, enter the result in brackets" is their sum, signed.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/total_split_income",
                "ca/net_income_signed",
            )
        },
        produces={"output": "ca/tosi_adjusted_net_income"},
    ),
    # "(If the TOSI–adjusted net income at line 6 is negative, use the negative value when it is
    # part of an adjusted net income calculation, otherwise use zero.)": the same sum, not below
    # zero, for the federal amounts that read it otherwise (the basic personal amount on line 30000,
    # the age amount on line 30100 and line 7 of Schedule 6).
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={
            "parts": (
                "ca/total_split_income",
                "ca/net_income_signed",
            )
        },
        produces={"output": "ca/tosi_adjusted_net_income_not_below_zero"},
    ),
    # Federal Worksheet "Line 25000 - Other payments deduction", "Complete the following
    # calculation if you reported net federal supplements on line 14600 of your return.":
    # line 1 "Amount from line 23400 of your return (if negative, enter "0")" is line 23400
    # floored at 0, not the net income of line 23600; line 4 "Line
    # 2 plus line 3 =" adds line 2 "Amount from line 11700 of your return" (the universal
    # child care benefit) and line 3 "Amount from line 12500 of your return" (the RDSP
    # income), in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/universal_child_care_benefit", "ca/rdsp_income")},
        produces={"output": "ca/uccb_and_rdsp_income"},
    ),
    # Line 5 "Line 1 minus line 4 =" prints no "(if negative, enter "0")", unlike line 1, so
    # it may be negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/net_income_before_adjustments_not_below_zero",
            "less": "ca/uccb_and_rdsp_income",
        },
        produces={"output": "ca/net_income_less_uccb_and_rdsp_income"},
    ),
    # Line 8 "Line 6 plus line 7 =": line 6 "Amount from line 21300 of your return" (the UCCB
    # repayment, a starting amount, also a part of line 23300) and line 7 "RDSP income
    # repayment (included in the amount on line 23200 of your return)", a starting amount of
    # its own that the caller also includes in line 23200, in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/uccb_repayment", "ca/rdsp_income_repayment")},
        produces={"output": "ca/uccb_and_rdsp_income_repayments"},
    ),
    # Line 9 "Line 5 plus line 8 =", the amount the worksheet compares with $93,454.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/net_income_less_uccb_and_rdsp_income",
                "ca/uccb_and_rdsp_income_repayments",
            )
        },
        produces={"output": "ca/other_payments_limit_income"},
    ),
    # "If the amount on line 9 is more than $93,454, go to canada.ca/line-25000 to find out
    # how much you can deduct. Otherwise, enter the amount from line 14700 of your return on
    # line 25000 of your return.": a count of 1 when line 9 is more than $93,454 (a starting
    # count, 0 or 1, until a comparison capability derives it) chooses the amount that chart
    # gives (a starting amount) over line 14700.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/other_payments_worksheet_line_9_over_limit",
            "when_none": "ca/income_support_benefits",
            "when_any": "ca/other_payments_deduction_above_limit",
        },
        produces={"output": "ca/other_payments_deduction_after_limit"},
    ),
    # T1 line 60 and line 25000 "Other payments deduction (enter the amount from line 14700
    # if you did not enter an amount on line 14600; otherwise, use Federal Worksheet)": a
    # count of 1 when an amount was entered on line 14600 (a starting count, 0 or 1, until a
    # comparison capability derives it) chooses the worksheet's result over line 14700.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/other_payments_worksheet_required",
            "when_none": "ca/income_support_benefits",
            "when_any": "ca/other_payments_deduction_after_limit",
        },
        produces={"output": "ca/other_payments_deduction"},
    ),
    # Form T2222 (Northern Residents Deductions) Step 2, "Zone A - Residents of prescribed
    # northern zones", "Basic residency amount" line 1 "Enter the number of days you lived in
    # a prescribed northern zone in 2025. multiplied by $11.00 =" and "Additional residency
    # amount" line 2 "Enter the number of days you qualify for the additional residency
    # amount in 2025. multiplied by $11.00 =": each a count of days (a starting count, the
    # form's) times the yearly $11.00 dataset.
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca/northern_zone_a_daily_amount"},
        consumes={"count": "ca/zone_a_days_lived"},
        produces={"output": "ca/zone_a_basic_residency_amount"},
    ),
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca/northern_zone_a_daily_amount"},
        consumes={"count": "ca/zone_a_additional_residency_days"},
        produces={"output": "ca/zone_a_additional_residency_amount"},
    ),
    # Line 3 and line 67490 "Line 1 plus line 2 =", then line 4 and line 67507 (a starting
    # amount, the non-taxable board and lodging benefits at a special work site, box 31 of
    # the T4 slip or box 124 of the T4A slip) and line 5 "Line 3 minus line 4 (if negative,
    # enter "0") =".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/zone_a_basic_residency_amount",
                "ca/zone_a_additional_residency_amount",
            )
        },
        produces={"output": "ca/zone_a_residency_amount"},
    ),
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/zone_a_residency_amount",
            "less": "ca/zone_a_special_work_site_benefits",
        },
        produces={"output": "ca/zone_a_residency_after_work_site"},
    ),
    # "Zone B - Residents of prescribed intermediate zones": line 6 "Enter the number of days
    # you lived in an intermediate zone in 2025. multiplied by $5.50 =" and line 7 "Enter the
    # number of days you qualify for the additional residency amount in 2025. multiplied by
    # $5.50 =", line 8 and line 67520 "Line 6 plus line 7 =", line 9 and line 67529 (the
    # special work site benefits) and line 10 "Line 8 minus line 9 (if negative, enter "0")
    # =".
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca/northern_zone_b_daily_amount"},
        consumes={"count": "ca/zone_b_days_lived"},
        produces={"output": "ca/zone_b_basic_residency_amount"},
    ),
    CapabilitySelection(
        name="core/per_unit_amount",
        params={"amount": "ca/northern_zone_b_daily_amount"},
        consumes={"count": "ca/zone_b_additional_residency_days"},
        produces={"output": "ca/zone_b_additional_residency_amount"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/zone_b_basic_residency_amount",
                "ca/zone_b_additional_residency_amount",
            )
        },
        produces={"output": "ca/zone_b_residency_amount"},
    ),
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/zone_b_residency_amount",
            "less": "ca/zone_b_special_work_site_benefits",
        },
        produces={"output": "ca/zone_b_residency_after_work_site"},
    ),
    # Line 11 "Line 5 plus line 10 =", line 12 "Enter your net income from line 23600 of your
    # return. multiplied by 20% =" and line 13 "Enter whichever is less: amount from line 11
    # or line 12. Residency deduction".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/zone_a_residency_after_work_site",
                "ca/zone_b_residency_after_work_site",
            )
        },
        produces={"output": "ca/residency_amount"},
    ),
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/northern_residency_rate"},
        consumes={"base": "ca/net_income"},
        produces={"output": "ca/residency_net_income_limit"},
    ),
    CapabilitySelection(
        name="core/lesser_of",
        params={},
        consumes={"amounts": ("ca/residency_amount", "ca/residency_net_income_limit")},
        produces={"output": "ca/residency_deduction"},
    ),
    # Step 3, Chart B: "Enter the lowest amount from column 3, 4, or 5 in the column for the
    # prescribed zone(s) you resided in at the time of the trip.", one record for each trip,
    # then "(A) Total (add all the amounts under Column 6)" and "(B) Total (add all the
    # amounts under Column 7)", line 14 "Amount A of Chart B" being total A.
    CapabilitySelection(
        name="ca/chart_b_zone_a_total",
        params={},
        consumes={"trips": "ca/travel_trips"},
        produces={"total": "ca/travel_total_zone_a"},
    ),
    CapabilitySelection(
        name="ca/chart_b_zone_b_total",
        params={},
        consumes={"trips": "ca/travel_trips"},
        produces={"total": "ca/travel_total_zone_b"},
    ),
    # Chart A, one record for each individual: "Row C: Enter the total of all amounts in row
    # B. This total cannot be more than $1,200.", the $1,200 standard amount from a dataset;
    # nothing else on the form reads it, so its total over the individuals is a manifest
    # output.
    CapabilitySelection(
        name="ca/chart_a_row_c_total",
        params={"maximum": "ca/northern_travel_standard_amount"},
        consumes={"individuals": "ca/travel_individuals"},
        produces={"total": "ca/standard_amount_allocated"},
    ),
    # Line 15 "Enter the total from box B. Line 67560 multiplied by 50% =", line 16 "Line 14
    # plus line 15 Travel deduction =".
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/northern_travel_zone_b_rate"},
        consumes={"base": "ca/travel_total_zone_b"},
        produces={"output": "ca/travel_zone_b_deduction"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/travel_total_zone_a",
                "ca/travel_zone_b_deduction",
            )
        },
        produces={"output": "ca/travel_deduction"},
    ),
    # Step 4: line 17 "Enter the amount from line 13 in Step 2. Residency deduction" and
    # line 18 "Enter the amount from line 16 in Step 3. Travel deduction" are those lines,
    # and line 19 "Line 17 plus line 18 Enter this amount on line 25500 of your return.
    # Northern residents deductions =" adds them in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/residency_deduction",
                "ca/travel_deduction",
            )
        },
        produces={"output": "ca/northern_residents_deductions"},
    ),
}

WIRING = {
    (
        AmountForCount,
        frozenset({CPP_MONTHS}),
        frozenset({CPP_MAXIMUM_PENSIONABLE_EARNINGS}),
    ),
    (
        AmountForCount,
        frozenset({CPP_MONTHS}),
        frozenset({CPP_SECOND_ADDITIONAL_EARNINGS_MAXIMUM}),
    ),
    (
        AmountForCount,
        frozenset({CPP_MONTHS}),
        frozenset({CPP_ADDITIONAL_MAXIMUM_PENSIONABLE_EARNINGS}),
    ),
    (
        AmountForCount,
        frozenset({CPP_MONTHS}),
        frozenset({CPP_BASIC_EXEMPTION}),
    ),
    (
        Sum,
        frozenset({NET_PARTNERSHIP_INCOME, NET_SELF_EMPLOYMENT_INCOME}),
        frozenset({PENSIONABLE_NET_SELF_EMPLOYMENT_EARNINGS}),
    ),
    (
        SumNotBelowZero,
        frozenset({PENSIONABLE_NET_SELF_EMPLOYMENT_EARNINGS, CPT20_EARNINGS}),
        frozenset({CPP_PENSIONABLE_EARNINGS}),
    ),
    (
        LesserOf,
        frozenset({CPP_ADDITIONAL_MAXIMUM_PENSIONABLE_EARNINGS, CPP_PENSIONABLE_EARNINGS}),
        frozenset({CPP_PENSIONABLE_EARNINGS_UP_TO_ADDITIONAL_MAXIMUM}),
    ),
    (
        SubtractNotBelowZero,
        frozenset(
            {
                CPP_PENSIONABLE_EARNINGS_UP_TO_ADDITIONAL_MAXIMUM,
                CPP_MAXIMUM_PENSIONABLE_EARNINGS,
            }
        ),
        frozenset({CPP_EARNINGS_SUBJECT_TO_SECOND_ADDITIONAL}),
    ),
    (
        SubtractNotBelowZero,
        frozenset(
            {
                CPP_PENSIONABLE_EARNINGS_UP_TO_ADDITIONAL_MAXIMUM,
                CPP_EARNINGS_SUBJECT_TO_SECOND_ADDITIONAL,
            }
        ),
        frozenset({CPP_EARNINGS_UP_TO_MAXIMUM}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({CPP_EARNINGS_UP_TO_MAXIMUM, CPP_BASIC_EXEMPTION}),
        frozenset({CPP_EARNINGS_SUBJECT_TO_BASE_AND_FIRST_ADDITIONAL}),
    ),
    (
        TieredContribution,
        frozenset({CPP_EARNINGS_SUBJECT_TO_BASE_AND_FIRST_ADDITIONAL}),
        frozenset({SELF_EMPLOYED_CPP_BASE_CONTRIBUTIONS}),
    ),
    (
        TieredContribution,
        frozenset({CPP_EARNINGS_SUBJECT_TO_BASE_AND_FIRST_ADDITIONAL}),
        frozenset({SELF_EMPLOYED_CPP_FIRST_ADDITIONAL_CONTRIBUTIONS}),
    ),
    (
        TieredContribution,
        frozenset({CPP_EARNINGS_SUBJECT_TO_SECOND_ADDITIONAL}),
        frozenset({SELF_EMPLOYED_CPP_SECOND_ADDITIONAL_CONTRIBUTIONS}),
    ),
    (
        Sum,
        frozenset(
            {
                SELF_EMPLOYED_CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
                SELF_EMPLOYED_CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
            }
        ),
        frozenset({SELF_EMPLOYED_CPP_ENHANCED_CONTRIBUTIONS}),
    ),
    (
        Sum,
        frozenset({SELF_EMPLOYED_CPP_BASE_CONTRIBUTIONS, SELF_EMPLOYED_CPP_ENHANCED_CONTRIBUTIONS}),
        frozenset({SELF_EMPLOYED_CPP_CONTRIBUTIONS_PAYABLE}),
    ),
    (
        ApplyRate,
        frozenset({SELF_EMPLOYED_CPP_BASE_CONTRIBUTIONS}),
        frozenset({SELF_EMPLOYED_CPP_BASE_CREDIT}),
    ),
    (
        Sum,
        frozenset({SELF_EMPLOYED_CPP_BASE_CREDIT, SELF_EMPLOYED_CPP_ENHANCED_CONTRIBUTIONS}),
        frozenset({SELF_EMPLOYED_CPP_DEDUCTION}),
    ),
    (
        TimesCount,
        frozenset({SELF_EMPLOYED_CPP_DEDUCTION, CPP_PART_4_COMPLETED}),
        frozenset({CPP_DEDUCTION_ON_SELF_EMPLOYMENT}),
    ),
    (
        TimesCount,
        frozenset({CPP_PART_5_LINE_88, CPP_PART_5_COMPLETED}),
        frozenset({CPP_PART_5_DEDUCTION_ON_SELF_EMPLOYMENT}),
    ),
    (
        Sum,
        frozenset(
            {
                CPP_DEDUCTION_ON_SELF_EMPLOYMENT,
                CPP_PART_5_DEDUCTION_ON_SELF_EMPLOYMENT,
                RC381_CPP_DEDUCTION_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
            }
        ),
        frozenset({CPP_DEDUCTION_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS}),
    ),
    (
        Sum,
        frozenset({NET_PARTNERSHIP_INCOME, NET_SELF_EMPLOYMENT_INCOME}),
        frozenset({EI_SELF_EMPLOYMENT_BEFORE_SLIPS}),
    ),
    (
        EiExcludedSlipsNetIncome,
        frozenset({EI_EXCLUDED_SLIPS}),
        frozenset({EI_EXCLUDED_SLIPS_NET_INCOME}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({EI_SELF_EMPLOYMENT_BEFORE_SLIPS, EI_EXCLUDED_SLIPS_NET_INCOME}),
        frozenset({EI_SELF_EMPLOYMENT_EARNINGS}),
    ),
    (
        Sum,
        frozenset(
            {
                EI_SELF_EMPLOYMENT_EARNINGS,
                EI_CONTROLLED_CORPORATION_EARNINGS,
                EI_EXEMPT_SELF_EMPLOYMENT_INCOME,
            }
        ),
        frozenset({EI_NET_SELF_EMPLOYMENT_INCOME}),
    ),
    (
        CreditAmount,
        frozenset(),
        frozenset({EI_MAXIMUM_INSURABLE_EARNINGS}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({EI_MAXIMUM_INSURABLE_EARNINGS, EI_INSURABLE_EARNINGS}),
        frozenset({EI_INSURABLE_EARNINGS_REMAINING}),
    ),
    (
        LesserOf,
        frozenset({EI_NET_SELF_EMPLOYMENT_INCOME, EI_INSURABLE_EARNINGS_REMAINING}),
        frozenset({EI_EARNINGS_SUBJECT_TO_PREMIUM}),
    ),
    (
        TieredContribution,
        frozenset({EI_EARNINGS_SUBJECT_TO_PREMIUM}),
        frozenset({SELF_EMPLOYED_EI_PREMIUMS}),
    ),
    (
        PerUnitAmount,
        frozenset({CHILDREN_UNDER_SEVEN}),
        frozenset({CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN}),
    ),
    (
        PerUnitAmount,
        frozenset({CHILDREN_WITH_DISABILITY}),
        frozenset({CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY}),
    ),
    (
        PerUnitAmount,
        frozenset({CHILDREN_SEVEN_TO_SIXTEEN}),
        frozenset({CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN}),
    ),
    (
        Sum,
        frozenset(
            {
                CHILD_CARE_LIMIT_FOR_CHILDREN_UNDER_SEVEN,
                CHILD_CARE_LIMIT_FOR_CHILDREN_WITH_DISABILITY,
                CHILD_CARE_LIMIT_FOR_CHILDREN_SEVEN_TO_SIXTEEN,
            }
        ),
        frozenset({CHILD_CARE_BASIC_LIMIT}),
    ),
    (Sum, frozenset({EMPLOYMENT_INCOME}), frozenset({CHILD_CARE_EARNED_INCOME})),
    (
        ApplyFraction,
        frozenset({CHILD_CARE_EARNED_INCOME}),
        frozenset({CHILD_CARE_EARNED_INCOME_LIMIT}),
    ),
    (
        LesserOf,
        frozenset(
            {CHILD_CARE_BASIC_LIMIT, CHILD_CARE_EXPENSES_PAID, CHILD_CARE_EARNED_INCOME_LIMIT}
        ),
        frozenset({CHILD_CARE_EXPENSES}),
    ),
    (
        Sum,
        frozenset({TOTAL_CARRYING_CHARGES, TOTAL_INTEREST_EXPENSES, TOTAL_OTHER_EXPENSES}),
        frozenset({CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES}),
    ),
    (
        Sum,
        frozenset(
            {
                CAPITAL_GAINS_DEDUCTIONS_1985_TO_1987,
                CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_OTHER_THAN_ELIGIBLE_CAPITAL_PROPERTY,
                CAPITAL_GAINS_DEDUCTIONS_1988_AND_1989_ELIGIBLE_CAPITAL_PROPERTY,
                CAPITAL_GAINS_DEDUCTIONS_1990_TO_1999,
                CAPITAL_GAINS_DEDUCTIONS_2000,
                CAPITAL_GAINS_DEDUCTIONS_2001_TO_2024,
            }
        ),
        frozenset({CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024}),
    ),
    (
        Sum,
        frozenset(
            {
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_1994,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1994_TO_1996,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1997_TO_1999,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2000,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2001_TO_2023,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_2024,
            }
        ),
        frozenset({OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024}),
    ),
    (
        Subtract,
        frozenset(
            {
                CAPITAL_GAINS_DEDUCTIONS_CLAIMED_1985_TO_2024,
                OTHER_BUSINESS_INVESTMENT_LOSS_REDUCTIONS_1986_TO_2024,
            }
        ),
        frozenset({BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE}),
    ),
    (
        LesserOf,
        frozenset({BUSINESS_INVESTMENT_LOSS_REDUCTION_AVAILABLE, BUSINESS_INVESTMENT_LOSS}),
        frozenset({BUSINESS_INVESTMENT_LOSS_REDUCTION}),
    ),
    (
        Subtract,
        frozenset({BUSINESS_INVESTMENT_LOSS, BUSINESS_INVESTMENT_LOSS_REDUCTION}),
        frozenset({BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION}),
    ),
    (
        ApplyRate,
        frozenset({BUSINESS_INVESTMENT_LOSS_AFTER_REDUCTION}),
        frozenset({ALLOWABLE_BUSINESS_INVESTMENT_LOSS}),
    ),
    (
        Sum,
        frozenset(
            {
                RPP_DEDUCTION,
                RRSP_DEDUCTION,
                FHSA_DEDUCTION,
                ELECTED_SPLIT_PENSION_DEDUCTION,
                UNION_DUES,
                UCCB_REPAYMENT,
                CHILD_CARE_EXPENSES,
                ALLOWABLE_BUSINESS_INVESTMENT_LOSS,
                SUPPORT_PAYMENTS_DEDUCTION,
                CARRYING_CHARGES_INTEREST_EXPENSES_AND_OTHER_EXPENSES,
                CPP_DEDUCTION_ON_SELF_EMPLOYMENT_AND_OTHER_EARNINGS,
                CPP_ENHANCED_CONTRIBUTIONS_ON_RETURN,
                EXPLORATION_AND_DEVELOPMENT_EXPENSES,
                OTHER_DEDUCTIONS,
                TOTAL_SPLIT_INCOME,
            }
        ),
        frozenset({DEDUCTIONS_FROM_TOTAL_INCOME}),
    ),
    (
        Subtract,
        frozenset({TOTAL_INCOME, DEDUCTIONS_FROM_TOTAL_INCOME}),
        frozenset({NET_INCOME_BEFORE_ADJUSTMENTS}),
    ),
    (
        SumNotBelowZero,
        frozenset({NET_INCOME_BEFORE_ADJUSTMENTS}),
        frozenset({NET_INCOME_BEFORE_ADJUSTMENTS_NOT_BELOW_ZERO}),
    ),
    (
        CountByConditions,
        frozenset(
            {
                EI_AND_OTHER_BENEFITS,
                NET_INCOME_BEFORE_ADJUSTMENTS,
                OLD_AGE_SECURITY,
                NET_FEDERAL_SUPPLEMENTS,
            }
        ),
        frozenset({SOCIAL_BENEFITS_REPAYMENT_APPLIES}),
    ),
    (
        Sum,
        frozenset({OLD_AGE_SECURITY, NET_FEDERAL_SUPPLEMENTS}),
        frozenset({OAS_AND_FEDERAL_SUPPLEMENTS}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({OAS_AND_FEDERAL_SUPPLEMENTS, OAS_OVERPAYMENT_RECOVERED}),
        frozenset({SOCIAL_BENEFITS_LINE_5}),
    ),
    (
        Sum,
        frozenset({NET_INCOME_BEFORE_ADJUSTMENTS, TOTAL_SPLIT_INCOME}),
        frozenset({SOCIAL_BENEFITS_LINE_6}),
    ),
    (
        Sum,
        frozenset({EI_BENEFITS_REPAYMENT, UNIVERSAL_CHILD_CARE_BENEFIT, RDSP_INCOME}),
        frozenset({SOCIAL_BENEFITS_LINE_10}),
    ),
    (
        Subtract,
        frozenset({SOCIAL_BENEFITS_LINE_6, SOCIAL_BENEFITS_LINE_10}),
        frozenset({SOCIAL_BENEFITS_LINE_11}),
    ),
    (
        Sum,
        frozenset({UCCB_REPAYMENT, RDSP_INCOME_REPAYMENT}),
        frozenset({SOCIAL_BENEFITS_LINE_14}),
    ),
    (
        Sum,
        frozenset({SOCIAL_BENEFITS_LINE_11, SOCIAL_BENEFITS_LINE_14}),
        frozenset({SOCIAL_BENEFITS_LINE_15}),
    ),
    (CreditAmount, frozenset(), frozenset({OAS_BENEFITS_BASE_AMOUNT})),
    (
        SubtractNotBelowZero,
        frozenset({SOCIAL_BENEFITS_LINE_15, OAS_BENEFITS_BASE_AMOUNT}),
        frozenset({SOCIAL_BENEFITS_LINE_17}),
    ),
    (ApplyRate, frozenset({SOCIAL_BENEFITS_LINE_17}), frozenset({SOCIAL_BENEFITS_LINE_18})),
    (
        LesserOf,
        frozenset({SOCIAL_BENEFITS_LINE_5, SOCIAL_BENEFITS_LINE_18}),
        frozenset({SOCIAL_BENEFITS_LINE_19}),
    ),
    (
        Sum,
        frozenset({SOCIAL_BENEFITS_LINE_19, EI_BENEFITS_REPAYMENT}),
        frozenset({SOCIAL_BENEFITS_LINE_21}),
    ),
    (
        TimesCount,
        frozenset({SOCIAL_BENEFITS_LINE_21, SOCIAL_BENEFITS_REPAYMENT_APPLIES}),
        frozenset({SOCIAL_BENEFITS_REPAYMENT}),
    ),
    (
        Subtract,
        frozenset({NET_INCOME_BEFORE_ADJUSTMENTS, SOCIAL_BENEFITS_REPAYMENT}),
        frozenset({NET_INCOME_SIGNED}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({NET_INCOME_BEFORE_ADJUSTMENTS, SOCIAL_BENEFITS_REPAYMENT}),
        frozenset({NET_INCOME}),
    ),
    (
        Sum,
        frozenset({SPLIT_INCOME_DIVIDENDS, OTHER_SPLIT_INCOME}),
        frozenset({TOTAL_SPLIT_INCOME}),
    ),
    (
        Sum,
        frozenset({TOTAL_SPLIT_INCOME, NET_INCOME_SIGNED}),
        frozenset({TOSI_ADJUSTED_NET_INCOME}),
    ),
    (
        SumNotBelowZero,
        frozenset({TOTAL_SPLIT_INCOME, NET_INCOME_SIGNED}),
        frozenset({TOSI_ADJUSTED_NET_INCOME_NOT_BELOW_ZERO}),
    ),
    (
        Sum,
        frozenset({UNIVERSAL_CHILD_CARE_BENEFIT, RDSP_INCOME}),
        frozenset({UCCB_AND_RDSP_INCOME}),
    ),
    (
        Subtract,
        frozenset({NET_INCOME_BEFORE_ADJUSTMENTS_NOT_BELOW_ZERO, UCCB_AND_RDSP_INCOME}),
        frozenset({NET_INCOME_LESS_UCCB_AND_RDSP_INCOME}),
    ),
    (
        Sum,
        frozenset({UCCB_REPAYMENT, RDSP_INCOME_REPAYMENT}),
        frozenset({UCCB_AND_RDSP_INCOME_REPAYMENTS}),
    ),
    (
        Sum,
        frozenset({NET_INCOME_LESS_UCCB_AND_RDSP_INCOME, UCCB_AND_RDSP_INCOME_REPAYMENTS}),
        frozenset({OTHER_PAYMENTS_LIMIT_INCOME}),
    ),
    (
        ChooseByCount,
        frozenset(
            {
                OTHER_PAYMENTS_WORKSHEET_LINE_9_OVER_LIMIT,
                INCOME_SUPPORT_BENEFITS,
                OTHER_PAYMENTS_DEDUCTION_ABOVE_LIMIT,
            }
        ),
        frozenset({OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT}),
    ),
    (
        ChooseByCount,
        frozenset(
            {
                OTHER_PAYMENTS_WORKSHEET_REQUIRED,
                INCOME_SUPPORT_BENEFITS,
                OTHER_PAYMENTS_DEDUCTION_AFTER_LIMIT,
            }
        ),
        frozenset({OTHER_PAYMENTS_DEDUCTION}),
    ),
    (
        PerUnitAmount,
        frozenset({ZONE_A_DAYS_LIVED}),
        frozenset({ZONE_A_BASIC_RESIDENCY_AMOUNT}),
    ),
    (
        PerUnitAmount,
        frozenset({ZONE_A_ADDITIONAL_RESIDENCY_DAYS}),
        frozenset({ZONE_A_ADDITIONAL_RESIDENCY_AMOUNT}),
    ),
    (
        Sum,
        frozenset({ZONE_A_BASIC_RESIDENCY_AMOUNT, ZONE_A_ADDITIONAL_RESIDENCY_AMOUNT}),
        frozenset({ZONE_A_RESIDENCY_AMOUNT}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({ZONE_A_RESIDENCY_AMOUNT, ZONE_A_SPECIAL_WORK_SITE_BENEFITS}),
        frozenset({ZONE_A_RESIDENCY_AFTER_WORK_SITE}),
    ),
    (
        PerUnitAmount,
        frozenset({ZONE_B_DAYS_LIVED}),
        frozenset({ZONE_B_BASIC_RESIDENCY_AMOUNT}),
    ),
    (
        PerUnitAmount,
        frozenset({ZONE_B_ADDITIONAL_RESIDENCY_DAYS}),
        frozenset({ZONE_B_ADDITIONAL_RESIDENCY_AMOUNT}),
    ),
    (
        Sum,
        frozenset({ZONE_B_BASIC_RESIDENCY_AMOUNT, ZONE_B_ADDITIONAL_RESIDENCY_AMOUNT}),
        frozenset({ZONE_B_RESIDENCY_AMOUNT}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({ZONE_B_RESIDENCY_AMOUNT, ZONE_B_SPECIAL_WORK_SITE_BENEFITS}),
        frozenset({ZONE_B_RESIDENCY_AFTER_WORK_SITE}),
    ),
    (
        Sum,
        frozenset({ZONE_A_RESIDENCY_AFTER_WORK_SITE, ZONE_B_RESIDENCY_AFTER_WORK_SITE}),
        frozenset({RESIDENCY_AMOUNT}),
    ),
    (ApplyRate, frozenset({NET_INCOME}), frozenset({RESIDENCY_NET_INCOME_LIMIT})),
    (
        LesserOf,
        frozenset({RESIDENCY_AMOUNT, RESIDENCY_NET_INCOME_LIMIT}),
        frozenset({RESIDENCY_DEDUCTION}),
    ),
    (ChartBZoneATotal, frozenset({TRAVEL_TRIPS}), frozenset({TRAVEL_TOTAL_ZONE_A})),
    (ChartBZoneBTotal, frozenset({TRAVEL_TRIPS}), frozenset({TRAVEL_TOTAL_ZONE_B})),
    (ChartARowCTotal, frozenset({TRAVEL_INDIVIDUALS}), frozenset({STANDARD_AMOUNT_ALLOCATED})),
    (ApplyRate, frozenset({TRAVEL_TOTAL_ZONE_B}), frozenset({TRAVEL_ZONE_B_DEDUCTION})),
    (
        Sum,
        frozenset({TRAVEL_TOTAL_ZONE_A, TRAVEL_ZONE_B_DEDUCTION}),
        frozenset({TRAVEL_DEDUCTION}),
    ),
    (
        Sum,
        frozenset({RESIDENCY_DEDUCTION, TRAVEL_DEDUCTION}),
        frozenset({NORTHERN_RESIDENTS_DEDUCTIONS}),
    ),
}
