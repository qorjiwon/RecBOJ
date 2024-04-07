from gensim.models import Word2Vec
from .utils import *
import json
import boto3
from dotenv import load_dotenv
import os

with open('data/ProblemDict.json', 'r') as f:
    ProblemDict = json.load(f)
with open('data/ProblemTagsDict.json', 'r') as f:
    TagDict = json.load(f)
with open('data/level_to_tier.json', 'r') as f:
    TierDict = json.load(f)

def get_item2vec_problem(problem_id, submits, div) -> dict:
    # 저장된 모델 불러오기
    model = Word2Vec.load("recsys_models/item2vec/word2vec_model.bin") 
    similar_problem = model.wv.most_similar(problem_id, topn= 500)

    problems = {}
    level_flag = get_levelflag(problem_id, submits, ProblemDict)
    problem_list = get_problem_by_level(problem_id, ProblemDict, similar_problem, level_flag)
    print(problem_list)
    for i in range(3): 
        try:
            n = (3 * div + i) % len(problem_list)
            problems['problem'+str(i)] = problem_list[n][0]
            problems['problem'+str(i)+'_similarity'] = problem_list[n][1]
            problems['problem'+str(i)+'_titleKo'] = ProblemDict[problem_list[n][0]]['titleKo']
            problems['problem'+str(i)+'_tags'] = TagDict[problem_list[n][0]]
            problems['problem'+str(i)+'_tier'] = TierDict[str(ProblemDict[problem_list[n][0]]['level'])]
        except:
            pass
    if level_flag == 0:
        problems['message'] = "비슷한 난이도의 문제들에 도전해보세요!"
    elif level_flag == 1:
        problems['message'] = "더 낮은 난이도의 문제들을 문저 풀어보는건 어떨까요?"
    elif level_flag == 2:
        problems['message'] = "더 높은 난이도의 문제들로 레벨업!"
    results = json.dumps(problems)
    return results

class EASE:
    """
    Embarrassingly Shallow Autoencoders model class
    """

    def __init__(self, lambda_):
        self.B = None
        self.lambda_ = lambda_

    def train(self, interaction_matrix):
        """
        train pass
        :param interaction_matrix: interaction_matrix
        """
        G = interaction_matrix.T @ interaction_matrix
        diag = list(range(G.shape[0]))
        G[diag, diag] += self.lambda_
        P = np.linalg.inv(G)

        # B = P * (X^T * X − diagMat(γ))
        self.B = P / -np.diag(P)
        min_dim = min(*self.B.shape)
        self.B[range(min_dim), range(min_dim)] = 0

    def forward(self, user_row):
        """
        forward pass
        """
        return user_row @ self.B
