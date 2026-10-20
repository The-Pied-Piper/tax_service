"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.choose_by_count import ChooseByCount
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.tiered_surcharge import TieredSurcharge
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.catalog import (
    ADJUSTED_FAMILY_NET_INCOME,
    CANADA_WORKERS_BENEFIT,
    CANADA_WORKERS_BENEFIT_WITH_DEPENDANT,
    CANADA_WORKERS_BENEFIT_WITHOUT_DEPENDANT,
    CWB_BEFORE_REDUCTION_WITH_DEPENDANT,
    CWB_BEFORE_REDUCTION_WITHOUT_DEPENDANT,
    CWB_ELIGIBLE_DEPENDANTS,
    CWB_REDUCTION_WITH_DEPENDANT,
    CWB_REDUCTION_WITHOUT_DEPENDANT,
    EMPLOYMENT_INCOME,
    NET_INCOME,
    WORKING_INCOME,
)

INPUTS = frozenset(
    {
        "ca/cwb_eligible_dependants",
    }
)

OUTPUTS = frozenset[str]()

STEPS = {
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
}

WIRING = {
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
}
