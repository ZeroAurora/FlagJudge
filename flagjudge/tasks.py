from datetime import datetime

import requests

from flagjudge import app
from flagjudge.db import get_db
from flagjudge.utils.language import load_languages
from flagjudge.utils.problem import load_problem, load_testcases
from flagjudge.utils.submission import generate_dynflag, strip


def judge(subid: int, probid: int, language: str, code: str):
    prob = load_problem(probid)
    cases = load_testcases(probid)
    assert prob

    status = 0
    for case in cases:
        try:
            output = submit_to_piston(
                language,
                code,
                strip(case["stdin"], True),
                int(prob["limit"]["time"] * 1000),
                int(prob["limit"]["memory"] * 1024 * 1024),
            )

        except Exception:
            app.logger.exception("")
            status = 6
            break

        if output.get("compile", {}).get("code", 0) != 0:
            status = 5  # CE
        elif output["run"]["signal"] == "SIGKILL":
            status = 3  # RsE
        elif output["run"]["code"] != 0:
            status = 4  # RE
        else:
            stdout: str = output["run"]["stdout"]
            if strip(stdout) != strip(case["stdout"]):
                status = 2  # WA

        get_db().execute(
            "INSERT INTO judgelog VALUES (?, ?, ?, ?, ?);",
            (
                subid,
                datetime.now().timestamp(),
                case["stdin"],
                output["run"]["stdout"],
                output.get("compile", {}).get("stderr", "") or output["run"]["stderr"],
            ),
        )
        get_db().commit()

        if status != 0:
            break

    # if judge is not terminated then it's successful
    if status == 0:
        status = 1

    get_db().execute(
        "UPDATE submission SET flag=?, status=? WHERE rowid=?;",
        (generate_dynflag(prob["flag"], probid), status, subid),
    )
    get_db().commit()


def submit_to_piston(language: str, code: str, stdin: str, timeout: int, memlimit: int):
    langs = load_languages()
    version = next(filter(lambda x: x["id"] == language, langs))["version"]

    r = requests.post(
        f"{app.config['PISTON_URL']}/api/v2/execute",
        json={
            "language": language,
            "version": version,
            "files": [{"content": code}],
            "stdin": stdin,
            "run_timeout": timeout,
            "compile_timeout": 10,
            "run_memory_limit": memlimit,
            "compile_memory_limit": 512 * 1024 * 1024,
        },
        timeout=15,
    )
    if r.status_code != 200:
        app.logger.error(r.status_code)
        raise Exception()
    output = r.json()
    return output
