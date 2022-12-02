from typing import TypedDict


class Case(TypedDict):
    id: int
    stdin: str
    stdout: str


CaseList = list[Case]

class Limit(TypedDict):
    time: float
    memory: float

class Problem(TypedDict):
    id: int
    title: str
    description: str
    instruction: str
    accepted_languages: list[str]
    flag: str
    limit: Limit
    samples: list[Case]


Problems = dict[int, Problem]
