import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from utils.utils import *
from utils.model import *
from utils.preprocessing import *
from utils.recommendation import *
from routes.mypage import mypage_router
from routes.register import register_router
from routes.submit_page import submit_page_router

app = FastAPI()
app.include_router(mypage_router, prefix="/mypage")
app.include_router(register_router, prefix="/register")
app.include_router(submit_page_router, prefix="/submit_page")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# 로깅 레벨 설정
logging.basicConfig(level=logging.DEBUG)
templates = Jinja2Templates(directory="templates")  # 템플릿 파일이 위치한 디렉토리 지정

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)