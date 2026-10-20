"""Federal Canada's capabilities: mechanisms specific to its forms, parameters from data.

Each capability registers itself with `@capability` when its module is imported; this package
imports every one of them, so importing the package fills the shared CapabilityRegistry.
`NAMESPACE` comes first because the decorators read it while this file is still being imported.
"""

NAMESPACE = "ca"

from app.jurisdictions.ca.capabilities import (  # noqa: E402
    amount_or_divided_by_rate,
    caregiver_amount,
    cca_claim,
    cca_table,
    chart_a_row_c_total,
    chart_b_zone_a_total,
    chart_b_zone_b_total,
    chart_b_zone_total,
    closing_ucc,
    disability_transfer_amount,
    other_dependants_medical,
    principal_residence_gain,
    recaptured_cca,
    rental_gross_rents,
    short_term_rental_gross_rents,
    short_term_rental_non_compliant_expenses,
    terminal_loss,
    threshold_gate,
)

__all__ = [
    "NAMESPACE",
    "amount_or_divided_by_rate",
    "caregiver_amount",
    "cca_claim",
    "cca_table",
    "chart_a_row_c_total",
    "chart_b_zone_a_total",
    "chart_b_zone_b_total",
    "chart_b_zone_total",
    "closing_ucc",
    "disability_transfer_amount",
    "other_dependants_medical",
    "principal_residence_gain",
    "recaptured_cca",
    "rental_gross_rents",
    "short_term_rental_gross_rents",
    "short_term_rental_non_compliant_expenses",
    "terminal_loss",
    "threshold_gate",
]
