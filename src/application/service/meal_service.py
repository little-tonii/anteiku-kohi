from ...application.command.meal.create_meal_command import CreateMealCommand, CreateMealCommandHandler
from ...application.schema.response.meal_response_schema import CreateMealResponse
from ...domain.repository.meal_repository import MealRepository


class MealService:
    meal_repository: MealRepository
    
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository
        
    async def create_meal(self, name: str, description: str, price: int) -> CreateMealResponse:
        command = CreateMealCommand(name=name, description=description, price=price)
        command_handler = CreateMealCommandHandler(meal_repository=self.meal_repository)
        return await command_handler.handle(command=command)