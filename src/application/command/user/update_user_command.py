from typing import Optional
from fastapi import Depends, HTTPException
from application.schema.response.user_response_schema import UpdateUserResponse
from domain.repository.user_repository import UserRepository
from starlette import status

from infrastructure.repository_impl.user_repository_impl import UserRepositoryImpl

class UpdateUserCommand:
    id: int
    full_name: str | None
    phone_number: str | None
    address: str | None
    hashed_password:str | None
    refresh_token: str | None
    
    def __init__(self, id: int, full_name: Optional[str], phone_number: Optional[str], address: Optional[str], hashed_password: Optional[str], refresh_token: Optional[str]):
        self.id = id
        self.full_name = full_name
        self.phone_number = phone_number
        self.address = address
        self.hashed_password = hashed_password
        self.refresh_token = refresh_token
    
class UpdateUserCommandHandler:
    user_repository: UserRepository
    
    def __init__(self, user_repository: UserRepositoryImpl = Depends()):
        self.user_repository = user_repository
        
    async def handle(self, command: UpdateUserCommand) -> UpdateUserResponse:
        user_entity = await self.user_repository.get_by_id(id=command.id)
        if not user_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if command.full_name:
            user_entity.full_name = command.full_name
        if command.phone_number:
            user_entity.phone_number = command.phone_number
        if command.address:
            user_entity.address = command.address
        if command.hashed_password:
            user_entity.hashed_password = command.hashed_password
        if command.refresh_token:
            user_entity.refresh_token = command.refresh_token
        updated_user_entity = await self.user_repository.update(user_entity=user_entity)
        return UpdateUserResponse(
            id=updated_user_entity.id,
            full_name=updated_user_entity.full_name,
            phone_number=updated_user_entity.phone_number,
            email=updated_user_entity.email,
            address=updated_user_entity.address,
            updated_at=updated_user_entity.updated_at,
            joined_at=updated_user_entity.joined_at,
            is_active=updated_user_entity.is_active
        )