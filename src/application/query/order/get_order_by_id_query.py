from fastapi import HTTPException
from starlette import status

from ....domain.entity.meal_entity import MealEntity
from ....application.schema.response.order_response_schema import GetOrderByIdResponse, OrderMealResponse
from ....domain.repository.order_repository import OrderRepository
from ....domain.repository.meal_repository import MealRepository

class GetOrderByIdQuery:
    order_id: int

    def __init__(self, order_id: int):
        self.order_id = order_id


class GetOrderByIdQueryHandler:
    order_repository: OrderRepository
    meal_repository: MealRepository

    def __init__(self, order_repository: OrderRepository, meal_repository: MealRepository):
        self.order_repository = order_repository
        self.meal_repository = meal_repository

    async def handle(self, query: GetOrderByIdQuery) -> GetOrderByIdResponse:
        order = await self.order_repository.find_order_by_id(order_id=query.order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Đơn hàng không tồn tại")
        order_meals = await self.order_repository.get_order_meal_list(order_id=query.order_id)
        meal_lookup: dict[int, MealEntity] = {}
        for meal in order_meals:
            meal_result = await self.meal_repository.get_by_id(id=meal.meal_id)
            if meal_result:
                meal_lookup[meal.meal_id] = meal_result
        return GetOrderByIdResponse(
            id=order.id,
            updated_at=order.updated_at,
            created_at=order.created_at,
            order_status=order.order_status,
            payment_status=order.payment_status,
            meals=[
                OrderMealResponse(
                    id=order_meal.id,
                    price=order_meal.price,
                    quantity=order_meal.quantity,
                    name=meal_lookup[order_meal.meal_id].name,
                    description=meal_lookup[order_meal.meal_id].description,
                    image_url=meal_lookup[order_meal.meal_id].image_url,
                )
                for order_meal in order_meals
            ],
            staff_id=order.staff_id
        )
