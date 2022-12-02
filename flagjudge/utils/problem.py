import tomllib
from pathlib import Path

from flask import g

from flagjudge import app
from flagjudge._typing.problem import *

DATA_ROOT = Path(app.root_path) / ".." / "data"


def load_problems() -> Problems:
    problems = {}
    for child in DATA_ROOT.iterdir():
        if child.is_file():
            continue
        prob_path = child / "problem.toml"
        if prob_path.exists():
            with open(prob_path, "rb") as f:
                detail = tomllib.load(f)
                problems[detail["id"]] = detail
    app.logger.info("Loaded problems")
    # app.logger.debug(problems)
    return problems


def get_testcases(id: str) -> CaseList:
    cases = []
    prob_root = DATA_ROOT / id
    for casefile in prob_root.glob("*.case.toml"):
        id = casefile.name.rstrip(".case.toml")
        with open(casefile, "rb") as f:
            case = tomllib.load(f)
        case["id"] = id
        cases.append(case)
    app.logger.info(f"Loaded testcases of id:{id}")
    return cases
