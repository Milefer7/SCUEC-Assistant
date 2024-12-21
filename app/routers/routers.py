from fastapi import APIRouter

from app.controller.query import api_chat

router = APIRouter()

router.add_api_route("/api/chat", api_chat, methods=["POST"])
