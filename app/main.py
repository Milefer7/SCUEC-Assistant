# app/main.py

from fastapi import FastAPI

from app.routers.routers import router

# 初始化 FastAPI 应用
app = FastAPI()

# 包含查询 API 路由
app.include_router(router)
