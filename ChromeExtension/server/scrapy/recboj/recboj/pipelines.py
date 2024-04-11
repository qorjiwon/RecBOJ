# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import time
import pandas as pd
from recboj.items import *
import os

database_host = os.getenv('DATABASE_HOST', 'localhost')

class RecbojPipeline:
    
    def __init__(self) :
        try:
            self.conn = psycopg2.connect(user="myuser", password="mypassword", host=database_host, port=5433, database="mydatabase")
            self.cur = self.conn.cursor()
            print("Database Connect Success")
        except Exception as err:
            print(str(err)) 


    def process_item(self, item, spider):
        if isinstance(item, User):
            return self.handle_user(item, spider)
        if isinstance(item, Problem):
            return self.handle_problem(item, spider)
    
    def handle_user(self,item, spider) :
        user_id = item.get('user_id')
        level = item.get('level')
        print("handle user 시작합니다")
        sql_query = "INSERT INTO user_info(user_id, level) " \
                "VALUES (%s, %s) " \
                "ON CONFLICT (user_id) DO UPDATE " \
                "SET level = EXCLUDED.level;" 
        data_to_insert = (user_id, level)
        print(user_id, level)
        self.cur.execute(sql_query, data_to_insert)
        self.conn.commit()

        return item

    def handle_problem(self, item, spider) :
        user_id = item.get('user_id')
        problem_id = item.get('problem_id')
        total_count = item.get('total_count')
        wrong_count = item.get('wrong_count')
        last_time = item.get('last_time')
        sql_query = "INSERT INTO problem_log (user_id, problem_id, total_count, wrong_count, " \
                "last_time) " \
                "VALUES (%s, %s, %s, %s, %s) " \
                "ON CONFLICT (user_id, problem_id) DO UPDATE " \
                "SET total_count = EXCLUDED.total_count, " \
                "wrong_count = EXCLUDED.wrong_count, " \
                "last_time = EXCLUDED.last_time;"
        data_to_insert = (user_id, problem_id, total_count, wrong_count, last_time)

        try:
        # 만약 문자열을 정수로 변환할 수 있다면 변환 후 반환
            problem_id = int(problem_id)
        except ValueError:
            # 정수로 변환할 수 없는 경우에는 그대로 문자열로 반환
            problem_id = str(problem_id)

        try:
            last_time = int(last_time)
        except ValueError:
            last_time = str(last_time)

        # Problem_id에 빈 문자열이 들어가는 경우가 존재해 예외처리
        if isinstance(user_id, str) and isinstance(problem_id, int) and isinstance(total_count, int) and isinstance(wrong_count, int) and isinstance(last_time, int):
            self.cur.execute(sql_query, data_to_insert)
            self.conn.commit()
        else:
            print("문제가 발생한 오류 Data :", data_to_insert)
            if not isinstance(user_id, str):
                print("user_id는 문자열이어야 합니다.", type(user_id))
            # problem_id가 정수인지 확인
            if not isinstance(problem_id, int):
                print("problem_id는 정수여야 합니다.", type(problem_id))
            
            # total_count와 wrong_count가 모두 정수인지 확인
            if not isinstance(total_count, int) or not isinstance(wrong_count, int):
                print("total_count와 wrong_count는 모두 정수여야 합니다.")
            
            # last_time이 정수인지 확인
            if not isinstance(last_time, int):
                print("last_time은 정수여야 합니다.", type(last_time))
            pass
            
        return item
    
    def close_spider(self, spider) :
        try:
            self.conn.close()
            self.cur.close()
            print("DB Connect Close")
        except:
            print("Error: ", "Database Not Connected")


