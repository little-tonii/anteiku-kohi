from fastapi import Depends, HTTPException
from application.schema.response.user_response_schema import GetUserByIdResponse
from domain.entity.user_entity import UserEntity
from domain.repository.user_repository import UserRepository
from starlette import status

from infrastructure.repository_impl.user_repository_impl import UserRepositoryImpl

class GetUserByIdQuery:
    id: int
    
    def __init__(self, id: str):
        self.id = id
        
class GetUserByIdQueryHandler:
    user_repository: UserRepository
    
    def __init__(self, user_repository: UserRepositoryImpl = Depends()):
        self.user_repository = user_repository
        
    async def handle(self, query: GetUserByIdQuery) -> GetUserByIdResponse:
        user_entity = await self.user_repository.get_by_id(id=query.id)
        if not user_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
        return GetUserByIdResponse(
            id=user_entity.id,
            full_name=user_entity.full_name,
            phone_number=user_entity.phone_number,
            email=user_entity.email,
            address=user_entity.address,
            updated_at=user_entity.updated_at,
            joined_at=user_entity.joined_at,
            is_active=user_entity.is_active
        )