from fastapi import HTTPException
from application.schema.response.staff_response_schema import GetStaffByIdResponse
from domain.entity.staff_entity import StaffEntity
from domain.repository.staff_repository import StaffRepository
from starlette import status

class GetStaffByIdQuery:
    id: int
    
    def __init__(self, id: str):
        self.id = id
        
class GetStaffByIdQueryHandler:
    staff_repository: StaffRepository
    
    def __init__(self, staff_repository: StaffRepository):
        self.staff_repository = staff_repository
        
    async def handle(self, query: GetStaffByIdQuery) -> GetStaffByIdResponse:
        staff_entity = await self.staff_repository.get_by_id(id=query.id)
        if not staff_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nhân viên không tồn tại")
        return GetStaffByIdResponse(
            id=staff_entity.id,
            full_name=staff_entity.full_name,
            phone_number=staff_entity.phone_number,
            email=staff_entity.email,
            address=staff_entity.address,
            updated_at=staff_entity.updated_at,
            joined_at=staff_entity.joined_at,
            is_active=staff_entity.is_active
        )