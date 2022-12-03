import tomllib
from pathlib import Path

from flagjudge import app
from flagjudge._typing.problem import *
from flagjudge.db import get_db


def preload_problems() -> None:
    """Preloads problems into the database."""
    data_root = Path(app.root_path) / ".." / "data"

    # delete all prolems first
    get_db().execute("DELETE FROM problem;")

    for child in data_root.iterdir():
        if child.is_file():
            continue
        prob_path = child / "problem.toml"
        if prob_path.exists():
            with open(prob_path) as f:
                detail_str = f.read()
                detail = tomllib.loads(detail_str)
                get_db().execute(
                    "INSERT INTO problem VALUES (?, ?, ?, ?);",
                    (
                        detail["id"],
                        detail["title"],
                        detail_str,
                        child.resolve().as_posix(),
                    ),
                )
        get_db().commit()

    app.logger.info("Preloaded problems")


def load_problems() -> list[SimpleProblem]:
    """Load problems from database."""
    if get_db().execute("SELECT count(*) FROM problem").fetchone()[0] == 0:
        preload_problems()
    problems = []
    for row in (
        get_db().execute("SELECT id, title FROM problem ORDER BY id ASC;").fetchall()
    ):
        problems.append({"id": row[0], "title": row[1]})
    return problems


def load_problem(id: int) -> Problem:
    """Load a problem from database."""
    detail_str = (
        get_db().execute("SELECT detail FROM problem WHERE id=?;", (id,)).fetchone()[0]
    )
    return tomllib.loads(detail_str)  # type: ignore


def load_testcases(id: str) -> list[Case]:
    cases = []
    prob_root = Path(app.root_path) / ".." / "data" / id
    for casefile in prob_root.glob("*.case.toml"):
        id = casefile.name.rstrip(".case.toml")
        with open(casefile, "rb") as f:
            case = tomllib.load(f)
        case["id"] = id
        cases.append(case)
    app.logger.info(f"Loaded testcases of id:{id}")
    return cases
