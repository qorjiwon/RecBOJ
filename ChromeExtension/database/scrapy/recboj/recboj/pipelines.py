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
        correct_problem = item.get('correct_problem')
        wrong_problem = item.get('wrong_problem')
        sql_query = "INSERT INTO user_info(user_id, correct_problem, wrong_problem) " \
                "VALUES (%s, %s, %s) " \
                "ON CONFLICT (user_id) DO UPDATE " \
                "SET correct_problem = EXCLUDED.correct_problem, " \
                "wrong_problem = EXCLUDED.wrong_problem;"
        # 데이터를 정수 배열로 변환
        correct_problems = [int(x) for x in correct_problem]
        wrong_problems = [int(x) for x in wrong_problem]
        data_to_insert = (user_id, correct_problems, wrong_problems)
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
        self.cur.execute(sql_query, data_to_insert)
        self.conn.commit()
        return item
    
    def close_spider(self, spider) :
        try:
            self.conn.close()
            self.cur.close()
            print("DB Connect Close")
        except:
            print("Error: ", "Database Not Connected")