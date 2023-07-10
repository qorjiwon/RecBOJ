import pandas as pd
import time , os, requests
import warnings
warnings.filterwarnings(action='ignore')

from bs4 import BeautifulSoup as bs

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

def get_course_detail(total_course):
    init_url = "https://www.acmicpc.net/workbook/view/"

    data_all_df = pd.DataFrame({}, columns=['course_id', 'problem_list'])
    course_list=[]

    for num in range(len(total_course)): 
        page = total_course['course_id'][num]

        url = init_url+str(page)
        req = requests.get(url, headers=headers).text
        page_source = bs(req, "html.parser")

        try :
            detail = page_source.find('div', {'class':'page-header'}).text
            content_box = page_source.find_all('tr')[1:]

            ## -- get content
            for content in content_box:
                problem_id = content.find('td').text
                try : 
                    title = content.find_all('a')[0].text

                    try:
                        correct_count = content.find_all('a')[1].text
                        submmission_count = content.find_all('a')[2].text
                    except:
                        correct_count = '-'
                        submmission_count = '-'
                    correct_ratio = content.find_all('td')[-1]
                    correct_ratio=correct_ratio.text
                    course_id = page
                    flash_data = [course_id, problem_id, title, correct_count, submmission_count, correct_ratio]
                    course_list.append(flash_data)
                except :
                    None      
            # time.sleep()
            print(f"{total_course['course_name'][num]}'s course extract complete!")
            if num % 500 == 0:
                print(f"{num}개 완료!")
                time.sleep(10)
        except :
            None   
    data_all_df=pd.DataFrame(course_list)
    data_all_df.columns=['course_id','problem_id','title','correct_count','submission_count','correct_ratio']
    return data_all_df


if __name__ == '__main__':
    total_course = pd.read_csv('RecBOJ/data/course_data_list.csv')
    course_detail = get_course_detail(total_course)
    course_detail.to_csv('course_detail.csv', index=False)
    print('Done!')