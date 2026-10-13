"""Jurisdiction packages: one package per jurisdiction, holding everything specific to it.

Each package has an `__init__.py` declaring its `NAMESPACE`, a `catalog.py` declaring its
artifact kinds, `manifests/` selecting capabilities and `parameters/` holding its datasets.
Real jurisdiction names appear only here and in the mirrored `tests/jurisdictions/`.
"""
