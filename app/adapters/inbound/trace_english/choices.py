"""English text for the trace lines of `app.domain.trace.choices`: one renderer class
per line class, each registered with `@english_renderer`.
"""

from __future__ import annotations

from app.adapters.inbound.trace_english.figures import EnglishFigures
from app.adapters.inbound.trace_english.registry import english_renderer
from app.domain.trace.choices import (
    ChosenByCountLine,
    ChosenByRangeLine,
    ConditionLine,
    ConditionsCountLine,
)


@english_renderer
class ChosenByCountRenderer(EnglishFigures):
    """English text for ChosenByCountLine."""

    line_class = ChosenByCountLine

    def render(self, line: ChosenByCountLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        count_kind = line.count_kind
        count = line.count
        chosen_kind = line.chosen_kind
        chosen = line.chosen_value
        return (
            f"{output.label}: {chosen_kind.label} {self._money(chosen)}, "
            f"chosen as {count_kind.label} is {count}"
        )


@english_renderer
class ChosenByRangeRenderer(EnglishFigures):
    """English text for ChosenByRangeLine."""

    line_class = ChosenByRangeLine

    def render(self, line: ChosenByRangeLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        tested_kind = line.tested_kind
        tested = line.tested_value
        chosen_kind = line.chosen_kind
        chosen = line.chosen_value
        return (
            f"{output.label}: {chosen_kind.label} {self._money(chosen)}, "
            f"chosen as {tested_kind.label} is {self._money(tested)}"
        )


@english_renderer
class ConditionRenderer(EnglishFigures):
    """English text for ConditionLine."""

    line_class = ConditionLine

    def render(self, line: ConditionLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        position = line.position
        text = line.text
        reads = line.reads
        applies = line.applies
        figures = ", ".join(
            f"{kind.label} {value if isinstance(value, int) else self._money(value)}"
            for kind, value in reads
        )
        verdict = "applies" if applies else "does not apply"
        return f'{output.label}: condition {position} "{text}": {figures}, {verdict}'


@english_renderer
class ConditionsCountRenderer(EnglishFigures):
    """English text for ConditionsCountLine."""

    line_class = ConditionsCountLine

    def render(self, line: ConditionsCountLine) -> str:
        """The English sentence for `line`."""
        output = line.output
        applied = line.applied
        count = line.count
        if not applied:
            which = "no condition applies"
        elif len(applied) == 1:
            which = f"condition {applied[0]} applies"
        else:
            which = f"conditions {', '.join(str(position) for position in applied)} apply"
        return f"{output.label}: {which}, so {count}"
