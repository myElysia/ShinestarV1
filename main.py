import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
import contextvars

from src.utils.database import lifespan
from src.views import router

# 加载环境变量
load_dotenv()

REQUEST_ID_CTX_KEY = 'request_id'

app = FastAPI(lifespan=lifespan)
app.include_router(router)
# 全局上下文对象，用于存储 request_id
request_id = contextvars.ContextVar(REQUEST_ID_CTX_KEY)

if __name__ == '__main__':
    uvicorn.run(app, host=os.getenv('HOST'), port=int(os.getenv("PORT")))
