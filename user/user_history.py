import pandas as pd
import time,os,requests
from datetime import datetime
import warnings
warnings.filterwarnings(action="ignore")

from bs4 import BeautifulSoup as bs

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

# 사용자 정보에 해당하는 페이지
def open_user_page(user_id) :
    url='https://www.acmicpc.net/user/'+str(user_id)
    req=requests.get(url,headers=headers).text
    page=bs(req,"html.parser")
    return page

# 사용자 정보 받아와서 dataframe 형태로 저장
def get_uer_info(page) :
    table_list=page.find_all('div', {'class':'panel panel-default'})
    for table in table_list :
        table_title=table.find('h3',{'class':'panel-title'}).text
        if table_title == '맞은 문제' :
            correct=table.find_all('div',{'class':'problem-list'})
            correct_list=correct[0].text.split(' ')[:-1]
        elif table_title=='시도했지만 맞지 못한 문제' :
            wrong=table.find_all('div',{'class':'problem-list'})  
            wrong_list=wrong[0].text.split(' ')[:-1]
    return correct_list,wrong_list

def open_problem_page(problem_id,user_id) :
    url=f'https://www.acmicpc.net/status?problem_id={problem_id}&user_id={user_id}&language_id=-1&result_id=-1'
    req=requests.get(url,headers=headers).text
    page=bs(req,"html.parser")
    return page

def get_problem_info(user_id,problem_id,page) :
    # 사용자 번호 ,문제 번호, 총 시도 횟수, 틀린 횟수, 맨 위의 맞았습니다에 대한 '메모리, 시간', 언어, 코드 길이, 제출한 시간
    total_cnt,wrong_cnt=[0]* 2
    memory,run_time,language,code_length,last_time=[-1]*5
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
    if -1 in [language,code_length,last_time] :
        print(f'{problem_id}번 문제 수집 과정에서 에러 발생')
        return Exception
    else :
        problem_info=[user_id,problem_id,total_cnt-1,wrong_cnt,memory.text,run_time.text,language.text,code_length.text,last_time]
        return problem_info
        

def main() :
    user_list=pd.read_csv('RecBOJ/data/solvedac_user_data.csv',index_col=0)['handle'][:100]
    user_info_df=pd.DataFrame()
    user_problem_df = pd.DataFrame()
    cnt=0
    for user in user_list :
        cnt+=1
        print(cnt)
        page=open_user_page(user)
        correct_list,wrong_list=get_uer_info(page)
        user_info_df=pd.concat([user_info_df, pd.DataFrame([[user,correct_list,wrong_list]])], ignore_index=True)
        
        problem_list=correct_list+wrong_list
        for pro in problem_list :
            page2=open_problem_page(pro,user)
            try :
                user_problem_df=pd.concat([user_problem_df, pd.DataFrame([get_problem_info(user,pro,page2)])], ignore_index=True)
            except :
                None
        
    user_info_df.columns=['user_id','correct_problem','wrong_problem']
    user_problem_df.columns=['user_id','problem_id','total_count','wrong_count',
                                                        'memory','time','language','code_length','last_time']
    user_info_df.to_csv('user_info_csv')
    user_problem_df.to_csv('user_problem_csv')

if __name__ == "__main__" :
    main()
