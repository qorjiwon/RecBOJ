import pandas as pd
import time,os,requests
import warnings
warnings.filterwarnings(action="ignore")

from bs4 import BeautifulSoup as bs

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

# 문제 번호에 해당하는 페이지
def open_page(problem_id) :
    url="https://www.acmicpc.net/problem/"+str(problem_id)
    req=requests.get(url,headers=headers).text
    page=bs(req,"html.parser")
    return page

# 문제 정보를 dict로 저장
def save_dict(info_list) :
    json={
        'time' : info_list[0],
        'memory' : info_list[1],
        'submission' : info_list[2],
        'solution' : info_list[3],
        'num_people' : info_list[4],
        'rate_correct' : info_list[5]
    }
    return json

# 문제 정보 받아와서 dict 형태로 저장
def get_problem_info(page) :
    # 문제 기본 정보
    problem_info=page.find_all('td')
    info_list=[]
    for td in problem_info :
        td=str(td)
        td=td.replace('<td>','')
        td=td.replace('</td>','')
        info_list.append(td)
    json=save_dict(info_list)
    
    # 문제 텍스트
    problem_text=page.find('div', {'class':'problem-text', 'id':'problem_description'}).text
    return json,problem_text

def main() :
    df_problem=pd.DataFrame()
    start=1000
    end=25000
    for id in range(start,end+1) :
        try :
            page=open_page(id)
            info,text=get_problem_info(page)
            text=text.replace('\n',' ')
            df_problem=pd.concat([df_problem,pd.DataFrame([[id,info,text]])])
        except :
            None
    df_problem.columns=["problem_id","problem_info",'problem_text']
    df_problem.to_csv('problem_df.csv')

if __name__ == "__main__" :
    main()