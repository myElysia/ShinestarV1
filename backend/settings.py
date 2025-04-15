import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from contextvars import ContextVar
from tortoise.contrib.fastapi import register_tortoise

from backend.src.views import router
# 加载环境变量
load_dotenv()

REQUEST_ID_CTX_KEY = 'request_id'
DB_URL: str = f"{os.getenv('DB_TYPE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

app = FastAPI()
app.include_router(router)
# 全局上下文对象，用于存储 request_id
request_id = ContextVar(REQUEST_ID_CTX_KEY)

# 注册Tortoise
register_tortoise(app, db_url=DB_URL, modules={"models": ["backend.src.models"]})

if __name__ == '__main__':
    uvicorn.run(app, host=os.getenv('HOST'), port=int(os.getenv("PORT")))
