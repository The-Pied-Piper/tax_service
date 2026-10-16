"""The federal Canada artifact catalog: artifact kinds named from Canada's own return (§2, §7).

Only the kinds in use are declared. Identifiers are stable: `tests/jurisdictions/ca/test_catalog.py`
snapshots them.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactCatalog
from app.domain.registry import Namespace
from app.jurisdictions.ca import NAMESPACE

CATALOG = ArtifactCatalog(Namespace(NAMESPACE))

TAXABLE_INCOME = CATALOG.declare("taxable_income", Decimal)
"""Taxable income, T1 line 26000: the base the federal and Ontario brackets apply to."""

FEDERAL_BASIC_TAX = CATALOG.declare("federal_basic_tax", Decimal)
"""Federal tax on taxable income from the bracket schedule, before non-refundable credits.

Its T1 line reference is still to be confirmed: design.md §2 marks federal line semantics
UNVERIFIED.
"""

FEDERAL_TAX_AFTER_CREDITS = CATALOG.declare("federal_tax_after_credits", Decimal)
"""Federal basic tax less federal non-refundable tax credits, not below zero.

Its T1 line reference is still to be confirmed: design.md §2 marks federal line semantics
UNVERIFIED.
"""
