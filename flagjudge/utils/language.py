import tomllib
from pathlib import Path

from flagjudge import app
from flagjudge._typing.language import *

DATA_ROOT = Path(app.root_path) / ".." / "data"


def load_languages() -> Languages:
    with open(DATA_ROOT / "langmap.toml", "rb") as f:
        return tomllib.load(f)
