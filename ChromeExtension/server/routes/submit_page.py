from fastapi import APIRouter
import json

from models.submit_page import *
from utils.utils import extract_problem_id_from_url, extract_user_id_from_url
from utils.model import get_item2vec_problem

submit_page_router = APIRouter(
    tags=["submit"]
)

@submit_page_router.post('/', response_model=ResponseData)
async def sendRelatedProblem(request_data: SubmitPageRequest) -> dict:
    # url을 받아옴
    current_url = request_data.url
    div = request_data.div
    submits = request_data.submits
    
    # url에서 필요한 정보를 추출
    user_id = extract_user_id_from_url(current_url)
    problem_id = extract_problem_id_from_url(current_url)
    
    # 터미널에 데이터 출력
    print(f'Received URL: {current_url}\nUser ID: {user_id}\nProblem ID: {problem_id}')  
    problems = get_item2vec_problem(problem_id, submits, div)
    # 문자열을 딕셔너리로 변환
    problems_dict = json.loads(problems)
    resopnse = ResponseData(**problems_dict)
    return resopnse