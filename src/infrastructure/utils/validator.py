import io
import PIL.Image
from fastapi import File, Form, HTTPException, Query, UploadFile
from starlette import status
import email_validator

async def validate_user_id(id: int) -> int:
    if id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID không hợp lệ")
    return id

async def validate_email(email: str) -> str:
    if not email.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email không được để trống")
    try:
        email_infor = email_validator.validate_email(email, check_deliverability=True)
        return email_infor.normalized
    except email_validator.EmailNotValidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email {email} không hợp lệ")
    

async def validate_meal_name(name: str = Form(...)) -> str:
    if not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tên món ăn không được để trống")
    return name.strip()

async def validate_meal_description(description: str = Form(...)) -> str:
    if not description.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mô tả món ăn không được để trống")
    return description.strip()

async def validate_meal_price(price: int = Form(...)) -> int:
    if price <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Giá món ăn phải lớn hơn 0")
    return price

async def validate_picture(picture: UploadFile = File(...)) -> UploadFile:
    try:
        image = PIL.Image.open(io.BytesIO(await picture.read()))
        image.verify()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vui lòng chọn file ảnh")
    picture.file.seek(0, 2)
    file_size = picture.file.tell()
    if file_size > 10 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vui lòng chọn ảnh có kích thước dưới 10 MB")
    picture.file.seek(0)
    return picture

async def validate_is_available_meal(is_available: bool | None = Query(None)) -> bool | None:
    if is_available not in [True, False, None]:  
        raise HTTPException(
            status_code=400,
            detail="Tham số có sẵn phải là true hoặc false (tham số không bắt buộc)"
        )
    return is_available

async def validate_page(page: int = Query(...)) -> int:
    if page < 1:
        raise HTTPException(status_code=400, detail="Số trang phải bắt đầu từ 1")
    return page

async def validate_size(size: int = Query(...)) -> int:
    if size < 1:
        raise HTTPException(status_code=400, detail="Kích thước trang phải lớn hơn hoặc bằng 1")
    return size