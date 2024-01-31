from hashlib import md5

from flask import session

from flagjudge import app


def strip_stdout(stdout: str):
    return "\n".join([line.strip() for line in stdout.split("\n")])


def generate_dynflag(tmpl: str, probid: int):
    data = session.get("token", "") + app.config.get("SECRET_KEY", "") + str(probid)
    hash = md5(data.encode()).hexdigest()
    flag = tmpl.replace("{hash}", hash)
    return flag
