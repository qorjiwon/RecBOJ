import scrapy
from scrapy import Spider, Request
from recboj import items
import pandas as pd
import urllib.parse
import json
import requests
from scrapy.utils.defer import maybe_deferred_to_future
import sys

class ProblemInfoSpider(Spider) :
    name = "probleminfo"

    def start_requests(self):
        user_list = list(pd.read_csv('./user_list.csv')['user_id'])
        print(user_list)
        try :
            if (self.newUser != None) :
                user_list = [self.newUser]
        except :
            None
        for user in user_list :
            profile_url = f"https://www.acmicpc.net/status?user_id={user}&result_id=4"
            yield scrapy.Request(url = profile_url, callback = self.parse_user, cb_kwargs = {'user_id':user})

    async def parse_user(self, response, user_id) :
        user = items.User()
        user['user_id'] = user_id
        print(user_id)
        #Problem 정보 가져오기
        problem_list=[]
        for page in range(3) :
            if page != 0 :
                additional_request = Request(url = f"https://www.acmicpc.net/status?user_id={user_id}&result_id=4&top={top}")
                deferred = self.crawler.engine.download(additional_request)
                response = await maybe_deferred_to_future(deferred)
            res = response.xpath('//*[@class="table-responsive"]/table/tbody')
            for index in range(20):
                submission = res.xpath(f'./tr[{index+1}]/td//text()').getall()
                submission_number = submission[0]
                problem_list.append(submission[2])
                if index == 19 :
                    top = submission[0]
        problem_list = set(problem_list)

        #level 정보 받아오기.
        url = f"https://solved.ac/api/v3/user/show?handle={user_id}"
        r_profile = requests.get(url)
        if r_profile.status_code == requests.codes.ok:
            profile = json.loads(r_profile.content.decode('utf-8'))
            level = profile.get('tier')
        else:
            level = 0
        user['level'] = level #level 정보 넣어주면 됌

        # correct problem
        additional_request = Request(url = f"https://www.acmicpc.net/user/{user_id}")
        deferred = self.crawler.engine.download(additional_request)
        response = await maybe_deferred_to_future(deferred)
        user['correct problem'] = response.xpath('//*[@class="problem-list"]')[0].xpath("./a/text()").getall()

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
        