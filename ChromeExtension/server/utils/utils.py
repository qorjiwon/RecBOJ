import re

def extract_user_id_from_url(url):
    pattern = r'user_id=([a-zA-Z0-9_-]+)'
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
                    if cnt == 3:
                        return problem_list
        
        # target보다 난이도가 낮은 문제를 찾음
        elif level_flag == 1:
            for i in range(200):
                if int(ProblemDict[similar_problem[i][0]]['level']) < target_level \
                     and int(ProblemDict[similar_problem[i][0]]['level']) >= max(target_level - 2, 1):
                    problem_list.append((similar_problem[i][0], round(similar_problem[i][1] * 100)))
                    cnt += 1
                    if cnt == 3:
                        return problem_list
        
        # target보다 난이도가 높은 문제를 찾음
        elif level_flag == 2:
            for i in range(200):
                if int(ProblemDict[similar_problem[i][0]]['level']) > target_level \
                    and int(ProblemDict[similar_problem[i][0]]['level']) <= target_level + 2:
                    problem_list.append((similar_problem[i][0], round(similar_problem[i][1] * 100)))
                    cnt += 1
                    if cnt == 3:
                        return problem_list
    
        return []

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
    print(f'avgTries: {avgTries}, wa_nums: {wa_nums}, flag = {flag}')
    return flag
    
    