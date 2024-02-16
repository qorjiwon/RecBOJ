from fastapi import APIRouter
import pandas as pd
import asyncio

from utils.preprocessing import make_csv
from models.register import *

register_router = APIRouter(
    tags=["register"]
)

lock = asyncio.Lock()

@register_router.post("/")
async def register(request_data: RegisterRequest):
    global weak_strong_forget_df, pivot_table, id_to_index

    user_id = request_data.user_id
    print("Registered: ", user_id)
    try:
        make_csv(user_id)
        async with lock:
            weak_strong_forget_df = pd.read_csv('data/final_khu_forgetting_curve_df.csv').drop(columns=['memory','time','language','code_length'])
            pivot_table = pd.read_csv('data/khu_pivot_table.csv')
            id_to_index = pd.read_csv('data/khu_id_to_index.csv')
        print("╔══════════════════════╗")
        print("║       Complete!      ║")
        print("╚══════════════════════╝")
    except:
        print("Register Error!")
        
    return f'입력받은 아이디: {user_id}'
