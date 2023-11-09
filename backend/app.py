from utils import *
from model import *

def main_page():
    # url에서 필요한 정보를 추출
    user_id = "eu2525" #extract_user_id_from_url(current_url)
    #user_id에 맞는 문제 풀이 내역 추출
    solve_problem = get_problem_list(user_id)
    #user 문제 풀이 내역을 통한 추천 문제
    vae_rec = vae_recommend_problem(solve_problem)
    ease_rec = ease_recommend_problem(solve_problem)
    total_rec = ease_rec + vae_rec
    NUM_TOP_PROBLEMS = 2
    top_problems = np.argpartition(-total_rec, NUM_TOP_PROBLEMS) # np.argpartition은 partition과 똑같이 동작하고, index를 리턴.
    top_problems = top_problems[ :NUM_TOP_PROBLEMS]

    return top_problems

problem = main_page()
print("추천 결과 :", problem)
