from asyncio import sleep
import random
from typing import List

from tasks.constants import RABBIT_QUEUE
from tasks.enums import StatusEnum
from tasks.logger import logger
from tasks.models.task import Task
from tasks.queue.rabbit import RabbitMQClient
from tasks.schemas.tasks import CreateTaskSchema, ReadTaskSchema
from tasks.uow import UnitOfWork


class TasksService():
    async def get_tasks(self, status: StatusEnum = None) -> List[ReadTaskSchema]:
        filter_by = []
        if status is not None:
            filter_by.append(Task.status.contains(status))

        async with UnitOfWork() as uow:
            return await uow.tasks.find_all(*filter_by)

    async def create_task(self, schema: CreateTaskSchema) -> int:
        async with UnitOfWork() as uow:
            new_task_id = await uow.tasks.add_one(
                {
                    "name": schema.name,
                    "status": StatusEnum.new,
                }
            )
            await uow.commit()

        RabbitMQClient(RABBIT_QUEUE).send_message(
            {
                "task_id": new_task_id
            }
        )

        return new_task_id

    async def get_task_info(self, task_id: int) -> ReadTaskSchema:
        async with UnitOfWork() as uow:
            return await uow.tasks.find_one(id=task_id)

    async def handle_task(self, message: dict) -> None:
        async with UnitOfWork() as uow:
            task = await uow.tasks.find_one(id=message["task_id"])

            task.status = StatusEnum.process
            await uow.tasks.edit_one(task.id, task.model_dump())
            await uow.commit()
            logger.info(f"Task {task.id} in progress")

            sleep(30)

            if random.randint(1, 6) == 6:
                task.status = StatusEnum.error
                await uow.tasks.edit_one(task.id, task.model_dump())
                await uow.commit()
                logger.info(f"Task {task.id} error")
                return

            task.status = StatusEnum.done
            await uow.tasks.edit_one(task.id, task.model_dump())
            await uow.commit()
            logger.info(f"Task {task.id} done")

            return task.id
