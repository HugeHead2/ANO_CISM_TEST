from typing import Annotated, List

from fastapi import APIRouter, Depends

from tasks.dependencies.tasks import get_tasks_service
from tasks.enums import StatusEnum
from tasks.schemas.tasks import ReadTaskSchema, CreateTaskSchema
from tasks.services.tasks import TasksService

router = APIRouter(
    prefix="tasks",
    tags=["tasks"]
)


@router.get("/")
async def get_tasks(
    service: Annotated[TasksService, Depends(get_tasks_service)],
    status: StatusEnum = None
) -> List[ReadTaskSchema]:
    return await service.get_tasks(status)

@router.get("/{task_id}")
async def get_task_info(
    task_id: int,
    service: Annotated[TasksService, Depends(get_tasks_service)]
) -> ReadTaskSchema:
    return await service.get_task_info(task_id)

@router.post("/")
async def create_task(
    schema: CreateTaskSchema,
    service: Annotated[TasksService, Depends(get_tasks_service)]
):
    return await service.create_task(schema)
