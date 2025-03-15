from abc import ABC, abstractmethod
from typing import Optional

from ...domain.entity.meal_entity import MealEntity


class MealRepository(ABC):
    
    @abstractmethod
    async def get_list(self, page: int, size: int) -> list[MealEntity]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[MealEntity]:
        pass
    
    @abstractmethod
    async def update(self, meal_entity: MealEntity) -> Optional[MealEntity]:
        pass
    
    @abstractmethod
    async def create(self, name: str, description: str, price: int, image_url: str) -> MealEntity:
        pass
    
    @abstractmethod
    async def deactivate(self, id: int) -> bool:
        pass
    
    @abstractmethod
    async def activate(self, id: int) -> bool:
        pass