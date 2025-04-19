from typing import Dict
from fastapi import HTTPException
from ....application.schema.response.order_response_schema import OrderMealResponse, UpdateOrderStatusResponse
from ....domain.entity.meal_entity import MealEntity
from ....domain.repository.meal_repository import MealRepository
from ....domain.repository.order_repository import OrderRepository
from starlette import status

class UpdateOrderStatusCommand:
    staff_id: int
    order_id: int
    status: str

    def __init__(self, staff_id: int, order_id: int, status: str):
        self.staff_id = staff_id
        self.order_id = order_id
        self.status = status

class UpdateOrderStatusCommandHandler:
    order_repository: OrderRepository
    meal_repository: MealRepository

    def __init__(self, order_repository: OrderRepository, meal_repository: MealRepository):
        self.order_repository = order_repository
        self.meal_repository = meal_repository

    async def handle(self, command: UpdateOrderStatusCommand) -> UpdateOrderStatusResponse:
        existed_order = await self.order_repository.find_order_by_id(order_id=command.order_id)
        if not existed_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Đơn hàng không tồn tại")
        if existed_order.staff_id != command.staff_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không phải là nhân viên chịu trách nhiệm đơn hàng này")
        updated_order = await self.order_repository.update_order_status(order_id=command.order_id, status=command.status)
        if not updated_order:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cập nhật trạng thái đơn hàng thất bại")
        order_meal_list = await self.order_repository.get_order_meal_list(order_id=updated_order.id)
        meal_lookup: Dict[int, MealEntity] = {}
        for order_meal in order_meal_list:
            meal = await self.meal_repository.get_by_id(id=order_meal.meal_id)
            if meal:
                meal_lookup[order_meal.meal_id] = meal
        return UpdateOrderStatusResponse(
            id=updated_order.id,
            updated_at=updated_order.updated_at,
            created_at=updated_order.created_at,
            order_status=updated_order.order_status,
            payment_status=updated_order.payment_status,
            meals=[
                OrderMealResponse(
                    id=order_meal.id,
                    price=order_meal.price,
                    quantity=order_meal.quantity,
                    name=meal_lookup[order_meal.meal_id].name,
                    description=meal_lookup[order_meal.meal_id].description,
                    image_url=meal_lookup[order_meal.meal_id].image_url,
                )
                for order_meal in order_meal_list
            ],
            staff_id=updated_order.staff_id,
        )
