from sqlalchemy import Integer, String, Enum, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from tasks.db import Base
from tasks.enums import StatusEnum


class Task(Base):
    __tablename__ = "tasks"

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    status = mapped_column(Enum(StatusEnum))

    def to_read_model(self):
        pass
