import json

from aiohttp import web

from app.connectors import RabbitConnection
from app.constants import RABBIT_HOST


class WebSocketHandler(object):

    def __init__(self, request):
        self.request = request

    @staticmethod
    def to_json(message):
        body = message.body.decode("utf8").replace("'", '"')
        return json.loads(body)

    async def get_ws(self):
        try:
            ws = web.WebSocketResponse()
            await ws.prepare(self.request)
        except ConnectionResetError:
            pass

        return ws

    async def send_messages(self):
        """Отправлка сообщений через веб-сокеты"""

        self.request.app["websockets"].append(await self.get_ws())

        async with RabbitConnection(RABBIT_HOST) as rabbit:
            async with rabbit.queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        for i in self.request.app["websockets"]:
                            try:
                                await i.send_json(self.to_json(message))
                            except ConnectionResetError:
                                continue
