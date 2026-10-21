"""CA-ON 2025 end to end: return ai."""

from __future__ import annotations

from typing import Any

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.record_list import RecordList
from app.domain.trace import ItemsTotalLine
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.capabilities.principal_residence_gain import PrincipalResidenceGain
from app.jurisdictions.ca.catalog import (
    CAPITAL_GAIN,
    INCLUDED_CAPITAL_GAIN,
    NET_INCOME,
    PERSONAL_USE_PROPERTY_GAIN,
    PERSONAL_USE_PROPERTY_GAIN_ROWS,
    PRINCIPAL_RESIDENCE_GAIN,
    PRINCIPAL_RESIDENCE_PROPERTIES,
    REFUND_OR_BALANCE_OWING,
    RESIDENCE_ADJUSTED_COST_BASE,
    RESIDENCE_OUTLAYS,
    RESIDENCE_PLUS_ONE_YEAR,
    RESIDENCE_PROCEEDS,
    RESIDENCE_YEARS_DESIGNATED_1972_TO_1981,
    RESIDENCE_YEARS_DESIGNATED_AFTER_1981,
    RESIDENCE_YEARS_OWNED_1972_TO_1981,
    RESIDENCE_YEARS_OWNED_AFTER_1981,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_INCOME,
    TOTAL_INCOME,
    TOTAL_PAYABLE,
)
from app.jurisdictions.ca.trace import PrincipalResidenceGainLine
from tests.jurisdictions.ca_on.end_to_end.support import CENT, D, compute

EXAMPLE = (6, 0, 10, 0, "400000.00", "5000.00", "95000.00", 1)
NOT_ENDING = (1, 0, 6, 0, "250000.00", "0.00", "180000.00", 1)


def return_ai(**overrides: Any) -> Worksheet:
    """Return AI's inputs, as in `returns/2025_return_ai.yaml`: employment income of 60000 and two
    principal residence properties sold, each a chosen figure; `overrides` replace any keyword of
    `compute`, for the variants below.
    """
    given: dict[str, Any] = {
        "principal_residence_properties_rows": (EXAMPLE, NOT_ENDING),
        "income_tax_deducted": "25000",
    }
    return compute("60000", (), "0", "0", "0", "0", "0", **{**given, **overrides})


def test_return_ais_two_properties_have_taxable_gains_of_90000_and_46666_67() -> None:
    # Property 1 (the worked example): line 18 = 400000.00 - (95000.00 + 5000.00) = 300000.00;
    # line 20 = 6 + 1 = 7; line 21 = 2100000.00; line 23 = 2100000.00 / 10 = 210000.00; line 24 =
    # 300000.00 - 210000.00 = 90000.00. Property 2: line 18 = 250000.00 - 180000.00 = 70000.00;
    # line 20 = 1 + 1 = 2; line 21 = 140000.00; line 23 = 140000.00 / 6 = 23333.333..., half-up
    # to the cent 23333.33; line 24 = 70000.00 - 23333.33 = 46666.67. Line 54 is line 24 for each
    # (no Part 2, no Part 4), and the total is 90000.00 + 46666.67 = 136666.67.
    worksheet = return_ai()

    assert worksheet.get(PRINCIPAL_RESIDENCE_PROPERTIES).value == RecordList(
        PRINCIPAL_RESIDENCE_PROPERTIES.fields,
        [
            {
                RESIDENCE_YEARS_DESIGNATED_AFTER_1981: 6,
                RESIDENCE_YEARS_DESIGNATED_1972_TO_1981: 0,
                RESIDENCE_YEARS_OWNED_AFTER_1981: 10,
                RESIDENCE_YEARS_OWNED_1972_TO_1981: 0,
                RESIDENCE_PROCEEDS: D("400000.00"),
                RESIDENCE_OUTLAYS: D("5000.00"),
                RESIDENCE_ADJUSTED_COST_BASE: D("95000.00"),
                RESIDENCE_PLUS_ONE_YEAR: 1,
            },
            {
                RESIDENCE_YEARS_DESIGNATED_AFTER_1981: 1,
                RESIDENCE_YEARS_DESIGNATED_1972_TO_1981: 0,
                RESIDENCE_YEARS_OWNED_AFTER_1981: 6,
                RESIDENCE_YEARS_OWNED_1972_TO_1981: 0,
                RESIDENCE_PROCEEDS: D("250000.00"),
                RESIDENCE_OUTLAYS: D("0.00"),
                RESIDENCE_ADJUSTED_COST_BASE: D("180000.00"),
                RESIDENCE_PLUS_ONE_YEAR: 1,
            },
        ],
    )
    assert worksheet.producer_of(PRINCIPAL_RESIDENCE_PROPERTIES) is None
    assert isinstance(worksheet.producer_of(PRINCIPAL_RESIDENCE_GAIN), PrincipalResidenceGain)
    assert worksheet.get(PRINCIPAL_RESIDENCE_GAIN).value == D("136666.67")


def test_return_ais_trace_names_each_property_and_totals_the_taxable_gains() -> None:
    worksheet = return_ai()

    lines = [
        line
        for line in worksheet.trace
        if isinstance(line, PrincipalResidenceGainLine | ItemsTotalLine)
        and line.output == PRINCIPAL_RESIDENCE_GAIN
    ]
    assert lines == [
        PrincipalResidenceGainLine(
            output=PRINCIPAL_RESIDENCE_GAIN,
            position=1,
            years_designated_after_1981=6,
            years_designated_1972_to_1981=0,
            designated=6,
            years_owned_after_1981=10,
            years_owned_1972_to_1981=0,
            owned=10,
            plus_one=1,
            proceeds=D("400000.00"),
            adjusted_cost_base=D("95000.00"),
            outlays=D("5000.00"),
            gain=D("300000.00"),
            line_20=7,
            line_21=D("2100000.00"),
            rounding=CENT,
            exempt=D("210000.00"),
            result=D("90000.00"),
        ),
        PrincipalResidenceGainLine(
            output=PRINCIPAL_RESIDENCE_GAIN,
            position=2,
            years_designated_after_1981=1,
            years_designated_1972_to_1981=0,
            designated=1,
            years_owned_after_1981=6,
            years_owned_1972_to_1981=0,
            owned=6,
            plus_one=1,
            proceeds=D("250000.00"),
            adjusted_cost_base=D("180000.00"),
            outlays=D("0.00"),
            gain=D("70000.00"),
            line_20=2,
            line_21=D("140000.00"),
            rounding=CENT,
            exempt=D("23333.33"),
            result=D("46666.67"),
        ),
        ItemsTotalLine(
            output=PRINCIPAL_RESIDENCE_GAIN,
            items=((1, D("90000.00")), (2, D("46666.67"))),
            total=D("136666.67"),
        ),
    ]
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    first = rendered.index(
        "principal_residence_gain: property 1: gain 300000 = proceeds 400000 less adjusted cost "
        "base 95000 less outlays 5000; exempt 210000 = 300000 × (6 designated + 1) ÷ 10 owned "
        "(half-up to 0.01); taxable gain 90000 = 300000 less 210000, not below 0"
    )
    assert rendered[first : first + 3] == (
        "principal_residence_gain: property 1: gain 300000 = proceeds 400000 less adjusted cost "
        "base 95000 less outlays 5000; exempt 210000 = 300000 × (6 designated + 1) ÷ 10 owned "
        "(half-up to 0.01); taxable gain 90000 = 300000 less 210000, not below 0",
        "principal_residence_gain: property 2: gain 70000 = proceeds 250000 less adjusted cost "
        "base 180000 less outlays 0; exempt 23333.33 = 70000 × (1 designated + 1) ÷ 6 owned "
        "(half-up to 0.01); taxable gain 46666.67 = 70000 less 23333.33, not below 0",
        "principal_residence_gain: item 1 90000 + item 2 46666.67 = 136666.67",
    )


def test_return_ais_taxable_gains_are_schedule_3_line_9_and_line_15800() -> None:
    # Line 54 of each form is entered on line 15800, the personal-use property gain of Schedule 3
    # Part 3 ("Line 9 and line 15800: Total gain only"): the rows add 0, so line 9 is 136666.67,
    # and it is the whole of the total capital gains or losses (line 21, 19700) and of line 22.
    worksheet = return_ai()

    assert worksheet.get(PERSONAL_USE_PROPERTY_GAIN_ROWS).value == D("0")
    assert worksheet.get(PERSONAL_USE_PROPERTY_GAIN).value == D("136666.67")
    assert worksheet.get(CAPITAL_GAIN).value == D("136666.67")


def test_return_ais_taxable_capital_gains_are_68333_34_on_line_12700() -> None:
    # Line 24 = 136666.67 x 50% = 68333.335, half-up to the cent 68333.34, positive, so line 12700
    # is 68333.34. Total income (line 15000) = 60000 + 68333.34 = 128333.34. The enhanced CPP
    # contributions (565.00) are deducted: net income and taxable income 127768.34. The total
    # payable is 31585.93 and with the chosen tax deducted of 25000, the balance owing (line 48500)
    # is 6585.93.
    worksheet = return_ai()

    assert worksheet.get(INCLUDED_CAPITAL_GAIN).value == D("68333.34")
    assert worksheet.get(TAXABLE_CAPITAL_GAINS).value == D("68333.34")
    assert worksheet.get(TOTAL_INCOME).value == D("128333.34")
    assert worksheet.get(NET_INCOME).value == D("127768.34")
    assert worksheet.get(TAXABLE_INCOME).value == D("127768.34")
    assert worksheet.get(TOTAL_PAYABLE).value == D("31585.93")
    assert worksheet.get(REFUND_OR_BALANCE_OWING).value == D("6585.93")


def test_no_properties_sold_add_nothing_to_line_9() -> None:
    worksheet = return_ai(principal_residence_properties_rows=())

    assert worksheet.get(PRINCIPAL_RESIDENCE_GAIN).value == D("0")
    assert worksheet.get(PERSONAL_USE_PROPERTY_GAIN).value == D("0")
    assert worksheet.get(CAPITAL_GAIN).value == D("0")
    assert worksheet.get(TAXABLE_CAPITAL_GAINS).value == D("0")
    assert worksheet.get(TOTAL_INCOME).value == D("60000")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert "principal_residence_gain: no items = 0" in rendered


def test_the_taxable_gains_are_added_to_the_personal_use_property_rows_on_line_9() -> None:
    # A personal-use property row of 3000 - 1500 - 0 = 1500 ("Total gain only") plus line 54 of
    # the two forms, 136666.67: line 9 and line 15800 are 138166.67.
    worksheet = return_ai(personal_use_property_dispositions=(("3000", "1500", "0"),))

    assert worksheet.get(PERSONAL_USE_PROPERTY_GAIN_ROWS).value == D("1500")
    assert worksheet.get(PRINCIPAL_RESIDENCE_GAIN).value == D("136666.67")
    assert worksheet.get(PERSONAL_USE_PROPERTY_GAIN).value == D("138166.67")
    assert worksheet.get(CAPITAL_GAIN).value == D("138166.67")
