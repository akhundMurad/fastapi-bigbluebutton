from typing import Protocol
from uuid import UUID

from pydantic import BaseModel

from src.services.base.result import ServiceResult


class Service(Protocol):
    async def create(self, item: BaseModel) -> ServiceResult:
        ...

    async def read(self, item_id: UUID) -> ServiceResult:
        ...

    async def update(self, item: BaseModel) -> ServiceResult:
        ...

    async def delete(self, item_id: UUID) -> ServiceResult:
        ...
