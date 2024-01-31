import base64
import tomllib

from flask import Flask, request, session, redirect, make_response
import OpenSSL

from flagjudge.filters.markdown import markdown_filter

app = Flask(__name__)
app.config.from_file("../config.toml", lambda f: tomllib.loads(f.read()))
app.jinja_env.filters["markdown"] = markdown_filter
app.secret_key = app.config["SECRET_KEY"]

with open("./cert.pem") as f:
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())  # type: ignore


@app.before_request
def token_login():
    if request.path.startswith("/static/"):
        return
    if request.args.get("token"):
        try:
            token = request.args.get("token") or ""
            id, sig = token.split(":", 1)
            sig = base64.b64decode(sig, validate=True)
            OpenSSL.crypto.verify(cert, sig, id.encode(), "sha256")  # type: ignore
            session["token"] = token
        except Exception:
            session["token"] = None
        return redirect("/")
    if session.get("token") is None:
        return make_response("Token error.", 403)


from flagjudge import views
