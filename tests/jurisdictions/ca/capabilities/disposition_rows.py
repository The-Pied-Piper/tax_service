"""Shared test data for the DispositionGains and DispositionGainsOnly capabilities, Schedule 3
Part 3 (form 5000-S3).

Each record of a list holds one disposition: "(Column 2): Proceeds of disposition", "(Column 3):
Adjusted cost base" and "(Column 4): Outlays and expenses"; "(Column 5): Gain or loss (column 2
minus columns 3 and 4)" is worked out. The rows below are (proceeds, adjusted cost base, outlays).
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from app.domain.artifact import Artifact, ArtifactKind
from app.domain.record_list import RecordList, RecordListKind
from app.jurisdictions.ca.catalog import (
    DISPOSITION_ADJUSTED_COST_BASE,
    DISPOSITION_OUTLAYS,
    DISPOSITION_PROCEEDS,
    PERSONAL_USE_PROPERTY_DISPOSITIONS,
    SHARE_DISPOSITIONS,
)

D = Decimal

# One disposition: proceeds (column 2), adjusted cost base (column 3), outlays (column 4).
Row = tuple[str, str, str]
GAIN: Row = ("1500.00", "1000.00", "50.00")  # column 5: 450.00
LOSS: Row = ("800.00", "1000.00", "30.00")  # column 5: -230.00
NOTHING: Row = ("500.00", "400.00", "100.00")  # column 5: 0.00


def rows(kind: RecordListKind, *given: Row) -> Artifact[Any]:
    """A record list of `kind` with one record per row, in the order given."""
    records: list[dict[ArtifactKind[Any], object]] = [
        {
            DISPOSITION_PROCEEDS: D(proceeds),
            DISPOSITION_ADJUSTED_COST_BASE: D(cost_base),
            DISPOSITION_OUTLAYS: D(outlays),
        }
        for proceeds, cost_base, outlays in given
    ]
    return Artifact(kind, RecordList(kind.fields, records))


def shares(*given: Row) -> Artifact[Any]:
    return rows(SHARE_DISPOSITIONS, *given)


def personal_use(*given: Row) -> Artifact[Any]:
    return rows(PERSONAL_USE_PROPERTY_DISPOSITIONS, *given)
