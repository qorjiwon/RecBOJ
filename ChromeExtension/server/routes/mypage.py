from fastapi import APIRouter, HTTPException
import logging
import asyncio
from models.mypage import *
from utils.utils import *
from utils.model import *
import pandas as pd
from utils.preprocessing import *
from utils.recommendation import *


mypage_router = APIRouter(
    tags=["mypage"]
)
# 로깅 레벨 설정
logging.basicConfig( level=logging.DEBUG)
lock = asyncio.Lock()

weak_strong_forget_df = pd.read_csv('data/final_khu_forgetting_curve_df.csv').drop(columns=['memory','time','language','code_length'])
pivot_table = pd.read_csv('data/khu_pivot_table.csv')
index_to_problem = pd.read_csv('data/final_problem_processed.csv')
id_to_index = pd.read_csv('data/khu_id_to_index.csv')

cache = {}

@mypage_router.post("/problems", response_model=ResponseData)
async def send_mypage_data(request_data: MyPageRequest):
    try:
        global cache
        current_url = request_data.url
        rotate = request_data.div
        filter = request_data.filter
        user_id = extract_user_id_from_mypage(current_url)
        strong_tag, weak_tag, strong_pcr, weak_pcr = weak_strong_rec(weak_strong_forget_df, user_id)
        print("user id: ", user_id)
        try:
            if rotate == 0:
                strong_tag, weak_tag, strong_pcr, weak_pcr = weak_strong_rec(weak_strong_forget_df, user_id)
                # forget_curve를 이용해서...
                forgotten_tag, forgotten_pcr = forget_curve(weak_strong_forget_df, user_id)
                SolvedBasedProblems = Solved_Based_Recommenation(pivot_table, user_id, index_to_problem, id_to_index, 500)
                weakTagProblems, forgottenTagProblems, similarityBasedProblems = getMypageProblemsDict(SolvedBasedProblems, weak_tag, weak_pcr, forgotten_tag, forgotten_pcr, 200)
                async with lock:
                    cache[user_id] = {}
                    cache[user_id]['weakTagProblems'] = weakTagProblems   
                    cache[user_id]['forgottenTagProblems'] = forgottenTagProblems
                    cache[user_id]['similarityBasedTagProblems'] = similarityBasedProblems
                threeWeaks, threeForgotten, threeSimilar = cutThreeProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems)
            else:
                async with lock:
                    weakTagProblems = cache[user_id]['weakTagProblems']
                    forgottenTagProblems = cache[user_id]['forgottenTagProblems']
                    similarityBasedProblems = cache[user_id]['similarityBasedTagProblems']
                threeWeaks, threeForgotten, threeSimilar = reloadProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems, rotate, filter)
        except:
            user_id = 'eu2525'
            if rotate == 0:
                strong_tag, weak_tag, strong_pcr, weak_pcr = weak_strong_rec(weak_strong_forget_df, user_id)
                # forget_curve를 이용해서...
                forgotten_tag, forgotten_pcr = forget_curve(weak_strong_forget_df, user_id)
                SolvedBasedProblems = Solved_Based_Recommenation(pivot_table, user_id, index_to_problem, id_to_index, 500)
                weakTagProblems, forgottenTagProblems, similarityBasedProblems = getMypageProblemsDict(SolvedBasedProblems, weak_tag, weak_pcr, forgotten_tag, forgotten_pcr, 200)
                async with lock:
                    cache[user_id] = {}
                    cache[user_id]['weakTagProblems'] = weakTagProblems   
                    cache[user_id]['forgottenTagProblems'] = forgottenTagProblems
                    cache[user_id]['similarityBasedTagProblems'] = similarityBasedProblems
                threeWeaks, threeForgotten, threeSimilar = cutThreeProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems)
            else:
                async with lock:
                    weakTagProblems = cache[user_id]['weakTagProblems']
                    forgottenTagProblems = cache[user_id]['forgottenTagProblems']
                    similarityBasedProblems = cache[user_id]['similarityBasedTagProblems']
                threeWeaks, threeForgotten, threeSimilar = reloadProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems, rotate, filter)

        # 1. weak_tag_problems 전처리
        for tag_key, tag_value in threeWeaks.items():
            tag_value['explainations'] = [
                {
                    "problemID": exp[0],
                    "titleKo": exp[1],
                    "level": str(exp[2]),  # level이 문자열이라면 변환 필요 없음
                    "averageTries": float(exp[3])
                } for exp in tag_value['explainations']
            ]

        # 2. forgotten_tag_problems 전처리
        for tag_key, problem_value in threeForgotten.items():
            problem_value['problem']['tags'] = [problem_value['problem']['tags']] \
                if not isinstance(problem_value['problem']['tags'], list) else problem_value['problem']['tags']

        responseData = {
                'user_id' : user_id,    
                'weak_tag_problems': threeWeaks,
                'forgotten_tag_problems': threeForgotten,
                'similarity_based_problems': threeSimilar
            }
        print(f"Responsed to {user_id} (Mypage)")
        # cache가 너무 커지면 비우기
        if len(cache) >= 10000:
            cache.clear()
        response = ResponseData(**responseData)
        return response
    except HTTPException as e:
        # HTTP 예외 발생 시 로그로 출력
        logging.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        # 다른 예외 발생 시 로그로 출력
        logging.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")