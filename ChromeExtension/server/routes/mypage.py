from fastapi import APIRouter, HTTPException
import logging
import asyncio
from models.mypage import *
from utils.utils import *
from utils.model import *
import pandas as pd
from utils.preprocessing import *
from utils.recommendation import *
import os
import time


print("mypage_router전")
mypage_router = APIRouter(
    tags=["mypage"]
)
print("mypage_router 후")
# 로깅 레벨 설정
print("logging.basicConfig 전")
logging.basicConfig(level=logging.DEBUG)
print("logging.basicConfig 후")
lock = asyncio.Lock()
print("lock = asyncio.Lock() 전")

print("forgetting_df 드가자~")
weak_strong_forget_df = make_forgetting_df()
#pivot_table 만들 때 user_id를 어케주지...?            
print("user_df 드가자~")
user_df = make_df()

index_to_problem = pd.read_csv('data/final_problem_processed.csv')
id_to_index = pd.read_csv('data/khu_id_to_index.csv')

cache = {}

@mypage_router.post("/problems", response_model=ResponseData)
async def send_mypage_data(request_data: MyPageRequest):
    try:
        global cache
        current_url = request_data.url
        rotate = request_data.div
        num_problems = request_data.numProblems
        filter = request_data.filter
        user_id = extract_user_id_from_mypage(current_url)
        #User_id가 있는지
        find = user_find(user_id)
        #user_id는 있지만, 오래전에 업데이트 한 경우에는 다시 크롤링
        if find == False:
            global user_df, weak_strong_forget_df
            pwd = os.getcwd()
            os.chdir("./scrapy/recboj/recboj/spiders")
            os.system(f"scrapy runspider probleminfo.py -a newUser={user_id}")
            os.chdir(pwd)
            time.sleep(0.1)
            if not user_find(user_id):
                responseData = {
                    'user_id' : user_id,
                    'message' : "response failed"   
                }
                response = ResponseData(**responseData)
                return response
            user_df = make_df()
            weak_strong_forget_df = make_forgetting_df()

        if rotate == 0:
            pivot_table = make_pivot(user_df, user_id)
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
            Weaks, Forgottens, Similars = cutProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems, n = num_problems)
        else:
            async with lock:
                weakTagProblems = cache[user_id]['weakTagProblems']
                forgottenTagProblems = cache[user_id]['forgottenTagProblems']
                similarityBasedProblems = cache[user_id]['similarityBasedTagProblems']
            Weaks, Forgottens, Similars = reloadProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems, rotate, filter, n = num_problems)

        responseData = {
                'user_id' : user_id,    
                'weak_tag_problems': Weaks,
                'forgotten_tag_problems': Forgottens,
                'similarity_based_problems': Similars
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