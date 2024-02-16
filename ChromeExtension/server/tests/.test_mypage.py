from fastapi.testclient import TestClient
from app import app  # app.py의 FastAPI 인스턴스 import 경로 확인

client = TestClient(app)

def test_send_mypage_data():
    request_data = {
        "url": "https://www.acmicpc.net/user/crash1522",
        "div": 0,
        "filter": "None"
    }
    response = client.post("/mypage/problems", json=request_data)
    assert response.status_code == 200
    # 여기에 더 많은 assert 문 추가 (응답 데이터 구조에 따라)
