from dotenv import load_dotenv
from fastapi import FastAPI

from backend.src.views import router

load_dotenv()
app = FastAPI()
app.include_router(router)
