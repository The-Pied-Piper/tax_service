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
    ADJUSTED_FAMILY_NET_INCOME,
    BASIC_PERSONAL_AMOUNT,
    CANADA_EMPLOYMENT_AMOUNT,
    CANADA_WORKERS_BENEFIT,
    CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
    CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
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
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
    CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
    CWB_REDUCTION_WITH_DEPENDANT,
    CWB_REDUCTION_WITHOUT_DEPENDANT,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    DEPENDANT_NET_INCOME,
    EI_PREMIUMS,
    ELIGIBLE_DEPENDANT_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
    ELIGIBLE_DEPENDANTS,
    EMPLOYMENT_INCOME,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    INCOME_TAX_DEDUCTED,
    INFIRM_CHILDREN,
    INFIRM_CHILDREN_AMOUNT,
    NET_FEDERAL_TAX,
    NET_INCOME,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    REFUND_OR_BALANCE_OWING,
    RRSP_AMOUNT_DEDUCTED,
    RRSP_CONTRIBUTIONS,
    RRSP_CONTRIBUTIONS_AVAILABLE,
    RRSP_DEDUCTION,
    RRSP_DEDUCTION_LIMIT,
    RRSP_DEDUCTION_MAXIMUM,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
    TOTAL_CREDITS,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
    UNION_DUES,
    UNUSED_RRSP_CONTRIBUTIONS,
    UNUSED_RRSP_CONTRIBUTIONS_CARRIED_FORWARD,
    WORKING_INCOME,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    DEPENDANTS,
    DEPENDENT_CHILDREN,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
    ELIGIBLE_DEPENDANT_BASE,
    LIFT_CREDIT,
    LIFT_CREDIT_BEFORE_MAXIMUM,
    LIFT_MAXIMUM_CREDIT,
    LIFT_REDUCTION,
    ONTARIO_BASIC_TAX,
    ONTARIO_HEALTH_PREMIUM,
    ONTARIO_SURTAX,
    ONTARIO_TAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_AFTER_LIFT_CREDIT,
    ONTARIO_TAX_AFTER_REDUCTION,
    ONTARIO_TAX_REDUCTION,
    ONTARIO_TAX_WITH_SURTAX,
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
            "ca/child_care_expenses_paid",
            "ca/children_under_seven",
            "ca/children_with_disability",
            "ca/children_seven_to_sixteen",
            "ca/income_tax_deducted",
        }
    )
    # T1 line 167, the refund or balance owing, and Schedule 7 line 23, what the return produces
    # for the next year's line 1: the two lines the computation returns.
    assert found.outputs == frozenset(
        {"ca/refund_or_balance_owing", "ca/unused_rrsp_contributions_carried_forward"}
    )
    # List order carries no meaning: the composition derives the run order from the contracts.
    assert set(found.capabilities) == {
        CapabilitySelection(
            name="core/apply_rate",
            params={"rate": "ca/capital_gains_inclusion_rate"},
            consumes={"base": "ca/capital_gain"},
            produces={"output": "ca/taxable_capital_gains"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/employment_income", "ca/taxable_capital_gains")},
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
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ()},
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
        # T1 line 83 (line 30500) "Canada caregiver amount for infirm children under 18 years of
        # age (see Schedule 5) Number of children you are claiming this amount for Line 30499"
        # "multiplied by $2,687".
        CapabilitySelection(
            name="core/per_unit_amount",
            params={"amount": "ca/infirm_child_amount"},
            consumes={"count": "ca/infirm_children"},
            produces={"output": "ca/infirm_children_amount"},
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
        # T1 line 33500 (lines 30000, 30400, 30500, 30800, 31200, 31260) and ON428 line 58800
        # (lines 58040, 58160, 58240, 58300), in the forms' line order. ON428 lines 58240 and
        # 58300 are "Amount from line 30800 / 31200 of your return", so the Ontario sum reads the
        # federal kinds; it has no Canada employment amount.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/basic_personal_amount",
                    "ca/eligible_dependant_amount",
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
        # Each form's credits come off its basic tax, not below zero: the unused part is lost.
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={"amount": "ca/federal_basic_tax", "less": "ca/non_refundable_tax_credits"},
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
        # reduction": line 73 is the Ontario tax with surtax while neither the dividend tax
        # credit (line 70) nor the minimum tax (line 72) is modelled.
        CapabilitySelection(
            name="core/multiple_over",
            params={"factor": "ca-on/tax_reduction_factor"},
            consumes={
                "amount": "ca-on/tax_reduction_amounts",
                "less": "ca-on/ontario_tax_with_surtax",
            },
            produces={"output": "ca-on/ontario_tax_reduction"},
        ),
        # ON428 line 81 "Line 73 minus line 80 (if negative, enter "0")".
        CapabilitySelection(
            name="core/subtract_not_below_zero",
            params={},
            consumes={
                "amount": "ca-on/ontario_tax_with_surtax",
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
                "parts": ("ca-on/ontario_tax_after_lift_credit", "ca-on/ontario_health_premium")
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
        # spouse or dependant when the T1 line 30400 count is 0, else the line with one; that
        # count stands in for Schedule 6's own eligible dependant; an eligible spouse is not
        # modelled.
        CapabilitySelection(
            name="core/choose_by_count",
            params={},
            consumes={
                "count": "ca/eligible_dependants",
                "when_none": "ca/canada_workers_benefit_without_dependant",
                "when_any": "ca/canada_workers_benefit_with_dependant",
            },
            produces={"output": "ca/canada_workers_benefit"},
        ),
        # T1 line 166 (line 48200) "Add lines 150 to 165. Total credits": line 150 (43700) and
        # line 155 (45300) "Canada workers benefit (CWB) (complete Schedule 6)", in line order,
        # as the other lines are not triggered.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/income_tax_deducted", "ca/canada_workers_benefit")},
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
    assert len(found.capabilities) == 68


def test_its_first_tax_year_composes_every_selection() -> None:
    composition = service().compose(CA_ON, 2025)

    wiring = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composition.order
    }
    assert len(composition.order) == 68
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
            frozenset({EMPLOYMENT_INCOME, TAXABLE_CAPITAL_GAINS}),
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
        (Sum, frozenset(), frozenset({DEDUCTIONS_FROM_NET_INCOME})),
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
        (PerUnitAmount, frozenset({INFIRM_CHILDREN}), frozenset({INFIRM_CHILDREN_AMOUNT})),
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
                    ELIGIBLE_DEPENDANT_AMOUNT,
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
            SubtractNotBelowZero,
            frozenset({FEDERAL_BASIC_TAX, NON_REFUNDABLE_TAX_CREDITS}),
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
            frozenset({TAX_REDUCTION_AMOUNTS, ONTARIO_TAX_WITH_SURTAX}),
            frozenset({ONTARIO_TAX_REDUCTION}),
        ),
        (
            SubtractNotBelowZero,
            frozenset({ONTARIO_TAX_WITH_SURTAX, ONTARIO_TAX_REDUCTION}),
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
        (TieredSurcharge, frozenset({TAXABLE_INCOME}), frozenset({ONTARIO_HEALTH_PREMIUM})),
        (
            Sum,
            frozenset({ONTARIO_TAX_AFTER_LIFT_CREDIT, ONTARIO_HEALTH_PREMIUM}),
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
                    ELIGIBLE_DEPENDANTS,
                    CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
                    CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
                }
            ),
            frozenset({CANADA_WORKERS_BENEFIT}),
        ),
        (
            Sum,
            frozenset({INCOME_TAX_DEDUCTED, CANADA_WORKERS_BENEFIT}),
            frozenset({TOTAL_CREDITS}),
        ),
        (
            Subtract,
            frozenset({TOTAL_PAYABLE, TOTAL_CREDITS}),
            frozenset({REFUND_OR_BALANCE_OWING}),
        ),
    }
