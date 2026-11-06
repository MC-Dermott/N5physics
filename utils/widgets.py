"""Extra interactive visualisations that can be attached to any question.

`question.metadata["widget_html"]` holds a question's own (single) simulation.  Simulations
that apply to a whole family of questions are added alongside it in
`question.metadata["extra_widgets"]` (a list of {"title", "html", "height"}) and rendered
by `core/ui/scaffold_ui.render_widget` as separate expanders.
"""
import functools
import pathlib

_DATA = pathlib.Path(__file__).parent.parent / "core" / "data"
_NEWTON_HTML = (_DATA / "newtons_laws_widget.html").read_text(encoding="utf-8")


def add_newton_widget(question):
    """Attach the Newton's Laws simulator (forces linked to motion) to a question."""
    extras = question.metadata.setdefault("extra_widgets", [])
    if not any(w["title"] == "Newton's Laws Simulator" for w in extras):
        extras.append({"title": "Newton's Laws Simulator", "html": _NEWTON_HTML, "height": 1350})
    return question


def with_newton_widget(gen):
    """Wrap a question generator so every question it returns carries the Newton's Laws simulator."""
    @functools.wraps(gen)
    def wrapped(*args, **kwargs):
        return add_newton_widget(gen(*args, **kwargs))
    wrapped._newton_wrapped = True
    return wrapped
