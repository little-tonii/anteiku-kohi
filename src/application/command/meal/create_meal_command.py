from pathlib import Path
import shutil
import uuid
from fastapi import UploadFile

from ....infrastructure.config.variables import UPLOAD_FOLDER
from ....application.schema.response.meal_response_schema import CreateMealResponse
from ....domain.repository.meal_repository import MealRepository


class CreateMealCommand:
    name: str
    description: str
    price: int
    picture: UploadFile

    def __init__(self, name: str, description: str, price: int, picture: UploadFile):
        self.name = name
        self.description = description
        self.price = price
        self.picture = picture

class CreateMealCommandHandler:
    meal_repository: MealRepository

    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository

    async def handle(self, command: CreateMealCommand) -> CreateMealResponse:
        file_extension = Path(command.picture.filename or "unknown_file").suffix
        new_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = Path(UPLOAD_FOLDER) / new_filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(command.picture.file, buffer)
        image_url = f"/{UPLOAD_FOLDER}/{new_filename}"
        created_meal = await self.meal_repository.create(
            name=command.name,
            description=command.description,
            price=command.price,
            image_url=image_url
        )
        return CreateMealResponse(
            id=created_meal.id,
            name=created_meal.name,
            description=created_meal.description,
            created_at=created_meal.created_at,
            updated_at=created_meal.updated_at,
            is_available=created_meal.is_available,
            price=created_meal.price,
            image_url=created_meal.image_url
        )
