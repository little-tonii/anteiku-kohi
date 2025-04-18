from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio.session import AsyncSession

from ...infrastructure.model.order_meal_model import OrderMealModel

from ...infrastructure.model.order_model import OrderModel, OrderStatus

from ...domain.entity.order_meal_entity import OrderMealEntity
from ...domain.entity.order_entity import OrderEntity
from ...domain.repository.order_repository import OrderRepository


class OrderRepositoryImpl(OrderRepository):
    async_session: AsyncSession

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def create_order(self, meals: List[OrderMealEntity]) -> OrderEntity:
        async with self.async_session as session:
            async with session.begin():
                new_order_model = OrderModel()
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
                )

    async def get_order_meal_list(self, order_id: int) -> List[OrderMealEntity]:
        async with self.async_session as session:
            async with session.begin():
                order_meal_models = await session.execute(
                    select(OrderMealModel).where(OrderMealModel.order_id == order_id)
                )
                return [
                    OrderMealEntity(
                        id=order_meal_model.id, # type: ignore
                        order_id=order_meal_model.order_id, # type: ignore
                        meal_id=order_meal_model.meal_id, # type: ignore
                        price=order_meal_model.price, # type: ignore
                        quantity=order_meal_model.quantity, # type: ignore
                        created_at=order_meal_model.created_at, # type: ignore
                        updated_at=order_meal_model.updated_at, # type: ignore
                    )
                    for order_meal_model in order_meal_models.scalars()
                ]

    async def update_order_status(self, order_id: int, status: str) -> Optional[OrderEntity]:
        async with self.async_session as session:
            async with session.begin():
                stmt = (
                    update(OrderModel)
                    .where(OrderModel.id == order_id)
                    .values(order_status=OrderStatus(status))
                    .returning(OrderModel)
                )
                result = await session.execute(stmt)
                existed_order_model = result.scalar_one_or_none()
                if existed_order_model is None:
                    return None
                order_meals = await session.execute(
                    select(OrderMealModel)
                    .where(OrderMealModel.order_id == order_id)
                )
                meal_ids = [meal.meal_id for meal in order_meals.scalars()]
                return OrderEntity(
                    id=existed_order_model.id, # type: ignore
                    meals=meal_ids, # type: ignore
                    updated_at=existed_order_model.updated_at, # type: ignore
                    created_at=existed_order_model.created_at, # type: ignore
                    order_status=existed_order_model.order_status, # type: ignore
                    payment_status=existed_order_model.payment_status, # type: ignore
                    staff_id=existed_order_model.staff_id, # type: ignore
                )

    async def update_order_staff_id(self, order_id: int, staff_id: int) -> bool:
        async with self.async_session as session:
            async with session.begin():
                stmt = (
                    select(OrderModel)
                    .where(OrderModel.id == order_id)
                    .with_for_update()
                )
                result = await session.execute(stmt)
                order = result.scalar_one_or_none()
                if order is None:
                    return False
                if order.staff_id is not None:
                    return False
                update_stmt = (
                    update(OrderModel)
                    .where(
                        OrderModel.id == order_id,
                        OrderModel.staff_id.is_(None)
                    )
                    .values(staff_id=staff_id)
                    .returning(OrderModel)
                )
                update_result = await session.execute(update_stmt)
                updated_order = update_result.scalar_one_or_none()
                return updated_order is not None

    async def find_order_by_id(self, order_id: int) -> Optional[OrderEntity]:
        async with self.async_session as session:
            stmt = (
                select(OrderModel)
                .where(OrderModel.id == order_id)
            )
            result = await session.execute(stmt)
            order_model = result.scalar_one_or_none()
            if order_model is None:
                return None
            order_meals = await session.execute(
                select(OrderMealModel)
                .where(OrderMealModel.order_id == order_id)
            )
            meal_ids = [meal.meal_id for meal in order_meals.scalars()]
            return OrderEntity(
                id=order_model.id, # type: ignore
                meals=meal_ids, # type: ignore
                updated_at=order_model.updated_at, # type: ignore
                created_at=order_model.created_at, # type: ignore
                order_status=order_model.order_status, # type: ignore
                payment_status=order_model.payment_status, # type: ignore
                staff_id=order_model.staff_id, # type: ignore
            )

    async def update_order_payment_status(self, order_id: int, status: str) -> None:
        async with self.async_session as session:
            async with session.begin():
                stmt = (
                    update(OrderModel)
                    .where(OrderModel.id == order_id)
                    .values(payment_status=status)
                    .returning(OrderModel)
                )
                await session.execute(stmt)
