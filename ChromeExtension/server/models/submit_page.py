from pydantic import BaseModel
from typing import List

class SubmitPageRequest(BaseModel):
    url: str
    div: int
    submits: List[str]

class ResponseData(BaseModel):
    problem0: str
    problem1: str
    problem2: str
    problem0_similarity: str
    problem1_similarity: str
    problem2_similarity: str
    problem0_titleKo: str
    problem1_titleKo: str
    problem2_titleKo: str
    problem0_tags: List[str]
    problem1_tags: List[str]
    problem2_tags: List[str]
    problem0_tier: str
    problem1_tier: str
    problem2_tier: str
    message: str
