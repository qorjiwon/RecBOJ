import requests,time
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup as bs

HEADERS = {"User-illa/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def get_new_user_dataframe(user_id) :
    correct_problem_list, wrong_problem_list = get_problem_history_list(user_id)
    user_info_list = [user_id,correct_problem_list,wrong_problem_list]
    problem_info_list = correct_problem_list + wrong_problem_list
    
    get_each_problem_try_log(problem_info_list)
    user_info_df, user_problem_df = change_list_to_dataframe(user_info_list, problem_info_list)
    return user_info_df, user_problem_df

def get_problem_history_list(user_id) :
    correct_problem_list=[]
    wrong_problem_list=[]
    page = open_main_profile_page(user_id)
    correct_problem_list, wrong_problem_list = get_problem_list(page)
    return correct_problem_list, wrong_problem_list

def open_main_profile_page(user_id) :
    url='https://www.acmicpc.net/user/'+str(user_id)
    req=requests.get(url,headers=HEADERS).text
    page=bs(req,"html.parser")
    return page

def get_problem_list(page) :
    problem_table_list = page.find_all('div', {'class':'panel panel-default'})
    for table in problem_table_list :
        table_title = table.find('h3',{'class':'panel-title'}).text
        if table_title == '맞은 문제' :
            correct = table.find_all('div',{'class':'problem-list'})
            correct_list = correct[0].text.split(' ')[:-1]
        elif table_title == '시도했지만 맞지 못한 문제' :
            wrong = table.find_all('div',{'class':'problem-list'})  
            wrong_list = wrong[0].text.split(' ')[:-1]
    set_index_problem_list(correct_list,wrong_list)
    return correct_list, wrong_list

def set_index_problem_list(correct_list,wrong_list) :
    for idx in range(len(correct_list)) :
        correct_list[idx]=int(correct_list[idx])
    for idx in range(len(wrong_list)) :
        wrong_list[idx]=int(wrong_list[idx])

def get_each_problem_try_log(user_id, problem_list) :
    for problem in problem_list :
        page = open_problem_try_log_page(problem, user_id)
        try :
            problem_list.append(get_problem_try_log(user_id, problem, page))
        except :
            None

def open_problem_try_log_page(problem_id,user_id) :
    url=f'https://www.acmicpc.net/status?problem_id={problem_id}&user_id={user_id}&language_id=-1&result_id=-1'
    req=requests.get(url,headers=HEADERS).text
    page=bs(req,"html.parser")
    return page

def get_problem_try_log(user_id, problem_id, page) :
    total_cnt,wrong_cnt, wrong_timeover, wrong_wrong, wrong_memoryover = [0] * 5
    memory,run_time,language,code_length,last_time = [-1] * 5
    flag=True
    col_list=page.find_all('tr')
    for col in col_list :
        if total_cnt==0 :
            total_cnt+=1
            continue
        total_cnt+=1
        if total_cnt==2 : # 가장 상단으로부터 언어, 코드 길이, 제출한 시간을 받아온다.
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
        problem_info=[user_id,problem_id,total_cnt-1,wrong_cnt,wrong_timeover, wrong_wrong, wrong_memoryover, memory.text,run_time.text,language.text,code_length.text,last_time]
        return problem_info

def change_list_to_dataframe(user_info_list, problem_info_list) :
    user_info_df=pd.DataFrame(user_info_list)
    user_problem_df=pd.DataFrame(problem_info_list)
    user_info_df.columns=['user_id','correct_problem','wrong_problem']
    user_problem_df.columns=['user_id','problem_id','total_count','wrong_count', 'wrong_timeover', 'wrong_wrong', 'wrong_memoryover',
                                                        'memory','time','language','code_length','last_time']
    return user_info_df, user_problem_df