from pydantic import BaseModel

from tasks.enums import StatusEnum


class ReadTaskSchema(BaseModel):
    id: int
    name: str
    status: StatusEnum


class CreateTaskSchema(BaseModel):
    name: str
