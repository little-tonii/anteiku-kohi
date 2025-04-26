import random
from fastapi import HTTPException
from starlette import status

from ....domain.repository.reset_password_code_repository import ResetPasswordCodeRepository
from ....application.schema.response.user_response_schema import ForgotPasswordResponse
from ....domain.repository.user_repository import UserRepository
import string

class CreateResetPasswordCodeCommand:
    email: str

    def __init__(self, email: str):
        self.email = email

class CreateResetPasswordCodeCommandHandler:
    user_repository: UserRepository
    reset_password_code_repository: ResetPasswordCodeRepository

    def __init__(self, user_repository: UserRepository, reset_password_code_repository: ResetPasswordCodeRepository):
        self.user_repository = user_repository
        self.reset_password_code_repository = reset_password_code_repository

    async def handle(self, command: CreateResetPasswordCodeCommand) -> ForgotPasswordResponse:
        user_entity = await self.user_repository.get_by_email(email=command.email)
        if not user_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tài khoản không tồn tại")
        random_code = ''.join(random.choices(string.digits, k=6))
        reset_password_code = await self.reset_password_code_repository.create(user_id=user_entity.id, code=random_code)
        return ForgotPasswordResponse(
            code=reset_password_code.code,
            message="Vui lòng kiểm tra email để lấy mã xác nhận",
            user_id=user_entity.id,
            user_email=user_entity.email
        )
