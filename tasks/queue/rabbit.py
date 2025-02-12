import pika
import json

from tasks.utils import get_env


class RabbitMQClient:
    def __init__(self, queue: str = "default_queue"):
        self.host = get_env("RABBIT_HOST")
        self.queue = queue
        self.credentials = pika.PlainCredentials(get_env("RABBIT_USER"), get_env("RABBIT_PASSWORD"))
        self.connection = None
        self.channel = None

    def connect(self):
        parameters = pika.ConnectionParameters(self.host, get_env("RABBIT_PORT"), "/", self.credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)

    def send_message(self, message: dict):
        if not self.channel:
            self.connect()
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def close(self):
        if self.connection:
            self.connection.close()