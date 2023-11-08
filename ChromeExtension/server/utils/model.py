from gensim.models import Word2Vec
from .utils import *
import json

    
def get_item2vec_problem(problem_id, submits):
    # 저장된 모델 불러오기
    model = Word2Vec.load("server\models\item2vec\word2vec_model.bin") 
    with open('server\data\ProblemDict.json', 'r') as f:
        ProblemDict = json.load(f)
    similar_problem = model.wv.most_similar(problem_id, topn= 200)

    problems = {}
    level_flag = get_levelflag(problem_id, submits, ProblemDict)
    problem_list = get_problem_by_level(problem_id, ProblemDict, similar_problem, level_flag)
    problems['problem0'] = problem_list[0][0]
    problems['problem0_similarity'] = problem_list[0][1]
    problems['problem1'] = problem_list[1][0]
    problems['problem1_similarity'] = problem_list[1][1]
    problems['problem2'] = problem_list[2][0]
    problems['problem2_similarity'] = problem_list[2][1]
    if level_flag == 0:
        problems['message'] = "비슷한 난이도의 문제들에 도전해보세요!"
    elif level_flag == 1:
        problems['message'] = "더 낮은 난이도의 문제들을 문저 풀어보는건 어떨까요?"
    elif level_flag == 2:
        problems['message'] = "더 높은 난이도의 문제들로 레벨업!"

    results = json.dumps(problems)
    return results