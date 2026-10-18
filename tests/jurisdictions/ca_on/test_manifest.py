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
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.non_refundable_credit import NonRefundableCredit
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Manifest
from app.jurisdictions.ca.catalog import (
    BASIC_PERSONAL_AMOUNT,
    CAPITAL_GAIN,
    DEDUCTIONS_FROM_NET_INCOME,
    DEDUCTIONS_FROM_TOTAL_INCOME,
    EMPLOYMENT_INCOME,
    FEDERAL_BASIC_TAX,
    FEDERAL_TAX_AFTER_CREDITS,
    NET_INCOME,
    NON_REFUNDABLE_CREDIT_AMOUNTS,
    RRSP_DEDUCTION,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    UNION_DUES,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import ONTARIO_BASIC_TAX, ONTARIO_TAX_AFTER_CREDITS
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
        {"ca/employment_income", "ca/capital_gain", "ca/rrsp_deduction", "ca/union_dues"}
    )
    assert found.outputs == frozenset(
        {"ca/federal_tax_after_credits", "ca-on/ontario_tax_after_credits"}
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
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/rrsp_deduction", "ca/union_dues")},
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
        # Each basic personal amount dataset becomes an artifact of the same name (T1 line 30000,
        # ON428 line 58040), the first part of its form's total of credit amounts.
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca/basic_personal_amount"},
            consumes={},
            produces={"output": "ca/basic_personal_amount"},
        ),
        CapabilitySelection(
            name="core/credit_amount",
            params={"amount": "ca-on/basic_personal_amount"},
            consumes={},
            produces={"output": "ca-on/basic_personal_amount"},
        ),
        # T1 line 33500 and ON428 line 58800: one part each for now.
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca/basic_personal_amount",)},
            produces={"output": "ca/non_refundable_credit_amounts"},
        ),
        CapabilitySelection(
            name="core/sum",
            params={},
            consumes={"parts": ("ca-on/basic_personal_amount",)},
            produces={"output": "ca-on/non_refundable_credit_amounts"},
        ),
        # The rate is applied once, to the total (T1 line 33800, ON428 line 58840).
        CapabilitySelection(
            name="core/non_refundable_credit",
            params={"rate": "ca/credit_rate"},
            consumes={"amounts": "ca/non_refundable_credit_amounts", "tax": "ca/federal_basic_tax"},
            produces={"output": "ca/federal_tax_after_credits"},
        ),
        CapabilitySelection(
            name="core/non_refundable_credit",
            params={"rate": "ca-on/credit_rate"},
            consumes={
                "amounts": "ca-on/non_refundable_credit_amounts",
                "tax": "ca-on/ontario_basic_tax",
            },
            produces={"output": "ca-on/ontario_tax_after_credits"},
        ),
    }
    assert len(found.capabilities) == 14


def test_its_first_tax_year_composes_every_selection() -> None:
    composition = service().compose(CA_ON, 2025)

    wiring = {
        (type(capability), capability.consumes, capability.produces)
        for capability in composition.order
    }
    assert len(composition.order) == 14
    assert wiring == {
        (ApplyRate, frozenset({CAPITAL_GAIN}), frozenset({TAXABLE_CAPITAL_GAINS})),
        (
            Sum,
            frozenset({EMPLOYMENT_INCOME, TAXABLE_CAPITAL_GAINS}),
            frozenset({TOTAL_INCOME}),
        ),
        (
            Sum,
            frozenset({RRSP_DEDUCTION, UNION_DUES}),
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
        (CreditAmount, frozenset(), frozenset({BASIC_PERSONAL_AMOUNT})),
        (CreditAmount, frozenset(), frozenset({ontario.BASIC_PERSONAL_AMOUNT})),
        (Sum, frozenset({BASIC_PERSONAL_AMOUNT}), frozenset({NON_REFUNDABLE_CREDIT_AMOUNTS})),
        (
            Sum,
            frozenset({ontario.BASIC_PERSONAL_AMOUNT}),
            frozenset({ontario.NON_REFUNDABLE_CREDIT_AMOUNTS}),
        ),
        (
            NonRefundableCredit,
            frozenset({NON_REFUNDABLE_CREDIT_AMOUNTS, FEDERAL_BASIC_TAX}),
            frozenset({FEDERAL_TAX_AFTER_CREDITS}),
        ),
        (
            NonRefundableCredit,
            frozenset({ontario.NON_REFUNDABLE_CREDIT_AMOUNTS, ONTARIO_BASIC_TAX}),
            frozenset({ONTARIO_TAX_AFTER_CREDITS}),
        ),
    }
