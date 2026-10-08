"""A made-up module that registers on import, in a registry of its own."""

from app.domain.registry import NamespacedRegistry


class Thing:
    """A made-up thing to register."""


NamespacedRegistry[type[object]]().register("thing", Thing)
