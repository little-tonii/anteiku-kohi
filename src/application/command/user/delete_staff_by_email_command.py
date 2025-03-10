from fastapi import Depends, HTTPException
from domain.repository.user_repository import StaffRepository
from starlette import status

from infrastructure.repository_impl.user_repository_impl import StaffRepositoryImpl

class DeleteStaffByEmailCommand:
    email: str
    
    def __init__(self, email: str):
        self.email = email
        
class DeleteStaffByEmailCommandHandler:
    staff_repository: StaffRepository
    
    def __init__(self, staff_repository: StaffRepositoryImpl = Depends()):
        self.staff_repository = staff_repository
        
    async def handle(self, command: DeleteStaffByEmailCommand) -> None:
        success = await self.staff_repository.delete_by_email(email=command.email)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nhân viên không tồn tại")