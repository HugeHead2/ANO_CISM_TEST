from typing import Any, List
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepository():
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> Any:
        statement = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(statement)
        return res.scalar_one()

    async def edit_one(self, id: Any, data: dict) -> Any:
        statement = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
        res = await self.session.execute(statement)
        return res.scalar_one()

    async def find_all(self, *filter_by) -> List[Any]:
        statement = select(self.model).filter(*filter_by)
        res = await self.session.execute(statement)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def find_one(self, **filter_by) -> Any:
        statement = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(statement)
        res = res.scalar_one().to_read_model()
        return res

    async def delete(self, id: Any) -> None:
        statement = delete(self.model).filter_by(id=id)
        await self.session.execute(statement)

    async def get_total_count(self) -> int:
        statement = select(self.model)
        res = await self.session.execute(statement)
        return len(res.all())
