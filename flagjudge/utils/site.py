from pathlib import Path

from flagjudge import app


def load_notification() -> str:
    path = Path(app.root_path) / ".." / "data" / "notification.md"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return f.read()
    else:
        return ""
