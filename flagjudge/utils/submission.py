from hashlib import md5

from flask import session

from flagjudge import app


def strip(content: str, preserve_end: bool = False):
    res = "\n".join([line.rstrip() for line in content.split("\n")])
    if not preserve_end:
        res = res.rstrip()
    return res


def generate_dynflag(tmpl: str, probid: int):
    data = session.get("token", "") + app.config.get("SECRET_KEY", "") + str(probid)
    hash = md5(data.encode()).hexdigest()
    flag = tmpl.replace("{hash}", hash)
    return flag
