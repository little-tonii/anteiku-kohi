from abc import ABC, abstractmethod
from typing import List

from ...domain.entity.order_meal_entity import OrderMealEntity

from ...domain.entity.order_entity import OrderEntity


class OrderRepository(ABC):

    @abstractmethod
    async def create_order(self, staff_id: int, meals: List[OrderMealEntity]) -> OrderEntity:
       pass
