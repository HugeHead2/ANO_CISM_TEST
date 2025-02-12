from tasks.models.task import Task
from tasks.repositories.base import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = Task
