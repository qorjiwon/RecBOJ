from typing import List
from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic import BaseModel, Field

class MyPageRequest(BaseModel):
   url: str
   numProblems: int
   div: int
   filter: str

class Problem(BaseModel):
    problemID: str
    titleKo: str
    level: str
    averageTries: float
    tags: str

class Explaination(BaseModel):
    problemID: str
    titleKo: str
    level: str
    averageTries: float
    tags: str

class WeakTagProblem(BaseModel):

    tag_name: str
    problems: List[str]
    explainations: List[Explaination]
    weak_pcr: float

class ForgottenTagProblem(BaseModel):
    tag: str
    forgottenPercent: float
    problem: Problem

class ResponseData(BaseModel):
    user_id: str = Field(..., example="12345")
    message: str = "response ok"
    weak_tag_problems: Optional[List[WeakTagProblem]]
    forgotten_tag_problems: Optional[List[ForgottenTagProblem]]
    similarity_based_problems: Optional[List[Problem]]