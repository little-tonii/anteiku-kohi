from fastapi import HTTPException
from ....application.schema.response.user_response_schema import GetUserByEmailResponse
from ....domain.repository.user_repository import UserRepository
from starlette import status

from ....infrastructure.repository_impl.user_repository_impl import UserRepositoryImpl

class GetUserByEmailQuery:
    email: str
    
    def __init__(self, email: str):
        self.email = email
        
class GetUserByEmailQueryHandler:
    user_repository: UserRepository
    
    def __init__(self, user_repository: UserRepositoryImpl):
        self.user_repository = user_repository
        
    async def handle(self, query: GetUserByEmailQuery) -> GetUserByEmailResponse:
        user_entity = await self.user_repository.get_by_email(email=query.email)
        if not user_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
        return GetUserByEmailResponse(
            id=user_entity.id,
            full_name=user_entity.full_name,
            phone_number=user_entity.phone_number,
            email=user_entity.email,
            address=user_entity.address,
            updated_at=user_entity.updated_at,
            joined_at=user_entity.joined_at,
            is_active=user_entity.is_active,
            role=user_entity.role
        )