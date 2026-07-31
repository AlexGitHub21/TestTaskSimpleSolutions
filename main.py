from fastapi import FastAPI
import uvicorn
from app import apps_router

app = FastAPI()

app.include_router(apps_router)

def start():
    uvicorn.run(app="main:app", reload=True)