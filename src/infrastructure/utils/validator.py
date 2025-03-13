from fastapi import HTTPException
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