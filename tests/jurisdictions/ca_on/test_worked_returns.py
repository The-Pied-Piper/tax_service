"""Every worked return in `returns/`, computed end to end and checked line by line.

One test runs per `*.yaml` file in `returns/` (the pytest id is the file stem): the file's inputs
go through the service the composition root builds, and each expected line must equal the
worksheet's artifact exactly. A file must list every output its manifest declares. Adding a
return is adding a file.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.domain.artifact import ArtifactRegistry
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
  is 0, the unused contributions carried forward (line 23) are 0 - 0 = 0, and the enhanced
  contributions are the only deduction from total income. Net income and taxable
  income are 9935.00. The Canada employment amount is the lesser of 1471 and the employment
  income of 10000: 1471. The federal basic personal amount is computed from net income by the
  Federal Worksheet: 9935.00 is at or below its 177882 threshold, so it is the base amount
  14538 plus the whole supplement amount 1591, 16129, rounded half-up to the cent. The federal
  total of credit amounts is its basic personal amount plus 321.75, 164.00 and 1471; the
  Ontario total is its basic personal amount plus 321.75 and 164.00 (ON428 has no Canada
  employment amount). Each form's non-refundable tax credits are its total times its rate
  (14.5% of 18085.75 = 2622.43375; 5.05% of 13232.75 = 668.253875); each exceeds its tax,
  leaving zero. An Ontario tax of zero is below the first surtax threshold, so the surtax is
  zero and the Ontario tax with surtax is zero. With no dependent children and no dependants,
  the Ontario tax reduction amounts are the basic reduction of 294.00, and the reduction is
  twice them less the tax of zero: 588.00, which leaves an Ontario tax after the reduction of
  zero, not a refund. A taxable income of 9935.00 is at or below the health premium chart's
  first threshold of 20000, so the premium is zero and the Ontario tax is zero. The net
  federal tax is the federal tax after credits, zero, and the total payable is it plus the
  Ontario tax, zero. The income tax deducted is a chosen 500, the only credit, so the refund
  or balance owing is 0 less 500: -500, a refund.
sources:
  - >-
    T1, Federal Worksheet, Schedule 3, Schedule 7, Schedule 8, ON428 and EI table arithmetic on
    the 2025 figures.
inputs:
  ca/employment_income: "10000"
  ca/capital_gain: "0"
  ca/unused_rrsp_contributions: "0"
  ca/rrsp_contributions: "0"
  ca/rrsp_deduction_limit: "1800"
  ca/rrsp_amount_deducted: "0"
  ca/union_dues: "0"
  ca-on/dependent_children: "0"
  ca-on/dependants: "0"
  ca/income_tax_deducted: "500"
expected:
  ca/taxable_capital_gains: "0"
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
  ca/deductions_from_total_income: "65.00"
  ca/net_income: "9935.00"
  ca/deductions_from_net_income: "0"
  ca/taxable_income: "9935.00"
  ca/federal_basic_tax: "1440.575"
  ca/basic_personal_amount: "16129"
  ca/canada_employment_amount: "1471"
  ca/non_refundable_credit_amounts: "18085.75"
  ca/non_refundable_tax_credits: "2622.43375"
  ca/federal_tax_after_credits: "0"
  ca-on/ontario_basic_tax: "501.7175"
  ca-on/basic_personal_amount: "12747"
  ca-on/non_refundable_credit_amounts: "13232.75"
  ca-on/non_refundable_tax_credits: "668.253875"
  ca-on/ontario_tax_after_credits: "0"
  ca-on/ontario_surtax: "0"
  ca-on/ontario_tax_with_surtax: "0"
  ca-on/tax_reduction_basic: "294.00"
  ca-on/tax_reduction_for_children: "0"
  ca-on/tax_reduction_for_dependants: "0"
  ca-on/tax_reduction_amounts: "294.00"
  ca-on/ontario_tax_reduction: "588.00"
  ca-on/ontario_tax_after_reduction: "0"
  ca-on/ontario_health_premium: "0"
  ca-on/ontario_tax: "0"
  ca/net_federal_tax: "0"
  ca/total_payable: "0"
  ca/total_credits: "500"
  ca/refund_or_balance_owing: "-500"
"""


def test_the_returns_directory_holds_at_least_one_return() -> None:
    assert WorkedReturn.discover(RETURNS)


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
    path.write_text(LOW_INCOME.replace('"501.7175"', '"501.7176"'))

    with pytest.raises(AssertionError, match=r"wrong\.yaml: ca-on/ontario_basic_tax"):
        check(path)


def test_a_file_missing_a_declared_output_fails_naming_the_file_and_output(
    tmp_path: Path,
) -> None:
    path = tmp_path / "partial.yaml"
    path.write_text(LOW_INCOME.replace('  ca/refund_or_balance_owing: "-500"\n', ""))

    with pytest.raises(WorkedReturnError, match=r"partial\.yaml.*ca/refund_or_balance_owing"):
        check(path)
