import psycopg2
from psycopg2 import OperationalError
import pandas as pd
import os

database_host = os.getenv('DATABASE_HOST', 'localhost')

def DBconnect():
    try:
        global cur, conn
        #Port 지정시 Port Forwarding한 Host의 Port번호를 입력.
        try:
            conn = psycopg2.connect( user="myuser", password="mypassword", host= database_host, port=5432, database="mydatabase") #cursor 객체 생성(Create Object)
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
        correct_problem int[] NOT NULL,
        wrong_problem int[] NOT NULL
    );"""
    cur.execute(create_user_query)
    conn.commit()
    print("user_table complete")
    
def create_problem_table():
    create_problem_query = """
    CREATE TABLE IF NOT EXISTS problem_df (
        problem_id int PRIMARY KEY,
        level int NOT NULL,
        averageTries numeric NOT NULL,
        tag text
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

def insert_problem():
    problem_df = pd.read_csv('./final_problem_df.csv')
    table_name = 'problem_df'
    for index, row in problem_df.iterrows():
        cur.execute(f"INSERT INTO {table_name} (problem_id , level , averagetries , tag) VALUES (%s, %s, %s, %s)",
                    (row['problemId'], row['level'], row['averageTries'], row['tags'])
                    )
    conn.commit()

def main() :
    DBconnect()
    create_database()
    insert_problem()
    DBdisconnect()

if __name__ == "__main__" :
    main()