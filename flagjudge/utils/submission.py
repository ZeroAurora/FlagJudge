import json
from datetime import datetime
from hashlib import md5


def generate_dynflag(tmpl: str, code: str):
    data = json.dumps({"code": code, "time": datetime.now().isoformat()})
    hash = md5(data.encode()).hexdigest()
    flag = tmpl.replace("{hash}", hash)
    return flag
