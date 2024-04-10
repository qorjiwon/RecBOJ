import psycopg2
from psycopg2 import OperationalError
import pandas as pd
import os
import json
from time import sleep
import requests
import ast

database_host = os.getenv('DATABASE_HOST', 'localhost')

def DBconnect():
    try:
        global cur, conn
        #Port 지정시 Port Forwarding한 Host의 Port번호를 입력.
        try:
            conn = psycopg2.connect(user="myuser", password="mypassword", host= database_host, port=5433, database="mydatabase") #cursor 객체 생성(Create Object)
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

def create_user_table():
    create_user_query = """
    CREATE TABLE IF NOT EXISTS user_info (
        user_id text PRIMARY KEY,
        level int
    );"""
    cur.execute(create_user_query)
    conn.commit()
    print("user_table complete")
    
def create_problem_table():
    create_problem_query = """
    CREATE TABLE IF NOT EXISTS problem_df (
        problem_id int PRIMARY KEY,
        titleKo	text NOT NULL,
        level int NOT NULL,
        averageTries numeric NOT NULL,
        tags text
    );"""
    cur.execute(create_problem_query)
    conn.commit()
    print("problem_table complete")


# 크롤링 코드에는 problem_df가 없기 때문에 일단 외래키에서 제외.
def create_problem_log():
    create_log_query = """
    CREATE TABLE IF NOT EXISTS problem_log (
        user_id text REFERENCES user_info(user_id),
        problem_id int ,
        total_count int NOT NULL,
        wrong_count int NOT NULL,
        last_time BIGINT NOT NULL,
        PRIMARY KEY (user_id, problem_id)
    );"""
    cur.execute(create_log_query)
    conn.commit()
    print("problem_log table complete")

    
def create_database():
    create_user_table()
    create_problem_table()
    create_problem_log()

def get_many_problemData(start,end):
    problem_id = 0
    try:
        df = pd.DataFrame()
        allData = []
        
        for idx in range(start, end+1,100):
            id = ''
            if end - idx >= 100:
                for num in range(idx,idx+99):
                    id += str(num) + ","
                id += str(idx+99)
            else:
                for num in range(idx,end):
                    id += str(num) + ","
                id += str(end)
            
            problem_id = id
            
            url = f"https://solved.ac/api/v3/problem/lookup?problemIds={id}"
            r_profile = requests.get(url)
            if r_profile.status_code == requests.codes.too_many_requests: 
                print(f"{idx}번째 처리 중 Error 429 발생")
                sleep(500)
                url = f"https://solved.ac/api/v3/problem/lookup?problemIds={id}"
                r_profile = requests.get(url)
    
            profile = json.loads(r_profile.content.decode('utf-8'))
            allData = allData + profile
        
        for data in allData:  
            tag = ""
            tags = data["tags"]
            for t in tags:
                tag += t['key'] +','
            data["tags"] = tag
            df = df._append(data,ignore_index = True)

        return df
        
    except Exception as e:    
        print(f'{problem_id}예외가 발생했습니다.', e)

def extract_ko_rows(row):
    if isinstance(row, list):
        for item in row:
            if 'language' in item and item['language'] == 'ko':
                return True
    return False


def insert_problem():
    problem_df = get_many_problemData(1000, 25000) 
    filtered_df = problem_df[(problem_df['titles'].apply(extract_ko_rows)) & (problem_df['level'] != 0)]
    print(len(filtered_df))

    table_name = 'problem_df'
    for index, row in filtered_df.iterrows():
        cur.execute(f"INSERT INTO {table_name} (problem_id , titleKo, level , averagetries , tags) VALUES (%s, %s, %s, %s, %s)",
                    (row['problemId'],row['titleKo'] ,row['level'], row['averageTries'], row['tags'])
                    )
    conn.commit()

def main() :
    DBconnect()
    create_database()
    insert_problem()
    DBdisconnect()

if __name__ == "__main__" :
    main()
