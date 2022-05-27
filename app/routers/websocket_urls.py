"""Модуль с маршрутизацией для веб-сокетов."""
from aiohttp import web

from app.api.handlers import WebSocketHandler

ws_router = web.RouteTableDef()


@ws_router.get("/ws/", allow_head=False)
async def get_ws(request):
    return await WebSocketHandler(request).send_messages()
