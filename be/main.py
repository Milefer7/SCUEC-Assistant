# be/main.py
from fastapi import FastAPI

from be.controller.query import api_chat

# 初始化 FastAPI 应用
app = FastAPI()
# print("FastAPI 应用初始化完成")
app.add_websocket_route("/api/chat", api_chat)
# print("WebSocket 路由添加完成")
