import scrapy
from scrapy import Spider
from recboj import items
import pandas as pd
import urllib.parse
import json
import requests

class ProblemInfoSpider(Spider) :
    name = "probleminfo"

    def start_requests(self):
        #user_list = list(pd.read_csv('./khu_id_to_index.csv')['user_id'])[:4]
        user_list = ["eu2525"]
        base_url = "https://www.acmicpc.net/user/"
        for user in user_list :
            profile_url = base_url + user
            yield scrapy.Request(url = profile_url, callback = self.parse_user, cb_kwargs = {'user_id':user})

    def parse_user(self, response, user_id) :
        user = items.User()
        user['user_id'] = user_id
        res = response.xpath('//*[@class="problem-list"]')
        for index, link in enumerate(res):
            if index == 0 :
                user['correct_problem'] = link.xpath("./a/text()").getall()
            else :
                user['wrong_problem'] = link.xpath('./a/text()').getall()
        problem_list = response.xpath('//*[@class="problem-list"]/a/text()').getall()
        
        #level 정보 받아오기.
        url = f"https://solved.ac/api/v3/user/show?handle={user_id}"
        r_profile = requests.get(url)
        if r_profile.status_code == requests.codes.ok:
            profile = json.loads(r_profile.content.decode('utf-8'))
            level = profile.get('tier')
        else:
            level = 0
        user['level'] = level #level 정보 넣어주면 됌
        yield user
        for problem in problem_list :
            problem= urllib.parse.unquote(problem)
            problem_url = f'https://www.acmicpc.net/status?problem_id={problem}&user_id={user_id}&language_id=-1&result_id=-1'
            yield scrapy.Request(url = problem_url, callback = self.parse_problem, cb_kwargs={'id':user_id,'pro':problem})
    
    def parse_problem(self, response, id, pro) :
        log = items.Problem()
        log['user_id'] = id
        log['problem_id'] = pro
        log['total_count'] = len(response.xpath('//*[@class="result"]').getall())
        log['wrong_count'] = sum([False if (result == '맞았습니다!!' or result == '100점') else True for result in response.xpath('//*[@class="result"]/span/text()').getall()])
        log['last_time'] = response.xpath('//*[@class="real-time-update show-date "]/@data-timestamp').get()
        yield log
        