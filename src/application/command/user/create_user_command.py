from fastapi import Depends, HTTPException
from application.schema.response.user_response_schema import CreateUserResponse
from domain.entity.user_entity import UserEntity
from domain.repository.user_repository import UserRepository
from starlette import status

from infrastructure.repository_impl.user_repository_impl import UserRepositoryImpl

class CreateUserCommand:
    full_name: str
    phone_number: str
    email: str
    address: str
    hashed_password: str
    
    def __init__(self, full_name: str, phone_number: str, email: str, address: str, hashed_password: str):
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.hashed_password = hashed_password
        
    
class CreateUserCommandHandler:
    user_repository: UserRepository
    
    def __init__(self, user_repository: UserRepositoryImpl = Depends()):
        self.user_repository = user_repository
        
    async def handle(self, command: CreateUserCommand) -> CreateUserResponse:
        if await self.user_repository.get_by_email(email=command.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email đã được sử dụng")
        user_entity = await self.user_repository.create(
            UserEntity(
                full_name=command.full_name,
                phone_number=command.phone_number,
                email=command.email,
                address=command.address,
                hashed_password=command.hashed_password
            )
        )
        return CreateUserResponse(
            id=user_entity.id,
            full_name=user_entity.full_name,
            phone_number=user_entity.phone_number,
            email=user_entity.email,
            address=user_entity.address,
            updated_at=user_entity.updated_at,
            joined_at=user_entity.joined_at,
            is_active=user_entity.is_active
        )