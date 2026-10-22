"""English text for the trace line of `app.domain.trace.forms`: one renderer class, registered
with `@english_renderer`.
"""

from __future__ import annotations

from app.adapters.inbound.trace_english.registry import english_renderer
from app.adapters.inbound.trace_english.renderer import EnglishTraceRenderer
from app.domain.trace.forms import FormInstanceLine


@english_renderer
class FormInstanceRenderer:
    """English text for FormInstanceLine."""

    line_class = FormInstanceLine

    def render(self, line: FormInstanceLine) -> str:
        """The English sentences for the instance's lines, one per line, each prefixed."""
        prefix = f"{line.form}, instance {line.position}: "
        sentences = EnglishTraceRenderer().render_all(line.lines)
        return "\n".join(f"{prefix}{sentence}" for sentence in sentences)
