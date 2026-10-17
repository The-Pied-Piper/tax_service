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

EMPLOYMENT_INCOME = CATALOG.declare("employment_income", Decimal)
"""Employment income, T1 line 10100: a starting amount that total income sums directly."""

CAPITAL_GAIN = CATALOG.declare("capital_gain", Decimal)
"""The claimed capital gain before inclusion, mirroring Schedule 3 line 21 (total capital gains
or losses).

Losses, and netting gains against them, are not modelled yet.
"""

TAXABLE_CAPITAL_GAINS = CATALOG.declare("taxable_capital_gains", Decimal)
"""Taxable capital gains, T1 line 12700: the capital gain times the inclusion rate (Schedule 3
lines 23 to 26)."""

TOTAL_INCOME = CATALOG.declare("total_income", Decimal)
"""Total income, T1 line 15000: the sum of the income lines, here employment income and taxable
capital gains."""

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
