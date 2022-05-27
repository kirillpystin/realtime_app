import logging

from dotenv import load_dotenv

load_dotenv()

from aiohttp.web_app import Application
from aiohttp_middlewares import cors_middleware

from app.workers.generator import generator

from .routers import routers

GIGABYTE = 1024 ** 3
MAX_REQUEST_SIZE = 2 * GIGABYTE

log = logging.getLogger(__name__)


def create_app() -> Application:
    """Создает экземпляр приложения, готового к запуску."""
    app = Application(
        client_max_size=MAX_REQUEST_SIZE,
        middlewares=[
            cors_middleware(allow_all=True, allow_headers=["*"]),
        ],
    )

    for i in routers:
        app.router.add_routes(i)

    app["websockets"] = []

    return app


def tasks_init(loop):
    """Функция, инициализирующая асинхронные задачи"""
    loop.create_task(generator())
