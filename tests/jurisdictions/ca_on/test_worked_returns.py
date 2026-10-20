"""Every worked return in `returns/`, computed end to end and checked line by line.

One test runs per `*.yaml` file in `returns/` (the pytest id is the file stem): the file's inputs
go through the service the composition root builds, and each expected line must equal the
worksheet's artifact exactly. A file must list every output its manifest declares. Adding a
return is adding a file.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest

from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.domain.artifact import ArtifactRegistry
from app.jurisdictions.ca.catalog import (
    DEPENDANT_CARE_EXPENSES,
    DEPENDANT_CREDIT_AMOUNTS,
    DEPENDANT_NET_INCOME,
    DEPENDANT_TAXABLE_INCOME,
    DEPENDANT_UNDER_18,
    OTHER_DEPENDANT_MEDICAL_EXPENSES,
)
from app.jurisdictions.ca_on.catalog import CLAIMED_AS_ELIGIBLE_DEPENDANT
from app.main import build_tax_computation
from app.registrations import JURISDICTIONS
from tests.jurisdictions.ca_on.worked_return import WorkedReturn, WorkedReturnError

RETURNS = Path(__file__).parent / "returns"


def check(path: Path) -> None:
    """Load the worked return at `path`, compute it and assert every expected line."""
    service = build_tax_computation()  # registers the catalogs the loader resolves through
    worked = WorkedReturn.load(path, ArtifactRegistry.shared())
    manifest = (
        YamlJurisdictionSource(JURISDICTIONS.roots())
        .get_jurisdiction(worked.jurisdiction)
        .manifest_for(worked.tax_year)
    )
    worked.require_outputs(manifest.outputs)

    worksheet = service.compute(worked.jurisdiction, worked.tax_year, *worked.inputs)

    for expected in worked.expected:
        assert worksheet.get(expected.kind) == expected, f"{path.name}: {expected.kind.identifier}"


@pytest.mark.parametrize("path", WorkedReturn.discover(RETURNS), ids=lambda path: path.stem)
def test_worked_return(path: Path) -> None:
    check(path)


# A made-up low-income return for the tests of the mechanism itself; the real returns are
# only ever read from `returns/`, so nothing here names one of them.
LOW_INCOME = """\
jurisdiction: CA-ON
tax_year: 2025
description: >-
  Employment income of 10000, no capital gain, no unused or new RRSP contributions, no union
  dues and no deductions from net income. The CPP contributions are computed from employment
  income by Schedule 8's tiers: base contributions 4.95% x (10000 - 3500) = 321.75, first
  additional 1% x 6500 = 65.00, no second additional below the 71300 ceiling, so enhanced
  contributions of 65.00. The EI premiums are computed from employment income: 1.64% x 10000
  = 164.00. The contributions available to deduct (Schedule 7 line 10) are the unused
  contributions (line 1) of 0 plus the contributions (line 4) of 0: 0. The most that may be
  deducted (line 17) is the lesser of them and the deduction limit (line 11) of 1800, a
  chosen limit: 0. The amount deducted (line 18) is that 0, so the RRSP deduction (line 20)
  is 0, the unused contributions carried forward (line 23) are 0 - 0 = 0. With no eligible
  child and no child care expenses paid, the child care expenses deduction (T778 line 7) is
  the least of the basic limit 0 x 8000 + 0 x 11000 + 0 x 5000 = 0, the 0 paid and
  two-thirds of the earned income of 10000, 6666.666..., rounded half-up to the cent:
  6666.67: 0. So the enhanced contributions are the only deduction from total income that
  is not zero.
  Net income and taxable income are 9935.00. The Canada employment amount is the
  lesser of 1471 and the employment income of 10000: 1471. The federal basic personal
  amount is computed from net income by the Federal Worksheet: 9935.00 is at or below
  its 177882 threshold, so it is the base amount 14538 plus the whole supplement
  amount 1591, 16129, rounded half-up to the cent. With no eligible dependant and
  no infirm child, the amount for an eligible dependant (16129 less a dependant's
  net income of 0 federally, 11905.00 less it at most 10823 for Ontario) is claimed
  for 0 eligible dependants and the amount for infirm children is 0 x 2687: each 0. Born
  in 1961 or later, the age amount (9028 less 15% of net income over 45522, nothing) is
  claimed for 0 filers born in 1960 or earlier: 0. With a spouse's net income of 0 and no
  spouse amount claimed, the spouse amount (16129 less 0) and the Canada caregiver amount
  for the spouse (28798 less 0, at most 8601, less the spouse amount) are each claimed
  for 0: 0.
  The federal total of credit amounts is its basic personal amount plus those two zeros,
  321.75, 164.00 and 1471; the Ontario total is its basic personal amount plus its zero,
  321.75 and 164.00 (ON428 has no Canada employment amount). Each form's non-refundable tax
  credits are its total times its rate (14.5% of 18085.75 = 2622.43375, rounded half-up to
  the cent: 2622.43; 5.05% of 13232.75 = 668.253875, rounded half-up to the cent: 668.25);
  each exceeds its tax (14.5% of 9935.00 = 1440.575, rounded half-up to the cent: 1440.58;
  5.05% of it = 501.7175, rounded half-up to the cent: 501.72), leaving zero. An Ontario tax
  of zero is below the first surtax threshold, so the surtax is zero and the Ontario tax
  with surtax is zero. With no dependent children and no dependants, the Ontario tax
  reduction amounts are the basic reduction of 294.00, and the reduction is twice them less
  the tax of zero: 588.00, which leaves an Ontario tax after the reduction of zero, not a
  refund. The LIFT credit (Schedule ON428-A) is 5.05% of the employment income,
  505, below its 875 maximum, less 5% of net income over 32500, nothing as 9935.00 is below
  it: 505, more than the Ontario tax after the reduction of zero, so the Ontario tax after
  the LIFT credit is zero. With chosen qualifying donations of 0, the community food program
  donation tax credit for farmers (line 87) is 25% x 0 = 0 and the Ontario tax after it (line
  88) is 0 less 0, zero. A taxable income of 9935.00 is at or below the health premium chart's
  first threshold of 20000, so the premium is zero and the Ontario tax is zero. The net
  federal tax is the federal tax after credits, zero, and the total payable is it plus the
  Ontario tax, zero. The Canada workers benefit (Schedule 6) with no eligible spouse or
  dependant is 27% of the working income, the employment income of 10000, over 3000: 1890,
  at most 1633, less 15% of the adjusted family net income, the net income, over 26855,
  nothing as 9935.00 is below it: 1633; with one it would be 1890, at most 2813, less
  nothing over 30639: 1890. With 0 Schedule 6 eligible dependants the first applies: 1633.
  With no fertility treatment expenses, no seniors' transit amount paid, no political
  contributions (federal or Ontario), no Form T1221 slips and no co-operative education work
  placements (a chosen payroll of 0), the Ontario credits (ON479 lines 1, 14, 16, 17, 18, 20
  and 21) and the provincial credits (T1 line 47900) are 0, as is the federal political
  contribution tax credit (T1 line 41000).
  The income tax deducted is a chosen 500, so the total credits are 500 plus the benefit
  plus the provincial credits, 2133, and the refund or balance owing is 0 less 2133: -2133,
  a refund. Every amount computed from a rate, fraction, amount or chart on the forms is
  rounded half-up to the cent, each line being a dollars-and-cents box; here that changes
  Form T778 line 6, the federal and Ontario tax on taxable income and both forms'
  non-refundable tax credits. The lines that only add, subtract, compare or choose take
  amounts already in cents, so the refund or balance owing is in cents too.
sources:
  - >-
    T1, Federal Worksheet, Schedule 3, Schedule 5, Schedule 6, Schedule 7, Schedule 8, ON428,
    Schedule ON428-A, T778 and EI table arithmetic on the 2025 figures.
inputs:
  ca/employment_income: "10000"
  ca/capital_gain: "0"
  ca/other_employment_income: "0"
  ca/old_age_security: "0"
  ca/cpp_or_qpp_benefits: "0"
  ca/other_pensions_and_superannuation: "0"
  ca/elected_split_pension_amount: "0"
  ca/universal_child_care_benefit: "0"
  ca/ei_and_other_benefits: "0"
  ca/t3_taxable_dividends_other_than_eligible: "0"
  ca/t4ps_taxable_dividends_other_than_eligible: "0"
  ca/t5_taxable_dividends_other_than_eligible: "0"
  ca/t5013_taxable_dividends_other_than_eligible: "0"
  ca/t3_taxable_dividends: "0"
  ca/t4ps_taxable_dividends: "0"
  ca/t5_taxable_dividends: "0"
  ca/t5013_taxable_dividends: "0"
  ca/eligible_dividends_received_without_a_slip: "0"
  ca/other_dividends_received_without_a_slip: "0"
  ca/t3_dividend_tax_credit: "0"
  ca/t4ps_dividend_tax_credit: "0"
  ca/t5_dividend_tax_credit: "0"
  ca/t5013_dividend_tax_credit: "0"
  ca/t3_investment_income: "0"
  ca/t5_investment_income: "0"
  ca/t5013_investment_income: "0"
  ca/investment_income_credited_not_received: "0"
  ca/tax_refund_interest: "0"
  ca/foreign_investment_income: "0"
  ca/investment_income_without_a_slip: "0"
  ca/investment_royalties: "0"
  ca/investment_income_reported_in_previous_years: "0"
  ca/net_partnership_income: "0"
  ca/rdsp_income: "0"
  ca/taxable_support_payments: "0"
  ca/rrsp_income: "0"
  ca/fhsa_income: "0"
  ca/other_fhsa_income: "0"
  ca/other_income: "0"
  ca/taxable_scholarships: "0"
  ca/workers_compensation_benefits: "0"
  ca/social_assistance_payments: "0"
  ca/net_federal_supplements: "0"
  ca/uccb_repayment: "0"
  ca/rdsp_income_repayment: "0"
  ca/canadian_armed_forces_and_police_deduction: "0"
  ca/security_options_deductions: "0"
  ca/limited_partnership_losses_of_other_years: "0"
  ca/non_capital_losses_of_other_years: "0"
  ca/additional_deductions: "0"
  ca/other_payments_deduction_above_limit: "0"
  ca/other_payments_worksheet_required: "0"
  ca/other_payments_worksheet_line_9_over_limit: "0"
  ca/unused_rrsp_contributions: "0"
  ca/rrsp_contributions: "0"
  ca/rrsp_deduction_limit: "1800"
  ca/rrsp_amount_deducted: "0"
  ca/union_dues: "0"
  ca/rpp_deduction: "0"
  ca/elected_split_pension_deduction: "0"
  ca/support_payments_deduction: "0"
  ca/exploration_and_development_expenses: "0"
  ca/other_deductions: "0"
  ca/total_carrying_charges: "0"
  ca/total_interest_expenses: "0"
  ca/total_other_expenses: "0"
  ca/capital_gains_deductions_1985_to_1987: "0"
  ca/capital_gains_deductions_1988_and_1989_other_than_eligible_capital_property: "0"
  ca/capital_gains_deductions_1988_and_1989_eligible_capital_property: "0"
  ca/capital_gains_deductions_1990_to_1999: "0"
  ca/capital_gains_deductions_2000: "0"
  ca/capital_gains_deductions_2001_to_2024: "0"
  ca/other_business_investment_loss_reductions_1986_to_1994: "0"
  ca/other_business_investment_loss_reductions_1994_to_1996: "0"
  ca/other_business_investment_loss_reductions_1997_to_1999: "0"
  ca/other_business_investment_loss_reductions_2000: "0"
  ca/other_business_investment_loss_reductions_2001_to_2023: "0"
  ca/other_business_investment_loss_reductions_2024: "0"
  ca/business_investment_loss: "0"
  ca/fhsa_contributions_in_2025: "0"
  ca/fhsa_contributions_in_2025_after_first_qualifying_withdrawal: "0"
  ca/fhsa_variable_b_amount: "0"
  ca/fhsa_designated_withdrawals_in_2025: "0"
  ca/fhsa_contributions_in_2024: "0"
  ca/fhsa_contributions_in_2024_before_first_qualifying_withdrawal: "0"
  ca/fhsa_carryforward_for_2025: "0"
  ca/fhsa_rrsp_transfers_in_2024_and_prior_years: "0"
  ca/fhsa_rrsp_transfers_in_2025: "0"
  ca/fhsa_designated_transfers_in_2024_and_prior_years: "0"
  ca/fhsa_designated_transfers_in_2025: "0"
  ca/fhsa_variable_h_amount: "0"
  ca/fhsa_carryforward_for_2024: "0"
  ca/fhsa_variable_f_amount: "0"
  ca/fhsa_annual_limits_for_2024_and_prior_years: "0"
  ca/fhsa_deductions_for_2024_and_prior_years: "0"
  ca/fhsa_unused_contributions_brought_forward: "0"
  ca/fhsa_contributions_deducted: "0"
  ca/fhsa_maximum_participation_period_ended: "0"
  ca-on/dependent_children: "0"
  ca-on/dependants: "0"
  ca/eligible_dependants: "0"
  ca/dependant_net_income: "0"
  ca/infirm_dependants: []
  ca/medical_expenses: "0"
  ca/other_dependants: []
  ca-on/caregiver_dependants: []
  ca/disability_dependants: []
  ca/infirm_children: "0"
  ca/born_in_1960_or_earlier: "0"
  ca/spouse_net_income: "0"
  ca/spouses_claimed: "0"
  ca/spouse_caregiver_eligible: "0"
  ca/child_care_expenses_paid: "0"
  ca/children_under_seven: "0"
  ca/children_with_disability: "0"
  ca/children_seven_to_sixteen: "0"
  ca/cwb_eligible_dependants: "0"
  ca/income_tax_deducted: "500"
  ca/part_xii_2_tax_credit: "0"
  ca/employee_and_partner_gst_hst_rebate: "0"
  ca/educator_supplies_expenses: "0"
  ca/journalism_labour_tax_credit: "0"
  ca/tax_paid_by_instalments: "0"
  ca/itc_recapture_expenditure_at_15_percent: "0"
  ca/itc_recapture_expenditure_at_20_percent: "0"
  ca/labour_sponsored_funds_net_cost: "0"
  ca/advanced_canada_workers_benefit: "0"
  ca/resp_aips_received_part_a: "0"
  ca/resp_aips_rrsp_contributions: "0"
  ca/resp_aips_reduction_used_in_previous_years: "0"
  ca/resp_aips_received_part_b: "0"
  ca/resp_aips_part_a_applies: "0"
  ca/rl_10_labour_sponsored_fund_amount: "0"
  ca-on/opportunities_fund_donation: "0"
  ca-on/fertility_expenses: "0"
  ca-on/seniors_transit_paid: "0"
  ca-on/flow_through_share_slips: []
  ca-on/coop_education_payroll: "0"
  ca-on/coop_education_placements: []
  ca-on/community_food_program_donations: "0"
  ca/charitable_donations: "0"
  ca/government_donations: "0"
  ca/university_donations_outside_canada: "0"
  ca/foreign_charity_donations: "0"
  ca/ecological_and_cultural_gifts: "0"
  ca/ecological_gifts_before_2016: "0"
  ca/depreciable_gift_recaptured_depreciation: "0"
  ca/depreciable_gift_net_proceeds: "0"
  ca/depreciable_gift_capital_cost: "0"
  ca/capital_gift_taxable_gains: "0"
  ca/capital_gift_gains_deduction: "0"
  ca-on/political_contributions: "0"
  ca/political_contributions: "0"
expected:
  ca/taxable_capital_gains: "0"
  ca/taxable_dividends_other_than_eligible: "0"
  ca/investment_income_before_prior_years: "0"
  ca/interest_and_other_investment_income: "0"
  ca/income_support_benefits: "0"
  ca/total_income: "10000"
  ca/cpp_base_contributions: "321.75"
  ca/cpp_first_additional_contributions: "65.00"
  ca/cpp_second_additional_contributions: "0"
  ca/cpp_enhanced_contributions: "65.00"
  ca/ei_premiums: "164.00"
  ca/rrsp_contributions_available: "0"
  ca/rrsp_deduction_maximum: "0"
  ca/rrsp_deduction: "0"
  ca/unused_rrsp_contributions_carried_forward: "0"
  ca/child_care_limit_for_children_under_seven: "0"
  ca/child_care_limit_for_children_with_disability: "0"
  ca/child_care_limit_for_children_seven_to_sixteen: "0"
  ca/child_care_basic_limit: "0"
  ca/child_care_earned_income: "10000"
  ca/child_care_earned_income_limit: "6666.67"
  ca/child_care_expenses: "0"
  ca/deductions_from_total_income: "65.00"
  ca/net_income: "9935.00"
  ca/net_income_before_adjustments: "9935.00"
  ca/fhsa_unused_contributions_carried_forward: "0"
  ca/other_payments_limit_income: "9935.00"
  ca/deductions_from_net_income: "0"
  ca/taxable_income: "9935.00"
  ca/federal_basic_tax: "1440.58"
  ca/basic_personal_amount: "16129"
  ca/age_maximum: "9028.00"
  ca/age_income_threshold: "45522.00"
  ca/age_income_over_threshold: "0"
  ca/age_reduction: "0"
  ca/age_amount_before_count: "9028.00"
  ca/age_amount: "0"
  ca/spouse_infirmity_supplement: "0"
  ca/spouse_amount_basis: "16129"
  ca/spouse_amount_before_count: "16129"
  ca/spouse_amount: "0"
  ca/eligible_dependant_amount_before_count: "16129"
  ca/eligible_dependant_amount: "0"
  ca/spouse_caregiver_base: "28798.00"
  ca/spouse_caregiver_before_maximum: "28798.00"
  ca/spouse_caregiver_limit: "8601.00"
  ca/spouse_caregiver_amount_before_count: "8601.00"
  ca/spouse_caregiver_amount: "0"
  ca/infirm_children_amount: "0"
  ca/canada_employment_amount: "1471"
  ca/non_refundable_credit_amounts: "18085.75"
  ca/non_refundable_tax_credits: "2622.43"
  ca/federal_tax_after_credits: "0"
  ca-on/ontario_basic_tax: "501.72"
  ca-on/basic_personal_amount: "12747"
  ca-on/eligible_dependant_base: "11905.00"
  ca-on/eligible_dependant_amount_before_maximum: "11905.00"
  ca-on/eligible_dependant_amount_before_count: "10823"
  ca-on/eligible_dependant_amount: "0"
  ca-on/non_refundable_credit_amounts: "13232.75"
  ca-on/non_refundable_tax_credits: "668.25"
  ca-on/ontario_tax_after_credits: "0"
  ca-on/ontario_surtax: "0"
  ca-on/ontario_tax_with_surtax: "0"
  ca-on/dividends_amount_a: "0"
  ca-on/dividends_amount_b: "0"
  ca-on/other_dividends_credit: "0"
  ca-on/dividends_amount_a_less_b: "0"
  ca-on/eligible_dividends_credit: "0"
  ca-on/dividend_tax_credit: "0"
  ca-on/ontario_tax_before_dividend_credit: "0"
  ca-on/ontario_tax_less_dividend_credit: "0"
  ca-on/dividend_credit_from_line_57: "0"
  ca-on/ontario_tax_after_dividend_credit: "0"
  ca-on/tax_reduction_basic: "294.00"
  ca-on/tax_reduction_for_children: "0"
  ca-on/tax_reduction_for_dependants: "0"
  ca-on/tax_reduction_amounts: "294.00"
  ca-on/ontario_tax_reduction: "588.00"
  ca-on/ontario_tax_after_reduction: "0"
  ca-on/lift_credit_before_maximum: "505"
  ca-on/lift_maximum_credit: "505"
  ca-on/lift_reduction: "0"
  ca-on/lift_credit: "505"
  ca-on/ontario_tax_after_lift_credit: "0"
  ca-on/community_food_program_credit: "0"
  ca-on/ontario_tax_after_food_credit: "0"
  ca-on/ontario_health_premium: "0"
  ca-on/ontario_tax: "0"
  ca/itc_recapture_at_15_percent: "0"
  ca/itc_recapture_at_20_percent: "0"
  ca/itc_recapture: "0"
  ca/federal_tax_with_itc_recapture: "0"
  ca/political_credit_before_maximum: "0"
  ca/political_credit: "0"
  ca/labour_sponsored_funds_credit_before_maximum: "0"
  ca/labour_sponsored_funds_credit: "0"
  ca/credits_against_federal_tax: "0"
  ca/federal_tax_less_credits: "0"
  ca/resp_aips_contributions_counted: "0"
  ca/resp_aips_lifetime_limit: "50000"
  ca/resp_aips_limit_remaining: "50000"
  ca/resp_aips_reduction: "0"
  ca/resp_aips_subject_to_tax: "0"
  ca/resp_aips_part_a_tax: "0"
  ca/resp_aips_part_b_tax: "0"
  ca/resp_aips_additional_tax: "0"
  ca/special_taxes: "0"
  ca/net_federal_tax: "0"
  ca/total_payable: "0"
  ca/working_income: "10000"
  ca/adjusted_family_net_income: "9935.00"
  ca/cwb_before_reduction_without_dependant: "1633"
  ca/cwb_reduction_without_dependant: "0"
  ca/canada_workers_benefit_without_dependant: "1633"
  ca/cwb_before_reduction_with_dependant: "1890.00"
  ca/cwb_reduction_with_dependant: "0"
  ca/canada_workers_benefit_with_dependant: "1890.00"
  ca/canada_workers_benefit: "1633"
  ca-on/fertility_credit_before_maximum: "0"
  ca-on/fertility_credit: "0"
  ca-on/seniors_transit_amount_paid_at_most_maximum: "0"
  ca-on/seniors_transit_credit: "0"
  ca-on/political_credit_before_maximum: "0"
  ca-on/political_credit: "0"
  ca-on/flow_through_share_expenses: "0"
  ca-on/flow_through_share_credit: "0"
  ca-on/ontario_credits_subtotal: "0"
  ca-on/coop_education_payroll_threshold: "400000.00"
  ca-on/coop_education_payroll_over_threshold: "0"
  ca-on/coop_education_payroll_range: "200000.00"
  ca-on/coop_education_phase_out_share: "0"
  ca-on/coop_education_full_share: "1.00"
  ca-on/coop_education_remaining_share: "1.00"
  ca-on/coop_education_placement_count: "0"
  ca-on/coop_education_credit: "0"
  ca-on/ontario_credits: "0"
  ca/provincial_credits: "0"
  ca/total_credits: "2133"
  ca/refund_or_balance_owing: "-2133"
  ca/educator_supplies_expenses_at_most_maximum: "0"
  ca/educator_school_supply_credit: "0"
  ca/refund: "2133"
  ca-on/refund_before_donation: "2133"
  ca-on/net_refund: "2133"
"""


def test_the_returns_directory_holds_at_least_one_return() -> None:
    assert WorkedReturn.discover(RETURNS)


def test_return_q_claims_two_infirm_dependants_on_line_30450() -> None:
    path = RETURNS / "2025_return_q.yaml"
    build_tax_computation()  # registers the catalogs the loader resolves through
    worked = WorkedReturn.load(path, ArtifactRegistry.shared())

    (dependants,) = [a for a in worked.inputs if a.kind.identifier == "ca/infirm_dependants"]
    assert [record[DEPENDANT_NET_INCOME] for record in dependants.value.records] == [
        Decimal("5000"),
        Decimal("25000"),
    ]
    (caregiver,) = [a for a in worked.expected if a.kind.identifier == "ca/caregiver_amount"]
    assert caregiver.value == Decimal("12399.00")
    check(path)


def test_return_w_claims_two_ontario_caregiver_dependants_on_line_58185() -> None:
    path = RETURNS / "2025_return_w.yaml"
    build_tax_computation()  # registers the catalogs the loader resolves through
    worked = WorkedReturn.load(path, ArtifactRegistry.shared())

    (dependants,) = [a for a in worked.inputs if a.kind.identifier == "ca-on/caregiver_dependants"]
    assert [
        (record[DEPENDANT_NET_INCOME], record[CLAIMED_AS_ELIGIBLE_DEPENDANT])
        for record in dependants.value.records
    ] == [(Decimal("5000"), 0), (Decimal("25000"), 0)]
    (caregiver,) = [a for a in worked.expected if a.kind.identifier == "ca-on/caregiver_amount"]
    assert caregiver.value == Decimal("7570.00")
    check(path)


def test_return_x_claims_one_dependant_with_a_disability_on_line_31800() -> None:
    path = RETURNS / "2025_return_ab.yaml"
    build_tax_computation()  # registers the catalogs the loader resolves through
    worked = WorkedReturn.load(path, ArtifactRegistry.shared())

    (dependants,) = [a for a in worked.inputs if a.kind.identifier == "ca/disability_dependants"]
    (dependant,) = dependants.value.records
    assert dependant[DEPENDANT_UNDER_18] == 0
    assert dependant[DEPENDANT_CARE_EXPENSES] == Decimal("0")
    assert dependant[DEPENDANT_CREDIT_AMOUNTS] == Decimal("16129")
    assert dependant[DEPENDANT_TAXABLE_INCOME] == Decimal("20000")
    (transferred,) = [
        a for a in worked.expected if a.kind.identifier == "ca/disability_transferred_amount"
    ]
    assert transferred.value == Decimal("6267.00")
    check(path)


def test_return_ae_claims_the_federal_political_contribution_credit_on_line_41000() -> None:
    path = RETURNS / "2025_return_ae.yaml"
    build_tax_computation()  # registers the catalogs the loader resolves through
    worked = WorkedReturn.load(path, ArtifactRegistry.shared())

    (contributions,) = [
        a for a in worked.inputs if a.kind.identifier == "ca/political_contributions"
    ]
    assert contributions.value == Decimal("1000")
    (credit,) = [a for a in worked.expected if a.kind.identifier == "ca/political_credit"]
    assert credit.value == Decimal("558.33")
    check(path)


def test_return_x_claims_two_other_dependants_medical_expenses_on_line_33199() -> None:
    path = RETURNS / "2025_return_x.yaml"
    build_tax_computation()  # registers the catalogs the loader resolves through
    worked = WorkedReturn.load(path, ArtifactRegistry.shared())

    (dependants,) = [a for a in worked.inputs if a.kind.identifier == "ca/other_dependants"]
    assert [
        (record[OTHER_DEPENDANT_MEDICAL_EXPENSES], record[DEPENDANT_NET_INCOME])
        for record in dependants.value.records
    ] == [(Decimal("3000"), Decimal("10000")), (Decimal("1000"), Decimal("40000"))]
    (own,) = [a for a in worked.inputs if a.kind.identifier == "ca/medical_expenses"]
    assert own.value == Decimal("4500")
    (other,) = [a for a in worked.expected if a.kind.identifier == "ca/other_dependants_medical"]
    assert other.value == Decimal("2700.00")
    (claim,) = [a for a in worked.expected if a.kind.identifier == "ca/medical_claim"]
    assert claim.value == Decimal("5773.35")
    # ON428 line 42 (line 58729) and line 43 (line 58769), over the same list and expenses.
    (ontario_other,) = [
        a for a in worked.expected if a.kind.identifier == "ca-on/other_dependants_medical"
    ]
    assert ontario_other.value == Decimal("2700.00")
    (ontario_claim,) = [a for a in worked.expected if a.kind.identifier == "ca-on/medical_claim"]
    assert ontario_claim.value == Decimal("5773.35")
    (ontario_amounts,) = [
        a for a in worked.expected if a.kind.identifier == "ca-on/non_refundable_credit_amounts"
    ]
    assert ontario_amounts.value == Decimal("21510.30")
    (refund,) = [a for a in worked.expected if a.kind.identifier == "ca/refund_or_balance_owing"]
    assert refund.value == Decimal("-334.19")
    check(path)


def test_a_new_file_is_a_new_worked_return_without_a_test_change(tmp_path: Path) -> None:
    (tmp_path / "2025_low_income.yaml").write_text(LOW_INCOME)
    (tmp_path / "2025_low_income_cents.yaml").write_text(
        LOW_INCOME.replace('"10000"', '"10000.00"')
    )

    found = WorkedReturn.discover(tmp_path)

    assert [path.stem for path in found] == ["2025_low_income", "2025_low_income_cents"]
    for path in found:
        check(path)


def test_a_wrong_expected_amount_fails_naming_the_file_and_line(tmp_path: Path) -> None:
    path = tmp_path / "wrong.yaml"
    path.write_text(LOW_INCOME.replace('"501.72"', '"501.73"'))

    with pytest.raises(AssertionError, match=r"wrong\.yaml: ca-on/ontario_basic_tax"):
        check(path)


def test_a_file_missing_a_declared_output_fails_naming_the_file_and_output(
    tmp_path: Path,
) -> None:
    path = tmp_path / "partial.yaml"
    path.write_text(LOW_INCOME.replace('  ca/refund_or_balance_owing: "-2133"\n', ""))

    with pytest.raises(WorkedReturnError, match=r"partial\.yaml.*ca/refund_or_balance_owing"):
        check(path)
