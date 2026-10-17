"""Unit tests for YamlJurisdictionSource: YAML manifest files -> Jurisdiction domain object.

The source takes a mapping of namespace -> package directory. A jurisdiction's namespace is its
code lower-cased (`EX-ON` -> `ex-on`, `EX` -> `ex`), and its manifests are every `*.yaml` /
`*.yml` file under `roots[Namespace("ex-on")] / "manifests"`, recursively. Names are made up.

Each selection names a capability and fills its slots: `params` (slot -> family, optional),
`consumes` (slot -> artifact identifier, or a list of them kept in order as a tuple, optional)
and `produces` (slot -> artifact identifier, required). Slot names, and whether a slot takes one
identifier or a list, are not checked against capability classes here. The top-level `inputs` and
`outputs` list the computation's artifact identifiers: both required, non-empty lists of non-empty
strings without duplicates, and no identifier in both.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from textwrap import dedent
from types import MappingProxyType

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
inputs:
  - ex/gross_income
  - ex/taxable_base
outputs:
  - ex/savings_deduction
  - ex-on/levy
capabilities:
  - name: ex/savings_deduction
    params:
      cap: ex/savings_cap
      rate: ex/savings_rate
    consumes:
      income: ex/gross_income
    produces:
      output: ex/savings_deduction
  - name: ex/progressive_tax
    params:
      schedule: ex-on/brackets
    consumes:
      base: ex/taxable_base
    produces:
      output: ex-on/levy
"""


HEADER = """\
jurisdiction: EX-ON
version: 1
valid_from_tax_year: 2025
inputs: [ex/x]
outputs: [ex/y]
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
                inputs=frozenset({"ex/gross_income", "ex/taxable_base"}),
                outputs=frozenset({"ex/savings_deduction", "ex-on/levy"}),
                capabilities=(
                    CapabilitySelection(
                        name="ex/savings_deduction",
                        params={"cap": "ex/savings_cap", "rate": "ex/savings_rate"},
                        consumes={"income": "ex/gross_income"},
                        produces={"output": "ex/savings_deduction"},
                    ),
                    CapabilitySelection(
                        name="ex/progressive_tax",
                        params={"schedule": "ex-on/brackets"},
                        consumes={"base": "ex/taxable_base"},
                        produces={"output": "ex-on/levy"},
                    ),
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
        inputs: [ex/x]
        outputs: [ex/y]
        capabilities:
          - {name: ex/c, produces: {output: ex/c}}
          - {name: ex/a, produces: {output: ex/a}}
          - {name: ex/b, produces: {output: ex/b}}
        """,
    )

    (manifest,) = source(tmp_path).get_jurisdiction(EX_ON).manifests

    assert [c.name for c in manifest.capabilities] == ["ex/c", "ex/a", "ex/b"]


def test_allows_same_capability_with_different_bindings(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex-on/manifests/m.yaml",
        """\
        jurisdiction: EX-ON
        version: 1
        valid_from_tax_year: 2025
        inputs: [ex/x]
        outputs: [ex/y]
        capabilities:
          - name: ex/progressive_tax
            params: {schedule: ex/brackets}
            consumes: {base: ex/taxable_base}
            produces: {output: ex/levy}
          - name: ex/progressive_tax
            params: {schedule: ex-on/brackets}
            consumes: {base: ex/taxable_base}
            produces: {output: ex-on/levy}
        """,
    )

    (manifest,) = source(tmp_path).get_jurisdiction(EX_ON).manifests

    assert [c.params for c in manifest.capabilities] == [
        {"schedule": "ex/brackets"},
        {"schedule": "ex-on/brackets"},
    ]
    assert [c.produces for c in manifest.capabilities] == [
        {"output": "ex/levy"},
        {"output": "ex-on/levy"},
    ]


def test_params_and_consumes_may_be_omitted(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex-on/manifests/m.yaml",
        """\
        jurisdiction: EX-ON
        version: 1
        valid_from_tax_year: 2025
        inputs: [ex/x]
        outputs: [ex/y]
        capabilities:
          - name: ex/flat_grant
            produces:
              output: ex/grant
        """,
    )

    (manifest,) = source(tmp_path).get_jurisdiction(EX_ON).manifests

    assert manifest.capabilities == (
        CapabilitySelection(
            name="ex/flat_grant", params={}, consumes={}, produces={"output": "ex/grant"}
        ),
    )


def test_a_consumed_slot_may_list_identifiers(tmp_path: Path) -> None:
    write(
        tmp_path,
        "ex-on/manifests/m.yaml",
        HEADER
        + """\
capabilities:
  - name: ex/total_up
    consumes:
      base: ex/x
      parts:
        - ex/c
        - ex/a
        - ex/b
      others: [ex/d]
      none: []
    produces:
      total: ex/y
""",
    )

    (manifest,) = source(tmp_path).get_jurisdiction(EX_ON).manifests

    assert manifest.capabilities == (
        CapabilitySelection(
            name="ex/total_up",
            params={},
            consumes={
                "base": "ex/x",
                "parts": ("ex/c", "ex/a", "ex/b"),
                "others": ("ex/d",),
                "none": (),
            },
            produces={"total": "ex/y"},
        ),
    )
    (selection,) = manifest.capabilities
    assert isinstance(selection.consumes["base"], str)
    assert isinstance(selection.consumes["parts"], tuple)


def test_slot_bindings_are_read_only(tmp_path: Path) -> None:
    write(tmp_path, "ex-on/manifests/v1.yaml", EX_ON_V1)

    (manifest,) = source(tmp_path).get_jurisdiction(EX_ON).manifests

    for selection in manifest.capabilities:
        for bindings in (selection.params, selection.consumes, selection.produces):
            assert isinstance(bindings, MappingProxyType)


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
                "  - name: ex/savings_deduction\n",
                "  - name: ex/savings_deduction\n    name: ex/other\n",
            ),
            "duplicate key 'name'",
            id="duplicate-capability-key",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "      cap: ex/savings_cap\n", "      cap: ex/savings_cap\n      cap: ex/other\n"
            ),
            "duplicate key 'cap'",
            id="duplicate-parameter-slot",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "      base: ex/taxable_base\n",
                "      base: ex/taxable_base\n      base: ex/other\n",
            ),
            "duplicate key 'base'",
            id="duplicate-consumed-slot",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "      output: ex/savings_deduction\n",
                "      output: ex/savings_deduction\n      output: ex/other\n",
            ),
            "duplicate key 'output'",
            id="duplicate-produced-slot",
        ),
        pytest.param(EX_ON_V1 + "edges: []\n", r"unknown keys \['edges'\]", id="unknown-key"),
        pytest.param(
            EX_ON_V1.replace(
                "  - name: ex/savings_deduction\n",
                "  - name: ex/savings_deduction\n    after: ex/progressive_tax\n",
            ),
            r"capabilities\[0\]: unknown keys \['after'\]",
            id="unknown-capability-key",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "  - name: ex/savings_deduction\n",
                "  - name: ex/savings_deduction\n    params_family: ex/savings\n",
            ),
            r"capabilities\[0\]: unknown keys \['params_family'\]",
            id="params-family-no-longer-accepted",
        ),
        pytest.param(
            EX_ON_V1.replace("version: 1\n", ""), r"missing keys \['version'\]", id="missing-key"
        ),
        pytest.param(
            EX_ON_V1.replace("  - name: ex/savings_deduction\n", "  -\n"),
            r"capabilities\[0\]: missing keys? \[?'name'",
            id="missing-capability-name",
        ),
        pytest.param(
            EX_ON_V1.replace("    produces:\n      output: ex/savings_deduction\n", ""),
            r"capabilities\[0\]: missing keys? \[?'produces'",
            id="missing-produces",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "    produces:\n      output: ex/savings_deduction\n", "    produces: {}\n"
            ),
            r"capabilities\[0\]\.produces must name at least one slot",
            id="produces-empty",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "      output: ex/savings_deduction", '      "": ex/savings_deduction'
            ),
            r"capabilities\[0\]\.produces: keys must not be empty",
            id="produced-slot-empty",
        ),
        pytest.param(
            EX_ON_V1.replace("      output: ex/savings_deduction", '      output: ""'),
            r"capabilities\[0\]\.produces\.output must not be empty",
            id="produced-identifier-empty",
        ),
        pytest.param(
            EX_ON_V1.replace("      cap: ex/savings_cap", "      cap: 7"),
            r"capabilities\[0\]\.params\.cap must be a string, got int",
            id="parameter-family-int",
        ),
        pytest.param(
            EX_ON_V1.replace("      income: ex/gross_income", "      income: [ex/gross_income, 7]"),
            r"capabilities\[0\]\.consumes\.income\[1\] must be a string, got int",
            id="consumed-list-element-int",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "      income: ex/gross_income", '      income: [ex/gross_income, ""]'
            ),
            r"capabilities\[0\]\.consumes\.income\[1\] must not be empty",
            id="consumed-list-element-empty",
        ),
        pytest.param(
            EX_ON_V1.replace("      income: ex/gross_income", "      income: [[ex/gross_income]]"),
            r"capabilities\[0\]\.consumes\.income\[0\] must be a string, got list",
            id="consumed-list-element-list",
        ),
        pytest.param(
            EX_ON_V1.replace("      income: ex/gross_income", "      income: {a: ex/gross_income}"),
            r"capabilities\[0\]\.consumes\.income must be a string.*got dict",
            id="consumed-identifier-mapping",
        ),
        pytest.param(
            EX_ON_V1.replace("      cap: ex/savings_cap", "      cap: [ex/savings_cap]"),
            r"capabilities\[0\]\.params\.cap must be a string, got list",
            id="parameter-family-list",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "      output: ex/savings_deduction", "      output: [ex/savings_deduction]"
            ),
            r"capabilities\[0\]\.produces\.output must be a string, got list",
            id="produced-identifier-list",
        ),
        pytest.param(
            EX_ON_V1.replace("      output: ex/savings_deduction", "      output: null"),
            r"capabilities\[0\]\.produces\.output must be a string, got NoneType",
            id="produced-identifier-null",
        ),
        pytest.param(
            EX_ON_V1.replace("      cap: ex/savings_cap", "      7: ex/savings_cap"),
            r"capabilities\[0\]\.params.*7.*must be a string",
            id="slot-name-int",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "    params:\n      cap: ex/savings_cap\n      rate: ex/savings_rate\n",
                "    params: [ex/savings_cap]\n",
            ),
            r"capabilities\[0\]\.params must be a mapping",
            id="params-list",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "    params:\n      cap: ex/savings_cap\n      rate: ex/savings_rate\n",
                "    params:\n",
            ),
            r"capabilities\[0\]\.params must be a mapping",
            id="params-null",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "    consumes:\n      income: ex/gross_income\n", "    consumes: ex/gross_income\n"
            ),
            r"capabilities\[0\]\.consumes must be a mapping",
            id="consumes-string",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "    produces:\n      output: ex/savings_deduction\n",
                "    produces: ex/savings_deduction\n",
            ),
            r"capabilities\[0\]\.produces must be a mapping",
            id="produces-string",
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
            HEADER + "capabilities: x\n",
            "capabilities must be a list",
            id="capabilities-not-list",
        ),
        pytest.param(
            HEADER + "capabilities: [x]\n",
            r"capabilities\[0\] must be a mapping",
            id="capability-not-mapping",
        ),
        pytest.param(
            EX_ON_V1.replace("name: ex/savings_deduction", "name: 7"),
            r"capabilities\[0\].name must be a string, got int",
            id="capability-name-int",
        ),
        pytest.param(
            EX_ON_V1.replace("inputs:\n  - ex/gross_income\n  - ex/taxable_base\n", ""),
            r"missing keys \['inputs'\]",
            id="missing-inputs",
        ),
        pytest.param(
            EX_ON_V1.replace("outputs:\n  - ex/savings_deduction\n  - ex-on/levy\n", ""),
            r"missing keys \['outputs'\]",
            id="missing-outputs",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "inputs:\n  - ex/gross_income\n  - ex/taxable_base\n", "inputs: ex/gross_income\n"
            ),
            "inputs must be a list",
            id="inputs-not-list",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "outputs:\n  - ex/savings_deduction\n  - ex-on/levy\n", "outputs: {a: ex/levy}\n"
            ),
            "outputs must be a list",
            id="outputs-not-list",
        ),
        pytest.param(
            EX_ON_V1.replace("inputs:\n  - ex/gross_income\n  - ex/taxable_base\n", "inputs: []\n"),
            "inputs must name at least one artifact",
            id="inputs-empty",
        ),
        pytest.param(
            EX_ON_V1.replace(
                "outputs:\n  - ex/savings_deduction\n  - ex-on/levy\n", "outputs: []\n"
            ),
            "outputs must name at least one artifact",
            id="outputs-empty",
        ),
        pytest.param(
            EX_ON_V1.replace("inputs:\n  - ex/gross_income\n", "inputs:\n  - 7\n"),
            r"inputs\[0\] must be a string, got int",
            id="input-int",
        ),
        pytest.param(
            EX_ON_V1.replace("  - ex-on/levy\n", "  - null\n"),
            r"outputs\[1\] must be a string, got NoneType",
            id="output-null",
        ),
        pytest.param(
            EX_ON_V1.replace("inputs:\n  - ex/gross_income\n", 'inputs:\n  - ""\n'),
            r"inputs\[0\] must not be empty",
            id="input-empty-string",
        ),
        pytest.param(
            EX_ON_V1.replace("  - ex/taxable_base\n", "  - ex/gross_income\n"),
            r"inputs\[1\]: 'ex/gross_income' is listed more than once",
            id="input-duplicate",
        ),
        pytest.param(
            EX_ON_V1.replace("  - ex-on/levy\n", "  - ex/savings_deduction\n"),
            r"outputs\[1\]: 'ex/savings_deduction' is listed more than once",
            id="output-duplicate",
        ),
        pytest.param(
            EX_ON_V1.replace("  - ex-on/levy\n", "  - ex/taxable_base\n"),
            "'ex/taxable_base' is both an input and an output",
            id="input-also-output",
        ),
    ],
)
def test_rejects_malformed_manifest(tmp_path: Path, content: str, message: str) -> None:
    write(tmp_path, "ex-on/manifests/ex-on-v1.yaml", content)

    with pytest.raises(InvalidManifestError, match=message) as excinfo:
        source(tmp_path).get_jurisdiction(EX_ON)

    assert "ex-on-v1.yaml" in str(excinfo.value)
