import asyncio
import logging
from random import random

from app.connectors import RabbitConnection
from app.constants import RABBIT_HOST

logging.basicConfig(level=logging.INFO)


def generate_movement():
    return -1 if random() < 0.5 else 1


async def generator():
    """Генератор стоимости."""
    res_dict = {}
    items = [f"tool_{i}" for i in range(100)]

    async with RabbitConnection(RABBIT_HOST) as rabbit:
        while True:
            for i in items:
                res_dict[i] = max(0, res_dict.get(i, 0) + generate_movement())

            await rabbit.send_message(res_dict)
            await asyncio.sleep(1)


def run():
    logging.info("generator run!")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generator())


if __name__ == "__main__":
    run()
