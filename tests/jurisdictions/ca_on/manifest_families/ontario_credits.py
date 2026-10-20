"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.tiered_surcharge import TieredSurcharge
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    CPP_BASE_CONTRIBUTIONS,
    DONATIONS_FIRST_TIER,
    DONATIONS_OVER_FIRST_TIER,
    EI_PREMIUMS,
    TAXABLE_DIVIDENDS,
    TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.catalog import (
    ONTARIO_BASIC_TAX,
    ONTARIO_SURTAX,
    ONTARIO_TAX_AFTER_CREDITS,
    ONTARIO_TAX_AFTER_DIVIDEND_CREDIT,
    ONTARIO_TAX_BEFORE_DIVIDEND_CREDIT,
    ONTARIO_TAX_LESS_DIVIDEND_CREDIT,
    ONTARIO_TAX_WITH_SURTAX,
)

INPUTS = frozenset[str]()

OUTPUTS = frozenset(
    {
        "ca-on/ontario_tax_less_dividend_credit",
    }
)

STEPS = {
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca-on/basic_personal_amount",
                "ca-on/age_amount",
                "ca-on/spouse_amount",
                "ca-on/eligible_dependant_amount",
                "ca-on/caregiver_amount",
                "ca/cpp_base_contributions",
                "ca/ei_premiums",
                "ca-on/medical_claim",
            )
        },
        produces={"output": "ca-on/non_refundable_credit_amounts"},
    ),
    # ON428 line 46 (line 58840) "Line 44 multiplied by the percentage from line 45": the
    # Ontario credit rate is applied once, to the total of credit amounts. It is the first of
    # the two lines that line 50 adds.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca-on/credit_rate"},
        consumes={"base": "ca-on/non_refundable_credit_amounts"},
        produces={"output": "ca-on/credit_amounts_at_credit_rate"},
    ),
    # ON428 line 47 "Amount from line 13 of your federal Schedule 9" "multiplied by 5.05%":
    # 5.05% of the first $200 of the donations and gifts, the federal Schedule 9 line 13.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca-on/donation_first_tier_rate"},
        consumes={"base": "ca/donations_first_tier"},
        produces={"output": "ca-on/donations_first_tier_credit"},
    ),
    # ON428 line 48 "Amount from line 14 of your federal Schedule 9" "multiplied by 11.16%":
    # 11.16% of the rest of the donations and gifts, the federal Schedule 9 line 14.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca-on/donation_over_first_tier_rate"},
        consumes={"base": "ca/donations_over_first_tier"},
        produces={"output": "ca-on/donations_over_first_tier_credit"},
    ),
    # ON428 line 49 and line 58969 "Line 47 plus line 48".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca-on/donations_first_tier_credit",
                "ca-on/donations_over_first_tier_credit",
            )
        },
        produces={"output": "ca-on/donations_and_gifts_credit"},
    ),
    # ON428 line 50 and line 61500 "Line 46 plus line 49 Enter this amount on line 52.
    # Ontario non-refundable tax credits": line 46 (line 58840) and line 49 (line 58969), in
    # line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca-on/credit_amounts_at_credit_rate", "ca-on/donations_and_gifts_credit")
        },
        produces={"output": "ca-on/non_refundable_tax_credits"},
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
    # ON428 lines 66 to 68: the surtax on line 65, which is the Ontario tax after credits
    # while line 64 (tax on split income) is not modelled.
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
}

WIRING = {
    (
        Sum,
        frozenset(
            {
                ontario.BASIC_PERSONAL_AMOUNT,
                ontario.AGE_AMOUNT,
                ontario.SPOUSE_AMOUNT,
                ontario.ELIGIBLE_DEPENDANT_AMOUNT,
                ontario.CAREGIVER_AMOUNT,
                CPP_BASE_CONTRIBUTIONS,
                EI_PREMIUMS,
                ontario.MEDICAL_CLAIM,
            }
        ),
        frozenset({ontario.NON_REFUNDABLE_CREDIT_AMOUNTS}),
    ),
    (
        ApplyRate,
        frozenset({ontario.NON_REFUNDABLE_CREDIT_AMOUNTS}),
        frozenset({ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE}),
    ),
    (
        ApplyRate,
        frozenset({DONATIONS_FIRST_TIER}),
        frozenset({ontario.DONATIONS_FIRST_TIER_CREDIT}),
    ),
    (
        ApplyRate,
        frozenset({DONATIONS_OVER_FIRST_TIER}),
        frozenset({ontario.DONATIONS_OVER_FIRST_TIER_CREDIT}),
    ),
    (
        Sum,
        frozenset({ontario.DONATIONS_FIRST_TIER_CREDIT, ontario.DONATIONS_OVER_FIRST_TIER_CREDIT}),
        frozenset({ontario.DONATIONS_AND_GIFTS_CREDIT}),
    ),
    (
        Sum,
        frozenset({ontario.CREDIT_AMOUNTS_AT_CREDIT_RATE, ontario.DONATIONS_AND_GIFTS_CREDIT}),
        frozenset({ontario.NON_REFUNDABLE_TAX_CREDITS}),
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
}
