# Base 이미지
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# pip 업그레이드 및 Python 의존성 설치
# python:3.9-slim가 데비안 계열이기 때문에 추가적인 설치 필요
COPY requirements-prod.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# 애플리케이션 코드 복사
COPY . /app

ENV PYTHONPATH=/app

# 포트 8000 열기
EXPOSE 8000

CMD ["python", "app.py"]

# Uvicorn으로 애플리케이션 실행
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]