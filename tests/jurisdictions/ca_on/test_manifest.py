"""The CA-ON manifest: what it selects, and that production code builds it into a composition.

Building it through `TaxComputationService.compose` resolves every slot: each capability name to a
registered class, each parameter slot's family to a dataset of the slot's kind for the tax year,
and each artifact identifier to a registered kind of the slot's value type.
"""

from __future__ import annotations

import app.registrations  # lists the packages; build_tax_computation registers their catalogs
from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.application.services.tax_computation import TaxComputationService
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
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Manifest
from app.jurisdictions.ca.catalog import (
    ADDITIONAL_DEDUCTIONS,
    ADJUSTED_FAMILY_NET_INCOME,
    AGE_AMOUNT,
    AGE_AMOUNT_BEFORE_COUNT,
    AGE_INCOME_OVER_THRESHOLD,
    AGE_INCOME_THRESHOLD,
    AGE_MAXIMUM,
    AGE_REDUCTION,
    BASIC_PERSONAL_AMOUNT,
    BORN_IN_1960_OR_EARLIER,
    CANADA_EMPLOYMENT_AMOUNT,
    CANADA_WORKERS_BENEFIT,
    CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
    CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
    CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
    CAPITAL_GAIN,
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
    CPP_BASE_CONTRIBUTIONS,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_OR_QPP_BENEFITS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
    CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
    CWB_ELIGIBLE_DEPENDANTS,
    CWB_REDUCTION_WITH_DEPENDANT,
    CWB_REDUCTION_WITHOUT_DEPENDANT,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    DEPENDANT_NET_INCOME,
    DIVIDEND_TAX_CREDIT,
    DIVIDENDS_AMOUNT_A,
    DIVIDENDS_AMOUNT_A_LESS_B,
    DIVIDENDS_AMOUNT_B,
    DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
    EI_AND_OTHER_BENEFITS,
    EI_PREMIUMS,
    ELECTED_SPLIT_PENSION_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
    ELIGIBLE_DEPENDANTS,
    ELIGIBLE_DIVIDENDS_CREDIT,
    ELIGIBLE_DIVIDENDS_GROSSED_UP,
    ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    EMPLOYMENT_INCOME,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    FHSA_INCOME,
    FOREIGN_INVESTMENT_INCOME,
    INCOME_SUPPORT_BENEFITS,
    INCOME_TAX_DEDUCTED,
    INFIRM_CHILDREN,
    INFIRM_CHILDREN_AMOUNT,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
    INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
    INVESTMENT_INCOME_WITHOUT_A_SLIP,
    INVESTMENT_ROYALTIES,
    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
    NET_FEDERAL_SUPPLEMENTS,
    NET_FEDERAL_TAX,
    NET_INCOME,
    NET_INCOME_LESS_UCCB_AND_RDSP_INCOME,
    NET_PARTNERSHIP_INCOME,
    NO_SLIP_DIVIDEND_TAX_CREDIT,
    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    OLD_AGE_SECURITY,
    OTHER_DIVIDENDS_CREDIT,
    OTHER_DIVIDENDS_GROSSED_UP,
    OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
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
    PROVINCIAL_CREDITS,
    RDSP_INCOME,
    RDSP_INCOME_REPAYMENT,
    REFUND_OR_BALANCE_OWING,
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
    TAX_REFUND_INTEREST,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_DIVIDENDS,
    TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TAXABLE_INCOME,
    TAXABLE_SCHOLARSHIPS,
    TAXABLE_SUPPORT_PAYMENTS,
    TOTAL_CREDITS,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
    UCCB_AND_RDSP_INCOME,
    UCCB_AND_RDSP_INCOME_REPAYMENTS,
    UCCB_REPAYMENT,
    UNION_DUES,
    UNIVERSAL_CHILD_CARE_BENEFIT,
    UNUSED_RRSP_CONTRIBUTIONS,
    UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
    WORKERS_COMPENSATION_BENEFITS,
    WORKING_INCOME,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.capabilities.flow_through_share_expenses import (
    FlowThroughShareExpenses,
)
from app.jurisdictions.ca_on.catalog import (
    COMMUNITY_FOOD_PROGRAM_CREDIT,
    COMMUNITY_FOOD_PROGRAM_DONATIONS,
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
    ELIGIBLE_DEPENDANT_BASE,
    FERTILITY_CREDIT,
    FERTILITY_CREDIT_BEFORE_MAXIMUM,
    FERTILITY_EXPENSES,
    FLOW_THROUGH_SHARE_CREDIT,
    FLOW_THROUGH_SHARE_EXPENSES,
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
    ONTARIO_TAX_AFTER_DIVIDEND_CREDIT,
    ONTARIO_TAX_AFTER_FOOD_CREDIT,
    ONTARIO_TAX_AFTER_LIFT_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
    ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT,
    ONTARIO_TAX_LESS_DIVIDEND_CREDIT,
    ONTARIO_TAX_REDUCTION,
    ONTARIO_TAX_WITH_SURTAX,
    SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM,
    SENIORS_TRANSIT_CREDIT,
    SENIORS_TRANSIT_PAID,
    TAX_REDUCTION_AMOUNTS,
    TAX_REDUCTION_BASIC,
    TAX_REDUCTION_FOR_CHILDREN,
    TAX_REDUCTION_FOR_DEPENDANTS,
)
from app.main import build_tax_computation

ROOTS = app.registrations.JURISDICTIONS.roots()
CA_ON = JurisdictionCode("CA-ON")


def manifest() -> Manifest:
    (only,) = YamlJurisdictionSource(ROOTS).get_jurisdiction(CA_ON).manifests
    return only


def service() -> TaxComputationService:
    return build_tax_computation()


def test_ca_on_has_one_manifest_from_2025() -> None:
    found = manifest()

    assert found.jurisdiction == CA_ON
    assert found.version == 1
    assert found.valid_from_tax_year == 2025
    assert found.inputs == frozenset(
        {
            "ca/employment_income",
            "ca/capital_gain",
            "ca/other_employment_income",
            "ca/old_age_security",
            "ca/cpp_or_qpp_benefits",
            "ca/other_pensions_and_superannuation",
            "ca/elected_split_pension_amount",
            "ca/universal_child_care_benefit",
            "ca/ei_and_other_benefits",
            "ca/t3_taxable_dividends_other_than_eligible",
            "ca/t4ps_taxable_dividends_other_than_eligible",
            "ca/t5_taxable_dividends_other_than_eligible",
            "ca/t5013_taxable_dividends_other_than_eligible",
            "ca/t3_taxable_dividends",
            "ca/t4ps_taxable_dividends",
            "ca/t5_taxable_dividends",
            "ca/t5013_taxable_dividends",
            "ca/eligible_dividends_received_without_a_slip",
            "ca/other_dividends_received_without_a_slip",
            "ca/t3_dividend_tax_credit",
            "ca/t4ps_dividend_tax_credit",
            "ca/t5_dividend_tax_credit",
            "ca/t5013_dividend_tax_credit",
            "ca/t3_investment_income",
            "ca/t5_investment_income",
            "ca/t5013_investment_income",
            "ca/investment_income_credited_not_received",
            "ca/tax_refund_interest",
            "ca/foreign_investment_income",
            "ca/investment_income_without_a_slip",
            "ca/investment_royalties",
            "ca/investment_income_reported_in_previous_years",
            "ca/net_partnership_income",
            "ca/rdsp_income",
            "ca/taxable_support_payments",
            "ca/rrsp_income",
            "ca/fhsa_income",
            "ca/other_fhsa_income",
            "ca/other_income",
            "ca/taxable_scholarships",
            "ca/workers_compensation_benefits",
            "ca/social_assistance_payments",
            "ca/net_federal_supplements",
            "ca/uccb_repayment",
            "ca/rdsp_income_repayment",
            "ca/canadian_armed_forces_and_police_deduction",
            "ca/security_options_deductions",
            "ca/limited_partnership_losses_of_other_years",
            "ca/non_capital_losses_of_other_years",
            "ca/additional_deductions",
            "ca/other_payments_deduction_above_limit",
            "ca/other_payments_worksheet_required",
            "ca/other_payments_worksheet_line_9_over_limit",
            "ca/unused_rrsp_contributions",
            "ca/rrsp_contributions",
            "ca/rrsp_deduction_limit",
            "ca/rrsp_amount_deducted",
            "ca/union_dues",
            "ca-on/dependent_children",
            "ca-on/dependants",
            "ca/eligible_dependants",
            "ca/dependant_net_income",
            "ca/infirm_children",
            "ca/born_in_1960_or_earlier",
            "ca/spouse_net_income",
            "ca/spouses_claimed",
            "ca/spouse_caregiver_eligible",
            "ca/child_care_expenses_paid",
            "ca/children_under_seven",
            "ca/children_with_disability",
            "ca/children_seven_to_sixteen",
            "ca/cwb_eligible_dependants",
            "ca/income_tax_deducted",
            "ca-on/fertility_expenses",
            "ca-on/seniors_transit_paid",
            "ca-on/flow_through_share_slips",
            "ca-on/community_food_program_donations",
        }
    )
    # T1 line 167, the refund or balance owing, Schedule 7 line 23, what the return produces for
    # the next year's line 1, line 12010, the amount of dividends other than eligible, which
    # nothing else on the return reads; the Federal Worksheet's "Line 25000 - Other payments
    # deduction" line 9 "Line 5 plus line 8 =", which nothing consumes while the count of line 9
    # over $93,454 is a starting count; and ON428 line 58, the Ontario tax less the dividend tax
    # credit, which nothing else on the return reads (the surtax and line 69 read line 53; line
    # 60, the minimum tax carryover, is not modelled): the lines the computation returns.
    assert found.outputs == frozenset(
        {
            "ca/refund_or_balance_owing",
            "ca/unused_rrsp_contributions_carried_forward",
            "ca/taxable_dividends_other_than_eligible",
            "ca/other_payments_limit_income",
            "ca-on/ontario_tax_less_dividend_credit",
        }
    )
    # List order carries no meaning: the composition derives the run order from the contracts.
    assert set(found.capabilities) == {
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/capital_gains_inclusion_rate"},
            consumes={"base": "ca/capital_gain"},
            produces={"output": "ca/taxable_capital_gains"},
        ),
        # T1 line 9 (12000) "Amount of dividends (eligible and other than eligible)" and line
        # 12010 "Amount of dividends (other than eligible)" (use Federal Worksheet): the Federal
        # Worksheet's "Lines 12000 and 12010 - Taxable amount of dividends from taxable Canadian
        # corporations", line 5 "Add lines 1 to 4. Enter this amount on line 12010 of your
        # return." (the T3, T4PS, T5 and T5013 slip boxes of lines 1 to 4) and line 10 "Add lines
        # 6 to 9. Enter this amount on line 12000 of your return." (lines 6 to 9). For dividends
        # with no information slip, line 11 "Actual amount of eligible dividends received" and
        # line 12 "Applicable rate 138%" give line 13 "Line 11 multiplied by the percentage from
        # line 12"; line 14 "Actual amount of dividends other than eligible dividends received"
        # and line 15 "Applicable rate 115%" give line 16 "Line 14 multiplied by the percentage
        # from line 15 Include this amount on line 12010 of your return."; line 17 "Line 13 plus
        # line 16. Include this amount on line 12000 of your return." The rates are above one, so
        # they are fractions, not rates. Line 12010 is line 5 plus line 16 and line 12000 is line
        # 10 plus line 17.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/t3_taxable_dividends_other_than_eligible",
                    "ca/t4ps_taxable_dividends_other_than_eligible",
                    "ca/t5_taxable_dividends_other_than_eligible",
                    "ca/t5013_taxable_dividends_other_than_eligible",
                )
            },
            produces={"output": "ca/slip_taxable_dividends_other_than_eligible"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/t3_taxable_dividends",
                    "ca/t4ps_taxable_dividends",
                    "ca/t5_taxable_dividends",
                    "ca/t5013_taxable_dividends",
                )
            },
            produces={"output": "ca/slip_taxable_dividends"},
        ),
        CapabilitySelection(
            name="core/apply_fraction",
            params={"fraction": "ca/eligible_dividend_gross_up"},
            consumes={"base": "ca/eligible_dividends_received_without_a_slip"},
            produces={"output": "ca/eligible_dividends_grossed_up"},
        ),
        CapabilitySelection(
            name="core/apply_fraction",
            params={"fraction": "ca/other_dividend_gross_up"},
            consumes={"base": "ca/other_dividends_received_without_a_slip"},
            produces={"output": "ca/other_dividends_grossed_up"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca/eligible_dividends_grossed_up", "ca/other_dividends_grossed_up")
            },
            produces={"output": "ca/dividends_without_a_slip_grossed_up"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/slip_taxable_dividends_other_than_eligible",
                    "ca/other_dividends_grossed_up",
                )
            },
            produces={"output": "ca/taxable_dividends_other_than_eligible"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca/slip_taxable_dividends", "ca/dividends_without_a_slip_grossed_up")
            },
            produces={"output": "ca/taxable_dividends"},
        ),
        # T1 Step 2 line 10 (12100) "Interest and other investment income (use Federal
        # Worksheet)": the Federal Worksheet's "Line 12100 - Interest and other investment
        # income" line 9 "Add lines 1 to 8.", in line order, then line 11 "Line 9 minus line
        # 10. Enter this amount on line 12100 of your return." with line 10 "Interest and other
        # investment income, included on line 9, received and reported in previous years".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/t3_investment_income",
                    "ca/t5_investment_income",
                    "ca/t5013_investment_income",
                    "ca/investment_income_credited_not_received",
                    "ca/tax_refund_interest",
                    "ca/foreign_investment_income",
                    "ca/investment_income_without_a_slip",
                    "ca/investment_royalties",
                )
            },
            produces={"output": "ca/investment_income_before_prior_years"},
        ),
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={
                "amount": "ca/investment_income_before_prior_years",
                "less": "ca/investment_income_reported_in_previous_years",
            },
            produces={"output": "ca/interest_and_other_investment_income"},
        ),
        # T1 line 32 and line 14700 "Add lines 29 to 31 (see line 25000 in Step 4).": workers'
        # compensation benefits (14400), social assistance payments (14500) and net federal
        # supplements paid (14600), in line order.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/workers_compensation_benefits",
                    "ca/social_assistance_payments",
                    "ca/net_federal_supplements",
                )
            },
            produces={"output": "ca/income_support_benefits"},
        ),
        # T1 line 33 and line 15000 "Line 28 plus line 32 Total income": every income line the
        # return lists, in line order (lines 1 to 20, here with the amount of dividends of line
        # 9 (12000), the taxable capital gains of line 14 and the taxable support payments of
        # line 15, then line 32); rental income (line 13) and self-employment income (lines 22
        # to 26) are not wired yet.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/employment_income",
                    "ca/other_employment_income",
                    "ca/old_age_security",
                    "ca/cpp_or_qpp_benefits",
                    "ca/other_pensions_and_superannuation",
                    "ca/elected_split_pension_amount",
                    "ca/universal_child_care_benefit",
                    "ca/ei_and_other_benefits",
                    "ca/taxable_dividends",
                    "ca/interest_and_other_investment_income",
                    "ca/net_partnership_income",
                    "ca/rdsp_income",
                    "ca/taxable_capital_gains",
                    "ca/taxable_support_payments",
                    "ca/rrsp_income",
                    "ca/fhsa_income",
                    "ca/other_fhsa_income",
                    "ca/other_income",
                    "ca/taxable_scholarships",
                    "ca/income_support_benefits",
                )
            },
            produces={"output": "ca/total_income"},
        ),
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
        CapabilitySelection(
            name="core/contribution_tier",
            params={"tier": "ca/cpp_first_additional_contribution"},
            consumes={"earnings": "ca/employment_income"},
            produces={"output": "ca/cpp_first_additional_contributions"},
        ),
        CapabilitySelection(
            name="core/contribution_tier",
            params={"tier": "ca/cpp_second_additional_contribution"},
            consumes={"earnings": "ca/employment_income"},
            produces={"output": "ca/cpp_second_additional_contributions"},
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
        # Schedule 8 Part 3a line 28 "Line 26 plus line 27": the first and second additional
        # contributions together, the T1 line 22215 deduction.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/cpp_first_additional_contributions",
                    "ca/cpp_second_additional_contributions",
                )
            },
            produces={"output": "ca/cpp_enhanced_contributions"},
        ),
        # Schedule 7 line 5 "Line 1 plus line 4 ... Total contributions", line 6 "Total
        # contributions from line 5" and line 10 "Line 6 minus line 9 Contributions available to
        # deduct": with no HBP or LLP repayments (line 9), line 10 is line 5. In line 5's order:
        # the unused contributions (line 1), then the contributions (line 4).
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/unused_rrsp_contributions", "ca/rrsp_contributions")},
            produces={"output": "ca/rrsp_contributions_available"},
        ),
        # Schedule 7 line 17 "Enter whichever is less: amount from line 13 or line 16.": with no
        # employer PRPP contributions (line 12) and no transfers (line 15), line 13 is the limit
        # and line 16 the contributions available to deduct. The parts keep line 20's order (line
        # 10, then the limit).
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={"amounts": ("ca/rrsp_contributions_available", "ca/rrsp_deduction_limit")},
            produces={"output": "ca/rrsp_deduction_maximum"},
        ),
        # Schedule 7 line 18 "Enter your RRSP, PRPP, or SPP contributions you are deducting for
        # 2025 (cannot be more than the amount on line 17).", line 19 "Line 15 plus line 18" and
        # line 20 "Enter whichever is less: amount from line 10 or line 19. Enter this amount on
        # line 20800 of your return. RRSP deduction": with no transfers (line 15), line 19 is
        # line 18, at most line 17 and so at most line 10, and line 20 is line 18 itself. A
        # claim above line 17 is refused, not capped.
        CapabilitySelection(
            name="core/at_most",
            params={},
            consumes={"amount": "ca/rrsp_amount_deducted", "bound": "ca/rrsp_deduction_maximum"},
            produces={"output": "ca/rrsp_deduction"},
        ),
        # Schedule 7 line 23 "Line 21 minus line 22 Your unused contributions available to carry
        # forward to a future year": line 21 "Enter your contributions available to deduct from
        # line 10 of the previous page." less line 22 "Enter your RRSP deduction from line 20 of
        # the previous page."; never negative, as line 20 is at most line 10.
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca/rrsp_contributions_available", "less": "ca/rrsp_deduction"},
            produces={"output": "ca/unused_rrsp_contributions_carried_forward"},
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
        # T1 line 23300 "Add lines 35 to 52.": the deductions in the form's line order (20800,
        # 21200, 21400, 22215).
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/rrsp_deduction",
                    "ca/union_dues",
                    "ca/child_care_expenses",
                    "ca/cpp_enhanced_contributions",
                )
            },
            produces={"output": "ca/deductions_from_total_income"},
        ),
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/total_income", "less": "ca/deductions_from_total_income"},
            produces={"output": "ca/net_income"},
        ),
        # Federal Worksheet "Line 25000 - Other payments deduction", "Complete the following
        # calculation if you reported net federal supplements on line 14600 of your return.":
        # line 1 "Amount from line 23400 of your return (if negative, enter "0")" is the net
        # income artifact (line 23400 floored at 0, as line 23500 is not wired yet); line 4 "Line
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
            consumes={"amount": "ca/net_income", "less": "ca/uccb_and_rdsp_income"},
            produces={"output": "ca/net_income_less_uccb_and_rdsp_income"},
        ),
        # Line 8 "Line 6 plus line 7 =": line 6 "Amount from line 21300 of your return" (the UCCB
        # repayment, a starting amount as line 21300 is not wired yet) and line 7 "RDSP income
        # repayment (included in the amount on line 23200 of your return)", in line order.
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
        # T1 line 68 and line 25700 "Add lines 58 to 67.": lines 58, 59, 60, 61, 62 and 67 (lines
        # 24400, 24900, 25000, 25100, 25200 and 25600), in line order; lines 63 to 66 (25300,
        # 25395, 25400 and 25500) are not wired yet.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/canadian_armed_forces_and_police_deduction",
                    "ca/security_options_deductions",
                    "ca/other_payments_deduction",
                    "ca/limited_partnership_losses_of_other_years",
                    "ca/non_capital_losses_of_other_years",
                    "ca/additional_deductions",
                )
            },
            produces={"output": "ca/deductions_from_net_income"},
        ),
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/net_income", "less": "ca/deductions_from_net_income"},
            produces={"output": "ca/taxable_income"},
        ),
        CapabilitySelection(
            name="core/progressive_tax",
            params={"schedule": "ca/brackets"},
            consumes={"base": "ca/taxable_income"},
            produces={"output": "ca/federal_basic_tax"},
        ),
        CapabilitySelection(
            name="core/progressive_tax",
            params={"schedule": "ca-on/brackets"},
            consumes={"base": "ca/taxable_income"},
            produces={"output": "ca-on/ontario_basic_tax"},
        ),
        # T1 line 30000 "If the amount on line 23600 is $177,882 or less, enter $16,129. If the
        # amount on line 23600 is $253,414 or more, enter $14,538. Otherwise, use the Federal
        # Worksheet to calculate the amount to enter. (maximum $16,129)": the federal basic
        # personal amount is the worksheet's taper on net income (line 23600), the first part of
        # the T1's total of credit amounts.
        CapabilitySelection(
            name="core/tapered_amount",
            params={"taper": "ca/basic_personal_amount"},
            consumes={"base": "ca/net_income"},
            produces={"output": "ca/basic_personal_amount"},
        ),
        # ON428 line 58040 has no reduction: the Ontario basic personal amount dataset becomes an
        # artifact of the same name, the first part of ON428's total of credit amounts.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/basic_personal_amount"},
            consumes={},
            produces={"output": "ca-on/basic_personal_amount"},
        ),
        # The Canada employment amount: the lesser of the T1's cap and employment income.
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca/canada_employment_amount"},
            consumes={"base": "ca/employment_income"},
            produces={"output": "ca/canada_employment_amount"},
        ),
        # Federal Worksheet, "Line 30100 - Age amount": line 1 "Maximum amount 9,028.00", the
        # dataset as an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/age_maximum"},
            consumes={},
            produces={"output": "ca/age_maximum"},
        ),
        # Line 3 "Income threshold 45,522.00", the dataset as an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/age_income_threshold"},
            consumes={},
            produces={"output": "ca/age_income_threshold"},
        ),
        # Line 2 "Amount from line 23600 of your return", the net income, and line 4 "Line 2 minus
        # line 3 (if negative, enter "0")".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/net_income", "less": "ca/age_income_threshold"},
            produces={"output": "ca/age_income_over_threshold"},
        ),
        # Line 5 "Applicable rate 15%" and line 6 "Line 4 multiplied by the percentage from line
        # 5".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/age_rate"},
            consumes={"base": "ca/age_income_over_threshold"},
            produces={"output": "ca/age_reduction"},
        ),
        # Line 7 "Line 1 minus line 6 (if negative, enter "0") Enter this amount on line 30100 of
        # your return."
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/age_maximum", "less": "ca/age_reduction"},
            produces={"output": "ca/age_amount_before_count"},
        ),
        # T1 line 78 (line 30100) "Age amount (if you were born in 1960 or earlier) (use Federal
        # Worksheet) (maximum $9,028)": line 7 once if born in 1960 or earlier, else 0.
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca/age_amount_before_count",
                "count": "ca/born_in_1960_or_earlier",
            },
            produces={"output": "ca/age_amount"},
        ),
        # Schedule 5, "Line 30300 - Spouse or common-law partner amount": line 2 and line 51090
        # "If you are eligible for the Canada caregiver amount for your spouse or common-law
        # partner, enter $2,687", for each spouse eligible for it, at most one.
        CapabilitySelection(
            name="core/per_unit_amount",
            params={"amount": "ca/spouse_infirmity_amount"},
            consumes={"count": "ca/spouse_caregiver_eligible"},
            produces={"output": "ca/spouse_infirmity_supplement"},
        ),
        # Line 3 "Line 1 plus line 2", line 1 "Basic personal amount from line 30000 of your
        # return".
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/basic_personal_amount", "ca/spouse_infirmity_supplement")},
            produces={"output": "ca/spouse_amount_basis"},
        ),
        # Line 4 "Your spouse's or common-law partner's net income from line 23600 of their
        # return (Note 1)" and line 5 "Line 3 minus line 4 (if negative, enter "0") Enter this
        # amount on line 30300 of your return."
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/spouse_amount_basis", "less": "ca/spouse_net_income"},
            produces={"output": "ca/spouse_amount_before_count"},
        ),
        # T1 line 79 (line 30300) "Spouse or common-law partner amount (complete Schedule 5)":
        # line 5 once if the filer claims it ("Only one spouse or common-law partner can claim
        # the amount on line 30300 for each other for the same year"), else 0.
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca/spouse_amount_before_count",
                "count": "ca/spouses_claimed",
            },
            produces={"output": "ca/spouse_amount"},
        ),
        # Schedule 5, "Line 30400 - Amount for an eligible dependant": line 1 "Basic personal
        # amount from line 30000 of your return", line 3 "Line 1 plus line 2" with line 2 (an
        # infirm eligible dependant 18 or older) not triggered, line 4 (51106) "Dependant's net
        # income from line 23600 of their return" and line 5 "Line 3 minus line 4 (if negative,
        # enter "0") Enter this amount on line 30400 of your return.".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/basic_personal_amount", "less": "ca/dependant_net_income"},
            produces={"output": "ca/eligible_dependant_amount_before_count"},
        ),
        # T1 line 80 (line 30400) "Amount for an eligible dependant (complete Schedule 5)": line
        # 5 for each eligible dependant claimed, at most one ("Each household is allowed only one
        # claim for this amount").
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca/eligible_dependant_amount_before_count",
                "count": "ca/eligible_dependants",
            },
            produces={"output": "ca/eligible_dependant_amount"},
        ),
        # Schedule 5, "Line 30425 - Canada caregiver amount for spouse or common-law partner,
        # or eligible dependant age 18 or older": line 1 "Base amount 28,798.00", the dataset as
        # an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/spouse_caregiver_base"},
            consumes={},
            produces={"output": "ca/spouse_caregiver_base"},
        ),
        # Line 2 "Net income for this person from line 23600 of their return", the spouse's
        # net income, and line 3 "Line 1 minus line 2 (if negative, enter "0") (maximum
        # $8,601)", before its maximum, then at most it.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/spouse_caregiver_base", "less": "ca/spouse_net_income"},
            produces={"output": "ca/spouse_caregiver_before_maximum"},
        ),
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca/spouse_caregiver_maximum"},
            consumes={"base": "ca/spouse_caregiver_before_maximum"},
            produces={"output": "ca/spouse_caregiver_limit"},
        ),
        # Line 4 "Amount claimed on line 30300 or line 30400 of your return, if applicable", the
        # spouse amount, and line 5 "Line 3 minus line 4 (if negative, enter "0") Enter this
        # amount on line 30425 of your return."
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/spouse_caregiver_limit", "less": "ca/spouse_amount"},
            produces={"output": "ca/spouse_caregiver_amount_before_count"},
        ),
        # T1 line 81 (line 30425) "Canada caregiver amount for spouse or common-law partner,
        # or eligible dependant age 18 or older (complete Schedule 5)": line 5 once if the
        # spouse is eligible for the Canada caregiver amount (line 51090), else 0. The eligible
        # dependant 18 or older (line 30400) is not wired here.
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca/spouse_caregiver_amount_before_count",
                "count": "ca/spouse_caregiver_eligible",
            },
            produces={"output": "ca/spouse_caregiver_amount"},
        ),
        # T1 line 83 (line 30500) "Canada caregiver amount for infirm children under 18 years of
        # age (see Schedule 5) Number of children you are claiming this amount for Line 30499"
        # "multiplied by $2,687".
        CapabilitySelection(
            name="core/per_unit_amount",
            params={"amount": "ca/infirm_child_amount"},
            consumes={"count": "ca/infirm_children"},
            produces={"output": "ca/infirm_children_amount"},
        ),
        # Worksheet ON428, "Line 58080 - Age amount": line 1 "Maximum amount 6,223.00", the
        # dataset as an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/age_maximum"},
            consumes={},
            produces={"output": "ca-on/age_maximum"},
        ),
        # Line 3 "Income threshold 46,330.00", the dataset as an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/age_income_threshold"},
            consumes={},
            produces={"output": "ca-on/age_income_threshold"},
        ),
        # Line 2 "Amount from line 23600 of your return", the net income, and line 4 "Line 2
        # minus line 3 (if negative, enter "0")".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/net_income", "less": "ca-on/age_income_threshold"},
            produces={"output": "ca-on/age_income_over_threshold"},
        ),
        # Line 5 "Applicable rate 15%" and line 6 "Line 4 multiplied by the percentage from line
        # 5".
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/age_rate"},
            consumes={"base": "ca-on/age_income_over_threshold"},
            produces={"output": "ca-on/age_reduction"},
        ),
        # Line 7 "Line 1 minus line 6 (if negative, enter "0") Enter this amount on line 58080 of
        # your Form ON428."
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca-on/age_maximum", "less": "ca-on/age_reduction"},
            produces={"output": "ca-on/age_amount_before_count"},
        ),
        # ON428 line 10 and line 58080 "Age amount (if you were born in 1960 or earlier) (use
        # Worksheet ON428) (maximum $6,223)": line 7 once if born in 1960 or earlier, else 0.
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca-on/age_amount_before_count",
                "count": "ca/born_in_1960_or_earlier",
            },
            produces={"output": "ca-on/age_amount"},
        ),
        # ON428 line 11 "Base amount 11,905.00": the dataset becomes an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/spouse_base"},
            consumes={},
            produces={"output": "ca-on/spouse_base"},
        ),
        # Line 12 "Your spouse's or common-law partner's net income from line 23600 of their
        # return", and line 13 (line 58120) "Line 11 minus line 12 (if negative, enter "0")
        # (maximum $10,823)", before its maximum, then at most it.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca-on/spouse_base", "less": "ca/spouse_net_income"},
            produces={"output": "ca-on/spouse_amount_before_maximum"},
        ),
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca-on/spouse_maximum"},
            consumes={"base": "ca-on/spouse_amount_before_maximum"},
            produces={"output": "ca-on/spouse_amount_before_count"},
        ),
        # Line 58120 for each spouse or common-law partner amount claimed, the T1 line 30300
        # count.
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca-on/spouse_amount_before_count",
                "count": "ca/spouses_claimed",
            },
            produces={"output": "ca-on/spouse_amount"},
        ),
        # ON428 line 14 "Base amount 11,905.00": the dataset becomes an artifact of the same name.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/eligible_dependant_base"},
            consumes={},
            produces={"output": "ca-on/eligible_dependant_base"},
        ),
        # ON428 line 15 "Your eligible dependant's net income from line 23600 of their return",
        # the federal Schedule 5 line 4 figure, and line 16 (line 58160) "Line 14 minus line 15
        # (if negative, enter "0") (maximum $10,823)", before its maximum, then at most it.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/eligible_dependant_base",
                "less": "ca/dependant_net_income",
            },
            produces={"output": "ca-on/eligible_dependant_amount_before_maximum"},
        ),
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca-on/eligible_dependant_maximum"},
            consumes={"base": "ca-on/eligible_dependant_amount_before_maximum"},
            produces={"output": "ca-on/eligible_dependant_amount_before_count"},
        ),
        # Line 58160 for each eligible dependant claimed, the T1 line 30400 count.
        CapabilitySelection(
            name="core/times_count",
            params={},
            consumes={
                "amount": "ca-on/eligible_dependant_amount_before_count",
                "count": "ca/eligible_dependants",
            },
            produces={"output": "ca-on/eligible_dependant_amount"},
        ),
        # T1 line 33500 (lines 30000, 30100, 30300, 30400, 30425, 30500, 30800, 31200, 31260) and
        # ON428 line 58800 (lines 58040, 58080, 58120, 58160, 58240, 58300), in the forms' line
        # order. ON428 lines 58240 and 58300 are "Amount from line 30800 / 31200 of your
        # return", so the Ontario sum reads the federal kinds; it has no Canada employment
        # amount.
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
                    "ca/infirm_children_amount",
                    "ca/cpp_base_contributions",
                    "ca/ei_premiums",
                    "ca/canada_employment_amount",
                )
            },
            produces={"output": "ca/non_refundable_credit_amounts"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca-on/basic_personal_amount",
                    "ca-on/age_amount",
                    "ca-on/spouse_amount",
                    "ca-on/eligible_dependant_amount",
                    "ca/cpp_base_contributions",
                    "ca/ei_premiums",
                )
            },
            produces={"output": "ca-on/non_refundable_credit_amounts"},
        ),
        # The rate is applied once, to the total (T1 line 33800, ON428 line 58840), giving each
        # form's non-refundable tax credits (T1 line 35000, ON428 line 61500).
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/credit_rate"},
            consumes={"base": "ca/non_refundable_credit_amounts"},
            produces={"output": "ca/non_refundable_tax_credits"},
        ),
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/credit_rate"},
            consumes={"base": "ca-on/non_refundable_credit_amounts"},
            produces={"output": "ca-on/non_refundable_tax_credits"},
        ),
        # T1 line 123 (40425) "Federal dividend tax credit (use Federal Worksheet)": the Federal
        # Worksheet's "Line 40425 - Federal dividend tax credit", line 5 "Add lines 1 to 4." of
        # the credits shown on the T3, T4PS, T5 and T5013 slips. For dividends with no
        # information slip, line A "Amount from line 12000 of your return (Note 1)" and line B
        # "Amount from line 12010 of your return (Note 1)", Note 1 being "Enter only the amount
        # of dividends that were not shown on an information slip.", so line A is the
        # Worksheet's line 17 and line B its line 16, each its own step; line 6 is "Line B,
        # multiplied by 9.0301%"; line C is "Amount A minus amount B", and line 7 (printed
        # "Line 2") is line C "multiplied by 15.0198%"; line 8 is "Line 6 plus line 7" and
        # line 9 "Line 5 plus line 8 Enter this amount on line 40425 of your return."
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/t3_dividend_tax_credit",
                    "ca/t4ps_dividend_tax_credit",
                    "ca/t5_dividend_tax_credit",
                    "ca/t5013_dividend_tax_credit",
                )
            },
            produces={"output": "ca/slip_dividend_tax_credit"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/dividends_without_a_slip_grossed_up",)},
            produces={"output": "ca/dividends_amount_a"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/other_dividends_grossed_up",)},
            produces={"output": "ca/dividends_amount_b"},
        ),
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/dividend_credit_rate_other_than_eligible"},
            consumes={"base": "ca/dividends_amount_b"},
            produces={"output": "ca/other_dividends_credit"},
        ),
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca/dividends_amount_a", "less": "ca/dividends_amount_b"},
            produces={"output": "ca/dividends_amount_a_less_b"},
        ),
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/dividend_credit_rate_eligible"},
            consumes={"base": "ca/dividends_amount_a_less_b"},
            produces={"output": "ca/eligible_dividends_credit"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/other_dividends_credit", "ca/eligible_dividends_credit")},
            produces={"output": "ca/no_slip_dividend_tax_credit"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/slip_dividend_tax_credit", "ca/no_slip_dividend_tax_credit")},
            produces={"output": "ca/dividend_tax_credit"},
        ),
        # T1 line 125 "Add lines 122 to 124.": line 122 "Amount from line 35000" and line 123
        # (40425), in line order; line 124 (40427, minimum tax carryover) is not triggered.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/non_refundable_tax_credits", "ca/dividend_tax_credit")},
            produces={"output": "ca/credits_against_basic_federal_tax"},
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
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/ontario_basic_tax",
                "less": "ca-on/non_refundable_tax_credits",
            },
            produces={"output": "ca-on/ontario_tax_after_credits"},
        ),
        # ON428 lines 66 to 68: the surtax on the Ontario tax after credits, which is line 65
        # while line 64 (tax on split income) is not modelled. Line 69 "Line 62 plus line 68".
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca-on/surtax"},
            consumes={"base": "ca-on/ontario_tax_after_credits"},
            produces={"output": "ca-on/ontario_surtax"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca-on/ontario_tax_after_credits", "ca-on/ontario_surtax")},
            produces={"output": "ca-on/ontario_tax_with_surtax"},
        ),
        # ON428 line 56 "Enter the amount from line 53 above.", line 57 (printed "Line 57 and
        # line and line 61520") "Ontario dividend tax credit (use Worksheet ON428)" and line 58
        # "Line 56 minus line 57 (if negative, enter "0")". Worksheet ON428's "Line 61520 -
        # Ontario dividend tax credit": line A "Amount from line 12000 of your return" and line
        # 1 "Amount from line 12010 of your return Line B" "multiplied by 2.9863%", with no Note
        # 1, so A and B are the whole lines 12000 and 12010, each its own step; line 2 "Amount
        # A minus amount B Line C" "multiplied by 10%"; line 3 "Line 1 plus line 2 Enter this
        # amount on line 61520 of your Form ON428.", which is line 57.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca-on/ontario_tax_after_credits",)},
            produces={"output": "ca-on/ontario_tax_before_dividend_credit"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/taxable_dividends",)},
            produces={"output": "ca-on/dividends_amount_a"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/taxable_dividends_other_than_eligible",)},
            produces={"output": "ca-on/dividends_amount_b"},
        ),
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/dividend_credit_rate_other_than_eligible"},
            consumes={"base": "ca-on/dividends_amount_b"},
            produces={"output": "ca-on/other_dividends_credit"},
        ),
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca-on/dividends_amount_a", "less": "ca-on/dividends_amount_b"},
            produces={"output": "ca-on/dividends_amount_a_less_b"},
        ),
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/dividend_credit_rate_eligible"},
            consumes={"base": "ca-on/dividends_amount_a_less_b"},
            produces={"output": "ca-on/eligible_dividends_credit"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca-on/other_dividends_credit", "ca-on/eligible_dividends_credit")},
            produces={"output": "ca-on/dividend_tax_credit"},
        ),
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/ontario_tax_before_dividend_credit",
                "less": "ca-on/dividend_tax_credit",
            },
            produces={"output": "ca-on/ontario_tax_less_dividend_credit"},
        ),
        # ON428 line 70 "Ontario dividend tax credit from line 57" and line 71 "Line 69 minus
        # line 70 (if negative, enter "0")": line 71 is line 73, as line 72 (the additional tax
        # for minimum tax purposes) is not triggered.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca-on/dividend_tax_credit",)},
            produces={"output": "ca-on/dividend_credit_from_line_57"},
        ),
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/ontario_tax_with_surtax",
                "less": "ca-on/dividend_credit_from_line_57",
            },
            produces={"output": "ca-on/ontario_tax_after_dividend_credit"},
        ),
        # ON428 line 74 "Basic reduction 294.00": the dataset becomes an artifact of the same
        # name, the first part of line 77.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/tax_reduction_basic"},
            consumes={},
            produces={"output": "ca-on/tax_reduction_basic"},
        ),
        # ON428 line 75 (line 60969) "Number of dependent children multiplied by $544" and line
        # 76 (line 60970) "Number of dependants multiplied by $544".
        CapabilitySelection(
            name="core/per_unit_amount",
            params={"amount": "ca-on/tax_reduction_per_dependant"},
            consumes={"count": "ca-on/dependent_children"},
            produces={"output": "ca-on/tax_reduction_for_children"},
        ),
        CapabilitySelection(
            name="core/per_unit_amount",
            params={"amount": "ca-on/tax_reduction_per_dependant"},
            consumes={"count": "ca-on/dependants"},
            produces={"output": "ca-on/tax_reduction_for_dependants"},
        ),
        # ON428 line 77 "Add lines 74 to 76.", in line order.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca-on/tax_reduction_basic",
                    "ca-on/tax_reduction_for_children",
                    "ca-on/tax_reduction_for_dependants",
                )
            },
            produces={"output": "ca-on/tax_reduction_amounts"},
        ),
        # ON428 line 78 "Amount from line 77 above multiplied by 2", line 79 "Amount from line 73
        # above" and line 80 "Line 78 minus line 79 (if negative, enter "0") Ontario tax
        # reduction": line 73 is line 71, the Ontario tax after the dividend credit, while the
        # minimum tax (line 72) is not triggered.
        CapabilitySelection(
            name="core/multiple_over",
            params={"factor": "ca-on/tax_reduction_factor"},
            consumes={
                "amount": "ca-on/tax_reduction_amounts",
                "less": "ca-on/ontario_tax_after_dividend_credit",
            },
            produces={"output": "ca-on/ontario_tax_reduction"},
        ),
        # ON428 line 81 "Line 73 minus line 80 (if negative, enter "0")".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/ontario_tax_after_dividend_credit",
                "less": "ca-on/ontario_tax_reduction",
            },
            produces={"output": "ca-on/ontario_tax_after_reduction"},
        ),
        # Schedule ON428-A line 3 "Line 1 plus line 2", line 1 "Amount from line 10100 of your
        # return" (line 2, line 10400, not triggered), and line 5 "Line 3 multiplied by the
        # percentage from line 4 (maximum $875)", line 4 "Applicable rate 5.05%": the rate on
        # employment income, before its maximum.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/lift_rate"},
            consumes={"base": "ca/employment_income"},
            produces={"output": "ca-on/lift_credit_before_maximum"},
        ),
        # Line 5's "(maximum $875)" and Part A line 14 "Amount from line 5 above (maximum
        # $875)".
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca-on/lift_maximum"},
            consumes={"base": "ca-on/lift_credit_before_maximum"},
            produces={"output": "ca-on/lift_maximum_credit"},
        ),
        # Lines 15 to 19: line 15 "Amount from line 13 above", the adjusted net income, which is
        # net income (line 23600) while lines 7, 8, 10 and 11 are not triggered; line 16
        # "Individual income threshold 32,500.00"; line 17 "Line 15 minus line 16 (if negative,
        # enter "0")"; line 18 "Applicable rate 5%"; line 19 "Line 17 multiplied by the
        # percentage from line 18".
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca-on/lift_reduction"},
            consumes={"base": "ca/net_income"},
            produces={"output": "ca-on/lift_reduction"},
        ),
        # Line 20 "Line 14 minus line 19 (if negative, enter "0") Enter this amount on line 62140
        # of your Form ON428.", ON428 line 85.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca-on/lift_maximum_credit", "less": "ca-on/lift_reduction"},
            produces={"output": "ca-on/lift_credit"},
        ),
        # ON428 line 86 "Line 84 minus line 85 (if negative, enter "0")": line 84 "Amount from line
        # 83 of the previous page" carries line 83 "Line 81 minus line 82 (if negative, enter "0")",
        # which is line 81 while line 82 (the provincial foreign tax credit) is not triggered.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca-on/ontario_tax_after_reduction", "less": "ca-on/lift_credit"},
            produces={"output": "ca-on/ontario_tax_after_lift_credit"},
        ),
        # ON428 line 87 and line 62150 "Enter the amount of qualifying donations that have also
        # been claimed as a charitable donation." "multiplied by 25%", under "Community food
        # program donation tax credit for farmers:": the donations are a caller input, taken as
        # entered.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/community_food_program_rate"},
            consumes={"base": "ca-on/community_food_program_donations"},
            produces={"output": "ca-on/community_food_program_credit"},
        ),
        # ON428 line 88 "Line 86 minus line 87 (if negative, enter "0")".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/ontario_tax_after_lift_credit",
                "less": "ca-on/community_food_program_credit",
            },
            produces={"output": "ca-on/ontario_tax_after_food_credit"},
        ),
        # ON428 line 89 "Ontario health premium (complete the chart below)": the chart's tiers on
        # line 1 "Enter your taxable income from line 26000 of your return", each the previous
        # plateau plus a rate on the income over its threshold, at most the next plateau.
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca-on/health_premium"},
            consumes={"base": "ca/taxable_income"},
            produces={"output": "ca-on/ontario_health_premium"},
        ),
        # ON428 line 90 "Line 88 plus line 89 Enter this amount on line 42800 of your return.
        # Ontario tax": line 88 "Line 86 minus line 87 (if negative, enter "0")" carries line 86
        # while the community food program donation tax credit for farmers (line 87) is not
        # triggered by the returns.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": ("ca-on/ontario_tax_after_food_credit", "ca-on/ontario_health_premium")
            },
            produces={"output": "ca-on/ontario_tax"},
        ),
        # T1 line 142 (line 42000) "Add lines 139 to 141. Net federal tax": with lines 120, 123,
        # 124, 127 to 133 and 135 to 141 not modelled or not triggered, line 126 (42900) "Line
        # 121 minus line 125 (if negative, enter "0") Basic federal tax" is the federal tax
        # (lines 119 and 121) less line 122 "Amount from line 35000", the federal tax after
        # credits, and lines 134 (40600), 139 (41700) and 142 carry it: one part.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/federal_tax_after_credits",)},
            produces={"output": "ca/net_federal_tax"},
        ),
        # T1 line 148 (line 43500) "Add lines 143 to 147. Total payable": line 143 "Amount from
        # line 42000" and line 147 (42800), the Ontario tax, in line order; lines 144 to 146 are
        # not triggered.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/net_federal_tax", "ca-on/ontario_tax")},
            produces={"output": "ca/total_payable"},
        ),
        # Schedule 6 line 5 "Add lines 1 to 4. Enter the result, even if it is "0". Working
        # income", line 1 "Employment income and other employment income from line 10100 and line
        # 10400 of the return" (line 10400 and lines 2 to 4 not triggered), carried by line 6
        # "Add the amounts from line 5 in columns 1 and 2. Enter this amount on line 16. Family
        # working income" with no eligible spouse: one part.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/employment_income",)},
            produces={"output": "ca/working_income"},
        ),
        # Schedule 6 line 15 "Line 13 minus line 14 Enter this amount on line 23 and line 35.
        # Adjusted family net income": line 7 "Net income from line 23600 of the return", through
        # lines 10, 12 and 13 with lines 8, 9 and 11 not triggered and no eligible spouse (line
        # 14 not triggered): one part.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/net_income",)},
            produces={"output": "ca/adjusted_family_net_income"},
        ),
        # Schedule 6 lines 16 to 22: line 16 "Family working income from line 6"; line 17 "Base
        # amount 3,000.00"; line 18 "Line 16 minus line 17 (if negative, enter "0")"; line 19
        # "Rate 27%"; line 20 "Line 18 multiplied by the percentage from line 19"; line 21 "If
        # you had an eligible spouse or an eligible dependant, enter $2,813. If not, enter
        # $1,633."; line 22 "Enter whichever is less: amount from line 20 or line 21.": one tier
        # with a maximum, with no eligible spouse or dependant.
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca/cwb_basic"},
            consumes={"base": "ca/working_income"},
            produces={"output": "ca/cwb_before_reduction_without_dependant"},
        ),
        # The same lines with an eligible dependant: line 21's $2,813 as the tier's maximum.
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca/cwb_basic_with_dependant"},
            consumes={"base": "ca/working_income"},
            produces={"output": "ca/cwb_before_reduction_with_dependant"},
        ),
        # Schedule 6 lines 23 to 27: line 23 "Adjusted family net income from line 15"; line 24
        # "If you had an eligible spouse or an eligible dependant, enter $30,639. If not, enter
        # $26,855."; line 25 "Line 23 minus line 24 (if negative, enter "0")"; line 26 "Rate
        # 15%"; line 27 "Line 25 multiplied by the percentage from line 26": one tier, with no
        # eligible spouse or dependant.
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca/cwb_reduction"},
            consumes={"base": "ca/adjusted_family_net_income"},
            produces={"output": "ca/cwb_reduction_without_dependant"},
        ),
        # The same lines with an eligible dependant: line 24's $30,639 as the tier's threshold.
        CapabilitySelection(
            name="core/tiered_surcharge",
            params={"tiers": "ca/cwb_reduction_with_dependant"},
            consumes={"base": "ca/adjusted_family_net_income"},
            produces={"output": "ca/cwb_reduction_with_dependant"},
        ),
        # Schedule 6 line 28 "Line 22 minus line 27 (if negative, enter "0") If you are not
        # completing Step 3, enter this amount on line 45300 of your return.", with no eligible
        # spouse or dependant: Step 3 (the disability supplement) is not triggered.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/cwb_before_reduction_without_dependant",
                "less": "ca/cwb_reduction_without_dependant",
            },
            produces={"output": "ca/canada_workers_benefit_without_dependant"},
        ),
        # Line 28 with an eligible dependant.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca/cwb_before_reduction_with_dependant",
                "less": "ca/cwb_reduction_with_dependant",
            },
            produces={"output": "ca/canada_workers_benefit_with_dependant"},
        ),
        # Line 28 for the filer's family status, which lines 21 and 24 read ("If you had an
        # eligible spouse or an eligible dependant ... If not ..."): the line with no eligible
        # spouse or dependant when the number of Schedule 6 eligible dependants (line 38100) is
        # 0, else the line with one; an eligible spouse is not modelled.
        CapabilitySelection(
            name="core/choose_by_count",
            params={},
            consumes={
                "count": "ca/cwb_eligible_dependants",
                "when_none": "ca/canada_workers_benefit_without_dependant",
                "when_any": "ca/canada_workers_benefit_with_dependant",
            },
            produces={"output": "ca/canada_workers_benefit"},
        ),
        # Form ON479 line 1 and line 61268 "Eligible medical expenses for fertility treatment
        # multiplied by 25% (maximum $5,000) =": the rate on the expenses, before its maximum.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/fertility_credit_rate"},
            consumes={"base": "ca-on/fertility_expenses"},
            produces={"output": "ca-on/fertility_credit_before_maximum"},
        ),
        # Line 1's "(maximum $5,000)", printed after the percentage, so it caps the credit.
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca-on/fertility_credit_maximum"},
            consumes={"base": "ca-on/fertility_credit_before_maximum"},
            produces={"output": "ca-on/fertility_credit"},
        ),
        # Line 14 "Amount paid in the year for eligible seniors' use of Ontario public transit
        # services (maximum $3,000) Line 63100 multiplied by 15% =": the "(maximum $3,000)" is
        # printed before the percentage, so it caps the amount paid.
        CapabilitySelection(
            name="core/capped_amount",
            params={"cap": "ca-on/seniors_transit_maximum"},
            consumes={"base": "ca-on/seniors_transit_paid"},
            produces={"output": "ca-on/seniors_transit_amount_paid_at_most_maximum"},
        ),
        # Line 14's "multiplied by 15% =", on the capped amount.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/seniors_transit_rate"},
            consumes={"base": "ca-on/seniors_transit_amount_paid_at_most_maximum"},
            produces={"output": "ca-on/seniors_transit_credit"},
        ),
        # Form T1221 lines 1 to 3 "Enter the amount of qualifying expenses." (one line for each
        # corporation or slip) and line 4 "Add lines 1 to 3. Enter this amount on line 63220 of
        # your Form ON479.": the expenses of every slip in the list, added.
        CapabilitySelection(
            name="ca-on/flow_through_share_expenses",
            params={},
            consumes={"slips": "ca-on/flow_through_share_slips"},
            produces={"output": "ca-on/flow_through_share_expenses"},
        ),
        # Form ON479 line 17 and line 63220 "Enter your total expenses from your Form T1221.
        # multiplied by 5% =": the 5% on T1221 line 4.
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca-on/flow_through_share_rate"},
            consumes={"base": "ca-on/flow_through_share_expenses"},
            produces={"output": "ca-on/flow_through_share_credit"},
        ),
        # Line 18 "Add lines 1, 2, 13, 14, 16, and 17. =": lines 1, 14 and 17, in line order, as
        # lines 2, 13 and 16 are not triggered.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca-on/fertility_credit",
                    "ca-on/seniors_transit_credit",
                    "ca-on/flow_through_share_credit",
                )
            },
            produces={"output": "ca-on/ontario_credits_subtotal"},
        ),
        # Line 21 "Line 19 plus line 20 Enter this amount online 47900 of your return. Ontario
        # credits =": line 19 "Amount from line 18 of the previous page" carries line 18, and
        # line 20 (the co-operative education credit) is not triggered.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca-on/ontario_credits_subtotal",)},
            produces={"output": "ca-on/ontario_credits"},
        ),
        # T1 line 165 and line 47900 "Provincial or territorial credits (complete Form 479, if it
        # applies)": ON479 line 21, the Ontario credits.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca-on/ontario_credits",)},
            produces={"output": "ca/provincial_credits"},
        ),
        # T1 line 166 (line 48200) "Add lines 150 to 165. Total credits": line 150 (43700), line
        # 155 (45300) "Canada workers benefit (CWB) (complete Schedule 6)" and line 165 (47900), in
        # line order, as the other lines are not triggered.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/income_tax_deducted",
                    "ca/canada_workers_benefit",
                    "ca/provincial_credits",
                )
            },
            produces={"output": "ca/total_credits"},
        ),
        # T1 line 167 "Line 149 minus line 166 ... Refund or balance owing": not floored, so a
        # negative result is a refund (line 48400) and a positive one a balance owing (48500).
        CapabilitySelection(
            name="core/subtract",
            params={},
            consumes={"amount": "ca/total_payable", "less": "ca/total_credits"},
            produces={"output": "ca/refund_or_balance_owing"},
        ),
    }
    assert len(found.capabilities) == 139


def test_its_first_tax_year_composes_every_selection() -> None:
    composition = service().compose(CA_ON, 2025)

    wiring = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composition.order
    }
    assert len(composition.order) == 139
    assert wiring == {
        (ApplyRate, frozenset({CAPITAL_GAIN}), frozenset({TAXABLE_CAPITAL_GAINS})),
        (
            TieredContribution,
            frozenset({EMPLOYMENT_INCOME}),
            frozenset({CPP_BASE_CONTRIBUTIONS}),
        ),
        (
            TieredContribution,
            frozenset({EMPLOYMENT_INCOME}),
            frozenset({CPP_FIRST_ADDITIONAL_CONTRIBUTIONS}),
        ),
        (
            TieredContribution,
            frozenset({EMPLOYMENT_INCOME}),
            frozenset({CPP_SECOND_ADDITIONAL_CONTRIBUTIONS}),
        ),
        (TieredContribution, frozenset({EMPLOYMENT_INCOME}), frozenset({EI_PREMIUMS})),
        (
            Sum,
            frozenset({CPP_FIRST_ADDITIONAL_CONTRIBUTIONS, CPP_SECOND_ADDITIONAL_CONTRIBUTIONS}),
            frozenset({CPP_ENHANCED_CONTRIBUTIONS}),
        ),
        (
            Sum,
            frozenset(
                {
                    T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                    T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                    T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                    T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                }
            ),
            frozenset({SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
        ),
        (
            Sum,
            frozenset(
                {
                    T3_TAXABLE_DIVIDENDS,
                    T4PS_TAXABLE_DIVIDENDS,
                    T5_TAXABLE_DIVIDENDS,
                    T5013_TAXABLE_DIVIDENDS,
                }
            ),
            frozenset({SLIP_TAXABLE_DIVIDENDS}),
        ),
        (
            ApplyFraction,
            frozenset({ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP}),
            frozenset({ELIGIBLE_DIVIDENDS_GROSSED_UP}),
        ),
        (
            ApplyFraction,
            frozenset({OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP}),
            frozenset({OTHER_DIVIDENDS_GROSSED_UP}),
        ),
        (
            Sum,
            frozenset({ELIGIBLE_DIVIDENDS_GROSSED_UP, OTHER_DIVIDENDS_GROSSED_UP}),
            frozenset({DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP}),
        ),
        (
            Sum,
            frozenset({SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, OTHER_DIVIDENDS_GROSSED_UP}),
            frozenset({TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
        ),
        (
            Sum,
            frozenset({SLIP_TAXABLE_DIVIDENDS, DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP}),
            frozenset({TAXABLE_DIVIDENDS}),
        ),
        (
            Sum,
            frozenset(
                {
                    T3_INVESTMENT_INCOME,
                    T5_INVESTMENT_INCOME,
                    T5013_INVESTMENT_INCOME,
                    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
                    TAX_REFUND_INTEREST,
                    FOREIGN_INVESTMENT_INCOME,
                    INVESTMENT_INCOME_WITHOUT_A_SLIP,
                    INVESTMENT_ROYALTIES,
                }
            ),
            frozenset({INVESTMENT_INCOME_BEFORE_PRIOR_YEARS}),
        ),
        (
            Subtract,
            frozenset(
                {INVESTMENT_INCOME_BEFORE_PRIOR_YEARS, INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS}
            ),
            frozenset({INTEREST_AND_OTHER_INVESTMENT_INCOME}),
        ),
        (
            Sum,
            frozenset(
                {WORKERS_COMPENSATION_BENEFITS, SOCIAL_ASSISTANCE_PAYMENTS, NET_FEDERAL_SUPPLEMENTS}
            ),
            frozenset({INCOME_SUPPORT_BENEFITS}),
        ),
        (
            Sum,
            frozenset(
                {
                    EMPLOYMENT_INCOME,
                    OTHER_EMPLOYMENT_INCOME,
                    OLD_AGE_SECURITY,
                    CPP_OR_QPP_BENEFITS,
                    OTHER_PENSIONS_AND_SUPERANNUATION,
                    ELECTED_SPLIT_PENSION_AMOUNT,
                    UNIVERSAL_CHILD_CARE_BENEFIT,
                    EI_AND_OTHER_BENEFITS,
                    TAXABLE_DIVIDENDS,
                    INTEREST_AND_OTHER_INVESTMENT_INCOME,
                    NET_PARTNERSHIP_INCOME,
                    RDSP_INCOME,
                    TAXABLE_CAPITAL_GAINS,
                    TAXABLE_SUPPORT_PAYMENTS,
                    RRSP_INCOME,
                    FHSA_INCOME,
                    OTHER_FHSA_INCOME,
                    OTHER_INCOME,
                    TAXABLE_SCHOLARSHIPS,
                    INCOME_SUPPORT_BENEFITS,
                }
            ),
            frozenset({TOTAL_INCOME}),
        ),
        (
            Sum,
            frozenset({UNUSED_RRSP_CONTRIBUTIONS, RRSP_CONTRIBUTIONS}),
            frozenset({RRSP_CONTRIBUTIONS_AVAILABLE}),
        ),
        (
            LesserOf,
            frozenset({RRSP_CONTRIBUTIONS_AVAILABLE, RRSP_DEDUCTION_LIMIT}),
            frozenset({RRSP_DEDUCTION_MAXIMUM}),
        ),
        (
            AtMost,
            frozenset({RRSP_AMOUNT_DEDUCTED, RRSP_DEDUCTION_MAXIMUM}),
            frozenset({RRSP_DEDUCTION}),
        ),
        (
            Subtract,
            frozenset({RRSP_CONTRIBUTIONS_AVAILABLE, RRSP_DEDUCTION}),
            frozenset({UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD}),
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
            frozenset(
                {RRSP_DEDUCTION, UNION_DUES, CHILD_CARE_EXPENSES, CPP_ENHANCED_CONTRIBUTIONS}
            ),
            frozenset({DEDUCTIONS_FROM_TOTAL_INCOME}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({TOTAL_INCOME, DEDUCTIONS_FROM_TOTAL_INCOME}),
            frozenset({NET_INCOME}),
        ),
        (
            Sum,
            frozenset({UNIVERSAL_CHILD_CARE_BENEFIT, RDSP_INCOME}),
            frozenset({UCCB_AND_RDSP_INCOME}),
        ),
        (
            Subtract,
            frozenset({NET_INCOME, UCCB_AND_RDSP_INCOME}),
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
            Sum,
            frozenset(
                {
                    CANADIAN_ARMED_FORCES_AND_POLICE_DEDUCTION,
                    SECURITY_OPTIONS_DEDUCTIONS,
                    OTHER_PAYMENTS_DEDUCTION,
                    LIMITED_PARTNERSHIP_LOSSES_OF_OTHER_YEARS,
                    NON_CAPITAL_LOSSES_OF_OTHER_YEARS,
                    ADDITIONAL_DEDUCTIONS,
                }
            ),
            frozenset({DEDUCTIONS_FROM_NET_INCOME}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({NET_INCOME, DEDUCTIONS_FROM_NET_INCOME}),
            frozenset({TAXABLE_INCOME}),
        ),
        (ProgressiveTax, frozenset({TAXABLE_INCOME}), frozenset({FEDERAL_BASIC_TAX})),
        (ProgressiveTax, frozenset({TAXABLE_INCOME}), frozenset({ONTARIO_BASIC_TAX})),
        (TaperedAmount, frozenset({NET_INCOME}), frozenset({BASIC_PERSONAL_AMOUNT})),
        (CreditAmount, frozenset(), frozenset({ontario.BASIC_PERSONAL_AMOUNT})),
        (CappedAmount, frozenset({EMPLOYMENT_INCOME}), frozenset({CANADA_EMPLOYMENT_AMOUNT})),
        (CreditAmount, frozenset(), frozenset({AGE_MAXIMUM})),
        (CreditAmount, frozenset(), frozenset({AGE_INCOME_THRESHOLD})),
        (
            SubtractNotBelowZero,
            frozenset({NET_INCOME, AGE_INCOME_THRESHOLD}),
            frozenset({AGE_INCOME_OVER_THRESHOLD}),
        ),
        (ApplyRate, frozenset({AGE_INCOME_OVER_THRESHOLD}), frozenset({AGE_REDUCTION})),
        (
            SubtractNotBelowZero,
            frozenset({AGE_MAXIMUM, AGE_REDUCTION}),
            frozenset({AGE_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({AGE_AMOUNT_BEFORE_COUNT, BORN_IN_1960_OR_EARLIER}),
            frozenset({AGE_AMOUNT}),
        ),
        (
            PerUnitAmount,
            frozenset({SPOUSE_CAREGIVER_ELIGIBLE}),
            frozenset({SPOUSE_INFIRMITY_SUPPLEMENT}),
        ),
        (
            Sum,
            frozenset({BASIC_PERSONAL_AMOUNT, SPOUSE_INFIRMITY_SUPPLEMENT}),
            frozenset({SPOUSE_AMOUNT_BASIS}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({SPOUSE_AMOUNT_BASIS, SPOUSE_NET_INCOME}),
            frozenset({SPOUSE_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({SPOUSE_AMOUNT_BEFORE_COUNT, SPOUSES_CLAIMED}),
            frozenset({SPOUSE_AMOUNT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({BASIC_PERSONAL_AMOUNT, DEPENDANT_NET_INCOME}),
            frozenset({ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT, ELIGIBLE_DEPENDANTS}),
            frozenset({ELIGIBLE_DEPENDANT_AMOUNT}),
        ),
        (CreditAmount, frozenset(), frozenset({SPOUSE_CAREGIVER_BASE})),
        (
            SubtractNotBelowZero,
            frozenset({SPOUSE_CAREGIVER_BASE, SPOUSE_NET_INCOME}),
            frozenset({SPOUSE_CAREGIVER_BEFORE_MAXIMUM}),
        ),
        (
            CappedAmount,
            frozenset({SPOUSE_CAREGIVER_BEFORE_MAXIMUM}),
            frozenset({SPOUSE_CAREGIVER_LIMIT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({SPOUSE_CAREGIVER_LIMIT, SPOUSE_AMOUNT}),
            frozenset({SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({SPOUSE_CAREGIVER_AMOUNT_BEFORE_COUNT, SPOUSE_CAREGIVER_ELIGIBLE}),
            frozenset({SPOUSE_CAREGIVER_AMOUNT}),
        ),
        (PerUnitAmount, frozenset({INFIRM_CHILDREN}), frozenset({INFIRM_CHILDREN_AMOUNT})),
        (CreditAmount, frozenset(), frozenset({ontario.AGE_MAXIMUM})),
        (CreditAmount, frozenset(), frozenset({ontario.AGE_INCOME_THRESHOLD})),
        (
            SubtractNotBelowZero,
            frozenset({NET_INCOME, ontario.AGE_INCOME_THRESHOLD}),
            frozenset({ontario.AGE_INCOME_OVER_THRESHOLD}),
        ),
        (
            ApplyRate,
            frozenset({ontario.AGE_INCOME_OVER_THRESHOLD}),
            frozenset({ontario.AGE_REDUCTION}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ontario.AGE_MAXIMUM, ontario.AGE_REDUCTION}),
            frozenset({ontario.AGE_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({ontario.AGE_AMOUNT_BEFORE_COUNT, BORN_IN_1960_OR_EARLIER}),
            frozenset({ontario.AGE_AMOUNT}),
        ),
        (CreditAmount, frozenset(), frozenset({ontario.SPOUSE_BASE})),
        (
            SubtractNotBelowZero,
            frozenset({ontario.SPOUSE_BASE, SPOUSE_NET_INCOME}),
            frozenset({ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM}),
        ),
        (
            CappedAmount,
            frozenset({ontario.SPOUSE_AMOUNT_BEFORE_MAXIMUM}),
            frozenset({ontario.SPOUSE_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({ontario.SPOUSE_AMOUNT_BEFORE_COUNT, SPOUSES_CLAIMED}),
            frozenset({ontario.SPOUSE_AMOUNT}),
        ),
        (CreditAmount, frozenset(), frozenset({ELIGIBLE_DEPENDANT_BASE})),
        (
            SubtractNotBelowZero,
            frozenset({ELIGIBLE_DEPENDANT_BASE, DEPENDANT_NET_INCOME}),
            frozenset({ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM}),
        ),
        (
            CappedAmount,
            frozenset({ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM}),
            frozenset({ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT}),
        ),
        (
            TimesCount,
            frozenset({ontario.ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT, ELIGIBLE_DEPENDANTS}),
            frozenset({ontario.ELIGIBLE_DEPENDANT_AMOUNT}),
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
                    INFIRM_CHILDREN_AMOUNT,
                    CPP_BASE_CONTRIBUTIONS,
                    EI_PREMIUMS,
                    CANADA_EMPLOYMENT_AMOUNT,
                }
            ),
            frozenset({NON_REFUNDABLE_CREDIT_AMOUNTS}),
        ),
        (
            Sum,
            frozenset(
                {
                    ontario.BASIC_PERSONAL_AMOUNT,
                    ontario.AGE_AMOUNT,
                    ontario.SPOUSE_AMOUNT,
                    ontario.ELIGIBLE_DEPENDANT_AMOUNT,
                    CPP_BASE_CONTRIBUTIONS,
                    EI_PREMIUMS,
                }
            ),
            frozenset({ontario.NON_REFUNDABLE_CREDIT_AMOUNTS}),
        ),
        (
            ApplyRate,
            frozenset({NON_REFUNDABLE_CREDIT_AMOUNTS}),
            frozenset({NON_REFUNDABLE_TAX_CREDITS}),
        ),
        (
            ApplyRate,
            frozenset({ontario.NON_REFUNDABLE_CREDIT_AMOUNTS}),
            frozenset({ontario.NON_REFUNDABLE_TAX_CREDITS}),
        ),
        (
            Sum,
            frozenset(
                {
                    T3_DIVIDEND_TAX_CREDIT,
                    T4PS_DIVIDEND_TAX_CREDIT,
                    T5_DIVIDEND_TAX_CREDIT,
                    T5013_DIVIDEND_TAX_CREDIT,
                }
            ),
            frozenset({SLIP_DIVIDEND_TAX_CREDIT}),
        ),
        (
            Sum,
            frozenset({DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP}),
            frozenset({DIVIDENDS_AMOUNT_A}),
        ),
        (Sum, frozenset({OTHER_DIVIDENDS_GROSSED_UP}), frozenset({DIVIDENDS_AMOUNT_B})),
        (ApplyRate, frozenset({DIVIDENDS_AMOUNT_B}), frozenset({OTHER_DIVIDENDS_CREDIT})),
        (
            Subtract,
            frozenset({DIVIDENDS_AMOUNT_A, DIVIDENDS_AMOUNT_B}),
            frozenset({DIVIDENDS_AMOUNT_A_LESS_B}),
        ),
        (
            ApplyRate,
            frozenset({DIVIDENDS_AMOUNT_A_LESS_B}),
            frozenset({ELIGIBLE_DIVIDENDS_CREDIT}),
        ),
        (
            Sum,
            frozenset({OTHER_DIVIDENDS_CREDIT, ELIGIBLE_DIVIDENDS_CREDIT}),
            frozenset({NO_SLIP_DIVIDEND_TAX_CREDIT}),
        ),
        (
            Sum,
            frozenset({SLIP_DIVIDEND_TAX_CREDIT, NO_SLIP_DIVIDEND_TAX_CREDIT}),
            frozenset({DIVIDEND_TAX_CREDIT}),
        ),
        (
            Sum,
            frozenset({NON_REFUNDABLE_TAX_CREDITS, DIVIDEND_TAX_CREDIT}),
            frozenset({CREDITS_AGAINST_BASIC_FEDERAL_TAX}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({FEDERAL_BASIC_TAX, CREDITS_AGAINST_BASIC_FEDERAL_TAX}),
            frozenset({FEDERAL_TAX_AFTER_CREDITS}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ONTARIO_BASIC_TAX, ontario.NON_REFUNDABLE_TAX_CREDITS}),
            frozenset({ONTARIO_TAX_AFTER_CREDITS}),
        ),
        (TieredSurcharge, frozenset({ONTARIO_TAX_AFTER_CREDITS}), frozenset({ONTARIO_SURTAX})),
        (
            Sum,
            frozenset({ONTARIO_TAX_AFTER_CREDITS, ONTARIO_SURTAX}),
            frozenset({ONTARIO_TAX_WITH_SURTAX}),
        ),
        (
            Sum,
            frozenset({ONTARIO_TAX_AFTER_CREDITS}),
            frozenset({ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT}),
        ),
        (Sum, frozenset({TAXABLE_DIVIDENDS}), frozenset({ontario.DIVIDENDS_AMOUNT_A})),
        (
            Sum,
            frozenset({TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
            frozenset({ontario.DIVIDENDS_AMOUNT_B}),
        ),
        (
            ApplyRate,
            frozenset({ontario.DIVIDENDS_AMOUNT_B}),
            frozenset({ontario.OTHER_DIVIDENDS_CREDIT}),
        ),
        (
            Subtract,
            frozenset({ontario.DIVIDENDS_AMOUNT_A, ontario.DIVIDENDS_AMOUNT_B}),
            frozenset({ontario.DIVIDENDS_AMOUNT_A_LESS_B}),
        ),
        (
            ApplyRate,
            frozenset({ontario.DIVIDENDS_AMOUNT_A_LESS_B}),
            frozenset({ontario.ELIGIBLE_DIVIDENDS_CREDIT}),
        ),
        (
            Sum,
            frozenset({ontario.OTHER_DIVIDENDS_CREDIT, ontario.ELIGIBLE_DIVIDENDS_CREDIT}),
            frozenset({ontario.DIVIDEND_TAX_CREDIT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT, ontario.DIVIDEND_TAX_CREDIT}),
            frozenset({ONTARIO_TAX_LESS_DIVIDEND_CREDIT}),
        ),
        (
            Sum,
            frozenset({ontario.DIVIDEND_TAX_CREDIT}),
            frozenset({ontario.DIVIDEND_CREDIT_FROM_LINE_57}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ONTARIO_TAX_WITH_SURTAX, ontario.DIVIDEND_CREDIT_FROM_LINE_57}),
            frozenset({ONTARIO_TAX_AFTER_DIVIDEND_CREDIT}),
        ),
        (CreditAmount, frozenset(), frozenset({TAX_REDUCTION_BASIC})),
        (PerUnitAmount, frozenset({DEPENDENT_CHILDREN}), frozenset({TAX_REDUCTION_FOR_CHILDREN})),
        (PerUnitAmount, frozenset({DEPENDANTS}), frozenset({TAX_REDUCTION_FOR_DEPENDANTS})),
        (
            Sum,
            frozenset(
                {TAX_REDUCTION_BASIC, TAX_REDUCTION_FOR_CHILDREN, TAX_REDUCTION_FOR_DEPENDANTS}
            ),
            frozenset({TAX_REDUCTION_AMOUNTS}),
        ),
        (
            MultipleOver,
            frozenset({TAX_REDUCTION_AMOUNTS, ONTARIO_TAX_AFTER_DIVIDEND_CREDIT}),
            frozenset({ONTARIO_TAX_REDUCTION}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ONTARIO_TAX_AFTER_DIVIDEND_CREDIT, ONTARIO_TAX_REDUCTION}),
            frozenset({ONTARIO_TAX_AFTER_REDUCTION}),
        ),
        (ApplyRate, frozenset({EMPLOYMENT_INCOME}), frozenset({LIFT_CREDIT_BEFORE_MAXIMUM})),
        (CappedAmount, frozenset({LIFT_CREDIT_BEFORE_MAXIMUM}), frozenset({LIFT_MAXIMUM_CREDIT})),
        (TieredSurcharge, frozenset({NET_INCOME}), frozenset({LIFT_REDUCTION})),
        (
            SubtractNotBelowZero,
            frozenset({LIFT_MAXIMUM_CREDIT, LIFT_REDUCTION}),
            frozenset({LIFT_CREDIT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ONTARIO_TAX_AFTER_REDUCTION, LIFT_CREDIT}),
            frozenset({ONTARIO_TAX_AFTER_LIFT_CREDIT}),
        ),
        (
            ApplyRate,
            frozenset({COMMUNITY_FOOD_PROGRAM_DONATIONS}),
            frozenset({COMMUNITY_FOOD_PROGRAM_CREDIT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ONTARIO_TAX_AFTER_LIFT_CREDIT, COMMUNITY_FOOD_PROGRAM_CREDIT}),
            frozenset({ONTARIO_TAX_AFTER_FOOD_CREDIT}),
        ),
        (TieredSurcharge, frozenset({TAXABLE_INCOME}), frozenset({ONTARIO_HEALTH_PREMIUM})),
        (
            Sum,
            frozenset({ONTARIO_TAX_AFTER_FOOD_CREDIT, ONTARIO_HEALTH_PREMIUM}),
            frozenset({ONTARIO_TAX}),
        ),
        (Sum, frozenset({FEDERAL_TAX_AFTER_CREDITS}), frozenset({NET_FEDERAL_TAX})),
        (Sum, frozenset({NET_FEDERAL_TAX, ONTARIO_TAX}), frozenset({TOTAL_PAYABLE})),
        (Sum, frozenset({EMPLOYMENT_INCOME}), frozenset({WORKING_INCOME})),
        (Sum, frozenset({NET_INCOME}), frozenset({ADJUSTED_FAMILY_NET_INCOME})),
        (
            TieredSurcharge,
            frozenset({WORKING_INCOME}),
            frozenset({CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT}),
        ),
        (
            TieredSurcharge,
            frozenset({WORKING_INCOME}),
            frozenset({CWB_BEFORE_REDUCTION_WITH_DEPENDANT}),
        ),
        (
            TieredSurcharge,
            frozenset({ADJUSTED_FAMILY_NET_INCOME}),
            frozenset({CWB_REDUCTION_WITHOUT_DEPENDANT}),
        ),
        (
            TieredSurcharge,
            frozenset({ADJUSTED_FAMILY_NET_INCOME}),
            frozenset({CWB_REDUCTION_WITH_DEPENDANT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT, CWB_REDUCTION_WITHOUT_DEPENDANT}),
            frozenset({CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({CWB_BEFORE_REDUCTION_WITH_DEPENDANT, CWB_REDUCTION_WITH_DEPENDANT}),
            frozenset({CANADA_WORKERS_BENEFIT_WITH_DEPENDANT}),
        ),
        (
            ChooseByCount,
            frozenset(
                {
                    CWB_ELIGIBLE_DEPENDANTS,
                    CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
                    CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
                }
            ),
            frozenset({CANADA_WORKERS_BENEFIT}),
        ),
        (ApplyRate, frozenset({FERTILITY_EXPENSES}), frozenset({FERTILITY_CREDIT_BEFORE_MAXIMUM})),
        (CappedAmount, frozenset({FERTILITY_CREDIT_BEFORE_MAXIMUM}), frozenset({FERTILITY_CREDIT})),
        (
            CappedAmount,
            frozenset({SENIORS_TRANSIT_PAID}),
            frozenset({SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM}),
        ),
        (
            ApplyRate,
            frozenset({SENIORS_TRANSIT_AMOUNT_PAID_AT_MOST_MAXIMUM}),
            frozenset({SENIORS_TRANSIT_CREDIT}),
        ),
        (
            FlowThroughShareExpenses,
            frozenset({FLOW_THROUGH_SHARE_SLIPS}),
            frozenset({FLOW_THROUGH_SHARE_EXPENSES}),
        ),
        (
            ApplyRate,
            frozenset({FLOW_THROUGH_SHARE_EXPENSES}),
            frozenset({FLOW_THROUGH_SHARE_CREDIT}),
        ),
        (
            Sum,
            frozenset({FERTILITY_CREDIT, SENIORS_TRANSIT_CREDIT, FLOW_THROUGH_SHARE_CREDIT}),
            frozenset({ONTARIO_CREDITS_SUBTOTAL}),
        ),
        (Sum, frozenset({ONTARIO_CREDITS_SUBTOTAL}), frozenset({ONTARIO_CREDITS})),
        (Sum, frozenset({ONTARIO_CREDITS}), frozenset({PROVINCIAL_CREDITS})),
        (
            Sum,
            frozenset({INCOME_TAX_DEDUCTED, CANADA_WORKERS_BENEFIT, PROVINCIAL_CREDITS}),
            frozenset({TOTAL_CREDITS}),
        ),
        (
            Subtract,
            frozenset({TOTAL_PAYABLE, TOTAL_CREDITS}),
            frozenset({REFUND_OR_BALANCE_OWING}),
        ),
    }
