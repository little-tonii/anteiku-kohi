from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...infrastructure.model.meal_model import MealModel
from ...domain.entity.meal_entity import MealEntity
from ...domain.repository.meal_repository import MealRepository

class MealRepositoryImpl(MealRepository):
    async_session: AsyncSession

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def get_list(self, page: int, size: int, is_available: bool | None) -> list[MealEntity]:
        async with self.async_session as session:
            query = select(MealModel)
            if is_available is not None:
                query = query.where(MealModel.is_available == is_available)
            query = query.offset((page - 1) * size).limit(size)
            result = await session.execute(query)
            meals = list(result.scalars())
            return [
                MealEntity(
                    id=meal_model.id, # type: ignore
                    name=meal_model.name, # type: ignore
                    description=meal_model.description, # type: ignore
                    created_at=meal_model.created_at, # type: ignore
                    updated_at=meal_model.updated_at, # type: ignore
                    is_available=meal_model.is_available, # type: ignore
                    price=meal_model.price, # type: ignore
                    image_url=meal_model.image_url # type: ignore
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
                id=meal_model.id, # type: ignore
                name=meal_model.name, # type: ignore
                description=meal_model.description, # type: ignore
                created_at=meal_model.created_at, # type: ignore
                updated_at=meal_model.updated_at, # type: ignore
                is_available=meal_model.is_available, # type: ignore
                price=meal_model.price, # type: ignore
                image_url=meal_model.image_url # type: ignore
            )

    async def update(self, meal_entity: MealEntity) -> Optional[MealEntity]:
        async with self.async_session as session:
            async with session.begin():
                query=(
                    select(MealModel)
                    .where(MealModel.id == meal_entity.id)
                    .with_for_update()
                )
                result = await session.execute(query)
                meal_model = result.scalar_one_or_none()
                if not meal_model:
                    return None
                meal_model.name = meal_entity.name # type: ignore
                meal_model.description = meal_entity.description # type: ignore
                meal_model.price = meal_entity.price # type: ignore
                meal_model.image_url = meal_entity.image_url # type: ignore
                await session.refresh(meal_model)
                return MealEntity(
                    id=meal_model.id, # type: ignore
                    name=meal_model.name, # type: ignore
                    description=meal_model.description, # type: ignore
                    created_at=meal_model.created_at, # type: ignore
                    updated_at=meal_model.updated_at, # type: ignore
                    is_available=meal_model.is_available, # type: ignore
                    price=meal_model.price, # type: ignore
                    image_url=meal_model.image_url # type: ignore
                )

    async def create(self, name: str, description: str, price: int, image_url: str) -> MealEntity:
        meal_model = MealModel(
            name=name,
            description=description,
            price=price,
            image_url=image_url
        )
        async with self.async_session as session:
            async with session.begin():
                session.add(meal_model)
                await session.flush()
                await session.refresh(meal_model)
                return MealEntity(
                    id=meal_model.id, # type: ignore
                    name=meal_model.name, # type: ignore
                    description=meal_model.description, # type: ignore
                    created_at=meal_model.created_at, # type: ignore
                    updated_at=meal_model.updated_at, # type: ignore
                    is_available=meal_model.is_available, # type: ignore
                    price=meal_model.price, # type: ignore
                    image_url=meal_model.image_url # type: ignore
                )

    async def deactivate(self, id: int) -> bool:
        async with self.async_session as session:
            async with session.begin():
                query=(
                    select(MealModel)
                    .where(MealModel.id == id, MealModel.is_available == True)
                    .with_for_update()
                )
                result = await session.execute(query)
                meal_model = result.scalar()
                if not meal_model:
                    return False
                meal_model.is_available = False # type: ignore
                await session.refresh(meal_model)
                return meal_model.is_available == False # type: ignore

    async def activate(self, id: int) -> bool:
        async with self.async_session as session:
            async with session.begin():
                query=(
                    select(MealModel)
                    .where(MealModel.id == id, MealModel.is_available == False)
                    .with_for_update()
                )
                result = await session.execute(query)
                meal_model = result.scalar()
                if not meal_model:
                    return False
                meal_model.is_available = True # type: ignore
                await session.refresh(meal_model)
                return meal_model.is_available == True # type: ignore
