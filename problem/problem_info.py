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

# 문제 정보 받아와서 dict 형태로 저장
def get_problem_info(page) :
    # 문제 기본 정보
    problem_info=page.find_all('td')
    info_list=[]
    cnt=0
    for td in problem_info :
        cnt+=1
        if cnt==7 :
            break
        td=str(td)
        td=td.replace('<td>','')
        td=td.replace('</td>','')
        info_list.append(td)  
    # 문제 텍스트
    problem_text=page.find('div', {'class':'problem-text', 'id':'problem_description'})
    problem_text=problem_text.text.replace('\n','').replace('\xa0',' ')
    info_list.append(problem_text)
    return info_list

def main() :
    df_problem=pd.read_csv('RecBOJ/data/kor_problem_list.csv',index_col=0)
    cnt=0
    problem_list=[]
    for id in df_problem['0'] :
        cnt+=1
        if cnt%100 == 0 :
            print(f'{cnt}개 완료!')
        if cnt%1000==0 :
            temp_df=pd.DataFrame(problem_list)
            temp_df.columns=["problem_id","time",'memory','submission','solution','num_people','rate_correct','problem_text']
            temp_df.to_csv('temp_problem_df.csv')
        try :
            page=open_page(id)
            info=get_problem_info(page)
            problem_list.append([id]+info)
        except :
            None
    problem_info_df=pd.DataFrame(problem_list)
    problem_info_df.columns=["problem_id","time",'memory','submission','solution','num_people','rate_correct','problem_text']
    problem_info_df.to_csv('problem_df.csv')

if __name__ == "__main__" :
    main()