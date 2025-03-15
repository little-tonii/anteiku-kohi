from fastapi import HTTPException
from ....application.schema.response.meal_response_schema import DisableMealResponse
from ....domain.repository.meal_repository import MealRepository
from starlette import status

class DisableMealCommand:
    id: int
    
    def __init__(self, id: int):
        self.id = id
        
class DisableMealCommandHandler:
    meal_repository: MealRepository
    
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository
        
    async def handle(self, command: DisableMealCommand) -> DisableMealResponse:
        meal_entity = await self.meal_repository.get_by_id(id=command.id)
        if not meal_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Món ăn không tồn tại")
        success = await self.meal_repository.deactivate(id=command.id)
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Món ăn đã bị ẩn")
        return DisableMealResponse(message="Ẩn món ăn thành công")