from ....application.schema.response.meal_response_schema import GetMealResponse, GetMealsResponse
from ....domain.repository.meal_repository import MealRepository


class GetMealsQuery:
    page: int
    size: int
    is_available: bool | None
    
    def __init__(self, page: int, size: int, is_available: bool | None):
        self.page = page
        self.size = size
        self.is_available = is_available
        
class GetMealsQueryHandler:
    meal_repository: MealRepository
    
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository
        
    async def handle(self, query: GetMealsQuery) -> GetMealsResponse:
        meal_entities = await self.meal_repository.get_list(page=query.page, size=query.size, is_available=query.is_available)
        return GetMealsResponse(
            meals=[
                GetMealResponse(
                    id=meal_entity.id,
                    name=meal_entity.name,
                    description=meal_entity.description,
                    created_at=meal_entity.created_at,
                    updated_at=meal_entity.updated_at,
                    is_available=meal_entity.is_available,
                    price=meal_entity.price,
                    image_url=meal_entity.image_url
                )
                for meal_entity in meal_entities
            ],
            page=query.page,
            size=query.size,
        )