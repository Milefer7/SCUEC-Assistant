import _thread as thread
import asyncio
import base64
import datetime
import hashlib
import hmac
import json
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import streamlit as st
import websocket

from be.models import llm_model

answer = ""


def create_auth_url() -> str:
    """
    生成 Authorization 字段及请求 URL，用于 API 鉴权
    """
    # 获取当前时间并转换为HTTP格式
    cur_time = datetime.now()
    date = format_date_time(mktime(cur_time.timetuple()))

    # 拼接 HTTP 请求头的各个部分
    tmp = f"host: {llm_model.host}\n"
    tmp += f"date: {date}\n"
    tmp += "GET /v1.1/chat HTTP/1.1"

    # print(tmp)

    """上方拼接生成的tmp字符串如下
    host: spark-api.xf-yun.com
    date: Fri, 05 May 2023 10:43:39 GMT
    GET /v1.1/chat HTTP/1.1
    """

    # 使用 HMAC-SHA256 进行加密
    tmp_sha = hmac.new(llm_model.APISecret.encode('utf-8'), tmp.encode('utf-8'), digestmod=hashlib.sha256).digest()

    # 对加密结果进行 base64 编码
    signature = base64.b64encode(tmp_sha).decode(encoding='utf-8')

    # 拼接 Authorization 头部的字符串
    authorization_origin = f"api_key='{llm_model.APIKey}', algorithm='hmac-sha256', headers='host date request-line', signature='{signature}'"

    # 对 Authorization 字符串进行 base64 编码
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

    # 构建请求 URL
    v = {
        "authorization": authorization,  # 鉴权生成的 authorization
        "date": date,  # 当前时间的 HTTP 格式
        "host": llm_model.host  # 请求的主机名
    }

    # 生成最终的 URL
    url = llm_model.url + '?' + urlencode(v)

    # print(authorization)
    print(url)

    return url


# 生成请求参数的函数
def gen_params(question: str) -> dict:
    """
    通过appid和用户的提问来生成请求参数
    """
    data = {
        "header": {
            "app_id": llm_model.APPID,
            "patch_id": [llm_model.patch_id]  # 调用微调大模型时必传, 否则不传。对应resourceId
        },
        "parameter": {
            "chat": {
                "domain": llm_model.serviceId,
                "temperature": llm_model.temperature,
                "max_tokens": llm_model.max_tokens,
            }
        },
        "payload": {
            "message": {
                "text": [
                    {
                        "role": "system",
                        "content": "你是中南民族大学校园助理"
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }
        }
    }
    print(json.dumps(data, indent=4, ensure_ascii=False))
    return data


# gen_params("你好")


# # 处理 WebSocket 消息的异步函数
# async def on_message(ws, message, websocket):
#     """
#     处理从 WebSocket 服务接收到的消息，并实时发送给客户端
#     """
#     data = json.loads(message)
#     code = data['header']['code']
#
#     # 如果请求出错，则关闭连接
#     if code != 0:
#         print(f'请求错误: {code}, {json.dumps(data, indent=4)}')
#         await ws.close()
#     else:
#         # 解析返回数据
#         choices = data["payload"]["choices"]
#         status = choices["status"]
#         content = choices["text"][0]["content"]
#         print(content, end="")  # 打印内容
#
#         # 实时将内容发送给客户端
#         await websocket.send_text(content)
#
#         # 如果 status == 2 说明消息已完全接收
#         if status == 2:
#             pass  # 继续保持连接，直到需要关闭
#
#
# # WebSocket 客户端的主处理逻辑
# async def websocket_client(query: str, websocket: WebSocket):
#     """
#     与 WebSocket 服务建立连接，发送请求并接收响应，实时传输数据
#     :param query: 用户的查询问题
#     :param websocket: 与前端的 WebSocket 连接
#     """
#     try:
#         # 获取 WebSocket URL
#         ws_url = create_auth_url()
#
#         # 建立 WebSocket 连接
#         async with websockets.connect(ws_url, ssl=True) as websocket_server:
#             # 发送请求数据
#             data = json.dumps(gen_params(query))
#             await websocket_server.send(data)
#
#             # 接收 WebSocket 消息并逐段处理
#             while True:
#                 message = await websocket_server.recv()
#                 await on_message(websocket_server, message, websocket)
#
#     except Exception as e:
#         raise Exception(f"WebSocket 请求失败: {str(e)}")

# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws, one, two):
    print(" ")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(question=ws.question))
    ws.send(data)


def update_chat_history(role, content):
    # 确保会话历史中只有一条来自 "answer" 角色的记录
    if st.session_state.get('messages') is None:
        st.session_state['messages'] = []

    # 查找已有的回答记录，如果没有则创建
    existing_answer = next((msg for msg in st.session_state['messages'] if msg['role'] == 'answer'), None)

    if existing_answer:
        # 如果有现有的回答，拼接内容
        existing_answer['content'] += content
    else:
        # 如果没有现有的回答，添加新的回答
        st.session_state['messages'].append({"role": role, "content": content})


# WebSocket 消息处理
def on_message(ws, message):
    data = json.loads(message)
    code = data['header']['code']

    if code != 0:
        print(f'请求错误: {code}, {data}')
        update_chat_history('answer', f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]

        print(content, end="")  # 打印到控制台，不换行

        # 更新会话历史
        update_chat_history("answer", content)

        # 如果状态为2，表示已完成，关闭 WebSocket
        if status == 2:
            # ws.close()
            pass


def websocket_client(question):
    websocket.enableTrace(False)
    ws_url = create_auth_url()
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.question = question
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
