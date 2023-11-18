from flask import Flask, request, render_template, jsonify
from flask_cors import CORS  # CORS 미들웨어 추가
from utils.utils import *
from utils.model import *
import pandas as pd

app = Flask(__name__)
CORS(app)  # CORS 미들웨어 초기화

global weak_strong_forget_df, pivot_table, index_to_id_df, index_to_problem
weak_strong_forget_df = pd.read_csv('/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/data/forgetting_curve_df.csv')
pivot_table = pd.read_csv('/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/data/final_pivottable.csv')
index_to_problem = pd.read_csv('/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/data/final_problem_processed.csv')
#index_to_id_df 
# 얘는 나중에 경희대학교 학생 데이터 만들면 넣을 예정 


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_url', methods=['POST'])
def sendRelatedProblem():
    # url을 받아옴
    data = request.get_json()
    current_url = data.get('url')
    div = data.get('div')
    # url에서 필요한 정보를 추출
    user_id = extract_user_id_from_url(current_url)
    problem_id = extract_problem_id_from_url(current_url)
    
    submits = data.get('submits')
    
    # 터미널에 데이터 출력
    print(f'Received URL: {current_url}\nUser ID: {user_id}\nProblem ID: {problem_id}')  
    print(submits)
    problems = get_item2vec_problem(problem_id, submits, div)
    return jsonify(message=f'{problems}')


@app.route('/tags', methods=['POST'])
def send_tags():
    data = request.get_json()
    current_url = data.get('url')
    user_id = extract_user_id_from_mypage(current_url)
    
    submits = data.get('submits')
    
    tags = {}
    tags["strong0"] = "DP"
    tags["strong1"] = "Graphs"
    tags["strong2"] = "Greedy"
    tags["weak0"] = "String"
    tags["weak1"] = "DataStruct"
    tags["weak2"] = "Search"
    print(tags)
    return jsonify(message=f'{tags}')


@app.route('/mypage/problems', methods=['POST'])
def send_mypage_data():
    data = request.get_json()
    current_url = data.get('url')
    user_id = extract_user_id_from_mypage(current_url)
    user_id = '1000chw'
    submits = data.get('submits')
 
    strong_tag, weak_tag, strong_pcr, weak_pcr = weak_strong_rec(weak_strong_forget_df, user_id)
    # forget_curve를 이용해서...
    forgotten_tag, forgotten_pcr = forget_curve(weak_strong_forget_df, user_id)
    
    SolvedBasedProblems = Solved_Based_Recommenation(pivot_table, user_id, index_to_problem, 500)
    print(forgotten_tag, forgotten_pcr)
    print(strong_tag, weak_tag)
    print(strong_pcr, weak_pcr)
    
    weakTagProblems = {}
    for i in range(3):
        problems = []
        explainations = []
        for j in range(3):
            response = getProblemsByTag(SolvedBasedProblems, weak_tag[i])    
            problems.append(response['problem'+str(j+1)]['problemID'])
            tem = []
            for value in response['problem'+str(j+1)].values():
                tem.append(value)
            explainations.append(tem)
        weakTagProblems['tag'+str(i+1)] = {
            'tag_name' : weak_tag[i],
            'problems' : problems,
            'explainations' : explainations,
            'weak_pcr' : weak_pcr[i]
        }
    
    forgottenTagProblems = {}
    for i in range(3):
        problems = {}
        problems['tag'] = forgotten_tag[i]
        problems['forgottenPercent'] = forgotten_pcr[i]
        response = getProblemsByTag(SolvedBasedProblems, forgotten_tag[i])    
        problems['problem'] = response['problem'+str(1)]
        forgottenTagProblems['tag'+str(i+1)] = problems
    
    similarityBasedProblems = {}
    for j in range(3):
        response = getProblemsByTag(SolvedBasedProblems, forgotten_tag[i])    
        similarityBasedProblems['problem'+str(j+1)] = response['problem'+str(j+1)]

    responseData = {
        'weak_tag_problems': weakTagProblems,
        'forgotten_tag_problems': forgottenTagProblems,
        'similarity_based_problems': similarityBasedProblems
    }

    pretty_print(responseData)
    json_res = json.dumps(responseData)
    return jsonify(message=f'{json_res}')
    
if __name__ == '__main__':
    app.run('0.0.0.0',8080,debug=True)