"""The CA-ON manifest entries of Form T776 (see `test_manifest.py` and `test_manifest_t776.py`).

T776 is a form of the manifest: its 45 selections belong to the form `ca/t776` (`FORM_STEPS`), run
once for each statement of `ca/t776_statements`, whose fields are the T776 inputs (`FORM_INPUTS`).
The form exports seven artifacts, each readable by the other forms as `ca/t776.<export>`
(`FORM_EXPORTS`); the return reads one and declares no output for the six nothing reads (`OUTPUTS`
is empty). The return's own entries are the instances input, the total of the net income over the
statements that is T1 line 12600 (`STEPS` and `WIRING`).
"""

from __future__ import annotations

from app.domain.capabilities.at_most import AtMost
from app.domain.capabilities.choose_by_count import ChooseByCount
from app.domain.capabilities.credit_amount import CreditAmount
from app.domain.capabilities.record_total import RecordTotal
from app.domain.capabilities.subtract import Subtract
from app.domain.capabilities.sum import Sum
from app.domain.capabilities.sum_not_below_zero import SumNotBelowZero
from app.domain.capabilities.times_count import TimesCount
from app.domain.manifest import CapabilitySelection
from app.domain.record_list import RecordListKind
from app.jurisdictions.ca.capabilities.apply_percentage import ApplyPercentage
from app.jurisdictions.ca.capabilities.cca_claim_after_column_22_prorated import (
    CcaClaimAfterColumn22Prorated,
)
from app.jurisdictions.ca.capabilities.choose_by_sign import ChooseBySign
from app.jurisdictions.ca.capabilities.closing_ucc_after_column_22_prorated import (
    ClosingUccAfterColumn22Prorated,
)
from app.jurisdictions.ca.capabilities.fiscal_period_days import FiscalPeriodDays
from app.jurisdictions.ca.capabilities.immediate_expensing_claim import ImmediateExpensingClaim
from app.jurisdictions.ca.capabilities.recaptured_cca import RecapturedCca
from app.jurisdictions.ca.capabilities.rental_gross_rents import RentalGrossRents
from app.jurisdictions.ca.capabilities.short_term_rental_gross_rents import (
    ShortTermRentalGrossRents,
)
from app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_cca import (
    ShortTermRentalNonCompliantCca,
)
from app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_cca_by_class import (
    ShortTermRentalNonCompliantCcaByClass,
)
from app.jurisdictions.ca.capabilities.short_term_rental_non_compliant_expenses import (
    ShortTermRentalNonCompliantExpenses,
)
from app.jurisdictions.ca.capabilities.terminal_loss import TerminalLoss
from app.jurisdictions.ca.capabilities.yes_or_no_count import YesOrNoCount
from app.jurisdictions.ca.catalog import (
    GROSS_RENTAL_INCOME,
    NET_RENTAL_INCOME,
    RENTAL_ADVERTISING,
    RENTAL_ADVERTISING_PERSONAL_PORTION,
    RENTAL_ADVERTISING_SHORT_TERM_PORTION,
    RENTAL_CCA_BUSINESS_USE_OF_HOME,
    RENTAL_CCA_CLAIM,
    RENTAL_CCA_CLAIM_BEFORE_LIMIT,
    RENTAL_CCA_CLAIM_LESS_PERSONAL_PART,
    RENTAL_CCA_CLAIM_SHARE,
    RENTAL_CCA_CLASSES,
    RENTAL_CCA_LIMIT,
    RENTAL_CCA_PERSONAL_PART,
    RENTAL_CCA_TABLE_CLAIM,
    RENTAL_CCA_TABLE_RECAPTURE,
    RENTAL_CCA_TABLE_TERMINAL_LOSS,
    RENTAL_CLOSING_UCC,
    RENTAL_COOWNER,
    RENTAL_COOWNER_CCA_CLAIM,
    RENTAL_COOWNER_OTHER_EXPENSES,
    RENTAL_COOWNER_RECAPTURED_CCA,
    RENTAL_COOWNER_SHARE,
    RENTAL_COOWNER_TERMINAL_LOSS,
    RENTAL_DEDUCTIBLE_EXPENSES,
    RENTAL_EPOP_AGREEMENT_FILED,
    RENTAL_EPOP_AGREEMENT_FILED_CHECKED,
    RENTAL_EPOP_ASSOCIATED,
    RENTAL_EPOP_ASSOCIATED_CHECKED,
    RENTAL_EPOP_PERCENTAGE,
    RENTAL_EPOP_PERCENTAGE_CHECKED,
    RENTAL_EPOP_PERCENTAGE_MAXIMUM,
    RENTAL_EPOP_PERCENTAGE_ROOM,
    RENTAL_EPOP_PERCENTAGE_TOTAL,
    RENTAL_EXPENSES_LESS_PERSONAL_PORTION,
    RENTAL_FISCAL_PERIOD_DAYS,
    RENTAL_FISCAL_PERIOD_DAYS_ENTERED,
    RENTAL_GROSS_RENTS,
    RENTAL_IMMEDIATE_EXPENSING_ALLOCATED,
    RENTAL_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT,
    RENTAL_IMMEDIATE_EXPENSING_CAP,
    RENTAL_IMMEDIATE_EXPENSING_CLAIM,
    RENTAL_IMMEDIATE_EXPENSING_LIMIT,
    RENTAL_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER,
    RENTAL_IMMEDIATE_EXPENSING_SHARE,
    RENTAL_INSURANCE,
    RENTAL_INSURANCE_PERSONAL_PORTION,
    RENTAL_INSURANCE_SHORT_TERM_PORTION,
    RENTAL_INTEREST_AND_BANK_CHARGES,
    RENTAL_INTEREST_AND_BANK_CHARGES_PERSONAL_PORTION,
    RENTAL_INTEREST_AND_BANK_CHARGES_SHORT_TERM_PORTION,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_PERSONAL_PORTION,
    RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_SHORT_TERM_PORTION,
    RENTAL_MINISTER_ALLOCATION,
    RENTAL_MINISTER_ALLOCATION_GIVEN,
    RENTAL_MINISTER_ALLOCATION_GIVEN_CHECKED,
    RENTAL_MOTOR_VEHICLE_EXPENSES,
    RENTAL_MOTOR_VEHICLE_EXPENSES_PERSONAL_PORTION,
    RENTAL_MOTOR_VEHICLE_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_NET_INCOME_AFTER_CCA,
    RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES,
    RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS,
    RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS,
    RENTAL_NET_INCOME_SHARE,
    RENTAL_NET_INCOME_WITH_RECAPTURE,
    RENTAL_NON_COMPLIANT_CCA,
    RENTAL_NON_COMPLIANT_EXPENSES,
    RENTAL_OFFICE_EXPENSES,
    RENTAL_OFFICE_EXPENSES_PERSONAL_PORTION,
    RENTAL_OFFICE_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_OTHER_EXPENSES,
    RENTAL_OTHER_EXPENSES_PERSONAL_PORTION,
    RENTAL_OTHER_EXPENSES_SHORT_TERM_PORTION,
    RENTAL_OTHER_INCOME,
    RENTAL_PARTNER,
    RENTAL_PARTNER_GST_HST_REBATE,
    RENTAL_PARTNER_OTHER_EXPENSES,
    RENTAL_PARTNER_SHARE,
    RENTAL_PARTNER_SHARE_WITH_REBATE,
    RENTAL_PARTNERSHIP_NET_INCOME,
    RENTAL_PERSONAL_PORTION,
    RENTAL_PROFESSIONAL_FEES,
    RENTAL_PROFESSIONAL_FEES_PERSONAL_PORTION,
    RENTAL_PROFESSIONAL_FEES_SHORT_TERM_PORTION,
    RENTAL_PROPERTIES,
    RENTAL_PROPERTY_TAXES,
    RENTAL_PROPERTY_TAXES_PERSONAL_PORTION,
    RENTAL_PROPERTY_TAXES_SHORT_TERM_PORTION,
    RENTAL_RECAPTURED_CCA,
    RENTAL_REPAIRS_AND_MAINTENANCE,
    RENTAL_REPAIRS_AND_MAINTENANCE_PERSONAL_PORTION,
    RENTAL_REPAIRS_AND_MAINTENANCE_SHORT_TERM_PORTION,
    RENTAL_SALARIES_WAGES_AND_BENEFITS,
    RENTAL_SALARIES_WAGES_AND_BENEFITS_PERSONAL_PORTION,
    RENTAL_SALARIES_WAGES_AND_BENEFITS_SHORT_TERM_PORTION,
    RENTAL_SHORT_TERM_PORTION,
    RENTAL_TERMINAL_LOSS,
    RENTAL_TOTAL_EXPENSES,
    RENTAL_TRAVEL,
    RENTAL_TRAVEL_PERSONAL_PORTION,
    RENTAL_TRAVEL_SHORT_TERM_PORTION,
    RENTAL_UTILITIES,
    RENTAL_UTILITIES_PERSONAL_PORTION,
    RENTAL_UTILITIES_SHORT_TERM_PORTION,
    SHORT_TERM_RENTAL_CCA_UNITS,
    SHORT_TERM_RENTAL_GROSS_RENTS,
    SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS,
    SHORT_TERM_RENTAL_UNITS,
)

NET_RENTAL_INCOME_PER_STATEMENT = RecordListKind(
    "ca/t776.net_rental_income", fields=(NET_RENTAL_INCOME,)
)
SHORT_TERM_RENTAL_GROSS_RENTS_PER_STATEMENT = RecordListKind(
    "ca/t776.short_term_rental_gross_rents", fields=(SHORT_TERM_RENTAL_GROSS_RENTS,)
)
RENTAL_SHORT_TERM_PORTION_PER_STATEMENT = RecordListKind(
    "ca/t776.rental_short_term_portion", fields=(RENTAL_SHORT_TERM_PORTION,)
)
RENTAL_CLOSING_UCC_PER_STATEMENT = RecordListKind(
    "ca/t776.rental_closing_ucc", fields=(RENTAL_CLOSING_UCC,)
)
RENTAL_NON_COMPLIANT_CCA_PER_STATEMENT = RecordListKind(
    "ca/t776.rental_non_compliant_cca", fields=(RENTAL_NON_COMPLIANT_CCA,)
)
SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS_PER_STATEMENT = RecordListKind(
    "ca/t776.short_term_rental_non_compliant_cca_by_class",
    fields=(SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS,),
)
RENTAL_IMMEDIATE_EXPENSING_CLAIM_PER_STATEMENT = RecordListKind(
    "ca/t776.rental_immediate_expensing_claim", fields=(RENTAL_IMMEDIATE_EXPENSING_CLAIM,)
)

FORM_INPUTS = frozenset(
    {
        "ca/rental_properties",
        "ca/rental_other_income",
        "ca/rental_advertising",
        "ca/rental_advertising_personal_portion",
        "ca/rental_advertising_short_term_portion",
        "ca/rental_insurance",
        "ca/rental_insurance_personal_portion",
        "ca/rental_insurance_short_term_portion",
        "ca/rental_interest_and_bank_charges",
        "ca/rental_interest_and_bank_charges_personal_portion",
        "ca/rental_interest_and_bank_charges_short_term_portion",
        "ca/rental_office_expenses",
        "ca/rental_office_expenses_personal_portion",
        "ca/rental_office_expenses_short_term_portion",
        "ca/rental_professional_fees",
        "ca/rental_professional_fees_personal_portion",
        "ca/rental_professional_fees_short_term_portion",
        "ca/rental_management_and_administration_fees",
        "ca/rental_management_and_administration_fees_personal_portion",
        "ca/rental_management_and_administration_fees_short_term_portion",
        "ca/rental_repairs_and_maintenance",
        "ca/rental_repairs_and_maintenance_personal_portion",
        "ca/rental_repairs_and_maintenance_short_term_portion",
        "ca/rental_salaries_wages_and_benefits",
        "ca/rental_salaries_wages_and_benefits_personal_portion",
        "ca/rental_salaries_wages_and_benefits_short_term_portion",
        "ca/rental_property_taxes",
        "ca/rental_property_taxes_personal_portion",
        "ca/rental_property_taxes_short_term_portion",
        "ca/rental_travel",
        "ca/rental_travel_personal_portion",
        "ca/rental_travel_short_term_portion",
        "ca/rental_utilities",
        "ca/rental_utilities_personal_portion",
        "ca/rental_utilities_short_term_portion",
        "ca/rental_motor_vehicle_expenses",
        "ca/rental_motor_vehicle_expenses_personal_portion",
        "ca/rental_motor_vehicle_expenses_short_term_portion",
        "ca/rental_other_expenses",
        "ca/rental_other_expenses_personal_portion",
        "ca/rental_other_expenses_short_term_portion",
        "ca/short_term_rental_units",
        "ca/short_term_rental_cca_units",
        "ca/rental_coowner",
        "ca/rental_coowner_share",
        "ca/rental_coowner_other_expenses",
        "ca/rental_cca_classes",
        "ca/rental_fiscal_period_days_entered",
        "ca/rental_coowner_recaptured_cca",
        "ca/rental_coowner_terminal_loss",
        "ca/rental_coowner_cca_claim",
        "ca/rental_cca_personal_part",
        "ca/rental_cca_business_use_of_home",
        "ca/rental_partner",
        "ca/rental_partner_share",
        "ca/rental_partner_gst_hst_rebate",
        "ca/rental_partner_other_expenses",
        "ca/rental_epop_associated",
        "ca/rental_epop_agreement_filed",
        "ca/rental_epop_percentage",
        "ca/rental_epop_percentage_total",
        "ca/rental_minister_allocation_given",
        "ca/rental_minister_allocation",
    }
)

FORM_STEPS = {
    # T776 Part 3, "Line 8140: Total of your gross rents for short-term rentals in the
    # year you receive them (add amounts under "Gross rents for short-term rentals")":
    # the total of that column of the rental properties, one row for each property; it
    # feeds no other line.
    CapabilitySelection(
        name="ca/short_term_rental_gross_rents",
        params={},
        consumes={"properties": "ca/rental_properties"},
        produces={"output": "ca/short_term_rental_gross_rents"},
    ),
    # T776 Part 3, "Line 8141: Total of all your gross rents in the year you receive
    # them (add lines under "Gross rents for all units")": the total of that column of
    # the rental properties.
    CapabilitySelection(
        name="ca/rental_gross_rents",
        params={},
        consumes={"properties": "ca/rental_properties"},
        produces={"output": "ca/rental_gross_rents"},
    ),
    # T776 "Line 8299: Total gross rental income: Enter this amount on your income tax
    # and benefit return on line 12599 (line 8141 plus line 8230)"; T1 "Line 12599:
    # Gross".
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rental_gross_rents",
                "ca/rental_other_income",
            )
        },
        produces={"output": "ca/gross_rental_income"},
    ),
    # T776 Part 4, "Line A: Total expenses (add amounts listed under "Total expenses")":
    # the 13 expense lines (8521, 8690, 8710, 8810, 8860, 8871, 8960, 9060, 9180, 9200,
    # 9220, 9281 and 9270), in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rental_advertising",
                "ca/rental_insurance",
                "ca/rental_interest_and_bank_charges",
                "ca/rental_office_expenses",
                "ca/rental_professional_fees",
                "ca/rental_management_and_administration_fees",
                "ca/rental_repairs_and_maintenance",
                "ca/rental_salaries_wages_and_benefits",
                "ca/rental_property_taxes",
                "ca/rental_travel",
                "ca/rental_utilities",
                "ca/rental_motor_vehicle_expenses",
                "ca/rental_other_expenses",
            )
        },
        produces={"output": "ca/rental_total_expenses"},
    ),
    # T776 "Line 9949: Total for personal portion (add amounts listed under "Personal
    # portion of total expenses")": the same 13 expense lines, in line order.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rental_advertising_personal_portion",
                "ca/rental_insurance_personal_portion",
                "ca/rental_interest_and_bank_charges_personal_portion",
                "ca/rental_office_expenses_personal_portion",
                "ca/rental_professional_fees_personal_portion",
                "ca/rental_management_and_administration_fees_personal_portion",
                "ca/rental_repairs_and_maintenance_personal_portion",
                "ca/rental_salaries_wages_and_benefits_personal_portion",
                "ca/rental_property_taxes_personal_portion",
                "ca/rental_travel_personal_portion",
                "ca/rental_utilities_personal_portion",
                "ca/rental_motor_vehicle_expenses_personal_portion",
                "ca/rental_other_expenses_personal_portion",
            )
        },
        produces={"output": "ca/rental_personal_portion"},
    ),
    # T776 "Line 9365: Total for short-term rental portion (add amounts listed under
    # "Short-term rental portion of total expenses")": the same 13 expense lines, in
    # line order; it feeds no other line (Chart A's column 3 is a starting amount).
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rental_advertising_short_term_portion",
                "ca/rental_insurance_short_term_portion",
                "ca/rental_interest_and_bank_charges_short_term_portion",
                "ca/rental_office_expenses_short_term_portion",
                "ca/rental_professional_fees_short_term_portion",
                "ca/rental_management_and_administration_fees_short_term_portion",
                "ca/rental_repairs_and_maintenance_short_term_portion",
                "ca/rental_salaries_wages_and_benefits_short_term_portion",
                "ca/rental_property_taxes_short_term_portion",
                "ca/rental_travel_short_term_portion",
                "ca/rental_utilities_short_term_portion",
                "ca/rental_motor_vehicle_expenses_short_term_portion",
                "ca/rental_other_expenses_short_term_portion",
            )
        },
        produces={"output": "ca/rental_short_term_portion"},
    ),
    # T776 "Line 9366: Non-compliant amount for short-term rentals (amount B from Chart
    # A)": Chart A's column 3 times column 4 divided by column 5 for each row of
    # short-term rental units, rounded to the cent, and "Line B" the total of column 6.
    CapabilitySelection(
        name="ca/short_term_rental_non_compliant_expenses",
        params={"rounding": "ca/short_term_rental_non_compliant_rounding"},
        consumes={"units": "ca/short_term_rental_units"},
        produces={"output": "ca/rental_non_compliant_expenses"},
    ),
    # T776 Chart B "Column 7 ***: Non-compliant amount (column 4 multiplied by column 5
    # divided by column 6)" for each row of short-term rental CCA units, rounded to the cent,
    # and "Line C: Total non-compliant amount of CCA for short-term rentals: Total of column 7
    # (enter on line 9367 of Part 4)".
    CapabilitySelection(
        name="ca/short_term_rental_non_compliant_cca",
        params={"rounding": "ca/short_term_rental_non_compliant_cca_rounding"},
        consumes={"units": "ca/short_term_rental_cca_units"},
        produces={"output": "ca/rental_non_compliant_cca"},
    ),
    # T776 Chart B "*** For each class, add the amounts from column 7 of Chart B and enter each
    # total in column 22 of Area A, in the respective row.": one record for each class, the
    # class number and column 22.
    CapabilitySelection(
        name="ca/short_term_rental_non_compliant_cca_by_class",
        params={"rounding": "ca/short_term_rental_non_compliant_cca_rounding"},
        consumes={"units": "ca/short_term_rental_cca_units"},
        produces={"output": "ca/short_term_rental_non_compliant_cca_by_class"},
    ),
    # T776 "Line 1: Deductible expenses (amount A minus line 9949 minus line 9366)",
    # first step: amount A minus line 9949.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/rental_total_expenses", "less": "ca/rental_personal_portion"},
        produces={"output": "ca/rental_expenses_less_personal_portion"},
    ),
    # T776 "Line 1: Deductible expenses (amount A minus line 9949 minus line 9366)",
    # second step: that result minus line 9366.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_expenses_less_personal_portion",
            "less": "ca/rental_non_compliant_expenses",
        },
        produces={"output": "ca/rental_deductible_expenses"},
    ),
    # T776 "Line 9369: Net income (loss) before adjustments (total gross rental income
    # from line 8299 minus deductible expenses from amount 1)": signed, a loss is
    # negative.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={"amount": "ca/gross_rental_income", "less": "ca/rental_deductible_expenses"},
        produces={"output": "ca/rental_net_income_before_adjustments"},
    ),
    # T776 "Line 2: Co-owners: calculate your share of net income from line 9369. Enter
    # your result on amount 2": a count of 1 for a co-owner (a caller's 0 or 1) chooses
    # the co-owner's share (line 2, as entered); with a count of 0 amount 2 is line
    # 9369.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/rental_coowner",
            "when_none": "ca/rental_net_income_before_adjustments",
            "when_any": "ca/rental_coowner_share",
        },
        produces={"output": "ca/rental_net_income_share"},
    ),
    # T776 "Line 3: Subtotal (amount 2 minus line 9945)": line 9945 is a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_net_income_share",
            "less": "ca/rental_coowner_other_expenses",
        },
        produces={"output": "ca/rental_net_income_after_coowner_expenses"},
    ),
    # T776 Area A "Line ii: Total CCA claim for the year *: Total of column 23" and Note 3 "If you
    # have a negative amount in column 7, add it to income as a recapture under "Recaptured
    # capital cost allowance" on line 9947": the recapture of each class of the Area A list
    # (column 7 made positive when negative), totalled.
    CapabilitySelection(
        name="ca/recaptured_cca",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"classes": "ca/rental_cca_classes"},
        produces={"output": "ca/rental_cca_table_recapture"},
    ),
    # T776 "Line 9947: Recaptured capital cost allowance (co-owners: enter your share of the
    # amount)": a count of 1 for a co-owner (a caller's 0 or 1) chooses the co-owner's share, as
    # entered; with a count of 0 line 9947 is the recapture of Area A.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/rental_coowner",
            "when_none": "ca/rental_cca_table_recapture",
            "when_any": "ca/rental_coowner_recaptured_cca",
        },
        produces={"output": "ca/rental_recaptured_cca"},
    ),
    # T776 "Line 4: Subtotal (amount 3 plus line 9947)": line 9947 is computed from Area A.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rental_net_income_after_coowner_expenses",
                "ca/rental_recaptured_cca",
            )
        },
        produces={"output": "ca/rental_net_income_with_recapture"},
    ),
    # T776 Area A Note 3 "If no property is left in the class and there is a positive amount in
    # this column, deduct the amount from your income as a terminal loss under "Terminal loss" on
    # line 9948. Recapture and terminal loss do not apply to a Class 10.1 property unless it is a
    # DIEP": the terminal loss of each class of the Area A list, totalled.
    CapabilitySelection(
        name="ca/terminal_loss",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"classes": "ca/rental_cca_classes"},
        produces={"output": "ca/rental_cca_table_terminal_loss"},
    ),
    # T776 "Line 9948: Terminal loss (co-owners: enter your share of the amount)": a count of 1
    # for a co-owner chooses the co-owner's share, as entered; with a count of 0 line 9948 is the
    # terminal loss of Area A.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/rental_coowner",
            "when_none": "ca/rental_cca_table_terminal_loss",
            "when_any": "ca/rental_coowner_terminal_loss",
        },
        produces={"output": "ca/rental_terminal_loss"},
    ),
    # T776 "Line 5: Subtotal (amount 4 minus line 9948)": line 9948 is computed from Area A.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_net_income_with_recapture",
            "less": "ca/rental_terminal_loss",
        },
        produces={"output": "ca/rental_net_income_after_terminal_loss"},
    ),
    # T776 Part 1 "Fiscal period from Date (Year/Month/Day) to (Year/12/31)", the days of the
    # rental's fiscal period (Guide T4036, Area A "Column 23 – CCA claim for the year": "In your
    # first year of rental activities, you may have to prorate your CCA claim."; Guide T4002 "You
    # were asking?": "base your CCA claim on the number of days in your fiscal period compared to
    # 365 days."): the days the caller enters, or the 365 of a full year when none are.
    CapabilitySelection(
        name="ca/fiscal_period_days",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={"entered": "ca/rental_fiscal_period_days_entered"},
        produces={"output": "ca/rental_fiscal_period_days"},
    ),
    # T776 Area A "Line ii: Total CCA claim for the year *: Total of column 23": the CCA claimed
    # on each class of the Area A list, at most its maximum (column 19 multiplied by column 20)
    # less its column 22 (the Chart B total of the class), totalled, each maximum prorated by the
    # days of the fiscal period.
    CapabilitySelection(
        name="ca/cca_claim_after_column_22_prorated",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={
            "classes": "ca/rental_cca_classes",
            "non_compliant": "ca/short_term_rental_non_compliant_cca_by_class",
            "fiscal_period_days": "ca/rental_fiscal_period_days",
        },
        produces={"output": "ca/rental_cca_table_claim"},
    ),
    # T776 Area A "* Sole proprietors and partnerships: Enter the total CCA claim for the year
    # from amount ii on line 9936. Co-owners: Enter only your share of the total CCA claim for
    # the year from amount ii on line 9936": a count of 1 for a co-owner chooses the co-owner's
    # share, as entered; with a count of 0 it is amount ii.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/rental_coowner",
            "when_none": "ca/rental_cca_table_claim",
            "when_any": "ca/rental_coowner_cca_claim",
        },
        produces={"output": "ca/rental_cca_claim_share"},
    ),
    # T776 "Line 9936: Total CCA claim for the year (amount ii from Area A minus any personal
    # part of CCA, and any CCA for business-use-of home expenses)", first step: amount ii minus
    # the personal part of CCA, a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_cca_claim_share",
            "less": "ca/rental_cca_personal_part",
        },
        produces={"output": "ca/rental_cca_claim_less_personal_part"},
    ),
    # T776 "Line 9936: Total CCA claim for the year (amount ii from Area A minus any personal
    # part of CCA, and any CCA for business-use-of home expenses)", second step: that result
    # minus the CCA for business-use-of-home expenses, a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_cca_claim_less_personal_part",
            "less": "ca/rental_cca_business_use_of_home",
        },
        produces={"output": "ca/rental_cca_claim_before_limit"},
    ),
    # Guide T4036: "You cannot use CCA to create or increase a rental loss": the most line 9936
    # may be is amount 5 ("Line 5: Subtotal (amount 4 minus line 9948)"), or 0 when amount 5 is
    # negative.
    CapabilitySelection(
        name="core/sum_not_below_zero",
        params={},
        consumes={"parts": ("ca/rental_net_income_after_terminal_loss",)},
        produces={"output": "ca/rental_cca_limit"},
    ),
    # T776 "Line 9936: Total CCA claim for the year": the claim above, at most that limit. A claim
    # above it is refused, not capped, which also covers Classes 31 and 32.
    CapabilitySelection(
        name="core/at_most",
        params={},
        consumes={
            "amount": "ca/rental_cca_claim_before_limit",
            "bound": "ca/rental_cca_limit",
        },
        produces={"output": "ca/rental_cca_claim"},
    ),
    # T776 Area A "Column 24: UCC at the end of the year (column 7 minus column 23)": the class
    # number and column 24 of each class of the Area A list, a product of the return for next
    # year's column 2.
    CapabilitySelection(
        name="ca/closing_ucc_after_column_22_prorated",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={
            "classes": "ca/rental_cca_classes",
            "non_compliant": "ca/short_term_rental_non_compliant_cca_by_class",
            "fiscal_period_days": "ca/rental_fiscal_period_days",
        },
        produces={"output": "ca/rental_closing_ucc"},
    ),
    # T776 Note 5 "the immediate expensing limit, which is equal to one of the following, whichever
    # is applicable: $1.5 million, if you are not associated with any other eligible person or
    # partnership (EPOP) in the tax year" and Area G "Line iii: Immediate expensing limit allocated
    # to you: Multiply $1.5 million by the percentage assigned to you in column 3 (see note 11)":
    # the printed $1.5 million, a dataset.
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/rental_immediate_expensing_cap"},
        consumes={},
        produces={"output": "ca/rental_immediate_expensing_cap"},
    ),
    # T776 Area G "The total of all percentages assigned under the agreement should not be more than
    # 100%. If the total is more than 100%, then the associated group has an immediate expensing
    # limit of zero." and Note 11 "If the total of column 3 is more than 100%, enter "0."": the
    # printed 100%, a dataset, as the form prints a percentage (100 for 100%).
    CapabilitySelection(
        name="core/credit_amount",
        params={"amount": "ca/rental_epop_percentage_maximum"},
        consumes={},
        produces={"output": "ca/rental_epop_percentage_maximum"},
    ),
    # T776 Area G "Line iii: Immediate expensing limit allocated to you: Multiply $1.5 million by
    # the percentage assigned to you in column 3 (see note 11)", first step: $1.5 million times the
    # percentage assigned to you in column 3, a caller input as the form prints it (40 for 40%).
    CapabilitySelection(
        name="ca/apply_percentage",
        params={"rounding": "ca/rental_immediate_expensing_rounding"},
        consumes={
            "amount": "ca/rental_immediate_expensing_cap",
            "percentage": "ca/rental_epop_percentage_checked",
        },
        produces={"output": "ca/rental_immediate_expensing_share"},
    ),
    # T776 Area G Note 11 "If the total of column 3 is more than 100%, enter "0."", first step: 100%
    # less "Total of percentage assigned: Total of column 3", a caller input; negative when the
    # total is more than 100%.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_epop_percentage_maximum",
            "less": "ca/rental_epop_percentage_total",
        },
        produces={"output": "ca/rental_epop_percentage_room"},
    ),
    # T776 Area G "Line iii: Immediate expensing limit allocated to you: Multiply $1.5 million by
    # the percentage assigned to you in column 3 (see note 11)" and Note 11 "If the total of column
    # 3 is more than 100%, enter "0."": the multiple above when 100% less the total of column 3 is
    # zero or positive, else 0.
    CapabilitySelection(
        name="ca/choose_by_sign",
        params={},
        consumes={
            "sign": "ca/rental_epop_percentage_room",
            "when_positive": (),
            "when_zero": (),
            "when_negative": (),
            "when_non_positive": (),
            "when_non_negative": ("ca/rental_immediate_expensing_share",),
        },
        produces={"output": "ca/rental_immediate_expensing_allocated"},
    ),
    # T776 Note 5 "amount iii of Area G, if you are associated with one or more EPOPs in the tax
    # year" and "zero, if you are associated with one or more EPOPs and an agreement that assigns a
    # percentage to one or more of the associated EPOPs was not filed with the minister in a
    # prescribed form": line iii times the count of agreements filed (a caller's 0 or 1), so 0 when
    # none was filed.
    CapabilitySelection(
        name="core/times_count",
        params={},
        consumes={
            "amount": "ca/rental_immediate_expensing_allocated",
            "count": "ca/rental_epop_agreement_filed_checked",
        },
        produces={"output": "ca/rental_immediate_expensing_associated_limit"},
    ),
    # T776 Note 5 "the immediate expensing limit, which is equal to one of the following, whichever
    # is applicable": a count of 1 for associated with one or more EPOPs (a caller's 0 or 1) chooses
    # the limit above ("amount iii of Area G" or "zero"); with a count of 0 it is the $1.5 million
    # ("if you are not associated with any other eligible person or partnership (EPOP) in the tax
    # year").
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/rental_epop_associated_checked",
            "when_none": "ca/rental_immediate_expensing_cap",
            "when_any": "ca/rental_immediate_expensing_associated_limit",
        },
        produces={"output": "ca/rental_immediate_expensing_limit_before_minister"},
    ),
    # T776 Note 5 "any amount allocated by the minister under subsection 1104(3.4) of the
    # Regulations": a count of 1 (a caller's 0 or 1) chooses the amount allocated by the minister,
    # as entered, in place of the limit above; with a count of 0 the limit above stands.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/rental_minister_allocation_given_checked",
            "when_none": "ca/rental_immediate_expensing_limit_before_minister",
            "when_any": "ca/rental_minister_allocation",
        },
        produces={"output": "ca/rental_immediate_expensing_limit"},
    ),
    # T776 "Line i: Total immediate expensing claim for the year: Total of column 9" and Note 5 "The
    # total immediate expensing amount for the tax year (total of column 9) is limited to the lesser
    # of: the immediate expensing limit"; "the UCC of DIEPs in column 8"; "the amount of income, if
    # any, earned from the source of income that is a property (before any CCA deductions) in which
    # the relevant DIEP is used for the tax year": the total of column 9 of the Area A list, refused
    # when above the limit or above the income before CCA (amount 5 not below zero).
    CapabilitySelection(
        name="ca/immediate_expensing_claim",
        params={"class_rates": "ca/cca_class_rates"},
        consumes={
            "classes": "ca/rental_cca_classes",
            "immediate_expensing_limit": "ca/rental_immediate_expensing_limit",
            "income_before_cca": "ca/rental_cca_limit",
        },
        produces={"output": "ca/rental_immediate_expensing_claim"},
    ),
    # T776 "Line 6: Net income (loss) (amount 5 minus line 9936)": line 9936 is computed above.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_net_income_after_terminal_loss",
            "less": "ca/rental_cca_claim",
        },
        produces={"output": "ca/rental_net_income_after_cca"},
    ),
    # T776 "Line 9946: ... For partnerships, enter the result from amount 7 plus line
    # 9974 minus line 9943", first step: amount 7 (line 7, "Partners: your share of
    # amount 6, or the amount from your T5013 slip, Statement of Partnership Income")
    # plus line 9974 ("Partners: GST/HST rebate for partners received in the year"),
    # both caller inputs.
    CapabilitySelection(
        name="core/sum",
        params={},
        consumes={
            "parts": (
                "ca/rental_partner_share",
                "ca/rental_partner_gst_hst_rebate",
            )
        },
        produces={"output": "ca/rental_partner_share_with_rebate"},
    ),
    # T776 "Line 9946: ... For partnerships, enter the result from amount 7 plus line
    # 9974 minus line 9943", second step: that result minus line 9943 ("Partners: other
    # expenses of the partner"), a caller input.
    CapabilitySelection(
        name="core/subtract",
        params={},
        consumes={
            "amount": "ca/rental_partner_share_with_rebate",
            "less": "ca/rental_partner_other_expenses",
        },
        produces={"output": "ca/rental_partnership_net_income"},
    ),
    # T776 "Line 9946: Your net income (loss): For sole proprietors or co-owners, enter
    # the result from amount 6. For partnerships, enter the result from amount 7 plus
    # line 9974 minus line 9943. Enter this amount on line 12600 of your income tax and
    # benefit return"; T1 "Line 12600: Net". A count of 1 for a partner (a caller's 0 or
    # 1) chooses the partnership figure, else amount 6.
    CapabilitySelection(
        name="core/choose_by_count",
        params={},
        consumes={
            "count": "ca/rental_partner",
            "when_none": "ca/rental_net_income_after_cca",
            "when_any": "ca/rental_partnership_net_income",
        },
        produces={"output": "ca/net_rental_income"},
    ),
    # Area A endnote 5 answers, taken as a count of 0 or 1: each is checked to be 0 or 1 before
    # the step that reads it. A caller's 2 is refused, naming the kind.
    CapabilitySelection(
        name="ca/yes_or_no_count",
        params={},
        consumes={"count": "ca/rental_epop_associated"},
        produces={"output": "ca/rental_epop_associated_checked"},
    ),
    CapabilitySelection(
        name="ca/yes_or_no_count",
        params={},
        consumes={"count": "ca/rental_epop_agreement_filed"},
        produces={"output": "ca/rental_epop_agreement_filed_checked"},
    ),
    CapabilitySelection(
        name="ca/yes_or_no_count",
        params={},
        consumes={"count": "ca/rental_minister_allocation_given"},
        produces={"output": "ca/rental_minister_allocation_given_checked"},
    ),
    # Area G "Total of percentage assigned: Total of column 3": the forms are silent on a
    # percentage assigned to the business above that total. It is refused, not capped: a decision
    # a choice, not a form rule. The checked percentage is the one the next step applies.
    CapabilitySelection(
        name="core/at_most",
        params={},
        consumes={
            "amount": "ca/rental_epop_percentage",
            "bound": "ca/rental_epop_percentage_total",
        },
        produces={"output": "ca/rental_epop_percentage_checked"},
    ),
}

FORM_WIRING = {
    (
        ShortTermRentalGrossRents,
        frozenset({RENTAL_PROPERTIES}),
        frozenset({SHORT_TERM_RENTAL_GROSS_RENTS}),
    ),
    (RentalGrossRents, frozenset({RENTAL_PROPERTIES}), frozenset({RENTAL_GROSS_RENTS})),
    (
        Sum,
        frozenset({RENTAL_GROSS_RENTS, RENTAL_OTHER_INCOME}),
        frozenset({GROSS_RENTAL_INCOME}),
    ),
    (
        Sum,
        frozenset(
            {
                RENTAL_ADVERTISING,
                RENTAL_INSURANCE,
                RENTAL_INTEREST_AND_BANK_CHARGES,
                RENTAL_OFFICE_EXPENSES,
                RENTAL_PROFESSIONAL_FEES,
                RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES,
                RENTAL_REPAIRS_AND_MAINTENANCE,
                RENTAL_SALARIES_WAGES_AND_BENEFITS,
                RENTAL_PROPERTY_TAXES,
                RENTAL_TRAVEL,
                RENTAL_UTILITIES,
                RENTAL_MOTOR_VEHICLE_EXPENSES,
                RENTAL_OTHER_EXPENSES,
            }
        ),
        frozenset({RENTAL_TOTAL_EXPENSES}),
    ),
    (
        Sum,
        frozenset(
            {
                RENTAL_ADVERTISING_PERSONAL_PORTION,
                RENTAL_INSURANCE_PERSONAL_PORTION,
                RENTAL_INTEREST_AND_BANK_CHARGES_PERSONAL_PORTION,
                RENTAL_OFFICE_EXPENSES_PERSONAL_PORTION,
                RENTAL_PROFESSIONAL_FEES_PERSONAL_PORTION,
                RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_PERSONAL_PORTION,
                RENTAL_REPAIRS_AND_MAINTENANCE_PERSONAL_PORTION,
                RENTAL_SALARIES_WAGES_AND_BENEFITS_PERSONAL_PORTION,
                RENTAL_PROPERTY_TAXES_PERSONAL_PORTION,
                RENTAL_TRAVEL_PERSONAL_PORTION,
                RENTAL_UTILITIES_PERSONAL_PORTION,
                RENTAL_MOTOR_VEHICLE_EXPENSES_PERSONAL_PORTION,
                RENTAL_OTHER_EXPENSES_PERSONAL_PORTION,
            }
        ),
        frozenset({RENTAL_PERSONAL_PORTION}),
    ),
    (
        Sum,
        frozenset(
            {
                RENTAL_ADVERTISING_SHORT_TERM_PORTION,
                RENTAL_INSURANCE_SHORT_TERM_PORTION,
                RENTAL_INTEREST_AND_BANK_CHARGES_SHORT_TERM_PORTION,
                RENTAL_OFFICE_EXPENSES_SHORT_TERM_PORTION,
                RENTAL_PROFESSIONAL_FEES_SHORT_TERM_PORTION,
                RENTAL_MANAGEMENT_AND_ADMINISTRATION_FEES_SHORT_TERM_PORTION,
                RENTAL_REPAIRS_AND_MAINTENANCE_SHORT_TERM_PORTION,
                RENTAL_SALARIES_WAGES_AND_BENEFITS_SHORT_TERM_PORTION,
                RENTAL_PROPERTY_TAXES_SHORT_TERM_PORTION,
                RENTAL_TRAVEL_SHORT_TERM_PORTION,
                RENTAL_UTILITIES_SHORT_TERM_PORTION,
                RENTAL_MOTOR_VEHICLE_EXPENSES_SHORT_TERM_PORTION,
                RENTAL_OTHER_EXPENSES_SHORT_TERM_PORTION,
            }
        ),
        frozenset({RENTAL_SHORT_TERM_PORTION}),
    ),
    (
        ShortTermRentalNonCompliantExpenses,
        frozenset({SHORT_TERM_RENTAL_UNITS}),
        frozenset({RENTAL_NON_COMPLIANT_EXPENSES}),
    ),
    (
        ShortTermRentalNonCompliantCca,
        frozenset({SHORT_TERM_RENTAL_CCA_UNITS}),
        frozenset({RENTAL_NON_COMPLIANT_CCA}),
    ),
    (
        ShortTermRentalNonCompliantCcaByClass,
        frozenset({SHORT_TERM_RENTAL_CCA_UNITS}),
        frozenset({SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS}),
    ),
    (
        Subtract,
        frozenset({RENTAL_TOTAL_EXPENSES, RENTAL_PERSONAL_PORTION}),
        frozenset({RENTAL_EXPENSES_LESS_PERSONAL_PORTION}),
    ),
    (
        Subtract,
        frozenset({RENTAL_EXPENSES_LESS_PERSONAL_PORTION, RENTAL_NON_COMPLIANT_EXPENSES}),
        frozenset({RENTAL_DEDUCTIBLE_EXPENSES}),
    ),
    (
        Subtract,
        frozenset({GROSS_RENTAL_INCOME, RENTAL_DEDUCTIBLE_EXPENSES}),
        frozenset({RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS}),
    ),
    (
        ChooseByCount,
        frozenset({RENTAL_COOWNER, RENTAL_NET_INCOME_BEFORE_ADJUSTMENTS, RENTAL_COOWNER_SHARE}),
        frozenset({RENTAL_NET_INCOME_SHARE}),
    ),
    (
        Subtract,
        frozenset({RENTAL_NET_INCOME_SHARE, RENTAL_COOWNER_OTHER_EXPENSES}),
        frozenset({RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES}),
    ),
    (RecapturedCca, frozenset({RENTAL_CCA_CLASSES}), frozenset({RENTAL_CCA_TABLE_RECAPTURE})),
    (
        ChooseByCount,
        frozenset({RENTAL_COOWNER, RENTAL_CCA_TABLE_RECAPTURE, RENTAL_COOWNER_RECAPTURED_CCA}),
        frozenset({RENTAL_RECAPTURED_CCA}),
    ),
    (TerminalLoss, frozenset({RENTAL_CCA_CLASSES}), frozenset({RENTAL_CCA_TABLE_TERMINAL_LOSS})),
    (
        ChooseByCount,
        frozenset({RENTAL_COOWNER, RENTAL_CCA_TABLE_TERMINAL_LOSS, RENTAL_COOWNER_TERMINAL_LOSS}),
        frozenset({RENTAL_TERMINAL_LOSS}),
    ),
    (
        FiscalPeriodDays,
        frozenset({RENTAL_FISCAL_PERIOD_DAYS_ENTERED}),
        frozenset({RENTAL_FISCAL_PERIOD_DAYS}),
    ),
    (
        CcaClaimAfterColumn22Prorated,
        frozenset(
            {
                RENTAL_CCA_CLASSES,
                SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS,
                RENTAL_FISCAL_PERIOD_DAYS,
            }
        ),
        frozenset({RENTAL_CCA_TABLE_CLAIM}),
    ),
    (
        ChooseByCount,
        frozenset({RENTAL_COOWNER, RENTAL_CCA_TABLE_CLAIM, RENTAL_COOWNER_CCA_CLAIM}),
        frozenset({RENTAL_CCA_CLAIM_SHARE}),
    ),
    (
        Subtract,
        frozenset({RENTAL_CCA_CLAIM_SHARE, RENTAL_CCA_PERSONAL_PART}),
        frozenset({RENTAL_CCA_CLAIM_LESS_PERSONAL_PART}),
    ),
    (
        Subtract,
        frozenset({RENTAL_CCA_CLAIM_LESS_PERSONAL_PART, RENTAL_CCA_BUSINESS_USE_OF_HOME}),
        frozenset({RENTAL_CCA_CLAIM_BEFORE_LIMIT}),
    ),
    (
        SumNotBelowZero,
        frozenset({RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS}),
        frozenset({RENTAL_CCA_LIMIT}),
    ),
    (
        AtMost,
        frozenset({RENTAL_CCA_CLAIM_BEFORE_LIMIT, RENTAL_CCA_LIMIT}),
        frozenset({RENTAL_CCA_CLAIM}),
    ),
    (
        ClosingUccAfterColumn22Prorated,
        frozenset(
            {
                RENTAL_CCA_CLASSES,
                SHORT_TERM_RENTAL_NON_COMPLIANT_CCA_BY_CLASS,
                RENTAL_FISCAL_PERIOD_DAYS,
            }
        ),
        frozenset({RENTAL_CLOSING_UCC}),
    ),
    (
        Sum,
        frozenset({RENTAL_NET_INCOME_AFTER_COOWNER_EXPENSES, RENTAL_RECAPTURED_CCA}),
        frozenset({RENTAL_NET_INCOME_WITH_RECAPTURE}),
    ),
    (
        Subtract,
        frozenset({RENTAL_NET_INCOME_WITH_RECAPTURE, RENTAL_TERMINAL_LOSS}),
        frozenset({RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS}),
    ),
    (CreditAmount, frozenset(), frozenset({RENTAL_IMMEDIATE_EXPENSING_CAP})),
    (CreditAmount, frozenset(), frozenset({RENTAL_EPOP_PERCENTAGE_MAXIMUM})),
    (
        ApplyPercentage,
        frozenset({RENTAL_IMMEDIATE_EXPENSING_CAP, RENTAL_EPOP_PERCENTAGE_CHECKED}),
        frozenset({RENTAL_IMMEDIATE_EXPENSING_SHARE}),
    ),
    (
        Subtract,
        frozenset({RENTAL_EPOP_PERCENTAGE_MAXIMUM, RENTAL_EPOP_PERCENTAGE_TOTAL}),
        frozenset({RENTAL_EPOP_PERCENTAGE_ROOM}),
    ),
    (
        ChooseBySign,
        frozenset({RENTAL_EPOP_PERCENTAGE_ROOM, RENTAL_IMMEDIATE_EXPENSING_SHARE}),
        frozenset({RENTAL_IMMEDIATE_EXPENSING_ALLOCATED}),
    ),
    (
        TimesCount,
        frozenset({RENTAL_IMMEDIATE_EXPENSING_ALLOCATED, RENTAL_EPOP_AGREEMENT_FILED_CHECKED}),
        frozenset({RENTAL_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT}),
    ),
    (
        ChooseByCount,
        frozenset(
            {
                RENTAL_EPOP_ASSOCIATED_CHECKED,
                RENTAL_IMMEDIATE_EXPENSING_CAP,
                RENTAL_IMMEDIATE_EXPENSING_ASSOCIATED_LIMIT,
            }
        ),
        frozenset({RENTAL_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER}),
    ),
    (
        ChooseByCount,
        frozenset(
            {
                RENTAL_MINISTER_ALLOCATION_GIVEN_CHECKED,
                RENTAL_IMMEDIATE_EXPENSING_LIMIT_BEFORE_MINISTER,
                RENTAL_MINISTER_ALLOCATION,
            }
        ),
        frozenset({RENTAL_IMMEDIATE_EXPENSING_LIMIT}),
    ),
    (
        ImmediateExpensingClaim,
        frozenset({RENTAL_CCA_CLASSES, RENTAL_IMMEDIATE_EXPENSING_LIMIT, RENTAL_CCA_LIMIT}),
        frozenset({RENTAL_IMMEDIATE_EXPENSING_CLAIM}),
    ),
    (
        Subtract,
        frozenset({RENTAL_NET_INCOME_AFTER_TERMINAL_LOSS, RENTAL_CCA_CLAIM}),
        frozenset({RENTAL_NET_INCOME_AFTER_CCA}),
    ),
    (
        Sum,
        frozenset({RENTAL_PARTNER_SHARE, RENTAL_PARTNER_GST_HST_REBATE}),
        frozenset({RENTAL_PARTNER_SHARE_WITH_REBATE}),
    ),
    (
        Subtract,
        frozenset({RENTAL_PARTNER_SHARE_WITH_REBATE, RENTAL_PARTNER_OTHER_EXPENSES}),
        frozenset({RENTAL_PARTNERSHIP_NET_INCOME}),
    ),
    (
        ChooseByCount,
        frozenset({RENTAL_PARTNER, RENTAL_NET_INCOME_AFTER_CCA, RENTAL_PARTNERSHIP_NET_INCOME}),
        frozenset({NET_RENTAL_INCOME}),
    ),
    (
        YesOrNoCount,
        frozenset({RENTAL_EPOP_ASSOCIATED}),
        frozenset({RENTAL_EPOP_ASSOCIATED_CHECKED}),
    ),
    (
        YesOrNoCount,
        frozenset({RENTAL_EPOP_AGREEMENT_FILED}),
        frozenset({RENTAL_EPOP_AGREEMENT_FILED_CHECKED}),
    ),
    (
        YesOrNoCount,
        frozenset({RENTAL_MINISTER_ALLOCATION_GIVEN}),
        frozenset({RENTAL_MINISTER_ALLOCATION_GIVEN_CHECKED}),
    ),
    (
        AtMost,
        frozenset({RENTAL_EPOP_PERCENTAGE, RENTAL_EPOP_PERCENTAGE_TOTAL}),
        frozenset({RENTAL_EPOP_PERCENTAGE_CHECKED}),
    ),
}

INPUTS = frozenset({"ca/t776_statements"})

FORM_EXPORTS = (
    "ca/net_rental_income",
    "ca/short_term_rental_gross_rents",
    "ca/rental_short_term_portion",
    "ca/rental_closing_ucc",
    "ca/rental_non_compliant_cca",
    "ca/short_term_rental_non_compliant_cca_by_class",
    "ca/rental_immediate_expensing_claim",
)

# The form exports lines nothing on the return reads (line 8140, line 9365, Chart B's line C and
# total for each class, Area A column 24 and line i): an export nobody reads is fine, so the
# return declares no output for them.
OUTPUTS: frozenset[str] = frozenset()

# T1 line 12600 "Net": the total of T776 line 9946 over the statements.
STEPS = {
    CapabilitySelection(
        name="core/record_total",
        params={},
        consumes={"records": "ca/t776.net_rental_income"},
        produces={"output": "ca/net_rental_income"},
    ),
}

WIRING = {
    (
        RecordTotal,
        frozenset({NET_RENTAL_INCOME_PER_STATEMENT}),
        frozenset({NET_RENTAL_INCOME}),
    ),
}
