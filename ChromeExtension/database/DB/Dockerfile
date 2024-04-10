# 첫 번째 단계: PostgreSQL 이미지 기반으로 시작
FROM postgres:14.0 AS postgres-server

# 환경 변수 설정을 통해 사용자, 비밀번호, 데이터베이스를 생성
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydatabase