"""Builds one capability from a manifest selection (design.md §4).

The selection fills slots by identifier; whoever calls the builder resolves those identifiers to
datasets and artifact kinds. The builder checks the selection fills exactly the slots the
capability class declares, each in its own section, and that what was resolved for each slot is
what the selection names, with datasets of the slots' kinds; then it calls the constructor by
keyword. Value types of kinds are the constructor's check; the builder never calls ports.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from app.domain.artifact import ArtifactKind
from app.domain.capability import Capability
from app.domain.errors import InvalidSelectionError
from app.domain.manifest import CapabilitySelection
from app.domain.parameters.datasets import ParameterDataset

_SECTIONS = (("params", "PARAMETERS"), ("consumes", "CONSUMES"), ("produces", "PRODUCES"))
_SLOT_NOUNS = {
    "PARAMETERS": "parameter slot",
    "CONSUMES": "consumed slot",
    "PRODUCES": "produced slot",
}


class CapabilityBuilder:
    """Builds a capability of a given class from a selection and its resolved datasets and kinds."""

    def build(
        self,
        selection: CapabilitySelection,
        cls: type[Capability],
        datasets: Mapping[str, ParameterDataset[Any]],
        kinds: Mapping[str, ArtifactKind[Any]],
    ) -> Capability:
        """A `cls` built from the resolved `datasets` and `kinds`, each keyed by slot.

        Raises InvalidSelectionError naming the selection and slot if the selection does not fill
        exactly `cls`'s slots, or what was resolved for a slot is missing, extra, or not what the
        selection names.
        """
        who = self._describe(selection)
        self._check_sections(selection, cls, who)
        arguments = {
            **self._parameter_arguments(selection, cls, datasets, who),
            **self._artifact_arguments(selection, cls, kinds, who),
        }
        # `type[Capability]` cannot describe a subclass's constructor, so it is called through
        # `Callable[..., Capability]`: a deliberate, documented loosening at the manifest
        # boundary. Slot names were checked against `__init__` when the class was defined,
        # dataset kinds by `_parameter_arguments`, and kinds' value types are checked by
        # `Capability.__init__`.
        constructor: Callable[..., Capability] = cls
        return constructor(**arguments)

    def _parameter_arguments(
        self,
        selection: CapabilitySelection,
        cls: type[Capability],
        datasets: Mapping[str, ParameterDataset[Any]],
        who: str,
    ) -> dict[str, ParameterDataset[Any]]:
        """Each parameter slot's dataset, checked to be the family and kind the slot takes."""
        self._check_no_extra(datasets, cls.PARAMETERS, "dataset", "a parameter slot", cls, who)
        arguments: dict[str, ParameterDataset[Any]] = {}
        for slot, kind in cls.PARAMETERS.items():
            if slot not in datasets:
                raise InvalidSelectionError(
                    f"{who}: parameter slot {slot!r} has no resolved dataset"
                )
            dataset, family = datasets[slot], selection.params[slot]
            if dataset.family != family:
                raise InvalidSelectionError(
                    f"{who}: parameter slot {slot!r} names family {family!r}, "
                    f"but was resolved to {dataset.family!r}"
                )
            if dataset.kind != kind:
                raise InvalidSelectionError(
                    f"{who}: parameter slot {slot!r} takes a dataset of kind {kind.name!r}, "
                    f"got {dataset.family!r} of kind {dataset.kind.name!r}"
                )
            arguments[slot] = dataset
        return arguments

    def _artifact_arguments(
        self,
        selection: CapabilitySelection,
        cls: type[Capability],
        kinds: Mapping[str, ArtifactKind[Any]],
        who: str,
    ) -> dict[str, ArtifactKind[Any]]:
        """Each artifact slot's kind, checked to be the identifier the selection names for it."""
        artifact_slots = {**cls.CONSUMES, **cls.PRODUCES}
        self._check_no_extra(kinds, artifact_slots, "kind", "an artifact slot", cls, who)
        named = {**selection.consumes, **selection.produces}
        arguments: dict[str, ArtifactKind[Any]] = {}
        for slot in artifact_slots:
            if slot not in kinds:
                raise InvalidSelectionError(f"{who}: artifact slot {slot!r} has no resolved kind")
            if kinds[slot].identifier != named[slot]:
                raise InvalidSelectionError(
                    f"{who}: artifact slot {slot!r} names {named[slot]!r}, "
                    f"but was resolved to {kinds[slot].identifier!r}"
                )
            arguments[slot] = kinds[slot]
        return arguments

    @staticmethod
    def _describe(selection: CapabilitySelection) -> str:
        """The selection's name and produced identifiers, which tell repeated names apart."""
        produced = ", ".join(sorted(selection.produces.values())) or "nothing"
        return f"{selection.name} (produces {produced})"

    @staticmethod
    def _check_sections(selection: CapabilitySelection, cls: type[Capability], who: str) -> None:
        """Every key in each section names a slot of that section, and every slot is filled."""
        declared: dict[str, Mapping[str, object]] = {
            mapping: getattr(cls, mapping) for _section, mapping in _SECTIONS
        }
        for section, mapping in _SECTIONS:
            for slot in getattr(selection, section):
                if slot in declared[mapping]:
                    continue
                other = next((m for m, slots in declared.items() if slot in slots), None)
                what = "not a slot" if other is None else f"a {_SLOT_NOUNS[other]}"
                raise InvalidSelectionError(
                    f"{who}: {slot!r} is given under {section} but is {what} of {cls.__name__}"
                )
        for section, mapping in _SECTIONS:
            for slot in declared[mapping]:
                if slot not in getattr(selection, section):
                    raise InvalidSelectionError(
                        f"{who}: {_SLOT_NOUNS[mapping]} {slot!r} of {cls.__name__} "
                        f"is not filled under {section}"
                    )

    @staticmethod
    def _check_no_extra(
        resolved: Mapping[str, object],
        slots: Mapping[str, object],
        noun: str,
        slot_noun: str,
        cls: type[Capability],
        who: str,
    ) -> None:
        """Nothing was resolved for a key that is not one of `slots`."""
        for key in resolved:
            if key not in slots:
                raise InvalidSelectionError(
                    f"{who}: a {noun} was resolved for {key!r}, which is not {slot_noun} "
                    f"of {cls.__name__}"
                )
