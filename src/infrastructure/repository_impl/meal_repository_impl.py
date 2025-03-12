from typing import Optional

from sqlalchemy import select, update

from ...infrastructure.model.meal_model import MealModel
from ...domain.entity.meal_entity import MealEntity
from ...domain.repository.meal_repository import MealRepository
from sqlalchemy.ext.asyncio import AsyncSession

class MealRepositoryImpl(MealRepository):
    async_session: AsyncSession
    
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session
        
    async def get_list(self, page: int, size: int) -> list[MealEntity]:
        async with self.async_session as session:
            query = (
                select(MealModel)
                .where(MealModel.is_available == True)
                .offset((page - 1) * size)
                .limit(size)
            )
            result = await session.execute(query)
            meals = list(result.scalars())
            return [
                MealEntity(
                    id=meal_model.id,
                    name=meal_model.name,
                    description=meal_model.description,
                    created_at=meal_model.created_at,
                    updated_at=meal_model.updated_at,
                    is_avaiable=meal_model.is_available,
                    price=meal_model.price
                )
                for meal_model in meals
            ]
            
    async def get_by_id(self, id: int) -> Optional[MealEntity]:
        async with self.async_session as session:
            query = select(MealModel).where(MealModel.id == id)
            result = await session.execute(query)
            meal_model = result.scalar_one_or_none()
            if not meal_model:
                return None
            return MealEntity(
                id=meal_model.id,
                name=meal_model.name,
                description=meal_model.description,
                created_at=meal_model.created_at,
                updated_at=meal_model.updated_at,
                is_avaiable=meal_model.is_available,
                price=meal_model.price
            )
    
    async def update(self, meal_entity: MealEntity) -> MealEntity:
        async with self.async_session as session:
            async with session.begin():
                query= (
                    update(MealModel)
                    .where(MealModel.id == meal_entity.id)
                    .values(
                        name=meal_entity.name,
                        description=meal_entity.description,
                        price=meal_entity.price
                    )
                    .returning(MealModel)
                )
                result = await session.execute(query)
                meal_model = result.scalar_one()
            return MealEntity(
                id=meal_model.id,
                name=meal_model.name,
                description=meal_model.description,
                created_at=meal_model.created_at,
                updated_at=meal_model.updated_at,
                is_avaiable=meal_model.is_available,
                price=meal_model.price
            )
    
    async def create(self, name: str, description: str, price: int) -> MealEntity:
        meal_model = MealModel(
            name=name,
            description=description,
            price=price
        )
        async with self.async_session as session:
            async with session.begin():
                session.add(meal_model)
                await session.flush()
            await session.refresh(meal_model)
            return MealEntity(
                id=meal_model.id,
                name=meal_model.name,
                description=meal_model.description,
                created_at=meal_model.created_at,
                updated_at=meal_model.updated_at,
                is_avaiable=meal_model.is_available,
                price=meal_model.price
            )
    
    async def deactivate(self, id: int) -> bool:
        async with self.async_session as session:
            async with session.begin():
                query = (
                    update(MealModel)
                    .where(MealModel.id == id)
                    .values(
                        is_available=False
                    )
                    .returning(MealModel)
                )
                result = await session.execute(query)
                deactivated_meal = result.scalar()
                if deactivated_meal:
                    await session.commit()
                    return True
                return False