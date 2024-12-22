import json
import websockets
from fastapi import WebSocket, WebSocketDisconnect

from be.service.websocket.websocket_client import websocket_client


# async def api_chat(websocket: WebSocket):
#     print("WebSocket 连接中")  # 打印连接中日志
#     await websocket.accept()
#     print("WebSocket 已建立连接")  # 打印连接建立日志
#     try:
#         while True:
#             query = await websocket.receive_text()  # 接收前端发送的查询
#             print(f"接收 query: {query}")  # 打印接收到的查询
#
#             # 在此处调用某些业务逻辑来处理查询并返回响应
#             # await websocket_client(query, websocket)  # 与远程 API 连接并流式接收数据，再逐步发送给前端
#             response = await websocket_client(query)  # 调用远程 API 并获取响应
#             print(f"远程response")  # 打印响应
#             print(json.dumps(response, indent=4))
#
#             # 将响应发送回客户端
#             # await websocket.send_text(response)
#     except WebSocketDisconnect:
#         print("Client disconnected")


async def websocket_communicate(query):
    try:
        websocket_client(query)
    except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.InvalidURI) as e:
        return f"Connection failed: {e}"