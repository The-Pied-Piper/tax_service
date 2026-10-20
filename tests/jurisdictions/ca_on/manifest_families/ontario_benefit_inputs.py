"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.manifest import CapabilitySelection

INPUTS = frozenset(
    {
        # Form ON-BEN, "Application for the 2026 Ontario Trillium Benefit and Ontario Senior
        # Homeowners' Property Tax Grant": the tick boxes of lines 61020, 61040, 61060, 61070,
        # 61080 and 61140 and the amounts of Part A's lines 61100, 61120, 61210 and 61230, as
        # the form takes them. Each is also an output: the form computes nothing from them.
        "ca-on/applies_for_energy_and_property_tax_credit",
        "ca-on/applies_for_northern_energy_credit",
        "ca-on/chooses_single_benefit_payment",
        "ca-on/applies_for_senior_homeowners_grant",
        "ca-on/separate_residences_for_medical_reasons",
        "ca-on/lived_in_student_residence",
        "ca-on/rent_paid",
        "ca-on/property_tax_paid",
        "ca-on/reserve_home_energy_costs",
        "ca-on/public_long_term_care_paid",
    }
)

OUTPUTS = frozenset(
    {
        "ca-on/applies_for_energy_and_property_tax_credit",
        "ca-on/applies_for_northern_energy_credit",
        "ca-on/chooses_single_benefit_payment",
        "ca-on/applies_for_senior_homeowners_grant",
        "ca-on/separate_residences_for_medical_reasons",
        "ca-on/lived_in_student_residence",
        "ca-on/rent_paid",
        "ca-on/property_tax_paid",
        "ca-on/reserve_home_energy_costs",
        "ca-on/public_long_term_care_paid",
    }
)

STEPS = set[CapabilitySelection]()

WIRING = set[object]()
