"""EnglishRendererRegistry: the English text of each trace line class, by line class.

A renderer class names the line class it renders as `line_class` and registers itself with
`@english_renderer`, beside that line class's feature (a jurisdiction package's own lines
included); EnglishTraceRenderer looks renderers up by the exact class of each line. The string
keys are the line class's module and qualified name.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.domain.errors import DuplicateRegistrationError, UnknownRegistrationError
from app.domain.registry import Registry
from app.domain.trace import TraceLine


class EnglishRenderer(Protocol):
    """A renderer as a lookup returns it: an object naming the line class it renders."""

    @property
    def line_class(self) -> type[TraceLine]:
        """The exact line class this renderer renders."""
        ...


class EnglishRendererClass[L: TraceLine, R: EnglishRenderer](Protocol):
    """A renderer class as `@english_renderer` sees it: its line class, `render` and constructor.

    Matching both `line_class` and `render` against one `L` is what lets mypy reject a renderer
    whose `render` takes another line class than the one it names; `line_class` must be a class
    attribute.
    """

    line_class: type[L]

    def render(self, renderer: R, line: L, /) -> str:
        """The class's `render`, unbound: called with an instance and a line of `line_class`."""
        ...

    def __call__(self) -> R:
        """Construct the renderer."""
        ...


class EnglishRendering(Protocol):
    """A registered renderer, able to render any line of the class it was registered for."""

    @property
    def renderer(self) -> EnglishRenderer:
        """The registered renderer instance."""
        ...

    def text(self, line: TraceLine) -> str:
        """The English sentence for `line`, a line of the renderer's line class."""
        ...


@dataclass(frozen=True)
class _BoundRenderer[L: TraceLine, R: EnglishRenderer]:
    """A renderer instance with its class, whose `render` is typed for the class's line class."""

    renderer_class: EnglishRendererClass[L, R]
    renderer: R

    def text(self, line: TraceLine) -> str:
        """The English sentence for `line`; a line of another class is a TypeError."""
        line_class = self.renderer_class.line_class
        if not isinstance(line, line_class):
            raise TypeError(
                f"the English renderer for {line_class.__name__} cannot render a "
                f"{type(line).__name__}"
            )
        return self.renderer_class.render(self.renderer, line)


class EnglishRendererRegistry(Registry[EnglishRendering]):
    """Holds one English renderer per trace line class, looked up by the exact line class.

    Register renderers with `register_class` or `@english_renderer`; a subclass of a registered
    line class has no renderer until one is registered for it.
    """

    def register_class[L: TraceLine, R: EnglishRenderer](
        self, cls: EnglishRendererClass[L, R]
    ) -> type[R]:
        """Register an instance of `cls` under its line class and return the class unchanged."""
        renderer = cls()
        bound: _BoundRenderer[L, R] = _BoundRenderer(cls, renderer)
        try:
            self.register(self._key(cls.line_class), bound)
        except DuplicateRegistrationError:
            raise DuplicateRegistrationError(
                f"an English renderer for trace line {cls.line_class.__name__} is already "
                "registered"
            ) from None
        # `cls` is typed as the EnglishRendererClass protocol, not as a class; `type(renderer)`
        # is the same class at run time and gives mypy `type[R]`, with no cast.
        return type(renderer)

    def rendering_for(self, line_class: type[TraceLine]) -> EnglishRendering:
        """The renderer registered for exactly `line_class`, ready to render its lines."""
        try:
            found = self.get(self._key(line_class))
        except UnknownRegistrationError:
            found = None
        if found is None or found.renderer.line_class is not line_class:
            raise UnknownRegistrationError(
                f"no English renderer is registered for trace line {line_class.__name__}"
            )
        return found

    def for_line_class(self, line_class: type[TraceLine]) -> EnglishRenderer:
        """The renderer instance registered for exactly `line_class`."""
        return self.rendering_for(line_class).renderer

    @staticmethod
    def _key(line_class: type[TraceLine]) -> str:
        """The string key of `line_class`: its module and qualified name."""
        return f"{line_class.__module__}.{line_class.__qualname__}"


def english_renderer[L: TraceLine, R: EnglishRenderer](
    cls: EnglishRendererClass[L, R],
) -> type[R]:
    """Class decorator registering an instance of a renderer class in the shared registry.

    A renderer whose `render` takes another line class than its `line_class` fails `mypy .` here
    with "Cannot infer value of type parameter".
    """
    return EnglishRendererRegistry.shared().register_class(cls)
