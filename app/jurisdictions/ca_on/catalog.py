"""The Ontario artifact catalog: Ontario's own kinds, named from Form ON428 (§2, §7).

Only the kinds in use are declared; federal kinds come from `app.jurisdictions.ca.catalog`.
Identifiers are stable:
`tests/jurisdictions/ca_on/test_catalog.py` snapshots them.
"""

from __future__ import annotations

from decimal import Decimal

from app.domain.artifact import ArtifactCatalog
from app.domain.registry import Namespace
from app.jurisdictions.ca_on import NAMESPACE

CATALOG = ArtifactCatalog(Namespace(NAMESPACE))

ONTARIO_BASIC_TAX = CATALOG.declare("ontario_basic_tax", Decimal)
"""Ontario tax on taxable income, 2025 ON428 line 8 (Part A), before non-refundable credits."""

ONTARIO_TAX_AFTER_CREDITS = CATALOG.declare("ontario_tax_after_credits", Decimal)
"""Ontario tax after non-refundable tax credits, not below zero: 2025 ON428 line 53."""
