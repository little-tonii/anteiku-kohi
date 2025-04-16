from typing import List
from sqlalchemy.ext.asyncio.session import AsyncSession

from ...infrastructure.model.order_meal_model import OrderMealModel

from ...infrastructure.model.order_model import OrderModel

from ...domain.entity.order_meal_entity import OrderMealEntity
from ...domain.entity.order_entity import OrderEntity
from ...domain.repository.order_repository import OrderRepository


class OrderRepositoryImpl(OrderRepository):
    async_session: AsyncSession

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def create_order(self, staff_id: int, meals: List[OrderMealEntity]) -> OrderEntity:
        async with self.async_session as session:
            async with session.begin():
                new_order_model = OrderModel(staff_id=staff_id)
                session.add(new_order_model)
                await session.flush()
                await session.refresh(new_order_model)
                new_order_meal_models = []
                for meal in meals:
                    new_order_meal_model = OrderMealModel(
                        order_id=new_order_model.id,
                        meal_id=meal.meal_id,
                        price=meal.price,
                        quantity=meal.quantity,
                    )
                    session.add(new_order_meal_model)
                    new_order_meal_models.append(new_order_meal_model)
                await session.flush()
                for new_order_meal_model in new_order_meal_models:
                    await session.refresh(new_order_meal_model)
                return OrderEntity(
                    id=new_order_model.id, # type: ignore
                    meals=[
                        new_order_model.id
                        for new_order_meal_model in new_order_meal_models
                    ], # type: ignore
                    order_status=new_order_model.order_status, # type: ignore
                    created_at=new_order_model.created_at, # type: ignore
                    updated_at=new_order_model.updated_at, # type: ignore
                    payment_status=new_order_model.payment_status, # type: ignore
                    staff_id=new_order_model.staff_id, # type: ignore
                )
