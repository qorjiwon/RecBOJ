import time,os
import pandas as pd
from datetime import datetime
import warnings
import ast
from .registerNewUser import *
#from database.connection import *
import psycopg2
from psycopg2 import OperationalError
warnings.filterwarnings(action="ignore")

database_host = os.getenv('DATABASE_HOST', 'localhost')

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
        # EXIST문을 통한 사용자 Record 검색
        query = "SELECT EXISTS(SELECT 1 FROM USER_INFO UI WHERE UI.USER_ID = %s)"
        cur.execute(query, (user_id, ))
        result = cur.fetchone()
        
        # 사용자 ID의 존재 여부에 따라 True 또는 False 반환
        if result and result[0]:
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
    low_level = min(df[df.user_id == user_id].level) - 2
    high_level = max(df[df.user_id == user_id].level) + 2
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