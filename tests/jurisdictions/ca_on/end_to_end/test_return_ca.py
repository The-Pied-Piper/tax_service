"""CA-ON 2025 end to end: return ca."""

from __future__ import annotations

from typing import Any

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.trace import RatioAppliedLine, SubtractedLine, SubtractedNotBelowZeroLine
from app.domain.worksheet import Worksheet
from app.jurisdictions.ca.catalog import (
    FEDERAL_FOREIGN_TAX_CREDIT,
    NET_FEDERAL_TAX,
    SPLIT_INCOME_FROM_FOREIGN_SOURCES,
    SPLIT_INCOME_LINE_22,
    SPLIT_INCOME_LINE_23,
    SPLIT_INCOME_LINE_24,
    SPLIT_INCOME_LINE_29,
    SPLIT_INCOME_LINE_30,
    SPLIT_INCOME_NON_BUSINESS_FROM_FOREIGN_SOURCES,
    TOTAL_INCOME_FROM_FOREIGN_SOURCES,
    TOTAL_NON_BUSINESS_INCOME_FROM_FOREIGN_SOURCES,
    TOTAL_PAYABLE,
)
from app.jurisdictions.ca_on import catalog as ontario
from tests.jurisdictions.ca_on.end_to_end.support import CENT, D, compute


def return_ca(**overrides: Any) -> Worksheet:
    """Return CA's inputs, as in `returns/2025_return_ca.yaml`, over the keyword overrides given.

    Return AL's filer (10000 of dividends with no slip, 11500 of split income on lines 1 and 2 of
    Form T1206) with 40000 of other income that is all split income from foreign sources (line 3)
    and 10000 of other foreign investment income, 15000 of foreign tax paid to one country, the
    whole 50000 being net foreign non-business income. Lines 68370 and 68380 are 40000 and 50000,
    and so are their non-business parts.
    """
    inputs: dict[str, Any] = {
        "other_dividends_received_without_a_slip": "10000",
        "other_income": "40000",
        "foreign_investment_income": "10000",
        "foreign_tax_countries_rows": (("15000", "50000"),),
        "split_income_dividends": "11500",
        "split_income_dividends_other_than_eligible": "11500",
        "other_split_income": "40000",
        "split_income_from_foreign_sources": "40000",
        "total_income_from_foreign_sources": "50000",
        "split_income_non_business_from_foreign_sources": "40000",
        "total_non_business_income_from_foreign_sources": "50000",
    }
    inputs.update(overrides)
    return compute("0", (), "0", "0", "0", "0", "0", **inputs)


def test_return_cas_line_23_is_the_foreign_share_of_the_federal_foreign_tax_credit() -> None:
    worksheet = return_ca()

    # T2209: 50000 x 16106.29 / 61500.00 = 13094.5447..., less than the 15000 paid, so line 40500
    # is 13094.54. T1206 line 23 is that x 40000 / 50000 = 10475.632, rounded half-up to the cent.
    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("13094.54")
    assert worksheet.get(SPLIT_INCOME_FROM_FOREIGN_SOURCES).value == D("40000")
    assert worksheet.get(TOTAL_INCOME_FROM_FOREIGN_SOURCES).value == D("50000")
    assert worksheet.get(SPLIT_INCOME_LINE_23).value == D("10475.63")


def test_return_cas_line_24_takes_line_23_off_line_22_and_line_30_follows_it() -> None:
    worksheet = return_ca()

    # Line 22 is 16995.00 - 1038.46 = 15956.54; line 24 is 15956.54 - 10475.63 = 5480.91, more than
    # line 29 (1973.29), so it is line 30 and the net federal tax.
    assert worksheet.get(SPLIT_INCOME_LINE_22).value == D("15956.54")
    assert worksheet.get(SPLIT_INCOME_LINE_24).value == D("5480.91")
    assert worksheet.get(SPLIT_INCOME_LINE_29).value == D("1973.29")
    assert worksheet.get(SPLIT_INCOME_LINE_30).value == D("5480.91")
    assert worksheet.get(NET_FEDERAL_TAX).value == D("5480.91")


def test_return_cas_ontario_line_49_is_the_non_business_share_of_on428_line_82() -> None:
    worksheet = return_ca()

    # T2036 line 3 is 15000 - 13094.54 = 1905.46 (line 4, 8595.89, is more), so ON428 line 82 is
    # 1905.46. T1206 line 49 is that x 40000 / 50000 = 1524.368, rounded half-up to the cent;
    # line 50 is 10229.53 - 1524.37 = 8705.16, more than ON428 line 88 (8324.07), so it is line 52.
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT).value == D("1905.46")
    assert worksheet.get(SPLIT_INCOME_NON_BUSINESS_FROM_FOREIGN_SOURCES).value == D("40000")
    assert worksheet.get(TOTAL_NON_BUSINESS_INCOME_FROM_FOREIGN_SOURCES).value == D("50000")
    assert worksheet.get(ontario.SPLIT_INCOME_LINE_47).value == D("10229.53")
    assert worksheet.get(ontario.SPLIT_INCOME_LINE_49).value == D("1524.37")
    assert worksheet.get(ontario.SPLIT_INCOME_LINE_50).value == D("8705.16")
    assert worksheet.get(ontario.ONTARIO_TAX_AFTER_FOOD_CREDIT).value == D("8324.07")
    assert worksheet.get(ontario.SPLIT_INCOME_LINE_52).value == D("8705.16")
    assert worksheet.get(ontario.ONTARIO_TAX).value == D("9305.16")
    assert worksheet.get(TOTAL_PAYABLE).value == D("14786.07")


def test_the_ontario_share_reads_its_own_non_business_figures() -> None:
    # 30000 of the 40000 is non-business income: line 49 is 1905.46 x 30000 / 50000 = 1143.276,
    # rounded half-up to the cent, while line 23 still uses lines 68370 and 68380.
    worksheet = return_ca(split_income_non_business_from_foreign_sources="30000")

    assert worksheet.get(SPLIT_INCOME_LINE_23).value == D("10475.63")
    assert worksheet.get(ontario.SPLIT_INCOME_LINE_49).value == D("1143.28")
    assert worksheet.get(ontario.SPLIT_INCOME_LINE_50).value == D("9086.25")


def test_all_the_split_income_from_foreign_sources_takes_the_whole_credit() -> None:
    worksheet = return_ca(
        split_income_from_foreign_sources="50000",
        split_income_non_business_from_foreign_sources="50000",
    )

    assert worksheet.get(SPLIT_INCOME_LINE_23).value == D("13094.54")
    assert worksheet.get(SPLIT_INCOME_LINE_24).value == D("2862.00")
    assert worksheet.get(ontario.SPLIT_INCOME_LINE_49).value == D("1905.46")
    assert worksheet.get(ontario.SPLIT_INCOME_LINE_50).value == D("8324.07")


def test_no_income_from_foreign_sources_gives_lines_23_and_49_of_zero() -> None:
    # With 0 on lines 68380 (total income from foreign sources) the shares are 0: the whole of
    # line 22 and of line 47 stands, as in Return AL, although the credits themselves are not 0.
    worksheet = return_ca(
        split_income_from_foreign_sources="0",
        total_income_from_foreign_sources="0",
        split_income_non_business_from_foreign_sources="0",
        total_non_business_income_from_foreign_sources="0",
    )

    assert worksheet.get(FEDERAL_FOREIGN_TAX_CREDIT).value == D("13094.54")
    assert worksheet.get(SPLIT_INCOME_LINE_23).value == D("0.00")
    assert worksheet.get(SPLIT_INCOME_LINE_24).value == D("15956.54")
    assert worksheet.get(ontario.PROVINCIAL_FOREIGN_TAX_CREDIT).value == D("1905.46")
    assert worksheet.get(ontario.SPLIT_INCOME_LINE_49).value == D("0.00")
    assert worksheet.get(ontario.SPLIT_INCOME_LINE_50).value == D("10229.53")


def test_line_24_is_not_below_zero_and_line_50_may_be() -> None:
    # 200000 of employment income and 1000 of other income that is all split income from foreign
    # sources, with 50000 of foreign income in all: line 8 is 330.00, so line 22 is 330.00; the
    # credit (10878.83) is all of it for line 23, so line 24 is 330.00 - 10878.83, entered as 0
    # ("if negative, enter "0""). Line 50 prints no floor: 205.30 - 4121.17 = -3915.87.
    worksheet = compute(
        "200000",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        other_income="1000",
        foreign_investment_income="49000",
        foreign_tax_countries_rows=(("15000", "50000"),),
        other_split_income="1000",
        split_income_from_foreign_sources="1000",
        total_income_from_foreign_sources="1000",
        split_income_non_business_from_foreign_sources="1000",
        total_non_business_income_from_foreign_sources="1000",
    )

    assert worksheet.get(SPLIT_INCOME_LINE_22).value == D("330.00")
    assert worksheet.get(SPLIT_INCOME_LINE_23).value == D("10878.83")
    assert worksheet.get(SPLIT_INCOME_LINE_24).value == D("0")
    assert worksheet.get(ontario.SPLIT_INCOME_LINE_47).value == D("205.30")
    assert worksheet.get(ontario.SPLIT_INCOME_LINE_49).value == D("4121.17")
    assert worksheet.get(ontario.SPLIT_INCOME_LINE_50).value == D("-3915.87")


def test_the_trace_records_lines_23_and_24_and_lines_49_and_50() -> None:
    trace = return_ca().trace

    assert (
        RatioAppliedLine(
            SPLIT_INCOME_LINE_23,
            FEDERAL_FOREIGN_TAX_CREDIT,
            D("13094.54"),
            SPLIT_INCOME_FROM_FOREIGN_SOURCES,
            D("40000"),
            TOTAL_INCOME_FROM_FOREIGN_SOURCES,
            D("50000"),
            CENT,
            D("10475.63"),
        )
        in trace
    )
    assert (
        SubtractedNotBelowZeroLine(
            output=SPLIT_INCOME_LINE_24,
            minuend=SPLIT_INCOME_LINE_22,
            minuend_amount=D("15956.54"),
            subtrahend=SPLIT_INCOME_LINE_23,
            subtrahend_amount=D("10475.63"),
            result=D("5480.91"),
        )
        in trace
    )
    assert (
        RatioAppliedLine(
            ontario.SPLIT_INCOME_LINE_49,
            ontario.PROVINCIAL_FOREIGN_TAX_CREDIT,
            D("1905.46"),
            SPLIT_INCOME_NON_BUSINESS_FROM_FOREIGN_SOURCES,
            D("40000"),
            TOTAL_NON_BUSINESS_INCOME_FROM_FOREIGN_SOURCES,
            D("50000"),
            CENT,
            D("1524.37"),
        )
        in trace
    )
    assert (
        SubtractedLine(
            output=ontario.SPLIT_INCOME_LINE_50,
            minuend=ontario.SPLIT_INCOME_LINE_47,
            minuend_amount=D("10229.53"),
            subtrahend=ontario.SPLIT_INCOME_LINE_49,
            subtrahend_amount=D("1524.37"),
            result=D("8705.16"),
        )
        in trace
    )


def test_the_english_trace_reads_lines_23_and_24_and_lines_49_and_50() -> None:
    rendered = EnglishTraceRenderer().render_all(return_ca().trace)

    for line in (
        "split_income_line_23: federal_foreign_tax_credit 13094.54 "
        "× split_income_from_foreign_sources 40000 / total_income_from_foreign_sources 50000 "
        "(half-up to 0.01)",
        "split_income_line_24: split_income_line_22 15956.54 less split_income_line_23 10475.63, "
        "not below 0 = 5480.91",
        "split_income_line_49: provincial_foreign_tax_credit 1905.46 "
        "× split_income_non_business_from_foreign_sources 40000 "
        "/ total_non_business_income_from_foreign_sources 50000 (half-up to 0.01)",
        "split_income_line_50: split_income_line_47 10229.53 less split_income_line_49 1524.37 "
        "= 8705.16",
    ):
        assert line in rendered, line
