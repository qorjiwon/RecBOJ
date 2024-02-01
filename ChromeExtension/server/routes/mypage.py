from fastapi import APIRouter

from models.mypage import *
from utils.utils import *
from utils.model import *
import pandas as pd
import threading
from utils.preprocessing import *
from utils.recommendation import *


mypage_router = APIRouter(
    tags=["mypage"]
)

lock = threading.Lock()
weak_strong_forget_df = pd.read_csv('data/final_khu_forgetting_curve_df.csv').drop(columns=['memory','time','language','code_length'])
pivot_table = pd.read_csv('data/khu_pivot_table.csv')
index_to_problem = pd.read_csv('data/final_problem_processed.csv')
id_to_index = pd.read_csv('data/khu_id_to_index.csv')

cache = {}

@mypage_router.post("/problems", response_model=ResponseData)
async def send_mypage_data(request_data: MyPageRequest):
    global cache
    current_url = request_data.url
    rotate = request_data.div
    filter = request_data.filter
    user_id = extract_user_id_from_mypage(current_url)

    strong_tag, weak_tag, strong_pcr, weak_pcr = weak_strong_rec(weak_strong_forget_df, user_id)
    # forget_curve를 이용해서...
    try:
        if rotate == 0:
            strong_tag, weak_tag, strong_pcr, weak_pcr = weak_strong_rec(weak_strong_forget_df, user_id)
            # forget_curve를 이용해서...
            forgotten_tag, forgotten_pcr = forget_curve(weak_strong_forget_df, user_id)
            SolvedBasedProblems = Solved_Based_Recommenation(pivot_table, user_id, index_to_problem, id_to_index, 500)
            weakTagProblems, forgottenTagProblems, similarityBasedProblems = getMypageProblemsDict(SolvedBasedProblems, weak_tag, weak_pcr, forgotten_tag, forgotten_pcr, 200)
            with lock:
                cache[user_id] = {}
                cache[user_id]['weakTagProblems'] = weakTagProblems   
                cache[user_id]['forgottenTagProblems'] = forgottenTagProblems
                cache[user_id]['similarityBasedTagProblems'] = similarityBasedProblems
            threeWeaks, threeForgotten, threeSimilar = cutThreeProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems)
        else:
            with lock:
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
            with lock:
                cache[user_id] = {}
                cache[user_id]['weakTagProblems'] = weakTagProblems   
                cache[user_id]['forgottenTagProblems'] = forgottenTagProblems
                cache[user_id]['similarityBasedTagProblems'] = similarityBasedProblems
            threeWeaks, threeForgotten, threeSimilar = cutThreeProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems)
        else:
            with lock:
                weakTagProblems = cache[user_id]['weakTagProblems']
                forgottenTagProblems = cache[user_id]['forgottenTagProblems']
                similarityBasedProblems = cache[user_id]['similarityBasedTagProblems']
            threeWeaks, threeForgotten, threeSimilar = reloadProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems, rotate, filter)
    
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
    print(responseData)
    return response
