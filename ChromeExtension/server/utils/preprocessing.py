import time,os
import pandas as pd
from datetime import datetime
import warnings
import ast
from .registerNewUser import *
from database.connection import *
warnings.filterwarnings(action="ignore")

def make_pivot():
    database_host = os.getenv('DATABASE_HOST','localhost')
    cur, conn = DBconnect()
    query = """SELECT COALESCE(USER_ID, 'THISISNOTHUMANJUSTBOT') AS USER_ID, PD.PROBLEM_ID, 1 AS solve 
               FROM PROBLEM_DF PD LEFT JOIN PROBLEM_LOG PL 
                                  ON PL.PROBLEM_ID = PD.PROBLEM_ID"""
    df = pd.read_sql_query(query, conn)
    pivot_df = df.pivot_table(index='user_id', columns='problem_id', values='solve', aggfunc='sum')
    # NaN 값을 0으로 채우기
    pivot_df = pivot_df.fillna(0).astype(int)
    DBdisconnect()
    return pivot_df

def make_forgetting_df():
    database_host = os.getenv('DATABASE_HOST', 'localhost')
    conned = psycopg2.connect(user= "myuser", password = "mypassword", host = database_host, port = 5432, database="mydatabase")

    print("자아 드갔다")
    query = """SELECT pl.user_id, pl.problem_id , pl.total_count , pl.wrong_count, pl.last_time, pd.level, pd.averagetries, pd.tag
               FROM PROBLEM_log pl join problem_df pd on pl.problem_id = pd.problem_id """
    df = pd.read_sql_query(query, conned)
    return df