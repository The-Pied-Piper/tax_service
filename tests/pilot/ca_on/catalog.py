"""The CA-ON artifact catalog: pilot artifacts named from Canada's own return (design.md §2, §7).

It lives with the pilot tests until catalogs get a production home (#24). Only artifacts the
pilot tests use are declared. Identifiers are stable: `test_catalog.py` snapshots them.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactCatalog
from app.domain.registry import Namespace

CATALOG = ArtifactCatalog(Namespace("ca"))

TAXABLE_INCOME = CATALOG.artifact("taxable_income", Decimal)
"""Taxable income, T1 line 26000: the base the federal and Ontario brackets apply to."""

FEDERAL_BASIC_TAX = CATALOG.artifact("federal_basic_tax", Decimal)
"""Federal tax on taxable income from the bracket schedule, before non-refundable credits."""
