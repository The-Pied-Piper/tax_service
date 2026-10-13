"""Unit tests for YamlJurisdictionSource: YAML manifest files -> Jurisdiction domain object.

The source takes a mapping of namespace -> package directory. A jurisdiction's namespace is its
code lower-cased (`EX-ON` -> `ex-on`, `EX` -> `ex`), and its manifests are every `*.yaml` /
`*.yml` file under `roots[Namespace("ex-on")] / "manifests"`, recursively. Names are made up.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from textwrap import dedent

import pytest

from app.adapters.outbound.yaml_jurisdictions import YamlJurisdictionSource
from app.domain.errors import InvalidManifestError, NotFoundError
from app.domain.jurisdiction import Jurisdiction
from app.domain.jurisdiction_code import JurisdictionCode
from app.domain.manifest import CapabilitySelection, Manifest
from app.domain.registry import Namespace

EX_ON = JurisdictionCode("EX-ON")

EX_ON_V1 = """\
jurisdiction: EX-ON
version: 1
valid_from_tax_year: 2025
capabilities:
  - name: ex/savings_deduction
    params_family: ex/savings
  - name: ex/progressive_tax
    params_family: ex-on/brackets
"""


def roots(directory: Path) -> Mapping[Namespace, Path]:
    """One made-up package, namespace `ex-on`, whose directory is `<directory>/ex-on`."""
    return {Namespace("ex-on"): directory / "ex-on"}


def source(directory: Path) -> YamlJurisdictionSource:
    return YamlJurisdictionSource(roots(directory))


def write(directory: Path, name: str, content: str) -> Path:
    path = directory / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content), encoding="utf-8")
    return path


def test_parses_manifest_into_domain_objects(tmp_path: Path) -> None:
    write(tmp_path, "ex-on/manifests/v1.yaml", EX_ON_V1)

    result = source(tmp_path).get_jurisdiction(EX_ON)

    assert result == Jurisdiction(
        code=EX_ON,
        manifests=(
            Manifest(
                jurisdiction=EX_ON,
                version=1,
                valid_from_tax_year=2025,
                capabilities=(
                    CapabilitySelection(name="ex/savings_deduction", params_family="ex/savings"),
                    CapabilitySelection(name="ex/progressive_tax", params_family="ex-on/brackets"),
                ),
            ),
        ),
    )


def test_preserves_authored_capability_order(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex-on/manifests/m.yaml",
        """\
        jurisdiction: EX-ON
        version: 1
        valid_from_tax_year: 2025
        capabilities:
          - {name: ex/c, params_family: f}
          - {name: ex/a, params_family: f}
          - {name: ex/b, params_family: f}
        """,
    )

    (manifest,) = source(tmp_path).get_jurisdiction(EX_ON).manifests

    assert [c.name for c in manifest.capabilities] == ["ex/c", "ex/a", "ex/b"]


def test_allows_same_capability_with_different_params_families(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex-on/manifests/m.yaml",
        """\
        jurisdiction: EX-ON
        version: 1
        valid_from_tax_year: 2025
        capabilities:
          - {name: ex/progressive_tax, params_family: ex/brackets}
          - {name: ex/progressive_tax, params_family: ex-on/brackets}
        """,
    )

    (manifest,) = source(tmp_path).get_jurisdiction(EX_ON).manifests

    assert [c.params_family for c in manifest.capabilities] == ["ex/brackets", "ex-on/brackets"]


def test_groups_every_manifest_version_of_the_jurisdiction(tmp_path: Path) -> None:
    write(tmp_path, "ex-on/manifests/v1.yaml", EX_ON_V1)
    write(tmp_path, "ex-on/manifests/older/v2.yml", EX_ON_V1.replace("version: 1", "version: 2"))
    write(tmp_path, "ex-on/manifests/README.md", "not a manifest")

    result = source(tmp_path).get_jurisdiction(EX_ON)

    assert result.code == EX_ON
    assert sorted(m.version for m in result.manifests) == [1, 2]
    assert {m.jurisdiction for m in result.manifests} == {EX_ON}


def test_reads_only_the_manifests_directory_of_the_jurisdictions_namespace(
    tmp_path: Path,
) -> None:
    ex_zz = JurisdictionCode("EX-ZZ")
    write(tmp_path, "pkg_on/manifests/v1.yaml", EX_ON_V1)
    write(tmp_path, "pkg_on/parameters/stray.yaml", EX_ON_V1.replace("version: 1", "version: 9"))
    write(tmp_path, "pkg_zz/manifests/v1.yaml", EX_ON_V1.replace("EX-ON", "EX-ZZ"))
    two = YamlJurisdictionSource(
        {Namespace("ex-on"): tmp_path / "pkg_on", Namespace("ex-zz"): tmp_path / "pkg_zz"}
    )

    on = two.get_jurisdiction(EX_ON)
    zz = two.get_jurisdiction(ex_zz)

    assert [m.version for m in on.manifests] == [1]
    assert {m.jurisdiction for m in on.manifests} == {EX_ON}
    assert {m.jurisdiction for m in zz.manifests} == {ex_zz}


def test_a_country_code_maps_to_its_lowercase_namespace(tmp_path: Path) -> None:
    write(tmp_path, "ex/manifests/v1.yaml", EX_ON_V1.replace("EX-ON", "EX"))

    result = YamlJurisdictionSource({Namespace("ex"): tmp_path / "ex"}).get_jurisdiction(
        JurisdictionCode("EX")
    )

    assert result.code == JurisdictionCode("EX")


def test_jurisdiction_without_a_namespace_root_is_not_found(tmp_path: Path) -> None:
    write(tmp_path, "ex-on/manifests/v1.yaml", EX_ON_V1)

    with pytest.raises(NotFoundError, match="EX-ZZ.*'ex-zz'"):
        source(tmp_path).get_jurisdiction(JurisdictionCode("EX-ZZ"))


def test_package_without_manifests_is_not_found(tmp_path: Path) -> None:
    (tmp_path / "ex-on").mkdir()

    with pytest.raises(NotFoundError, match="no manifests for jurisdiction EX-ON"):
        source(tmp_path).get_jurisdiction(EX_ON)


def test_missing_package_directory_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(InvalidManifestError, match="directory not found"):
        YamlJurisdictionSource({Namespace("ex-on"): tmp_path / "nope"}).get_jurisdiction(EX_ON)


def test_a_manifest_for_another_jurisdiction_in_the_package_is_rejected(tmp_path: Path) -> None:
    write(tmp_path, "ex-on/manifests/v1.yaml", EX_ON_V1)
    write(tmp_path, "ex-on/manifests/stray.yaml", EX_ON_V1.replace("EX-ON", "EX-ZZ"))

    with pytest.raises(InvalidManifestError, match="stray.yaml.*EX-ZZ"):
        source(tmp_path).get_jurisdiction(EX_ON)


def test_one_bad_file_fails_the_whole_load(tmp_path: Path) -> None:
    write(tmp_path, "ex-on/manifests/good.yaml", EX_ON_V1)
    write(tmp_path, "ex-on/manifests/bad.yaml", EX_ON_V1 + "extra: 1\n")

    with pytest.raises(InvalidManifestError, match="bad.yaml"):
        source(tmp_path).get_jurisdiction(EX_ON)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        pytest.param("", "manifest must be a mapping", id="empty-file"),
        pytest.param("- a\n- b\n", "manifest must be a mapping", id="document-is-list"),
        pytest.param(
            "jurisdiction: [unclosed\n", "while parsing a flow sequence", id="invalid-yaml"
        ),
        pytest.param(
            EX_ON_V1 + "version: 2\n", "duplicate key 'version'", id="duplicate-top-level-key"
        ),
        pytest.param(
            EX_ON_V1.replace(
                "    params_family: ex/savings\n",
                "    params_family: ex/savings\n    params_family: ex/other\n",
            ),
            "duplicate key 'params_family'",
            id="duplicate-capability-key",
        ),
        pytest.param(EX_ON_V1 + "edges: []\n", r"unknown keys \['edges'\]", id="unknown-key"),
        pytest.param(
            EX_ON_V1.replace(
                "    params_family: ex/savings\n",
                "    params_family: ex/savings\n    after: ex/progressive_tax\n",
            ),
            r"capabilities\[0\]: unknown keys \['after'\]",
            id="unknown-capability-key",
        ),
        pytest.param(
            EX_ON_V1.replace("version: 1\n", ""), r"missing keys \['version'\]", id="missing-key"
        ),
        pytest.param(
            EX_ON_V1.replace("    params_family: ex/savings\n", ""),
            r"capabilities\[0\]: missing keys \['params_family'\]",
            id="missing-capability-key",
        ),
        pytest.param(
            EX_ON_V1.replace("version: 1", "version: '1'"),
            "version must be an integer, got str",
            id="version-str",
        ),
        pytest.param(
            EX_ON_V1.replace("version: 1", "version: yes"),
            "version must be an integer, got bool",
            id="version-bool",
        ),
        pytest.param(
            EX_ON_V1.replace("version: 1", "version: 1.0"),
            "version must be an integer, got float",
            id="version-float",
        ),
        pytest.param(
            EX_ON_V1.replace("valid_from_tax_year: 2025", "valid_from_tax_year: '2025'"),
            "valid_from_tax_year must be an integer, got str",
            id="tax-year-str",
        ),
        pytest.param(
            EX_ON_V1.replace("jurisdiction: EX-ON", "jurisdiction: 1"),
            "jurisdiction must be a string, got int",
            id="jurisdiction-int",
        ),
        pytest.param(
            EX_ON_V1.replace("jurisdiction: EX-ON", "jurisdiction: ex-on"),
            "jurisdiction: invalid jurisdiction code 'ex-on'",
            id="jurisdiction-malformed-code",
        ),
        pytest.param(
            "jurisdiction: EX-ON\nversion: 1\nvalid_from_tax_year: 2025\ncapabilities: x\n",
            "capabilities must be a list",
            id="capabilities-not-list",
        ),
        pytest.param(
            "jurisdiction: EX-ON\nversion: 1\nvalid_from_tax_year: 2025\ncapabilities: [x]\n",
            r"capabilities\[0\] must be a mapping",
            id="capability-not-mapping",
        ),
        pytest.param(
            EX_ON_V1.replace("name: ex/savings_deduction", "name: 7"),
            r"capabilities\[0\].name must be a string, got int",
            id="capability-name-int",
        ),
    ],
)
def test_rejects_malformed_manifest(tmp_path: Path, content: str, message: str) -> None:
    write(tmp_path, "ex-on/manifests/ex-on-v1.yaml", content)

    with pytest.raises(InvalidManifestError, match=message) as excinfo:
        source(tmp_path).get_jurisdiction(EX_ON)

    assert "ex-on-v1.yaml" in str(excinfo.value)
