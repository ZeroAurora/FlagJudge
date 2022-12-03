import tomllib

from flask import Flask

from flagjudge.filters.markdown import markdown_filter


app = Flask(__name__)
app.config.from_file("../config.toml", lambda f: tomllib.loads(f.read()))
app.jinja_env.filters["markdown"] = markdown_filter

from flagjudge import views
