from fastapi.testclient import TestClient
from app import app  # app.py의 FastAPI 인스턴스 import 경로 확인

client = TestClient(app)

def test_send_related_problem():
    request_data = {
        "url": "https://www.acmicpc.net/status?from_mine=1&problem_id=12738&user_id=crash1522",
        "div": 0,
        "submits": ["맞았습니다!!"]
    }
    response = client.post("/submit_page/", json=request_data)
    assert response.status_code == 200
    # 여기에 더 많은 assert 문 추가 (응답 데이터 구조에 따라)
