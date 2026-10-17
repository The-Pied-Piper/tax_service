"""Every worked return in `returns/`, computed end to end and checked line by line.

One test runs per `*.yaml` file in `returns/` (the pytest id is the file stem): the file's inputs
go through the service the composition root builds, and each expected line must equal the
worksheet's artifact exactly. A file must list every output its manifest declares. Adding a
return is adding a file.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.domain.artifact import ArtifactRegistry
from app.main import build_tax_computation
from app.registrations import JURISDICTIONS
from tests.jurisdictions.ca_on.worked_return import WorkedReturn, WorkedReturnError

RETURNS = Path(__file__).parent / "returns"


def check(path: Path) -> None:
    """Load the worked return at `path`, compute it and assert every expected line."""
    service = build_tax_computation()  # registers the catalogs the loader resolves through
    worked = WorkedReturn.load(path, ArtifactRegistry.shared())
    manifest = (
        YamlJurisdictionSource(JURISDICTIONS.roots())
        .get_jurisdiction(worked.jurisdiction)
        .manifest_for(worked.tax_year)
    )
    worked.require_outputs(manifest.outputs)

    worksheet = service.compute(worked.jurisdiction, worked.tax_year, *worked.inputs)

    for expected in worked.expected:
        assert worksheet.get(expected.kind) == expected, f"{path.name}: {expected.kind.identifier}"


@pytest.mark.parametrize("path", WorkedReturn.discover(RETURNS), ids=lambda path: path.stem)
def test_worked_return(path: Path) -> None:
    check(path)


def test_return_a_is_a_worked_return() -> None:
    assert RETURNS / "2025_return_a.yaml" in WorkedReturn.discover(RETURNS)


def test_a_new_file_is_a_new_worked_return_without_a_test_change(tmp_path: Path) -> None:
    (tmp_path / "2025_return_a.yaml").write_text((RETURNS / "2025_return_a.yaml").read_text())
    (tmp_path / "2025_low_income.yaml").write_text(
        """\
jurisdiction: CA-ON
tax_year: 2025
description: Taxable income of 10000; each credit exceeds its tax, leaving zero.
sources:
  - T1 and ON428 arithmetic on the 2025 figures.
inputs:
  ca/taxable_income: "10000"
expected:
  ca/federal_basic_tax: "1450"
  ca/federal_tax_after_credits: "0"
  ca-on/ontario_basic_tax: "505"
  ca-on/ontario_tax_after_credits: "0"
"""
    )

    found = WorkedReturn.discover(tmp_path)

    assert [path.stem for path in found] == ["2025_low_income", "2025_return_a"]
    for path in found:
        check(path)


def test_a_wrong_expected_amount_fails_naming_the_file_and_line(tmp_path: Path) -> None:
    text = (RETURNS / "2025_return_a.yaml").read_text().replace('"8539.5965"', '"8539.59"')
    path = tmp_path / "wrong.yaml"
    path.write_text(text)

    with pytest.raises(AssertionError, match=r"wrong\.yaml: ca-on/ontario_basic_tax"):
        check(path)


def test_a_file_missing_a_declared_output_fails_naming_the_file_and_output(
    tmp_path: Path,
) -> None:
    text = (RETURNS / "2025_return_a.yaml").read_text()
    path = tmp_path / "partial.yaml"
    path.write_text(text.replace('  ca-on/ontario_tax_after_credits: "7895.873"\n', ""))

    with pytest.raises(WorkedReturnError, match=r"partial\.yaml.*ca-on/ontario_tax_after_credits"):
        check(path)
