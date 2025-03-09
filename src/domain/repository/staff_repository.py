from abc import ABC, abstractmethod
from typing import Optional
from domain.entity.staff_entity import StaffEntity


class StaffRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[StaffEntity]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[StaffEntity]:
        pass
    
    @abstractmethod
    async def delete_by_id(self, id: int) -> bool:
        pass
    
    @abstractmethod
    async def delete_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    async def create(self, staff_entity: StaffEntity) -> StaffEntity:
        pass
    
    @abstractmethod
    async def update_by_id(self, staff_entity: StaffEntity) -> StaffEntity:
        pass