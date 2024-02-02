import requests,time
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup as bs

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

class ProblemList :
    def __init__(self, user_id) :
        self.user_id = user_id
        correct_problem_list=[]
        wrong_problem_list=[]

    def get_problem_list(self) :
        page = self.open_main_profile_page()
        problem_table_list = page.find_all('div', {'class':'panel panel-default'})
        for table in problem_table_list :
            table_title = table.find('h3',{'class':'panel-title'}).text
            if table_title == '맞은 문제' :
                correct = table.find_all('div',{'class':'problem-list'})
                correct_list = correct[0].text.split(' ')[:-1]
            elif table_title == '시도했지만 맞지 못한 문제' :
                wrong = table.find_all('div',{'class':'problem-list'})  
                wrong_list = wrong[0].text.split(' ')[:-1]
        self.set_index_problem_list(correct_list,wrong_list)
        return correct_list, wrong_list

    def open_main_profile_page(self) :
        url='https://www.acmicpc.net/user/'+str(self.user_id)
        req=requests.get(url,headers=HEADERS).text
        page=bs(req,"html.parser")
        return page

    def set_index_problem_list(self, correct_list, wrong_list) :
        for idx in range(len(correct_list)) :
            correct_list[idx] = int(correct_list[idx])
        for idx in range(len(wrong_list)) :
            wrong_list[idx] = int(wrong_list[idx])