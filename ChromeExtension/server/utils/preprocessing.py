import time,os
import pandas as pd
from datetime import datetime
import warnings
import ast
from .registerNewUser import *
warnings.filterwarnings(action="ignore")

def make_csv(user_id):
    try:
        if(check_id_duplicate(user_id) == False):
            new_user_info_df, new_user_problem_df = registerNewUser.get_new_user_dataframe(user_id)
            make_new_pivot_table(new_user_info_df)
            make_new_forget_df(new_user_problem_df)
    except:
        print("error detection")

def check_id_duplicate(user_id):
    tf_id = pd.read_csv('data/khu_id_to_index.csv')
    a = tf_id['user_id'] == user_id
    return (a.sum() > 0)

def make_new_pivot_table(u_i_df):
    khu_user_info = pd.read_csv('data/final_khu_user_info.csv')
    problem = pd.read_csv('data/final_problem_processed.csv')
    khu_user_info['correct_problem'] = khu_user_info['correct_problem'].apply(ast.literal_eval)
    user_df = pd.concat([khu_user_info, u_i_df],ignore_index=True)
    #khu_user_info에 대한 csv파일 
    user_df.to_csv('data/final_khu_user_info.csv', index = False)
    user_df['id_to_index'] = user_df.index
    
    #id_to_index.csv 만들기
    id_to_index = user_df[['user_id', 'id_to_index']]
    id_to_index.to_csv('data/khu_id_to_index.csv', index = False)
    
    #pivot_table 만들기
    user_df_result = user_df.explode('correct_problem')
    user_df_result['solve'] = [1] * len(user_df_result)
    final_df = pd.merge(user_df_result, problem, left_on='correct_problem', right_on='problemId').drop(columns=['problemId'])
    pivot_table = final_df.pivot_table(index= ['id_to_index'] ,  columns=["Unnamed: 0"], values="solve")
    pivot_table.to_csv('data/khu_pivot_table.csv', index = False)


def make_new_forget_df(u_p_df):
    #데이터 불러오기
    transform_csv = pd.read_csv('data/final_khu_user_problem_info.csv').drop(columns=['memory', 'time','language','code_length'])
    transform_csv = pd.concat([transform_csv, u_p_df],ignore_index=True)
    transform_csv.to_csv('data/final_khu_user_problem_info.csv', index = False)
    #망각곡선, 취약유형에 쓰일 데이터프레임 만들기.
    problem_info = pd.read_csv('data/final_problem_processed.csv').drop(columns=['titleKo','official','titles','isSolvable','acceptedUserCount','givesNoRating','Unnamed: 0','Unnamed: 0.1'])
    df = pd.merge(transform_csv, problem_info, left_on='problem_id', right_on='problemId').drop(columns=['problemId'])
    df.to_csv('data/final_khu_forgetting_curve_df.csv', index = False)