from fastapi import Depends, HTTPException
from application.schema.response.user_response_schema import DeleteStaffByIdResponse
from domain.repository.user_repository import StaffRepository
from starlette import status

from infrastructure.repository_impl.user_repository_impl import StaffRepositoryImpl

class DeleteStaffByIdCommand:
    id: int
    
    def __init__(self, id: int):
        self.id = id
        
class DeleteStaffByIdCommandHandler:
    staff_repository: StaffRepository
    
    def __init__(self, staff_repository: StaffRepositoryImpl = Depends()):
        self.staff_repository = staff_repository
        
    async def handle(self, command: DeleteStaffByIdCommand) -> None:
        success = await self.staff_repository.delete_by_id(id=command.id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nhân viên không tồn tại")