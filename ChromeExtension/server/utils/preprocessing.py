import pandas as pd
import time,os,requests
from datetime import datetime
import warnings
from bs4 import BeautifulSoup as bs
import ast
warnings.filterwarnings(action="ignore")

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
    correct_list=[]
    wrong_list=[]
    for table in table_list :
        table_title=table.find('h3',{'class':'panel-title'}).text
        if table_title == '맞은 문제' :
            correct=table.find_all('div',{'class':'problem-list'})
            correct_list=correct[0].text.split(' ')[:-1]
        elif table_title=='시도했지만 맞지 못한 문제' :
            wrong=table.find_all('div',{'class':'problem-list'})  
            wrong_list=wrong[0].text.split(' ')[:-1]
    for idx in range(len(correct_list)) :
        correct_list[idx]=int(correct_list[idx])
    for idx in range(len(wrong_list)) :
        wrong_list[idx]=int(wrong_list[idx])
    return correct_list,wrong_list

def open_problem_page(problem_id,user_id) :
    url=f'https://www.acmicpc.net/status?problem_id={problem_id}&user_id={user_id}&language_id=-1&result_id=-1'
    req=requests.get(url,headers=headers).text
    page=bs(req,"html.parser")
    return page

def get_problem_info(user_id,problem_id,page) :
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
        

def update_new_user(user) :
    u_list=[]
    p_list=[]

    page=open_user_page(user)
    correct_list,wrong_list=get_uer_info(page)
    u_list.append([user,correct_list,wrong_list])
    problem_list=correct_list+wrong_list

    for pro in problem_list :
        page2=open_problem_page(pro,user)
        try :
            p_list.append(get_problem_info(user,pro,page2))
        except :
            None
        
    user_info_df=pd.DataFrame(u_list)
    user_problem_df=pd.DataFrame(p_list)
    
    user_info_df.columns=['user_id','correct_problem','wrong_problem']
    user_problem_df.columns=['user_id','problem_id','total_count','wrong_count', 'wrong_timeover', 'wrong_wrong', 'wrong_memoryover',
                                                        'memory','time','language','code_length','last_time']
    
    return user_info_df, user_problem_df


def make_pivot_table(u_i_df):
    khu_user_info = pd.read_csv('data/final_khu_user_info.csv')
    problem = pd.read_csv('data/final_problem_processed.csv')
    khu_user_info['correct_problem'] = khu_user_info['correct_problem'].apply(ast.literal_eval)
    user_df = pd.concat([khu_user_info, u_i_df],ignore_index=True)
    #khu_user_info에 대한 csv파일 
    user_df.to_csv('data/final_khu_user_info.csv', index = False)
    user_df['id_to_index'] = user_df.index
    
    #id_to_index.csv 만들기
    id_to_index = user_df[['user_id', 'id_to_index']]
    id_to_index.to_csv('data/khu_id_to_index.csv', index = False)
    
    #pivot_table 만들기
    user_df_result = user_df.explode('correct_problem')
    user_df_result['solve'] = [1] * len(user_df_result)
    final_df = pd.merge(user_df_result, problem, left_on='correct_problem', right_on='problemId').drop(columns=['problemId'])
    pivot_table = final_df.pivot_table(index= ['id_to_index'] ,  columns=["Unnamed: 0"], values="solve")
    pivot_table.to_csv('data/khu_pivot_table.csv', index = False)

    return 

def make_forget_df(u_p_df):
    #데이터 불러오기
    transform_csv = pd.read_csv('data/final_khu_user_problem_info.csv').drop(columns=['memory', 'time','language','code_length'])
    transform_csv = pd.concat([transform_csv, u_p_df],ignore_index=True)
    transform_csv.to_csv('data/final_khu_user_problem_info.csv', index = False)
    #망각곡선, 취약유형에 쓰일 데이터프레임 만들기.
    problem_info = pd.read_csv('data/final_problem_processed.csv').drop(columns=['titleKo','official','titles','isSolvable','acceptedUserCount','givesNoRating','Unnamed: 0','Unnamed: 0.1'])
    df = pd.merge(transform_csv, problem_info, left_on='problem_id', right_on='problemId').drop(columns=['problemId'])
    df.to_csv('data/final_khu_forgetting_curve_df.csv', index = False)

    return

def dup_id(user):
    tf_id = pd.read_csv('data/khu_id_to_index.csv')
    a = tf_id['user_id'] == user 
    if (a.sum() > 0):
        return True
    else:
        return False

def make_csv(user):
    try:
        user_tf = dup_id(user)
        if(user_tf == False):
            user_info_df, user_problem_df = update_new_user(user)
            make_pivot_table(user_info_df)
            make_forget_df(user_problem_df)
    except:
        print("error detection")

    return