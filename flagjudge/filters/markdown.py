import markdown
from markupsafe import Markup


def markdown_filter(src: str) -> Markup:
    html = markdown.markdown(src, extensions=["extra"])
    return Markup(html)
