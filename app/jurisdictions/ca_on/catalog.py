"""The Ontario artifact catalog: Ontario's own kinds, named from Form ON428 (§2, §7).

Only the kinds in use are declared, each non-negative, as no ON428 line here can be negative;
federal kinds come from `app.jurisdictions.ca.catalog`. Identifiers are stable:
`tests/jurisdictions/ca_on/test_catalog.py` snapshots them.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactCatalog
from app.domain.registry import Namespace
from app.jurisdictions.ca_on import NAMESPACE

CATALOG = ArtifactCatalog(Namespace(NAMESPACE))

ONTARIO_BASIC_TAX = CATALOG.declare("ontario_basic_tax", Decimal, non_negative=True)
"""Ontario tax on taxable income, 2025 ON428 line 8 (Part A), before non-refundable credits."""

BASIC_PERSONAL_AMOUNT = CATALOG.declare("basic_personal_amount", Decimal, non_negative=True)
"""Basic personal amount, ON428 line 9 (line 58040) "Basic personal amount Claim $12,747": the
amount claimed, the first part of the total of the Ontario credit amounts."""

NON_REFUNDABLE_CREDIT_AMOUNTS = CATALOG.declare(
    "non_refundable_credit_amounts", Decimal, non_negative=True
)
"""Total of the Ontario non-refundable credit amounts, ON428 line 44 (line 58800) "Line 35 plus
line 43": the sum of the credit amounts the rate is applied to once, here the basic personal
amount, the base CPP contributions and the EI premiums."""

NON_REFUNDABLE_TAX_CREDITS = CATALOG.declare(
    "non_refundable_tax_credits", Decimal, non_negative=True
)
"""Ontario non-refundable tax credits, ON428 line 50 (line 61500) "Line 46 plus line 49 Enter this
amount on line 52. Ontario non-refundable tax credits": the total of the Ontario credit amounts
times the credit rate, here line 46 (line 58840) alone."""

ONTARIO_TAX_AFTER_CREDITS = CATALOG.declare("ontario_tax_after_credits", Decimal, non_negative=True)
"""Ontario tax after non-refundable tax credits, not below zero: 2025 ON428 line 53."""
