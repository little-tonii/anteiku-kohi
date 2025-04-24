import io
from pathlib import Path
from PIL import Image, UnidentifiedImageError

def process_and_save_image(image_bytes: bytes, output_path: Path, target_size: int, quality: int) -> None:
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
