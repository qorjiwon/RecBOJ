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

from model import *


def return_user_data():
    user_df = pd.read_csv('./silver_gold_half_with_tag.csv')
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
    model = tf.keras.models.load_model('./VAE_model.h5', custom_objects={'vae_loss': vae_loss , 'vae' : vae, 'encoder' : encoder, 'decoder' : decoder})
    origin_problem, _ = return_user_data()
    input_x = np.nan_to_num(problem_list)
    input = np.vstack([origin_problem[0, :], input_x])
    result = model.predict(input)
    result = result[-1, :]
    result[problem_list.nonzero()] = -np.inf

    
    return result
