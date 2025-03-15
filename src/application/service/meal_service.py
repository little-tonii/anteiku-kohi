from ...application.command.meal.enable_meal_command import EnableMealCommand, EnableMealCommandHandler
from ...application.command.meal.disable_meal_command import DisableMealCommand, DisableMealCommandHandler
from ...application.command.meal.create_meal_command import CreateMealCommand, CreateMealCommandHandler
from ...application.schema.response.meal_response_schema import CreateMealResponse, DisableMealResponse, EnableMealResponse
from ...domain.repository.meal_repository import MealRepository


class MealService:
    meal_repository: MealRepository
    
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository
        
    async def enable_meal(self, id: int) -> EnableMealResponse:
        command = EnableMealCommand(id=id)
        command_handler = EnableMealCommandHandler(meal_repository=self.meal_repository)
        return await command_handler.handle(command=command)
        
    async def disable_meal(self, id: int) -> DisableMealResponse:
        command = DisableMealCommand(id=id)
        command_handler = DisableMealCommandHandler(meal_repository=self.meal_repository)
        return await command_handler.handle(command=command)
        
    async def create_meal(self, name: str, description: str, price: int) -> CreateMealResponse:
        command = CreateMealCommand(name=name, description=description, price=price)
        command_handler = CreateMealCommandHandler(meal_repository=self.meal_repository)
        return await command_handler.handle(command=command)