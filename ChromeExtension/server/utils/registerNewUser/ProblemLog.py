import sys, os
import requests,time
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp
from User import *
sys.path.append(os.getcwd())

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

class ProblemLog :
    def __init__(self,user_id, problem_list) :
        self.user_id = user_id
        self.problem_list = problem_list

    def do_crawling(self):
        async def main():
            async with aiohttp.ClientSession() as session :
                problem_info_list = []
                await asyncio.gather(*[self.fetch(session, problem, problem_info_list) for problem in self.problem_list])
            return problem_info_list
        return asyncio.run(main())

    async def fetch(self, session, problem_id, problem_info_list):
        async with session.get(url = f'https://www.acmicpc.net/status?problem_id={problem_id}&user_id={self.user_id}&language_id=-1&result_id=-1', 
                               headers = HEADERS) as response:
            html = await response.text()
            page= bs(html,"html.parser")
            try :
                problem_info_list.append(self.get_problem_try_log(problem_id, page))
            except :
                None

    def get_problem_try_log(self, problem_id, page) :
        total_cnt,wrong_cnt, wrong_timeover, wrong_wrong, wrong_memoryover = [0] * 5
        memory,run_time,language,code_length,last_time = [-1] * 5
        flag = True
        col_list=page.find_all('tr')
        for col in col_list :
            if total_cnt == 0 :
                total_cnt+=1
                continue
            total_cnt+=1
            if total_cnt == 2 : # 가장 상단으로부터 언어, 코드 길이, 제출한 시간을 받아온다.
                language,code_length,last_time=col.find_all('td')[6:]
                last_time=col.find('a',{'class':'real-time-update'})['title']
                last_time=time.mktime(datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S').timetuple())
            if '맞았습니다!!' in str(col.text) or '100점' in str(col.text) : 
                if flag : # 맨 처음 등장한 '맞았습니다'에 대해서 메모리와 시간을 받아온다.
                    memory,run_time=col.find_all('td')[4:6]
            else : # 결과가 '맞았습니다'가 아니라면 틀린 횟수 증가
                wrong_cnt+=1
                if '시간 초과' in str(col.text) : wrong_timeover += 1
                elif '틀렸습니다' in str(col.text) : wrong_wrong += 1
                elif '메모리 초과' in str(col.text): wrong_memoryover += 1
        if -1 in [language,code_length,last_time] :
            print(f'{problem_id}번 문제 수집 과정에서 에러 발생')
            return Exception
        else :
            problem_info=[self.user_id,problem_id,total_cnt-1,wrong_cnt,wrong_timeover, wrong_wrong, wrong_memoryover, memory.text,run_time.text,language.text,code_length.text,last_time]
            return problem_info