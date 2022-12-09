from datetime import datetime

import httpx

from flagjudge import app
from flagjudge.db import get_db
from flagjudge.utils.language import load_languages
from flagjudge.utils.problem import load_problem, load_testcases
from flagjudge.utils.submission import generate_dynflag


def judge(subid: int, probid: int, language: str, code: str):
    prob = load_problem(probid)
    cases = load_testcases(probid)
    app.logger.debug(cases)
    status = 0
    for case in cases:
        try:
            output = submit_to_piston(
                language,
                code,
                case["stdin"],
                int(prob["limit"]["time"] * 1000),
                int(prob["limit"]["memory"] * 1024 * 1024),
            )

        except Exception as e:
            app.logger.exception(e)
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
            if stdout.rstrip() != case["stdout"].rstrip():
                status = 2  # WA

        get_db().execute(
            "INSERT INTO judgelog VALUES (?, ?, ?, ?, ?);",
            (
                subid,
                datetime.now().timestamp(),
                case["stdin"],
                output["run"]["stdout"],
                output.get("compile", {}).get("stderr", ""),
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
        (generate_dynflag(prob["flag"], code), status, subid),
    )
    get_db().commit()


def submit_to_piston(language: str, code: str, stdin: str, timeout: int, memlimit: int):
    langs = load_languages()
    version = ""
    for lang in langs:
        if lang["id"] == language:
            version = lang["version"]

    r = httpx.post(
        f"{app.config['PISTON_URL']}/api/v2/execute",
        json={
            "language": language,
            "version": version,
            "files": [{"content": code}],
            "stdin": stdin,
            "run_timeout": timeout,
            "compile_timeout": timeout,
            "run_memory_limit": memlimit,
            "compile_memory_limit": memlimit,
        },
        timeout=15,
    )
    if r.status_code != 200:
        raise Exception(r.text)
    output = r.json()
    return output
