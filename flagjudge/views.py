from flask import render_template, request

from flagjudge import app
from flagjudge.utils import problem 


@app.route("/")
def index():
    problems = problem.load_problems()
    return render_template("problem_list.html", problems=problems)


@app.route("/<int:id>/")
def get_problem(id: int):
    prob = problem.load_problems()[id]
    return render_template("problem.html", problem=prob)


@app.route("/queue/<int:id>")
def waiting_for_judge():
    return render_template("waiting_for_judge.html")
