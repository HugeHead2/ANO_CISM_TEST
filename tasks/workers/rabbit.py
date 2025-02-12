from typing import Callable
import pika
import asyncio
import json


class RabbitMQWorker:
    def __init__(self, queue: str = "default_queue", callback_func: Callable[[dict], str] = None):
        self.host = get_env("RABBIT_HOST")
        self.queue = queue
        self.func = callback_func

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        asyncio.run(self.func(message))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue, durable=True)
        channel.basic_consume(queue=self.queue, on_message_callback=self.callback)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            connection.close()