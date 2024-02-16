from .model import *
from .utils import *
import pandas as pd
from time import time   
import numpy as np

def vae_recommend_problem(problem_list, origin_problem):
    model = tf.keras.models.load_model('recsys_models/VAE/VAE_model_final_amd.h5', custom_objects={'vae_loss': vae_loss , 'vae' : vae, 'encoder' : encoder, 'decoder' : decoder})
    input_x = np.nan_to_num(problem_list)
    input = np.vstack([origin_problem[0, :], input_x])
    result = model.predict(input)
    result = result[-1, :]
    result[problem_list.nonzero()] = -np.inf
    
    return result


def Solved_Based_Recommenation(pivot_table, user_id, itpr, id_to_index ,NUM_TOP_PROBLEMS = 3):
    # url에서 필요한 정보를 
    #user_id에 맞는 문제 풀이 내역 추출
    origin_solution, _ = return_user_data(pivot_table)
    user_solution = get_problem_list(origin_solution, user_id, id_to_index)
    #user 문제 풀이 내역을 통한 추천 문제
    total_rec = vae_recommend_problem(user_solution, origin_solution)
    top_problems = np.argpartition(-total_rec, NUM_TOP_PROBLEMS) # np.argpartition은 partition과 똑같이 동작하고, index를 리턴.
    top_problems = top_problems[ :NUM_TOP_PROBLEMS]    
    problem_id = index_to_problem(itpr, top_problems)

    rtn = {}
    cnt = 0
    for item in problem_id:
        rtn['problem'+str(cnt)] = item
        cnt += 1
    return rtn

def getProblemsByTag(SolvedBaseProblems, tag):
    returnData = {}
    idx = 1
    for problem in SolvedBaseProblems.values():
        try:
            problem = str(problem)
            
            if tag in TagDict[problem]:
                returnData["problem"+str(idx)] = {
                    "problemID" : problem,
                    "titleKo" : ProblemDict[problem]['titleKo'],
                    "level" : TierDict[str(ProblemDict[problem]['level'])],
                    "averageTries" : round(ProblemDict[problem]['averageTries'], 1),
                    "tags": TagDict[problem][0]
                }
                idx += 1
        except:
            print(f'호환되지 데이터가 있습니다. {problem}가 Dictionary안에 없습니다')
    return returnData


def getMypageProblemsDict(SolvedBasedProblems, weak_tag, weak_pcr, forgotten_tag, forgotten_pcr, num_to_extract = 15):

    weakTagProblems = {}
    forgottenTagProblems = {}
    similarityBasedProblems = {}

    for i in range(3):
        problems = []
        explainations = []
        for j in range(num_to_extract):
            try:
                response = getProblemsByTag(SolvedBasedProblems, weak_tag[i])    
                problems.append(response['problem'+str(j+1)]['problemID'])
                tem = []
                for value in response['problem'+str(j+1)].values():
                    tem.append(value)
                explainations.append(tem)
            except:
                pass
        weakTagProblems['tag'+str(i+1)] = {
            'tag_name' : weak_tag[i],
            'problems' : problems,
            'explainations' : explainations,
            'weak_pcr' : weak_pcr[i]
        }
    
    try:
        for i in range(3):
            problems = {}
            problems['tag'] = forgotten_tag[i]
            problems['forgottenPercent'] = forgotten_pcr[i]
            response = getProblemsByTag(SolvedBasedProblems, forgotten_tag[i])    
            for j in range(num_to_extract):
                try:
                    problems['problem'+str(j+1)] = response['problem'+str(j+1)]
                except:
                    pass
            forgottenTagProblems['tag'+str(i+1)] = problems
    except:
        pass

    try:
        for j in range(num_to_extract):
            try:
                similarityBasedProblems['problem'+str(j+1)] = {}
                problem =  str(SolvedBasedProblems['problem'+str(j+1)])
                similarityBasedProblems['problem'+str(j+1)] = {
                            "problemID" : problem,
                            "titleKo" : ProblemDict[problem]['titleKo'],
                            "level" : TierDict[str(ProblemDict[problem]['level'])],
                            "averageTries" : round(ProblemDict[problem]['averageTries'], 1),
                            "tags": TagDict[problem][0]
                        }
            except:
                print(f'호환되지 데이터가 있습니다. {problem}가 Dictionary에 없습니다')    
    except:
        pass

    return weakTagProblems, forgottenTagProblems, similarityBasedProblems

def weak_strong_rec(df, user_id):
    df = df[df['user_id'] == user_id]
    # 개념 문제에 대해서만 할건지...??
    # df = df[df['level'] <= 10]
    # 평균 시도 횟수를 기준으로 나눔.
    weak_problem = df[(df['wrong_count'] + 1) > df['averageTries']]
    strong_problem = df[(df['wrong_count'] + 1 )<= df['averageTries']]
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