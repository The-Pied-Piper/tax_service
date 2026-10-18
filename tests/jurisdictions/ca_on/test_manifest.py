"""The CA-ON manifest: what it selects, and that production code builds it into a composition.

Building it through `TaxComputationService.compose` resolves every slot: each capability name to a
registered class, each parameter slot's family to a dataset of the slot's kind for the tax year,
and each artifact identifier to a registered kind of the slot's value type.
"""

from __future__ import annotations

import app.registrations  # lists the packages; build_tax_computation registers their catalogs
from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.application.services.tax_computation import TaxComputationService
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.contribution_tier import TieredContribution
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.lesser_of import LesserOf
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.tapered_amount import TaperedAmount
from app.domain.capabilities.tiered_surcharge import TieredSurcharge
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Manifest
from app.jurisdictions.ca.catalog import (
    BASIC_PERSONAL_AMOUNT,
    CANADA_EMPLOYMENT_AMOUNT,
    CAPITAL_GAIN,
    CPP_BASE_CONTRIBUTIONS,
    CPP_ENHANCED_CONTRIBUTIONS,
    CPP_FIRST_ADDITIONAL_CONTRIBUTIONS,
    CPP_SECOND_ADDITIONAL_CONTRIBUTIONS,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    EI_PREMIUMS,
    EMPLOYMENT_INCOME,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    NET_INCOME,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    NON_REFUNDABLE_TAX_CREDITS,
    RRSP_CONTRIBUTIONS,
    RRSP_CONTRIBUTIONS_AVAILABLE,
    RRSP_DEDUCTION,
    RRSP_DEDUCTION_LIMIT,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    UNION_DUES,
    UNUSED_RRSP_CONTRIBUTIONS,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    ONTARIO_BASIC_TAX,
    ONTARIO_SURTAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_WITH_SURTAX,
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
            "ca/union_dues",
        }
    )
    assert found.outputs == frozenset(
        {"ca/federal_tax_after_credits", "ca-on/ontario_tax_with_surtax"}
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
        # Schedule 7 line 20 "Enter whichever is less: amount from line 10 or line 19. Enter this
        # amount on line 20800 of your return.": with no employer PRPP contributions (line 12)
        # and no transfers (line 15), line 13 is the limit and line 16 the contributions
        # available to deduct; line 17 is the lesser of lines 13 and 16, deducted in full on
        # line 18, so line 19 is line 17, and line 20 is the lesser of the contributions
        # available to deduct and the limit. In line 20's order: the contributions available to
        # deduct (line 10), then the limit, which bounds line 19.
        CapabilitySelection(
            name="core/lesser_of",
            params={},
            consumes={"amounts": ("ca/rrsp_contributions_available", "ca/rrsp_deduction_limit")},
            produces={"output": "ca/rrsp_deduction"},
        ),
        # T1 line 23300: the deductions in the form's line order (20800, 21200, 22215).
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/rrsp_deduction",
                    "ca/union_dues",
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
        # T1 line 33500 (lines 30000, 30800, 31200, 31260) and ON428 line 58800 (lines 58040,
        # 58240, 58300), in the forms' line order. ON428 lines 58240 and 58300 are "Amount from
        # line 30800 / 31200 of your return", so the Ontario sum reads the federal kinds; it has
        # no Canada employment amount.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={
                "parts": (
                    "ca/basic_personal_amount",
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
    }
    assert len(found.capabilities) == 26


def test_its_first_tax_year_composes_every_selection() -> None:
    composition = service().compose(CA_ON, 2025)

    wiring = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composition.order
    }
    assert len(composition.order) == 26
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
            frozenset({RRSP_DEDUCTION}),
        ),
        (
            Sum,
            frozenset({RRSP_DEDUCTION, UNION_DUES, CPP_ENHANCED_CONTRIBUTIONS}),
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
            Sum,
            frozenset(
                {
                    BASIC_PERSONAL_AMOUNT,
                    CPP_BASE_CONTRIBUTIONS,
                    EI_PREMIUMS,
                    CANADA_EMPLOYMENT_AMOUNT,
                }
            ),
            frozenset({NON_REFUNDABLE_CREDIT_AMOUNTS}),
        ),
        (
            Sum,
            frozenset({ontario.BASIC_PERSONAL_AMOUNT, CPP_BASE_CONTRIBUTIONS, EI_PREMIUMS}),
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
    }
