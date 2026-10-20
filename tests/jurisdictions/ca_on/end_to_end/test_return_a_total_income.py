"""CA-ON 2025 end to end: return a total income."""

from __future__ import annotations

import pytest

from app.adapters.inbound.trace_english import EnglishTraceRenderer
from app.domain.errors import CapabilityContractError
from app.jurisdictions.ca.catalog import (
    INCOME_SUPPORT_BENEFITS,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    TAXABLE_CAPITAL_GAINS,
    TOTAL_INCOME,
)
from tests.jurisdictions.ca_on.end_to_end.support import D, compute


def test_the_interest_and_other_investment_income_is_the_worksheets_line_9_less_line_10() -> None:
    # The Federal Worksheet's "Line 12100 - Interest and other investment income": line 2 (the T5
    # boxes) 1200 and line 7 (bank interest with no slip) 300 add to line 9 "Add lines 1 to 8."
    # of 1500; line 10 (reported in previous years) 100 comes off it: line 11, and so line
    # 12100, is 1400.
    worksheet = compute(
        "0",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        t5_investment_income="1200",
        investment_income_without_a_slip="300",
        investment_income_reported_in_previous_years="100",
    )

    assert worksheet.get(INVESTMENT_INCOME_BEFORE_PRIOR_YEARS).value == D("1500")
    assert worksheet.get(INTEREST_AND_OTHER_INVESTMENT_INCOME).value == D("1400")
    assert worksheet.get(TOTAL_INCOME).value == D("1400")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "investment_income_before_prior_years: t3_investment_income 0 + t5_investment_income 1200 "
        "+ t5013_investment_income 0 + investment_income_credited_not_received 0 "
        "+ tax_refund_interest 0 + foreign_investment_income 0 "
        "+ investment_income_without_a_slip 300 + investment_royalties 0 = 1500"
    ) in rendered
    assert (
        "interest_and_other_investment_income: investment_income_before_prior_years 1500 "
        "less investment_income_reported_in_previous_years 100 = 1400"
    ) in rendered


def test_prior_year_investment_income_above_line_9_is_refused_as_a_negative_line_11() -> None:
    # The Federal Worksheet's line 10 (reported in previous years) of 200 is more than line 9 of
    # 150, so line 11 "Line 9 minus line 10", and so line 12100, would be negative; the kind
    # cannot be below zero, so the capability's output breaks its contract.
    with pytest.raises(
        CapabilityContractError,
        match="ca/interest_and_other_investment_income -50, which cannot be negative",
    ):
        compute(
            "0",
            (),
            "0",
            "0",
            "0",
            "0",
            "0",
            t5_investment_income="150",
            investment_income_reported_in_previous_years="200",
        )


def test_each_of_the_worksheets_lines_1_to_8_adds_to_line_9() -> None:
    # Distinct amounts, one per line, so a line left out or added twice changes the sum: 1 + 2 +
    # 4 + 8 + 16 + 32 + 64 + 128 = 255, and line 10 of 5 leaves 250.
    worksheet = compute(
        "0",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        t3_investment_income="1",
        t5_investment_income="2",
        t5013_investment_income="4",
        investment_income_credited_not_received="8",
        tax_refund_interest="16",
        foreign_investment_income="32",
        investment_income_without_a_slip="64",
        investment_royalties="128",
        investment_income_reported_in_previous_years="5",
    )

    assert worksheet.get(INVESTMENT_INCOME_BEFORE_PRIOR_YEARS).value == D("255")
    assert worksheet.get(INTEREST_AND_OTHER_INVESTMENT_INCOME).value == D("250")


def test_line_14700_adds_lines_29_to_31() -> None:
    # T1 line 32 and line 14700 "Add lines 29 to 31 (see line 25000 in Step 4).": the workers'
    # compensation benefits (14400), the social assistance payments (14500) and the net federal
    # supplements (14600), 2000 + 300 + 40 = 2340, which line 15000 adds.
    worksheet = compute(
        "0",
        (),
        "0",
        "0",
        "0",
        "0",
        "0",
        workers_compensation_benefits="2000",
        social_assistance_payments="300",
        net_federal_supplements="40",
    )

    assert worksheet.get(INCOME_SUPPORT_BENEFITS).value == D("2340")
    assert worksheet.get(TOTAL_INCOME).value == D("2340")
    rendered = EnglishTraceRenderer().render_all(worksheet.trace)
    assert (
        "income_support_benefits: workers_compensation_benefits 2000 "
        "+ social_assistance_payments 300 + net_federal_supplements 40 = 2340"
    ) in rendered


def test_total_income_adds_every_income_line_once() -> None:
    # T1 line 33 and line 15000 "Line 28 plus line 32 Total income": one distinct power of two
    # for each of the nineteen amounts that enter it, so a line left out or added twice changes
    # the total: 2^0 + ... + 2^18 = 524287. Employment income 1 (line 10100), other employment
    # income 2 (10400), OAS 4 (11300), CPP benefits 8 (11400), other pensions 16 (11500),
    # elected split-pension amount 32 (11600), UCCB 64 (11700), EI 128 (11900), interest and
    # other investment income 256 (12100, from the T5 slips), net partnership income 512
    # (12200), RDSP income 1024 (12500), taxable capital gains 2048 (12700, 50% of a capital
    # gain of 4096), taxable support payments 4096 (12800), RRSP income 8192 (12900), FHSA
    # income 16384 (12905), taxable FHSA income - other 32768 (12906), other income 65536
    # (13000), scholarships 131072 (13010) and the lines 14400 to 14600 of 262144 (14700).
    worksheet = compute(
        "1",
        (("4096", "0", "0"),),
        "0",
        "0",
        "0",
        "0",
        "0",
        other_employment_income="2",
        old_age_security="4",
        cpp_or_qpp_benefits="8",
        other_pensions_and_superannuation="16",
        elected_split_pension_amount="32",
        universal_child_care_benefit="64",
        ei_and_other_benefits="128",
        t5_investment_income="256",
        net_partnership_income="512",
        rdsp_income="1024",
        taxable_support_payments="4096",
        rrsp_income="8192",
        fhsa_income="16384",
        other_fhsa_income="32768",
        other_income="65536",
        taxable_scholarships="131072",
        workers_compensation_benefits="262144",
    )

    assert worksheet.get(TAXABLE_CAPITAL_GAINS).value == D("2048.00")
    assert worksheet.get(INTEREST_AND_OTHER_INVESTMENT_INCOME).value == D("256")
    assert worksheet.get(INCOME_SUPPORT_BENEFITS).value == D("262144")
    assert worksheet.get(TOTAL_INCOME).value == D("524287")
