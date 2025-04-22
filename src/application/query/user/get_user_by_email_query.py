from ....application.schema.response.user_response_schema import GetUserByEmailResponse
from ....domain.repository.user_repository import UserRepository
from fastapi import HTTPException
from starlette import status

class GetUserByEmailQuery:
    email: str

    def __init__(self, email: str):
        self.email = email

class GetUserByEmailQueryHandler:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def handle(self, query: GetUserByEmailQuery) -> GetUserByEmailResponse:
        user_entity = await self.user_repository.get_by_email(email=query.email)
        if not user_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
        if user_entity.is_active == False:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tài khoản đã bị vô hiệu hóa")
        return GetUserByEmailResponse(
            id=user_entity.id,
            full_name=user_entity.full_name,
            phone_number=user_entity.phone_number,
            email=user_entity.email,
            address=user_entity.address,
            updated_at=user_entity.updated_at,
            joined_at=user_entity.joined_at,
            is_active=user_entity.is_active,
            role=user_entity.role,
            is_verified=user_entity.is_verified,
        )
