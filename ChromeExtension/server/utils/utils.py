import re
import numpy as np
import json
from models.mypage import *
from typing import Dict
# Pivot_Table의 Nan값 처리
def return_user_data(pivot_table):
    column_info = pivot_table.columns
    X = pivot_table.to_numpy()
    X = np.nan_to_num(X)
    return X, column_info

# user_id에 맞는 pivot table의 행을 추출 
def get_problem_list(pivot, user_id, id_to_index):
    idx = id_to_index[id_to_index['user_id'] == user_id]['id_to_index']
    problem_list = pivot[['user_id'] == user_id].flatten()
    return problem_list

# 데이터프레임의 tag를 나눔
def tag_split(df):
    df['tags'] = df['tags'].str.split(',')
    tag_df = df.explode('tags').dropna().reset_index(drop=True)
    tag_df = tag_df[tag_df['tags'] != ""]
    return tag_df


def extract_user_id_from_url(url):
    pattern = r'user_id=([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def extract_user_id_from_mypage(url):
    pattern = r'user/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def extract_problem_id_from_url(url):
    pattern = r'problem_id=([0-9]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

# level_flag에 따라서 난이도별로 알맞은 문제를 찾음
def get_problem_by_level(target_problem, ProblemDict, similar_problem, level_flag):
    
        problem_list = []
        cnt = 0
        target_level = int(ProblemDict[target_problem]['level'])
        # target과 난이도가 같은 문제를 찾음
        if level_flag == 0:
            for i in range(200):
                if int(ProblemDict[similar_problem[i][0]]['level']) == target_level:
                    problem_list.append((similar_problem[i][0], round(similar_problem[i][1] * 100)))
                    cnt += 1
                    if cnt == 15:
                        return problem_list
        
        # target보다 난이도가 낮은 문제를 찾음
        elif level_flag == 1:
            for i in range(200):
                if int(ProblemDict[similar_problem[i][0]]['level']) < target_level \
                     and int(ProblemDict[similar_problem[i][0]]['level']) >= max(target_level - 2, 1):
                    problem_list.append((similar_problem[i][0], round(similar_problem[i][1] * 100)))
                    cnt += 1
                    if cnt == 15:
                        return problem_list
        
        # target보다 난이도가 높은 문제를 찾음
        elif level_flag == 2:
            for i in range(200):
                if int(ProblemDict[similar_problem[i][0]]['level']) > target_level \
                    and int(ProblemDict[similar_problem[i][0]]['level']) <= target_level + 2:
                    problem_list.append((similar_problem[i][0], round(similar_problem[i][1] * 100)))
                    cnt += 1
                    if cnt == 15:
                        return problem_list
        return problem_list

# 받아온 json 데이터로부터 제출 유형별 횟수를 반환
def GetTries(data):
    submits = eval(str(data))
    ac_nums = 0
    wa_nums = 0
    tle_nums = 0
    mle_nums = 0
    for submit in submits:
        if submit == "맞았습니다!!":
            ac_nums += 1
        elif submit == "시간 초과":
            tle_nums += 1
            wa_nums += 1
        elif submit == "메모리 초과":
            wa_nums += 1
            mle_nums += 1
        else:
            wa_nums += 1
    return (ac_nums, wa_nums, tle_nums, mle_nums)

# 제출 유형에 따른 level_flag를 반환
def get_levelflag(problem_id, data, ProblemDict):
    avgTries = ProblemDict[problem_id]['averageTries']
    ac_nums, wa_nums, tle_nums, mle_nums = GetTries(data)
    if wa_nums / max(ac_nums , 1) > avgTries + 1:
        flag = 1
    elif wa_nums < avgTries and ac_nums >= 1:
        flag = 2
    else:
        flag = 0
    return flag

def pretty_print(data, indent=0):
    for key, value in data.items():
        if isinstance(value, dict):
            # 만약 값이 딕셔너리이면 재귀 호출
            print(' ' * indent + f'{key}:')
            pretty_print(value, indent + 2)
        else:
            # 딕셔너리가 아니면 그냥 출력
            print(' ' * indent + f'{key}: {value}')

def cutProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems, tag_num = 3, n = 3):
    
    # 취약 유형 문제 
    weaks = []
    for i in range(1, tag_num + 1):
        tag_key = f'tag{i}'
        problems = weakTagProblems[tag_key]['problems'][:3]
        explainations_input = weakTagProblems[tag_key]['explainations'][:3]
        
        explainations = [
            Explaination(problemID=exp[0], titleKo=exp[1], level=exp[2], averageTries=exp[3], tags=exp[4])
            for exp in explainations_input
        ]
        
        weak = WeakTagProblem(
            tag_name=weakTagProblems[tag_key]['tag_name'],
            problems=problems,
            explainations=explainations,
            weak_pcr=weakTagProblems[tag_key]['weak_pcr']
        )
        weaks.append(weak)

    # 푼 지 오래된 문제
    forgottens = []
    for i in range(1, tag_num + 1):
        tag_key = f'tag{i}'
        print(forgottenTagProblems[tag_key])
        # Todo: 망각기반 추천 문제 한 개도 없을 때 예외 처리
        # 지금은 dummy data 전송
        # problem_data = forgottenTagProblems[tag_key]['problem1']
        problem_data = {'problemID': '1806', 'titleKo': '부분합', 'level': 'Gold IV', 'averageTries': 3.9, 'tags': 'prefix_sum'}
        forgotten = ForgottenTagProblem(
            tag=forgottenTagProblems[tag_key]['tag'],
            forgottenPercent=forgottenTagProblems[tag_key]['forgottenPercent'],
            problem=Problem(**problem_data)  # Problem 모델을 사용하여 직접 생성
        )
        
        forgottens.append(forgotten)

    # 유사도 기반 추천
    similars = [Problem(**similarityBasedProblems[f'problem{i}']) for i in range(1, n + 1)]
    return weaks, forgottens, similars

def reloadProblems(weakTagProblems: Dict, forgottenTagProblems: Dict, similarityBasedProblems: Dict, rotate: int, filter: str, tag_num: int = 3, n: int = 3):
    Weaks: List[WeakTagProblem] = []
    Forgottens: List[ForgottenTagProblem] = []
    Similars: List[Problem] = []

    rotate = int(rotate)

    for i in range(1, tag_num+1):
        tag_key = f'tag{i}'
        problems = []
        explainations = []
        cnt = 0
        problems_list = weakTagProblems[tag_key]['problems']
        explanations_list = weakTagProblems[tag_key]['explainations']
        index = (n * rotate - (n-1)) % len(problems_list)
        while cnt < len(problems_list) and len(problems) < n:
            exp = explanations_list[index]
            #exp가 List여서 2로 접근하는데 이거 아님.
            # exp = [문제번호, 이름, 티어, 평균시도횟수, tag]
            if checkTier(exp[2], filter):
                problems.append(problems_list[index])
                explainations.append(Explaination(problemID=exp[0], titleKo=exp[1], level=exp[2], averageTries=exp[3], tags=exp[4]))
            index = (index + 1) % len(problems_list)
            cnt += 1

        Weaks.append(WeakTagProblem(
            tag_name=weakTagProblems[tag_key]['tag_name'],
            problems=problems,
            explainations=explainations,
            weak_pcr=weakTagProblems[tag_key]['weak_pcr']
        ))
    
    
    # Forgotten 서비스 안한다고 가정하고 더미값 출력 중, 추후 수정
    for i in range(1, tag_num + 1):
        tag_key = f'tag{i}'
         # Todo: 망각기반 추천 문제 한 개도 없을 때 예외 처리
        # 지금은 dummy data 전송
        # problem_data = forgottenTagProblems[tag_key]['problem1']
        problem_data = {'problemID': '1806', 'titleKo': '부분합', 'level': 'Gold IV', 'averageTries': 3.9, 'tags': 'prefix_sum'}
        forgotten = ForgottenTagProblem(
            tag=forgottenTagProblems[tag_key]['tag'],
            forgottenPercent=forgottenTagProblems[tag_key]['forgottenPercent'],
            problem=Problem(**problem_data)  # Problem 모델을 사용하여 직접 생성
        )
        Forgottens.append(forgotten)
    
    for i in range(1, n+1):
        index = (rotate + i - 1) % len(similarityBasedProblems)
        cnt = 0
        while cnt < len(similarityBasedProblems):
            print(1)
            
            problem = similarityBasedProblems[f'problem{index + 1}']
            if checkTier(problem['level'], filter):
                Similars.append(Problem(**problem))
                print(111)
                break
            else:
                index = (index + 1) % len(similarityBasedProblems)
                cnt += 1
            print(2)
    

    return Weaks, Forgottens, Similars

# 딕셔너리를 JSON 파일로 저장하는 함수
def save_as_json(data, filename, dir_path = 'user_data/'):
    with open(dir_path + filename + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# JSON 파일을 딕셔너리로 읽어오는 함수
def load_from_json(filename, dir_path = 'user_data/'):
    with open(dir_path + filename + '.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def checkTier(tier, filter):
    if filter == "None":
        return True
    elif filter in tier:
        return True
    return False

def index_to_problem(problem_info, top_problems):
    rec_id = problem_info.loc[top_problems, 'problemId'].tolist() #tolist안붙이니깐 index랑 같이 나옴 결과가.
    return rec_id