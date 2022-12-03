import tomllib
from functools import cache
from pathlib import Path

from flagjudge import app
from flagjudge._typing.language import *

# I'm lazy so caching to database is gugugu-ed 
@cache
def load_languages() -> list[Language]:
    langmap_path = Path(app.root_path) / ".." / "data" / "langmap.toml"
    with open(langmap_path, "rb") as f:
        return tomllib.load(f)["languages"]
