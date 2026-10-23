"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.capabilities.apply_fraction import ApplyFraction
from app.domain.capabilities.apply_rate import ApplyRate
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.subtract_not_below_zero import SubtractNotBelowZero
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.sum_not_below_zero import SumNotBelowZero
from app.domain.manifest import CapabilitySelection
from app.jurisdictions.ca.capabilities.disposition_gains import DispositionGains
from app.jurisdictions.ca.capabilities.disposition_gains_only import DispositionGainsOnly
from app.jurisdictions.ca.capabilities.disposition_proceeds import DispositionProceeds
from app.jurisdictions.ca.capabilities.principal_residence_gain import PrincipalResidenceGain
from app.jurisdictions.ca.catalog import (
    AMT_MINIMUM_TAX_CARRYOVER_APPLIED,
    BOND_DISPOSITIONS,
    BOND_GAIN_OR_LOSS,
    BOND_PROCEEDS,
    BUSINESS_INCOME,
    BUSINESS_INVESTMENT_LOSS_REDUCTION,
    CAPITAL_GAIN,
    CAPITAL_GAINS_AFTER_DEFERRAL,
    CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION,
    CAPITAL_GAINS_BEFORE_RESERVES,
    CAPITAL_GAINS_DEFERRAL,
    CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES,
    CAPITAL_GAINS_RESERVES,
    COMMISSION_INCOME,
    CPP_OR_QPP_BENEFITS,
    CREDITS_AGAINST_BASIC_FEDERAL_TAX,
    CRYPTO_ASSET_DISPOSITIONS,
    CRYPTO_ASSET_GAIN_OR_LOSS,
    CRYPTO_ASSET_PROCEEDS,
    DIVIDEND_TAX_CREDIT,
    DIVIDENDS_AMOUNT_A,
    DIVIDENDS_AMOUNT_A_LESS_B,
    DIVIDENDS_AMOUNT_B,
    DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP,
    EI_AND_OTHER_BENEFITS,
    ELECTED_SPLIT_PENSION_AMOUNT,
    ELIGIBLE_DIVIDENDS_CREDIT,
    ELIGIBLE_DIVIDENDS_GROSSED_UP,
    ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    EMPLOYMENT_INCOME,
    FARMING_INCOME,
    FHSA_INCOME,
    FISHING_INCOME,
    FOREIGN_INVESTMENT_INCOME,
    INCLUDED_CAPITAL_GAIN,
    INCOME_SUPPORT_BENEFITS,
    INTEREST_AND_OTHER_INVESTMENT_INCOME,
    INVESTMENT_INCOME_BEFORE_PRIOR_YEARS,
    INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
    INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS,
    INVESTMENT_INCOME_WITHOUT_A_SLIP,
    INVESTMENT_ROYALTIES,
    LISTED_PERSONAL_PROPERTY_DISPOSITIONS,
    LISTED_PERSONAL_PROPERTY_GAIN_OR_LOSS,
    LISTED_PERSONAL_PROPERTY_NET_GAIN,
    NET_FEDERAL_SUPPLEMENTS,
    NET_PARTNERSHIP_INCOME,
    NET_RENTAL_INCOME,
    NET_SELF_EMPLOYMENT_INCOME,
    NO_SLIP_DIVIDEND_TAX_CREDIT,
    NON_REFUNDABLE_TAX_CREDITS,
    OLD_AGE_SECURITY,
    OTHER_DIVIDENDS_CREDIT,
    OTHER_DIVIDENDS_GROSSED_UP,
    OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP,
    OTHER_EMPLOYMENT_INCOME,
    OTHER_FHSA_INCOME,
    OTHER_FORECLOSURE_DISPOSITIONS,
    OTHER_FORECLOSURE_GAIN_OR_LOSS,
    OTHER_FORECLOSURE_PROCEEDS,
    OTHER_INCOME,
    OTHER_PENSIONS_AND_SUPERANNUATION,
    PARTNERSHIP_GAINS_AT_FULL_INCLUSION,
    PERSONAL_USE_PROPERTY_DISPOSITIONS,
    PERSONAL_USE_PROPERTY_GAIN,
    PERSONAL_USE_PROPERTY_GAIN_ROWS,
    PRINCIPAL_RESIDENCE_GAIN,
    PRINCIPAL_RESIDENCE_PROPERTIES,
    PROFESSIONAL_INCOME,
    QFFP_DISPOSITIONS,
    QFFP_FORECLOSURE_DISPOSITIONS,
    QFFP_FORECLOSURE_GAIN_OR_LOSS,
    QFFP_FORECLOSURE_PROCEEDS,
    QFFP_GAIN_OR_LOSS,
    QFFP_PROCEEDS,
    QSBCS_DISPOSITIONS,
    QSBCS_GAIN_OR_LOSS,
    QSBCS_PROCEEDS,
    RDSP_INCOME,
    REAL_ESTATE_DISPOSITIONS,
    REAL_ESTATE_GAIN_OR_LOSS,
    REAL_ESTATE_PROCEEDS,
    RRSP_INCOME,
    SHARE_DISPOSITIONS,
    SHARE_GAIN_OR_LOSS,
    SHARE_PROCEEDS,
    SLIP_CAPITAL_GAINS_OR_LOSSES,
    SLIP_DIVIDEND_TAX_CREDIT,
    SLIP_TAXABLE_DIVIDENDS,
    SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    SOCIAL_ASSISTANCE_PAYMENTS,
    T3_CAPITAL_GAINS_OR_LOSSES,
    T3_DIVIDEND_TAX_CREDIT,
    T3_INVESTMENT_INCOME,
    T3_TAXABLE_DIVIDENDS,
    T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    T4PS_DIVIDEND_TAX_CREDIT,
    T4PS_TAXABLE_DIVIDENDS,
    T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    T5_DIVIDEND_TAX_CREDIT,
    T5_INVESTMENT_INCOME,
    T5_TAXABLE_DIVIDENDS,
    T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    T5013_DIVIDEND_TAX_CREDIT,
    T5013_INVESTMENT_INCOME,
    T5013_TAXABLE_DIVIDENDS,
    T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TAX_REFUND_INTEREST,
    TAXABLE_CAPITAL_GAINS,
    TAXABLE_DIVIDENDS,
    TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
    TAXABLE_SCHOLARSHIPS,
    TAXABLE_SUPPORT_PAYMENTS,
    TOTAL_INCOME,
    UNAPPLIED_LISTED_PERSONAL_PROPERTY_LOSSES,
    UNIVERSAL_CHILD_CARE_BENEFIT,
    WORKERS_COMPENSATION_BENEFITS,
)

INPUTS = frozenset(
    {
        "ca/employment_income",
        # Schedule 3 Part 3 and Part 4: the ten property lists (lines 1 to 10), the unapplied
        # listed personal property losses, the properties sold (Form T2091(IND)), line 13
        # (16100), line 15 (17400), line 16 (17600) and line 20 (19200); line 21 (19700) is
        # computed.
        "ca/qsbcs_dispositions",
        "ca/qffp_dispositions",
        "ca/qffp_foreclosure_dispositions",
        "ca/share_dispositions",
        "ca/real_estate_dispositions",
        "ca/bond_dispositions",
        "ca/crypto_asset_dispositions",
        "ca/other_foreclosure_dispositions",
        "ca/personal_use_property_dispositions",
        "ca/listed_personal_property_dispositions",
        "ca/unapplied_listed_personal_property_losses",
        "ca/principal_residence_properties",
        "ca/capital_gains_deferral",
        "ca/slip_capital_gains_or_losses",
        "ca/t3_capital_gains_or_losses",
        "ca/capital_gains_reserves",
        # Schedule 3 Part 5 line 25 and line 19890: "Capital gains from certain dispositions of an
        # interest in a partnership subject to 100% inclusion rate (if negative, enter "0")", a
        # starting amount.
        "ca/partnership_gains_at_full_inclusion",
        "ca/other_employment_income",
        "ca/old_age_security",
        "ca/cpp_or_qpp_benefits",
        "ca/other_pensions_and_superannuation",
        "ca/elected_split_pension_amount",
        "ca/universal_child_care_benefit",
        "ca/ei_and_other_benefits",
        "ca/t3_taxable_dividends_other_than_eligible",
        "ca/t4ps_taxable_dividends_other_than_eligible",
        "ca/t5_taxable_dividends_other_than_eligible",
        "ca/t5013_taxable_dividends_other_than_eligible",
        "ca/t3_taxable_dividends",
        "ca/t4ps_taxable_dividends",
        "ca/t5_taxable_dividends",
        "ca/t5013_taxable_dividends",
        "ca/eligible_dividends_received_without_a_slip",
        "ca/other_dividends_received_without_a_slip",
        "ca/t3_dividend_tax_credit",
        "ca/t4ps_dividend_tax_credit",
        "ca/t5_dividend_tax_credit",
        "ca/t5013_dividend_tax_credit",
        "ca/t3_investment_income",
        "ca/t5_investment_income",
        "ca/t5013_investment_income",
        "ca/investment_income_credited_not_received",
        "ca/tax_refund_interest",
        "ca/foreign_investment_income",
        "ca/investment_income_without_a_slip",
        "ca/investment_royalties",
        "ca/investment_income_reported_in_previous_years",
        "ca/net_partnership_income",
        "ca/rdsp_income",
        "ca/taxable_support_payments",
        "ca/rrsp_income",
        "ca/fhsa_income",
        "ca/other_fhsa_income",
        "ca/other_income",
        "ca/taxable_scholarships",
        "ca/professional_income",
        "ca/commission_income",
        "ca/workers_compensation_benefits",
        "ca/social_assistance_payments",
        "ca/net_federal_supplements",
    }
)

OUTPUTS = frozenset(
    {
        "ca/taxable_dividends_other_than_eligible",
        # Schedule 3 Part 3: the eight "Total proceeds of disposition" lines feed no later line.
        "ca/qsbcs_proceeds",
        "ca/qffp_proceeds",
        "ca/qffp_foreclosure_proceeds",
        "ca/share_proceeds",
        "ca/real_estate_proceeds",
        "ca/bond_proceeds",
        "ca/crypto_asset_proceeds",
        "ca/other_foreclosure_proceeds",
    }
)

STEPS = {
    # Schedule 3 (form 5000-S3) Part 3: "For each Gain or loss enter as many lines as necessary."
    # Each property type lists one row per disposition: "(Column 2): Proceeds of disposition",
    # "(Column 3): Adjusted cost base", "(Column 4): Outlays and expenses", "(Column 5): Gain or
    # loss (column 2 minus columns 3 and 4)"; lines 1 to 8 (10700, 11000, 12400, 13200, 13800,
    # 15300, 15301, 15500) are each "Total gain or loss (add all the amounts under column 5)",
    # one step each.
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/qsbcs_dispositions"},
        produces={"output": "ca/qsbcs_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/qffp_dispositions"},
        produces={"output": "ca/qffp_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/qffp_foreclosure_dispositions"},
        produces={"output": "ca/qffp_foreclosure_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/share_dispositions"},
        produces={"output": "ca/share_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/real_estate_dispositions"},
        produces={"output": "ca/real_estate_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/bond_dispositions"},
        produces={"output": "ca/bond_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/crypto_asset_dispositions"},
        produces={"output": "ca/crypto_asset_gain_or_loss"},
    ),
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/other_foreclosure_dispositions"},
        produces={"output": "ca/other_foreclosure_gain_or_loss"},
    ),
    # Schedule 3 Part 3: lines 1 to 8 (10699, 10999, 12399, 13199, 13599, 15199, 15200, 15499) are
    # each "Total proceeds of disposition (add all the amounts under column 2)", one step each; the
    # totals feed no later line.
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/qsbcs_dispositions"},
        produces={"output": "ca/qsbcs_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/qffp_dispositions"},
        produces={"output": "ca/qffp_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/qffp_foreclosure_dispositions"},
        produces={"output": "ca/qffp_foreclosure_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/share_dispositions"},
        produces={"output": "ca/share_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/real_estate_dispositions"},
        produces={"output": "ca/real_estate_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/bond_dispositions"},
        produces={"output": "ca/bond_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/crypto_asset_dispositions"},
        produces={"output": "ca/crypto_asset_proceeds"},
    ),
    CapabilitySelection(
        name="ca/disposition_proceeds",
        params={},
        consumes={"dispositions": "ca/other_foreclosure_dispositions"},
        produces={"output": "ca/other_foreclosure_proceeds"},
    ),
    # Form T2091(IND) Part 1 and Part 3, one form for each property sold: "Divide line 21 by line
    # 22." (line 23, the exempt part, rounded half up to the cent), "Line 18 minus line 23 (if
    # negative, enter "0")" (line 24) and "Total capital gain" (line 54, which is line 24 when
    # Part 2 is not completed), added over the properties.
    CapabilitySelection(
        name="ca/principal_residence_gain",
        params={"rounding": "ca/principal_residence_gain_rounding"},
        consumes={"properties": "ca/principal_residence_properties"},
        produces={"output": "ca/principal_residence_gain"},
    ),
    # Part 3, Personal-use property: "Line 9 and line 15800: Total gain only (add all the amounts
    # under column 5)": the rows' gains, a row's loss counting 0, then line 9 itself, a sum of
    # those rows and line 54 of T2091(IND) ("enter the amount from line 54 above on line 15800 of
    # Schedule 3").
    CapabilitySelection(
        name="ca/disposition_gains_only",
        params={},
        consumes={"dispositions": "ca/personal_use_property_dispositions"},
        produces={"output": "ca/personal_use_property_gain_rows"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/personal_use_property_gain_rows", "ca/principal_residence_gain")},
        produces={"output": "ca/personal_use_property_gain"},
    ),
    # Part 3, Listed personal property: the rows' gains and losses (column 5) added, then line 10
    # and line 15900 "Net gain only": that total less the unapplied listed personal property
    # losses from other years, not below zero.
    CapabilitySelection(
        name="ca/disposition_gains",
        params={},
        consumes={"dispositions": "ca/listed_personal_property_dispositions"},
        produces={"output": "ca/listed_personal_property_gain_or_loss"},
    ),
    CapabilitySelection(
        name="core/subtract_not_below_zero",
        params={},
        consumes={
            "amount": "ca/listed_personal_property_gain_or_loss",
            "less": "ca/unapplied_listed_personal_property_losses",
        },
        produces={"output": "ca/listed_personal_property_net_gain"},
    ),
    # Part 3 "Line 11: Add lines 1 to 10. Total gains or losses of qualified properties and
    # other properties ="; Part 4 "Line 12: Amount from line 11 of the previous page" is the same
    # artifact, so it has no step of its own.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/qsbcs_gain_or_loss",
                "ca/qffp_gain_or_loss",
                "ca/qffp_foreclosure_gain_or_loss",
                "ca/share_gain_or_loss",
                "ca/real_estate_gain_or_loss",
                "ca/bond_gain_or_loss",
                "ca/crypto_asset_gain_or_loss",
                "ca/other_foreclosure_gain_or_loss",
                "ca/personal_use_property_gain",
                "ca/listed_personal_property_net_gain",
            )
        },
        produces={"output": "ca/capital_gains_of_qualified_and_other_properties"},
    ),
    # Part 4 "Line 14: Line 12 minus line 13 =" (line 13 and line 16100 is an input).
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/capital_gains_of_qualified_and_other_properties",
            "less": "ca/capital_gains_deferral",
        },
        produces={"output": "ca/capital_gains_after_deferral"},
    ),
    # Part 4 "Line 17: Add lines 14 to 16. =" (lines 15 and 16, 17400 and 17600, are inputs).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/capital_gains_after_deferral",
                "ca/slip_capital_gains_or_losses",
                "ca/t3_capital_gains_or_losses",
            )
        },
        produces={"output": "ca/capital_gains_before_investment_loss_reduction"},
    ),
    # Part 4 "Line 19 and line 19100: Total gains or losses before reserves: line 17 minus line
    # 18 =" (line 18 and line 17800 is the business investment loss reduction already computed).
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/capital_gains_before_investment_loss_reduction",
            "less": "ca/business_investment_loss_reduction",
        },
        produces={"output": "ca/capital_gains_before_reserves"},
    ),
    # Part 4 "Line 21 and line 19700: Line 19 plus line 20 Total capital gains or losses =" (line
    # 20 and line 19200, the reserves, is an input).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/capital_gains_before_reserves", "ca/capital_gains_reserves")},
        produces={"output": "ca/capital_gain"},
    ),
    # Part 5 line 22 is the same artifact as line 21; line 24 "Line 22 multiplied by the
    # percentage on line 23" (signed, the included capital gain), then line 26 and line 19900
    # "Line 24 plus line 25 If positive, enter the result on line 12700 of your return": line 24
    # and line 25 (the partnership gains at full inclusion, a caller input) as the parts of a sum
    # not below zero, so the taxable capital gains stay non-negative.
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/capital_gains_inclusion_rate"},
        consumes={"base": "ca/capital_gain"},
        produces={"output": "ca/included_capital_gain"},
    ),
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={"parts": ("ca/included_capital_gain", "ca/partnership_gains_at_full_inclusion")},
        produces={"output": "ca/taxable_capital_gains"},
    ),
    # T1 line 9 (12000) "Amount of dividends (eligible and other than eligible)" and line
    # 12010 "Amount of dividends (other than eligible)" (use Federal Worksheet): the Federal
    # Worksheet's "Lines 12000 and 12010 - Taxable amount of dividends from taxable Canadian
    # corporations", line 5 "Add lines 1 to 4. Enter this amount on line 12010 of your
    # return." (the T3, T4PS, T5 and T5013 slip boxes of lines 1 to 4) and line 10 "Add lines
    # 6 to 9. Enter this amount on line 12000 of your return." (lines 6 to 9). For dividends
    # with no information slip, line 11 "Actual amount of eligible dividends received" and
    # line 12 "Applicable rate 138%" give line 13 "Line 11 multiplied by the percentage from
    # line 12"; line 14 "Actual amount of dividends other than eligible dividends received"
    # and line 15 "Applicable rate 115%" give line 16 "Line 14 multiplied by the percentage
    # from line 15 Include this amount on line 12010 of your return."; line 17 "Line 13 plus
    # line 16. Include this amount on line 12000 of your return." The rates are above one, so
    # they are fractions, not rates. Line 12010 is line 5 plus line 16 and line 12000 is line
    # 10 plus line 17.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/t3_taxable_dividends_other_than_eligible",
                "ca/t4ps_taxable_dividends_other_than_eligible",
                "ca/t5_taxable_dividends_other_than_eligible",
                "ca/t5013_taxable_dividends_other_than_eligible",
            )
        },
        produces={"output": "ca/slip_taxable_dividends_other_than_eligible"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/t3_taxable_dividends",
                "ca/t4ps_taxable_dividends",
                "ca/t5_taxable_dividends",
                "ca/t5013_taxable_dividends",
            )
        },
        produces={"output": "ca/slip_taxable_dividends"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/eligible_dividend_gross_up"},
        consumes={"base": "ca/eligible_dividends_received_without_a_slip"},
        produces={"output": "ca/eligible_dividends_grossed_up"},
    ),
    CapabilitySelection(
        name="core/apply_fraction",
        params={"fraction": "ca/other_dividend_gross_up"},
        consumes={"base": "ca/other_dividends_received_without_a_slip"},
        produces={"output": "ca/other_dividends_grossed_up"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/eligible_dividends_grossed_up", "ca/other_dividends_grossed_up")},
        produces={"output": "ca/dividends_without_a_slip_grossed_up"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/slip_taxable_dividends_other_than_eligible",
                "ca/other_dividends_grossed_up",
            )
        },
        produces={"output": "ca/taxable_dividends_other_than_eligible"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/slip_taxable_dividends", "ca/dividends_without_a_slip_grossed_up")},
        produces={"output": "ca/taxable_dividends"},
    ),
    # T1 Step 2 line 10 (12100) "Interest and other investment income (use Federal
    # Worksheet)": the Federal Worksheet's "Line 12100 - Interest and other investment
    # income" line 9 "Add lines 1 to 8.", in line order, then line 11 "Line 9 minus line
    # 10. Enter this amount on line 12100 of your return." with line 10 "Interest and other
    # investment income, included on line 9, received and reported in previous years".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/t3_investment_income",
                "ca/t5_investment_income",
                "ca/t5013_investment_income",
                "ca/investment_income_credited_not_received",
                "ca/tax_refund_interest",
                "ca/foreign_investment_income",
                "ca/investment_income_without_a_slip",
                "ca/investment_royalties",
            )
        },
        produces={"output": "ca/investment_income_before_prior_years"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/investment_income_before_prior_years",
            "less": "ca/investment_income_reported_in_previous_years",
        },
        produces={"output": "ca/interest_and_other_investment_income"},
    ),
    # T1 line 32 and line 14700 "Add lines 29 to 31 (see line 25000 in Step 4).": workers'
    # compensation benefits (14400), social assistance payments (14500) and net federal
    # supplements paid (14600), in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/workers_compensation_benefits",
                "ca/social_assistance_payments",
                "ca/net_federal_supplements",
            )
        },
        produces={"output": "ca/income_support_benefits"},
    ),
    # T1 line 33 and line 15000 "Line 28 plus line 32 Total income": every income line
    # the return lists, in line order (lines 1 to 20, line 13 being the net rental
    # income, line 12600 "Net"; here with the amount of dividends of line 9 (12000), the
    # taxable capital gains of line 14 and the taxable support payments of line 15, then
    # line 32); line 27 "Add lines 22 to 26. Net self-employment income" (line 28 is line 21 plus
    # line 27) comes after line 20, before lines 29 to 31 (line 32).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/employment_income",
                "ca/other_employment_income",
                "ca/old_age_security",
                "ca/cpp_or_qpp_benefits",
                "ca/other_pensions_and_superannuation",
                "ca/elected_split_pension_amount",
                "ca/universal_child_care_benefit",
                "ca/ei_and_other_benefits",
                "ca/taxable_dividends",
                "ca/interest_and_other_investment_income",
                "ca/net_partnership_income",
                "ca/rdsp_income",
                "ca/net_rental_income",
                "ca/taxable_capital_gains",
                "ca/taxable_support_payments",
                "ca/rrsp_income",
                "ca/fhsa_income",
                "ca/other_fhsa_income",
                "ca/other_income",
                "ca/taxable_scholarships",
                "ca/net_self_employment_income",
                "ca/income_support_benefits",
            )
        },
        produces={"output": "ca/total_income"},
    ),
    # T1 line 123 (40425) "Federal dividend tax credit (use Federal Worksheet)": the Federal
    # Worksheet's "Line 40425 - Federal dividend tax credit", line 5 "Add lines 1 to 4." of
    # the credits shown on the T3, T4PS, T5 and T5013 slips. For dividends with no
    # information slip, line A "Amount from line 12000 of your return (Note 1)" and line B
    # "Amount from line 12010 of your return (Note 1)", Note 1 being "Enter only the amount
    # of dividends that were not shown on an information slip.", so line A is the
    # Worksheet's line 17 and line B its line 16, each its own step; line 6 is "Line B,
    # multiplied by 9.0301%"; line C is "Amount A minus amount B", and line 7 (printed
    # "Line 2") is line C "multiplied by 15.0198%"; line 8 is "Line 6 plus line 7" and
    # line 9 "Line 5 plus line 8 Enter this amount on line 40425 of your return."
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/t3_dividend_tax_credit",
                "ca/t4ps_dividend_tax_credit",
                "ca/t5_dividend_tax_credit",
                "ca/t5013_dividend_tax_credit",
            )
        },
        produces={"output": "ca/slip_dividend_tax_credit"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/dividends_without_a_slip_grossed_up",)},
        produces={"output": "ca/dividends_amount_a"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/other_dividends_grossed_up",)},
        produces={"output": "ca/dividends_amount_b"},
    ),
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/dividend_credit_rate_other_than_eligible"},
        consumes={"base": "ca/dividends_amount_b"},
        produces={"output": "ca/other_dividends_credit"},
    ),
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/dividends_amount_a", "less": "ca/dividends_amount_b"},
        produces={"output": "ca/dividends_amount_a_less_b"},
    ),
    CapabilitySelection(
        name="core/apply_rate",
        params={"rate": "ca/dividend_credit_rate_eligible"},
        consumes={"base": "ca/dividends_amount_a_less_b"},
        produces={"output": "ca/eligible_dividends_credit"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/other_dividends_credit", "ca/eligible_dividends_credit")},
        produces={"output": "ca/no_slip_dividend_tax_credit"},
    ),
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={"parts": ("ca/slip_dividend_tax_credit", "ca/no_slip_dividend_tax_credit")},
        produces={"output": "ca/dividend_tax_credit"},
    ),
    # T1 line 125 "Add lines 122 to 124.": line 122 "Amount from line 35000", line 123 (40425),
    # the federal dividend tax credit, and line 124 (40427), the minimum tax carryover applied
    # on Form T691 Part 8 line 12, in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/non_refundable_tax_credits",
                "ca/dividend_tax_credit",
                "ca/amt_minimum_tax_carryover_applied",
            )
        },
        produces={"output": "ca/credits_against_basic_federal_tax"},
    ),
    # T1 line 27 "Add lines 22 to 26. Net self-employment income": line 22 (13500) business
    # income, line 23 (13700) professional income, line 24 (13900) commission income, line 25
    # (14100) farming income and line 26 (14300) fishing income, the "Net" box of each, in line
    # order. Line 28 "Line 21 plus line 27" is not a step of its own: total income (line 15000)
    # adds line 27 to the lines 1 to 20, in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/business_income",
                "ca/professional_income",
                "ca/commission_income",
                "ca/farming_income",
                "ca/fishing_income",
            ),
        },
        produces={"output": "ca/net_self_employment_income"},
    ),
}

WIRING = {
    (ApplyRate, frozenset({CAPITAL_GAIN}), frozenset({INCLUDED_CAPITAL_GAIN})),
    (
        SumNotBelowZero,
        frozenset({INCLUDED_CAPITAL_GAIN, PARTNERSHIP_GAINS_AT_FULL_INCLUSION}),
        frozenset({TAXABLE_CAPITAL_GAINS}),
    ),
    (DispositionGains, frozenset({QSBCS_DISPOSITIONS}), frozenset({QSBCS_GAIN_OR_LOSS})),
    (DispositionGains, frozenset({QFFP_DISPOSITIONS}), frozenset({QFFP_GAIN_OR_LOSS})),
    (
        DispositionGains,
        frozenset({QFFP_FORECLOSURE_DISPOSITIONS}),
        frozenset({QFFP_FORECLOSURE_GAIN_OR_LOSS}),
    ),
    (DispositionGains, frozenset({SHARE_DISPOSITIONS}), frozenset({SHARE_GAIN_OR_LOSS})),
    (
        DispositionGains,
        frozenset({REAL_ESTATE_DISPOSITIONS}),
        frozenset({REAL_ESTATE_GAIN_OR_LOSS}),
    ),
    (DispositionGains, frozenset({BOND_DISPOSITIONS}), frozenset({BOND_GAIN_OR_LOSS})),
    (
        DispositionGains,
        frozenset({CRYPTO_ASSET_DISPOSITIONS}),
        frozenset({CRYPTO_ASSET_GAIN_OR_LOSS}),
    ),
    (
        DispositionGains,
        frozenset({OTHER_FORECLOSURE_DISPOSITIONS}),
        frozenset({OTHER_FORECLOSURE_GAIN_OR_LOSS}),
    ),
    (
        DispositionProceeds,
        frozenset({QSBCS_DISPOSITIONS}),
        frozenset({QSBCS_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({QFFP_DISPOSITIONS}),
        frozenset({QFFP_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({QFFP_FORECLOSURE_DISPOSITIONS}),
        frozenset({QFFP_FORECLOSURE_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({SHARE_DISPOSITIONS}),
        frozenset({SHARE_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({REAL_ESTATE_DISPOSITIONS}),
        frozenset({REAL_ESTATE_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({BOND_DISPOSITIONS}),
        frozenset({BOND_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({CRYPTO_ASSET_DISPOSITIONS}),
        frozenset({CRYPTO_ASSET_PROCEEDS}),
    ),
    (
        DispositionProceeds,
        frozenset({OTHER_FORECLOSURE_DISPOSITIONS}),
        frozenset({OTHER_FORECLOSURE_PROCEEDS}),
    ),
    (
        DispositionGainsOnly,
        frozenset({PERSONAL_USE_PROPERTY_DISPOSITIONS}),
        frozenset({PERSONAL_USE_PROPERTY_GAIN_ROWS}),
    ),
    (
        PrincipalResidenceGain,
        frozenset({PRINCIPAL_RESIDENCE_PROPERTIES}),
        frozenset({PRINCIPAL_RESIDENCE_GAIN}),
    ),
    (
        Sum,
        frozenset({PERSONAL_USE_PROPERTY_GAIN_ROWS, PRINCIPAL_RESIDENCE_GAIN}),
        frozenset({PERSONAL_USE_PROPERTY_GAIN}),
    ),
    (
        DispositionGains,
        frozenset({LISTED_PERSONAL_PROPERTY_DISPOSITIONS}),
        frozenset({LISTED_PERSONAL_PROPERTY_GAIN_OR_LOSS}),
    ),
    (
        SubtractNotBelowZero,
        frozenset(
            {LISTED_PERSONAL_PROPERTY_GAIN_OR_LOSS, UNAPPLIED_LISTED_PERSONAL_PROPERTY_LOSSES}
        ),
        frozenset({LISTED_PERSONAL_PROPERTY_NET_GAIN}),
    ),
    (
        Sum,
        frozenset(
            {
                QSBCS_GAIN_OR_LOSS,
                QFFP_GAIN_OR_LOSS,
                QFFP_FORECLOSURE_GAIN_OR_LOSS,
                SHARE_GAIN_OR_LOSS,
                REAL_ESTATE_GAIN_OR_LOSS,
                BOND_GAIN_OR_LOSS,
                CRYPTO_ASSET_GAIN_OR_LOSS,
                OTHER_FORECLOSURE_GAIN_OR_LOSS,
                PERSONAL_USE_PROPERTY_GAIN,
                LISTED_PERSONAL_PROPERTY_NET_GAIN,
            }
        ),
        frozenset({CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES}),
    ),
    (
        Subtract,
        frozenset({CAPITAL_GAINS_OF_QUALIFIED_AND_OTHER_PROPERTIES, CAPITAL_GAINS_DEFERRAL}),
        frozenset({CAPITAL_GAINS_AFTER_DEFERRAL}),
    ),
    (
        Sum,
        frozenset(
            {CAPITAL_GAINS_AFTER_DEFERRAL, SLIP_CAPITAL_GAINS_OR_LOSSES, T3_CAPITAL_GAINS_OR_LOSSES}
        ),
        frozenset({CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION}),
    ),
    (
        Subtract,
        frozenset(
            {CAPITAL_GAINS_BEFORE_INVESTMENT_LOSS_REDUCTION, BUSINESS_INVESTMENT_LOSS_REDUCTION}
        ),
        frozenset({CAPITAL_GAINS_BEFORE_RESERVES}),
    ),
    (
        Sum,
        frozenset({CAPITAL_GAINS_BEFORE_RESERVES, CAPITAL_GAINS_RESERVES}),
        frozenset({CAPITAL_GAIN}),
    ),
    (
        Sum,
        frozenset(
            {
                T3_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                T4PS_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                T5_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
                T5013_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE,
            }
        ),
        frozenset({SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
    ),
    (
        Sum,
        frozenset(
            {
                T3_TAXABLE_DIVIDENDS,
                T4PS_TAXABLE_DIVIDENDS,
                T5_TAXABLE_DIVIDENDS,
                T5013_TAXABLE_DIVIDENDS,
            }
        ),
        frozenset({SLIP_TAXABLE_DIVIDENDS}),
    ),
    (
        ApplyFraction,
        frozenset({ELIGIBLE_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP}),
        frozenset({ELIGIBLE_DIVIDENDS_GROSSED_UP}),
    ),
    (
        ApplyFraction,
        frozenset({OTHER_DIVIDENDS_RECEIVED_WITHOUT_A_SLIP}),
        frozenset({OTHER_DIVIDENDS_GROSSED_UP}),
    ),
    (
        Sum,
        frozenset({ELIGIBLE_DIVIDENDS_GROSSED_UP, OTHER_DIVIDENDS_GROSSED_UP}),
        frozenset({DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP}),
    ),
    (
        Sum,
        frozenset({SLIP_TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE, OTHER_DIVIDENDS_GROSSED_UP}),
        frozenset({TAXABLE_DIVIDENDS_OTHER_THAN_ELIGIBLE}),
    ),
    (
        Sum,
        frozenset({SLIP_TAXABLE_DIVIDENDS, DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP}),
        frozenset({TAXABLE_DIVIDENDS}),
    ),
    (
        Sum,
        frozenset(
            {
                T3_INVESTMENT_INCOME,
                T5_INVESTMENT_INCOME,
                T5013_INVESTMENT_INCOME,
                INVESTMENT_INCOME_CREDITED_NOT_RECEIVED,
                TAX_REFUND_INTEREST,
                FOREIGN_INVESTMENT_INCOME,
                INVESTMENT_INCOME_WITHOUT_A_SLIP,
                INVESTMENT_ROYALTIES,
            }
        ),
        frozenset({INVESTMENT_INCOME_BEFORE_PRIOR_YEARS}),
    ),
    (
        Subtract,
        frozenset(
            {INVESTMENT_INCOME_BEFORE_PRIOR_YEARS, INVESTMENT_INCOME_REPORTED_IN_PREVIOUS_YEARS}
        ),
        frozenset({INTEREST_AND_OTHER_INVESTMENT_INCOME}),
    ),
    (
        Sum,
        frozenset(
            {WORKERS_COMPENSATION_BENEFITS, SOCIAL_ASSISTANCE_PAYMENTS, NET_FEDERAL_SUPPLEMENTS}
        ),
        frozenset({INCOME_SUPPORT_BENEFITS}),
    ),
    (
        Sum,
        frozenset(
            {
                EMPLOYMENT_INCOME,
                OTHER_EMPLOYMENT_INCOME,
                OLD_AGE_SECURITY,
                CPP_OR_QPP_BENEFITS,
                OTHER_PENSIONS_AND_SUPERANNUATION,
                ELECTED_SPLIT_PENSION_AMOUNT,
                UNIVERSAL_CHILD_CARE_BENEFIT,
                EI_AND_OTHER_BENEFITS,
                TAXABLE_DIVIDENDS,
                INTEREST_AND_OTHER_INVESTMENT_INCOME,
                NET_PARTNERSHIP_INCOME,
                RDSP_INCOME,
                NET_RENTAL_INCOME,
                TAXABLE_CAPITAL_GAINS,
                TAXABLE_SUPPORT_PAYMENTS,
                RRSP_INCOME,
                FHSA_INCOME,
                OTHER_FHSA_INCOME,
                OTHER_INCOME,
                TAXABLE_SCHOLARSHIPS,
                NET_SELF_EMPLOYMENT_INCOME,
                INCOME_SUPPORT_BENEFITS,
            }
        ),
        frozenset({TOTAL_INCOME}),
    ),
    (
        Sum,
        frozenset(
            {
                T3_DIVIDEND_TAX_CREDIT,
                T4PS_DIVIDEND_TAX_CREDIT,
                T5_DIVIDEND_TAX_CREDIT,
                T5013_DIVIDEND_TAX_CREDIT,
            }
        ),
        frozenset({SLIP_DIVIDEND_TAX_CREDIT}),
    ),
    (
        Sum,
        frozenset({DIVIDENDS_WITHOUT_A_SLIP_GROSSED_UP}),
        frozenset({DIVIDENDS_AMOUNT_A}),
    ),
    (Sum, frozenset({OTHER_DIVIDENDS_GROSSED_UP}), frozenset({DIVIDENDS_AMOUNT_B})),
    (ApplyRate, frozenset({DIVIDENDS_AMOUNT_B}), frozenset({OTHER_DIVIDENDS_CREDIT})),
    (
        Subtract,
        frozenset({DIVIDENDS_AMOUNT_A, DIVIDENDS_AMOUNT_B}),
        frozenset({DIVIDENDS_AMOUNT_A_LESS_B}),
    ),
    (
        ApplyRate,
        frozenset({DIVIDENDS_AMOUNT_A_LESS_B}),
        frozenset({ELIGIBLE_DIVIDENDS_CREDIT}),
    ),
    (
        Sum,
        frozenset({OTHER_DIVIDENDS_CREDIT, ELIGIBLE_DIVIDENDS_CREDIT}),
        frozenset({NO_SLIP_DIVIDEND_TAX_CREDIT}),
    ),
    (
        Sum,
        frozenset({SLIP_DIVIDEND_TAX_CREDIT, NO_SLIP_DIVIDEND_TAX_CREDIT}),
        frozenset({DIVIDEND_TAX_CREDIT}),
    ),
    (
        Sum,
        frozenset(
            {NON_REFUNDABLE_TAX_CREDITS, DIVIDEND_TAX_CREDIT, AMT_MINIMUM_TAX_CARRYOVER_APPLIED}
        ),
        frozenset({CREDITS_AGAINST_BASIC_FEDERAL_TAX}),
    ),
    (
        Sum,
        frozenset(
            {
                BUSINESS_INCOME,
                PROFESSIONAL_INCOME,
                COMMISSION_INCOME,
                FARMING_INCOME,
                FISHING_INCOME,
            }
        ),
        frozenset({NET_SELF_EMPLOYMENT_INCOME}),
    ),
}
