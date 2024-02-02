from typing import List, Dict
from pydantic import BaseModel, validator

class MyPageRequest(BaseModel):
    url: str
    div: int
    filter: str


class Problem(BaseModel):
    problemID: str
    titleKo: str
    level: str
    averageTries: int
    tags: List[str]

class Explaination(BaseModel):
    problemID: str
    titleKo: str
    level: str
    averageTries: int

class Tag(BaseModel):
    tag_name: str
    problems: List[str]
    explainations: List[Explaination]
    weak_pcr: float

class WeakTagProblems(BaseModel):
    __root__: Dict[str, Tag]

class ForgottenTagProblem(BaseModel):
    tag: str
    forgottenPercent: float
    problem: Problem

class ForgottenTagProblems(BaseModel):
    __root__: Dict[str, ForgottenTagProblem]

class SimilarityBasedProblems(BaseModel):
    problem1: Problem
    problem2: Problem
    problem3: Problem

class ResponseData(BaseModel):
    user_id: str
    weak_tag_problems: Dict[str, Tag]
    forgotten_tag_problems: Dict[str, ForgottenTagProblem]
    similarity_based_problems: SimilarityBasedProblems

    @validator('similarity_based_problems', pre=True)
    def ensure_tags_are_lists(cls, v):
        problems = ['problem1', 'problem2', 'problem3']
        for problem in problems:
            if problem in v and 'tags' in v[problem] and not isinstance(v[problem]['tags'], list):
                v[problem]['tags'] = [v[problem]['tags']]
        return v
