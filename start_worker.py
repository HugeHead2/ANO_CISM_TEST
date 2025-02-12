from tasks.constants import RABBIT_QUEUE
from tasks.services.tasks import TasksService
from tasks.workers.rabbit import RabbitMQWorker


def start_worker():
    RabbitMQWorker(queue=RABBIT_QUEUE, callback_func=TasksService().handle_task)


if __name__ == "__main__":
    start_worker()