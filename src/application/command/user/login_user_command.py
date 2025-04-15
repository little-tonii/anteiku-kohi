from fastapi import HTTPException
from starlette import status
from ....application.schema.response.user_response_schema import LoginUserResponse
from ....domain.repository.user_repository import UserRepository
from ....infrastructure.utils.token_util import create_access_token, create_refresh_token

from ....infrastructure.config.cryptography import bcrypt_context

class LoginUserCommand:
    email: str
    password: str

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class LoginUserCommandHandler:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, command: LoginUserCommand) -> LoginUserResponse:
        user_entity = await self.user_repository.get_by_email(email=command.email)
        if not user_entity:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email hoặc mật khẩu không chính xác")
        if not bcrypt_context.verify(command.password, user_entity.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email hoặc mật khẩu không chính xác")
        refresh_token = create_refresh_token(user_id=user_entity.id, role=user_entity.role)
        access_token = create_access_token(user_id=user_entity.id, role=user_entity.role)
        user_entity.refresh_token = refresh_token
        await self.user_repository.update(user_entity=user_entity)
        return LoginUserResponse(
            refresh_token=refresh_token,
            access_token=access_token,
            token_type="bearer"
        )
