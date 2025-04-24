import asyncio
from concurrent.futures import ThreadPoolExecutor
import io
from pathlib import Path
import uuid
from fastapi import HTTPException, UploadFile
from starlette import status
from PIL import Image, UnidentifiedImageError

from ....infrastructure.config.variables import IMAGE_QUALITY, TARGET_IMAGE_SIZE, UPLOAD_FOLDER
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
    executor: ThreadPoolExecutor

    def __init__(self, meal_repository: MealRepository, executor: ThreadPoolExecutor):
        self.meal_repository = meal_repository
        self.executor = executor

    def _process_image(self, image_bytes: bytes, output_path: Path, target_size: int, quality: int) -> None:
        try:
            with Image.open(io.BytesIO(image_bytes)) as image:
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
                width, height = image.size
                short_side = min(width, height)
                left = (width - short_side) / 2
                top = (height - short_side) / 2
                right = (width + short_side) / 2
                bottom = (height + short_side) / 2
                img_cropped = image.crop((left, top, right, bottom))
                if img_cropped.width > target_size:
                    img_resized = img_cropped.resize((target_size, target_size), Image.Resampling.LANCZOS)
                else:
                    img_resized = img_cropped
                img_resized.save(
                    output_path,
                    format="JPEG",
                    quality=quality,
                    optimize=True,
                    progressive=True,
                )
        except UnidentifiedImageError:
            raise UnidentifiedImageError("Vui lòng chọn file ảnh")
        except IOError:
            raise IOError("Có lỗi khi lưu ảnh đã qua xử lý")
        except Exception:
            raise Exception("Đã xảy ra lỗi trong quá trình xử lý ảnh")

    async def handle(self, command: UpdateMealImageCommand) -> UpdateMealImageResponse:
        meal_entity = await self.meal_repository.get_by_id(id=command.id)
        if not meal_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Món ăn không tồn tại")
        old_image_url = meal_entity.image_url.lstrip("/")
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
                self._process_image,
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
