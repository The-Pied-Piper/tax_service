"""The CA-ON package: its namespace and where its data and manifest live."""

from __future__ import annotations

from pathlib import Path

import app.jurisdictions.ca_on


def test_declares_its_namespace() -> None:
    assert app.jurisdictions.ca_on.NAMESPACE == "ca-on"


def test_holds_its_manifest_and_parameter_data() -> None:
    directory = Path(app.jurisdictions.ca_on.__file__).parent

    assert (directory / "manifests" / "v1.yaml").is_file()
    assert (directory / "parameters" / "brackets" / "2025.yaml").is_file()
    assert (directory / "parameters" / "basic_personal_amount" / "2025.yaml").is_file()
    assert (directory / "parameters" / "credit_rate" / "2025.yaml").is_file()
