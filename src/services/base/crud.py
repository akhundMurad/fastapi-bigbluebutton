from typing import Protocol, List, Any
from uuid import UUID

from pydantic import BaseModel


class CRUD(Protocol):
    def __init__(self, session):
        self.session = session

    async def create(self, item: BaseModel) -> Any:
        ...

    async def read(self, item_id: UUID) -> Any:
        ...

    async def update(self, item: BaseModel) -> Any:
        ...

    async def delete(self, item_id: UUID) -> None:
        ...
