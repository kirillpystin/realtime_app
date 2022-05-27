import os

ENV = os.environ

RABBIT_HOST = (
    f"amqp://{ENV['RABBIT_USER']}:{ENV['RABBIT_PASSWORD']}@{ENV['RABBIT_HOST']}/"
)
