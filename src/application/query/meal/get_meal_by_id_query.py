from fastapi import HTTPException
from ....application.schema.response.meal_response_schema import GetMealResponse
from ....domain.repository.meal_repository import MealRepository
from starlette import status

class GetMealByIdQuery:
    id: int
    
    def __init__(self, id: str):
        self.id = id
        
class GetMealByIdQueryHandler:
    meal_repository: MealRepository
    
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository
        
    async def handle(self, query: GetMealByIdQuery) -> GetMealResponse:
        meal_entity = await self.meal_repository.get_by_id(id=query.id)
        if not meal_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Món ăn không tồn tại") 
        return GetMealResponse(
            id=meal_entity.id,
            name=meal_entity.name,
            description=meal_entity.description,
            created_at=meal_entity.created_at,
            updated_at=meal_entity.updated_at,
            is_available=meal_entity.is_available,
            price=meal_entity.price,
            image_url=meal_entity.image_url
        )