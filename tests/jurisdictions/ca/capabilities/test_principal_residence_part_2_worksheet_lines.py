"""Unit tests for Form T2091(IND)-WS Part 2, lines 28 to 58, and line 59 of Part 3, which reads
line 58.

Each line of Part 2 that is calculated is one capability,
`PrincipalResidenceWorksheetLine<N>Capability` (N the worksheet's line number), with its own catalog
kind and trace line. The copies of earlier
figures (lines 28, 29, 31, 34, 37, 38, 39, 42, 43, 45, 48, 49, 51, 52, 54, 56 and 57) are not
capabilities. An area is skipped when the form says so: area A (lines 28 to 35) when line 2 is not
less than line 5, area B (lines 37 to 46) when line 1 is not less than line 4 or line 11 is more
than line 19, and area C (line 48 to 49) when line 1 is not less than line 4. A skipped line is 0,
and so is every Part 2 line of a property whose T664 election was not filed or whose Part 2 does not
apply.

The figures are those of `principal_residence_figures.py`: `PART_2_WORKSHEET_PROPERTY_1` (Part 2
applies, Chart 1 does not) and `PART_2_WORKSHEET_PROPERTY_2` (Part 2 applies, Chart 1 applies, area
B skipped), each worked by hand in that module.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any, cast

import pytest

import app.jurisdictions.ca.capabilities as ca_capabilities
from app.domain.artifact import Artifact, ArtifactKind
from app.domain.capability import CapabilityRegistry
from app.domain.errors import InvalidCapabilityError, MissingArtifactError
from app.domain.record_list import RecordList
from app.domain.trace import ItemsTotalLine
from app.domain.trace.base import TraceLine
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_30 import (
    PrincipalResidenceWorksheetLine30Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_32 import (
    PrincipalResidenceWorksheetLine32Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_33 import (
    PrincipalResidenceWorksheetLine33Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_35 import (
    PrincipalResidenceWorksheetLine35Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_36 import (
    PrincipalResidenceWorksheetLine36Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_40 import (
    PrincipalResidenceWorksheetLine40Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_41 import (
    PrincipalResidenceWorksheetLine41Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_44 import (
    PrincipalResidenceWorksheetLine44Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_46 import (
    PrincipalResidenceWorksheetLine46Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_47 import (
    PrincipalResidenceWorksheetLine47Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_50 import (
    PrincipalResidenceWorksheetLine50Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_53 import (
    PrincipalResidenceWorksheetLine53Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_55 import (
    PrincipalResidenceWorksheetLine55Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_58 import (
    PrincipalResidenceWorksheetLine58Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_59 import (
    PrincipalResidenceWorksheetLine59Capability,
)
from app.jurisdictions.ca.capabilities.principal_residence_worksheet_rows import (
    PrincipalResidenceWorksheetRows,
)
from app.jurisdictions.ca.catalog import (
    CAREGIVER_AMOUNT,
    PRINCIPAL_RESIDENCE_PROPERTIES,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_30,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_32,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_33,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_35,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_36,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_40,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_41,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_44,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_46,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_47,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_50,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_53,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_55,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_58,
    PRINCIPAL_RESIDENCE_WORKSHEET_LINE_59,
    RESIDENCE_WS_COST_BASE_ADJUSTMENTS_TO_FEB_1994,
)
from app.jurisdictions.ca.trace import (
    PrincipalResidenceWorksheetLine30,
    PrincipalResidenceWorksheetLine32,
    PrincipalResidenceWorksheetLine33,
    PrincipalResidenceWorksheetLine35,
    PrincipalResidenceWorksheetLine36,
    PrincipalResidenceWorksheetLine40,
    PrincipalResidenceWorksheetLine41,
    PrincipalResidenceWorksheetLine44,
    PrincipalResidenceWorksheetLine46,
    PrincipalResidenceWorksheetLine47,
    PrincipalResidenceWorksheetLine50,
    PrincipalResidenceWorksheetLine53,
    PrincipalResidenceWorksheetLine55,
    PrincipalResidenceWorksheetLine58,
)
from tests.jurisdictions.ca.capabilities.principal_residence_figures import (
    CENT,
    DOLLAR_FLOOR,
    PART_2_WORKSHEET_PROPERTY_1,
    PART_2_WORKSHEET_PROPERTY_2,
    WORKSHEET_NOT_FILED,
    WORKSHEET_WORKED,
    chart_1_factor,
    part_2_worksheet,
    properties,
    rounding,
)

D = Decimal

PART_2_CAPABILITIES: dict[int, Any] = {
    30: PrincipalResidenceWorksheetLine30Capability,
    32: PrincipalResidenceWorksheetLine32Capability,
    33: PrincipalResidenceWorksheetLine33Capability,
    35: PrincipalResidenceWorksheetLine35Capability,
    36: PrincipalResidenceWorksheetLine36Capability,
    40: PrincipalResidenceWorksheetLine40Capability,
    41: PrincipalResidenceWorksheetLine41Capability,
    44: PrincipalResidenceWorksheetLine44Capability,
    46: PrincipalResidenceWorksheetLine46Capability,
    47: PrincipalResidenceWorksheetLine47Capability,
    50: PrincipalResidenceWorksheetLine50Capability,
    53: PrincipalResidenceWorksheetLine53Capability,
    55: PrincipalResidenceWorksheetLine55Capability,
    58: PrincipalResidenceWorksheetLine58Capability,
}

PART_2_KINDS: dict[int, ArtifactKind[Decimal]] = {
    30: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_30,
    32: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_32,
    33: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_33,
    35: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_35,
    36: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_36,
    40: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_40,
    41: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_41,
    44: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_44,
    46: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_46,
    47: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_47,
    50: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_50,
    53: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_53,
    55: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_55,
    58: PRINCIPAL_RESIDENCE_WORKSHEET_LINE_58,
}

PART_2_TRACE: dict[int, type[TraceLine]] = {
    30: PrincipalResidenceWorksheetLine30,
    32: PrincipalResidenceWorksheetLine32,
    33: PrincipalResidenceWorksheetLine33,
    35: PrincipalResidenceWorksheetLine35,
    36: PrincipalResidenceWorksheetLine36,
    40: PrincipalResidenceWorksheetLine40,
    41: PrincipalResidenceWorksheetLine41,
    44: PrincipalResidenceWorksheetLine44,
    46: PrincipalResidenceWorksheetLine46,
    47: PrincipalResidenceWorksheetLine47,
    50: PrincipalResidenceWorksheetLine50,
    53: PrincipalResidenceWorksheetLine53,
    55: PrincipalResidenceWorksheetLine55,
    58: PrincipalResidenceWorksheetLine58,
}

PART_2_LINE_NUMBERS = list(PART_2_CAPABILITIES)

# Property 1 (Part 2 applies, Chart 1 does not): area A 60,000.00 (line 36), area B 37,384.62
# (line 47), area C 0 (line 50), line 58 58,235.29.
VALUES_PROPERTY_1: dict[int, str] = {
    30: "120000.00",
    32: "2",
    33: "240000.00",
    35: "60000.00",
    36: "60000.00",
    40: "246000.00",
    41: "54000.00",
    44: "216000.00",
    46: "16615.38",
    47: "37384.62",
    50: "0",
    53: "97384.62",
    55: "97384.62",
    58: "58235.29",
}

# Property 2 (Part 2 applies, Chart 1 applies, area B skipped): area A 80,000.00 (line 36), area C
# 70,000.00 (line 50), line 55 10,000.00, line 58 10,000.00.
VALUES_PROPERTY_2: dict[int, str] = {
    30: "160000.00",
    32: "1",
    33: "160000.00",
    35: "80000.00",
    36: "80000.00",
    40: "0",
    41: "0",
    44: "0",
    46: "0",
    47: "0",
    50: "70000.00",
    53: "80000.00",
    55: "10000.00",
    58: "10000.00",
}

# Each of the two properties not filed, or with Part 2 not applying, has every Part 2 line 0.
VALUES_NONE: dict[int, str] = {line: "0" for line in PART_2_LINE_NUMBERS}


def capability(
    line: int,
    rounding_data: Any = None,
    factor: Any = None,
) -> Any:
    """The capability of `line`, wired to the `ca/principal_residence_properties` record list and
    its kind; by default the rounding dataset rounds half up to the cent."""
    return PART_2_CAPABILITIES[line](
        rounding=rounding_data or rounding(),
        chart_1_factor=factor or chart_1_factor(),
        properties=PRINCIPAL_RESIDENCE_PROPERTIES,
        output=PART_2_KINDS[line],
    )


def output_of(
    line: int,
    *given: Any,
    rule: Any = CENT,
) -> Artifact[Any]:
    """The output of `line` over the properties `given`, in the order given."""
    outputs: tuple[Artifact[Any], ...] = (
        capability(line, rounding(rule)).compute((properties(*given),)).outputs
    )
    (output,) = outputs
    return output


def value_of(line: int, *given: Any, rule: Any = CENT) -> Decimal:
    value = output_of(line, *given, rule=rule).value
    assert isinstance(value, Decimal)
    return value


def line_59_of(*given: Any) -> Decimal:
    """Line 59 over the properties `given`."""
    wired = PrincipalResidenceWorksheetLine59Capability(
        rounding=rounding(),
        chart_1_factor=chart_1_factor(),
        properties=PRINCIPAL_RESIDENCE_PROPERTIES,
        output=PRINCIPAL_RESIDENCE_WORKSHEET_LINE_59,
    )
    (output,) = wired.compute((properties(*given),)).outputs
    assert isinstance(output.value, Decimal)
    return output.value


# --- contract and wiring ------------------------------------------------------------------------


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_is_registered_under_its_identifier(line: int) -> None:
    registered = CapabilityRegistry.shared().get(f"ca/principal_residence_worksheet_line_{line}")

    assert registered is PART_2_CAPABILITIES[line]
    assert registered.__module__ == (
        f"app.jurisdictions.ca.capabilities.principal_residence_worksheet_line_{line}"
    )


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_is_exported_from_the_ca_capabilities_package(line: int) -> None:
    assert f"principal_residence_worksheet_line_{line}" in ca_capabilities.__all__
    module = getattr(ca_capabilities, f"principal_residence_worksheet_line_{line}")
    assert getattr(module, PART_2_CAPABILITIES[line].__name__) is PART_2_CAPABILITIES[line]


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_is_a_subclass_of_the_worksheet_rows_base(line: int) -> None:
    assert issubclass(PART_2_CAPABILITIES[line], PrincipalResidenceWorksheetRows)


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_declares_its_contract(line: int) -> None:
    assert capability(line).consumes == frozenset({PRINCIPAL_RESIDENCE_PROPERTIES})
    assert capability(line).produces == frozenset({PART_2_KINDS[line]})


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_declares_its_slots(line: int) -> None:
    cls = PART_2_CAPABILITIES[line]
    assert list(cls.PARAMETERS) == ["rounding", "chart_1_factor"]
    assert cls.CONSUMES == {"properties": RecordList}
    assert cls.PRODUCES == {"output": Decimal}
    assert not cls.is_list_slot("properties")


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_leaves_its_contract_to_the_base(line: int) -> None:
    assert "consumes" not in vars(PART_2_CAPABILITIES[line])
    assert "produces" not in vars(PART_2_CAPABILITIES[line])


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_is_built_from_its_slot_names_as_keywords(line: int) -> None:
    wired = PART_2_CAPABILITIES[line](
        rounding=rounding(),
        chart_1_factor=chart_1_factor(),
        properties=PRINCIPAL_RESIDENCE_PROPERTIES,
        output=PART_2_KINDS[line],
    )

    assert wired.compute((properties(PART_2_WORKSHEET_PROPERTY_1),)).outputs == (
        Artifact(PART_2_KINDS[line], D(VALUES_PROPERTY_1[line])),
    )


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_takes_no_separate_rounding_argument(line: int) -> None:
    with pytest.raises(TypeError):
        PART_2_CAPABILITIES[line](
            rounding(),
            chart_1_factor(),
            PRINCIPAL_RESIDENCE_PROPERTIES,
            PART_2_KINDS[line],
            CENT,
        )


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_rejects_a_money_kind_for_its_properties(line: int) -> None:
    name = PART_2_CAPABILITIES[line].__name__
    with pytest.raises(InvalidCapabilityError, match=f"{name}.*'properties'"):
        PART_2_CAPABILITIES[line](
            rounding=rounding(),
            chart_1_factor=chart_1_factor(),
            properties=CAREGIVER_AMOUNT,
            output=PART_2_KINDS[line],
        )


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_has_one_output_of_its_kind(line: int) -> None:
    outputs = capability(line).compute((properties(PART_2_WORKSHEET_PROPERTY_1),)).outputs

    assert len(outputs) == 1
    assert outputs[0].kind is PART_2_KINDS[line]
    assert type(outputs[0].value) is Decimal


def test_line_59_is_registered_under_its_identifier() -> None:
    registered = CapabilityRegistry.shared().get("ca/principal_residence_worksheet_line_59")

    assert registered is PrincipalResidenceWorksheetLine59Capability
    assert PrincipalResidenceWorksheetLine59Capability.PRODUCES == {"output": Decimal}


# --- computing: the two worked properties -------------------------------------------------------


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_each_line_of_property_1(line: int) -> None:
    assert value_of(line, PART_2_WORKSHEET_PROPERTY_1) == D(VALUES_PROPERTY_1[line])


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_each_line_of_property_2(line: int) -> None:
    assert value_of(line, PART_2_WORKSHEET_PROPERTY_2) == D(VALUES_PROPERTY_2[line])


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_two_properties_give_the_sum_of_their_own_amounts(line: int) -> None:
    total = value_of(line, PART_2_WORKSHEET_PROPERTY_1, PART_2_WORKSHEET_PROPERTY_2)

    assert total == D(VALUES_PROPERTY_1[line]) + D(VALUES_PROPERTY_2[line])


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_the_total_does_not_depend_on_the_order(line: int) -> None:
    assert value_of(line, PART_2_WORKSHEET_PROPERTY_1, PART_2_WORKSHEET_PROPERTY_2) == value_of(
        line, PART_2_WORKSHEET_PROPERTY_2, PART_2_WORKSHEET_PROPERTY_1
    )


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_no_properties_give_zero(line: int) -> None:
    result = capability(line).compute((properties(),))

    assert result.outputs == (Artifact(PART_2_KINDS[line], D("0")),)


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_compute_is_repeatable(line: int) -> None:
    wired = capability(line)

    first = wired.compute((properties(PART_2_WORKSHEET_PROPERTY_1),))
    second = wired.compute((properties(PART_2_WORKSHEET_PROPERTY_1),))

    assert first == second


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_ignores_artifacts_it_does_not_consume(line: int) -> None:
    other = Artifact(CAREGIVER_AMOUNT, D("9"))

    result = capability(line).compute((other, properties(PART_2_WORKSHEET_PROPERTY_1)))

    assert result.outputs == (Artifact(PART_2_KINDS[line], D(VALUES_PROPERTY_1[line])),)


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_missing_properties_is_a_missing_artifact(line: int) -> None:
    with pytest.raises(MissingArtifactError, match="principal_residence_properties"):
        capability(line).compute(())


# --- computing: a property not filed, or with Part 2 not applying, has every Part 2 line 0 -------


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_a_property_not_filed_has_every_part_2_line_0(line: int) -> None:
    assert value_of(line, part_2_worksheet(t664_filed=0)) == D(VALUES_NONE[line])


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_a_property_not_filed_adds_nothing_to_the_others(line: int) -> None:
    assert value_of(line, PART_2_WORKSHEET_PROPERTY_1, WORKSHEET_NOT_FILED) == D(
        VALUES_PROPERTY_1[line]
    )


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_a_property_filed_without_part_2_applying_has_every_part_2_line_0(line: int) -> None:
    assert value_of(line, part_2_worksheet(PART_2_WORKSHEET_PROPERTY_2, part_2_applies=0)) == D(
        VALUES_NONE[line]
    )


# --- computing: the skipped areas ---------------------------------------------------------------


@pytest.mark.parametrize("line", [30, 32, 33, 35, 36])
def test_area_a_is_0_when_the_property_designated_every_year_before_1982(line: int) -> None:
    # Line 2 (designated before 1982) 4 is not less than line 5 (owned before 1982) 4, so area A
    # is not completed: lines 28 to 35 are not completed, and line 36 is 0. Area B is still worked:
    # line 47 is 37,384.62, so line 53 = 0 + 37,384.62 and line 58 is the lesser of line 27 and
    # line 57 (37,384.62).
    wired = part_2_worksheet(designated_before=4)

    assert value_of(line, wired) == D("0")


def test_area_b_is_worked_when_area_a_is_skipped() -> None:
    wired = part_2_worksheet(designated_before=4)

    assert value_of(47, wired) == D("37384.62")
    assert value_of(53, wired) == D("37384.62")
    assert value_of(55, wired) == D("37384.62")
    assert value_of(58, wired) == D("37384.62")


@pytest.mark.parametrize("line", [40, 41, 44, 46, 47, 50])
def test_areas_b_and_c_are_0_when_line_1_is_not_less_than_line_4(line: int) -> None:
    # Line 1 (designated after 1981 and before 1995) 13 is not less than line 4 (owned in the same
    # period) 13, so area B (lines 37 to 47) and area C (lines 48 to 50) are not completed.
    wired = part_2_worksheet(ws_years_designated_after_1981=13, ws_years_owned_after_1981=13)

    assert value_of(line, wired) == D("0")


def test_area_d_takes_area_a_alone_when_areas_b_and_c_are_skipped() -> None:
    # Line 51 = line 36 = 60,000.00; line 52 = line 47 = 0; line 53 = 60,000.00; line 54 = line 50
    # = 0; line 55 = 60,000.00. Line 27 is 10,588.24 here (line 3 is now 14), so line 58 is that.
    wired = part_2_worksheet(ws_years_designated_after_1981=13, ws_years_owned_after_1981=13)

    assert value_of(36, wired) == D("60000.00")
    assert value_of(53, wired) == D("60000.00")
    assert value_of(55, wired) == D("60000.00")
    assert value_of(58, wired) == D("10588.24")


def test_area_b_is_skipped_when_fair_market_value_1981_is_more_than_line_19() -> None:
    # Line 11 is 300,001.00, more than line 19 (300,000.00), so lines 40 to 47 are 0. Area C is
    # worked: line 50 = 300,001.00 - 300,000.00 = 1.00. Area A: line 30 = 300,001.00 - 120,000.00
    # = 180,001.00; line 33 = 180,001.00 x 2 = 360,002.00; line 35 = 360,002.00 / 4 = 90,000.50;
    # line 36 = 90,000.50. Area D: line 53 = 90,000.50 and line 55 = 90,000.50 - 1.00 = 89,999.50.
    wired = part_2_worksheet(fmv_1981="300001.00")

    assert value_of(30, wired) == D("180001.00")
    assert value_of(35, wired) == D("90000.50")
    assert value_of(36, wired) == D("90000.50")
    for line in (40, 41, 44, 46, 47):
        assert value_of(line, wired) == D("0"), line
    assert value_of(50, wired) == D("1.00")
    assert value_of(53, wired) == D("90000.50")
    assert value_of(55, wired) == D("89999.50")


def test_area_c_is_the_loss_and_area_d_is_floored_at_0() -> None:
    # Property 2 with line 11 at 400,000.00: area A line 36 = 100,000.00, area C line 50 =
    # 400,000.00 - 290,000.00 = 110,000.00, so line 53 = 100,000.00 and line 55 = 0.
    wired = part_2_worksheet(PART_2_WORKSHEET_PROPERTY_2, fmv_1981="400000.00")

    assert value_of(36, wired) == D("100000.00")
    assert value_of(50, wired) == D("110000.00")
    assert value_of(53, wired) == D("100000.00")
    assert value_of(55, wired) == D("0")
    assert value_of(58, wired) == D("0")


def test_line_47_is_floored_at_0_and_line_41_and_44_keep_their_sign() -> None:
    # Line 40 = 240,000.00 + 100,000.00 = 340,000.00, so line 41 = 300,000.00 - 340,000.00 =
    # -40,000.00; line 44 = -40,000.00 x 4 = -160,000.00; line 46 = -160,000.00 / 13 = -12,307.69;
    # line 47 = -40,000.00 + 12,307.69, which is below 0, so 0.
    wired = part_2_worksheet(ws_cost_base_adjustments_to_feb_1994="100000.00")

    assert value_of(40, wired) == D("340000.00")
    assert value_of(41, wired) == D("-40000.00")
    assert value_of(44, wired) == D("-160000.00")
    assert value_of(46, wired) == D("-12307.69")
    assert value_of(47, wired) == D("0")


# --- computing: the ratios, rounded by the dataset's rule ---------------------------------------


def test_line_46_a_half_cent_rounds_up_and_line_47_takes_the_rounded_figure() -> None:
    # Line 44 is line 41 (1.00) x line 1 (1), and line 45 is line 4 (8): 1.00 / 8 = 0.125, half up
    # to 0.13. Line 47 = 1.00 - 0.13 = 0.87.
    wired = part_2_worksheet(
        ws_years_designated_after_1981=1,
        ws_years_owned_after_1981=8,
        ws_cost_base_adjustments_to_feb_1994="59999.00",
    )

    assert value_of(41, wired) == D("1.00")
    assert value_of(46, wired) == D("0.13")
    assert value_of(47, wired) == D("0.87")


def test_line_35_is_rounded_by_the_datasets_rule() -> None:
    # Line 33 is 240,000.00 and line 34 (owned before 1982) is 7: 240,000.00 / 7 = 34,285.714...,
    # half up to the cent 34,285.71, or whole dollars 34,285. Line 36 = 120,000.00 - the quotient.
    wired = part_2_worksheet(owned_before=7)

    assert value_of(35, wired) == D("34285.71")
    assert value_of(35, wired, rule=DOLLAR_FLOOR) == D("34285")
    assert value_of(36, wired) == D("85714.29")
    assert value_of(36, wired, rule=DOLLAR_FLOOR) == D("85715")


def test_line_46_is_rounded_by_the_datasets_rule() -> None:
    # Line 44 is 216,000.00 and line 45 is 13: 16,615.384..., half up to 16,615.38 or 16,615.
    assert value_of(46, PART_2_WORKSHEET_PROPERTY_1) == D("16615.38")
    assert value_of(46, PART_2_WORKSHEET_PROPERTY_1, rule=DOLLAR_FLOOR) == D("16615")
    assert value_of(47, PART_2_WORKSHEET_PROPERTY_1, rule=DOLLAR_FLOOR) == D("37385")


# --- computing: the lesser of lines 56 and 57 --------------------------------------------------


def test_line_58_is_the_lesser_of_lines_56_and_57() -> None:
    # Property 1: line 56 (line 27) 58,235.29 is less than line 57 (line 55) 97,384.62. Property 2:
    # line 56 80,666.67 is more than line 57 10,000.00.
    assert value_of(58, PART_2_WORKSHEET_PROPERTY_1) == D("58235.29")
    assert value_of(58, PART_2_WORKSHEET_PROPERTY_2) == D("10000.00")


# --- the kinds ----------------------------------------------------------------------------------


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_each_line_is_a_decimal_kind_registered_under_its_line(line: int) -> None:
    kind = PART_2_KINDS[line]

    assert kind.identifier == f"ca/principal_residence_worksheet_line_{line}"
    assert kind.value_type is Decimal


def test_line_32_is_a_decimal_count_as_line_23_is() -> None:
    assert value_of(32, PART_2_WORKSHEET_PROPERTY_1) == D("2")
    assert type(value_of(32, PART_2_WORKSHEET_PROPERTY_1)) is Decimal


# --- the line 59 change: line 58 when Part 2 is completed, else line 27 --------------------------


def test_line_59_is_line_58_when_part_2_is_completed() -> None:
    assert line_59_of(PART_2_WORKSHEET_PROPERTY_1) == D("58235.29")
    assert line_59_of(PART_2_WORKSHEET_PROPERTY_2) == D("10000.00")


def test_line_59_is_line_27_when_part_2_does_not_apply() -> None:
    # Line 27 of property 2 is 80,666.67 and its line 58 is 10,000.00; with Part 2 not applying,
    # line 59 is line 27.
    assert line_59_of(part_2_worksheet(PART_2_WORKSHEET_PROPERTY_2, part_2_applies=0)) == D(
        "80666.67"
    )


def test_line_59_is_0_when_the_election_was_not_filed() -> None:
    assert line_59_of(part_2_worksheet(t664_filed=0)) == D("0")


def test_line_59_adds_the_line_58_of_a_completed_property_and_the_line_27_of_another() -> None:
    # Property 2 completed: line 59 10,000.00. The worked example (not Part 2): line 27 50,000.00.
    assert line_59_of(PART_2_WORKSHEET_PROPERTY_2, WORKSHEET_WORKED) == D("60000.00")


def test_the_worksheet_line_59_of_a_worked_example_is_still_line_27() -> None:
    assert line_59_of(WORKSHEET_WORKED) == D("50000.00")


# --- the cost base adjustments to February 1994 (line 12) are a field of each property ------------


def test_worksheet_line_12_is_the_cost_base_adjustments_field() -> None:
    # Line 39 = worksheet line 12 (6,000.00 for property 1), not the T2091 line 13 (10,000.00).
    assert RESIDENCE_WS_COST_BASE_ADJUSTMENTS_TO_FEB_1994.value_type is Decimal
    assert RESIDENCE_WS_COST_BASE_ADJUSTMENTS_TO_FEB_1994.non_negative is True
    assert value_of(40, PART_2_WORKSHEET_PROPERTY_1) == D("246000.00")


# --- the trace: one line per property, then the total -------------------------------------------


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_traces_one_line_per_property_then_the_total(line: int) -> None:
    trace = (
        capability(line)
        .compute((properties(PART_2_WORKSHEET_PROPERTY_1, PART_2_WORKSHEET_PROPERTY_2),))
        .trace
    )

    assert [type(item) for item in trace] == [
        PART_2_TRACE[line],
        PART_2_TRACE[line],
        ItemsTotalLine,
    ]
    total = D(VALUES_PROPERTY_1[line]) + D(VALUES_PROPERTY_2[line])
    assert trace[-1] == ItemsTotalLine(
        PART_2_KINDS[line],
        ((1, D(VALUES_PROPERTY_1[line])), (2, D(VALUES_PROPERTY_2[line]))),
        total,
    )


@pytest.mark.parametrize("line", PART_2_LINE_NUMBERS)
def test_a_property_not_completed_is_traced_as_not_completed(line: int) -> None:
    trace = capability(line).compute((properties(part_2_worksheet(t664_filed=0)),)).trace

    first = cast(Any, trace[0])
    assert first.completed is False
    assert first.position == 1
    assert first.amount == D("0")
