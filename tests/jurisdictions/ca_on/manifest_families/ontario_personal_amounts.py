"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.times_count import TimesCount
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.other_dependants_medical import OtherDependantsMedical
from app.jurisdictions.ca.catalog import (
    BORN_IN_1960_OR_EARLIER,
    DEPENDANT_NET_INCOME,
    ELIGIBLE_DEPENDANTS,
    MEDICAL_EXPENSES,
    NET_INCOME,
    OTHER_DEPENDANTS,
    SPOUSE_NET_INCOME,
    SPOUSES_CLAIMED,
    TAXABLE_INCOME,
)
from app.jurisdictions.ca_on import catalog as ontario
from app.jurisdictions.ca_on.capabilities.caregiver_amount import OntarioCaregiverAmount
from app.jurisdictions.ca_on.catalog import (
    CAREGIVER_DEPENDANTS,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_MAXIMUM,
    ELIGIBLE_DEPENDANT_BASE,
    ONTARIO_BASIC_TAX,
)

INPUTS = frozenset(
    {
        "ca-on/caregiver_dependants",
    }
)

OUTPUTS = frozenset[str]()

STEPS = {
    CapabilitySelection(
        name="core/progressive_tax",
        params={"schedule": "ca-on/brackets"},
        consumes={"base": "ca/taxable_income"},
        produces={"output": "ca-on/ontario_basic_tax"},
    ),
    # ON428 line 58040 has no reduction: the Ontario basic personal amount dataset becomes an
    # artifact of the same name, the first part of ON428's total of credit amounts.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca-on/basic_personal_amount"},
        consumes={},
        produces={"output": "ca-on/basic_personal_amount"},
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
    # ON428 line 39 "Line 37 multiplied by the percentage from line 38" (line 37 "Amount from
    # line 23600 of your return", line 38 "Applicable rate 3%"): 3% of the net income.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca-on/medical_net_income_rate"},
        consumes={"base": "ca/net_income"},
        produces={"output": "ca-on/medical_net_income_share"},
    ),
    # ON428 line 40 "Enter whichever is less: $2,885 or the amount on line 39."
    CapabilitySelection(
        name="core/capped_amount",
        params={"cap": "ca-on/medical_threshold_ceiling"},
        consumes={"base": "ca-on/medical_net_income_share"},
        produces={"output": "ca-on/medical_threshold"},
    ),
    # ON428 line 41 "Line 36 minus line 40 (if negative, enter "0")": line 36 is the filer's
    # medical expenses, the caller input of T1 line 107 (line 33099), shared with the T1.
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/medical_expenses", "less": "ca-on/medical_threshold"},
        produces={"output": "ca-on/medical_expenses_over_threshold"},
    ),
    # ON428 line 42 and line 58729 "Allowable amount of medical expenses for other dependants
    # (use Worksheet ON428)"; Worksheet ON428, line 58729, for each dependant: line 1 "Medical
    # expenses for other dependant", line 2 "Enter the amount from line 40 of the dependant's
    # Form ON428.", line 3 "Line 1 minus line 2 (if negative, enter "0") (maximum $15,551 per
    # dependant)", and line 4 "Add the amounts from line 3 of columns 1, 2, and 3 (and others,
    # if any). Enter this amount on line 58729 of your Form ON428." The same people as T1 line
    # 33199, so the same record list.
    CapabilitySelection(
        name="ca/other_dependants_medical",
        params={"reduction": "ca-on/other_dependants_medical_reduction"},
        consumes={"dependants": "ca/other_dependants"},
        produces={"output": "ca-on/other_dependants_medical"},
    ),
    # ON428 line 43 and line 58769 "Line 41 plus line 42".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": ("ca-on/medical_expenses_over_threshold", "ca-on/other_dependants_medical")
        },
        produces={"output": "ca-on/medical_claim"},
    ),
    # ON428 line 17 and line 58185 "Ontario caregiver amount (use Worksheet ON428)", Worksheet
    # ON428 "Line 58185 - Ontario caregiver amount": for each dependant, line 1 "Base amount
    # 26,562.00" less line 2 "Dependant's net income from line 23600 of their return", line 3
    # "Line 1 minus line 2 (if negative, enter "0") (maximum $6,008 per dependant)", line 4
    # "Amount claimed for this dependant on line 58160 of your Form ON428, if any", line 5
    # "Allowable amount for this dependant: line 3 minus line 4 (if negative, enter "0")" and
    # line 6 "Add the amounts from line 5 of columns 1, 2, and 3 (and others, if any). Enter
    # this amount on line 58185 of your Form ON428."
    CapabilitySelection(
        name="ca-on/caregiver_amount",
        params={
            "base": "ca-on/caregiver_base_amount",
            "maximum": "ca-on/caregiver_maximum_amount",
        },
        consumes={
            "dependants": "ca-on/caregiver_dependants",
            "eligible_dependant_amount": "ca-on/eligible_dependant_amount",
        },
        produces={"output": "ca-on/caregiver_amount"},
    ),
}

WIRING = {
    (ProgressiveTax, frozenset({TAXABLE_INCOME}), frozenset({ONTARIO_BASIC_TAX})),
    (CreditAmount, frozenset(), frozenset({ontario.BASIC_PERSONAL_AMOUNT})),
    (ApplyRate, frozenset({NET_INCOME}), frozenset({ontario.MEDICAL_NET_INCOME_SHARE})),
    (
        CappedAmount,
        frozenset({ontario.MEDICAL_NET_INCOME_SHARE}),
        frozenset({ontario.MEDICAL_THRESHOLD}),
    ),
    (
        SubtractNotBelowZero,
        frozenset({MEDICAL_EXPENSES, ontario.MEDICAL_THRESHOLD}),
        frozenset({ontario.MEDICAL_EXPENSES_OVER_THRESHOLD}),
    ),
    (
        OtherDependantsMedical,
        frozenset({OTHER_DEPENDANTS}),
        frozenset({ontario.OTHER_DEPENDANTS_MEDICAL}),
    ),
    (
        Sum,
        frozenset({ontario.MEDICAL_EXPENSES_OVER_THRESHOLD, ontario.OTHER_DEPENDANTS_MEDICAL}),
        frozenset({ontario.MEDICAL_CLAIM}),
    ),
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
        OntarioCaregiverAmount,
        frozenset({CAREGIVER_DEPENDANTS, ontario.ELIGIBLE_DEPENDANT_AMOUNT}),
        frozenset({ontario.CAREGIVER_AMOUNT}),
    ),
}
