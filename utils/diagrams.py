"""Diagrams attached to questions (circuits, light-gate set-ups…) as SVG in metadata["diagram"]."""
import base64


def with_diagram(question, svg):
    """Attaches an SVG diagram to a question and returns it."""
    question.metadata["diagram"] = svg
    return question


def diagram_markdown(svg, alt="Diagram"):
    """Markdown image for an SVG diagram, embedded as a data URI."""
    uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"![{alt}]({uri})"
