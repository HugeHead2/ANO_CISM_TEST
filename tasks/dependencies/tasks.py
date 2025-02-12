from tasks.services.tasks import TasksService


async def get_tasks_service():
    return TasksService()
