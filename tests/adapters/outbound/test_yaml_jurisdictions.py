"""Unit tests for YamlJurisdictionSource: YAML manifest files -> Jurisdiction domain object."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.domain.errors import InvalidManifestError, NotFoundError
from app.domain.jurisdiction import Jurisdiction
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Manifest

CA_ON = JurisdictionCode("CA-ON")

CA_ON_V1 = """\
jurisdiction: CA-ON
version: 1
valid_from_tax_year: 2025
capabilities:
  - name: ex/rrsp_deduction
    params_family: ca/rrsp
  - name: ex/progressive_tax
    params_family: ca-on/brackets
"""


def write(directory: Path, name: str, content: str) -> Path:
    path = directory / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content), encoding="utf-8")
    return path


def test_parses_manifest_into_domain_objects(tmp_path: Path) -> None:
    write(tmp_path, "ca-on-v1.yaml", CA_ON_V1)

    result = YamlJurisdictionSource(tmp_path).get_jurisdiction(CA_ON)

    assert result == Jurisdiction(
        code=CA_ON,
        manifests=(
            Manifest(
                jurisdiction=CA_ON,
                version=1,
                valid_from_tax_year=2025,
                capabilities=(
                    CapabilitySelection(name="ex/rrsp_deduction", params_family="ca/rrsp"),
                    CapabilitySelection(name="ex/progressive_tax", params_family="ca-on/brackets"),
                ),
            ),
        ),
    )


def test_preserves_authored_capability_order(tmp_path: Path) -> None:
    write(
        tmp_path,
        "m.yaml",
        """\
        jurisdiction: CA-ON
        version: 1
        valid_from_tax_year: 2025
        capabilities:
          - {name: ex/c, params_family: f}
          - {name: ex/a, params_family: f}
          - {name: ex/b, params_family: f}
        """,
    )

    (manifest,) = YamlJurisdictionSource(tmp_path).get_jurisdiction(CA_ON).manifests

    assert [c.name for c in manifest.capabilities] == ["ex/c", "ex/a", "ex/b"]


def test_allows_same_capability_with_different_params_families(tmp_path: Path) -> None:
    write(
        tmp_path,
        "m.yaml",
        """\
        jurisdiction: CA-ON
        version: 1
        valid_from_tax_year: 2025
        capabilities:
          - {name: ex/progressive_tax, params_family: ca/brackets}
          - {name: ex/progressive_tax, params_family: ca-on/brackets}
        """,
    )

    (manifest,) = YamlJurisdictionSource(tmp_path).get_jurisdiction(CA_ON).manifests

    assert [c.params_family for c in manifest.capabilities] == ["ca/brackets", "ca-on/brackets"]


def test_groups_every_manifest_version_of_the_jurisdiction(tmp_path: Path) -> None:
    write(tmp_path, "ca-on/v1.yaml", CA_ON_V1)
    write(tmp_path, "ca-on/v2.yml", CA_ON_V1.replace("version: 1", "version: 2"))
    write(tmp_path, "ca-bc/v1.yaml", CA_ON_V1.replace("CA-ON", "CA-BC"))
    write(tmp_path, "README.md", "not a manifest")

    result = YamlJurisdictionSource(tmp_path).get_jurisdiction(CA_ON)

    assert result.code == CA_ON
    assert sorted(m.version for m in result.manifests) == [1, 2]
    assert {m.jurisdiction for m in result.manifests} == {CA_ON}


def test_unknown_jurisdiction_is_not_found(tmp_path: Path) -> None:
    write(tmp_path, "ca-on-v1.yaml", CA_ON_V1)

    with pytest.raises(NotFoundError, match="CA-BC"):
        YamlJurisdictionSource(tmp_path).get_jurisdiction(JurisdictionCode("CA-BC"))


def test_missing_directory_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(InvalidManifestError, match="directory not found"):
        YamlJurisdictionSource(tmp_path / "nope").get_jurisdiction(CA_ON)


def test_one_bad_file_fails_the_whole_load(tmp_path: Path) -> None:
    write(tmp_path, "good.yaml", CA_ON_V1)
    write(tmp_path, "bad.yaml", CA_ON_V1 + "extra: 1\n")

    with pytest.raises(InvalidManifestError, match="bad.yaml"):
        YamlJurisdictionSource(tmp_path).get_jurisdiction(CA_ON)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param("", "manifest must be a mapping", id="empty-file"),
        pytest.param("- a\n- b\n", "manifest must be a mapping", id="document-is-list"),
        pytest.param(
            "jurisdiction: [unclosed\n", "while parsing a flow sequence", id="invalid-yaml"
        ),
        pytest.param(
            CA_ON_V1 + "version: 2\n", "duplicate key 'version'", id="duplicate-top-level-key"
        ),
        pytest.param(
            CA_ON_V1.replace(
                "    params_family: ca/rrsp\n",
                "    params_family: ca/rrsp\n    params_family: ca/other\n",
            ),
            "duplicate key 'params_family'",
            id="duplicate-capability-key",
        ),
        pytest.param(CA_ON_V1 + "edges: []\n", r"unknown keys \['edges'\]", id="unknown-key"),
        pytest.param(
            CA_ON_V1.replace(
                "    params_family: ca/rrsp\n",
                "    params_family: ca/rrsp\n    after: ex/progressive_tax\n",
            ),
            r"capabilities\[0\]: unknown keys \['after'\]",
            id="unknown-capability-key",
        ),
        pytest.param(
            CA_ON_V1.replace("version: 1\n", ""), r"missing keys \['version'\]", id="missing-key"
        ),
        pytest.param(
            CA_ON_V1.replace("    params_family: ca/rrsp\n", ""),
            r"capabilities\[0\]: missing keys \['params_family'\]",
            id="missing-capability-key",
        ),
        pytest.param(
            CA_ON_V1.replace("version: 1", "version: '1'"),
            "version must be an integer, got str",
            id="version-str",
        ),
        pytest.param(
            CA_ON_V1.replace("version: 1", "version: yes"),
            "version must be an integer, got bool",
            id="version-bool",
        ),
        pytest.param(
            CA_ON_V1.replace("version: 1", "version: 1.0"),
            "version must be an integer, got float",
            id="version-float",
        ),
        pytest.param(
            CA_ON_V1.replace("valid_from_tax_year: 2025", "valid_from_tax_year: '2025'"),
            "valid_from_tax_year must be an integer, got str",
            id="tax-year-str",
        ),
        pytest.param(
            CA_ON_V1.replace("jurisdiction: CA-ON", "jurisdiction: 1"),
            "jurisdiction must be a string, got int",
            id="jurisdiction-int",
        ),
        pytest.param(
            CA_ON_V1.replace("jurisdiction: CA-ON", "jurisdiction: ca-on"),
            "jurisdiction: invalid jurisdiction code 'ca-on'",
            id="jurisdiction-malformed-code",
        ),
        pytest.param(
            "jurisdiction: CA-ON\nversion: 1\nvalid_from_tax_year: 2025\ncapabilities: x\n",
            "capabilities must be a list",
            id="capabilities-not-list",
        ),
        pytest.param(
            "jurisdiction: CA-ON\nversion: 1\nvalid_from_tax_year: 2025\ncapabilities: [x]\n",
            r"capabilities\[0\] must be a mapping",
            id="capability-not-mapping",
        ),
        pytest.param(
            CA_ON_V1.replace("name: ex/rrsp_deduction", "name: 7"),
            r"capabilities\[0\].name must be a string, got int",
            id="capability-name-int",
        ),
    ],
)
def test_rejects_malformed_manifest(tmp_path: Path, content: str, message: str) -> None:
    write(tmp_path, "ca-on-v1.yaml", content)

    with pytest.raises(InvalidManifestError, match=message) as excinfo:
        YamlJurisdictionSource(tmp_path).get_jurisdiction(CA_ON)

    assert "ca-on-v1.yaml" in str(excinfo.value)
