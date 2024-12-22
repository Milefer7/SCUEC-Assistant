import json
import websockets
from fastapi import WebSocket, WebSocketDisconnect

from be.service.websocket.websocket_client import websocket_client

async def websocket_communicate(query):
    try:
        websocket_client(query)
    except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.InvalidURI) as e:
        return f"Connection failed: {e}"