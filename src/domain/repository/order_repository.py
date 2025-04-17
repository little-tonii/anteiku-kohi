from abc import ABC, abstractmethod
from typing import List
from typing_extensions import Optional

from ...domain.entity.order_meal_entity import OrderMealEntity

from ...domain.entity.order_entity import OrderEntity


class OrderRepository(ABC):

    @abstractmethod
    async def create_order(self, meals: List[OrderMealEntity]) -> OrderEntity:
       pass

    @abstractmethod
    async def get_order_meal_list(self, order_id: int) -> List[OrderMealEntity]:
        pass

    @abstractmethod
    async def update_order_status(self, order_id: int, status: str) -> Optional[OrderEntity]:
        pass

    @abstractmethod
    async def update_order_staff_id(self, order_id: int, staff_id: int) -> bool:
        pass

    @abstractmethod
    async def find_order_by_id(self, order_id: int) -> Optional[OrderEntity]:
        pass
