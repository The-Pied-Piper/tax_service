"""The design document's vocabulary: consume / produce only (design.md §2, §3).

Fold contributions were dropped in favour of list-valued consume slots, so the design document
must no longer describe them.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import app

DESIGN = Path(app.__file__).parent.parent / "design.md"


def test_the_design_document_exists() -> None:
    assert DESIGN.is_file()


@pytest.mark.parametrize("term", ["fold contribution", "contributes_to", "contribute_to"])
def test_the_design_document_does_not_mention_fold_contributions(term: str) -> None:
    assert term not in DESIGN.read_text(encoding="utf-8").lower()
