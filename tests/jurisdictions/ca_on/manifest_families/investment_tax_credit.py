"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.sum import Sum
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.apprenticeship_wages_total import ApprenticeshipWagesTotal
from app.jurisdictions.ca.catalog import (
    ITC_AGRICULTURAL_SRED_CONTRIBUTIONS,
    ITC_AGRICULTURAL_SRED_CREDIT,
    ITC_APPRENTICES,
    ITC_APPRENTICESHIP_CREDIT,
    ITC_APPRENTICESHIP_T3_BOX_40,
    ITC_APPRENTICESHIP_WAGES_TOTAL,
    ITC_APPRENTICESHIP_WAGES_WITH_T3,
    ITC_CRITICAL_MINERAL_CREDIT,
    ITC_CRITICAL_MINERAL_EXPENDITURES,
    ITC_MINERAL_EXPLORATION_CREDIT,
    ITC_MINERAL_EXPLORATION_EXPENDITURES,
    ITC_NONREFUNDABLE_CREDITS,
    ITC_QUALIFIED_PROPERTY,
    ITC_QUALIFIED_PROPERTY_CREDIT,
    ITC_REFUNDABLE_CREDITS,
    ITC_SRED_CREDIT,
    ITC_SRED_EXPENDITURES,
    ITC_SRED_PARTNERSHIP_ALLOCATION,
    ITC_SRED_REPAYMENT_2014_AND_PRIOR,
    ITC_SRED_REPAYMENT_2015_AND_AFTER,
    ITC_SRED_REPAYMENT_CREDIT,
    ITC_SRED_REPAYMENT_CREDIT_2014_AND_PRIOR,
    ITC_SRED_REPAYMENT_CREDIT_2015_AND_AFTER,
)

# The caller's lines of Form T2038(IND) Parts A and B, as the form takes them (manifest part
# 01b_investment_tax_credit.yaml): Part A lines 67120, 67130, 67135 and 67140, Part B lines 67170
# and 67175, the apprentices of Table 1, the T3 box 40 amount on line 67180, and lines 67184 and
# 67185.
INPUTS = frozenset(
    {
        "ca/itc_sred_expenditures",
        "ca/itc_agricultural_sred_contributions",
        "ca/itc_sred_partnership_allocation",
        "ca/itc_qualified_property",
        "ca/itc_mineral_exploration_expenditures",
        "ca/itc_critical_mineral_expenditures",
        "ca/itc_apprentices",
        "ca/itc_apprenticeship_t3_box_40",
        "ca/itc_sred_repayment_2014_and_prior",
        "ca/itc_sred_repayment_2015_and_after",
    }
)

# Form T2038(IND) Part A "Total current-year refundable credits (add amounts 1 to 4)" and Part B
# "Total current-year non-refundable tax credits (add amounts B, C, D and E)", which Part D of the
# form reads ("Enter amount A at amount 2 in Part D" and "Enter amount F at amount 3 in Part D").
OUTPUTS = frozenset({"ca/itc_refundable_credits", "ca/itc_nonrefundable_credits"})

STEPS = {
    # Form T2038(IND) Part A line 1, "ITC for qualified expenditures for SR&ED (amount from line 559
    # of Form T661 plus applicable amount from box 40* of your T3 slip, minus amounts from lines
    # 67130 and 67135)" "× 0.15 =" amount 1: the caller's line 67120 at the rate of its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/itc_part_a_line_1_rate"},
        consumes={"base": "ca/itc_sred_expenditures"},
        produces={"output": "ca/itc_sred_credit"},
    ),
    # Form T2038(IND) Part A line 2, "80% of total contributions made to agricultural organizations
    # for SR&ED" "× 0.15 =" amount 2: the caller's line 67130 at the rate of its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/itc_part_a_line_2_rate"},
        consumes={"base": "ca/itc_agricultural_sred_contributions"},
        produces={"output": "ca/itc_agricultural_sred_credit"},
    ),
    # Form T2038(IND) Part A line 4, "ITC for total investments in qualified property (include
    # applicable amount from box 40* of your T3 slip)" "× 0.10 =" amount 4: the caller's line 67140
    # at the rate of its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/itc_part_a_line_4_rate"},
        consumes={"base": "ca/itc_qualified_property"},
        produces={"output": "ca/itc_qualified_property_credit"},
    ),
    # Form T2038(IND) Part A "Total current-year refundable credits (add amounts 1 to 4)", amount A:
    # amounts 1, 2, 3 and 4 in line order, amount 3 being the caller's line 67135 "ITC allocated
    # from a partnership for SR&ED", read as it is.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/itc_sred_credit",
                "ca/itc_agricultural_sred_credit",
                "ca/itc_sred_partnership_allocation",
                "ca/itc_qualified_property_credit",
            )
        },
        produces={"output": "ca/itc_refundable_credits"},
    ),
    # Form T2038(IND) Part B line 67170, "Mineral exploration tax credit (METC)" "× 0.15 =" amount
    # B: the caller's flow-through mining expenditures at the rate of its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/itc_part_b_amount_b_rate"},
        consumes={"base": "ca/itc_mineral_exploration_expenditures"},
        produces={"output": "ca/itc_mineral_exploration_credit"},
    ),
    # Form T2038(IND) Part B line 67175, "Critical mineral exploration tax credit (CMETC)"
    # "× 0.30 =" amount C: the caller's flow-through critical mineral expenditures at the rate of
    # its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/itc_part_b_amount_c_rate"},
        consumes={"base": "ca/itc_critical_mineral_expenditures"},
        produces={"output": "ca/itc_critical_mineral_credit"},
    ),
    # Form T2038(IND) Part B Table 1, column 3, "The lesser of eligible salary and wages** payable
    # in the year or $20,000.": the total over the apprentices, each one's lesser taken with the
    # maximum dataset's amount.
    CapabilitySelection(
        name="ca/apprenticeship_wages_total",
        params={"maximum": "ca/itc_apprentice_wages_maximum"},
        consumes={"apprentices": "ca/itc_apprentices"},
        produces={"output": "ca/itc_apprenticeship_wages_total"},
    ),
    # Form T2038(IND) Part B line 67180, "Total apprenticeship job creation tax credit (Total of
    # amounts in column 3 plus applicable amount from box 40* of your T3 slip)": the total of
    # column 3 plus the caller's T3 box 40 amount.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/itc_apprenticeship_wages_total",
                "ca/itc_apprenticeship_t3_box_40",
            )
        },
        produces={"output": "ca/itc_apprenticeship_wages_with_t3"},
    ),
    # Form T2038(IND) Part B line 67180 "× 0.10 =" amount D, "The credit is 10% of the total of the
    # amounts in Table 1, column 3.": the total of line 67180 at the rate of its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/itc_part_b_amount_d_rate"},
        consumes={"base": "ca/itc_apprenticeship_wages_with_t3"},
        produces={"output": "ca/itc_apprenticeship_credit"},
    ),
    # Form T2038(IND) Part B, "Repayment of assistance that reduced qualified SR&ED expenditures
    # incurred in 2014 and prior years (amount from line 560 of Form T661)" 67184 "× 0.20 =" amount
    # 1: the caller's line 67184 at the rate of its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/itc_part_b_repayment_line_1_rate"},
        consumes={"base": "ca/itc_sred_repayment_2014_and_prior"},
        produces={"output": "ca/itc_sred_repayment_credit_2014_and_prior"},
    ),
    # Form T2038(IND) Part B, "Repayment of assistance that reduced qualified SR&ED expenditures
    # incurred in 2015 and subsequent years (amount from line 560 of Form T661)" 67185 "× 0.15 ="
    # amount 2: the caller's line 67185 at the rate of its dataset.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/itc_part_b_repayment_line_2_rate"},
        consumes={"base": "ca/itc_sred_repayment_2015_and_after"},
        produces={"output": "ca/itc_sred_repayment_credit_2015_and_after"},
    ),
    # Form T2038(IND) Part B "Total repayment of assistance for SR&ED (add amounts 1 and 2)", amount
    # E: amounts 1 and 2 in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/itc_sred_repayment_credit_2014_and_prior",
                "ca/itc_sred_repayment_credit_2015_and_after",
            )
        },
        produces={"output": "ca/itc_sred_repayment_credit"},
    ),
    # Form T2038(IND) Part B "Total current-year non-refundable tax credits (add amounts B, C, D and
    # E)", amount F: amounts B, C, D and E in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/itc_mineral_exploration_credit",
                "ca/itc_critical_mineral_credit",
                "ca/itc_apprenticeship_credit",
                "ca/itc_sred_repayment_credit",
            )
        },
        produces={"output": "ca/itc_nonrefundable_credits"},
    ),
}

WIRING = {
    (
        ApplyRate,
        frozenset({ITC_SRED_EXPENDITURES}),
        frozenset({ITC_SRED_CREDIT}),
    ),
    (
        ApplyRate,
        frozenset({ITC_AGRICULTURAL_SRED_CONTRIBUTIONS}),
        frozenset({ITC_AGRICULTURAL_SRED_CREDIT}),
    ),
    (
        ApplyRate,
        frozenset({ITC_QUALIFIED_PROPERTY}),
        frozenset({ITC_QUALIFIED_PROPERTY_CREDIT}),
    ),
    (
        Sum,
        frozenset(
            {
                ITC_SRED_CREDIT,
                ITC_AGRICULTURAL_SRED_CREDIT,
                ITC_SRED_PARTNERSHIP_ALLOCATION,
                ITC_QUALIFIED_PROPERTY_CREDIT,
            }
        ),
        frozenset({ITC_REFUNDABLE_CREDITS}),
    ),
    (
        ApplyRate,
        frozenset({ITC_MINERAL_EXPLORATION_EXPENDITURES}),
        frozenset({ITC_MINERAL_EXPLORATION_CREDIT}),
    ),
    (
        ApplyRate,
        frozenset({ITC_CRITICAL_MINERAL_EXPENDITURES}),
        frozenset({ITC_CRITICAL_MINERAL_CREDIT}),
    ),
    (
        ApprenticeshipWagesTotal,
        frozenset({ITC_APPRENTICES}),
        frozenset({ITC_APPRENTICESHIP_WAGES_TOTAL}),
    ),
    (
        Sum,
        frozenset({ITC_APPRENTICESHIP_WAGES_TOTAL, ITC_APPRENTICESHIP_T3_BOX_40}),
        frozenset({ITC_APPRENTICESHIP_WAGES_WITH_T3}),
    ),
    (
        ApplyRate,
        frozenset({ITC_APPRENTICESHIP_WAGES_WITH_T3}),
        frozenset({ITC_APPRENTICESHIP_CREDIT}),
    ),
    (
        ApplyRate,
        frozenset({ITC_SRED_REPAYMENT_2014_AND_PRIOR}),
        frozenset({ITC_SRED_REPAYMENT_CREDIT_2014_AND_PRIOR}),
    ),
    (
        ApplyRate,
        frozenset({ITC_SRED_REPAYMENT_2015_AND_AFTER}),
        frozenset({ITC_SRED_REPAYMENT_CREDIT_2015_AND_AFTER}),
    ),
    (
        Sum,
        frozenset(
            {ITC_SRED_REPAYMENT_CREDIT_2014_AND_PRIOR, ITC_SRED_REPAYMENT_CREDIT_2015_AND_AFTER}
        ),
        frozenset({ITC_SRED_REPAYMENT_CREDIT}),
    ),
    (
        Sum,
        frozenset(
            {
                ITC_MINERAL_EXPLORATION_CREDIT,
                ITC_CRITICAL_MINERAL_CREDIT,
                ITC_APPRENTICESHIP_CREDIT,
                ITC_SRED_REPAYMENT_CREDIT,
            }
        ),
        frozenset({ITC_NONREFUNDABLE_CREDITS}),
    ),
}
