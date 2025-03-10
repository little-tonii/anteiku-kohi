from fastapi import Depends, HTTPException
from application.schema.response.user_response_schema import CreateStaffResponse
from domain.entity.user_entity import StaffEntity
from domain.repository.user_repository import StaffRepository
from starlette import status

from infrastructure.repository_impl.user_repository_impl import StaffRepositoryImpl

class CreateStaffCommand:
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
        
    
class CreateStaffCommandHandler:
    staff_repository: StaffRepository
    
    def __init__(self, staff_repository: StaffRepositoryImpl = Depends()):
        self.staff_repository = staff_repository
        
    async def handle(self, command: CreateStaffCommand) -> CreateStaffResponse:
        if await self.staff_repository.get_by_email(email=command.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email đã được sử dụng")
        staff_entity = await self.staff_repository.create(
            StaffEntity(
                full_name=command.full_name,
                phone_number=command.phone_number,
                email=command.email,
                address=command.address,
                hashed_password=command.hashed_password
            )
        )
        return CreateStaffResponse(
            id=staff_entity.id,
            full_name=staff_entity.full_name,
            phone_number=staff_entity.phone_number,
            email=staff_entity.email,
            address=staff_entity.address,
            updated_at=staff_entity.updated_at,
            joined_at=staff_entity.joined_at,
            is_active=staff_entity.is_active
        )