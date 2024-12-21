import json
import ssl

import websockets

from app.service.auth.auth import create_auth_url
from app.models import llm_model
answer = ""


# 生成请求参数的函数
def gen_params(question: str) -> dict:
    """
    通过appid和用户的提问来生成请求参数
    """
    data = {
        "header": {
            "app_id": llm_model.appid,
            "uid": "1234",
            "patch_id": llm_model.patch_id  # 调用微调大模型时必传, 否则不传。对应resourceId
        },
        "parameter": {
            "chat": {
                "domain": llm_model.serviceId,
                "temperature": 0.5,
                "max_tokens": 2048
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data


# 处理 WebSocket 消息的异步函数
async def on_message(ws, message):
    """
    处理从 WebSocket 服务接收到的消息
    """
    global answer
    data = json.loads(message)
    code = data['header']['code']

    # 如果请求出错，则关闭连接
    if code != 0:
        print(f'请求错误: {code}, {data}')
        await ws.close()
    else:
        # 解析返回数据
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        print(content, end="")
        answer += content

        # 如果 status == 2 说明消息已完全接收，关闭连接
        if status == 2:
            await ws.close()


# WebSocket 客户端的主处理逻辑
async def websocket_client(question: str):
    """
    与 WebSocket 服务建立连接，发送请求并接收响应
    :param question: 用户的查询问题
    :return: WebSocket 服务返回的响应数据
    """
    try:
        # 获取 WebSocket URL
        ws_url = create_auth_url()

        # 建立 WebSocket 连接
        async with websockets.connect(ws_url, ssl=ssl.CERT_NONE) as websocket:
            # 发送请求数据
            data = json.dumps(gen_params(question=question))
            await websocket.send(data)

            # 接收 WebSocket 消息并处理
            await on_message(websocket, await websocket.recv())

        # 返回处理结果
        return answer

    except Exception as e:
        raise Exception(f"WebSocket 请求失败: {str(e)}")
