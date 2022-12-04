import markdown
from markupsafe import Markup


def markdown_filter(src: str) -> Markup:
    html = (
        markdown.markdown(src, extensions=["extra"])
        .replace("<h1>", "<h3>")
        .replace("</h1>", "</h3>")
        .replace("<h2>", "<h3>")
        .replace("</h2>", "</h3>")
    )
    return Markup(html)
