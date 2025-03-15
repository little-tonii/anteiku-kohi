from fastapi import HTTPException
from ....application.schema.response.user_response_schema import GetUserInfoResponse
from ....domain.repository.user_repository import UserRepository
from starlette import status

class GetUserInfoQuery:
    id: int
    
    def __init__(self, id: int):
        self.id = id
        
class GetUserInfoQueryHandler:
    user_repository: UserRepository
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    async def handle(self, query: GetUserInfoQuery) -> GetUserInfoResponse:
        user_entity = await self.user_repository.get_by_id(id=query.id)
        if not user_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
        return GetUserInfoResponse(
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