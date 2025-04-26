from datetime import datetime, timedelta
from fastapi import HTTPException
from starlette import status

from ....infrastructure.config.cryptography import bcrypt_context
from ...schema.response.user_response_schema import ResetPasswordResponse
from ....domain.repository.reset_password_code_repository import ResetPasswordCodeRepository
from ....domain.repository.user_repository import UserRepository

class ResetPasswordCommand:
    email: str
    code: str
    new_password: str

    def __init__(self, email: str, code: str, new_password: str):
        self.email = email
        self.code = code
        self.new_password = new_password

class ResetPasswordCommandHandler:
    user_repository: UserRepository
    reset_password_code_repository: ResetPasswordCodeRepository

    def __init__(
        self,
        user_repository: UserRepository,
        reset_password_code_repository: ResetPasswordCodeRepository,
    ):
        self.user_repository = user_repository
        self.reset_password_code_repository = reset_password_code_repository

    async def handle(self, command: ResetPasswordCommand) -> ResetPasswordResponse:
        user_entity = await self.user_repository.get_by_email(email=command.email)
        if user_entity is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tài khoản không tồn tại")
        reset_password_code_entity = await self.reset_password_code_repository.find_by_code_and_user_id(
            code=command.code,
            user_id=user_entity.id
        )
        if reset_password_code_entity is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mã khôi phục không hợp lệ")
        if reset_password_code_entity.created_at + timedelta(minutes=5) < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mã khôi phục đã hết hạn")
        delete_code_result = await self.reset_password_code_repository.delete_by_user_id(user_id=user_entity.id)
        if delete_code_result == False:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra khi hủy mã khôi phục")
        user_entity.hashed_password = bcrypt_context.hash(command.new_password)
        updated_user = await self.user_repository.update(user_entity=user_entity)
        if updated_user is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Có lỗi xảy ra khi cập nhật mật khẩu mới")
        return ResetPasswordResponse(message="Cập nhật mật khẩu thành công")
