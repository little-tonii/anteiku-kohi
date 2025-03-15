from ....application.schema.response.meal_response_schema import CreateMealResponse
from ....domain.repository.meal_repository import MealRepository


class CreateMealCommand:
    name: str
    description: str
    price: int
    
    def __init__(self, name: str, description: str, price: int):
        self.name = name
        self.description = description
        self.price = price
        
class CreateMealCommandHandler:
    meal_repository: MealRepository
    
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository
        
    async def handle(self, command: CreateMealCommand) -> CreateMealResponse:
        created_meal = await self.meal_repository.create(
            name=command.name, 
            description=command.description,
            price=command.price
        )
        return CreateMealResponse(
            id=created_meal.id,
            name=created_meal.name,
            description=created_meal.description,
            created_at=created_meal.created_at,
            updated_at=created_meal.updated_at,
            is_available=created_meal.is_available,
            price=created_meal.price
        )