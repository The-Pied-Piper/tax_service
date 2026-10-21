"""Unit tests for ShortTermRentalCcaRows, the base of the two Chart B capabilities of Form T776.

Form T776, Chart B, "Non-compliant amount of CCA for short-term rentals": "Enter each short-term
rental or mixed rental property on a separate row"; "Column 1: Class number"; "Column 4: Related
portion of the available CCA from column 21 in Area A"; "Column 7 ***: Non-compliant amount
(column 4 multiplied by column 5 divided by column 6)".

The base is not registered itself. It reads and checks the rows once for both capabilities: each
row is column 4 times column 5 over column 6 as an exact fraction, rounded once with the
`rounding` dataset's rule, in the caller's order. A row whose column 6 is 0, or whose column 5 is
above column 6, is a ValidationError naming the row. What is built from the rows (a total, a
total for each class) is each capability's own; these tests run both on the same rows.
"""

from __future__ import annotations

from typing import Any

import pytest

from app.domain.capability import Capability, CapabilityRegistry
from app.domain.errors import ValidationError
from app.domain.parameters.rounding import RoundingMode, RoundTo
from app.jurisdictions.ca.capabilities.short_term_rental_cca_rows import ShortTermRentalCcaRows
from app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_cca import (
    ShortTermRentalNonCompliantCca,
)
from app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_cca_by_class import (
    ShortTermRentalNonCompliantCcaByClass,
)
from app.jurisdictions.ca.catalog import SHORT_TERM_RENTAL_CCA_UNITS
from tests.jurisdictions.ca.capabilities.short_term_rental_cca import (
    BY_CLASS,
    CENT,
    CLASS_8_ROW,
    LINE_9367,
    THIRD_ROW,
    TICKET_ROW,
    D,
    Row,
    rounding,
    units,
)


def total_capability(**changes: Any) -> Capability:
    return ShortTermRentalNonCompliantCca(
        changes.get("rounding", rounding()), SHORT_TERM_RENTAL_CCA_UNITS, LINE_9367
    )


def by_class_capability(**changes: Any) -> Capability:
    return ShortTermRentalNonCompliantCcaByClass(
        changes.get("rounding", rounding()), SHORT_TERM_RENTAL_CCA_UNITS, BY_CLASS
    )


BOTH = [total_capability, by_class_capability]


def run(make: Any, *rows: Row, **changes: Any) -> Any:
    return make(**changes).compute((units(*rows),))


def test_both_capabilities_are_built_on_the_one_base() -> None:
    assert issubclass(ShortTermRentalNonCompliantCca, ShortTermRentalCcaRows)
    assert issubclass(ShortTermRentalNonCompliantCcaByClass, ShortTermRentalCcaRows)
    assert issubclass(ShortTermRentalCcaRows, Capability)


def test_the_base_is_not_registered_itself() -> None:
    registry = CapabilityRegistry.shared()

    assert registry.get("ca/short_term_rental_non_compliant_cca") is ShortTermRentalNonCompliantCca
    assert (
        registry.get("ca/short_term_rental_non_compliant_cca_by_class")
        is ShortTermRentalNonCompliantCcaByClass
    )
    registered = [registry.get(name) for name in registry.identifiers()]
    assert ShortTermRentalCcaRows not in registered


def test_both_capabilities_read_the_same_slots() -> None:
    for cls in (ShortTermRentalNonCompliantCca, ShortTermRentalNonCompliantCcaByClass):
        assert set(cls.PARAMETERS) == {"rounding"}
        assert set(cls.CONSUMES) == {"units"}


def test_the_capabilities_leave_the_row_work_to_the_base() -> None:
    for cls in (ShortTermRentalNonCompliantCca, ShortTermRentalNonCompliantCcaByClass):
        assert "_rows" not in vars(cls)
    assert "_rows" in vars(ShortTermRentalCcaRows)


@pytest.mark.parametrize("make", BOTH)
def test_a_row_whose_column_6_is_zero_is_refused_naming_the_row(make: Any) -> None:
    with pytest.raises(ValidationError, match="row 2.*short_term_rental_days"):
        run(make, TICKET_ROW, ("1", "900", 0, 0))


@pytest.mark.parametrize("make", BOTH)
def test_a_row_whose_column_5_is_above_column_6_is_refused_naming_the_row(make: Any) -> None:
    with pytest.raises(ValidationError, match="row 3.*short_term_rental_non_compliant_days"):
        run(make, TICKET_ROW, THIRD_ROW, ("1", "900", 91, 90))


@pytest.mark.parametrize("make", BOTH)
def test_the_first_refused_row_is_the_one_named(make: Any) -> None:
    with pytest.raises(ValidationError, match="row 2"):
        run(make, TICKET_ROW, ("1", "900", 0, 0), ("1", "900", 91, 90))


@pytest.mark.parametrize("make", BOTH)
def test_a_column_5_equal_to_column_6_is_not_refused(make: Any) -> None:
    assert run(make, ("1", "900", 90, 90)).trace


@pytest.mark.parametrize("make", BOTH)
def test_each_row_is_rounded_once_by_the_dataset_rule_before_it_is_used(make: Any) -> None:
    # Three rows of 100 x 1 / 3 = 33.333...: 33.33 each, 99.99 in all, not the rounded 100.00.
    (output,) = run(make, THIRD_ROW, THIRD_ROW, THIRD_ROW).outputs

    if output.kind is LINE_9367:
        assert output.value == D("99.99")
    else:
        (record,) = output.value.records
        assert list(record.values())[1] == D("99.99")


@pytest.mark.parametrize("make", BOTH)
def test_the_rounding_comes_from_the_dataset(make: Any) -> None:
    whole = rounding(RoundTo(D("1"), RoundingMode.FLOOR))

    (output,) = run(make, ("1", "100", 2, 3), rounding=whole).outputs

    # 100 x 2 / 3 = 66.67 floors to 66 whole dollars.
    if output.kind is LINE_9367:
        assert output.value == D("66")
    else:
        (record,) = output.value.records
        assert list(record.values())[1] == D("66")


@pytest.mark.parametrize("make", BOTH)
def test_both_work_the_acceptance_row_the_same_way(make: Any) -> None:
    # 900 of related CCA, 30 non-compliant days of 90: column 7 is 300.00.
    (output,) = run(make, TICKET_ROW, CLASS_8_ROW).outputs

    if output.kind is LINE_9367:
        assert output.value == D("550.00")
    else:
        assert [list(record.values())[1] for record in output.value.records] == [
            D("300.00"),
            D("250.00"),
        ]


def test_the_cent_rule_is_the_one_the_tests_assume() -> None:
    assert rounding().rounding == CENT
