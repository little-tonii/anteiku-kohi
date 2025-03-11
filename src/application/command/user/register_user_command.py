from fastapi import HTTPException
from ....application.schema.response.user_response_schema import RegisterUserResponse
from ....domain.entity.user_entity import UserEntity
from ....domain.repository.user_repository import UserRepository
from ....infrastructure.repository_impl.user_repository_impl import UserRepositoryImpl
from ....infrastructure.config.security import bcrypt_context
from starlette import status

class RegisterUserCommand:
    full_name: str
    phone_number: str
    email: str
    address: str
    password: str
    
    def __init__(self, full_name: str, phone_number: str, address: str, email: str, password: str):
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.password = password
        
    
class RegisterUserCommandHandler:
    user_repository: UserRepository
    
    def __init__(self, user_repository: UserRepositoryImpl):
        self.user_repository = user_repository
        
    async def handle(self, command: RegisterUserCommand) -> RegisterUserResponse:
        if await self.user_repository.get_by_email(email=command.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email đã được sử dụng")
        created_user = await self.user_repository.create(
            full_name=command.full_name,
            phone_number=command.phone_number,
            email=command.email,
            address=command.address,
            hashed_password=bcrypt_context.hash(command.password)
        )
        return RegisterUserResponse(
            id=created_user.id,
            full_name=created_user.full_name,
            phone_number=created_user.phone_number,
            email=created_user.email,
            address=created_user.address,
            updated_at=created_user.updated_at,
            joined_at=created_user.joined_at,
            is_active=created_user.is_active,
            role=created_user.role
        )
        