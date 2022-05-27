import argparse
import asyncio
import pwd

from aiohttp.web import run_app
from aiomisc import bind_socket
from aiomisc.log import LogFormat, basic_config
from configargparse import ArgumentParser

from . import create_app, tasks_init

ENV_VAR_PREFIX = "KOTIRAPP"


parser = ArgumentParser(
    auto_env_var_prefix=ENV_VAR_PREFIX,
    allow_abbrev=False,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--user", required=False, type=pwd.getpwnam, help="Change process UID"
)

group = parser.add_argument_group("API Options")
group.add_argument(
    "--api-address",
    default="0.0.0.0",
    help="IPv4/IPv6 address API server would listen on",
)
group.add_argument(
    "--api-port",
    default=8082,
    help="TCP port API server would listen on",
)

group = parser.add_argument_group("Logging options")
group.add_argument(
    "--log-level",
    default="info",
    choices=("debug", "info", "warning", "error", "fatal"),
)
group.add_argument("--log-format", choices=LogFormat.choices(), default="color")


def run():
    loop = asyncio.get_event_loop()

    args = parser.parse_args()
    # Конфигурируем логгер
    basic_config(args.log_level, args.log_format, buffered=True)
    sock = bind_socket(address=args.api_address, port=args.api_port, proto_name="http")
    app = create_app()

    tasks_init(loop)
    run_app(app, sock=sock, loop=loop)


if __name__ == "__main__":
    run()
