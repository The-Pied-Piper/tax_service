"""CA-ON 2025 end to end: return dm, T1 line 31400 when the filer elects to split pension income."""

from __future__ import annotations

from app.domain.artifact import Artifact
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    PENSION_INCOME_CREDIT,
    PENSION_SPLIT_AMOUNT,
    PENSION_SPLIT_ELECTION,
    PENSION_WORKSHEET_AMOUNT,
)
from tests.jurisdictions.ca_on.end_to_end.support import CA_ON, D, service, starting


def return_dm(*, election: int, split_amount: str) -> Worksheet:
    """Return DG's filer: 100,000 of employment income and a 20,000 pension (line 11500), so the
    Federal Worksheet for line 31400 gives 2,000.00, with the election and the Form T1032 amount
    as given."""
    base = starting(
        "100000", (), "0", "0", "0", "0", "0", other_pensions_and_superannuation="20000"
    )
    given = (
        Artifact(PENSION_SPLIT_ELECTION, election),
        Artifact(PENSION_SPLIT_AMOUNT, D(split_amount)),
    )
    kinds = {artifact.kind for artifact in given}
    rest = [artifact for artifact in base if artifact.kind not in kinds]
    return service().compute(CA_ON, 2025, *rest, *given)["ca-on/return"][0]


def test_an_election_of_0_leaves_line_31400_as_the_worksheet_gives_it() -> None:
    # Federal Worksheet for line 31400: the lesser of line 8 (20,000.00) and $2,000. The Form
    # T1032 amount is given but the filer does not elect to split, so it is not read.
    worksheet = return_dm(election=0, split_amount="1000")

    assert worksheet.get(PENSION_WORKSHEET_AMOUNT).value == D("2000.00")
    assert worksheet.get(PENSION_INCOME_CREDIT).value == D("2000.00")


def test_an_election_of_1_enters_the_form_t1032_amount_on_line_31400() -> None:
    # "if you are electing to split your eligible pension ... complete Form T1032 ... to calculate
    # the amount to enter on line 31400 of your return instead": the worksheet still gives
    # 2,000.00 and line 31400 is the caller's 1,000.00.
    worksheet = return_dm(election=1, split_amount="1000")

    assert worksheet.get(PENSION_WORKSHEET_AMOUNT).value == D("2000.00")
    assert worksheet.get(PENSION_INCOME_CREDIT).value == D("1000.00")


def test_the_form_t1032_amount_is_taken_as_entered_whatever_the_worksheet_gives() -> None:
    # The Form T1032 amount is the caller's, taken as entered: 1,500.00 here, the worksheet
    # giving 2,000.00.
    worksheet = return_dm(election=1, split_amount="1500")

    assert worksheet.get(PENSION_WORKSHEET_AMOUNT).value == D("2000.00")
    assert worksheet.get(PENSION_INCOME_CREDIT).value == D("1500.00")


def test_an_election_of_1_with_a_form_t1032_amount_of_0_gives_a_line_31400_of_0() -> None:
    # The election picks the Form T1032 amount even when the worksheet gives more (2,000.00).
    worksheet = return_dm(election=1, split_amount="0")

    assert worksheet.get(PENSION_WORKSHEET_AMOUNT).value == D("2000.00")
    assert worksheet.get(PENSION_INCOME_CREDIT).value == D("0")
