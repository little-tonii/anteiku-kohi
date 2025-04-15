from typing import Optional

from fastapi import HTTPException
from starlette import status
from ....application.schema.response.meal_response_schema import UpdateMealDataResponse

from ....domain.repository.meal_repository import MealRepository

class UpdateMealDataCommand:
    id: int
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]

    def __init__(self, id: int, name: Optional[str], description: Optional[str], price: Optional[int]):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

class UpdateMealDataCommandHandler:
    meal_repository: MealRepository

    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository

    async def handle(self, command: UpdateMealDataCommand) -> UpdateMealDataResponse:
        meal_entity = await self.meal_repository.get_by_id(id=command.id)
        updated_field = 0
        if not meal_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Món ăn không tồn tại")
        if command.description:
            updated_field += 1
            meal_entity.description = command.description
        if command.name:
            updated_field += 1
            meal_entity.name = command.name
        if command.price:
            updated_field += 1
            meal_entity.price = command.price
        if updated_field == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vui lòng nhập trường thông tin muốn cập nhật")
        updated_meal = await self.meal_repository.update(meal_entity=meal_entity)
        if not updated_meal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Món ăn không tồn tại")
        return UpdateMealDataResponse(
            id=updated_meal.id,
            name=updated_meal.name,
            description=updated_meal.description,
            created_at=updated_meal.created_at,
            updated_at=updated_meal.updated_at,
            is_available=updated_meal.is_available,
            price=updated_meal.price
        )
