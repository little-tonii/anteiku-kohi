from fastapi import HTTPException

from ....domain.repository.user_repository import UserRepository
from ...schema.response.user_response_schema import VerifyAccountResponse
from starlette import status
from itsdangerous import SignatureExpired, BadSignature
from ....infrastructure.config.serializer import serializer
from ....infrastructure.config.variables import EMAIL_SALT_VERIFYCATION

class VerifyAccountCommand:
    token: str

    def __init__(self, token: str):
        self.token = token

class VerifyAccountCommandHandler:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, command: VerifyAccountCommand) -> VerifyAccountResponse:
        try:
            email = serializer.loads(command.token, salt=EMAIL_SALT_VERIFYCATION, max_age=3600)
        except SignatureExpired:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Link xác thực đã hết hạn")
        except BadSignature:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Link xác thực không hợp lệ")
        user_enity = await self.user_repository.get_by_email(email)
        if user_enity is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email chưa đăng ký tài khoản")
        else:
            user_enity.is_verified = True
            updated_user = await self.user_repository.update(user_enity)
            if updated_user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email chưa đăng ký tài khoản")
            return VerifyAccountResponse(
                message="Xác thực tài khoản thành công",
                user_email=updated_user.email,
            )
