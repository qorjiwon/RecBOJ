from gensim.models import Word2Vec
from utils import *
import json
# 저장된 모델 불러오기
from gensim.models import Word2Vec
from utils import *
import json
# 저장된 모델 불러오기
def get_problem_by_level(target_problem, ProblemLevelDict, similar_problem, level_flag):
        # target과 난이도가 같은 문제를 찾음
        if level_flag == 0:
            for i in range(200):
                if int(ProblemLevelDict[similar_problem[i][0]]) == int(ProblemLevelDict[target_problem]):
                    return similar_problem[i][0]
        # target보다 난이도가 낮은 문제를 찾음
        elif level_flag == 1:
            for i in range(200):
                if int(ProblemLevelDict[similar_problem[i][0]]) < int(ProblemLevelDict[target_problem]) and int(ProblemLevelDict[similar_problem[i][0]]) != 0:
                    return similar_problem[i][0]
        # target보다 난이도가 높은 문제를 찾음
        elif level_flag == 2:
            for i in range(200):
                if int(ProblemLevelDict[similar_problem[i][0]]) > int(ProblemLevelDict[target_problem]):
                    print(similar_problem[i][0],ProblemLevelDict[similar_problem[i][0]], ProblemLevelDict[target_problem])
                    return similar_problem[i][0]
    
        return -1
    
def get_similar_problem(problem_id):
    model = Word2Vec.load("/Users/im_jungwoo/Desktop/project/ChromeExtension/server/models/model/item2vec/word2vec_model.bin") 
    with open('/Users/im_jungwoo/Desktop/project/ChromeExtension/server/models/model/item2vec/ProblemLevelDict.json', 'r') as f:
        ProblemLevelDict = json.load(f)
    similar_problem = model.wv.most_similar(problem_id, topn= 200)
    
    problems = {}
    r_equal = get_problem_by_level(problem_id, ProblemLevelDict, similar_problem, level_flag=0)
    problems["problem_equal"] = r_equal
    r_low = get_problem_by_level(problem_id, ProblemLevelDict, similar_problem, level_flag=1)
    problems["problem_low"] = r_low
    r_high = get_problem_by_level(problem_id, ProblemLevelDict, similar_problem, level_flag=2)
    problems["problem_high"] = r_high 
    
    results = json.dumps(problems)
    return results