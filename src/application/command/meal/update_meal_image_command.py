import asyncio
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import uuid
from fastapi import HTTPException, UploadFile
from starlette import status
from PIL import UnidentifiedImageError

from ....infrastructure.config.variables import IMAGE_QUALITY, TARGET_IMAGE_SIZE, UPLOAD_FOLDER
from ....application.schema.response.meal_response_schema import UpdateMealImageResponse
from ....domain.repository.meal_repository import MealRepository
from ....infrastructure.utils.image_processing import process_and_save_image

class UpdateMealImageCommand:
    id: int
    picture: UploadFile

    def __init__(self, id: int, picture: UploadFile):
        self.id = id
        self.picture = picture

class UpdateMealImageCommandHandler:
    meal_repository: MealRepository
    executor: ProcessPoolExecutor

    def __init__(self, meal_repository: MealRepository, executor: ProcessPoolExecutor):
        self.meal_repository = meal_repository
        self.executor = executor

    async def handle(self, command: UpdateMealImageCommand) -> UpdateMealImageResponse:
        meal_entity = await self.meal_repository.get_by_id(id=command.id)
        if not meal_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Món ăn không tồn tại")
        new_filename = f"{uuid.uuid4()}.jpg"
        file_path = Path(UPLOAD_FOLDER) / new_filename
        new_image_url = f"/{UPLOAD_FOLDER}/{new_filename}"
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
        old_image_url = meal_entity.image_url.lstrip("/")
        meal_entity.image_url = new_image_url
        updated_meal = await self.meal_repository.update(meal_entity=meal_entity)
        if not updated_meal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Món ăn không tồn tại")
        if old_image_url and Path(old_image_url).exists():
            Path(old_image_url).unlink(missing_ok=True)
        return UpdateMealImageResponse(
            id=updated_meal.id,
            image_url=updated_meal.image_url,
        )
