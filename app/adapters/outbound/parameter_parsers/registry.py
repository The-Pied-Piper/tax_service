"""ParameterParserRegistry: the parameter parsers packages contribute, by parameter kind.

A parser registers itself with `@parameter_parser`; YamlParameterSource looks parsers up by
the kind it was asked for. Parsers are keyed by their kind's name (`brackets`, `credit`), which
is not namespaced yet.
"""

from __future__ import annotations

from typing import Any, Protocol, cast

from app.adapters.outbound.parameter_parsers.parser import ParameterParser
from app.adapters.outbound.yaml_support import YamlNode
from app.domain.errors import UnknownRegistrationError
from app.domain.parameters.kind import ParameterKind
from app.domain.registry import Registry


class ParserClass[T, P](Protocol):
    """A parser class as `@parameter_parser` sees it: its kind, its `parse`, its constructor.

    Matching both `kind` and `parse` against one `T` is what lets mypy reject a parser whose
    `parse` returns another type than its kind's values; `kind` must be a class attribute.
    """

    kind: ParameterKind[T]

    def parse(self, parser: P, document: YamlNode, /) -> T:
        """The class's `parse`, unbound: called with an instance and a dataset document."""
        ...

    def __call__(self) -> P:
        """Construct the parser."""
        ...


class ParameterParserRegistry(Registry[object]):
    """Holds one parser per parameter kind; lookups by `ParameterKind[T]` give `ParameterParser[T]`.

    Unlike other registries it is keyed by kind name rather than by a namespaced identifier.
    """

    def register[T](self, parser: ParameterParser[T]) -> ParameterParser[T]:
        """Register `parser` under its kind's name and return it; one parser per kind."""
        self._add(parser.kind.name, parser)
        return parser

    def get[T](self, kind: ParameterKind[T]) -> ParameterParser[T]:
        """The parser registered for exactly `kind` (same name and value type)."""
        # Safe: `register` stores every parser under its own kind's name, and the check below
        # confirms that kind is `kind` itself, value type included.
        parser = cast(ParameterParser[T], self._find(kind.name))
        if parser.kind != kind:
            raise UnknownRegistrationError(
                f"no parser for parameter kind {kind.name!r} with values of {kind.value_type!r}"
            )
        return parser

    def register_class[T, P: ParameterParser[Any]](self, cls: ParserClass[T, P]) -> type[P]:
        """Register an instance of the parser class `cls` and return the class unchanged."""
        parser = cls()
        self.register(parser)
        # `cls` is typed as the ParserClass protocol, not as a class; `type(parser)` is the
        # same class at run time and gives mypy `type[P]`, with no cast.
        return type(parser)


def parameter_parser[T, P: ParameterParser[Any]](cls: ParserClass[T, P]) -> type[P]:
    """Class decorator registering an instance of a parser class in the shared registry.

    A parser whose `parse` returns another type than its kind's values fails `mypy .` here
    with "Cannot infer value of type parameter".
    """
    return ParameterParserRegistry.shared().register_class(cls)
