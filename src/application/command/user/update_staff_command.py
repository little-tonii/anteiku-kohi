from typing import Optional
from fastapi import Depends, HTTPException
from application.schema.response.user_response_schema import UpdateStaffResponse
from domain.repository.user_repository import StaffRepository
from starlette import status

from infrastructure.repository_impl.user_repository_impl import StaffRepositoryImpl

class UpdateStaffCommand:
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
    
class UpdateStaffCommandHandler:
    staff_repository: StaffRepository
    
    def __init__(self, staff_repository: StaffRepositoryImpl = Depends()):
        self.staff_repository = staff_repository
        
    async def handle(self, command: UpdateStaffCommand) -> UpdateStaffResponse:
        staff_entity = await self.staff_repository.get_by_id(id=command.id)
        if not staff_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if command.full_name:
            staff_entity.full_name = command.full_name
        if command.phone_number:
            staff_entity.phone_number = command.phone_number
        if command.address:
            staff_entity.address = command.address
        if command.hashed_password:
            staff_entity.hashed_password = command.hashed_password
        if command.refresh_token:
            staff_entity.refresh_token = command.refresh_token
        updated_staff_entity = await self.staff_repository.update(staff_entity=staff_entity)
        return UpdateStaffResponse(
            id=updated_staff_entity.id,
            full_name=updated_staff_entity.full_name,
            phone_number=updated_staff_entity.phone_number,
            email=updated_staff_entity.email,
            address=updated_staff_entity.address,
            updated_at=updated_staff_entity.updated_at,
            joined_at=updated_staff_entity.joined_at,
            is_active=updated_staff_entity.is_active
        )