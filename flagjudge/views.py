from datetime import datetime
import asyncio

from flask import render_template, request, jsonify

from flagjudge import app
from flagjudge.db import get_db
from flagjudge.utils import problem, language
from flagjudge.tasks import judge


@app.get("/")
def index():
    problems = problem.load_problems()
    return render_template("problem_list.html", problems=problems)


@app.get("/<int:id>/")
def get_problem(id: int):
    prob = problem.load_problem(id)
    lang = language.load_languages()
    return render_template("problem.html", problem=prob, languages=lang)


@app.post("/<int:id>/submit/")
def submit(id: int):
    lang = request.form["language"]
    code = request.form["code"]
    timestamp = datetime.now().timestamp()
    rowid = (
        get_db()
        .execute(
            "INSERT INTO submission VALUES (?, ?, ?, ?, ?, ?) RETURNING rowid;",
            (timestamp, id, lang, code, "", 0),
        )
        .fetchone()[0]
    )
    get_db().commit()
    judge(rowid, id, lang, code)
    return {"submission": rowid}


@app.get("/queue/<int:id>")
def waiting_for_judge():
    return render_template("waiting_for_judge.html")
