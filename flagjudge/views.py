import asyncio
from datetime import datetime

from flask import jsonify, render_template, request

from flagjudge import app
from flagjudge.db import get_db
from flagjudge.tasks import judge
from flagjudge.utils import language, problem, site


@app.get("/")
def index():
    problems = problem.load_problems()
    notification = site.load_notification()
    return render_template(
        "problem_list.html", problems=problems, notification=notification
    )


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
            "INSERT INTO submission VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING rowid;",
            (timestamp, id, lang, code, "", 0, 0),
        )
        .fetchone()[0]
    )
    get_db().commit()
    judge(rowid, id, lang, code)
    return {"submission": rowid}


@app.get("/result/<int:id>/")
def judge_result(id: int):
    submission = (
        get_db()
        .execute("SELECT rowid, * FROM submission WHERE rowid=?;", (id,))
        .fetchone()
    )
    judgelogs = (
        get_db()
        .execute("SELECT rowid, * FROM judgelog WHERE submission=?;", (id,))
        .fetchall()
    )
    get_db().execute("UPDATE submission SET visited=1 WHERE rowid=?;", (id,))
    get_db().commit()
    return render_template("result.html", submission=submission, judgelogs=judgelogs)
