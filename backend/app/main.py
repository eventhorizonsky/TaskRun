import uvicorn
from fastapi import FastAPI
from funboost.faas import CareProjectNameEnv

# (可选) 设置项目名，只管理本项目相关的队列，避免干扰
CareProjectNameEnv.set('my_awesome_project')

from app.routers.auth import router as auth_router
from app.routers.funboost import router as funboost_router

app = FastAPI()

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(funboost_router, prefix="/api")