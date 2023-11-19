from flask import Flask, request, render_template, jsonify
from flask_cors import CORS  # CORS 미들웨어 추가
from utils.utils import *
from utils.model import *
import pandas as pd
import threading

app = Flask(__name__)
CORS(app)  # CORS 미들웨어 초기화
lock = threading.Lock()

global weak_strong_forget_df, pivot_table, index_to_id_df, index_to_problem
weak_strong_forget_df = pd.read_csv('/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/data/forgetting_curve_df.csv')
pivot_table = pd.read_csv('/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/data/final_pivottable.csv')
index_to_problem = pd.read_csv('/Users/im_jungwoo/Desktop/project/backup/ChromeExtension/server/data/final_problem_processed.csv')
cache = {}
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
    global cache
    data = request.get_json()
    current_url = data.get('url')
    user_id = extract_user_id_from_mypage(current_url)
    rotate = data.get('div')
    try:
        with lock:
            if rotate == 0:
                strong_tag, weak_tag, strong_pcr, weak_pcr = weak_strong_rec(weak_strong_forget_df, user_id)
                # forget_curve를 이용해서...
                forgotten_tag, forgotten_pcr = forget_curve(weak_strong_forget_df, user_id)
                SolvedBasedProblems = Solved_Based_Recommenation(pivot_table, user_id, index_to_problem, 500)
                weakTagProblems, forgottenTagProblems, similarityBasedProblems = getMypageProblemsDict(SolvedBasedProblems, weak_tag, weak_pcr, forgotten_tag, forgotten_pcr, 30)
                cache[user_id] = {}
                cache[user_id]['weakTagProblems'] = weakTagProblems   
                cache[user_id]['forgottenTagProblems'] = forgottenTagProblems
                cache[user_id]['similarityBasedTagProblems'] = similarityBasedProblems
                threeWeaks, threeForgotten, threeSimilar = cutThreeProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems)
            else:
                weakTagProblems = cache[user_id]['weakTagProblems']
                forgottenTagProblems = cache[user_id]['forgottenTagProblems']
                similarityBasedProblems = cache[user_id]['similarityBasedTagProblems']
                threeWeaks, threeForgotten, threeSimilar = reloadProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems, rotate)
    except:
        user_id = '1000chw'
        if rotate == 0:
            strong_tag, weak_tag, strong_pcr, weak_pcr = weak_strong_rec(weak_strong_forget_df, user_id)
            # forget_curve를 이용해서...
            forgotten_tag, forgotten_pcr = forget_curve(weak_strong_forget_df, user_id)
            SolvedBasedProblems = Solved_Based_Recommenation(pivot_table, user_id, index_to_problem, 500)
            weakTagProblems, forgottenTagProblems, similarityBasedProblems = getMypageProblemsDict(SolvedBasedProblems, weak_tag, weak_pcr, forgotten_tag, forgotten_pcr, 30)
            cache[user_id] = {}
            cache[user_id]['weakTagProblems'] = weakTagProblems   
            cache[user_id]['forgottenTagProblems'] = forgottenTagProblems
            cache[user_id]['similarityBasedTagProblems'] = similarityBasedProblems
            threeWeaks, threeForgotten, threeSimilar = cutThreeProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems)
        else:
            weakTagProblems = cache[user_id]['weakTagProblems']
            forgottenTagProblems = cache[user_id]['forgottenTagProblems']
            similarityBasedProblems = cache[user_id]['similarityBasedTagProblems']
            threeWeaks, threeForgotten, threeSimilar = reloadProblems(weakTagProblems, forgottenTagProblems, similarityBasedProblems, rotate)

    
    responseData = {
            'user_id' : user_id,    
            'weak_tag_problems': threeWeaks,
            'forgotten_tag_problems': threeForgotten,
            'similarity_based_problems': threeSimilar
        }
    # cache가 너무 커지면 비우기
    if len(cache) >= 50:
        cache.clear()
    json_res = json.dumps(responseData)
    return jsonify(message=f'{json_res}')

if __name__ == '__main__':
    app.run('0.0.0.0',8080,debug=True, threaded=True)