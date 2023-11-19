from gensim.models import Word2Vec
from .utils import *
import json
import os
import random
import numpy as np
import pandas as pd
from tqdm import tqdm
import bottleneck as bn
import torch
import tensorflow as tf
from tensorflow import shape,math
from tensorflow.keras import Input,layers,Model
from tensorflow.keras.losses import mse,binary_crossentropy
import warnings

with open('/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/data/ProblemDict.json', 'r') as f:
    ProblemDict = json.load(f)
with open('/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/data/ProblemTagsDict.json', 'r') as f:
    TagDict = json.load(f)
with open('/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/data/level_to_tier.json', 'r') as f:
    TierDict = json.load(f)
  

def get_item2vec_problem(problem_id, submits, div):
    # 저장된 모델 불러오기
    model = Word2Vec.load("/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/models/item2vec/word2vec_model.bin") 
    similar_problem = model.wv.most_similar(problem_id, topn= 500)

    problems = {}
    level_flag = get_levelflag(problem_id, submits, ProblemDict)
    problem_list = get_problem_by_level(problem_id, ProblemDict, similar_problem, level_flag)
    print(problem_list)
    for i in range(3): 
        try:
            n = (3 * div + i) % len(problem_list)
            problems['problem'+str(i)] = problem_list[n][0]
            problems['problem'+str(i)+'_similarity'] = problem_list[n][1]
            problems['problem'+str(i)+'_titleKo'] = ProblemDict[problem_list[n][0]]['titleKo']
            problems['problem'+str(i)+'_tags'] = TagDict[problem_list[n][0]]
            problems['problem'+str(i)+'_tier'] = TierDict[str(ProblemDict[problem_list[n][0]]['level'])]
        except:
            pass
    if level_flag == 0:
        problems['message'] = "비슷한 난이도의 문제들에 도전해보세요!"
    elif level_flag == 1:
        problems['message'] = "더 낮은 난이도의 문제들을 문저 풀어보는건 어떨까요?"
    elif level_flag == 2:
        problems['message'] = "더 높은 난이도의 문제들로 레벨업!"
    results = json.dumps(problems)
    return results

# network parameters
input_shape = 5221
original_dim= input_shape
intermediate_dim = 512
latent_dim = 2

def encoder():
  inputs = Input(shape=(input_shape,), name='input_shape')

  encoder_hidden = layers.Dense(intermediate_dim, activation='relu', name='encoder_hidden1')(inputs)

  z_mean = layers.Dense(latent_dim, name='z_mean')(encoder_hidden)
  z_log_var = layers.Dense(latent_dim, name='z_log_var')(encoder_hidden)

  def sampling(args):
      z_mean, z_log_var = args
      batch = shape(z_mean)[0]
      dim = shape(z_mean)[1]

      # by default, random_normal has mean = 0 and std = 1.0
      # Reparameterization Trick사용을 위해 Gussian(=normal)분포에서 랜덤변수(sample) ε추출
      epsilon = tf.compat.v2.random.normal(shape=(batch, dim))
      return z_mean + tf.math.exp(0.5 * z_log_var) * epsilon

  #  layers.Lambda API 래핑에 사용할 함수와, 유닛수(n,)를 지정합니다.
  z_sampling = layers.Lambda(sampling, (latent_dim,), name='z_sample')([z_mean, z_log_var])

  # 하나의 입력과 다중충력을 포함하는 encoder 모델을 만듭니다.
  return Model(inputs,[z_mean,z_log_var,z_sampling], name='encoder')

def decoder():

  # 디코더의 입력층을 생성합니다. (Decoder의 입력은 latent입니다)
  input_z = Input(shape=(latent_dim,), name='input_z')

  # 디코더의 hidden층을 생성합니다. 인코더와 동일하게 500개의 유닛을 사용했습니다.
  decoder_hidden = layers.Dense(intermediate_dim, activation='relu', name='decoder_hidden')(input_z)

  # 디코더의 출력층은 인코더 입력벡터 수만큼 유닛을 사용합니다.
  outputs = layers.Dense(original_dim, activation='sigmoid',name='output')(decoder_hidden)

  return Model(input_z, outputs, name='decoder')

def vae():
  # vae는 입력으로 이미지로 들어와 encoder를 통해 z_sampling 되어 decoder로 출력됩니다.
  inputs = Input(shape=(input_shape,), name='input_shape')
  outputs = decoder(encoder(inputs)[2]) #[0]:z_mean, [1]:z_log_var,[2]:z_sampling

  return Model(inputs,outputs, name='vae_mlp')

def vae_loss(x,recon_x):
    # (1)Reconstruct loss (Marginal_likelihood) : Cross-entropy
    z_mean,z_log_var,z_sampling = encoder(x)
    recon_x=decoder(z_sampling)
    reconstruction_loss = binary_crossentropy(x,recon_x)
    #reconstruction_loss = mse(inputs, outputs)
    reconstruction_loss *= original_dim
    # (2) KL divergence(Latent_loss)
    kl_loss = 0.5 * tf.reduce_sum(tf.square(z_mean)+ tf.exp(z_log_var)- z_log_var -1, 1)
    return tf.reduce_mean(reconstruction_loss + kl_loss) #ELBO(=VAE_loss)

def return_user_data(pivot_table):
    column_info = pivot_table.columns
    X = pivot_table.to_numpy()
    X = np.nan_to_num(X)
    return X, column_info

def get_problem_list(user_input, user_id):
    #이 위에는 이제 user_id가 들어오면 user_id에 맞는 pivot_table에서의 행을 추출하는 코드를 작성 예정
    problem_list = user_input[0]
    return problem_list

# problem_list는    0    1   2   3   4   5   6   7   8   9  ...
#                 [1.0   NaN   NaN   1.0   NaN   1.0   NaN   1.0   1.0   NaN   ...   NaN   NaN   NaN   NaN   NaN   NaN   NaN   NaN   NaN   NaN]
#이런식으로 구성되게 만들어야 함.
def vae_recommend_problem(problem_list, origin_problem):
    model = tf.keras.models.load_model('/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/models/VAE/VAE_model_ver3.h5', custom_objects={'vae_loss': vae_loss , 'vae' : vae, 'encoder' : encoder, 'decoder' : decoder})
    input_x = np.nan_to_num(problem_list)
    input = np.vstack([origin_problem[0, :], input_x])
    result = model.predict(input)
    result = result[-1, :]
    result[problem_list.nonzero()] = -np.inf
    
    return result

def index_to_problem(problem_info, top_problems):
    rec_id = problem_info.loc[top_problems, 'problemId']
    return rec_id    

def Solved_Based_Recommenation(pivot_table, user_id, itpr, NUM_TOP_PROBLEMS = 3):
    # url에서 필요한 정보를 추출
    #user_id에 맞는 문제 풀이 내역 추출
    origin_solution, _ = return_user_data(pivot_table)
    user_solution = get_problem_list(origin_solution, user_id)
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
                    print(f'추천 문제가 {num_to_extract}개 보다 적습니다')
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
