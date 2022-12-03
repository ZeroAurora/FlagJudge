import sqlite3

from flask import g

from flagjudge import app


def get_db():
    db_file = app.config["DATABASE"]
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_file)
    return db

@app.teardown_appcontext
def teardown_db(_exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.cli.command("initdb")
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
