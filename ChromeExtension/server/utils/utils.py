import re
import tensorflow as tf
from tensorflow import shape,math
from tensorflow.keras import Input,layers,Model
from tensorflow.keras.losses import mse,binary_crossentropy
import os
import random
import numpy as np
import pandas as pd
from tqdm import tqdm
import bottleneck as bn
import torch
import warnings
import json

import pandas as pd
from time import time
from datetime import datetime
import numpy as np

def tag_split(df):
    df['tags'] = df['tags'].str.split(',')
    tag_df = df.explode('tags').dropna().reset_index(drop=True)
    tag_df = tag_df[tag_df['tags'] != ""]
    return tag_df

def weak_strong_rec(df, user_id):
    df = df[df['user_id'] == user_id]
    # 개념 문제에 대해서만 할건지...??
    # df = df[df['level'] <= 10]
    # 평균 시도 횟수를 기준으로 나눔.
    weak_problem = df[df['wrong_count'] > df['averageTries']]
    strong_problem = df[df['wrong_count'] <= df['averageTries']]
    #tag를 split
    weak_df_tags = tag_split(weak_problem)
    st_df_tags = tag_split(strong_problem)
    # weak_df_tags의 user_id별 tag 수 세기
    weak_tag_counts = weak_df_tags.groupby(['user_id', 'tags']).size().reset_index(name='weak_count')
    # st_df_tags의 user_id별 tag 수 세기
    strong_tag_counts = st_df_tags.groupby(['user_id', 'tags']).size().reset_index(name='strong_count')

    # 정답률 계산
    merged_df = pd.merge(weak_tag_counts, strong_tag_counts, how='outer', on=['user_id', 'tags']).fillna(0)
    merged_df['total_count'] = merged_df['strong_count'] + merged_df['weak_count']
    merged_df = merged_df[merged_df['total_count'] >= 10]
    merged_df['accuracy'] = merged_df['strong_count'] / merged_df['total_count']
    #strong, weak 3문제 뽑음
    strong_3tag = merged_df.groupby('user_id').apply(lambda x: x.nlargest(3, 'accuracy')).reset_index(drop=True)
    weak_3tag = merged_df.groupby('user_id').apply(lambda x: x.nsmallest(3, 'accuracy')).reset_index(drop=True)
    #strong, weak 문제를 리스트로..
    strong = strong_3tag[strong_3tag['user_id'] == user_id]['tags'].to_list()
    weak = weak_3tag[weak_3tag['user_id'] == user_id]['tags'].to_list()
    strong_pcr = strong_3tag[strong_3tag['user_id'] == user_id]['accuracy'].to_list()
    weak_pcr = weak_3tag[weak_3tag['user_id'] == user_id]['accuracy'].to_list()

    for i in range(len(min(strong_pcr, weak_pcr))):
        strong_pcr[i] = round(strong_pcr[i] * 100, 1)
        weak_pcr[i] = round(weak_pcr[i] * 100, 1)
    return strong, weak, strong_pcr, weak_pcr


def forgetting_curve_with_repetition(df):
    #t는 경과 시간, s는 상대적인 기억력, n은 반복 횟수
    t = df['day']
    s = 7  #일주일 뒤에는 푼 문제에 대해서 까먹는다고 가정...
    n = df['count']
    return np.exp(-((t / s) ** (1 / n)))

def forget_curve(df, user_id):
    #data 불러오기
    df = df[df['user_id'] == user_id]
    
    # tag 나누기
    dfs = tag_split(df)
    # tag별 최신 풀었던 문제와 푼 문제수 추출
    df_tag = dfs.groupby('tags')['last_time'].agg(**{'recent_time':'max', 'count':'count'}).reset_index() 
    
    # 15문제 이상은 풀어야 애들 tag가 이상한게 안 뽑히더라....
    df_tag = df_tag[df_tag['count'] >= 15]
    
    # 망각 곡선 계산 하기
    current_timestamp = time()
    df_tag['day'] = (current_timestamp - df_tag['recent_time']) / 86400
    df_tag['forget_curve'] = df_tag.apply(forgetting_curve_with_repetition, axis=1).round(4)
    
    weak_3tag = df_tag.sort_values('forget_curve', ascending = True).head(3)
    weak_tag = weak_3tag['tags'].to_list()
    weak_tag_forgetpcr = weak_3tag['forget_curve'].to_list()

    for i in range(len(weak_tag_forgetpcr)):
        weak_tag_forgetpcr[i] = round(weak_tag_forgetpcr[i] * 100 , 1)
    return weak_tag, weak_tag_forgetpcr


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


def cutThreeProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems):
    threeWeaks = {}
    for i in range(1,4):
        threeWeaks['tag'+str(i)] = {}
        problems = weakTagProblems['tag'+str(i)]['problems'][:3]
        explainations = weakTagProblems['tag'+str(i)]['explainations'][:3]
        threeWeaks['tag'+str(i)]['tag_name'] = weakTagProblems['tag'+str(i)]['tag_name']
        threeWeaks['tag'+str(i)]['problems'] = problems
        threeWeaks['tag'+str(i)]['explainations'] = explainations
        threeWeaks['tag'+str(i)]['weak_pcr'] = weakTagProblems['tag'+str(i)]['weak_pcr']
    
    threeForgotten = {}
    problems = {}
    for i in range(1, 4):
        threeForgotten['tag'+str(i)] = {}
        threeForgotten['tag'+str(i)]['tag'] = forgottenTagProblems['tag'+str(i)]['tag']
        threeForgotten['tag'+str(i)]['forgottenPercent'] = forgottenTagProblems['tag'+str(i)]['forgottenPercent']
        for j in range(1, 2):  # Extracting first three problems
            problem_key = f'problem{j}'
            if problem_key in forgottenTagProblems['tag'+str(i)]:
                threeForgotten['tag'+str(i)]['problem'] = forgottenTagProblems['tag'+str(i)][problem_key]
    threeSimilar = {}
    for i in range(1, 4):
        threeSimilar['problem'+str(i)] = similarityBasedProblems['problem'+str(i)]
    
    return threeWeaks, threeForgotten, threeSimilar

def reloadProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems, rotate, filter):
    threeWeaks = {}
    threeForgotten = {}
    threeSimilar = {}

    rotate = int(rotate)
   
    for i in range(1,4):
        tag_key = 'tag' + str(i)
        problems = []
        explainations = []
        cnt = 0
        threeWeaks[tag_key] = {}
       
        problems_list = weakTagProblems[tag_key]['problems']
        explanations_list = weakTagProblems[tag_key]['explainations']
        index = (3 * rotate - 2) % len(problems_list)
        while cnt < len(problems_list) and len(problems) < 3:
            if checkTier(explanations_list[index][2], filter):
                problems.append(problems_list[index])
                explainations.append(explanations_list[index])
            index = (index + 1) % len(problems_list)
            cnt += 1

        threeWeaks['tag'+str(i)]['tag_name'] = weakTagProblems['tag'+str(i)]['tag_name']
        threeWeaks['tag'+str(i)]['problems'] = problems
        threeWeaks['tag'+str(i)]['explainations'] = explainations
        threeWeaks['tag'+str(i)]['weak_pcr'] = weakTagProblems['tag'+str(i)]['weak_pcr']
    
    problems = {}
    for i in range(1, 4):
        tag_key = 'tag' + str(i)
        
        threeForgotten[tag_key] = {}
        threeForgotten[tag_key]['tag'] = forgottenTagProblems['tag'+str(i)]['tag']
        threeForgotten[tag_key]['forgottenPercent'] = forgottenTagProblems[tag_key]['forgottenPercent']
        
        problems_list = forgottenTagProblems[tag_key]
        # 2를 빼는 이유는 태크와 망각률를 제외하고 문제수를 세기 위함
        rotated_index = rotate % (len(problems_list) - 2)
        cnt = 0
        while cnt < len(problems_list) - 2:
            if checkTier(problems_list['problem' + str(rotated_index)]['level'] ,filter):
                threeForgotten[tag_key]['problem'] = problems_list['problem' + str(rotated_index)]
                break
            else:
                cnt += 1
                rotated_index = (rotated_index + 1) % (len(problems_list) - 2) + 1
        if 'problem' not in threeForgotten[tag_key]:
            threeForgotten[tag_key]['problem'] = {
                'problemID': '',
                'titleKo': '알맞은 문제가 없어요',
                'level': '',
                'averageTries': '',
                'tags': ''
            }
    for i in range(1, 4):
        index = (rotate + i) % len(similarityBasedProblems) + 1
        cnt = 0
        while cnt <= len(similarityBasedProblems):
            tier = similarityBasedProblems['problem'+str(index)]['level']
            if checkTier(tier ,filter):
                threeSimilar['problem'+str(i)] = similarityBasedProblems['problem'+str(index)]
                break
            else:
                index = 3 * (index + 1) % len(similarityBasedProblems) + 1
                cnt += 1
        if 'problem'+str(i) not in threeSimilar:
            threeSimilar['problem'+str(i)] = {
                'problemID': '',
                'titleKo': '알맞은 문제가 없어요',
                'level': '',
                'averageTries': '',
                'tags': ''
            }

    return threeWeaks, threeForgotten, threeSimilar

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
