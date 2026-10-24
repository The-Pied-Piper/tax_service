"""The CA-ON manifest entries of one family of lines (see `test_manifest.py`)."""

from __future__ import annotations

from app.domain.manifest import CapabilitySelection

INPUTS = frozenset(
    {
        "ca/rl_10_labour_sponsored_fund_amount",
        "ca/political_contributions",
        "ca/other_employment_expenses",
        "ca/wage_loss_replacement_plan_income",
        "ca/resident_in_canada_throughout_2025",
        "ca/aged_18_or_older_at_end_of_2025",
        "ca/spouse_net_income_before_adjustments",
        "ca/spouse_uccb_repayment",
        "ca/spouse_rdsp_income_repayment",
        "ca/spouse_universal_child_care_benefit",
        "ca/spouse_rdsp_income",
    }
)

OUTPUTS = frozenset[str]()

STEPS = set[CapabilitySelection]()

WIRING = set[object]()
