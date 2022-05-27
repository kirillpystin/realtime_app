import aio_pika


class RabbitConnection(object):
    """Контекстный менеджер, который обрабатывает соединения к RabbitMQ"""

    def __init__(self, host, queue_name="my_queue"):
        self.host = host
        self.queue_name = queue_name

    async def __aenter__(self):
        self.connection = await aio_pika.connect_robust(self.host)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(self.queue_name)
        return self

    async def send_message(self, message):
        exchange = self.channel.default_exchange
        await exchange.publish(
            aio_pika.Message(body="{}".format(message).encode()),
            routing_key=self.queue_name,
        )

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.close()
