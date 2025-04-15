from pathlib import Path
import shutil
import uuid
from fastapi import HTTPException, UploadFile
from starlette import status

from ....infrastructure.config.variables import UPLOAD_FOLDER
from ....application.schema.response.meal_response_schema import UpdateMealImageResponse

from ....domain.repository.meal_repository import MealRepository


class UpdateMealImageCommand:
    id: int
    picture: UploadFile

    def __init__(self, id: int, picture: UploadFile):
        self.id = id
        self.picture = picture

class UpdateMealImageCommandHandler:
    meal_repository: MealRepository

    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository

    async def handle(self, command: UpdateMealImageCommand) -> UpdateMealImageResponse:
        meal_entity = await self.meal_repository.get_by_id(id=command.id)
        if not meal_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Món ăn không tồn tại")
        old_image_url = meal_entity.image_url.lstrip("/")
        file_extension = Path(command.picture.filename or "unknown_file").suffix
        new_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = Path(UPLOAD_FOLDER) / new_filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(command.picture.file, buffer)
        new_image_url = f"/{UPLOAD_FOLDER}/{new_filename}"
        meal_entity.image_url = new_image_url
        updated_meal = await self.meal_repository.update(meal_entity=meal_entity)
        if not updated_meal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Món ăn không tồn tại")
        if old_image_url and Path(old_image_url).exists():
            Path(old_image_url).unlink()
        return UpdateMealImageResponse(
            id=updated_meal.id,
            image_url=updated_meal.image_url,
        )
