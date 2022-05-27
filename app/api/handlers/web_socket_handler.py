import json

from aiohttp import web

from app.connectors import RabbitConnection
from app.constants import RABBIT_HOST


class WebSocketHandler(object):
    @staticmethod
    def to_json(message):
        body = message.body.decode("utf8").replace("'", '"')
        return json.loads(body)

    @staticmethod
    async def get_ws(request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        return ws

    @classmethod
    async def websocket_handler(cls, request):
        try:
            ws = await cls.get_ws(request)
            request.app["websockets"].append(ws)
        except ConnectionResetError:
            pass

        async with RabbitConnection(RABBIT_HOST) as rabbit:
            async with rabbit.queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        for i in request.app["websockets"]:
                            try:
                                await i.send_json(cls.to_json(message))
                            except ConnectionResetError:
                                continue
                                pass

        return ws
