import tomllib
from pathlib import Path

from flask import g

from flagjudge import app
from flagjudge._typing.language import *

DATA_ROOT = Path(app.root_path) / ".." / "data"


def _build_language_list() -> Languages:
    with open(DATA_ROOT / "langmap.toml", "rb") as f:
        return tomllib.load(f)


def load_languages() -> Languages:
    languages = getattr(g, "languages", None)
    if languages is None:
        languages = g.languages = _build_language_list()
    return languages


def reload_languages() -> Languages:
    languages = g.languages = _build_language_list()
    return languages
