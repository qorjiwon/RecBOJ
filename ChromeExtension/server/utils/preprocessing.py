import time,os
import pandas as pd
from datetime import datetime, timedelta
import warnings
import ast
from .registerNewUser import *
#from database.connection import *
import psycopg2
from psycopg2 import OperationalError

warnings.filterwarnings(action="ignore")

database_host = os.getenv('DATABASE_HOST')

def DBconnect():
    try:
        global cur, conn
        #Port 지정시 Port Forwarding한 Host의 Port번호를 입력.
        try:
            conn = psycopg2.connect( user="myuser", password="mypassword", host = database_host , port=5433, database="mydatabase") #cursor 객체 생성(Create Object)
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        cur = conn.cursor()
        print("Database Connect Success")
        return cur, conn
    except Exception as err:
        print(str(err))

def DBdisconnect():
    try:
        conn.close()
        cur.close()
        print("DB Connect Close")
    except:
        print("Error: ", "Database Not Connected")


def user_find(user_id):
    try:
        DBconnect()
        query = "SELECT updated_at FROM USER_INFO UI WHERE UI.USER_ID = %s"
        cur.execute(query, (user_id,))
        result = cur.fetchone()

        if result:
            updated_at = result[0]
            time_diff = datetime.now(updated_at.tzinfo) - updated_at
            
            if time_diff > timedelta(hours=3):
                return False
            
            return True
        else:
            return False
    except Exception as e:
        print("Error:", e)
        return False
    
    finally:
        # DB 연결 해제
        DBdisconnect()

def make_df():
    cur, conn = DBconnect()
    print("make_pivot을 위한 DB connection 성공")
    query = """ SELECT COALESCE(PL.USER_ID, 'THISISNOTHUMANJUSTBOT') AS USER_ID, PD.PROBLEM_ID, 1 AS solve, UI.LEVEL 
                FROM PROBLEM_DF PD LEFT JOIN PROBLEM_LOG PL 
                                ON PL.PROBLEM_ID = PD.PROBLEM_ID, USER_INFO UI
                WHERE PL.USER_ID = UI.USER_ID """
    df = pd.read_sql_query(query, conn)
    return df

def make_pivot(df, user_id):
    low_level = 7
    high_level = 13
    try: 
        low_level = min(df[df.user_id == user_id].level) - 2
        high_level = max(df[df.user_id == user_id].level) + 2
    except Exception as e:
        print("low, high 여기가 문제다!!", e)

    # level이 낮은 애들은 컬럼 수가 너무 부족함.
    # EASE모델에 넣을 컬럼 확보를 위해 조정.
    if(high_level <= 10):
        low_level = 0
        high_level = 10
    selected_rows = df[(df['level'] >= low_level) & (df['level'] <= high_level)]
    pivot_df = selected_rows.pivot_table(index='user_id', columns='problem_id', values='solve', aggfunc='sum')
    # NaN 값을 0으로 채우기
    pivot_df = pivot_df.fillna(0).astype(int)
    print(pivot_df.shape)
    DBdisconnect()
    return pivot_df

def make_forgetting_df():
    cur, conned = DBconnect()
    query = """SELECT pl.user_id, pl.problem_id , pl.total_count , pl.wrong_count, pl.last_time, pd.level, pd.averagetries as "averageTries", pd.tags
                FROM PROBLEM_log pl join problem_df pd on pl.problem_id = pd.problem_id """
    df = pd.read_sql_query(query, conned)
    conned.close()
    cur.close()
    print("Make_Pivot의 DB Connect Close")
    return df


def make_user_correct_problem(user_id):
    cur, conn = DBconnect()
    print("User_correct_problem 을 위한 DB connection 성공")
    
    query = """ SELECT CORRECT_PROBLEM
                FROM USER_INFO UI
                WHERE UI.USER_ID = %s """

    cur.execute(query, (user_id, ))
    correct_list_str = cur.fetchone()

    if correct_list_str:
        print(type(correct_list_str[0]))
        correct_list = [int(num) for num in correct_list_str[0]]    
        return correct_list
    else:
        return None 

