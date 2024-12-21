from fastapi import HTTPException

from app.models.vo.request import QueryPayload
from app.service.websocket.websocket_client import websocket_client


async def api_chat(payload: QueryPayload):
    """
    调用外部 API，进行查询处理并返回结果
    :param payload: 用户输入的查询
    :return: 外部 API 返回的结果
    """
    try:
        # 通过 service 层处理 WebSocket 请求和消息
        response_data = await websocket_client(payload.query)
        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
