"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.capped_amount import CappedAmount
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.per_unit_amount import PerUnitAmount
from app.domain.capabilities.progressive_tax import ProgressiveTax
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.tapered_amount import TaperedAmount
from app.domain.capabilities.times_count import TimesCount
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.caregiver_amount import CaregiverAmount
from app.jurisdictions.ca.capabilities.disability_transfer_amount import DisabilityTransferAmount
from app.jurisdictions.ca.capabilities.other_dependants_medical import OtherDependantsMedical
from app.jurisdictions.ca.catalog import (
    AGE_AMOUNT,
    AGE_AMOUNT_BEFORE_COUNT,
    AGE_INCOME_OVER_THRESHOLD,
    AGE_INCOME_THRESHOLD,
    AGE_MAXIMUM,
    AGE_REDUCTION,
    BASIC_PERSONAL_AMOUNT,
    BORN_IN_1960_OR_EARLIER,
    CAREGIVER_AMOUNT,
    DEPENDANT_NET_INCOME,
    DISABILITY_DEPENDANTS,
    DISABILITY_TRANSFERRED_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT,
    ELIGIBLE_DEPENDANT_AMOUNT_BEFORE_COUNT,
    ELIGIBLE_DEPENDANTS,
    FEDERAL_BASIC_TAX,
    INFIRM_CHILDREN,
    INFIRM_CHILDREN_AMOUNT,
    INFIRM_DEPENDANTS,
    MEDICAL_CLAIM,
    MEDICAL_EXPENSES,
    MEDICAL_EXPENSES_OVER_THRESHOLD,
    MEDICAL_NET_INCOME_SHARE,
    MEDICAL_THRESHOLD,
    NET_INCOME,
    OTHER_DEPENDANTS,
    OTHER_DEPENDANTS_MEDICAL,
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
    TAXABLE_INCOME,
)

INPUTS = frozenset(
    {
        "ca/eligible_dependants",
        "ca/dependant_net_income",
        "ca/infirm_dependants",
        "ca/medical_expenses",
        "ca/other_dependants",
        "ca/disability_dependants",
        "ca/infirm_children",
        "ca/born_in_1960_or_earlier",
        "ca/spouse_net_income",
        "ca/spouses_claimed",
        "ca/spouse_caregiver_eligible",
    }
)

OUTPUTS = frozenset[str]()

STEPS = {
    CapabilitySelection(
        name="core/progressive_tax",
        params={"schedule": "ca/brackets"},
        consumes={"base": "ca/taxable_income"},
        produces={"output": "ca/federal_basic_tax"},
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
    # T1 line 100 (line 31800) "Disability amount transferred from a dependant (use Federal
    # Worksheet)", Federal Worksheet "Line 31800 - Disability amount transferred from a
    # dependant": for each dependant who is eligible for the disability tax credit, line 1
    # "Base amount 10,138.00", line 2 "Maximum supplement 5,914.00", line 4 "Threshold for
    # child care and attendant care expenses 3,464.00", line 8 "Line 1 plus line 7 (maximum
    # $16,052)", line 13 "Enter whichever is less: amount from line 8 or line 12. Allowable
    # amount for this dependant", and "the total of allowable amounts claimed for all
    # dependants who qualify for the disability tax credit".
    CapabilitySelection(
        name="ca/disability_transfer_amount",
        params={
            "base": "ca/disability_transfer_base_amount",
            "supplement": "ca/disability_transfer_supplement_maximum",
            "threshold": "ca/disability_transfer_care_threshold",
            "maximum": "ca/disability_transfer_maximum",
        },
        consumes={"dependants": "ca/disability_dependants"},
        produces={"output": "ca/disability_transferred_amount"},
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
    # T1 line 82 (line 30450) "Canada caregiver amount for other infirm dependants age 18 or
    # older (complete Schedule 5)", Schedule 5 "Line 30450 - Canada caregiver amount for other
    # infirm dependants age 18 or older": for each dependant, line 1 "Base amount 28,798.00"
    # less line 2 "Infirm dependant's net income from line 23600 of their return", line 3
    # "Line 1 minus line 2 (if negative, enter "0") (maximum $8,601)", and "the total of
    # allowable amounts claimed for all dependants".
    CapabilitySelection(
        name="ca/caregiver_amount",
        params={"base": "ca/caregiver_base_amount", "maximum": "ca/caregiver_maximum_amount"},
        consumes={"dependants": "ca/infirm_dependants"},
        produces={"output": "ca/caregiver_amount"},
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
    # T1 line 108 "Amount from line 23600" "multiplied by 3%": 3% of the net income.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/medical_net_income_rate"},
        consumes={"base": "ca/net_income"},
        produces={"output": "ca/medical_net_income_share"},
    ),
    # T1 line 109 "Enter whichever is less: $2,834 or the amount from line 108."
    CapabilitySelection(
        name="core/capped_amount",
        params={"cap": "ca/medical_threshold_ceiling"},
        consumes={"base": "ca/medical_net_income_share"},
        produces={"output": "ca/medical_threshold"},
    ),
    # T1 line 107 and line 33099 "Medical expenses for self, spouse or common-law partner and
    # your dependent children under 18 years of age", a caller input, and line 110 "Line 107
    # minus line 109 (if negative, enter "0")".
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={"amount": "ca/medical_expenses", "less": "ca/medical_threshold"},
        produces={"output": "ca/medical_expenses_over_threshold"},
    ),
    # T1 line 111 and line 33199 "Allowable amount of medical expenses for other dependants
    # (use Federal Worksheet)"; Federal Worksheet, line 33199, for each dependant: line 1
    # "Medical expenses for other dependant", line 2 "For provinces and territories other
    # than Quebec: amount from line 109 of the dependant's return.", line 3 "Line 1 minus
    # line 2 (if negative, enter "0")", and line 4 "Add the amounts from line 3 of columns 1,
    # 2, and 3 (and others, if any). Enter this amount on line 33199 of your return."
    CapabilitySelection(
        name="ca/other_dependants_medical",
        params={"reduction": "ca/other_dependants_medical_reduction"},
        consumes={"dependants": "ca/other_dependants"},
        produces={"output": "ca/other_dependants_medical"},
    ),
    # T1 line 112 and line 33200 "Line 110 plus line 111".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/medical_expenses_over_threshold", "ca/other_dependants_medical")},
        produces={"output": "ca/medical_claim"},
    ),
}

WIRING = {
    (ProgressiveTax, frozenset({TAXABLE_INCOME}), frozenset({FEDERAL_BASIC_TAX})),
    (TaperedAmount, frozenset({NET_INCOME}), frozenset({BASIC_PERSONAL_AMOUNT})),
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
    (CaregiverAmount, frozenset({INFIRM_DEPENDANTS}), frozenset({CAREGIVER_AMOUNT})),
    (ApplyRate, frozenset({NET_INCOME}), frozenset({MEDICAL_NET_INCOME_SHARE})),
    (CappedAmount, frozenset({MEDICAL_NET_INCOME_SHARE}), frozenset({MEDICAL_THRESHOLD})),
    (
        SubtractNotBelowZero,
        frozenset({MEDICAL_EXPENSES, MEDICAL_THRESHOLD}),
        frozenset({MEDICAL_EXPENSES_OVER_THRESHOLD}),
    ),
    (
        OtherDependantsMedical,
        frozenset({OTHER_DEPENDANTS}),
        frozenset({OTHER_DEPENDANTS_MEDICAL}),
    ),
    (
        Sum,
        frozenset({MEDICAL_EXPENSES_OVER_THRESHOLD, OTHER_DEPENDANTS_MEDICAL}),
        frozenset({MEDICAL_CLAIM}),
    ),
    (
        DisabilityTransferAmount,
        frozenset({DISABILITY_DEPENDANTS}),
        frozenset({DISABILITY_TRANSFERRED_AMOUNT}),
    ),
    (PerUnitAmount, frozenset({INFIRM_CHILDREN}), frozenset({INFIRM_CHILDREN_AMOUNT})),
}
