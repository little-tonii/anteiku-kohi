from typing import List
from src.domain.repository.order_repository import OrderRepository
from src.domain.repository.meal_repository import MealRepository


class CreateOrderCommand:
    staff_id: int
    meal_ids: List[int]

    def __init__(self, staff_id: int, meal_ids: List[int]):
        self.staff_id = staff_id
        self.meal_ids = meal_ids

class CreateOrderCommandHandler:
    order_repository: OrderRepository
    meal_repository: MealRepository

    def __init__(self, order_repository: OrderRepository, meal_repository: MealRepository):
        self.order_repository = order_repository
        self.meal_repository = meal_repository

    def handle(self, command: CreateOrderCommand):
        pass
