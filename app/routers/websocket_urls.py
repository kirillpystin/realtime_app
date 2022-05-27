"""Модуль с маршрутизацией для веб-сокетов."""
from aiohttp import web
from aiohttp.web import Response

from app.api.handlers import WebSocketHandler

ws_router = web.RouteTableDef()


@ws_router.get("/ws/", allow_head=False)
async def get_ws(request):
    """Извлечение положения объекта.
    Args:
        request(Request): Словарь с параметрами.
    Returns:
        Response: Ответ с статусом.
    """

    return await WebSocketHandler.websocket_handler(request)
