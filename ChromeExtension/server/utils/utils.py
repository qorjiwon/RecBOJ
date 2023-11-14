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


def return_user_data():
    user_df = pd.read_csv('/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/utils/final_silvergold_user_with_tag.csv')
    df_user_problems = user_df[['id_to_index', 'target']]
    df_user_problems['solve'] = [1] * len(df_user_problems)
    pivot_table = df_user_problems.pivot_table(index=["id_to_index"], columns=["target"], values="solve")
    column_info = pivot_table.columns
    X = pivot_table.to_numpy()
    X = np.nan_to_num(X)
    return X, column_info


def get_problem_list(user_id):
    user_input, col = return_user_data()
    problem_list = user_input[3000]
    return problem_list
# problem_list는    0    1   2   3   4   5   6   7   8   9  ...
#                 [1.0	NaN	NaN	1.0	NaN	1.0	NaN	1.0	1.0	NaN	...	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN]
#이런식으로 구성되게 만들어야 함.

def ease_recommend_problem(problem_list):
    origin_problem, _ = return_user_data()
    ease = EASE(300)
    ease.train(origin_problem)
    result = ease.forward(problem_list)
    # 풀었던 문제는 리스트에서 제외해야하기 때문
    result[problem_list.nonzero()] = -np.inf

    return result


def vae_recommend_problem(problem_list):
    model = tf.keras.models.load_model('/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/models/VAE/VAE_model_ver3.h5', custom_objects={'vae_loss': vae_loss , 'vae' : vae, 'encoder' : encoder, 'decoder' : decoder})
    origin_problem, _ = return_user_data()
    input_x = np.nan_to_num(problem_list)
    input = np.vstack([origin_problem[0, :], input_x])
    result = model.predict(input)
    result = result[-1, :]
    result[problem_list.nonzero()] = -np.inf

    return result

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
    print(f'avgTries: {avgTries}, wa_nums: {wa_nums}, flag = {flag}')
    return flag

def index_to_problem(top_problems):
    problem_info = pd.read_csv('/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/data/final_problem_processed.csv')
    rec_id = problem_info.loc[top_problems, 'problemId']
    return rec_id    

def Solved_Based_Recommenation(user_id):
        # url에서 필요한 정보를 추출
    #user_id에 맞는 문제 풀이 내역 추출
    solve_problem = get_problem_list(user_id)
    #user 문제 풀이 내역을 통한 추천 문제
    vae_rec = vae_recommend_problem(solve_problem)
    ease_rec = ease_recommend_problem(solve_problem)
    total_rec = ease_rec + vae_rec
    NUM_TOP_PROBLEMS = 3
    top_problems = np.argpartition(-total_rec, NUM_TOP_PROBLEMS) # np.argpartition은 partition과 똑같이 동작하고, index를 리턴.
    top_problems = top_problems[ :NUM_TOP_PROBLEMS]
    problem_id = index_to_problem(top_problems)

    rtn = {}
    cnt = 0
    for item in problem_id:
        rtn['problem'+str(cnt)] = item
        cnt += 1
    return rtn

