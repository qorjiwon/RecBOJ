from flask import Flask, request, render_template, jsonify
from flask_cors import CORS  # CORS 미들웨어 추가
from utils.utils import *
from utils.model import *

app = Flask(__name__)
CORS(app)  # CORS 미들웨어 초기화

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_url', methods=['POST'])
def send_url():
    # url을 받아옴
    data = request.get_json()
    current_url = data.get('url')
    # url에서 필요한 정보를 추출
    user_id = extract_user_id_from_url(current_url)
    problem_id = extract_problem_id_from_url(current_url)
    
    submits = data.get('submits')
    
    # 터미널에 데이터 출력
    print(f'Received URL: {current_url}\nUser ID: {user_id}\nProblem ID: {problem_id}')  
    print(submits)
    
    problems = get_item2vec_problem(problem_id, submits)
    return jsonify(message=f'{problems}')


if __name__ == '__main__':
    app.run('0.0.0.0',8080,debug=True)
