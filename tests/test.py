import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from main import app
from tasks.enums import StatusEnum
from tasks.services.tasks import TasksService
from tasks.uow import UnitOfWork

client = TestClient(app)


@pytest_asyncio.fixture
async def test_task():
    with UnitOfWork() as uow:
        id = await uow.tasks.add_one(
            {
                "name":"test",
                "status": StatusEnum.new
            }
        )
        await uow.commit()
        task = await uow.tasks.find_one(id=id)

    yield task

    with UnitOfWork() as uow:
        await uow.tasks.delete(task.id)


@pytest.mark.asyncio
async def get_tasks(test_task):
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def get_task(test_task):
    response = client.get(f"/{test_task.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_task


@pytest.mark.asyncio
async def create_task():
    response = client.get(f"/{test_task.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def handle_task(test_task):
    await TasksService().handle_task({"task_id": test_task.id})

    with UnitOfWork() as uow:
        task_db = await uow.tasks.find_one(id=test_task.id)
        assert task_db.status == StatusEnum.done || task_db.status == StatusEnum.error
