import asyncio
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from starlette import status
import uuid
from fastapi import HTTPException, UploadFile
from PIL import UnidentifiedImageError

from ....infrastructure.utils.image_processing import process_and_save_image
from ....infrastructure.config.variables import IMAGE_QUALITY, TARGET_IMAGE_SIZE, UPLOAD_FOLDER
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
    executor: ProcessPoolExecutor

    def __init__(self, meal_repository: MealRepository, executor: ProcessPoolExecutor):
        self.meal_repository = meal_repository
        self.executor = executor

    async def handle(self, command: CreateMealCommand) -> CreateMealResponse:
        new_filename = f"{uuid.uuid4()}.jpg"
        file_path = Path(UPLOAD_FOLDER) / new_filename
        image_url = f"/{UPLOAD_FOLDER}/{new_filename}"
        try:
            image_bytes = await command.picture.read()
            if not image_bytes:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File ảnh rỗng")
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                self.executor,
                process_and_save_image,
                image_bytes, file_path, TARGET_IMAGE_SIZE, IMAGE_QUALITY
            )
        except (UnidentifiedImageError, IOError, Exception) as e:
            if file_path.exists():
                file_path.unlink(missing_ok=True)
            if isinstance(e, UnidentifiedImageError):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"{e}")
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"{e}")
        finally:
            await command.picture.close()
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
